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
│   │   │   │   ├── full-ipo.md          # Comprehensive 9-section IPO deep-dive checklist
│   │   │   │   └── quick-ipo.md         # Rapid triage checklist (decide: apply / pass / escalate)
│   │   │   └── scripts/
│   │   │       ├── fetch_rhp.py         # Download RHP/DRHP from SEBI/exchange URLs → tmp/company/ipo/
│   │   │       └── ipo_client.py        # Chittorgarh API client: list IPOs, fetch details, trigger RHP download
│   │   │
│   │   └── listed/          # Listed equity research (8-pillar framework)
│   │       ├── WORKFLOW.md              # ★ Master orchestrator: step-by-step prompts for Steps 1–6
│   │       ├── peer-finder.md           # Deterministic peer-selection runbook for relative valuation
│   │       ├── checklists/              # The 8 analytical pillars (execute in order)
│   │       │   ├── 1-business-model.md      # Step 1: Describe the machine (no judgment)
│   │       │   ├── 2-industry.md            # Step 2: Judge the pond, not the fish
│   │       │   ├── 3-moat-guidance.md       # Step 3: Return durability — moat + management guidance
│   │       │   ├── 4-mgmt-capital-allocation.md  # Step 4: Management competence & capital allocation
│   │       │   ├── 5-financials.md          # Step 5: Test Steps 1–4 against the ledger
│   │       │   ├── 6-valuation.md           # Step 6: What's priced in vs. your view
│   │       │   ├── 7-risks.md               # Step 7: Permanent loss of capital risks & kill criteria
│   │       │   └── 8-others.md              # Step 8: Differentiated thesis, catalyst & position sizing
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
| `src/company/ipo/scripts/ipo_client.py` | List/search IPOs, fetch detailed metadata | `.venv/bin/python src/company/ipo/scripts/ipo_client.py list [--board mainboard\|sme\|both] [--year YYYY]` |
| | | `.venv/bin/python src/company/ipo/scripts/ipo_client.py details <id_or_url> [--fetch-rhp] [--to-markdown]` |
| `src/company/ipo/scripts/fetch_rhp.py` | Download RHP/DRHP from SEBI/exchange URLs | `.venv/bin/python src/company/ipo/scripts/fetch_rhp.py <url> [-c company_slug] [--to-markdown]` |

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

### Listed Company Deep-Dive (8-Pillar Framework)

1. **Start with** `src/company/listed/WORKFLOW.md` — it contains execution rules, step-by-step prompts, prerequisites, and tool integration for Steps 1–6.
2. Steps 7 (Risks) and 8 (Thesis) follow their checklists directly: `checklists/7-risks.md` and `checklists/8-others.md`.
3. **Prerequisites by step:**
   - Steps 1–2: Web search only (no tools needed).
   - Step 3+: `screener.md` must exist in the company folder. If missing, generate it first via `screener_scrape.py`.
   - Step 5: Also run `financial_calculator.py` to compute ratio tables and forensic screens.
   - Step 6: Also run `valuation_calculator.py` for multiples-based valuation and sensitivity analysis.
4. **Reference material:** `src/common/docs/valuation-guide.md` contains Indian-market-specific DCF parameters (cost of equity 11–14%, terminal growth 4–6%) and a sector → valuation metric cheat sheet. Consult it during Steps 5–6.
5. **PDF conversion:** When downloading annual reports, concalls, or investor presentations, convert them to markdown via `src/common/scripts/pdf_to_markdown.py` before reading.

### IPO Analysis

1. **Start with** `src/company/ipo/WORKFLOW.md` — master orchestrator containing execution rules, data ingestion commands, and prompts for both Mode 1 (Quick Review / Triage) and Mode 2 (Full Deep-Dive).
2. **Find the IPO:** Use `ipo_client.py list` to search, or look up in `data/mainboard_ipos.csv` / `data/sme_ipos.csv`. Quick triage descriptions are in `data/ipo_descriptions.json`.
3. **Pre-requisite ingestion:** Fetch metadata via `ipo_client.py details <id>` and download/convert RHP via `fetch_rhp.py <url> --to-markdown` into `tmp/company/ipo/<slug>/`.
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
