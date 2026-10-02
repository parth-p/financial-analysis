# Repository Guidelines

**Purpose:** Structured Indian equity research (NSE/BSE listed equities, IPOs, investment themes, and value chains).

---

## Directory Organization

```text
analysis/
├── .gitignore               # Ignores tmp/, .venv/, __pycache__, *.pyc, .DS_Store
├── data/                    # Static reference data (e.g., NSE master lists EQUITY_L.csv, SME_EQUITY_L.csv)
├── src/                     # Source methodology, playbooks, checklists, and automation tools
│   ├── company/
│   │   ├── ipo/             # IPO playbooks (full/quick checklists) and tools (fetch_rhp, run_ipo)
│   │   └── listed/          # 8-pillar listed equity framework & peer benchmarking protocols
│   └── general/             # Top-down playbooks: theme discovery, multi-order analysis, value-chain mapping
└── tmp/                     # Ephemeral scratchpad & output repository (GITIGNORED BY DESIGN)
    ├── company/
    │   ├── ipo/             # Downloaded RHP PDFs, parsed text files, and generated IPO reports
    │   └── listed/          # Generated listed equity research reports and peer comparisons
    └── general/             # Generated theme discovery, sector, and value-chain reports
```

---

## Output Routing & Storage Rules

- **`tmp/` is untracked on purpose:** All generated analysis markdown files, scrapers' intermediate files, raw RHP PDFs, and converted `.txt` files MUST be saved under the appropriate `tmp/` subdirectory:
  - IPO reports and downloads: `tmp/company/ipo/`
  - Listed company reports: `tmp/company/listed/`
  - Thematic and market reports: `tmp/general/`
- **Never save generated reports in `src/` or the repository root.**
- **Never remove `tmp/` from `.gitignore` or stage files in `tmp/`.**

---

## Research & Execution Guardrails

1. **Follow playbooks strictly:** When running an analysis, adhere to the relevant checklist under `src/` without skipping sections or hallucinating data.
2. **Evidence-first & cited:**
   - Every metric, market size, and financial figure must state its source and reference year (e.g., `FY25`).
   - If a number cannot be verified from filings or reliable portals, label it `[UNVERIFIED]` rather than fabricating or guessing.
3. **Primary sources prioritized:**
   - For IPOs: Base analysis on SEBI filings (RHP/DRHP).
   - For listed companies: Base analysis on annual reports, investor presentations, concalls, and verified portal aggregates (e.g., Screener.in).
4. **Token & context efficiency:**
   - Do not attempt to load full multi-hundred-page PDFs into agent context directly when targeted text extraction or summarized portal data is available.

---

## Python Environment & Execution Invariant

- **Mandatory Virtual Environment:** A dedicated virtual environment is initialized at the repository root (`.venv/`).
- **ALWAYS execute Python through `.venv`:** Every Python script, module, pip install, or CLI execution MUST use `.venv/bin/python` or `.venv/bin/pip` (e.g., `.venv/bin/python <script_path>`).
- **NEVER use system/global Python:** Never invoke system `python` or `python3` directly. All environment isolation must be preserved within `.venv/`.
- Target Python 3.10+ (current environment is Python 3.14+).

