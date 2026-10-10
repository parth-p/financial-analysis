# Equity Analysis

A structured framework and toolset for Indian equity research, covering listed companies (NSE/BSE), IPOs, investment themes, and value-chain mapping.

---

## Quick Start

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
.venv/bin/pip install -r requirements.txt
```

---

## What You Can Do

### Listed Company Deep-Dive (8-Pillar Framework)
Structured analysis across 8 pillars — business model, industry, moat & guidance, management, financials, valuation, risks, and thesis. Each step has a checklist in `src/company/listed/checklists/` and automation scripts for financial calculations, screener scraping, and announcement fetching. Start with `src/company/listed/WORKFLOW.md`.

### IPO Analysis
Screen and analyze upcoming/recent IPOs using structured checklists (`src/company/ipo/checklists/`). Tools fetch IPO metadata from Chittorgarh and download RHP filings from SEBI.

### Theme Discovery
Scout, research, and rank investment themes across multiple time horizons using `src/general/theme-discovery.md`.

### Theme → Companies
Map a theme through its value chain to find all NSE/BSE-listed companies with exposure, classified into 3 tiers. See `src/general/theme-to-companies.md`.

### Multi-Order Effects Mapping
Trace the causal chain of a theme to surface non-obvious beneficiaries using `src/general/order-of-effects.md`.

---

## Project Structure

```
analysis/
├── data/           # Static reference data (BSE stocks, IPO lists, sector taxonomy)
├── src/
│   ├── common/     # Shared utilities (PDF converter, valuation guide)
│   ├── company/
│   │   ├── ipo/    # IPO checklists and tools (fetch_rhp, ipo_client)
│   │   └── listed/ # 8-pillar framework: checklists, workflow, and scripts
│   └── general/    # Top-down playbooks (themes, effects mapping)
└── tmp/            # Generated outputs (gitignored)
```

See [AGENTS.md](AGENTS.md) for the full annotated file tree, tool catalog, data reference, and execution conventions.

---

## For AI Agents

All agent-facing conventions — directory rules, tool usage, workflow entry points, data schemas, and research guardrails — are documented in [AGENTS.md](AGENTS.md). Read it before running any analysis.

---

*Disclaimer: This framework is for educational and research purposes only. It is not investment advice. Markets carry risk. Consider consulting a SEBI-registered investment adviser before making investment decisions.*
