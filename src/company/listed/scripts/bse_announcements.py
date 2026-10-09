#!/usr/bin/env python3
"""
bse_announcements.py
Fetch corporate announcements and regulatory filings from BSE India (Mainboard and BSE SME).

Supports:
- Ticker symbol or 6-digit scrip code resolution using bse_stocks.csv
- Unified support for all BSE groups: Group A (Large Cap), Group B, Group M/MT (BSE SME)
- Automatic chunking for date ranges > 365 days (bypassing BSE's 365-day single-query limit)
- Automatic pagination across 50-record pages
- Server-side and client-side Order wins filtering (--orders-only)
- Material events filter (--material-only)
- Category and keyword filtering
- PDF attachment downloading from BSE archives (AttachLive)
- Auto-conversion of downloaded PDFs to Markdown via pdf_to_markdown.py
- CSV and JSON exports

Usage Examples:
    .venv/bin/python src/company/listed/scripts/bse_announcements.py BEL --orders-only
    .venv/bin/python src/company/listed/scripts/bse_announcements.py LT --from-date 01-01-2024 --to-date 01-10-2026 --orders-only
    .venv/bin/python src/company/listed/scripts/bse_announcements.py MACFOS --limit 10
    .venv/bin/python src/company/listed/scripts/bse_announcements.py 500002 --material-only
    .venv/bin/python src/company/listed/scripts/bse_announcements.py BEL --orders-only --download 2 --convert-md
"""

from __future__ import annotations

import argparse
import math
import os
import re
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

# Ensure repository root is in sys.path
REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

try:
    from curl_cffi import requests as cffi_requests
except ImportError:
    print(
        "Error: 'curl_cffi' is required to bypass BSE WAF protection.\n"
        "Install it in .venv via: .venv/bin/pip install curl_cffi pandas",
        file=sys.stderr,
    )
    sys.exit(1)

import pandas as pd


# ── Stock Dictionary Loader ───────────────────────────────────────────────────

def get_bse_stocks_mapping() -> tuple[dict[str, int], dict[int, str]]:
    """
    Load mapping of Ticker / Security ID <-> Security Code from bse_stocks.csv.
    Returns (ticker_to_code, code_to_ticker).
    """
    possible_paths = [
        REPO_ROOT / "data" / "bse_stocks.csv",
        Path.cwd() / "data" / "bse_stocks.csv",
    ]
    csv_path = next((p for p in possible_paths if p.exists()), None)
    if not csv_path:
        return {}, {}

    try:
        df = pd.read_csv(csv_path, usecols=range(9))
        df["Security Code"] = pd.to_numeric(df["Security Code"], errors="coerce")
        df = df.dropna(subset=["Security Code"])
        df["Security Code"] = df["Security Code"].astype(int)
        df["Security Id"] = df["Security Id"].astype(str).str.strip().str.upper()

        ticker_to_code = dict(zip(df["Security Id"], df["Security Code"]))
        code_to_ticker = dict(zip(df["Security Code"], df["Security Id"]))
        return ticker_to_code, code_to_ticker
    except Exception:
        return {}, {}


# ── Output Path Resolver ──────────────────────────────────────────────────────

def resolve_output_dir(ticker: str, company_name: str | None = None, custom_dir: str | Path | None = None) -> Path:
    """Resolve destination directory under tmp/company/listed/<company-folder>/announcements/."""
    if custom_dir:
        p = Path(custom_dir)
        p.mkdir(parents=True, exist_ok=True)
        return p

    base_dir = REPO_ROOT / "tmp" / "company" / "listed"
    base_dir.mkdir(parents=True, exist_ok=True)

    ticker_clean = ticker.lower().strip()
    clean_name = re.sub(r"[^\w\s-]", "", company_name or ticker)
    slug = re.sub(r"[-\s]+", "-", clean_name).strip("-").lower()
    noise = {"ltd", "limited", "india", "pvt", "corp", "corporation", "industries", "technologies", "co"}
    comp_words = [w for w in re.findall(r"\w+", clean_name.lower()) if w not in noise]

    existing_dirs = [d for d in base_dir.iterdir() if d.is_dir()]
    for d in existing_dirs:
        dname = d.name.lower()
        if dname == slug or dname == ticker_clean:
            target = d / "announcements"
            target.mkdir(parents=True, exist_ok=True)
            return target
        d_tokens = re.findall(r"\w+", dname)
        if ticker_clean in d_tokens:
            target = d / "announcements"
            target.mkdir(parents=True, exist_ok=True)
            return target
        if comp_words and all(w in dname for w in comp_words):
            target = d / "announcements"
            target.mkdir(parents=True, exist_ok=True)
            return target

    target = base_dir / (slug or ticker_clean) / "announcements"
    target.mkdir(parents=True, exist_ok=True)
    return target


# ── BSE Client Class ─────────────────────────────────────────────────────────

class BSEAnnouncementsClient:
    """Thread-safe client to fetch corporate announcements from BSE India."""

    API_URL = "https://api.bseindia.com/BseIndiaAPI/api/AnnSubCategoryGetData/w"
    PDF_LIVE_URL = "https://www.bseindia.com/xml-data/corpfiling/AttachLive/{}"
    PDF_HIS_URL = "https://www.bseindia.com/xml-data/corpfiling/AttachHis/{}"

    # Routine categories to exclude when --material-only is specified
    NOISE_SUBCATEGORIES = {
        "Closure of Trading Window",
        "Loss of Share Certificates",
        "Loss of Share Certificate / Issue of Duplicate Share Certificate",
        "Duplicate Share Certificate",
        "Issue of Duplicate Share Certificate",
        "Newspaper Publication",
        "Newspaper Clippings",
    }

    def __init__(self, impersonate: str = "chrome120"):
        self.impersonate = impersonate
        self.session = cffi_requests.Session(impersonate=self.impersonate)
        self.session.headers.update({
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "origin": "https://www.bseindia.com",
            "referer": "https://www.bseindia.com/",
            "user-agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
        })
        self.ticker_to_code, self.code_to_ticker = get_bse_stocks_mapping()

    def resolve_scrip(self, symbol_or_code: str | int) -> tuple[int, str]:
        """
        Resolve symbol string or numeric code to (scrip_code: int, ticker_symbol: str).
        Supports Security Id (e.g. 'ROBU', 'BEL'), Scrip Code ('543787'), or Issuer Name substring ('Macfos').
        """
        val_str = str(symbol_or_code).strip().upper()
        if val_str.isdigit():
            code = int(val_str)
            ticker = self.code_to_ticker.get(code, str(code))
            return code, ticker

        # Exact match on Security Id
        if val_str in self.ticker_to_code:
            return self.ticker_to_code[val_str], val_str

        # Fallback: Search in bse_stocks.csv for Issuer Name match
        possible_paths = [
            REPO_ROOT / "data" / "bse_stocks.csv",
            Path.cwd() / "data" / "bse_stocks.csv",
        ]
        csv_path = next((p for p in possible_paths if p.exists()), None)
        if csv_path:
            try:
                df = pd.read_csv(csv_path, usecols=range(9))
                # Match start of name or exact word
                matches = df[df["Issuer Name"].astype(str).str.upper().str.contains(r"\b" + re.escape(val_str) + r"\b", regex=True, na=False)]
                if matches.empty:
                    matches = df[df["Issuer Name"].astype(str).str.upper().str.contains(re.escape(val_str), na=False)]
                if not matches.empty:
                    row = matches.iloc[0]
                    scrip = int(row["Security Code"])
                    sec_id = str(row["Security Id"]).strip().upper()
                    return scrip, sec_id
            except Exception:
                pass

        raise ValueError(
            f"Could not resolve BSE security '{symbol_or_code}'. Provide a valid ticker or 6-digit scrip code."
        )

    def _fetch_window(
        self,
        scrip_code: int,
        from_str: str,
        to_str: str,
        category: str | int = -1,
        subcategory: str | int = -1,
        max_retries: int = 3,
        timeout: int = 15,
    ) -> list[dict]:
        """
        Fetch announcements for a single window (max 365 days) across all pages.
        """
        records: list[dict] = []
        page = 1

        while True:
            params = {
                "pageno": page,
                "strCat": category,
                "strPrevDate": from_str,
                "strScrip": scrip_code,
                "strSearch": "P",
                "strToDate": to_str,
                "strType": "C",
                "subcategory": subcategory,
            }

            for attempt in range(1, max_retries + 1):
                try:
                    resp = self.session.get(self.API_URL, params=params, timeout=timeout)
                    resp.raise_for_status()
                    data = resp.json()
                    break
                except Exception as e:
                    if attempt == max_retries:
                        print(f"Warning: Failed to fetch page {page} for window {from_str}-{to_str}: {e}", file=sys.stderr)
                        return records
                    time.sleep(0.5 * attempt)

            table = data.get("Table", [])
            if not table:
                break

            records.extend(table)
            row_cnt = data.get("Table1", [{}])[0].get("ROWCNT") or 0

            if len(records) >= row_cnt or len(table) < 50:
                break

            page += 1

        return records

    def get_announcements(
        self,
        symbol_or_code: str | int,
        from_date: str | datetime | None = None,
        to_date: str | datetime | None = None,
        category: str | int = -1,
        subcategory: str | int = -1,
        orders_only: bool = False,
    ) -> pd.DataFrame:
        """
        Fetch corporate announcements for any BSE security.
        Automatically splits ranges > 365 days into 365-day chunks to prevent BSE silent failure.

        Args:
            symbol_or_code: Ticker symbol (e.g. 'BEL', 'LT') or 6-digit code (e.g. 500510).
            from_date: Start date string ('DD-MM-YYYY' or 'YYYYMMDD') or datetime. Default: 365 days ago.
            to_date: End date string ('DD-MM-YYYY' or 'YYYYMMDD') or datetime. Default: today.
            category: Top-level category string or -1.
            subcategory: Subcategory string or -1.
            orders_only: If True, automatically filters for 'Award of Order / Receipt of Order'.

        Returns:
            pd.DataFrame sorted newest first.
        """
        scrip_code, ticker_sym = self.resolve_scrip_code_and_ticker(symbol_or_code)

        # Parse date parameters
        today = datetime.today()
        start_dt = self._parse_date(from_date, default=today - timedelta(days=365))
        end_dt = self._parse_date(to_date, default=today)

        if start_dt > end_dt:
            start_dt, end_dt = end_dt, start_dt

        # If orders_only is set, configure BSE server-side filter
        if orders_only:
            category = "Company Update"
            subcategory = "Award of Order / Receipt of Order"

        # Generate chunk intervals of at most 365 days each
        intervals: list[tuple[datetime, datetime]] = []
        cur_start = start_dt
        while cur_start < end_dt:
            cur_end = min(cur_start + timedelta(days=364), end_dt)
            intervals.append((cur_start, cur_end))
            cur_start = cur_end + timedelta(days=1)

        raw_records: list[dict] = []
        for c_start, c_end in intervals:
            f_str = c_start.strftime("%Y%m%d")
            t_str = c_end.strftime("%Y%m%d")
            chunk_records = self._fetch_window(
                scrip_code=scrip_code,
                from_str=f_str,
                to_str=t_str,
                category=category,
                subcategory=subcategory,
            )
            raw_records.extend(chunk_records)

        if not raw_records:
            return pd.DataFrame()

        df = pd.DataFrame(raw_records)

        # Deduplicate records by NEWSID if overlapping
        if "NEWSID" in df.columns:
            df = df.drop_duplicates(subset=["NEWSID"])

        return self._normalize_dataframe(df, ticker_sym=ticker_sym)

    def resolve_scrip_code_and_ticker(self, symbol_or_code: str | int) -> tuple[int, str]:
        return self.resolve_scrip(symbol_or_code)

    def _normalize_dataframe(self, df: pd.DataFrame, ticker_sym: str) -> pd.DataFrame:
        """Map raw BSE fields to clean normalized columns while retaining all raw fields."""
        if df.empty:
            return df

        col_map = {
            "SCRIP_CD": "scrip_code",
            "SLONGNAME": "company_name",
            "CATEGORYNAME": "category",
            "SUBCATNAME": "subcategory",
            "HEADLINE": "headline",
            "NEWSSUB": "description",
            "DT_TM": "announcement_time",
            "DissemDT": "dissemination_time",
            "TimeDiff": "dissemination_diff",
            "CRITICALNEWS": "is_critical",
            "PDFFLAG": "has_pdf",
            "ATTACHMENTNAME": "attachment_file",
            "Fld_Attachsize": "attachment_size",
            "NSURL": "bse_url",
            "NEWSID": "news_id",
            "XML_NAME": "xml_name",
            "NEWS_DT": "news_dt",
            "AGENDA_ID": "agenda_id",
            "News_submission_dt": "submission_time",
        }
        normalized = df.rename(columns=col_map).copy()
        normalized["symbol"] = ticker_sym

        # Parse timestamp
        if "announcement_time" in normalized.columns:
            normalized["timestamp"] = pd.to_datetime(normalized["announcement_time"], errors="coerce")
            normalized = normalized.sort_values("timestamp", ascending=False).reset_index(drop=True)

        # Construct full download URL for PDF
        if "attachment_file" in normalized.columns:
            normalized["attachment_url"] = normalized["attachment_file"].apply(
                lambda x: self.PDF_LIVE_URL.format(x.strip())
                if isinstance(x, str) and x.strip() and x.strip().endswith(".pdf")
                else None
            )

        return normalized

    @staticmethod
    def _parse_date(d_val: str | datetime | None, default: datetime) -> datetime:
        if d_val is None:
            return default
        if isinstance(d_val, datetime):
            return d_val
        s = str(d_val).strip()
        for fmt in ["%d-%m-%Y", "%Y%m%d", "%Y-%m-%d", "%d/%m/%Y"]:
            try:
                return datetime.strptime(s, fmt)
            except ValueError:
                pass
        return default

    @classmethod
    def filter_material(cls, df: pd.DataFrame) -> pd.DataFrame:
        """Filter out routine secretarial noise (trading window closures, lost certificates)."""
        if df.empty:
            return df
        mask = ~df["subcategory"].isin(cls.NOISE_SUBCATEGORIES)
        return df[mask].reset_index(drop=True)

    @staticmethod
    def filter_keyword(df: pd.DataFrame, keyword: str) -> pd.DataFrame:
        """Search for keyword in headline, category, or description."""
        if df.empty:
            return df
        pat = keyword.strip()
        mask = (
            df["headline"].astype(str).str.contains(pat, case=False, na=False)
            | df["description"].astype(str).str.contains(pat, case=False, na=False)
            | df["subcategory"].astype(str).str.contains(pat, case=False, na=False)
        )
        return df[mask].reset_index(drop=True)

    def download_attachment(self, url: str, dest_dir: Path, filename: str | None = None) -> Path | None:
        """Download an attachment PDF from BSE to dest_dir."""
        if not url or not str(url).startswith("http"):
            return None

        dest_dir.mkdir(parents=True, exist_ok=True)
        if not filename:
            filename = url.rstrip("/").split("/")[-1]
            if not filename.endswith(".pdf"):
                filename += ".pdf"

        clean_name = re.sub(r'[\\/*?:"<>|]', "_", filename)
        target = dest_dir / clean_name

        for target_url in [url, url.replace("/AttachLive/", "/AttachHis/")]:
            try:
                resp = self.session.get(target_url, timeout=30)
                if resp.status_code == 200 and resp.content.startswith(b"%PDF"):
                    target.write_bytes(resp.content)
                    return target
            except Exception:
                continue

        print(f"Failed to download PDF from {url}", file=sys.stderr)
        return None


# ── CLI Interface ─────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch official corporate announcements & filings from BSE India (Mainboard & SME).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "symbol",
        type=str,
        help="BSE stock ticker (e.g. BEL, LT, MACFOS) or 6-digit scrip code (e.g. 500049, 500510)",
    )
    parser.add_argument("--from-date", type=str, default=None, help="Start date (DD-MM-YYYY or YYYYMMDD)")
    parser.add_argument("--to-date", type=str, default=None, help="End date (DD-MM-YYYY or YYYYMMDD)")
    parser.add_argument(
        "--orders-only",
        action="store_true",
        help="Filter strictly for order receipts and contract awards",
    )
    parser.add_argument(
        "--material-only",
        action="store_true",
        help="Exclude routine noise (lost certificates, trading window notices)",
    )
    parser.add_argument("--category", type=str, default=-1, help="BSE category filter (e.g. 'Company Update', 'Result')")
    parser.add_argument("--subcategory", type=str, default=-1, help="BSE subcategory filter (e.g. 'Financial Results')")
    parser.add_argument("--keyword", type=str, default=None, help="Search for keyword in headline/description")
    parser.add_argument(
        "--limit",
        type=int,
        default=15,
        help="Number of records to display in terminal preview (default: 15, 0 for all)",
    )
    parser.add_argument(
        "--download",
        type=str,
        default=None,
        metavar="N",
        help="Download latest N matching PDF attachments (e.g. 5 or 'all')",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Directory to save downloads and exported data (default: tmp/company/listed/<company-folder>/announcements)",
    )
    parser.add_argument("--csv", action="store_true", help="Save results to a CSV file in output-dir")
    parser.add_argument("--json", action="store_true", help="Save results to a JSON file in output-dir")
    parser.add_argument(
        "--convert-md",
        action="store_true",
        help="Auto-convert downloaded PDFs to Markdown using pdf_to_markdown.py",
    )

    args = parser.parse_args()

    client = BSEAnnouncementsClient()
    try:
        scrip_code, ticker_sym = client.resolve_scrip(args.symbol)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Fetching announcements for '{ticker_sym}' (Scrip: {scrip_code}) from BSE...")
    df = client.get_announcements(
        symbol_or_code=scrip_code,
        from_date=args.from_date,
        to_date=args.to_date,
        category=args.category,
        subcategory=args.subcategory,
        orders_only=args.orders_only,
    )

    if df.empty:
        print(f"No announcements found for '{ticker_sym}' in the specified date range.")
        sys.exit(0)

    total_fetched = len(df)
    company_name = df["company_name"].iloc[0] if "company_name" in df.columns else ticker_sym

    output_dir = resolve_output_dir(ticker_sym, company_name=company_name, custom_dir=args.output_dir)

    # Apply client-side filters
    if args.material_only:
        df = client.filter_material(df)
    if args.keyword:
        df = client.filter_keyword(df, args.keyword)

    filtered_count = len(df)
    print(f"\nCompany:  {company_name} ({ticker_sym} | BSE: {scrip_code})")
    print(f"Total:    {total_fetched} filings fetched -> {filtered_count} matching filter criteria")
    print(f"Output:   {output_dir}")

    if df.empty:
        print("No records matched your filter criteria.")
        sys.exit(0)

    # Preview table
    preview_limit = len(df) if args.limit == 0 else min(args.limit, len(df))
    print(f"\n--- Preview of Latest {preview_limit} Filings ---")
    for i, (_, row) in enumerate(df.head(preview_limit).iterrows(), 1):
        dt = str(row.get("announcement_time", "")).replace("T", " ")
        cat = row.get("category", "")
        subcat = row.get("subcategory", "")
        hl = (row.get("headline", "") or "").replace("\n", " ").strip()
        if len(hl) > 130:
            hl = hl[:127] + "..."
        pdf = row.get("attachment_url") or "None"
        print(f"\n[{i}] {dt} | {cat} -> {subcat}")
        print(f"    Headline: {hl}")
        if pdf and pdf != "None":
            print(f"    Filing:   {pdf}")

    # Export CSV / JSON
    output_dir.mkdir(parents=True, exist_ok=True)
    if args.csv:
        csv_file = output_dir / f"{ticker_sym}_bse_announcements.csv"
        df.to_csv(csv_file, index=False)
        print(f"\nExported {len(df)} records to CSV: {csv_file}")

    if args.json:
        json_file = output_dir / f"{ticker_sym}_bse_announcements.json"
        df.to_json(json_file, orient="records", date_format="iso", indent=2)
        print(f"Exported {len(df)} records to JSON: {json_file}")

    # Handle PDF Downloads
    if args.download:
        dl_arg = args.download.strip().lower()
        num_dl = len(df) if dl_arg == "all" else int(dl_arg)
        valid_files = df[df["attachment_url"].notna() & df["attachment_url"].str.startswith("http")].head(num_dl)
        print(f"\nDownloading {len(valid_files)} PDF filings to: {output_dir}")

        for idx, (_, row) in enumerate(valid_files.iterrows(), 1):
            url = row["attachment_url"]
            dt_str = str(row.get("announcement_time", "")).split("T")[0].replace("-", "")
            subcat_slug = re.sub(r"[^\w]+", "_", str(row.get("subcategory", "")))[:25].strip("_")
            custom_name = f"{ticker_sym}_{dt_str}_{subcat_slug}_{idx}.pdf"
            saved_path = client.download_attachment(url, dest_dir=output_dir, filename=custom_name)
            if saved_path:
                print(f"  [{idx}/{len(valid_files)}] Downloaded: {saved_path.name}")
                if args.convert_md:
                    try:
                        from src.common.scripts.pdf_to_markdown import convert_pdf_to_markdown
                        convert_pdf_to_markdown(saved_path, delete_original=False)
                    except Exception as e:
                        print(f"  Warning: Failed to convert {saved_path.name} to Markdown: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
