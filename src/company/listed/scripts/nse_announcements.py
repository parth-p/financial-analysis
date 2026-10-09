#!/usr/bin/env python3
"""
nse_announcements.py
Fetch corporate announcements and regulatory filings from NSE India (Mainboard and SME).

Supports:
- Automatic segment detection (Mainboard 'equities' vs SME 'sme')
- Order wins & contract receipts filtering (--orders-only)
- Material event filtering (--material-only)
- Keyword and category searching
- Date range filtering (DD-MM-YYYY)
- Direct PDF attachment downloading from NSE archives
- Auto-conversion of downloaded PDFs to Markdown via pdf_to_markdown.py
- Exporting to CSV / JSON

Usage Examples:
    .venv/bin/python src/company/listed/scripts/nse_announcements.py TCS
    .venv/bin/python src/company/listed/scripts/nse_announcements.py LT --orders-only
    .venv/bin/python src/company/listed/scripts/nse_announcements.py NMSTEEL --limit 10
    .venv/bin/python src/company/listed/scripts/nse_announcements.py RVNL --orders-only --download 3
    .venv/bin/python src/company/listed/scripts/nse_announcements.py INFY --from-date 01-01-2026 --material-only --csv
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

# Ensure repository root is in sys.path
REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

try:
    from curl_cffi import requests as cffi_requests
except ImportError:
    print(
        "Error: 'curl_cffi' is required to bypass NSE Akamai bot protection.\n"
        "Install it in .venv via: .venv/bin/pip install curl_cffi pandas",
        file=sys.stderr,
    )
    sys.exit(1)

import pandas as pd


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


# ── Client Class ─────────────────────────────────────────────────────────────

class NSEAnnouncementsClient:
    """Thread-safe client to fetch corporate announcements from NSE India."""

    BASE_URL = "https://www.nseindia.com"
    API_URL = "https://www.nseindia.com/api/corporate-announcements"

    # Routine secretarial categories to exclude when --material-only is specified
    NOISE_CATEGORIES = {
        "Loss of Share Certificates",
        "Loss of Share Certificate / Issue of Duplicate Share Certificate",
        "Duplicate Share Certificate",
        "Issue of Duplicate Share Certificate",
        "Trading Window",
        "Closure of Trading Window",
        "Copy of Newspaper Publication",
        "Newspaper Publication",
        "Newspaper Clippings",
    }

    def __init__(self, impersonate: str = "chrome120"):
        self.impersonate = impersonate
        self.session = None
        self._init_session()

    def _init_session(self) -> None:
        """Establish session cookies by visiting the NSE homepage with browser TLS fingerprint."""
        self.session = cffi_requests.Session(impersonate=self.impersonate)
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
        }
        self.session.headers.update(headers)
        try:
            resp = self.session.get(self.BASE_URL, timeout=12)
            resp.raise_for_status()
            time.sleep(0.3)
            self.session.headers.update({
                "Accept": "application/json, text/plain, */*",
                "Referer": "https://www.nseindia.com/companies-listing/corporate-filings-announcements",
            })
        except Exception:
            pass

    def _normalize_dataframe(self, df: pd.DataFrame, segment: str) -> pd.DataFrame:
        """Normalize raw NSE payload columns into clean, consistent fields."""
        if df.empty:
            return df

        col_map = {
            "symbol": "symbol",
            "sm_name": "company_name",
            "sm_isin": "isin",
            "smIndustry": "industry",
            "desc": "category",
            "attchmntText": "description",
            "attchmntFile": "attachment_url",
            "fileSize": "attachment_size",
            "an_dt": "announcement_time",
            "sort_date": "sort_date",
            "exchdisstime": "dissemination_time",
            "difference": "dissemination_diff",
            "hasXbrl": "has_xbrl",
            "seq_id": "seq_id",
        }
        # Rename known keys to friendly names while preserving ALL other fields
        normalized = df.rename(columns=col_map).copy()
        normalized["segment"] = segment

        # Parse timestamp
        if "sort_date" in normalized.columns:
            normalized["timestamp"] = pd.to_datetime(normalized["sort_date"], errors="coerce")
            normalized = normalized.sort_values("timestamp", ascending=False).reset_index(drop=True)
        elif "announcement_time" in normalized.columns:
            normalized["timestamp"] = pd.to_datetime(
                normalized["announcement_time"], format="%d-%b-%Y %H:%M:%S", errors="coerce"
            )
            normalized = normalized.sort_values("timestamp", ascending=False).reset_index(drop=True)

        return normalized

    def get_announcements(
        self,
        symbol: str,
        from_date: str | None = None,
        to_date: str | None = None,
        segment: str = "auto",
        max_retries: int = 3,
        timeout: int = 15,
    ) -> pd.DataFrame:
        """
        Fetch corporate announcements for a company.

        Args:
            symbol: NSE symbol (e.g. 'LT', 'TCS', 'NMSTEEL').
            from_date: Start date string 'DD-MM-YYYY'. Optional.
            to_date: End date string 'DD-MM-YYYY'. Optional.
            segment: 'auto' (checks equities then sme), 'equities' (Mainboard), or 'sme'.
            max_retries: Retry attempts on session disconnect.
            timeout: HTTP request timeout.

        Returns:
            pd.DataFrame containing all announcements.
        """
        clean_symbol = symbol.strip().upper()
        segments_to_try = ["equities", "sme"] if segment == "auto" else [segment]

        for seg in segments_to_try:
            params = {
                "index": seg,
                "symbol": clean_symbol,
            }
            if from_date:
                params["from_date"] = from_date.strip()
            if to_date:
                params["to_date"] = to_date.strip()

            for attempt in range(1, max_retries + 1):
                try:
                    resp = self.session.get(self.API_URL, params=params, timeout=timeout)
                    if resp.status_code in (401, 403):
                        time.sleep(0.5)
                        self._init_session()
                        resp = self.session.get(self.API_URL, params=params, timeout=timeout)

                    if resp.status_code == 404:
                        break

                    resp.raise_for_status()
                    data = resp.json()

                    if isinstance(data, list) and len(data) > 0:
                        df = pd.DataFrame(data)
                        return self._normalize_dataframe(df, segment=seg)

                    # If empty list, break out to try next segment (e.g. sme)
                    if isinstance(data, list) and len(data) == 0:
                        break

                except Exception:
                    if attempt == max_retries:
                        break
                    time.sleep(0.5 * attempt)

        return pd.DataFrame()

    @staticmethod
    def filter_orders(df: pd.DataFrame) -> pd.DataFrame:
        """
        Filter DataFrame for order receipts, contract awards, LoA, and commercial wins.
        Matches official SEBI Regulation 30 category and broad keywords.
        """
        if df.empty:
            return df

        cat_match = df["category"] == "Bagging/Receiving of orders/contracts"
        keyword_pat = r"\b(?:order|contract|award|awarded|bagged|bagging|letter of award|letter of acceptance|loa|loi|purchase order|work order)\b"
        text_match = df["description"].str.contains(keyword_pat, case=False, na=False)
        subject_match = df["category"].str.contains(keyword_pat, case=False, na=False)

        # Exclude administrative orders / tax demand orders
        neg_pat = r"\b(?:order passed|penalty|assessment order|tribunal|quash|stay order|demand order)\b"
        neg_match = (
            df["description"].str.contains(neg_pat, case=False, na=False)
            & ~cat_match
        )

        mask = (cat_match | text_match | subject_match) & ~neg_match
        return df[mask].reset_index(drop=True)

    @classmethod
    def filter_material(cls, df: pd.DataFrame) -> pd.DataFrame:
        """Filter out routine secretarial noise (lost certificates, trading window closures)."""
        if df.empty:
            return df
        mask = ~df["category"].isin(cls.NOISE_CATEGORIES)
        return df[mask].reset_index(drop=True)

    @staticmethod
    def filter_keyword(df: pd.DataFrame, keyword: str) -> pd.DataFrame:
        """Filter announcements matching a keyword or regular expression."""
        if df.empty:
            return df
        pat = keyword.strip()
        mask = (
            df["category"].str.contains(pat, case=False, na=False)
            | df["description"].str.contains(pat, case=False, na=False)
        )
        return df[mask].reset_index(drop=True)

    def download_attachment(self, url: str, dest_dir: Path, filename: str | None = None) -> Path | None:
        """Download an attachment PDF file from nsearchives to dest_dir."""
        if not url or not str(url).startswith("http") or str(url).rstrip("/").endswith("-"):
            return None

        dest_dir.mkdir(parents=True, exist_ok=True)
        if not filename:
            filename = url.rstrip("/").split("/")[-1]
            if not filename.endswith(".pdf"):
                filename += ".pdf"

        # Sanitize filename
        clean_name = re.sub(r'[\\/*?:"<>|]', "_", filename)
        target = dest_dir / clean_name

        try:
            resp = self.session.get(url, timeout=30)
            resp.raise_for_status()
            target.write_bytes(resp.content)
            return target
        except Exception as e:
            print(f"Failed to download {url}: {e}", file=sys.stderr)
            return None


# ── CLI Interface ─────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch official corporate announcements & filings from NSE India (Mainboard & SME).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("symbol", type=str, help="NSE stock ticker symbol (e.g. LT, TCS, RVNL, NMSTEEL)")
    parser.add_argument("--from-date", type=str, default=None, help="Start date filter 'DD-MM-YYYY'")
    parser.add_argument("--to-date", type=str, default=None, help="End date filter 'DD-MM-YYYY'")
    parser.add_argument(
        "--segment",
        type=str,
        default="auto",
        choices=["auto", "equities", "sme"],
        help="Market segment (default: auto detects Mainboard or SME)",
    )
    parser.add_argument(
        "--orders-only",
        action="store_true",
        help="Filter strictly for order receipts, contract wins, and LoAs",
    )
    parser.add_argument(
        "--material-only",
        action="store_true",
        help="Exclude routine noise (lost certificates, trading window notices)",
    )
    parser.add_argument(
        "--category",
        type=str,
        default=None,
        help="Filter for a specific category (e.g. 'Press Release', 'Outcome of Board Meeting')",
    )
    parser.add_argument(
        "--keyword",
        type=str,
        default=None,
        help="Search for a specific keyword in subject/description",
    )
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
    sym = args.symbol.strip().upper()

    client = NSEAnnouncementsClient()
    print(f"Fetching announcements for '{sym}' from NSE...")
    df = client.get_announcements(
        symbol=sym,
        from_date=args.from_date,
        to_date=args.to_date,
        segment=args.segment,
    )

    if df.empty:
        print(f"No announcements found for symbol '{sym}'. Check if symbol is correct.")
        sys.exit(0)

    total_fetched = len(df)
    detected_segment = df["segment"].iloc[0] if "segment" in df.columns else "unknown"
    company_name = df["company_name"].iloc[0] if "company_name" in df.columns else sym

    output_dir = resolve_output_dir(sym, company_name=company_name, custom_dir=args.output_dir)

    # Apply filters
    if args.orders_only:
        df = client.filter_orders(df)
    if args.material_only:
        df = client.filter_material(df)
    if args.category:
        df = client.filter_keyword(df, args.category)
    if args.keyword:
        df = client.filter_keyword(df, args.keyword)

    filtered_count = len(df)
    print(f"\nCompany:  {company_name} ({sym})")
    print(f"Segment:  {detected_segment.upper()}")
    print(f"Total:    {total_fetched} historical filings fetched -> {filtered_count} matching filter criteria")
    print(f"Output:   {output_dir}")

    if df.empty:
        print("No records matched your filter criteria.")
        sys.exit(0)

    # Display preview table
    display_cols = ["announcement_time", "category", "description"]
    cols = [c for c in display_cols if c in df.columns]
    preview_limit = len(df) if args.limit == 0 else min(args.limit, len(df))

    print(f"\n--- Preview of Latest {preview_limit} Filings ---")
    for i, (_, row) in enumerate(df.head(preview_limit).iterrows(), 1):
        dt = row.get("announcement_time", "")
        cat = row.get("category", "")
        desc = (row.get("description", "") or "").replace("\n", " ").strip()
        if len(desc) > 130:
            desc = desc[:127] + "..."
        pdf = row.get("attachment_url") or "None"
        print(f"\n[{i}] {dt} | {cat}")
        print(f"    Summary: {desc}")
        if pdf and pdf != "None":
            print(f"    Filing:  {pdf}")

    # Export CSV / JSON
    output_dir.mkdir(parents=True, exist_ok=True)
    if args.csv:
        csv_file = output_dir / f"{sym}_announcements.csv"
        df.to_csv(csv_file, index=False)
        print(f"\nExported {len(df)} records to CSV: {csv_file}")

    if args.json:
        json_file = output_dir / f"{sym}_announcements.json"
        df.to_json(json_file, orient="records", date_format="iso", indent=2)
        print(f"Exported {len(df)} records to JSON: {json_file}")

    # Handle PDF Downloads
    if args.download:
        dl_arg = args.download.strip().lower()
        num_dl = len(df) if dl_arg == "all" else int(dl_arg)
        valid_files = df["attachment_url"].str.contains(r"\.(?:pdf|zip|xbrl|xml)$", case=False, na=False)
        download_df = df[valid_files].head(num_dl)
        print(f"\nDownloading {len(download_df)} PDF filings to: {output_dir}")

        for idx, (_, row) in enumerate(download_df.iterrows(), 1):
            url = row["attachment_url"]
            dt_str = str(row.get("announcement_time", "")).split()[0].replace("-", "")
            cat_slug = re.sub(r"[^\w]+", "_", str(row.get("category", "")))[:25].strip("_")
            custom_name = f"{sym}_{dt_str}_{cat_slug}_{idx}.pdf"
            saved_path = client.download_attachment(url, dest_dir=output_dir, filename=custom_name)
            if saved_path:
                print(f"  [{idx}/{len(download_df)}] Downloaded: {saved_path.name}")
                if args.convert_md:
                    try:
                        from src.common.scripts.pdf_to_markdown import convert_pdf_to_markdown
                        convert_pdf_to_markdown(saved_path, delete_original=False)
                    except Exception as e:
                        print(f"  Warning: Failed to convert {saved_path.name} to Markdown: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
