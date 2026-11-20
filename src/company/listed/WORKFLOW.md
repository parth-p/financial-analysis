# Listed Company Analysis Workflow (Stages 1–4)

Master workflow rules, data source protocols, and execution prompts for listed Indian equity research.

---

## 1. Execution & Core Writing Rules

1. **Output Directory & File Naming:**
   - Look in `tmp/company/listed/` for an existing folder matching `<company name>`, its ticker, or slug (e.g., reuse `tmp/company/listed/automotive-axles-ltd/` if present). If none exists, create `tmp/company/listed/<company-slug>/`.
   - Each stage outputs a dedicated markdown report:
     - Stage 1: `tmp/company/listed/<company-slug>/1-business-analysis.md`
     - Stage 2: `tmp/company/listed/<company-slug>/2-management-analysis.md`
     - Stage 3: `tmp/company/listed/<company-slug>/3-financials-analysis.md`
     - Stage 4: `tmp/company/listed/<company-slug>/4-thesis-analysis.md`

2. **Simple, Plain Language:**
   - Write clearly and directly in everyday conversational English.
   - Avoid consulting fluff, Wall Street jargon, and over-complicated buzzwords. Describe the business, factory, customers, and cash flows as concrete real-world operations.

3. **STRICTLY NO LaTeX Formatting:**
   - Never use LaTeX syntax (such as `$$\mathbf{...}$$`, `\frac{...}{...}`, `\ge`, `\times`).
   - Use clean, standard Markdown formulas and symbols (e.g., `Downside % = [(Bear Price - CMP) / CMP] * 100%`, `>=`, `*`, `/`).

4. **Audited Annual Report Priority for Financials:**
   - For financial numbers, **give strict priority to Audited Annual Reports** (specifically the Notes to Accounts, Balance Sheet schedules, Cash Flow statements, and Auditor's Disclosures) over portal aggregates.
   - Portals like Screener.in are fast starting points, but always verify critical figures (cash balances, lease liabilities, contingent liabilities, CWIP aging, related-party transactions, segment margins) against the official annual report.

5. **Standalone vs. Consolidated Protocol:**
   - **Default:** Always analyze Consolidated financials for companies with operating subsidiaries or group entities.
   - **Standalone Exception:** Analyze Standalone financials if:
     1. The company is a single operating entity with no operating subsidiaries (e.g., Automotive Axles Ltd).
     2. Verifying parent-level debt, holding company cash leaks, or confirming whether cash is trapped at subsidiaries.

6. **Evidence-First & Fact vs. Assumption Tagging:**
   - Every metric, market share, capacity figure, and financial number must cite its source and reference period (e.g., `FY25 Annual Report`, `Q2 FY26 Investor Presentation`).
   - If a number cannot be verified from filings or reputable primary sources, label it `[UNVERIFIED]` rather than guessing.

---

## 2. Primary Data Sources & Tool Catalog

Always execute python scripts using the project's virtual environment: `.venv/bin/python`.

| Source Type | Primary Use Case & How to Fetch |
|---|---|
| **Screener.in** | Fast 10-year financial summary, peer comparisons, and links to official filings.<br>` .venv/bin/python src/company/listed/scripts/screener_scrape.py <screener_url>` |
| **Audited Annual Reports** | The bedrock for financial truth: Notes to Accounts, CWIP aging, Related Party Disclosures, Contingent Liabilities, and Auditor's Report.<br>Convert downloaded PDFs via: `.venv/bin/python src/common/scripts/pdf_to_markdown.py <pdf_path> [--keep-pdf]` |
| **Earnings Concall Transcripts** | Read 2–4 years of transcripts (including cyclical downturns) to assess management honesty, guidance delivery (say-do ratio), and real customer demand. |
| **Investor Presentations** | Visual breakdown of business segments, order book, customer profiles, and capacity expansions. |
| **Credit Rating Reports** | CRISIL, ICRA, CARE, India Ratings rationales. Invaluable for unvarnished bank debt details, working capital limits utilization, and parent support assumptions. |
| **Exchange Filings (BSE/NSE)** | Regulatory announcements: Regulation 30 (material contracts, capacity, senior management changes), Regulation 44 (shareholder voting results), Regulation 31 (shareholding & promoter pledge).<br>Fetch via: `.venv/bin/python src/company/listed/scripts/bse_announcements.py <symbol_or_code>` or `nse_announcements.py <symbol>` |
| **RHP / DRHP Filings** | For recently listed companies (last 1–3 years), fetch original prospectuses containing detailed industry studies and unit economics.<br>Fetch via: `.venv/bin/python src/company/ipo/scripts/fetch_rhp.py <url> [-c company_slug] [--to-markdown]` |
| **Industry & Web Research** | Association data (SIAM, CareEdge, Crisil MI&A, ICRA Industry reports, Gartner) and focused web searches. |

---

## 3. Workflow Prerequisites (Step 0)

Before executing any analytical stage, set up the company folder and base financial dataset:

1. **Find Screener Link:** Search web for `Screener.in <Company Name>`.
2. **Generate `screener.md`:**
   ```bash
   .venv/bin/python src/company/listed/scripts/screener_scrape.py <screener_url>
   ```
   This creates `tmp/company/listed/<company-slug>/screener.md`, which contains historical financial statements, ratios, and direct download links for annual reports and investor presentations.

---

## 4. The 4 Analytical Stages & Execution Prompts

Execute the 4 stages sequentially. Each stage builds on the facts verified in earlier stages.

```
+-----------------------------------------------------------------------------------+
| Stage 1: Business Model, Industry Arena & Moat (1-business.md)                    |
| Unit economics, value chain, pricing power, structural moat, industry headwinds   |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| Stage 2: Management, Capital Allocation & Governance (2-management.md)            |
| Promoter integrity, Say-Do ratio, RPT audit, dilution history, reinvestment skill|
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| Stage 3: Financial Forensics & Valuation Collision (3-financials.md)              |
| Part A: Forensic integrity, cash conversion, capital treadmill (NO PRICE)         |
| Part B: Multiple realities, 3-yr inversion, asymmetry & downside floor (WITH PRICE)|
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| Stage 4: Investment Decision, Strategic Arc & Thesis (4-thesis.md)                |
| Strategic arc (Past/Present/Future), asymmetry thesis, kill triggers, decision    |
+-----------------------------------------------------------------------------------+
```

---

### Stage 1: Business Model, Industry Arena & Moat

- **Checklist:** `src/company/listed/checklists/1-business.md`
- **Output:** `tmp/company/listed/<company-slug>/1-business-analysis.md`
- **Focus:** How the business actually makes money, what customer problem it solves, its position in the value chain, unit economics, industry structure, and whether a durable economic moat exists.

#### Execution Prompt
```text
I want to do a comprehensive Stage 1 Business Model, Industry Arena & Moat analysis of <Company Name>.
Strictly follow the checklist in src/company/listed/checklists/1-business.md.

Execution instructions:
1. Output File: tmp/company/listed/<company-slug>/1-business-analysis.md (reuse existing company folder in tmp/company/listed/ if present, else create it).
2. Writing Style: Plain, direct English. Avoid consulting jargon. No LaTeX math syntax (use clean markdown text).
3. Data Sources: Use screener.md in the company folder, Investor Presentations, Concall Transcripts, Annual Reports, and industry reports via web search.
4. Process: Systematically cover each section of 1-business.md:
   - What the company sells, to whom, and how it gets paid (real-world product flow)
   - Value chain map and bargaining power against suppliers and customers
   - Real unit economics, margin structure, and operating leverage
   - Capacity footprint, utilization, and brownfield/greenfield expansion plans
   - Licensing, technology, and joint venture dependencies
   - Industry arena, competitive landscape, and regulatory guardrails
   - Moat identification and the 5 empirical moat falsification tests
5. Conclude with Section 8: The Business Model & Moat Verdict (Moat Classification, Fragility Points, and Key Uncertainties).
Do not guess. If information is unavailable or unverified, state it plainly.
```

---

### Stage 2: Management, Capital Allocation & Governance

- **Checklist:** `src/company/listed/checklists/2-management.md`
- **Output:** `tmp/company/listed/<company-slug>/2-management-analysis.md`
- **Prior Input:** Read `tmp/company/listed/<company-slug>/1-business-analysis.md`.
- **Focus:** Promoter integrity, say-do track record across historical downcycles, related-party transaction leakages, share dilution and pledging, promoter compensation vs. minority dividends, and reinvestment track record.

#### Execution Prompt
```text
I want to do a comprehensive Stage 2 Management, Capital Allocation & Governance analysis of <Company Name>.
Strictly follow the checklist in src/company/listed/checklists/2-management.md.

Execution instructions:
1. Output File: tmp/company/listed/<company-slug>/2-management-analysis.md.
2. Prior Step Input: Read 1-business-analysis.md in the company folder to understand business context.
3. Writing Style: Plain, direct English. Avoid corporate fluff. No LaTeX math syntax.
4. Data Sources: Use screener.md, Annual Reports (Mandatory: Related Party Disclosures, Director's Report, Corporate Governance Report), Concall transcripts (track guidance given 2–4 years ago vs. actual audited outcomes), BSE/NSE filings for Reg 31 (pledge) and Reg 44 (voting results). Convert PDFs using src/common/scripts/pdf_to_markdown.py when needed.
5. Process: Systematically cover each section of 2-management.md:
   - Promoter pedigree, ownership skin in the game, and pledge history
   - The Say-Do Audit: Multi-year guidance tracking table vs. audited reality
   - Capital allocation track record: 5-to-10 year Sources and Uses of Cash table
   - Related Party Transaction (RPT) audit: Loans, shared services, brand royalties, or routing sales/purchases through promoter-owned entities
   - Dilution & equity hygiene: Historical share count changes, warrants, preferential allotments
   - Remuneration vs. Return: Total promoter/executive compensation vs. PAT and minority dividends
   - Shareholder democracy & board independence: Red flags in shareholder votes or auditor qualifications
6. Conclude with Section 8: The Governance & Capital Allocation Verdict (Integrity Grade, Capital Allocator Profile, and Critical Governance Gaps).
```

---

### Stage 3: Financial Forensics & Valuation Collision

- **Checklist:** `src/company/listed/checklists/3-financials.md`
- **Output:** `tmp/company/listed/<company-slug>/3-financials-analysis.md`
- **Prior Input:** Read `1-business-analysis.md` and `2-management-analysis.md`.
- **Special Architecture:**
  - **Part A: Financial Forensics & Real Cash Flows (SEPARATE FROM PRICE):** Audit earnings quality, 10-year cash conversion, working capital integrity, debt structure, contingent liabilities, and Core Operating ROIC vs. WACC.
  - **Part B: Valuation Collision (PRICE INTRODUCED):** Peer-benchmarked multiples, 3-year financial inversion (what growth/margin/multiple is baked into CMP for a 15% hurdle?), scenario distribution (Bear, Base, Bull), and asymmetric risk-reward assessment.

#### Helper Scripts for Stage 3:
1. **Financial Calculator:** Run quantitative screens and DuPont breakdown:
   ```bash
   .venv/bin/python src/company/listed/scripts/financial_calculator.py --template
   # Fill input JSON from screener.md / annual report, then run:
   .venv/bin/python src/company/listed/scripts/financial_calculator.py <input.json> --wacc 13 -o tmp/company/listed/<company-slug>/financial-calc-output.md
   ```
2. **Peer Finder:** Consult `src/company/listed/peer-finder.md` to select true operating peers.
3. **Valuation Calculator:** Run multiples, inversion, and sensitivity:
   ```bash
   .venv/bin/python src/company/listed/scripts/valuation_calculator.py --template
   # Fill input JSON, then run:
   .venv/bin/python src/company/listed/scripts/valuation_calculator.py <input.json> --hurdle 15 -o tmp/company/listed/<company-slug>/valuation-calc-output.md
   ```

#### Execution Prompt
```text
I want to do a comprehensive Stage 3 Financial Forensics & Valuation Collision analysis of <Company Name>.
Strictly follow the checklist in src/company/listed/checklists/3-financials.md.

Execution instructions:
1. Output File: tmp/company/listed/<company-slug>/3-financials-analysis.md.
2. Prior Step Inputs: Read 1-business-analysis.md and 2-management-analysis.md in the company folder.
3. Financial Data Priority: For all balance sheet and note-based numbers, give strict priority to Audited Annual Reports (Notes to Accounts) over portal numbers.
4. Writing Style: Plain, direct English. No LaTeX math syntax (use standard markdown equations).
5. Part A Protocol (Zero Price): Complete Sections 1 through 7 with ZERO reference to current stock price or market capitalization. Focus purely on forensic integrity, cash conversion, capital treadmill, balance sheet health, and Core Operating ROIC vs. WACC.
6. Part B Protocol (Valuation Collision): In Sections 8 through 12, introduce market price and enterprise value. Execute peer benchmarking, 3-year inversion math (solving for implied growth/multiples at a 15% hurdle rate), 3-scenario financial modeling (Bear, Base, Bull), and compute the Risk-Reward Asymmetry Ratio and Margin of Safety.
7. Conclude with Section 13: The Financials & Valuation Verdict.
```

---

### Stage 4: Investment Decision, Strategic Arc & Thesis

- **Checklist:** `src/company/listed/checklists/4-thesis.md`
- **Output:** `tmp/company/listed/<company-slug>/4-thesis-analysis.md`
- **Prior Inputs:** Read `1-business-analysis.md`, `2-management-analysis.md`, and `3-financials-analysis.md`.
- **Focus:** Synthesizes the entire deep dive into an institutional investment memo:
  - Strategic Arc: The Past (origin & past cycle), The Present (current operational reality, headwinds & tailwinds), and The Likely Future (next 3–5 years).
  - The Asymmetry Thesis: Why the upside significantly outweighs downside risk.
  - The 2–3 Real Risks & Falsification Conditions.
  - Pre-Committed Kill Triggers: Specific, measurable operating conditions that mandate an immediate exit.
  - Key Monitoring Dashboard & Dated Catalysts.
  - Final Capital Allocation Decision: `BUY` (with portfolio % tier), `WATCHLIST` (with trigger price/event), or `PASS` (with dealbreaker reason).

#### Execution Prompt
```text
I want to do a definitive Stage 4 Investment Decision, Strategic Arc & Thesis memo for <Company Name>.
Strictly follow the checklist in src/company/listed/checklists/4-thesis.md.

Execution instructions:
1. Output File: tmp/company/listed/<company-slug>/4-thesis-analysis.md.
2. Prior Step Inputs: Read all three prior reports in the company folder:
   - 1-business-analysis.md
   - 2-management-analysis.md
   - 3-financials-analysis.md
3. Writing Style: Clear, decisive, plain English. No consulting jargon, no hand-waving, no LaTeX formatting.
4. Process: Systematically cover each section of 4-thesis.md:
   - Executive Summary Snapshot (Decision, CMP, Fair Value, Asymmetry Ratio, Margin of Safety, Portfolio Weight)
   - The Strategic Arc (The Past, The Present with Headwinds & Tailwinds, The Likely Future)
   - The Core Asymmetry Thesis (Why the risk/reward is heavily skewed in our favor)
   - The 2–3 Real Un-Priced Risks
   - Pre-Committed Kill Triggers (Precise fundamental breaches that trigger an immediate, non-negotiable exit)
   - Key Operating Metrics to Monitor (Quarterly tracking scorecard)
   - Catalysts & Value Realization Calendar (Dated events expected over the next 12–36 months)
   - Final Investment Committee Decision & Capital Sizing (BUY / WATCHLIST / PASS, with exact portfolio % allocation)
```

---

## 5. Quality Control & Red Flag Invariants

Before considering any listed company analysis complete:
1. **Never fabricate numbers:** If a metric (e.g., segment ROCE, CWIP breakdown, warranty claims) is not disclosed in filings, state `[UNVERIFIED - Not Disclosed in Filings]` rather than guessing.
2. **Reconciliation check:** Ensure net debt, shares outstanding, and tax rates match the audited annual report notes.
3. **Moat verification:** An assertion of a "moat" is invalid unless corroborated by Stage 3 Section 6 (Core Operating ROIC consistently > WACC and Incremental ROIC > WACC across cycles).
4. **Kill trigger clarity:** Every kill trigger must be an objective, verifiable operational number (e.g., "Receivables >6m exceeds 2% of revenue" or "Core ROIC drops below 13% for 2 consecutive years"), never a vague sentiment ("sentiment deteriorates").
