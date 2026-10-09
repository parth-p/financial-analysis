#!/usr/bin/env python3
"""Chittorgarh IPO API client for listing and retrieving detailed IPO metadata.

Provides programmatic access and a CLI interface to fetch:
1. IPO listings (mainboard, SME, or both) from Chittorgarh's report data API.
2. Comprehensive IPO details (issue structure, timetable, financials, KPIs,
   and regulatory filing URLs including SEBI RHP/DRHP) from Chittorgarh's cloud detail API.
"""

from __future__ import annotations

import argparse
import datetime
import json
import logging
import re
import sys
from pathlib import Path
from typing import Any

import requests

try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False

# Ensure repository root is on sys.path
REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("ipo_client")

API_BASE = "https://webnodejs.chittorgarh.com"
REPORT_ID_LIVE = 82       # Active/Current Year IPO list (with prices, issue sizes, symbols)
REPORT_ID_ARCHIVE = 118   # Historical IPO list (complete multi-year schedule archive)

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.chittorgarh.com/",
    "Origin": "https://www.chittorgarh.com",
}


def _strip_html(text: str) -> str:
    """Remove HTML tags, character entities, and extra whitespace from text."""
    if not text:
        return ""
    # Strip HTML tags
    cleaned = re.sub(r"<[^>]+>", " ", text)
    # Decode entities
    cleaned = (
        cleaned.replace("&amp;", "&")
        .replace("&nbsp;", " ")
        .replace("&#8377;", "₹")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&quot;", '"')
    )
    return re.sub(r"\s+", " ", cleaned).strip()


def _clean_date_str(val: str | None) -> str:
    """Strip tentative HTML badges and normalize ISO date strings to DD-Mon-YYYY."""
    if not val:
        return "-"
    # Strip badges such as <span class="badge ...">T</span>
    val = re.sub(r"<span[^>]*>.*?</span>", "", val, flags=re.DOTALL | re.IGNORECASE)
    val = _strip_html(val).strip()
    if not val:
        return "-"
    # Check for ISO format: 2026-10-08T00:00:00.000Z
    if "T" in val and val.endswith("Z"):
        try:
            dt = datetime.datetime.fromisoformat(val.replace("Z", "+00:00"))
            return dt.strftime("%d-%b-%Y")
        except Exception:
            pass
    return val


def _format_amt_cr(val: Any) -> str:
    """Format rupee amount into clean crores representation."""
    if val is None or val == "":
        return "-"
    try:
        clean = str(val).replace(",", "").strip()
        amt = float(clean)
        # If amount is greater than 1 lakh, it represents raw rupees, convert to Cr
        if amt > 100000:
            return f"{amt / 1e7:.2f}"
        return f"{amt:.2f}"
    except (ValueError, TypeError):
        return str(val)


def _parse_html_table(html_snippet: str) -> dict[str, Any]:
    """Parse an HTML table into headers and rows of stripped text."""
    if not html_snippet:
        return {"headers": [], "rows": []}

    headers: list[str] = []
    rows: list[list[str]] = []

    th_matches = re.findall(r"<th[^>]*>(.*?)</th>", html_snippet, re.DOTALL | re.IGNORECASE)
    if th_matches:
        headers = [_strip_html(th) for th in th_matches]

    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", html_snippet, re.DOTALL | re.IGNORECASE):
        td_matches = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.DOTALL | re.IGNORECASE)
        if td_matches:
            rows.append([_strip_html(td) for td in td_matches])

    return {"headers": headers, "rows": rows}


class ChittorgarhClient:
    """Client for Chittorgarh IPO reporting and detail endpoints."""

    def __init__(self, session: requests.Session | None = None) -> None:
        self.session = session or requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)

    def fetch_ipo_list(
        self,
        board_type: str = "mainboard",
        year: int | None = None,
        month: int = 12,
        fy: str | None = None,
        fetch_sizes: bool = False,
    ) -> list[dict[str, Any]]:
        """Fetch IPO listing for mainboard, sme, or both.

        Args:
            board_type: "mainboard", "sme", or "both".
            year: Calendar year (defaults to current year).
            month: Month integer (12 queries full financial year).
            fy: Financial year string (e.g., '2026-27'). Auto-calculated if None.
            fetch_sizes: For historical archives, concurrently query detail API to populate issue_size_cr.

        Returns:
            List of parsed IPO summary dictionaries.
        """
        board_type = board_type.lower()
        if board_type not in ("mainboard", "sme", "both"):
            raise ValueError(f"Invalid board_type '{board_type}'. Must be 'mainboard', 'sme', or 'both'.")

        targets = ["mainboard", "sme"] if board_type == "both" else [board_type]

        now = datetime.datetime.now()
        target_year = year or now.year
        target_fy = fy or f"{target_year}-{str(target_year + 1)[-2:]}"

        # Report 82 for current/live year; Report 118 for historical schedule archive
        report_id = REPORT_ID_LIVE if target_year >= now.year else REPORT_ID_ARCHIVE

        combined_records: list[dict[str, Any]] = []
        seen_keys: set[tuple[str, str]] = set()

        url_regex_id = re.compile(r"/ipo/([^/]+)/(\d+)/?")

        for board in targets:
            page = 1
            total_pages = 1

            while page <= total_pages:
                url = (
                    f"{API_BASE}/cloud/report/data-read/{report_id}/"
                    f"{page}/{month}/{target_year}/{target_fy}/0/{board}/0?search="
                )
                logger.debug("Requesting IPO list: %s", url)

                resp = self.session.get(url, timeout=25)
                resp.raise_for_status()
                data = resp.json()

                if data.get("msg") != 1:
                    break

                rows = data.get("reportTableData", [])
                if not rows:
                    break

                total_pages = data.get("totalPages", 1)

                for row in rows:
                    if report_id == REPORT_ID_LIVE:
                        raw_company = row.get("Company", "")
                        clean_company = _strip_html(raw_company)
                        clean_company = re.sub(r"\s+[A-Z]$", "", clean_company).strip()

                        match = url_regex_id.search(raw_company)
                        ipo_id = int(match.group(2)) if match else None
                        slug = match.group(1) if match else (row.get("~URLRewrite_Folder_Name") or "")
                        ipo_url = f"https://www.chittorgarh.com/ipo/{slug}/{ipo_id}/" if ipo_id and slug else ""

                        open_date = row.get("Opening Date") or row.get("~Issue_Open_Date") or ""
                        close_date = row.get("Closing Date") or row.get("~IssueCloseDate") or ""
                        listing_date = row.get("Listing Date") or row.get("~ListingDate") or ""
                        issue_price = row.get("Issue Price (Rs.)") or ""
                        issue_size_cr = row.get("Total Issue Amount (Incl.Firm reservations) (Rs.cr.)") or ""
                        fresh_capital_cr = row.get("Fresh Capital (Rs.cr.)") or ""
                        offer_for_sale_cr = row.get("Offer for sale (Rs.cr.)") or ""
                        listing_at = row.get("Listing at") or ""
                        pricing_method = row.get("Pricing Method") or ""
                        nse_symbol = row.get("~nse_symbol") or ""
                        bse_code = str(row.get("~bse_script_code") or "")
                        isin = row.get("~isin") or ""
                    else:
                        clean_company = _strip_html(row.get("Company", ""))
                        clean_company = re.sub(r"\s+[A-Z]$", "", clean_company).strip()
                        raw_id = row.get("~id")
                        ipo_id = int(raw_id) if raw_id else None
                        slug = row.get("~urlrewrite_folder_name") or ""
                        ipo_url = f"https://www.chittorgarh.com/ipo/{slug}/{ipo_id}/" if ipo_id and slug else ""

                        open_date = row.get("Opening Date") or row.get("~Issue_Open_Date") or ""
                        close_date = row.get("Closing Date") or row.get("~Issue_Close_Date") or ""
                        listing_date = row.get("Listing Date") or row.get("~IPO_Listing_date") or ""
                        issue_price = ""
                        issue_size_cr = ""
                        fresh_capital_cr = ""
                        offer_for_sale_cr = ""
                        listing_at = ""
                        pricing_method = ""
                        nse_symbol = ""
                        bse_code = ""
                        isin = ""

                    key = (clean_company, open_date)
                    if key in seen_keys:
                        continue
                    seen_keys.add(key)

                    record = {
                        "id": ipo_id,
                        "company": clean_company,
                        "slug": slug,
                        "board_type": board,
                        "open_date": open_date,
                        "close_date": close_date,
                        "listing_date": listing_date,
                        "issue_price": issue_price,
                        "issue_size_cr": issue_size_cr,
                        "fresh_capital_cr": fresh_capital_cr,
                        "offer_for_sale_cr": offer_for_sale_cr,
                        "listing_at": listing_at,
                        "pricing_method": pricing_method,
                        "nse_symbol": nse_symbol,
                        "bse_code": bse_code,
                        "isin": isin,
                        "url": ipo_url,
                    }
                    combined_records.append(record)

                page += 1

        if fetch_sizes and report_id == REPORT_ID_ARCHIVE and combined_records:
            logger.info("Fetching issue sizes concurrently for %d historical IPOs...", len(combined_records))
            import concurrent.futures

            def _get_size(rec: dict[str, Any]) -> str:
                target_id = rec.get("id")
                if not target_id:
                    return ""
                try:
                    u = f"{API_BASE}/cloud/ipo/detail-read/{target_id}"
                    r = self.session.get(u, timeout=15)
                    if r.status_code == 200:
                        d = r.json()
                        raw = d.get("ipoData", [{}])[0]
                        return _format_amt_cr(raw.get("issue_size_in_amt"))
                except Exception:
                    pass
                return ""

            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
                sizes = list(ex.map(_get_size, combined_records))
            for rec, sz in zip(combined_records, sizes):
                if sz and sz != "-":
                    rec["issue_size_cr"] = sz

        return combined_records

    def fetch_ipo_details(self, ipo_id_or_url: int | str) -> dict[str, Any]:
        """Fetch comprehensive IPO metadata, financials, timetable, and regulatory filing URLs.

        Args:
            ipo_id_or_url: Numerical Chittorgarh IPO ID (e.g., 2974) or full Chittorgarh URL.

        Returns:
            Normalized dictionary containing IPO specifications, links, timetable, and financials.
        """
        ipo_id: int
        slug_hint: str = ""

        if isinstance(ipo_id_or_url, int):
            ipo_id = ipo_id_or_url
        else:
            query = str(ipo_id_or_url).strip()
            url_match = re.search(r"/ipo/([^/]+)/(\d+)/?", query)
            if url_match:
                slug_hint = url_match.group(1)
                ipo_id = int(url_match.group(2))
            elif query.isdigit():
                ipo_id = int(query)
            else:
                raise ValueError(
                    f"Invalid target '{ipo_id_or_url}'. Expected an integer IPO ID or Chittorgarh URL."
                )

        url = f"{API_BASE}/cloud/ipo/detail-read/{ipo_id}"
        logger.debug("Requesting IPO detail: %s", url)

        resp = self.session.get(url, timeout=25)
        resp.raise_for_status()
        data = resp.json()

        if data.get("msg") != 1 or not data.get("ipoData"):
            raise ValueError(f"No detail data returned by Chittorgarh for IPO ID {ipo_id}.")

        raw_ipo: dict[str, Any] = data["ipoData"][0]
        slug = raw_ipo.get("urlrewrite_folder_name") or slug_hint

        # Format price band
        p_lower = raw_ipo.get("issue_price_lower")
        p_upper = raw_ipo.get("issue_price_upper")
        price_band = (
            f"₹{p_lower} to ₹{p_upper}"
            if p_lower and p_upper and p_lower != p_upper
            else f"₹{p_upper or p_lower or '-'}"
        )

        timetable = {
            "open": raw_ipo.get("timetable_issue_open_date") or raw_ipo.get("issue_open_date") or "",
            "close": raw_ipo.get("timetable_issue_close_date") or raw_ipo.get("issue_close_date") or "",
            "allotment": raw_ipo.get("timetable_boa_dt") or "",
            "refund": raw_ipo.get("timetable_refunds_dt") or "",
            "credit": raw_ipo.get("timetable_share_credit_dt") or "",
            "listing": raw_ipo.get("timetable_listing_dt") or "",
        }

        documents = {
            "rhp": raw_ipo.get("prospectus_rhp") or "",
            "drhp": raw_ipo.get("prospectus_drhp") or "",
            "final_prospectus": raw_ipo.get("final_prospectus") or "",
            "logo": (
                f"https://www.chittorgarh.net/images/ipo/{raw_ipo.get('logo_url')}"
                if raw_ipo.get("logo_url")
                else ""
            ),
        }

        kpis = {
            "ronw": raw_ipo.get("kpi_ronw") or "",
            "roe": raw_ipo.get("kpi_roe") or "",
            "roce": raw_ipo.get("kpi_roce") or "",
            "debt_equity": raw_ipo.get("kpi_debt_equity") or "",
            "eps": raw_ipo.get("kpi_eps") or "",
            "pe_ratio": raw_ipo.get("pe_ratio") or "",
            "price_to_book_value": raw_ipo.get("price_to_book_value") or "",
            "pat_margin": raw_ipo.get("kpi_pat_margin") or "",
            "ebitda": raw_ipo.get("kpi_ebitda") or "",
        }

        # Parse financials HTML table
        financial_html = raw_ipo.get("financial") or ""
        financial_tables = _parse_html_table(financial_html)

        # Lead managers
        lead_managers = [
            mgr.get("lead_manager_name")
            for mgr in data.get("ipoLeadManagersList", [])
            if isinstance(mgr, dict) and mgr.get("lead_manager_name")
        ]

        # Peer comparisons
        peers = [
            {
                "peer": p.get("company_name"),
                "pe": p.get("pe_ratio"),
                "ronw": p.get("ronw"),
                "eps": p.get("basic_eps"),
            }
            for p in data.get("ipoPeerComparisonData", [])
            if isinstance(p, dict) and p.get("company_name")
        ]

        return {
            "id": ipo_id,
            "company_name": raw_ipo.get("company_name") or "",
            "slug": slug,
            "url": f"https://www.chittorgarh.com/ipo/{slug}/{ipo_id}/" if slug else "",
            "board_type": raw_ipo.get("issue_category") or "",
            "issue_type": raw_ipo.get("issue_type") or "",
            "listing_at": raw_ipo.get("ipo_listing_at") or "",
            "price_band": price_band,
            "face_value": raw_ipo.get("face_value") or "",
            "market_lot_size": raw_ipo.get("market_lot_size") or "",
            "total_issue_size_cr": _format_amt_cr(raw_ipo.get("issue_size_in_amt")),
            "fresh_issue_size_cr": _format_amt_cr(raw_ipo.get("issue_size_fresh_in_amt")),
            "ofs_size_cr": _format_amt_cr(raw_ipo.get("issue_size_ofs_in_amt")),
            "market_cap_cr": _format_amt_cr(raw_ipo.get("market_cap")),
            "nse_symbol": raw_ipo.get("nse_symbol") or raw_ipo.get("il_nse_script_symbol") or "",
            "bse_scripcode": raw_ipo.get("bse_scripcode") or raw_ipo.get("il_bse_script_code") or "",
            "isin": raw_ipo.get("il_isin") or "",
            "timetable": timetable,
            "documents": documents,
            "kpis": kpis,
            "financials": financial_tables,
            "lead_managers": lead_managers,
            "peers": peers,
            "about": _strip_html(raw_ipo.get("company_desc") or ""),
            "raw_data": data,
        }

    def save_details(self, details: dict[str, Any], output_path: Path | None = None) -> Path:
        """Save IPO details to JSON file under tmp/company/ipo/<id>_<slug>/details.json."""
        ipo_id = details["id"]
        slug = details["slug"] or "ipo"

        if output_path is None:
            folder = REPO_ROOT / "tmp" / "company" / "ipo" / f"{ipo_id}_{slug}"
            target_file = folder / "details.json"
        else:
            target_file = Path(output_path)

        target_file.parent.mkdir(parents=True, exist_ok=True)
        with target_file.open("w", encoding="utf-8") as f:
            json.dump(details, f, indent=2, ensure_ascii=False)

        logger.info("Saved IPO details to: %s", target_file)
        return target_file


def format_list_table(ipos: list[dict[str, Any]], limit: int | None = None) -> str:
    """Format list of IPOs into a clean terminal table."""
    if not ipos:
        return "No IPOs found."

    display_items = ipos[:limit] if limit else ipos

    headers = [
        "ID",
        "Company",
        "Board",
        "Open Date",
        "Close Date",
        "Listing Date",
        "Price (₹)",
        "Issue (₹ Cr)",
        "Symbol",
    ]

    rows = []
    for item in display_items:
        comp_name = item.get("company", "")
        # Truncate very long company names for neat terminal display
        if len(comp_name) > 38:
            comp_name = comp_name[:35] + "..."

        rows.append([
            item.get("id") or "-",
            comp_name,
            (item.get("board_type") or "").upper(),
            _clean_date_str(item.get("open_date")),
            _clean_date_str(item.get("close_date")),
            _clean_date_str(item.get("listing_date")),
            item.get("issue_price") or "-",
            item.get("issue_size_cr") or "-",
            item.get("nse_symbol") or item.get("bse_code") or "-",
        ])

    if HAS_TABULATE:
        return tabulate(rows, headers=headers, tablefmt="rounded_outline")

    # Simple fallback formatter if tabulate is unavailable
    col_widths = [len(h) for h in headers]
    for row in rows:
        for idx, val in enumerate(row):
            col_widths[idx] = max(col_widths[idx], len(str(val)))

    line_fmt = " | ".join(f"{{:<{w}}}" for w in col_widths)
    sep_line = "-+-".join("-" * w for w in col_widths)

    out = [line_fmt.format(*headers), sep_line]
    for row in rows:
        out.append(line_fmt.format(*[str(v) for v in row]))
    return "\n".join(out)


def format_details_table(details: dict[str, Any]) -> str:
    """Format comprehensive IPO details into structured terminal tables."""
    sections: list[str] = []

    # 1. Company Header & Overview
    overview_headers = ["Field", "Value"]
    overview_rows = [
        ["Company Name", details.get("company_name", "-")],
        ["Chittorgarh ID", str(details.get("id", "-"))],
        ["Board / Category", f"{details.get('board_type', '-')} ({details.get('issue_type', '-')})"],
        ["Listing Exchange", details.get("listing_at", "-") or "-"],
        ["Price Band", details.get("price_band", "-")],
        ["Market Lot", f"{details.get('market_lot_size', '-')} shares"],
        ["Total Issue Size", f"₹ {details.get('total_issue_size_cr', '-')} Cr"],
        ["Fresh Issue Size", f"₹ {details.get('fresh_issue_size_cr', '-')} Cr"],
        ["Offer for Sale (OFS)", f"₹ {details.get('ofs_size_cr', '-')} Cr"],
        ["Market Cap at Offer", f"₹ {details.get('market_cap_cr', '-')} Cr"],
        ["NSE Symbol / BSE Scrip", f"{details.get('nse_symbol') or '-'} / {details.get('bse_scripcode') or '-'}"],
    ]

    # 2. Timetable
    tt = details.get("timetable", {})
    timetable_rows = [
        ["Issue Open Date", tt.get("open") or "-"],
        ["Issue Close Date", tt.get("close") or "-"],
        ["Basis of Allotment", tt.get("allotment") or "-"],
        ["Refunds Initiation", tt.get("refund") or "-"],
        ["Credit of Shares", tt.get("credit") or "-"],
        ["Listing Date", tt.get("listing") or "-"],
    ]

    # 3. Valuation & KPIs
    kpi = details.get("kpis", {})
    kpi_rows = [
        ["RoNW / RoE", f"{kpi.get('ronw') or '-'} / {kpi.get('roe') or '-'}"],
        ["RoCE", kpi.get("roce") or "-"],
        ["Debt / Equity", kpi.get("debt_equity") or "-"],
        ["EPS (₹)", kpi.get("eps") or "-"],
        ["P/E Ratio", kpi.get("pe_ratio") or "-"],
        ["Price to Book (P/BV)", kpi.get("price_to_book_value") or "-"],
        ["PAT Margin / EBITDA", f"{kpi.get('pat_margin') or '-'} / {kpi.get('ebitda') or '-'}"],
    ]

    # 4. Documents & Filings
    docs = details.get("documents", {})
    doc_rows = [
        ["RHP URL", docs.get("rhp") or "-"],
        ["DRHP URL", docs.get("drhp") or "-"],
        ["Chittorgarh URL", details.get("url") or "-"],
    ]

    if HAS_TABULATE:
        sections.append("### 1. Issue Overview")
        sections.append(tabulate(overview_rows, headers=overview_headers, tablefmt="rounded_outline"))
        sections.append("\n### 2. Timetable")
        sections.append(tabulate(timetable_rows, headers=["Event", "Date"], tablefmt="rounded_outline"))
        sections.append("\n### 3. Key Financial KPIs & Valuation")
        sections.append(tabulate(kpi_rows, headers=["KPI Metric", "Value"], tablefmt="rounded_outline"))
        sections.append("\n### 4. Regulatory Documents")
        sections.append(tabulate(doc_rows, headers=["Document", "URL"], tablefmt="rounded_outline"))

        # Financials table if present
        fin = details.get("financials", {})
        if fin.get("headers") and fin.get("rows"):
            sections.append("\n### 5. Restated Financial Summary (from RHP)")
            sections.append(tabulate(fin["rows"], headers=fin["headers"], tablefmt="rounded_outline"))
    else:
        # Fallback formatting
        sections.append("=== Issue Overview ===")
        for k, v in overview_rows:
            sections.append(f"{k:25}: {v}")
        sections.append("\n=== Timetable ===")
        for k, v in timetable_rows:
            sections.append(f"{k:25}: {v}")
        sections.append("\n=== Key KPIs ===")
        for k, v in kpi_rows:
            sections.append(f"{k:25}: {v}")
        sections.append("\n=== Documents ===")
        for k, v in doc_rows:
            sections.append(f"{k:25}: {v}")

    return "\n".join(sections)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Chittorgarh IPO Client: List IPOs and inspect individual IPO details."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 1. 'list' subcommand
    list_parser = subparsers.add_parser("list", help="Fetch and display list of IPOs.")
    list_parser.add_argument(
        "-b",
        "--board",
        choices=["mainboard", "sme", "both"],
        default="mainboard",
        help="Board type filter (default: mainboard).",
    )
    list_parser.add_argument(
        "-y",
        "--year",
        type=int,
        default=None,
        help="Target year (default: current year).",
    )
    list_parser.add_argument(
        "-m",
        "--month",
        type=int,
        default=12,
        help="Month filter (default: 12 queries full financial year).",
    )
    list_parser.add_argument(
        "--fy",
        type=str,
        default=None,
        help="Financial year string (e.g. 2026-27).",
    )
    list_parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Maximum rows to display in terminal table.",
    )
    list_parser.add_argument(
        "--fetch-sizes",
        action="store_true",
        help="Concurrently query detail API to populate issue sizes for historical years.",
    )
    list_parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON array instead of terminal table.",
    )

    # 2. 'details' subcommand
    details_parser = subparsers.add_parser("details", help="Fetch detailed specifications for an IPO.")
    details_parser.add_argument(
        "target",
        nargs="?",
        default=None,
        help="Chittorgarh IPO ID (e.g., 2974) or full Chittorgarh URL.",
    )
    details_parser.add_argument(
        "--id",
        type=int,
        default=None,
        help="Numerical Chittorgarh IPO ID.",
    )
    details_parser.add_argument(
        "--url",
        type=str,
        default=None,
        help="Chittorgarh IPO page URL.",
    )
    details_parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Custom destination JSON file path.",
    )
    details_parser.add_argument(
        "--no-save",
        action="store_true",
        help="Do not save output JSON file to tmp/company/ipo/.",
    )
    details_parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON payload instead of terminal summary table.",
    )
    details_parser.add_argument(
        "--fetch-rhp",
        action="store_true",
        help="Automatically invoke fetch_rhp.py if RHP document URL is available.",
    )
    details_parser.add_argument(
        "--to-markdown",
        action="store_true",
        help="When used with --fetch-rhp, convert the downloaded RHP PDF to Markdown.",
    )

    args = parser.parse_args()
    client = ChittorgarhClient()

    if args.command == "list":
        try:
            records = client.fetch_ipo_list(
                board_type=args.board,
                year=args.year,
                month=args.month,
                fy=args.fy,
                fetch_sizes=args.fetch_sizes,
            )
            if args.json:
                print(json.dumps(records, indent=2, ensure_ascii=False))
            else:
                table_output = format_list_table(records, limit=args.limit)
                print(table_output)
                print(f"\nTotal IPOs listed: {len(records)} (Displaying: {args.limit or len(records)})")
        except Exception as exc:
            logger.error("Failed to fetch IPO list: %s", exc)
            sys.exit(1)

    elif args.command == "details":
        target = args.target or args.id or args.url
        if not target:
            details_parser.error("You must provide an IPO ID or Chittorgarh URL.")

        try:
            details = client.fetch_ipo_details(target)

            if not args.no_save:
                out_path = Path(args.output) if args.output else None
                saved_path = client.save_details(details, output_path=out_path)
            else:
                saved_path = None

            if args.json:
                print(json.dumps(details, indent=2, ensure_ascii=False))
            else:
                table_output = format_details_table(details)
                print(table_output)
                if saved_path:
                    print(f"\n[Artifact Saved] Detailed JSON saved to: {saved_path}")

            if args.fetch_rhp:
                rhp_url = details.get("documents", {}).get("rhp")
                if not rhp_url:
                    logger.warning("No RHP link available in Chittorgarh metadata for this IPO.")
                else:
                    logger.info("Triggering fetch_rhp for %s", rhp_url)
                    from src.company.ipo.scripts.fetch_rhp import fetch_rhp

                    company_slug = details.get("slug") or str(details.get("id"))
                    fetch_rhp(
                        url=rhp_url,
                        company=company_slug,
                        to_markdown=args.to_markdown,
                        progress_callback=lambda msg: print(f"-> {msg}"),
                    )

        except Exception as exc:
            logger.error("Failed to fetch IPO details: %s", exc)
            sys.exit(1)


if __name__ == "__main__":
    main()
