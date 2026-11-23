# Quarterly Results & Concall Diagnostic — Agent Playbook
*A deterministic, machine-executable runbook for dissecting quarterly/annual financial results, earnings call transcripts, and investor presentations for Indian listed companies (NSE/BSE). Written for an AI agent to execute end-to-end; readable by an institutional equity research analyst.*

**Scope:** Applicable to any Indian listed company reporting quarterly (Q1, Q2, Q3, Q4) or full-year annual financial results. Consumes SEBI Regulation 33 financial filings, concall transcripts, and investor presentations. **Not** a superficial PR summary; an institutional diagnostic of core operating numbers, footnote forensics, segmental mix shifts, operational intelligence, management tone changes, and forward commitment tracking.

---

## 0. Operating Principles (The Agent Invariants)

1. **No Management Monologue Regurgitation:** Management opening remarks in a concall and press release bullet points are pre-scripted corporate PR. Summarize management's opening narrative in **at most one short paragraph**, then immediately pivot to the hard audited numbers, footnote disclosures, and the analyst Q&A session.
2. **Sequential (QoQ) Over Year-on-Year (YoY):** While the media focuses on YoY numbers, YoY growth is frequently distorted by low or high base effects from the previous year. Always analyze sequential Quarter-on-Quarter (QoQ) performance first to measure true operational momentum, contextualized against the sector's historical Indian seasonal cycle.
3. **The Notes to Accounts Invariant (Where the Bodies Are Buried):** Never take reported EBITDA or PAT at face value. The agent must read every numbered footnote in the SEBI Regulation 33 "Notes to Accounts". Check for: exceptional items, prior-period adjustments, CWIP/R&D expense capitalization, deferred tax adjustments, and statutory auditor qualifications or emphasis of matter.
4. **Core Operating Truth (Excluding Non-Operating Noise):** Compute **Core Operating EBITDA** by stripping out Other Income (treasury income, mutual fund gains, interest on tax refunds, foreign exchange fluctuations) and exceptional items. Measure the **Gross Spread** (Gross Margin in bps delta) to gauge real pricing power against raw material inflation.
5. **The Analyst Grill & Evasion Tracker:** The primary signal in an earnings call lives in the Q&A session. Track:
   - What were the top 3 hardest questions analysts pressed management on?
   - Where did management evade, hedge, or promise to *"share details offline"*?
   - Have management's adjectives and tone shifted compared to previous quarters (e.g., from *"strong visible growth"* to *"cautiously optimistic amidst headwinds"*)?
6. **Graceful Say-Do & Forward Commitments Register:** You cannot verify past guidance from a single concall in isolation. The agent must:
   - Extract past guidance failures directly from the Q&A (where analysts confront management on past targets).
   - If prior concalls exist in `tmp/company/listed/<slug>/`, compare against them directly.
   - Emit a structured **Forward Commitments Register** logging every new date, number, margin target, and capex deadline promised today, creating the baseline for subsequent quarters.
7. **The Q2 & Q4 Balance Sheet Invariant:** In India, companies are legally mandated to publish full Balance Sheets and Cash Flow Statements only with **Q2 (Half-Yearly)** and **Q4 (Annual)** filings. For Q2 and Q4 runs, the agent must audit working capital expansion, cash conversion, and net debt changes.
8. **STRICTLY NO LaTeX Formatting:** Use plain Markdown formulas and standard arithmetic symbols (`*`, `/`, `+`, `-`, `>=`, `<=`). Never use `$$`, `\frac`, `\times`, or LaTeX tags.
9. **Provenanced & Dated Facts:** Every revenue number, margin delta, capacity metric, and management quote must cite its source document and period (e.g., `Q2 FY27 Reg 33 Note 4`, `Concall Transcript Page 8`).

---

## 1. Input & Invocation

**How to invoke:**
```text
RUN CONCALL ANALYSIS company="<Ticker | Company Name>" period="<e.g., Q2 FY27 | Q4 FY26 | FY26 Annual>" [results_doc="<path/url>"] [concall_doc="<path/url>"] [ppt_doc="<path/url>"]
```

*Examples:*
- `RUN CONCALL ANALYSIS company="Poly Medicure" period="Q2 FY27"`
- `RUN CONCALL ANALYSIS company="GRCL" period="Q1 FY27"`
- `RUN CONCALL ANALYSIS company="Tata Motors Ltd" period="Q4 FY26"`

### Document Ingestion & Preparation Protocol:
If local document paths are not explicitly provided in the command, the agent uses the repository's automation scripts to retrieve and convert them:
1. **Locate Documents:** Search `tmp/company/listed/<company-slug>/screener.md` or execute:
   - `.venv/bin/python src/company/listed/scripts/nse_announcements.py <symbol> --download 5` or
   - `.venv/bin/python src/company/listed/scripts/bse_announcements.py <scrip_code> --download 5`
2. **Convert PDFs to Markdown:** Run the converter utility:
   - `.venv/bin/python src/common/scripts/pdf_to_markdown.py <pdf_path>`
3. **Ingest Three Primary Sources:**
   - **Source A (Mandatory):** Regulation 33 Financial Results (P&L, Segmental, Notes to Accounts, and Balance Sheet if Q2/Q4).
   - **Source B (Mandatory):** Concall Earnings Transcript.
   - **Source C (Optional but Recommended):** Investor Presentation / Earnings Deck.

**Output Destination:**
- Listed deep-dive folder: `tmp/company/listed/<company-slug>/concall-<period-slug>.md`
- Standalone / Ad-hoc: `tmp/company/adhoc/<company-slug>-concall-<period-slug>.md`

---

## 2. The 7 Analytical Stages

```
+-----------------------------------------------------------------------------------------+
| Stage 0: Historical Baseline & Indian Seasonality Context                               |
+-----------------------------------------------------------------------------------------+
                                            │
                                            ▼
+-----------------------------------------------------------------------------------------+
| Stage 1: The Clean Numbers Audit & Footnote Forensics (Regulation 33 Review)            |
+-----------------------------------------------------------------------------------------+
                                            │
                                            ▼
+-----------------------------------------------------------------------------------------+
| Stage 2: Segmental Health & Product Mix Divergence (The Blended Illusion)               |
+-----------------------------------------------------------------------------------------+
                                            │
                                            ▼
+-----------------------------------------------------------------------------------------+
| Stage 3: The Operational Intelligence Radar (The 5 Core Buckets)                        |
+-----------------------------------------------------------------------------------------+
                                            │
                                            ▼
+-----------------------------------------------------------------------------------------+
| Stage 4: Concall Q&A & Management Grill Session (Evasions, Tonality, Toughest Probes)   |
+-----------------------------------------------------------------------------------------+
                                            │
                                            ▼
+-----------------------------------------------------------------------------------------+
| Stage 5: Forward Commitments Register & Say-Do Verification                             |
+-----------------------------------------------------------------------------------------+
                                            │
                                            ▼
+-----------------------------------------------------------------------------------------+
| Stage 6: Balance Sheet Pulse (Q2 / Q4 Check) & Thesis Delta                             |
+-----------------------------------------------------------------------------------------+
```

---

### STAGE 0 — Historical Baseline & Indian Seasonality Context

**Objective:** Contextualize the reported quarter against the multi-quarter financial baseline and Indian seasonal patterns.

**Procedure:**
1. **Load Historical Baseline:** Read `screener.md` to establish the trailing 4-to-8 quarter run-rate for Revenue, Gross Margin %, EBITDA %, and Net Profit.
2. **Identify Sector Seasonality Anchor:** Explicitly state the quarterly seasonality archetype for this industry:
   - *Q1 Surge (Summer / Agri Season):* Cooling/ACs, beverages, agrochemical pre-sowing placements. Construction slows.
   - *Q2 Slump (Monsoon Quarter):* Cement, construction materials, infrastructure, mining, commercial vehicles, and real estate hit seasonal lows.
   - *Q3 Surge (Festive Season):* Autos, consumer durables, retail, textiles, jewelry, and paints surge due to Diwali, Dussehra, and wedding season.
   - *Q4 Flush (Fiscal Year-End):* Capital goods, EPC, defense, electrical equipment, and IT hardware surge due to government budget flushing and corporate year-end Capex completions.
3. **Seasonality Sanity Check:** Did sequential revenue/margin moves follow or contradict the sector's historical seasonal pattern?

---

### STAGE 1 — The Clean Numbers Audit & Footnote Forensics

**Objective:** Strip out non-operating distortions from the Regulation 33 filing to isolate the true core operating performance.

**Procedure:**
1. **Headline vs. Core Operating Metric Table:**
   - *Revenue from Operations:* Reported ₹ Cr (QoQ % and YoY %). Decompose into Volume vs. Realization growth if disclosed.
   - *Raw Material Costs & Gross Margin:* Material cost % of sales; Gross Margin % (QoQ bps change and YoY bps change). State whether gross spread expanded or compressed.
   - *Core Operating EBITDA:* `Operating Revenue - Raw Material Costs - Employee Expenses - Other Operating Expenses`. **Strictly exclude Other Income**.
   - *Core Operating EBITDA Margin (%):* Core EBITDA / Revenue from Operations. Compare QoQ and YoY.
   - *Other Income Analysis:* Identify Other Income as a % of Profit Before Tax (PBT). If Other Income represents >15% of PBT, flag as a quality-of-earnings distortion.
   - *Reported PAT & Diluted EPS:* Net profit and EPS (QoQ % and YoY %).
   - *Effective Tax Rate:* `Tax Expense / PBT`. Flag if significantly different from the standard corporate rate of ~25.17%.
2. **Regulation 33 Footnote Forensics (Notes to Accounts):**
   - Read all numbered notes in the statutory filing and document findings:
     - *Exceptional Items:* Disclose any one-off asset sales, insurance receipts, litigation provisions, or voluntary retirement schemes (VRS).
     - *Expense Capitalization:* Did the company capitalize interest or operating expenses into CWIP or intangible assets?
     - *Auditor Comments:* Note any qualifications, reservations, adverse remarks, or "Emphasis of Matter" paragraphs.
     - *Accounting Policy Changes:* Any modification in depreciation schedules, lease accounting (Ind AS 116), or revenue recognition policies.

---

### STAGE 2 — Segmental Health & Product Mix Divergence

**Objective:** Uncover internal divergence across business divisions to verify whether high-margin core products are growing or low-margin commodity lines are masking underlying weakness.

**Procedure:**
1. **Segment Financial Matrix:** Extract Regulation 33 Segment Disclosures:
   | Segment Name | Segment Revenue (₹ Cr) | QoQ Growth (%) | YoY Growth (%) | Segment EBIT (₹ Cr) | Segment EBIT Margin (%) | Margin Delta (bps QoQ) |
   |---|---|---|---|---|---|---|
2. **The Mix Shift Diagnostic:**
   - Which segment was the primary growth driver this quarter?
   - Did the revenue contribution of the highest-margin segment expand or contract as a % of total revenue?
   - Is low-margin trading or commodity volume artificially inflating top-line revenue while dragging blended margins?

---

### STAGE 3 — The Operational Intelligence Radar (The 5 Core Buckets)

**Objective:** Extract all material operational intelligence revealed across the concall, results release, and investor presentation.

**Procedure:**
Sweep the documents across the five mandatory intelligence categories:

1. **Forward Guidance & Quantitative Targets:**
   - Explicit management targets for full-year revenue growth, volume CAGR, and EBITDA margins.
   - Full-year guidance changes: Reconfirmed, Upgraded, Downgraded, or Quietly Dropped.
2. **Capex, Plant Expansions & Commercial Operation Dates (COD):**
   - Status of every major under-construction greenfield and brownfield facility.
   - Specific COD dates: On schedule vs. delayed (state the exact delay in months and the cited reason).
   - Capex budget revisions: Are project costs escalating beyond original approvals?
   - Capacity utilization rate of existing mature plants vs. newly commissioned lines.
3. **Supply Chain, Raw Materials & Pricing Mechanics:**
   - Price trajectory of key raw material inputs (chemicals, polymers, metals, crude derivatives, freight).
   - Pass-through lag status: Exact time lag to pass cost increases to customers (e.g., 30 days vs. quarterly formulaic PVC vs. fixed-price exposure).
   - Domestic and global supply chain bottlenecks (container freight rates, port congestion, import restrictions).
4. **Commercial Traction, Order Book & Client Wins:**
   - New client empanelments, vendor code approvals, or OEM platform nominations.
   - Customer losses, in-sourcing by key clients, or contract non-renewals.
   - Order backlog status: Unexecuted order book (₹ Cr), fresh order inflows during the quarter, execution duration, and book-to-bill ratio.
   - Export markets: Status of regulatory audits (US FDA, EU CE MDR, ANVISA), warning letters, or export tariff impacts.
5. **Corporate Actions, Governance & Senior Leadership:**
   - Management transitions: Resignations or appointments of CFO, CEO, COO, or Statutory Auditor.
   - Capital allocation announcements: Dividend declarations, preferential warrants, buybacks, or QIP/rights issue plans.
   - Statutory, legal, or tax notices: Environmental notices from SPCB, GST/income tax demands, or litigation developments.

---

### STAGE 4 — Concall Q&A & Management Grill Session

**Objective:** Interrogate the analyst Q&A session to detect evasions, analyst pushback, and subtle shifts in management tone.

**Procedure:**
1. **The Top 3 Toughest Analyst Questions:**
   - Identify the three hardest, most probing questions asked by institutional analysts during the call.
   - Summarize the specific question and management's exact response.
2. **The Evasion & "Offline Deflection" Tracker:**
   - Document any question where management:
     - Gave an evasive non-answer or long philosophical generality instead of numbers.
     - Promised to *"share that offline"* or *"let the IR team follow up"*.
     - Refused to provide customary segment or volume data.
3. **Management Demeanor & Tonality Shift:**
   - Evaluate management's demeanor: Confident & metric-driven vs. Defensive, hurried, or overly promotional.
   - Track adjective changes compared to prior quarters: Did management's language transition from aggressive optimism to cautious qualification?

---

### STAGE 5 — Forward Commitments Register & Say-Do Verification

**Objective:** Audit past promises where possible and record new dated commitments to build institutional memory for future tracking.

**Procedure:**
1. **Past Say-Do Verification:**
   - Did analysts cite specific past guidance in the Q&A? Document what was promised vs. what was delivered this quarter.
   - If prior concall analyses exist in `tmp/company/listed/<slug>/`, cross-check current numbers against the previous *Forward Commitments Register*.
   - Classify past guidance delivery: **Delivered (Say = Do)** / **Partially Delivered** / **Missed (Excuse Given)** / **Target Goalposts Shifted**.
2. **The New Forward Commitments Register (To Be Tracked Next Quarter):**
   - Populate the forward tracking table for all explicit quantitative promises made during this call:
     | Metric / Project Promised | Stated Forward Target | Promised Target Period / Deadline | Verification Metric |
     |---|---|---|---|
     | [e.g., Full-Year Revenue] | [e.g., ₹500 Cr (+25% YoY)] | FY27 Full Year | Audited Annual P&L |
     | [e.g., EBITDA Margin] | [e.g., 20% to 22%] | H2 FY27 | Q3/Q4 Results |
     | [e.g., Plant 3 COD] | [e.g., Commercial production in Q4] | March 2027 | Reg 30 Exchange Filing |
     | [e.g., Debt Reduction] | [e.g., Pay off ₹50 Cr debt] | By end of FY27 | Year-end Balance Sheet |

---

### STAGE 6 — Balance Sheet Pulse (Q2 / Q4 Check) & Thesis Delta

**Objective:** Audit working capital and leverage deltas (when balance sheets are filed) and determine whether this quarter's results alter the long-term investment thesis.

**Procedure:**
1. **Balance Sheet & Working Capital Pulse (Mandatory for Q2 & Q4; Skip for Q1 & Q3 if BS not filed):**
   - Trade Receivables & Debtor Days: Did receivables grow faster than sales?
   - Inventory & Inventory Days: Is inventory accumulating, signaling unsold finished goods?
   - Working Capital Cash Absorption: Calculate Operating Cash Flow (CFO) to EBITDA conversion ratio (`CFO / Core EBITDA`). Is it >=75%, or is cash locked up in working capital?
   - Net Debt & Borrowings: Did short-term or long-term debt increase during the 6-month / 12-month period?
2. **Impact on the Core Investment Thesis:**
   - Classify this quarter's net impact on the investment thesis:
     - **Strengthened:** Operational execution exceeded expectations; moats widening; earnings upgrades likely.
     - **Intact / Neutral:** Performance aligned with baseline expectations; thesis unchanged.
     - **Weakened:** Structural margins compressing, capex delayed, or working capital deteriorating. Place on Watchlist.
     - **Broken (Kill Trigger Fired):** An explicit pre-committed kill condition (from `4-thesis.md`) has fired.
3. **Pre-Committed Kill Condition Audit:**
   - Check if any operational, financial, or governance kill triggers established in Stage 4 of the research framework were triggered this quarter.
4. **Street Consensus & Earnings Outlook:**
   - Are sell-side consensus earnings estimates likely to be: **Upgraded (>=5%)**, **Maintained**, or **Downgraded (>=5%)** following this print?

---

## 3. Structured Output Document Template

The agent must output the final report using this exact markdown schema:
`tmp/company/listed/<company-slug>/concall-<period-slug>.md`

```markdown
# Results & Concall Diagnostic: [Company Name] ([Period])

**Ticker:** [NSE: TICKER / BSE: CODE]  
**Period Analyzed:** [e.g., Q2 FY27 / Q4 FY26 / FY26 Annual]  
**Financial Result Date:** YYYY-MM-DD | **Concall Date:** YYYY-MM-DD  
**Report Date:** YYYY-MM-DD  
**Analyst Engine:** Antigravity Equity Research Framework  

---

## Executive Diagnostic & Core Verdict

- **Quarterly Performance Verdict:** [Strong Beat / Inline / Operational Miss / Low-Quality Beat via Other Income]
- **Thesis Delta:** [Strengthened / Intact / Weakened / Broken (Kill Trigger Fired)]
- **Street Estimate Trajectory:** [Consensus Upgrades Likely / Neutral / Downgrades Expected]
- **The Core Analytical Takeaway:** [2–3 sentences summarizing the real operational story behind the headline numbers]

---

## 1. Historical Baseline & Seasonality Context

- **Sector Seasonality Archetype:** [Q1 Summer Surge / Q2 Monsoon Slump / Q3 Festive Spike / Q4 Fiscal Year-End Flush]
- **Seasonal Conformity:** [Did results conform to seasonal norms or show unseasonal strength/weakness? Explain.]
- **Trailing 4-Quarter Run-Rate Context:** [Brief context on revenue and margin trends leading into this quarter]

---

## 2. The Clean Numbers Audit & Footnote Forensics

### Core Financial Performance Matrix
| Financial Metric | Reported Value | QoQ Growth (%) | YoY Growth (%) | Operational Commentary |
|---|---|---|---|---|
| **Revenue from Operations** | ₹[X] Cr | [X]% | [Y]% | [Volume vs. Realization breakdown] |
| **Gross Margin (%)** | [X]% | [+/- X] bps | [+/- Y] bps | [Raw material spread expansion/compression] |
| **Core Operating EBITDA** (ex-Other Income) | ₹[X] Cr | [X]% | [Y]% | [Operating leverage / overhead drag impact] |
| **Core EBITDA Margin (%)** | [X]% | [+/- X] bps | [+/- Y] bps | [True operating profitability] |
| **Other Income** | ₹[X] Cr | [X]% | [Y]% | [[X]% of PBT; Quality of earnings verdict] |
| **Profit Before Tax (PBT)** | ₹[X] Cr | [X]% | [Y]% | |
| **Effective Tax Rate (%)** | [X]% | — | — | [Normal (~25%) vs. Tax write-back/anomaly] |
| **Reported Net Profit (PAT)** | ₹[X] Cr | [X]% | [Y]% | |
| **Diluted EPS** | ₹[X] | [X]% | [Y]% | |

### Regulation 33 Footnote Forensics (Notes to Accounts)
- **Exceptional / One-Off Items:** [None / Detailed description of exceptionals in Note X]
- **Expense Capitalization Check:** [None / Note X reveals ₹X Cr capitalized into CWIP/Intangibles]
- **Auditor Qualifications & Emphasis of Matter:** [Clean / Details of any auditor reservations]
- **Accounting Policy Changes:** [None / Modifications to depreciation, revenue recognition, etc.]

---

## 3. Segmental Health & Product Mix Divergence

| Segment / Division | Revenue (₹ Cr) | QoQ (%) | YoY (%) | EBIT (₹ Cr) | EBIT Margin (%) | Margin Delta (bps QoQ) |
|---|---|---|---|---|---|---|
| [Segment 1] | ₹[X] | [X]% | [Y]% | ₹[X] | [X]% | [+/- X] bps |
| [Segment 2] | ₹[X] | [X]% | [Y]% | ₹[X] | [X]% | [+/- X] bps |

- **Mix Shift Diagnostic:** [Did high-margin core products grow or decline as a % of mix? Is low-margin volume masking weakness?]

---

## 4. The Operational Intelligence Radar

### 1. Forward Guidance & Targets
- **Revenue Target:** [Target volume/value growth for FY / next year]
- **Margin Guidance:** [Target EBITDA / Gross margin range]
- **Guidance Trajectory:** [Reconfirmed / Upgraded / Lowered / Dropped / Not Provided]

### 2. Capex, Expansions & COD Timelines
- **Active Projects & COD Dates:** [Plant-by-plant progress, commercial operation dates, and schedule updates]
- **Capex Budget Revisions:** [On-budget vs. Cost overruns]
- **Capacity Utilization:** [Mature plant utilization % vs. ramp-up curve of new assets]

### 3. Raw Materials & Supply Chain
- **Input Cost Environment:** [Inflation / deflation in key commodities; current price trends]
- **Pass-Through Lag:** [Contractual lag duration and gross margin protection status]
- **Supply Bottlenecks:** [Freight rates, domestic/import shortages, port congestion]

### 4. Commercial Traction & Order Book
- **Client Empanelments & Wins:** [New OEM/institutional accounts won]
- **Customer Losses / Contract Expiries:** [Any client attrition or insourcing threats]
- **Order Book Status:** Total Backlog: ₹[X] Cr | Inflows this Quarter: ₹[Y] Cr | Book-to-Bill: [Z]x | Execution Timeline: [X] months
- **Export Certifications:** [US FDA, CE MDR, foreign audit updates]

### 5. Corporate Actions, Governance & Senior Leadership
- **Leadership Changes:** [CFO, CEO, or auditor transitions]
- **Capital Allocation:** [Dividends, warrant issuances, buybacks, QIP plans]
- **Statutory / Legal Notices:** [Tax disputes, NGT/SPCB environmental notices, litigation]

---

## 5. Concall Q&A & Management Grill Session

### Top 3 Toughest Analyst Questions
1. **[Analyst Name / Firm]:** *"[Question on margin pressure / project delay / working capital]"*  
   **Management Response:** [Detailed summary of management's explanation]
2. **[Analyst Name / Firm]:** *"[Question]"*  
   **Management Response:** [Summary]
3. **[Analyst Name / Firm]:** *"[Question]"*  
   **Management Response:** [Summary]

### The Evasion & "Offline Deflection" Tracker
- **Evaded Questions / Data Refusals:** [List any questions where management dodged or gave vague platitudes]
- **"Offline" Deflections:** [List any items management promised to take offline or have IR share later]

### Management Demeanor & Tonality Shift
- **Demeanor Assessment:** [Confident & metric-driven / Defensive / Promotional / Cautious]
- **Language / Adjective Shift:** [Document any subtle shifts in terminology compared to earlier quarters]

---

## 6. Forward Commitments Register & Say-Do Verification

### Past Say-Do Verification (Audit of Past Promises)
- **Past Promises Tested This Quarter:** [What was guided previously vs. actual reported numbers today]
- **Say-Do Delivery Verdict:** [Delivered / Partially Delivered / Missed / Goalposts Shifted]

### New Forward Commitments Register (To Track in Subsequent Quarters)
| Metric / Milestone Promised | Stated Forward Target | Promised Target Period / Deadline | Verification Metric |
|---|---|---|---|
| [Target 1] | [Number / Guideline] | [Target Quarter / Year] | [Filing line item / announcement] |
| [Target 2] | [Number / Guideline] | [Target Quarter / Year] | [Filing line item] |
| [Target 3] | [Number / Guideline] | [Target Quarter / Year] | [Filing line item] |

---

## 7. Balance Sheet Pulse (Q2 / Q4) & Thesis Delta

*(Section 7.1 is populated for Q2 and Q4 runs; omitted for Q1/Q3 if Balance Sheet is not published)*

### 7.1 Balance Sheet & Working Capital Health (Q2 / Q4 Only)
- **Trade Receivables:** ₹[X] Cr (Debtor Days: [X] days vs. [Y] days in prior period)
- **Inventories:** ₹[X] Cr (Inventory Days: [X] days vs. [Y] days in prior period)
- **Operating Cash Flow Conversion (CFO / EBITDA):** [X]% (Cash generative vs. Working capital sponge)
- **Net Debt & Borrowings:** Total Debt: ₹[X] Cr (Change of ₹[+/- X] Cr over last 6/12 months)

### 7.2 Investment Thesis & Kill Trigger Audit
- **Impact on Core Investment Thesis:** [Strengthened / Intact / Weakened / Broken]
- **Kill Condition Check:** [State whether any pre-committed operational or financial kill triggers fired]
- **Next Key Milestone to Track:** [The single most critical operational data print to watch next quarter]

---

## Research Audit & Provenance Log
- **Documents Ingested:** [List exact PDF/text file paths and dates for Results, Concall, and Presentation]
- **Unverified Items Tagged:** [Any management commentary that could not be reconciled against audited figures]
```

---

## 4. Execution Summary (One-Line Workflow)

> **Ingest results, concall, and presentation documents (Stage 0) -> audit clean operating numbers, gross spread bps, and Regulation 33 footnotes (Stage 1) -> analyze segmental mix shifts (Stage 2) -> sweep the 5-bucket operational intelligence radar (Stage 3) -> interrogate concall Q&A for evasions and tone shifts (Stage 4) -> verify past Say-Do and register new forward commitments (Stage 5) -> audit balance sheet working capital deltas and thesis impact (Stage 6) -> emit structured report to `tmp/company/listed/<company-slug>/concall-<period>.md`.**
