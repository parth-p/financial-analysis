#!/usr/bin/env python3
"""
Scrape financial data from screener.in and save to Markdown.
Usage: .venv/bin/python src/company/listed/scripts/screener_scrape.py <screener_url>
Example: .venv/bin/python src/company/listed/scripts/screener_scrape.py https://www.screener.in/company/KAYNES/consolidated/
"""

from __future__ import annotations

import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.screener.in"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

SECTION_IDS = [
    ("quarters", "Quarterly Results"),
    ("profit-loss", "Profit & Loss"),
    ("balance-sheet", "Balance Sheet"),
    ("cash-flow", "Cash Flows"),
    ("ratios", "Ratios"),
]


def get_workspace_root() -> Path:
    """Resolve repository root directory."""
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / ".git").exists() or (parent / "AGENTS.md").exists():
            return parent
    return Path.cwd()


def fetch(url: str, extra_headers: dict | None = None) -> requests.Response:
    """Fetch URL with default browser headers."""
    h = {**HEADERS, **(extra_headers or {})}
    resp = requests.get(url, headers=h, timeout=30)
    resp.raise_for_status()
    return resp


def extract_cmp(soup: BeautifulSoup) -> str:
    """Extract Current Market Price from default ratio items."""
    for li in soup.find_all("li", attrs={"data-source": "default"}):
        name_el = li.find("span", class_="name")
        if name_el and name_el.get_text(strip=True) == "Current Price":
            number_el = li.find("span", class_="number")
            return f"₹{number_el.get_text(strip=True)}" if number_el else "N/A"
    return "N/A"


def extract_top_ratios(soup: BeautifulSoup) -> list[tuple[str, str]]:
    """Extract top summary metrics from the header."""
    ratios = []
    top_ratios_el = soup.find("ul", id="top-ratios")
    if not top_ratios_el:
        return ratios

    for li in top_ratios_el.find_all("li"):
        name_el = li.find("span", class_="name")
        value_el = li.find("span", class_="nowrap value") or li.find("span", class_="number")
        if name_el and value_el:
            name = name_el.get_text(strip=True)
            val = value_el.get_text(" ", strip=True)
            ratios.append((name, val))
    return ratios


def fetch_schedule(company_id: str, parent: str, section: str, is_consolidated: bool) -> tuple[str, dict]:
    """Fetch expandable schedule JSON data for a specific parent row."""
    params = f"parent={quote(parent)}&section={quote(section)}"
    if is_consolidated:
        params += "&consolidated="
    url = f"{BASE_URL}/api/company/{company_id}/schedules/?{params}"

    for attempt in range(3):
        try:
            resp = fetch(url, {"X-Requested-With": "XMLHttpRequest", "Accept": "application/json"})
            return parent, resp.json()
        except Exception as e:
            if attempt < 2:
                time.sleep(1.5 * (attempt + 1))
            else:
                print(f"  Warning: could not fetch sub-rows for '{parent}': {e}", file=sys.stderr)
                return parent, {}
    return parent, {}


def parse_section(section_el, company_id: str, is_consolidated: bool):
    """Parse HTML table for a section and fetch all expandable sub-schedules."""
    table = section_el.find("table")
    if not table:
        return [], []

    expandable = []
    for btn in section_el.find_all("button", onclick=True):
        m = re.search(r"showSchedule\('([^']+)',\s*'([^']+)'", btn.get("onclick", ""))
        if m:
            expandable.append((m.group(1), m.group(2)))

    schedule_data = {}
    if expandable:
        with ThreadPoolExecutor(max_workers=6) as pool:
            futures = {
                pool.submit(fetch_schedule, company_id, parent, sec, is_consolidated): parent
                for parent, sec in expandable
            }
            for future in as_completed(futures):
                parent, data = future.result()
                schedule_data[parent] = data

    all_trs = table.find_all("tr")
    if not all_trs:
        return [], []

    headers = [c.get_text(strip=True) for c in all_trs[0].find_all(["th", "td"])]

    rows = []
    for tr in all_trs[1:]:
        cells = tr.find_all(["td", "th"])
        if not cells:
            continue

        label_cell = cells[0]
        btn = label_cell.find("button", onclick=re.compile(r"showSchedule"))
        if btn:
            m = re.search(r"showSchedule\('([^']+)'", btn.get("onclick", ""))
            label = m.group(1) if m else label_cell.get_text(strip=True).rstrip("+\xa0").strip()
        else:
            label = label_cell.get_text(strip=True)

        values = {}
        for i, cell in enumerate(cells[1:], 1):
            if i < len(headers) and headers[i]:
                values[headers[i]] = cell.get_text(strip=True)

        bold = "strong" in tr.get("class", [])

        rows.append({
            "label": label,
            "values": values,
            "bold": bold,
            "sub_rows": schedule_data.get(label, {}),
        })

    return headers, rows



def parse_documents(soup: BeautifulSoup) -> dict:
    """Parse annual reports, credit ratings, and concall links from documents section."""
    doc_sec = soup.find("section", id="documents")
    if not doc_sec:
        return {}

    data: dict = {
        "annual_reports": [],
        "drhp": None,
        "credit_ratings": [],
        "concalls": [],
    }

    # Annual reports & DRHP
    ar_div = doc_sec.find("div", class_="annual-reports")
    if ar_div:
        for li in ar_div.find_all("li"):
            a = li.find("a")
            if a and a.get("href"):
                name = a.get_text(strip=True)
                url = a["href"].strip()
                source_el = li.find("span", class_="ink-600")
                source = source_el.get_text(strip=True) if source_el else ""
                data["annual_reports"].append({
                    "name": name,
                    "url": url,
                    "source": source,
                })
        for a in ar_div.find_all("a"):
            if "drhp" in a.get_text().lower():
                data["drhp"] = a.get("href", "").strip()

    # Credit ratings
    cr_div = doc_sec.find("div", class_="credit-ratings")
    if cr_div:
        for li in cr_div.find_all("li"):
            a = li.find("a")
            if a and a.get("href"):
                url = a["href"].strip()
                sub = a.find("div")
                detail = sub.get_text(" ", strip=True) if sub else ""
                m = re.match(r"(.*?)\s+from\s+(.*)", detail, re.I)
                if m:
                    date_str = m.group(1).strip()
                    agency = m.group(2).strip().upper()
                else:
                    date_str = detail
                    agency = ""
                data["credit_ratings"].append({
                    "date": date_str,
                    "agency": agency,
                    "url": url,
                })

    # Concalls
    for col in doc_sec.find_all("div", class_="documents"):
        h = col.find(["h3", "h4"])
        if h and "concall" in h.get_text().lower():
            for li in col.find_all("li"):
                date_div = li.find("div", class_="ink-600")
                date_str = date_div.get_text(strip=True) if date_div else ""
                chips = {
                    a.get_text(strip=True): a["href"].strip()
                    for a in li.find_all("a", class_="button-chip")
                    if a.get("href")
                }
                data["concalls"].append({
                    "period": date_str,
                    "transcript": chips.get("Transcript"),
                    "ppt": chips.get("PPT"),
                    "recording": chips.get("REC"),
                })
            break

    return data


def find_or_create_company_folder(company_name: str, ticker: str, base_dir: Path) -> Path:
    """Find an existing folder in base_dir with a similar name, or create a new one."""
    base_dir.mkdir(parents=True, exist_ok=True)

    # Clean slug
    clean_name = re.sub(r"[^\w\s-]", "", company_name)
    slug = re.sub(r"[-\s]+", "-", clean_name).strip("-").lower()
    ticker_clean = ticker.lower().strip()

    # Significant words from company name
    noise = {"ltd", "limited", "india", "pvt", "corp", "corporation", "industries", "technologies", "co"}
    comp_words = [w for w in re.findall(r"\w+", clean_name.lower()) if w not in noise]

    # Search existing folders in base_dir
    existing_dirs = [d for d in base_dir.iterdir() if d.is_dir()]
    for d in existing_dirs:
        dname = d.name.lower()
        # Direct slug or ticker match
        if dname == slug or dname == ticker_clean:
            return d
        # Ticker token match
        d_tokens = re.findall(r"\w+", dname)
        if ticker_clean in d_tokens:
            return d
        # Word overlap match
        if comp_words and all(w in dname for w in comp_words):
            return d

    # Fall back to creating a clean slug folder
    target = base_dir / slug
    target.mkdir(parents=True, exist_ok=True)
    return target


def write_markdown(
    company_name: str,
    cmp: str,
    url: str,
    is_consolidated: bool,
    top_ratios: list[tuple[str, str]],
    all_section_data: list,
    documents: dict,
    output_file: Path,
) -> None:
    """Write parsed financial sections and document links into a structured Markdown document."""
    lines = []
    lines.append(f"# {company_name} — Financial Overview (Screener.in)")
    lines.append("")
    lines.append(f"- **Source URL:** {url}")
    lines.append(f"- **Report Type:** {'Consolidated' if is_consolidated else 'Standalone'}")
    lines.append(f"- **Current Market Price (CMP):** {cmp}")
    lines.append("")

    if top_ratios:
        lines.append("## Key Financial Indicators")
        lines.append("")
        lines.append("| Indicator | Value |")
        lines.append("| :--- | :--- |")
        for indicator, val in top_ratios:
            lines.append(f"| {indicator} | {val} |")
        lines.append("")

    for _sec_id, sec_name, headers, rows in all_section_data:
        lines.append(f"## {sec_name}")
        lines.append("")

        if not headers or not rows:
            lines.append("*No data available.*")
            lines.append("")
            continue

        first_col = headers[0] if headers[0] else "Metric"
        date_cols = headers[1:]

        # Header row
        header_str = "| " + first_col + " | " + " | ".join(date_cols) + " |"
        sep_str = "| :--- | " + " | ".join([":---:"] * len(date_cols)) + " |"
        lines.append(header_str)
        lines.append(sep_str)

        # Data rows
        for row in rows:
            label_text = f"**{row['label']}**" if row["bold"] else row["label"]
            vals = [row["values"].get(h, "") for h in date_cols]
            lines.append(f"| {label_text} | " + " | ".join(vals) + " |")

            # Expandable sub-rows
            for sub_label, sub_vals in row.get("sub_rows", {}).items():
                s_vals = [sub_vals.get(h, "") for h in date_cols]
                lines.append(f"| &nbsp;&nbsp;&nbsp;&nbsp;↳ *{sub_label}* | " + " | ".join(s_vals) + " |")

        lines.append("")

    # Document sections
    annual_reports = documents.get("annual_reports", [])
    drhp = documents.get("drhp")
    credit_ratings = documents.get("credit_ratings", [])
    concalls = documents.get("concalls", [])

    if annual_reports or drhp:
        lines.append("## Annual Reports")
        lines.append("")
        if annual_reports:
            lines.append("| Report | Source | Link |")
            lines.append("| :--- | :--- | :--- |")
            for ar in annual_reports:
                src = ar["source"].replace("from ", "").upper() or "BSE"
                lines.append(f"| {ar['name']} | {src} | [PDF]({ar['url']}) |")
            lines.append("")
        if drhp:
            lines.append(f"- **Prospectus (DRHP):** [SEBI Filing]({drhp})")
            lines.append("")

    if credit_ratings:
        lines.append("## Credit Ratings")
        lines.append("")
        lines.append("| Date | Agency | Report Link |")
        lines.append("| :--- | :--- | :--- |")
        for cr in credit_ratings:
            agency = cr["agency"] or "-"
            lines.append(f"| {cr['date']} | {agency} | [Rating Report]({cr['url']}) |")
        lines.append("")

    if concalls:
        lines.append("## Concalls & Investor Presentations")
        lines.append("")
        lines.append("| Period | Transcript | Presentation | Audio Recording |")
        lines.append("| :--- | :---: | :---: | :---: |")
        for cc in concalls:
            t_link = f"[Transcript]({cc['transcript']})" if cc.get("transcript") else "-"
            p_link = f"[PPT]({cc['ppt']})" if cc.get("ppt") else "-"
            r_link = f"[Audio]({cc['recording']})" if cc.get("recording") else "-"
            lines.append(f"| {cc['period']} | {t_link} | {p_link} | {r_link} |")
        lines.append("")

    output_file.write_text("\n".join(lines), encoding="utf-8")


def main():
    if len(sys.argv) < 2:
        print("Usage: .venv/bin/python src/company/listed/scripts/screener_scrape.py <screener_url>")
        print("Example: .venv/bin/python src/company/listed/scripts/screener_scrape.py https://www.screener.in/company/KAYNES/consolidated/")
        sys.exit(1)

    url = sys.argv[1].strip().rstrip("/") + "/"
    if "/consolidated/" not in url and "/standalone/" not in url:
        url = url.rstrip("/") + "/consolidated/"

    # Extract ticker from URL pattern /company/<TICKER>/
    m = re.search(r"/company/([^/]+)/", url)
    ticker = m.group(1) if m else "company"

    print(f"Fetching {url} ...")
    html = fetch(url).text
    soup = BeautifulSoup(html, "lxml")

    info_el = soup.find(id="company-info")
    if not info_el or not info_el.has_attr("data-company-id"):
        print("Error: could not find company ID — is this a valid screener.in company URL?", file=sys.stderr)
        sys.exit(1)

    company_id = info_el["data-company-id"]
    is_consolidated = "/consolidated/" in url

    h1 = soup.find("h1")
    company_name = h1.get_text(strip=True) if h1 else ticker.upper()
    cmp = extract_cmp(soup)
    top_ratios = extract_top_ratios(soup)

    print(f"Company : {company_name}")
    print(f"CMP     : {cmp}")

    all_data = []
    for section_id, section_name in SECTION_IDS:
        print(f"  Fetching {section_name}...", end=" ", flush=True)
        section_el = soup.find("section", id=section_id)
        if not section_el:
            print("not found.")
            continue
        headers, rows = parse_section(section_el, company_id, is_consolidated)
        if not headers:
            print("no table.")
            continue
        sub_count = sum(len(r["sub_rows"]) for r in rows)
        print(f"{len(rows)} rows + {sub_count} expanded sub-rows")
        all_data.append((section_id, section_name, headers, rows))

    if not all_data:
        print("\nNo financial data found.", file=sys.stderr)
        sys.exit(1)

    print("  Fetching Documents...", end=" ", flush=True)
    documents = parse_documents(soup)
    ar_count = len(documents.get("annual_reports", []))
    cr_count = len(documents.get("credit_ratings", []))
    cc_count = len(documents.get("concalls", []))
    print(f"{ar_count} annual reports, {cr_count} credit ratings, {cc_count} concalls")

    # Resolve output directory under tmp/company/listed/
    workspace_root = get_workspace_root()
    listed_tmp_dir = workspace_root / "tmp" / "company" / "listed"
    target_folder = find_or_create_company_folder(company_name, ticker, listed_tmp_dir)
    output_file = target_folder / "screener.md"

    write_markdown(company_name, cmp, url, is_consolidated, top_ratios, all_data, documents, output_file)
    print(f"\nSaved Markdown → {output_file.resolve()}")


if __name__ == "__main__":
    main()

