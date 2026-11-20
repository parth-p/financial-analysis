# IPO Quick Review — Analyst's Triage Checklist

*The 25-to-40 minute institutional triage screen. Run this on every IPO in the window to evaluate the transaction, the business engine, industry defensibility, accounting forensics, and valuation before deciding whether to APPLY, WAIT, or PASS, and whether to escalate to a full deep-dive. Structured modules, complete operational depth, zero consulting fluff.*

> **The Epistemological Discipline:**
> - **Informed Insider Asymmetry:** An IPO is a transaction initiated by insiders who selected the listing window, groomed the financial statements, and determined the price band. The burden of proof rests entirely on the deal.
> - **RHP Landmark Anchors:** Ground every probe in specific RHP chapters (*Capital Structure*, *Objects of the Offer*, *Our Business*, *Industry Overview*, *Restated Financials & Notes*, *Basis for Issue Price*, *Litigation*). Do not rely on generic web searches or portal summaries.
> - **Zero Text Blobs:** Use structured tables, clear subheadings, and concrete bullets. If a table communicates the offering matrix, 3-year cash flow conversion, receivables aging, or peer multiples better than prose, use a table.
> - **No Artificial Brevity Constraints:** Explain the operational machine, industry dynamics, and forensic findings with complete clarity. Strip filler, but never compromise on load-bearing operational depth.
> - **The 6-Stage Narrative Arc:** Every complete triage follows the investor's natural mental model:
>   `1. The Deal (Transaction) → 2. The Business (Machine) → 3. Industry & Moat (Arena & Durability) → 4. Forensics (Ledger Truth) → 5. Valuation (Price Collision) → 6. Verdict (Decision)`

---

## The Triage Probe Set

---

### §1. The Deal & Insider Arbitrage

*Identify who is selling, what they paid, how much cash exits the business, and where the fresh capital goes. Sourced from RHP chapters: Capital Structure & Objects of the Offer.*

- [ ] **Issue Structure & Insider Cash-Out:**
  - Total offer size (₹ Cr at cap price).
  - Split between **Fresh Issue** (₹ Cr and %) and **Offer for Sale (OFS)** (₹ Cr and %).
  - Who sells in the OFS (Promoters vs. PE/institutional investors), and what percentage of **their own pre-issue holding** are they offloading? (A promoter selling 5% for float compliance vs. selling 40%+ of their stake).
- [ ] **Promoter & Seller WACA vs. Cap Price:**
  - Extract the Weighted Average Cost of Acquisition (WACA) for promoters and major selling shareholders from *Capital Structure*.
  - Calculate their gain multiple at the cap price: `Gain Multiple = Cap Price / WACA`.
  - **The Synthetic WACA Check:** Did recent loan conversions, preferential allotments, or share consolidations artificially inflate the reported WACA? Reconcile back to the cash acquisition cost of their pre-bonus founding shares.
- [ ] **Pre-IPO Equity Games & Valuation Arbitrage:**
  - **Bonus Issues & Stock Splits:** Did the company execute aggressive bonus issues (e.g., 5:1, 10:1, or 1000:1) or stock splits in the last 12–24 months to cosmetically lower the nominal per-share price?
  - **Recent Private Transaction Benchmark:** Did any PE fund, strategic investor, or promoter acquire, convert (CCPS/loans), or transfer shares in the last 12–24 months? At what valuation/share price? Compute the markup the public is asked to pay: `Markup % = [(Cap Price - Recent Round Price) / Recent Round Price] * 100%`.
- [ ] **Objects of the Offer Forensic Dissection:**
  - Complete the proceeds allocation table for the Fresh Issue:
    | Category | Amount Allocated (₹ Cr) | % of Fresh Issue | Appraisal Status (Bank Appraised / Management Estimate) |
    |---|---|---|---|
    | **Growth Capex (Greenfield / Brownfield / Equipment)** | | | |
    | **Debt Repayment / Prepayment** | | | |
    | **Incremental Working Capital** | | | |
    | **General Corporate Purposes (GCP)** | | | |
    | **Issue Expenses** | | | |
    | **Total Gross Fresh Proceeds** | | 100.0% | |
  - *Capex Verification:* Is capex appraised by a scheduled commercial bank/monitoring agency, or based solely on internal management estimates and vendor quotations?
  - *Debt Repayment Check:* Trace the specific borrowings being repaid from the Objects schedule. Are funds repaying third-party bank term loans, or are they repaying unsecured loans from promoter entities or bridge facilities?
  - *GCP Flag:* Is GCP pushing the statutory 20%–25% regulatory ceiling with vague deployment milestones?

---

### §2. Business Model & Operating Machine

*Map what the company physically produces or delivers, its native unit economics, its operating headroom, and its customer relationships. Sourced from RHP chapter: Our Business.*

- [ ] **The Offering & Segment Matrix:**
  Complete the table for all material revenue lines:
  | Segment / Product Line | Physical Product / Service Delivered | Concrete End Application | % of Revenue | Contract Pricing Basis (Fixed / PVC Pass-Through / Spot / Tender) |
  |---|---|---|---|---|
- [ ] **Value Proposition & Customer Decision:**
  - What economic problem does the customer solve by hiring or buying from this company?
  - *The Alternative:* What is the customer's real alternative? (Make in-house, buy equipment outright via capex, hire a competitor, or use manual labor?).
  - What is physically shipped/invoiced vs. what economic outcome is the customer actually paying for?
- [ ] **Native Unit Economics:**
  - What native unit metric governs this business model?
    - *For Asset Rental / Equipment Fleet:* Purchase cost per unit, monthly rental yield (%), asset turnover, maintenance cost per machine, and payback period (years).
    - *For Manufacturing:* Realization per tonne/unit, raw material conversion spread, and scrap recovery.
    - *For Logistics / Services:* Revenue per employee/operator, operating cost per vehicle, and fleet utilization %.
- [ ] **Physical Asset Footprint & Expansion Headroom:**
  - Facilities, plants, or operational warehouses: Locations, owned freehold land vs. leased (and whether leased from promoter entities).
  - State nameplate installed capacity or fleet size in physical units (tonnes, meters, pieces, machines) and current capacity utilization (%).
  - Can the company expand revenue through existing brownfield infrastructure, or is it running at peak utilization requiring a greenfield capex step-cliff?
  - What percentage of products are manufactured in-house vs. contract-manufactured / imported for trading?
- [ ] **Customer Qualification, Criticality & Manpower Dependency:**
  - Buyer profile: Direct OEMs vs. Tier-1 integrators vs. 3PL logistics vs. EPC contractors vs. government agencies vs. retail distributors.
  - What commercial hurdles are required to win vendor code empanelment: First Article Inspection (FAI), PPAP Level 3/4 sign-offs, customer plant audits, or statutory certifications (UL, FM, USFDA, IATF, CE)? How long is the qualification lead time?
  - **The "Who Gets Fired?" Test (Customer Criticality):** If this product or service fails in the field, does it risk catastrophic loss (line halt, plant explosion, vehicle recall), while costing <2%–3% of the customer's total bill of materials?
  - **Manpower / Staffing Model:** Is this a pure asset/software model, or a labor-intensive operation? Number of direct operational workers/drivers on payroll, employee cost as % of revenue, and annual labor attrition rate (%).
- [ ] **Customer Concentration & Pricing Pass-Through:**
  - Concentration: Top 1 customer % and Top 10 customers % of revenue.
  - **Price Variation Clause (PVC):** How does the company handle raw material, fuel, or wage inflation? Is there an explicit contract pass-through formula, and what is the reset time-lag (monthly, quarterly, bi-annually)? (A 90-day lag causes sharp gross margin volatility during commodity price spikes).

---

### §3. Industry Arena & Moat Assessment

*Deconstruct the pond the company swims in, expose commissioned report biases, and evaluate whether excess returns are structurally defensible. Sourced from RHP chapters: Industry Overview and Our Business.*

- [ ] **Industry Arena & Macro Growth Drivers:**
  - What is the estimated market size (in ₹ Cr or $M) and underlying historical/projected volume growth rate?
  - What secular operational shifts are driving demand? (e.g., transition from capex equipment purchasing to opex rental; GST-driven warehouse consolidation; stringent ESG/safety regulations; supply-chain formalization).
  - Is demand secular or cyclical, and where is the industry currently situated in the economic cycle?
- [ ] **Deconstructing the Commissioned Industry Report (The Bias Check):**
  - Who authored the independent industry report (CRISIL, CareEdge, Frost & Sullivan, Technopak)?
  - **The Gerrymandering Audit:** How did they define the market? Did they artificially gerrymander the market into a hyper-narrow micro-niche so the company can claim *"We are the #1 player"*?
  - What is the real, unvarnished Addressable Market (TAM / SAM) across India once artificial filters are removed?
- [ ] **Industry Structure & Competitive Dynamics:**
  - Is the industry fragmented or consolidated, and what is the organized vs. unorganized split?
  - Pricing rationality: Is the industry disciplined, or plagued by unorganized price-cutting and tender underbidding?
  - Threat of low-cost imports (e.g., Chinese machinery/components) or alternative technological substitutes.
- [ ] **Structural Moat Identification & Testing:**
  - Does the company possess an authentic, verifiable economic moat? Identify the structural source:
    - *Switching Costs:* Multi-year customer integration, ERP lock-in, mission-critical failure risk.
    - *Structural Cost Advantage:* Favorable geographic location, proprietary tooling, lower operating cost per unit.
    - *Intangibles / Regulatory Approvals:* Exclusive distribution rights, specialized patents, 10-year customer empanelment libraries.
    - *Network Density / Scale:* Unmatched fleet density, regional branch network, rapid maintenance turnaround.
  - **The Commodity Verdict:** If none of these sources provide a durable barrier, explicitly label the business: **"No Structural Moat / Commoditized Operator"**.
- [ ] **The Replication Test:**
  - What would a well-capitalized competitor need to replicate this business in 2 to 3 years with ₹50–₹100 Cr of capital?
  - Can equipment be bought off-the-shelf from OEMs? Where exactly does a new entrant get stuck (customer vendor codes, driver staffing, client trust, balance sheet scale)?

---

### §4. Pre-IPO Accounting Forensics & Earnings Quality

*Audit the restated financial statements for pre-IPO grooming, cash conversion, receivables aging, and contingent liabilities. Sourced from RHP chapters: Restated Financial Information, MD&A, and Outstanding Litigation.*

- [ ] **Pre-IPO Margin Jump & Stub-Period Check:**
  - Track EBITDA and PAT margins across FY-2, FY-1, the pre-IPO Filing Year, and the Interim Stub Period. Did margins suddenly jump in the 12 months immediately preceding the RHP filing?
  - Did the company annualize a bumper 3-month or 6-month stub period that was boosted by seasonal bunched billing or channel stuffing?
- [ ] **The 3-Year Cash Conversion Reality Check:**
  Complete the cash conversion table from the Restated Cash Flow Statement:
  | Metric (₹ Cr) | FY-2 | FY-1 | Pre-IPO Full Year | Interim Stub Period | Cumulative 3-Yr Total |
  |---|---|---|---|---|---|
  | **Restated Profit After Tax (PAT)** | | | | | |
  | **Operating Cash Flow (CFO)** | | | | | |
  | **CFO / PAT Conversion Ratio (%)** | | | | | |
  | **Capital Expenditure (Capex)** | | | | | |
  | **Free Cash Flow (FCF = CFO - Capex)** | | | | | |
  - **The Cash Conversion Red Flag:** Is Cumulative CFO substantially lower than Cumulative PAT (CFO/PAT < 60%)?
  - **The Free Cash Flow Reality:** Is Free Cash Flow (FCF) positive, or does the capex treadmill consume more cash than operations generate (negative cumulative FCF)?
- [ ] **Trade Receivables Aging Schedule (>6 Months Old):**
  - Extract the mandatory trade receivables aging schedule from the Restated Notes to Accounts:
    | Receivables Metric (₹ Cr) | FY-2 | FY-1 | Pre-IPO Full Year | Latest Stub Period |
    |---|---|---|---|---|
    | **Total Trade Receivables** | | | | |
    | **Receivables Outstanding > 6 Months** | | | | |
    | **% of Receivables > 6 Months Old** | | | | |
  - Are overdue receivables (>6 months) or unbilled revenues surging faster than top-line sales, indicating customer payment friction or aggressive revenue recognition?
- [ ] **Balance Sheet Solvency & Leverage:**
  - Total Borrowings, Cash & Bank Balances, and Net Debt.
  - Net Debt / EBITDA ratio and Interest Coverage ratio.
  - What will Net Debt look like post-listing after the debt repayment portion of the Fresh Issue is applied?
- [ ] **Contingent Liabilities & Litigation vs. Net Worth:**
  - Extract total disputed claims from *Outstanding Litigation*: Direct tax demands, indirect tax (GST/customs/excise) notices, civil disputes, and commercial arbitration against the company or promoters.
  - Calculate exposure: `Disputed Claims % = (Total Quantified Claims / Net Worth) * 100%`. (If >25%–30%, an adverse ruling threatens equity solvency).

---

### §5. True Peer Benchmarking & Valuation Reality

*Collide the IPO price band against true operating peers, actively filtering out merchant banker flattery. Sourced from RHP chapter: Basis for Issue Price and independent peer screens.*

- [ ] **Quarantine & Expose RHP Cherry-Picked Peers:**
  - Which listed peers did the merchant bankers present in *Basis for Issue Price*?
  - **Falsification Check:** Why are these peers mismatched? (e.g., comparing a contract manufacturer to high-multiple consumer brands, a forklift rental operator to a pallet-pooling platform, or an SME to an industry giant).
- [ ] **True Peer Comparison Matrix:**
  Identify 2 to 4 true operating peers (matching business model, customer concentration, and economic profile) and complete the comparison:
  | Company Name | Business / Segment Match | Market Cap (₹ Cr) | P/E Ratio (TTM / FY) | EV/EBITDA | ROCE (%) | EBITDA Margin (%) | Debtor Days | 3-Yr CFO / PAT (%) |
  |---|---|---|---|---|---|---|---|---|
  | **Target IPO (at Cap Price)** | **Subject Company** | | | | | | | |
  | **Real Peer 1** | | | | | | | | |
  | **Real Peer 2** | | | | | | | | |
  | **Real Peer 3** | | | | | | | | |
  | **RHP Peer (Excluded Cherry-Pick)** | | | | | | | | |
- [ ] **Valuation Multiples on Normalized & Forward Earnings:**
  - Compute multiples at upper price band:
    - P/E on Trailing Pre-IPO Normalized PAT.
    - P/E on Forward Normalized PAT (accounting for interest expense savings from IPO debt repayment).
    - EV/EBITDA on pre-IPO operating EBITDA.
    - Price-to-Book (P/BV) against post-issue Net Asset Value (NAV).
- [ ] **The Valuation Verdict:**
  - Does the IPO price band command a discount, parity, or premium relative to the median of **real operating peers**?
  - Given the target's cash conversion track record, fleet/capacity age, and return ratios, is this multiple justified, or are investors paying a premium for pre-IPO window dressing?

---

### §6. Supply Cliffs & Triage Verdict

*Synthesize the findings into an actionable decision, map post-listing lock-in supply releases, and test against disqualifying kill gates.*

- [ ] **Post-Listing Lock-In Supply Calendar:**
  Map the upcoming supply release milestones from *Capital Structure*:
  | Milestone | Release Date (from Listing) | Shares Unlocked | % of Total Post-Issue Capital | Potential Supply Overhang Risk |
  |---|---|---|---|---|
  | **30-Day Anchor Lock-in** | 30 days post-allotment | 50% of Anchor portion | | |
  | **90-Day Anchor Lock-in** | 90 days post-allotment | Remaining 50% of Anchor | | |
  | **6-Month Pre-IPO Lock-in** | 6 months post-allotment | Non-promoter pre-IPO holders | | |
  | **1-Year Promoter Lock-in** | 12 months post-allotment | 50% of excess Promoter stake | | |
  | **2-Year Promoter Lock-in** | 24 months post-allotment | Remaining excess Promoter stake | | |
  | **3-Year Minimum Promoter Lock-in** | 36 months post-allotment | Mandatory 20% Promoter stake | | |
- [ ] **The 5 Knockout Kill Gates (Pass / Fail):**
  - **Gate 1 (Governance Integrity):** Has the statutory auditor resigned or become CFO/KMP? Are promoter shares pledged? Are there active criminal charges against promoters or core revenue assets? `[PASS / FAIL]`
  - **Gate 2 (Proceeds Siphoning):** Is the issue 100% OFS while treasury cash was drained pre-IPO? Do fresh proceeds repay promoter-controlled unsecured loans or unappraised capex? `[PASS / FAIL]`
  - **Gate 3 (Cash Conversion & Aging):** Is 3-year cumulative CFO negative or <40% of PAT? Are receivables >6 months old growing faster than revenue (>15%–20% of receivables)? `[PASS / FAIL]`
  - **Gate 4 (Valuation Sanity):** Is the IPO priced at a material premium (>30%) to real operating peers despite equal or inferior cash generation? `[PASS / FAIL]`
  - **Gate 5 (Solvency & Litigation):** Do quantified tax demands, regulatory claims, or contingent liabilities exceed 30% of Net Worth? `[PASS / FAIL]`

---

## The Triage Deliverable Template

```markdown
# <Company Name> — IPO Quick Triage

## §1. The Deal & Insider Arbitrage
- **Offer Structure & Proceeds:** Total offer size ₹____ Cr. Fresh Issue ₹____ Cr (___%), OFS ₹____ Cr (___%). Promoters selling ___% of their holding.
- **WACA vs. Cap Price:** Promoter WACA is ₹____/sh; selling shareholders WACA is ₹____/sh. At cap price of ₹____, insiders realize a ____× multiple on cost. Reconciled cash acquisition cost of pre-bonus founding equity is ₹____/sh (____× markup).
- **Pre-IPO Rounds & Capital Structuring:** [Recent private rounds / Bonus issues / Stock splits]. Public markup is ____% over the last private round.
- **Use of Fresh Proceeds:**
  | Category | Amount Allocated (₹ Cr) | % of Fresh Issue | Appraisal Status |
  |---|---|---|---|
  | Growth Capex | | | |
  | Debt Repayment | | | |
  | Working Capital | | | |
  | GCP | | | |
  | Total | | 100.0% | |
  - *Capex Verification:* [Bank-appraised vs. Management estimates].
  - *Debt Repayment Check:* [Third-party bank debt vs. Promoter-controlled loans].
  - *GCP Flag:* [Amount and % of issue].

## §2. Business Model & Operating Machine
- **Offering & Segment Matrix:**
  | Segment / Product Line | Physical Product / Service Delivered | Concrete End Application | % of Revenue | Contract Pricing Basis |
  |---|---|---|---|---|
- **Value Proposition & Customer Decision:** [Why customers buy/hire, customer's real alternatives, what is physically delivered vs economic outcome].
- **Native Unit Economics:** [Asset purchase cost, monthly rental / conversion spread, payback period, asset turnover].
- **Physical Footprint & Expansion Headroom:** [Facilities, owned vs leased from promoters, capacity/fleet size, utilization %, brownfield headroom vs capex step-cliff].
- **Customer Qualification & Staffing Model:** [Empanelment lead times, PPAP/vendor codes, "Who gets fired?" criticality test, workforce size, operator wages as % of revenue, labor attrition %].
- **Concentration & Pricing Pass-Through:** Top 1 customer: ___%, Top 10: ___%. Price Variation Clause (PVC) terms and reset lag.

## §3. Industry Arena & Moat Assessment
- **Industry Arena & Secular Drivers:** [Market size, projected CAGR, structural shifts e.g. capex to opex, warehousing growth].
- **Commissioned Report Audit:** [Report author, gerrymandered niche definitions exposed, real unvarnished TAM].
- **Industry Structure & Competitive Dynamics:** [Organized vs unorganized split, pricing discipline, import/substitute threats].
- **Moat Identification & Durability:** [Structural moat source (switching costs, cost advantage, intangibles, scale) OR verdict: No Structural Moat / Commoditized Operator].
- **The Replication Test:** [What ₹50–100 Cr and 2–3 years can replicate; where a well-funded competitor gets stuck].

## §4. Pre-IPO Accounting Forensics
- **Pre-IPO Margin Jump & Stub Check:** [Trend across FY-2, FY-1, Pre-IPO FY, and Stub Period].
- **3-Year Cash Conversion Table:**
  | Metric (₹ Cr) | FY-2 | FY-1 | Pre-IPO Full Year | Interim Stub Period | Cumulative 3-Yr Total |
  |---|---|---|---|---|---|
  | Restated PAT | | | | | |
  | Operating Cash Flow (CFO) | | | | | |
  | CFO / PAT Conversion (%) | | | | | |
  | Capex | | | | | |
  | Free Cash Flow (FCF) | | | | | |
- **Receivables Aging (>6 Months):** Receivables >6 months represent ₹____ Cr (___% of total receivables), trending [up/down]. Debtor days stand at ____ days.
- **Solvency & Litigation:** Net Debt is ₹____ Cr. Quantified disputed litigation/tax claims total ₹____ Cr (___% of Net Worth).

## §5. True Peer Benchmark & Valuation Reality
- **RHP Peer Bias Falsification:** RHP presents [Peers] at median P/E of ____×. Falsified because [Reasons for mismatch].
- **Real Peer Comparison Table:**
  | Company Name | Business Match | Market Cap (₹ Cr) | P/E (TTM) | EV/EBITDA | ROCE (%) | OPM (%) | Debtor Days | CFO / PAT (%) |
  |---|---|---|---|---|---|---|---|---|
  | **Target Company (at Cap)** | Subject Company | | | | | | | |
  | **Real Peer 1** | | | | | | | | |
  | **Real Peer 2** | | | | | | | | |
- **Valuation Multiples:** Upper band implies ____× P/E on normalized PAT (____× forward post-debt-repayment) and ____× EV/EBITDA. Trades at [premium/discount] to real peers.

## §6. Supply Cliffs & Triage Verdict
- **Lock-in Supply Calendar:**
  | Milestone | Release Date | Shares Unlocked | % of Capital | Overhang Risk |
  |---|---|---|---|---|
  | 30-Day Anchor | | | | |
  | 90-Day Anchor | | | | |
  | 6-Month Pre-IPO | | | | |
  | 1-Year / 2-Year / 3-Year Promoter | | | | |
- **5 Knockout Kill Gates:** Gate 1 [P/F], Gate 2 [P/F], Gate 3 [P/F], Gate 4 [P/F], Gate 5 [P/F].

---

## Verdict & Triage Decision

> **Final Call: [APPLY (Fundamental) / WAIT (For 30/90-Day Lock-in Cliff or Lower Price) / PASS]**
> - **Primary Decision Rationale:** (3–4 load-bearing operational/forensic reasons, most decisive first).
> - **What Flips the Call:** (Price target, cash conversion proof, or specific operational resolution).
> - **Top 2 Observable Kill Tripwires:**
>   1. 
>   2. 
> - **Escalate to Full Deep-Dive? [Yes → run full-ipo.md / No → stop here]**
```
