# Repository Guidelines

**Purpose:** Structured Indian equity research (NSE/BSE listed equities, IPOs, investment themes, and value chains). Playbooks, checklists, and automation scripts live in `src/`; static reference data in `data/`; all generated outputs route to `tmp/` (gitignored).

---

## Directory Organization

```text
analysis/
├── AGENTS.md                # Agent conventions and project guide (this file)
├── README.md                # Human-facing project overview & setup
├── requirements.txt         # Python dependencies (install via .venv/bin/pip)
├── .gitignore               # Ignores tmp/, .venv/, __pycache__, *.pyc, .DS_Store
│
├── data/                    # Static reference data (read-only, version-controlled)
│   ├── bse_stocks.csv           # BSE master list: ~10,900 scrip codes → tickers/names/groups
│   ├── mainboard_ipos.csv       # Recent mainboard IPOs: id, name, listing_date, issue_size, url
│   ├── sme_ipos.csv             # Recent SME IPOs: same schema as mainboard_ipos.csv
│   ├── ipo_descriptions.json    # Company name → rich business profile text (from Chittorgarh)
│   └── indian_market_taxonomy_5_tier.md  # 5-tier SEBI sector taxonomy (~500+ sub-segments)
│
├── src/                     # Source methodology, playbooks, checklists, and tools
│   ├── common/              # Shared utilities used across IPO and listed workflows
│   │   ├── docs/
│   │   │   └── valuation-guide.md       # Plain-language valuation primer (sector→metric cheat sheet, DCF params)
│   │   └── scripts/
│   │       └── pdf_to_markdown.py       # Convert PDF → Markdown via pymupdf4llm (deletes PDF by default)
│   │
│   ├── company/
│   │   ├── ipo/             # IPO research
│   │   │   ├── WORKFLOW.md              # ★ Master orchestrator: Quick Triage & Full Deep-Dive workflows
│   │   │   ├── checklists/
│   │   │   │   ├── full-ipo.md          # Comprehensive 6-stage IPO deep-dive checklist
│   │   │   │   └── quick-ipo.md         # Rapid triage checklist (decide: apply / pass / escalate)
│   │   │   └── scripts/
│   │   │       ├── fetch_rhp.py         # Download RHP/DRHP from SEBI/exchange URLs → tmp/company/ipo/
│   │   │       └── ipo_client.py        # Chittorgarh API client: list IPOs, fetch details, trigger RHP download
│   │   │
│   │   └── listed/          # Listed equity research (4-stage framework)
│   │       ├── WORKFLOW.md              # ★ Master orchestrator: execution rules, sources & stage prompts
│   │       ├── peer-finder.md           # Deterministic peer-selection runbook for relative valuation
│   │       ├── checklists/              # The 4 analytical stages (execute in order)
│   │       │   ├── 1-business.md            # Stage 1: Business model, industry arena & moat falsification
│   │       │   ├── 2-management.md          # Stage 2: Management competence, capital allocation & governance
│   │       │   ├── 3-financials.md          # Stage 3: Financial forensics & valuation collision (Parts A & B)
│   │       │   └── 4-thesis.md              # Stage 4: Investment decision, strategic arc & thesis
│   │       └── scripts/                 # Automation tools for listed research
│   │           ├── screener_scrape.py       # Scrape Screener.in → screener.md (financials, ratios, doc links)
│   │           ├── financial_calculator.py  # Ratio tables, DuPont, forensics (Altman Z, Beneish M) from JSON
│   │           ├── valuation_calculator.py  # 3-year multiples valuation, inversion, sensitivity grid from JSON
│   │           ├── bse_announcements.py     # Fetch BSE announcements (orders, filings, PDFs)
│   │           └── nse_announcements.py     # Fetch NSE announcements (orders, filings, PDFs)
│   │
│   └── general/             # Top-down / thematic research playbooks
│       ├── theme-discovery.md           # Scout & rank 10–20 investment themes across time horizons
│       ├── order-of-effects.md          # Map multi-order causal effects of a theme (no tickers until Phase 6)
│       └── theme-to-companies.md        # Theme → all NSE/BSE-listed companies with exposure tiers
│
└── tmp/                     # Ephemeral output (GITIGNORED — never commit)
    ├── company/
    │   ├── ipo/             # Downloaded RHPs, parsed text, generated IPO reports
    │   └── listed/          # Per-company folders: screener.md, step analyses, announcements/
    └── general/             # Theme discovery, sector, and value-chain reports
```

---

## Output Routing & Storage Rules

- **`tmp/` is untracked on purpose.** All generated analysis, scraped data, downloaded PDFs, and converted markdown MUST go under the appropriate `tmp/` subdirectory:
  - IPO reports and downloads → `tmp/company/ipo/<company-slug>/`
  - Listed company analyses → `tmp/company/listed/<company-slug>/` (reuse an existing folder matching the company name, ticker, or slug)
  - Announcement PDFs and conversions → `tmp/company/listed/<company-slug>/announcements/`
  - Thematic and market reports → `tmp/general/`
- **Never save generated reports in `src/` or the repository root.**
- **Never remove `tmp/` from `.gitignore` or stage files in `tmp/`.**

---

## Data Reference

| File | Records | Columns / Schema | Used by |
|---|---|---|---|
| `bse_stocks.csv` | ~10,900 | Security Code, Issuer Name, Security Id, Security Name, Status, Group, Face Value, ISIN No, Instrument | `bse_announcements.py` (scrip code ↔ ticker resolution) |
| `mainboard_ipos.csv` | ~390 | id, name, listing_date, issue_size, ipo_url | `ipo_client.py`, direct lookup |
| `sme_ipos.csv` | ~980 | id, name, listing_date, issue_size, ipo_url | `ipo_client.py`, direct lookup |
| `ipo_descriptions.json` | ~390 | `{ "Company Name": "multi-paragraph business profile..." }` | Quick IPO triage without downloading RHP |
| `indian_market_taxonomy_5_tier.md` | 1,120 lines | 5-level hierarchy: Macro Sector → Sector → Industry → Basic Industry → Product/Niche | `theme-to-companies.md`, `peer-finder.md`, thematic research |

---

## Tool Catalog

All scripts live in `src/` and must be executed via `.venv/bin/python`. Use `--help` on any script for full options.

### Shared Utilities

| Script | Purpose | CLI |
|---|---|---|
| `src/common/scripts/pdf_to_markdown.py` | Convert PDF → Markdown, delete original | `.venv/bin/python src/common/scripts/pdf_to_markdown.py <pdf_path> [--keep-pdf]` |

### IPO Tools

| Script | Purpose | CLI |
|---|---|---|
| `src/company/ipo/scripts/ipo_client.py` | Search IPOs across boards, list issues, fetch metadata + RHP in one step | `.venv/bin/python src/company/ipo/scripts/ipo_client.py search "<name>" [--board both\|mainboard\|sme]`<br>`.venv/bin/python src/company/ipo/scripts/ipo_client.py list [--board both\|mainboard\|sme]`<br>`.venv/bin/python src/company/ipo/scripts/ipo_client.py details <id_or_url> --fetch-rhp --to-markdown` |
| `src/company/ipo/scripts/fetch_rhp.py` | Download RHP/DRHP from SEBI/exchange URLs (fallback) | `.venv/bin/python src/company/ipo/scripts/fetch_rhp.py <url> [-c company_slug] [--to-markdown]` |

### Listed Equity Tools

| Script | Purpose | CLI |
|---|---|---|
| `src/company/listed/scripts/screener_scrape.py` | Scrape Screener.in → `screener.md` | `.venv/bin/python src/company/listed/scripts/screener_scrape.py <screener_url>` |
| `src/company/listed/scripts/financial_calculator.py` | Compute ratio tables, DuPont ROE, forensic screens | `.venv/bin/python src/company/listed/scripts/financial_calculator.py <input.json> [--template] [--wacc N] [--section NAME] [-o out.md]` |
| `src/company/listed/scripts/valuation_calculator.py` | 3-year multiples valuation, inversion, sensitivity | `.venv/bin/python src/company/listed/scripts/valuation_calculator.py <input.json> [--template] [--hurdle N] [-o out.md]` |
| `src/company/listed/scripts/bse_announcements.py` | Fetch BSE corporate announcements & filings | `.venv/bin/python src/company/listed/scripts/bse_announcements.py <symbol_or_code> [--orders-only] [--material-only] [--download N] [--convert-md]` |
| `src/company/listed/scripts/nse_announcements.py` | Fetch NSE corporate announcements & filings | `.venv/bin/python src/company/listed/scripts/nse_announcements.py <symbol> [--orders-only] [--material-only] [--download N] [--convert-md]` |

> **Tip:** For `financial_calculator.py` and `valuation_calculator.py`, run with `--template` first to see the expected JSON input schema. Prepare the JSON from `screener.md` data.

---

## Workflow Entry Points

### Listed Company Deep-Dive (4-Stage Framework)

1. **Start with** `src/company/listed/WORKFLOW.md` — master orchestrator containing execution rules, data ingestion commands, and prompts for Stages 1–4.
2. **Execute Stages sequentially:**
   - **Stage 1 (Business Model & Moat):** `checklists/1-business.md` -> `1-business-analysis.md`
   - **Stage 2 (Management & Governance):** `checklists/2-management.md` -> `2-management-analysis.md`
   - **Stage 3 (Financials & Valuation):** `checklists/3-financials.md` -> `3-financials-analysis.md` (Part A: forensics & cash flow with zero price; Part B: valuation collision, inversion & asymmetry with price).
   - **Stage 4 (Decision & Thesis):** `checklists/4-thesis.md` -> `4-thesis-analysis.md` (Strategic arc, 2–3 real risks, pre-committed kill triggers, capital sizing).
3. **Prerequisites & Tooling:**
   - **Step 0:** Generate `screener.md` in the company folder via `screener_scrape.py <screener_url>`.
   - **Financials Priority:** Give strict priority to Audited Annual Reports (Notes to Accounts) over portal aggregates.
   - **Stage 3 Tools:** Use `financial_calculator.py` for forensics/DuPont, `peer-finder.md` for peer selection, and `valuation_calculator.py` for multiples and 3-year inversion.
   - **Style Invariants:** Plain conversational English, no consulting fluff, and STRICTLY NO LaTeX formatting.
4. **Reference material:** `src/common/docs/valuation-guide.md` contains Indian-market-specific DCF parameters (cost of equity 11–14%, terminal growth 4–6%) and a sector -> valuation metric cheat sheet. Consult it during Stage 3.
5. **PDF conversion:** When downloading annual reports, concalls, or investor presentations, convert them to markdown via `src/common/scripts/pdf_to_markdown.py` before reading.

### IPO Analysis

1. **Start with** `src/company/ipo/WORKFLOW.md` — master orchestrator containing execution rules, data ingestion commands, and prompts for both Mode 1 (Quick Review / Triage) and Mode 2 (Full Deep-Dive).
2. **Find the IPO:** Run `.venv/bin/python src/company/ipo/scripts/ipo_client.py search "<company name>"` to search across both mainboard and SME databases and get the exact ID.
3. **Pre-requisite ingestion:** Run `.venv/bin/python src/company/ipo/scripts/ipo_client.py details <id> --fetch-rhp --to-markdown` to ingest metadata and convert RHP into `tmp/company/ipo/<slug>/rhp.md` in a single command. Never do ad-hoc web searches for RHP PDFs.
4. **Analyze:** Follow `src/company/ipo/WORKFLOW.md` applying `checklists/quick-ipo.md` (Mode 1) or `checklists/full-ipo.md` (Mode 2). Base analysis strictly on RHP text.

### Thematic / Top-Down Research

- **Discover themes:** Run `src/general/theme-discovery.md` — scouts and ranks 10–20 themes.
- **Map theme → companies:** Run `src/general/theme-to-companies.md` — finds all NSE/BSE-listed companies exposed to a theme with 3-tier exposure classification. Use `data/indian_market_taxonomy_5_tier.md` as the sector reference.
- **Multi-order effects:** Run `src/general/order-of-effects.md` — maps causal chains (no tickers until Phase 6).

### Peer Selection

Run `src/company/listed/peer-finder.md` — deterministic procedure for assembling comparable-company sets for relative valuation.

---

## Research & Execution Guardrails

1. **Follow playbooks strictly.** When running an analysis, adhere to the relevant checklist under `src/` without skipping sections or hallucinating data.
2. **Evidence-first & cited:**
   - Every metric, market size, and financial figure must state its source and reference year (e.g., `FY25`).
   - If a number cannot be verified from filings or reliable portals, label it `[UNVERIFIED]` rather than fabricating or guessing.
3. **Primary sources prioritized:**
   - For IPOs: Base analysis on SEBI filings (RHP/DRHP).
   - For listed companies: Base analysis on annual reports, investor presentations, concalls, and verified portal aggregates (e.g., Screener.in).
4. **Token & context efficiency:**
   - Do not attempt to load full multi-hundred-page PDFs into agent context directly when targeted text extraction or summarized portal data is available.
5. **Use prescribed tools.** When `WORKFLOW.md` specifies a script for a step (e.g., `screener_scrape.py` for Step 3+, `financial_calculator.py` for Step 5, `valuation_calculator.py` for Step 6), use it. Do not substitute web searches for data the tool provides.
6. **`screener.md` is the primary data source for Steps 3–6.** If it doesn't exist in the company folder, generate it first via `screener_scrape.py` before starting the analysis step.

---

## Python Environment & Execution Invariant

- **Mandatory Virtual Environment:** A dedicated virtual environment is initialized at the repository root (`.venv/`).
- **ALWAYS execute Python through `.venv`:** Every Python script, module, pip install, or CLI execution MUST use `.venv/bin/python` or `.venv/bin/pip` (e.g., `.venv/bin/python <script_path>`).
- **NEVER use system/global Python:** Never invoke system `python` or `python3` directly. All environment isolation must be preserved within `.venv/`.
- **Dependencies:** `requirements.txt` lists all required packages. Install via `.venv/bin/pip install -r requirements.txt`.
- Target Python 3.10+ (current environment is Python 3.14+).
