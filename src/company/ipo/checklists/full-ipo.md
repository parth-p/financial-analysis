# Full IPO Analysis — Institutional Deep-Dive Checklist

*The institutional primary-market equity research framework. Run this on every IPO that passes initial triage to build a definitive, evidence-backed investment memo. Grounded in RHP filings, primary ledgers, restated annexures, and operational physics. No consulting fluff, no artificial length restrictions, strictly no LaTeX formatting.*

> **The Epistemological Discipline:**
> - **Informed Insider Asymmetry:** An IPO is a transaction initiated by informed insiders who chose the timing, groomed the financials, and set the valuation band. Default stance is skepticism; the burden of proof rests entirely on the deal.
> - **The Strict Firewall: Part A (Zero Price) vs. Part B (Valuation Collision):** In Stage 5 (Part A), the stock price, market cap, and valuation multiples are strictly forbidden. Evaluate the business as an auditor dissecting restated ledgers and cash conversion. Price is introduced only in Stage 6 (Part B) to collide market expectations against operational reality.
> - **Operational Physics over DCF Fantasy:** Discard 10-year DCF hand-waving. Confine all valuation scenarios to a rigorous 3-year operational window (FY+1 to FY+3) anchored to installed plant capacity, funded expansions, and addressable market ceilings.
> - **Primary Filing Verification:** Reconcile all critical balance sheet schedules, CWIP aging, related-party disclosures, restatement adjustments, and contingent liabilities directly from the RHP Restated Notes to Accounts.
> - **The 6-Stage Narrative Arc:**
>   `§1. Deal Anatomy & Proceeds → §2. Business Model & Operations → §3. Industry & Moat → §4. Management & Governance → §5. Restated Forensics (Zero Price) → §6. Valuation Collision & Decision (With Price)`

---

## Executive Summary & Deliverable Template (Synthesized Last, Placed First)

The final deliverable in `tmp/company/ipo/<company-slug>/full-analysis.md` opens with this snapshot block:

```markdown
# <Company Name> — IPO Institutional Deep-Dive Memo

## Executive Summary & Investment Verdict Box

> **Final Decision: [APPLY TO OWN / APPLY TO FLIP / WAIT FOR LOCK-IN CLIFF / PASS]**
> - **Conviction Tier / Position Sizing:** [Tier 1 Core (5.0%–7.0%) / Tier 2 Tactical (3.0%–5.0%) / Speculative Flip / None (0%)]
> - **Upper Price Band:** ₹____ | **Implied Market Cap:** ₹____ Cr | **Implied Enterprise Value:** ₹____ Cr
> - **Base Case Fair Value Target (Year 3):** ₹____ (+____% upside) | **Bear Case Downside Floor:** ₹____ (-____% downside)
> - **Risk-Reward Asymmetry Ratio:** ____:1 (Base Upside % / |Bear Downside %|) | **Margin of Safety:** ____%
> - **The Core Variant Perception:** (In 2–3 sentences: What does the market believe that we believe is fundamentally wrong, what RHP evidence proves us right, and what will force the re-rating?)
> - **Top Pre-Committed Kill Trigger:** (The single observable operational or financial threshold that mandates an immediate exit).

### Key Offer & Forensic Facts Snapshot
| Metric | Reported Value | Forensic Finding / Audit Status |
|---|---|---|
| **Total Offer Size** | ₹____ Cr | Fresh: ₹____ Cr (___%) · OFS: ₹____ Cr (___%) |
| **True Economic OFS %** | ___% | Includes fresh proceeds used to repay promoter debt / buy promoter assets |
| **Promoter WACA vs. Cap Price** | ₹____/sh | Gain Multiple: ____× (Reconciled pre-bonus founding cost: ₹____/sh) |
| **Pre-IPO Private Round Markup** | ₹____/sh (Round Date: ____) | Public Issue Markup: ____% over last private round |
| **3-Year Cumulative PAT vs. CFO** | PAT: ₹____ Cr · CFO: ₹____ Cr | Cumulative Cash Conversion: ____% (FCF: ₹____ Cr) |
| **Trade Receivables > 6 Months** | ₹____ Cr (___% of receivables) | Trailing 3-year trend: [Expanding / Stable / Contracting] |
| **Net Debt (Post-Issue Adjusted)** | ₹____ Cr | Net Debt / EBITDA: ____× · Interest Coverage: ____× |
| **Quantified Litigation vs. Net Worth** | ₹____ Cr | Represents ____% of post-issue Net Worth |
| **Valuation at Upper Band** | P/E: ____× · EV/EBITDA: ____× | Real Peer Median: ____× P/E (RHP Cherry-Pick Median: ____×) |
| **Nearest Lock-In Supply Cliff** | 30-Day: ____ shares (____%) | 90-Day: ____ shares (____%) · 6-Month: ____ shares (____%) |
```

---

## §1. The Deal Anatomy, Capital Structure Archaeology & Proceeds Forensics

*Interrogate the transaction structure, uncover the historical equity cost base, and track every rupee of proceeds. Sourced from RHP chapters: Capital Structure & Objects of the Offer.*

- [ ] **1.1 Issue Architecture & True Economic OFS:**
  - Total offer size (₹ Cr) at floor and cap price.
  - Split between **Fresh Issue** (₹ Cr and %) and **Offer for Sale (OFS)** (₹ Cr and %).
  - **The Economic OFS Calculation:** Is the "Fresh Issue" genuinely funding enterprise growth, or is it an OFS in disguise?
    `Economic OFS % = [(Headline OFS + Fresh Proceeds Used to Buy Promoter Assets + Fresh Proceeds Repaying Promoter Debt) / Total Issue Size] * 100%`
  - Who is selling in the OFS? Complete the selling shareholder breakdown:
    | Selling Shareholder | Category (Promoter / PE / Angel / KMP) | Pre-Issue Shares Held | Shares Offered in OFS | % of Own Stake Liquidated | Retained Post-Issue Stake (%) |
    |---|---|---|---|---|---|
  - What signal does the exit pattern convey? (A promoter offloading 5% for statutory float compliance vs. selling 40%+ of their family stake; PE fund calendar end-of-life vs. strategic partner dumping).
- [ ] **1.2 Capital Structure Archaeology (Since Inception):**
  - Audit the mandatory RHP table of historical share capital build-up since incorporation:
    - Trace all equity share allotments: dates, issue price per share, cash vs. consideration other than cash.
    - **Bonus Issues & Stock Splits:** Document all historical bonus issues (ratios, dates, reserves capitalized) and share splits. Did the company execute aggressive bonus floods (e.g., 5:1, 10:1, or 1000:1) in the last 12–24 months to cosmetically reduce the nominal per-share price?
    - **Preferred Instruments & Conversions:** Track Compulsorily Convertible Preference Shares (CCPS), Compulsorily Convertible Debentures (CCDs), or warrants. What were the original conversion formulas and effective entry valuations?
- [ ] **1.3 WACA Forensics & Insider Gain Multiples:**
  - Extract the Weighted Average Cost of Acquisition (WACA) from *Capital Structure* for Promoters, Promoter Group, Selling Shareholders, and All Equity Shares.
  - Compute the gain multiple at the cap price: `Gain Multiple = Cap Price / WACA`.
  - **Synthetic WACA Exposure:** Did recent high-priced transactions (e.g., converting promoter debt at the IPO cap price or issuing shares to friendly parties right before filing) synthetically inflate the reported WACA? Reconcile back to the **true cash acquisition cost of pre-bonus founding shares** to uncover actual promoter profit multiples.
- [ ] **1.4 Pre-IPO Placement Valuation Arbitrage (Last 12–24 Months):**
  - Identify all equity issuances, private placements, rights issues, or secondary share transfers in the 12–24 months preceding the RHP:
    | Transaction Date | Investor Name | Instrument | Number of Shares | Price per Share (₹) | Total Consideration (₹ Cr) | Implied Company Valuation (₹ Cr) |
    |---|---|---|---|---|---|---|
  - Calculate the public markup: `Public Markup % = [(Cap Price - Private Round Price) / Private Round Price] * 100%`.
  - What fundamental milestones were achieved between that private round and today to justify the public markup, or is the public simply paying for liquidity?
- [ ] **1.5 Objects of the Offer Forensic Dissection:**
  - Complete the proceeds allocation table for the Fresh Issue:
    | Category | Amount Allocated (₹ Cr) | % of Fresh Issue | Appraisal Status (Bank Appraised / Management Estimate) | Deployment Timeline (FY+1 / FY+2 / FY+3) |
    |---|---|---|---|---|
    | **Growth Capex (Greenfield / Brownfield / Equipment)** | | | | |
    | **Debt Repayment / Prepayment** | | | | |
    | **Incremental Working Capital Requirements** | | | | |
    | **General Corporate Purposes (GCP)** | | | | |
    | **Estimated Issue Expenses** | | | | |
    | **Total Gross Fresh Proceeds** | | 100.0% | | |
  - *Capex Verification:* Is proposed capex backed by an independent appraisal by a scheduled commercial bank or financial institution, or based entirely on internal management estimates and vendor quotations? Audit vendor quotation dates and verify whether any suppliers are related parties.
  - *Debt Repayment Trail:* Mandatory audit of the borrowings schedule in *Objects of the Offer*:
    | Lender Name | Facility Type (Term Loan / Overdraft) | Sanctioned Amount (₹ Cr) | Outstanding Amount (₹ Cr) | Interest Rate (%) | Purpose of Original Borrowing | Repayment from IPO (₹ Cr) |
    |---|---|---|---|---|---|---|
    - Are proceeds repaying third-party bank capex debt, or unsecured loans and advances extended by promoter entities, directors, or bridge lenders?
  - *GCP Compliance:* Ensure General Corporate Purposes do not exceed statutory ceilings (≤25% under SEBI ICDR Reg 7 / ≤15% or ₹10 Cr for SME). Are deployment milestones clearly defined or an unmonitored slush fund?
  - *Monitoring Agency Mandate:* Name of monitoring agency appointed (mandatory if fresh issue > ₹100 Cr under Reg 41 / Reg 262), reporting frequency, and audit committee oversight terms.
- [ ] **1.6 Section Verdict:** One-line verdict on deal alignment:
  > **Deal Verdict:** Fresh ___% / OFS ___% (Economic OFS ___%); primary seller ______; WACA gain multiple ___× (pre-bonus founding cash multiple ___×); proceeds **[Build Real Asset Value / Fund Working Capital Drag / Bail Out Promoter Debt / Extract Cash]**.

---

## §2. Business Model, Operating Machine & Value Chain Economics

*Map the physical engine, customer economics, operational constraints, and commercial power. Sourced from RHP chapter: Our Business.*

- [ ] **2.1 The Complete Segment & Offering Matrix:**
  Complete the table for all material product lines and revenue streams:
  | Segment / Product Line | Physical Product / Service Delivered | Concrete End Application | % of Revenue | Gross Margin / Conversion Spread Profile | Contract Pricing Basis (Fixed / Indexed PVC / L1 Tender / Spot) | Key End-User Industry |
  |---|---|---|---|---|---|---|
- [ ] **2.2 Value Proposition & Customer Decision Economics:**
  - What concrete operational, economic, or regulatory problem does the customer solve by purchasing or hiring from this company?
  - **The Customer's Real Alternatives:**
    - Captive in-house fabrication or DIY execution.
    - Outright capex equipment purchase vs. opex rental/leasing.
    - Hiring unorganized regional jobbers or local commodity suppliers.
    - Substituting with alternative materials, automation, or manual labor.
  - What is physically invoiced (e.g., machined aluminum castings; 3-ton electric reach trucks; biological wastewater SBR hardware) vs. what economic outcome the customer actually buys (e.g., zero assembly line halts; 100% tax-deductible warehouse throughput; NGT effluent discharge compliance)?
- [ ] **2.3 Native Unit Economics & Operating Velocity:**
  - Define the sector's native operational primitives that govern gross profitability:
    - *Asset Rental / Fleet Operations:* Purchase cost per unit, monthly rental rate per machine, gross rental yield (%), direct operating cost (driver wage, maintenance/spares), net cash spread per machine, asset turnover, and fully loaded payback period in years.
    - *Precision Manufacturing / Engineering:* Realization per unit/tonne, raw material conversion spread per unit, power/fuel cost per unit, and scrap recovery %.
    - *Chemicals / API Formulations:* Product realization per kg, raw material consumption factor, batch yield %, and solvent recovery efficiency.
    - *Contract Manufacturing / EMS:* Component pass-through margin, assembly conversion fee per board, test yield %.
    - *B2B Logistics / Services:* Revenue per operator/route, fuel/maintenance cost per vehicle, and fleet utilization %.
- [ ] **2.4 Physical Asset Footprint & Expansion Headroom:**
  - Manufacturing facilities, assembly workshops, and warehousing hubs: Locations, owned freehold land vs. leased.
  - **The Related-Party Landlord Seam:** Does any plant, office, or depot sit on land or buildings leased from promoter-owned entities? Are lease agreements long-term, and are lease rents benchmarked to prevailing market rates?
  - **Installed Capacity & Utilization:**
    - State nameplate installed capacity in physical units (tonnes, meters, pieces, machine hours) across each major product line.
    - Historical capacity utilization (%) over the last 3 fiscal years and interim stub period.
    - Can the company double revenue through existing sheds via debottlenecking/brownfield additions, or is it running at peak utilization requiring greenfield land acquisition and utility setup?
  - **Manufacturing Depth vs. Trading / Contract Outsourcing:**
    - What percentage of the production chain is executed in-house (foundry casting, heat treatment, 5-axis CNC machining, proprietary PLC automation)?
    - What percentage of cost of goods sold represents contract-manufactured finished goods, semi-finished assemblies, or imported goods for outright trading?
- [ ] **2.5 Statutory, Regulatory & Environmental Ceilings:**
  - **Consent to Operate (CTO / CTE):** State Pollution Control Board (SPCB) consented capacity in physical units. Is current production running near the legal CTO cap?
  - Effluent treatment, Zero Liquid Discharge (ZLD) status, and hazardous waste permissions.
  - Statutory certifications: USFDA, EU GMP, IATF 16949, AS9100, CE, UL, FM, BIS Quality Control Orders (QCOs). Audit cycles, upcoming re-inspection dates, and warning letter history.
- [ ] **2.6 Supply Chain, Inputs & Pricing Pass-Through Architecture:**
  - Top 3 raw material inputs (e.g., alloy steel, copper, specialized chemical intermediates, Li-ion cells).
  - Domestic vs. imported raw material split. Exposure to basic customs duties, anti-dumping duties (ADD), ocean container freight spikes, and port congestion.
  - **Approved Manufacturer Lists (AML):** Are raw material sources strictly dictated by customer engineering drawings? Does the company depend on a single supplier for >25% of purchases?
  - **Pricing Pass-Through Mechanics:**
    - Fixed-price contract, indexed cost-plus, or tender L1 bidding.
    - Explicit **Price Variation Clause (PVC):** What commodity index is used, how frequently does price reset (monthly, quarterly, bi-annually), and what is the exact reset time-lag? (A 90-day lag means severe quarterly margin volatility during sharp commodity spikes).
- [ ] **2.7 Customer Base, Empanelment & Criticality:**
  - Buyer segmentation: Direct OEMs vs. Tier-1 integrators vs. 3PLs vs. EPCs vs. government agencies vs. retail distributors.
  - **Empanelment Barriers & Qualification Lead Times:**
    - What is required to win commercial vendor code empanelment: First Article Inspection (FAI), PPAP Level 3/4 sign-offs, plant safety audits?
    - How long is the qualification cycle (e.g., 6 months vs. 24 months)?
    - Once qualified, is the company single-source, dual-source (60:40 share), or one of five commodity vendors?
  - **The "Who Gets Fired?" Test (Customer Criticality):**
    - If this component or service fails in the field, who at the customer faces career or operational damage?
    - *Extreme Asymmetry:* Does the component cost <1%–3% of the customer's total system cost while carrying catastrophic failure risk (plant explosion, assembly line halt, vehicle safety recall)?
    - *Low Asymmetry:* Is it a commoditized consumable that can be substituted on 24 hours' notice?
  - **The Payer vs. Decision-Maker Dynamic (Tier-1 Arrangements):**
    - Does the end customer (e.g., auto OEM, global tech giant) mandate the specification on the blueprint, leaving the Tier-1 assembler with zero authority to switch suppliers?
  - **Territorial & MNC/JV Export Restrictions (Ring-Fencing):**
    - Is the company legally, contractually, or via technology licensing agreements restricted from exporting to specific global territories (e.g., North America, Europe, East Asia)?
    - Does the foreign parent or JV partner restrict the Indian entity to India/SAARC while serving global markets from other parent-owned entities?
    - Can the company sell directly to global OEMs, or MUST all export sales route through parent-controlled overseas entities with parent-dictated transfer pricing?
- [ ] **2.8 Manpower, Staffing & Operating Leverage:**
  - Total permanent workforce vs. contract workers. Breakdown between technical/engineering staff, direct machine operators/drivers, and sales/administrative personnel.
  - Annual labor attrition rate (%) and employee benefit expenses as % of revenue.
  - Is the business model a labor-intensive staffing machine vulnerable to minimum wage inflation and driver churn?
- [ ] **2.9 Concentration Mapping:**
  - Customer Concentration: Top 1, Top 5, Top 10 customer share (%) across all restated years and interim period.
  - Supplier Concentration: Top 1, Top 5, Top 10 supplier share (%) of purchases.
  - Geographic Profile: Domestic vs. export split (and country breakdown). Reliance on export incentive schemes (RoDTEP, Duty Drawback, EPCG).
- [ ] **2.10 Section Verdict:** Two-sentence summary of the operational machine:
  > **Business Model Verdict:** The company physically operates as a ______ generating economics via ______. Operational headroom is **[Constrained by CTO/Capacity / Ample Brownfield Runway]**, with customer criticality classified as **[Mission-Critical / Moderate / Commoditized]**.

---

## §3. Industry Arena, Commissioned Report Audit & Structural Moat Testing

*Audit the macro arena, expose commissioned report biases, and evaluate whether excess returns are structurally defensible. Sourced from RHP chapters: Industry Overview & Our Business.*

- [ ] **3.1 Macro Industry Arena & Secular Operational Shifts:**
  - What is the estimated market size (in ₹ Cr or $M) and historical/projected volume growth rate of the core addressable sector?
  - What secular structural shifts are driving demand? (e.g., transition from capex purchase to opex rental; GST-driven warehouse formalization; tightening environmental/safety regulations; import substitution / PLI schemes).
  - Lifecycle position and cyclicality: Is industry demand secular or cyclical, and where is the sector currently situated in the broader economic cycle?
- [ ] **3.2 Deconstructing the Commissioned Industry Report (The Bias Check):**
  - Author of the commissioned report (CRISIL, CareEdge, Frost & Sullivan, Technopak, Infomerics) and confirmation that it was commissioned and paid for by the issuer.
  - **The Gerrymandering Audit:** How did the report define the addressable market? Did they artificially slice the market into an obscure micro-niche so the company can claim *"We are the #1 player"*?
  - **Real Addressable Market (TAM / SAM):** What is the real, unvarnished market size in India once artificial gerrymandering is stripped away?
  - **True Market Share:** Compute the company's actual market share across the unvarnished total market. (Does a claimed "market leader" actually hold less than 1% of the broader industry?).
- [ ] **3.3 Industry Value Chain Economics & Profit Pools:**
  - Map the vertical chain from raw material extraction to end customer:
    `Raw Materials → Component / Process Packager → Tier-1 / EPC Integrator → End Client`
  - Map typical operating margin and return profiles across each node. **Where does economic profit pool, and where is margin compressed?**
  - Is there active margin migration along the chain (e.g., OEMs disintermediating distributors or outsourcing sub-assemblies upstream)?
- [ ] **3.4 Industry Capacity & Supply-Demand Balance:**
  - Industry-wide capacity utilization in the company's primary product categories.
  - *Sellers' Market (>80%–85% utilization):* Disciplined pricing, stable-to-rising conversion margins, long customer lead times.
  - *Buyers' Market (<65%–70% utilization):* Idle overheads, aggressive discounting, unorganized price-cutting.
  - **The Capacity Pipeline:** What large greenfield or brownfield capacity expansions are currently under construction across the industry? Will supply additions outpace demand growth over the next 24 months?
  - Competitive landscape breakdown: Organized domestic peers, unorganized regional share, and low-cost import threats (e.g., subsidized Chinese equipment).
- [ ] **3.5 The Binding Competitive Force:**
  - Across Porter's Five Forces, identify the **single binding force** that places a ceiling on profitability for the average player in this industry.
- [ ] **3.6 Structural Moat Identification & Testing (Helmer's 7 Powers):**
  - Test the business against the 5 primary structural moat archetypes:
    - *Switching Costs:* Re-tooling costs, 12–24 month OEM audit recertifications, mission-critical failure risk vs. low piece cost.
    - *Structural Cost Advantage:* Favorable geographic plant location, captive raw materials, continuous proprietary thermal furnace yield, scale amortization.
    - *Intangibles / Regulatory Approvals:* High-barrier statutory pollution permits (CTO), USFDA/DIN certifications, granted patents, multi-decade brand trust in safety-critical parts.
    - *Network Density / Scale:* Unmatched fleet density, regional branch service network, rapid maintenance turnaround.
    - *Efficient Scale:* Market size too small to justify a second scale competitor entering the niche.
  - **The Commodity Verdict:** If none of these sources provide a durable barrier, explicitly label the business: **"No Structural Moat / Commoditized Operator."**
  - Moat Width, Depth, and Direction (Widening, Stable, Eroding).
  - Rule Out Moat Masqueraders: Temporary cyclical peak in commodity spreads, temporary government subsidy/tariff, or fast industry volume growth floating all boats.
- [ ] **3.7 The Replication Test (The ₹100–₹500 Cr Exercise):**
  - What would a well-capitalized competitor need with ₹100–₹500 Cr and 3 years to clone this business?
  - What can be bought trivially off-the-shelf from OEMs vs. where the competitor gets stuck (vendor codes, customer qualification libraries, driver management, balance sheet scale).
- [ ] **3.8 Pre-Listing Falsification Conditions (Contract with Stage 5):**
  - Complete this sentence with concrete numerical thresholds:
    > *"If this structural moat hypothesis is true, Stage 5 restated financial forensics MUST confirm:  
    > 1. Restated Operating ROIC consistently exceeds ____% across all historical years.  
    > 2. Gross conversion spread / EBITDA margin held within ±____% despite raw material inflation in FY____.  
    > 3. Trade receivables days have remained stable or contracted, proving customers cannot stretch credit terms.  
    > **If these are NOT confirmed in the restated ledger, the moat hypothesis is FALSE.**"*
- [ ] **3.9 Adjacent Optionality & Expansion Runway:**
  - Natural "Right to Win" adjacencies using existing machinery, vendor codes, customer relationships.
  - Static Fortress (high-ROIC cash cow that cannot absorb capital) vs. Compounding Machine (large addressable runway for high incremental ROIC reinvestment).
- [ ] **3.10 Section Verdict:**
  > **Industry & Moat Verdict:** Industry pond is **[Structurally Attractive / Mediocre / Value-Destroying]**; Economic Moat is **[Wide / Narrow / None - Commoditized]**, sourced from ______, currently **[Widening / Stable / Eroding]**.

---

## §4. Promoter Ecosystem, Governance Integrity & Pre-IPO Cleanup

*Audit the people steering the enterprise, unlisted parallel entities, related-party transactions, executive pay, and personnel stability. Sourced from RHP chapters: Promoters, Management, Group Companies, and Outstanding Litigation.*

- [ ] **4.1 Promoter Pedigree, Skin in the Game & Encumbrance:**
  - Background, track record, and educational pedigree of founding promoters and executive leadership.
  - Pre-issue vs. post-issue promoter shareholding % and retained voting control.
  - **Promoter Share Encumbrance:** Are any promoter shares pledged, held under Non-Disposal Undertakings (NDUs), or pledged as collateral for group company borrowings? What is the risk of post-listing re-encumbrance?
- [ ] **4.2 The Unlisted Promoter Parallel Ecosystem (Conflict of Interest Audit):**
  - Complete the map of all unlisted private companies, LLPs, and partnerships owned by the promoters or promoter group:
    | Entity Name | Relationship / Promoter Stake | Line of Business | Operational Overlap with Listed Company | Conflict of Interest / Non-Compete Status |
    |---|---|---|---|---|
  - **Shared Assets & Seams:** Do unlisted entities share registered office premises, operational warehouses, factory land, or key employees with the listed company?
  - **Brand & Intellectual Property Ownership:** Does the listed company own its corporate name, registered trademarks, logos, and patents, or are they owned by promoters / private entities with the listed company paying royalties, licensing fees, or operating under revocable agreements?
- [ ] **4.3 Related Party Transactions (RPT) Forensic Audit:**
  - Audit the mandatory RPT schedule from the Restated Notes to Accounts across all restated years:
    | Category of RPT | Related Party Entity | Commercial Nature | Cumulative ₹ Cr (3-Yr / Restated Period) | % of Revenue / Expense | Arm's Length Pricing Justification |
    |---|---|---|---|---|---|
    | **Lease Rentals** | Promoter / Group Firm | Factory / warehouse / office rent | | | |
    | **Royalty / Brand Fees** | Promoter / Group Firm | Trademark licensing | | | |
    | **Sales of Goods/Services** | Promoter / Group Firm | Commercial off-take | | | |
    | **Purchases of Goods** | Promoter / Group Firm | Component / raw material sourcing | | | |
    | **Loans / ICDs / Advances** | Promoter / Group Firm | Financing / treasury transfers | | | |
    | **Personal Guarantees** | Promoters | Collateral for company borrowings | | | |
  - *Post-Listing Continuity:* Will these transactions terminate upon listing, or will they continue under ongoing master service agreements? Are independent appraisals or audit committee approvals documented?
- [ ] **4.4 Executive Remuneration vs. Minority Returns:**
  - Total compensation (salary, commissions, perquisites, post-employment benefits) paid to promoter directors and KMPs across each restated year:
    | Fiscal Year | Total Promoter / KMP Remuneration (₹ Cr) | Restated Net Profit (PAT) (₹ Cr) | Remuneration as % of PAT | Total Cash Dividends Distributed (₹ Cr) |
    |---|---|---|---|---|
  - Are promoters paying themselves disproportionately high compensation relative to company scale (>10%–15% of PAT)? Did promoters distribute large liquid cash dividends immediately prior to filing the RHP?
- [ ] **4.5 Personnel, Board & Governance Churn Screen:**
  - **CFO & Finance Function Stability:** How long has the current CFO been in the seat? How many CFOs has the company had over the last 3–5 years? Did any CFO resign mid-term or right before RHP filing?
  - **Company Secretary & Compliance Officer Churn:** Frequent turnover indicates disclosure friction or internal friction regarding regulatory filings.
  - **Independent Director (ID) Resignations & Dissent:** Have any Independent Directors resigned prior to the completion of their statutory term? Review mandatory resignation letters filed with stock exchanges under Regulation 30 (checking for stated reasons of governance concerns or audit committee friction vs. generic "preoccupation").
  - **Auditor-to-KMP Transitions:** Did any partner or employee of the statutory audit firm resign and join the company as CFO, director, or executive within 24 months?
- [ ] **4.6 Statutory Auditor Pedigree & Audit Qualifications:**
  - Auditor identity: Big 4 firm vs. reputed national audit firm vs. obscure local auditor.
  - Audit fee reasonableness relative to corporate scale and geographic dispersion.
  - Has there been any mid-term resignation of a statutory auditor in the last 5 years?
  - Audit remarks, CARO qualifications, emphasis of matters, or internal financial control (IFC) deficiencies noted in the auditor's restatement report.
- [ ] **4.7 Outstanding Litigation & Contingent Liabilities:**
  - Audit the mandatory *Outstanding Litigation* chapter across all categories:
    | Category of Proceeding | Number of Cases | Quantified Amount Under Dispute (₹ Cr) | Disputed Amount as % of Post-Issue Net Worth | Potential Operational / Balance Sheet Impact |
    |---|---|---|---|---|
    | **Direct Tax Demands (Income Tax)** | | | | |
    | **Indirect Tax Demands (GST / Customs / Excise)** | | | | |
    | **Civil & Commercial Arbitration** | | | | |
    | **Criminal / Regulatory Actions (SEBI / ED / Police)** | | | | |
    | **Actions against Promoters / Group Companies** | | | | |
    | **Total Quantified Disputed Claims** | | | | |
  - If total disputed claims exceed **25%–30% of Net Worth**, an adverse tribunal ruling represents a solvency-threatening capital loss.
- [ ] **4.8 Section Verdict:**
  > **Governance Verdict:** Promoter integrity and alignment are graded **[High / Adequate / Compromised]**; Parallel unlisted conflicts of interest are **[Clean / Managed / High Leakage Risk]**; Governance churn screen is **[Stable / Flagged]**.

---

## §5. Restated Financial Forensics & Ledger Reality (PART A: ZERO PRICE)

*Put the restated numbers on trial. Audit cash conversion, working capital integrity, balance sheet solvency, and return on capital. STRICTLY ZERO MENTION of stock price, market cap, or valuation multiples.*

- [ ] **5.1 Restatement Adjustments Annexure Audit:**
  - Audit the mandatory Restatement Adjustments Annexure in the financial statements:
    - Reconcile statutory audited profit with Restated Profit After Tax across each historical year.
    - What specific adjustments were made? (e.g., reclassifying prior-period expenses, shifting asset write-downs backwards into older years, or adjusting provisioning policies).
    - Did the restatement adjustments cosmetically boost the pre-IPO filing year's profit at the expense of older fiscal years?
- [ ] **5.2 Pre-IPO Margin Jump & Stub-Period De-Annualization:**
  - Multi-year trajectory of Gross Margin, Operating EBITDA Margin, and PAT Margin:
    | Metric | FY-4 | FY-3 | FY-2 | FY-1 | Pre-IPO Full Year | Interim Stub Period |
    |---|---|---|---|---|---|---|
    | **Revenue from Operations (₹ Cr)** | | | | | | |
    | **Gross Margin / Spread (%)** | | | | | | |
    | **Operating EBITDA Margin (%)** | | | | | | |
    | **Net Profit (PAT) Margin (%)** | | | | | | |
  - Did operating margins suddenly spike in the 12–24 months immediately preceding the RHP filing? Check whether this was achieved by cutting discretionary maintenance/R&D, deferring expenses, or capitalizing costs into CWIP.
  - **Stub Period De-Annualization:** Never annualize a bumper 3-month or 6-month stub period if the business experiences quarterly seasonality, bunched Q4 billing, or pre-IPO channel stuffing.
- [ ] **5.3 The Capital Treadmill & Self-Funding Audit:**
  - Over the restated historical run, for every **₹100 of incremental revenue**, how many actual rupees of capital were consumed?
    - Rupees consumed by Net Working Capital = Change in Receivables + Change in Inventory - Change in Payables
    - Rupees consumed by Fixed Capital = Change in Gross Block
  - Is the business model a **Cash Generator** (throws off cash as it grows), a **Working Capital Absorber** (every ₹100 of growth traps ₹30–₹50 in debtors/inventory), or a **Heavy Capex Guzzler** (requires continuous machine additions just to grow)?
- [ ] **5.4 The Multi-Year Cash Flow Autopsy (PAT vs. CFO vs. FCF):**
  - Complete the cash conversion table from the Restated Cash Flow Statement:
    | Metric (₹ Cr) | FY-4 | FY-3 | FY-2 | FY-1 | Pre-IPO Full Year | Interim Stub Period | Cumulative Total |
    |---|---|---|---|---|---|---|---|
    | **Restated Profit After Tax (PAT)** | | | | | | | |
    | **Operating Cash Flow (CFO)** | | | | | | | |
    | **CFO / PAT Conversion Ratio (%)** | | | | | | | |
    | **Capital Expenditure (Capex)** | | | | | | | |
    | **Free Cash Flow (FCF = CFO - Capex)** | | | | | | | |
  - **The Cash Conversion Red Flag:** Is Cumulative CFO substantially lower than Cumulative PAT (CFO/PAT < 60%–70%)? Did operating cash flow turn negative in any recent year despite rising accounting profits?
  - **The Free Cash Flow Reality:** Is Free Cash Flow (FCF) positive, or does the capex treadmill consume more cash than operations generate (chronic negative cumulative FCF)? If cumulative FCF is negative, how did the business survive (bank borrowings vs. promoter loans vs. equity dilution)?
- [ ] **5.5 Trade Receivables Aging & Revenue Integrity:**
  - Extract the mandatory trade receivables aging schedule from the Restated Notes to Accounts:
    | Receivables Aging Schedule (₹ Cr) | Less than 6 Months | 6 Months to 1 Year | 1 to 2 Years | 2 to 3 Years | More than 3 Years | Total Trade Receivables |
    |---|---|---|---|---|---|---|
    | **Undisputed Receivables — Considered Good** | | | | | | |
    | **Disputed Receivables — Considered Good** | | | | | | |
    | **Disputed / Undisputed — Credit Impaired** | | | | | | |
    | **Provision for Doubtful Debts** | | | | | | |
  - Are overdue receivables (>6 months old) surging faster than revenue? Compute overdue receivables as % of total receivables.
  - Unbilled revenue trajectory: Are unbilled revenues growing rapidly, signaling aggressive percentage-of-completion revenue recognition?
  - Debtor Days / Days Sales Outstanding (DSO) trend.
- [ ] **5.6 Inventory Aging & Provisioning:**
  - Finished goods vs. work-in-progress (WIP) vs. raw materials breakdown.
  - Inventory holding days trend. Provisions for slow-moving, obsolete, or damaged inventory.
- [ ] **5.7 CWIP Aging Schedule (The Asset Parking Lot):**
  - Extract the mandatory Capital Work-in-Progress (CWIP) Aging Schedule from the notes:
    | CWIP Aging Schedule (₹ Cr) | Less than 1 Year | 1 to 2 Years | 2 to 3 Years | More than 3 Years | Total CWIP |
    |---|---|---|---|---|---|
    | **Projects in Progress** | | | | | |
    | **Projects Temporarily Suspended** | | | | | |
  - Are stalled projects or operational cost overruns parked in CWIP to avoid P&L depreciation?
- [ ] **5.8 Cash Existence & Treasury Yield Check:**
  - Extract total cash, bank balances, fixed deposits, and liquid investments from the balance sheet.
  - Extract **Interest Income** from the Note on Other Income.
  - Implied Treasury Yield: `Implied Yield = Interest Income / Average Cash & Liquid Investments`.
  - **Red Flag Detection:** If the company reports ₹100 Cr of cash but interest income implies a yield of <2%–3% in a 7% interest rate environment, that cash is encumbered (pledged as margin money for group entities), held in current accounts, or fabricated.
- [ ] **5.9 The Cash-to-Debt Paradox:**
  - Does the company simultaneously carry large cash balances AND large, high-cost bank borrowings (negative carry)?
- [ ] **5.10 Tax Rate Integrity (Cash Tax vs. P&L Tax):**
  - Check effective tax rate in P&L against statutory corporate tax rates (25.17% under Section 115BAA).
  - Compare P&L tax expense against **Direct Taxes Actually Paid** in the Cash Flow Statement.
  - Scrutinize deferred tax asset (DTA) build-ups and MAT credit recognitions.
- [ ] **5.11 Depreciation Policy & Useful Life Games:**
  - Check whether the company switched depreciation methods (WDV to SLM) or extended estimated useful lives of plant and machinery over the restated period to cosmetically lower annual depreciation charges.
- [ ] **5.12 Balance Sheet Solvency & Leverage:**
  - Total Long-Term Debt, Short-Term Debt, and Gross Borrowings.
  - Cash & Liquid Investments, and Net Debt.
  - Net Debt / EBITDA ratio and Interest Coverage ratio across each year.
  - Non-Fund-Based (NFB) banking lines: Outstanding Bank Guarantees (BGs) and Letters of Credit (LCs).
- [ ] **5.13 Core Operating ROIC vs. WACC across Cycles:**
  - Core Operating Invested Capital = `Gross Block - Accumulated Depreciation + Net Working Capital - Cash & Liquid Investments`.
  - Core Operating NOPAT = `Operating EBIT * (1 - Effective Tax Rate)`.
  - Core Operating ROIC = `Core Operating NOPAT / Core Operating Invested Capital`.
  - Compare Core Operating ROIC against cost of capital (WACC ≈ 12%–14% in India). Does ROIC consistently clear WACC, confirming Stage 3's moat hypothesis?
- [ ] **5.14 DuPont ROE Decomposition:**
  - Decompose Restated ROE across each fiscal year:
    `ROE = (PAT / Revenue) * (Revenue / Average Assets) * (Average Assets / Average Equity)`
    `ROE = Net Profit Margin * Total Asset Turnover * Financial Leverage Multiplier`
  - Is return on equity driven by high operating margins and asset efficiency, or flattered by dangerous balance-sheet leverage?
- [ ] **5.15 Section Verdict:**
  > **Financials Verdict:** Restated earnings **[Confirm / Contradict]** the Stage 2–3 narrative; Earnings **[Do / Do Not]** convert to real cash (CFO/PAT: ___%); Free Cash Flow is **[Positive / Chronic Negative Treadmill]**; Core Operating ROIC **[Does / Does Not]** clear WACC (___% vs. ___%).

---

## §6. Valuation Collision, Market Mechanics & Asymmetric Decision (PART B: WITH PRICE)

*Introduce the offer price band, market capitalization, and enterprise value. Collide market expectations against operational reality, map lock-in supply cliffs, and deliver the definitive investment decision.*

- [ ] **6.1 Falsification of RHP Cherry-Picked Peers:**
  - Audit the peer table presented by merchant bankers in *Basis for Issue Price*.
  - **Quarantine Convenient Inclusions:** Explain why RHP peers are mismatched (e.g., comparing a contract manufacturer to high-multiple consumer brands, or an asset-heavy rental fleet to a circular pallet platform).
  - **Expose Convenient Omissions:** Identify direct operating competitors omitted from the RHP peer set because they trade at lower valuation multiples.
- [ ] **6.2 Deterministic True Peer Matrix (ROIC-Adjusted):**
  - Assemble 3 to 5 true operating peers using the `peer-finder.md` runbook:
  | Company Name | Business / Economic Match | Market Cap (₹ Cr) | P/E Ratio (TTM / FY) | EV/EBITDA | ROCE (%) | Operating EBITDA Margin (%) | Debtor Days | 3-Yr CFO / PAT (%) |
  |---|---|---|---|---|---|---|---|---|
  | **Target IPO (at Cap Price)** | **Subject Company** | | | | | | | |
  | **Real Peer 1** | | | | | | | | |
  | **Real Peer 2** | | | | | | | | |
  | **Real Peer 3** | | | | | | | | |
  | **RHP Peer (Excluded Cherry-Pick)** | | | | | | | | |
  - Compute the median multiple of real operating peers vs. the RHP's cherry-picked peers to quantify the merchant banker pricing bias.
- [ ] **6.3 Valuation Multiples on Normalized & Forward Earnings:**
  - Upper price band multiples:
    - P/E on Trailing Pre-IPO Normalized PAT.
    - P/E on Forward Normalized PAT (accounting for interest expense savings from debt repayment proceeds).
    - EV/EBITDA on pre-IPO operating EBITDA.
    - Price-to-Book (P/BV) against post-issue Net Asset Value (NAV).
- [ ] **6.4 The 3-Year Price Band Inversion Equation:**
  - Set required investor hurdle rate: **15.0% CAGR**.
  - Target Market Cap in Year 3 to deliver hurdle: `Target M-Cap = Current M-Cap * (1.15)^3`.
  - Target Enterprise Value in Year 3 = `Target M-Cap + Projected Year 3 Net Debt`.
  - Solve for Year-3 implied operating requirements:
    - If the exit multiple contracts to the real peer median: **What Year-3 revenue and EBITDA margin must the company achieve?**
    - If margins remain at current levels: **What exit multiple is the market implicitly demanding in Year 3?**
  - **The Inversion Verdict:** Does delivering a 15% return require conservative, realistic, or heroic growth and multiple assumptions?
- [ ] **6.5 The Operational Physics & Reality Collision:**
  - *Collision with Stage 2 (Physical Capacity):* What rupee revenue must the company achieve in Year 3 to satisfy the market price? Can existing plants, plus announced and funded capex expansions, **physically produce that volume**?
  - *Collision with Stage 3 (Addressable Market):* Does the implied production volume exceed the company's Serviceable Addressable Market (SAM) or require winning unrealistic market share from entrenched incumbents?
  - *Collision with Stage 5 (The Capital Treadmill):* Based on Stage 5's capital treadmill, how many ₹ Cr of working capital and capex are required to support that market-implied revenue? Can internal CFO fund that expansion, or does the market price quietly assume massive debt or equity dilution?
- [ ] **6.6 Scenario Valuation Distribution (Bear, Base, Bull):**
  Complete the 3-year scenario model:
  | Scenario | Operational Assumptions (Revenue CAGR / Margin) | Year 3 PAT (₹ Cr) | Target Exit Multiple (P/E or EV/EBITDA) | Year 3 Target Value per Share (₹) | Return CAGR (%) | Expected Downside / Upside (%) |
  |---|---|---|---|---|---|---|
  | **Bear Case Floor** | Industry downturn, margin contraction by 300 bps, multiple derating | | | | | -____% |
  | **Base Case Fair Value** | Execution of funded capex, steady margins, peer median multiple | | | | | +____% |
  | **Bull Case** | Optimal capacity utilization, operating leverage expansion, multiple re-rating | | | | | +____% |
  - Compute Risk-Reward Asymmetry Ratio: `Asymmetry Ratio = Base Upside % / |Bear Downside %|` (Minimum threshold: ≥ 2.0:1).
  - Margin of Safety %: `[(Base Fair Value - Cap Price) / Base Fair Value] * 100%`.
- [ ] **6.7 Demand & Supply Cliff Mechanics:**
  - **QIB & Anchor Book Quality:** (Audited from anchor allocation filing on Day -1). Proportion taken by marquee domestic mutual funds vs. sovereign wealth funds vs. offshore hedge funds / flippers.
  - **Post-Listing Lock-In Supply Calendar:**
    | Milestone | Release Date (from Listing) | Shares Unlocked | % of Total Post-Issue Capital | Potential Supply Overhang Risk |
    |---|---|---|---|---|
    | **30-Day Anchor Lock-in** | 30 days post-allotment | 50% of Anchor allocation | | |
    | **90-Day Anchor Lock-in** | 90 days post-allotment | Remaining 50% of Anchor | | |
    | **6-Month Pre-IPO Lock-in** | 6 months post-allotment | Non-promoter pre-IPO holders | | |
    | **1-Year Promoter Lock-in** | 12 months post-allotment | 50% of excess Promoter stake | | |
    | **2-Year Promoter Lock-in** | 24 months post-allotment | Remaining excess Promoter stake | | |
    | **3-Year Minimum Promoter Lock-in** | 36 months post-allotment | Mandatory 20% Promoter stake | | |
  - **Day-1 Free Float & Liquidity:** Tradeable float % on Day 1. (Thin float <15% creates sharp volatility, easy manipulation, and severe post-lock-in dump risk).
- [ ] **6.8 The Strategic Arc:**
  - *The Past:* Where did this company come from over the last 5–10 years? How did it navigate previous industry downturns?
  - *The Present:* What is the ground reality right now? (Current TTM run-rate, active headwinds depressing sentiment/margins, and active tailwinds supporting demand).
  - *The Likely Future:* Over the next 2–3 years, what will this enterprise physically look like once IPO proceeds are deployed?
- [ ] **6.9 The Core Asymmetry Thesis:**
  - State the differentiated investment thesis in 2–3 clear sentences:
    > *"The market believes [Consensus assumption baked into IPO band]; We believe [Our variant perception based on Stages 1–5]; Factual evidence confirms our view because [Load-bearing operational/forensic facts]; We expect the mispricing to resolve when [Specific catalyst/milestone]."*
- [ ] **6.10 Key Risks to Capital (Top 2–3 Real Threats):**
  - Screen out temporary market volatility. Enumerate ONLY the 2–3 concrete threats that could permanently impair capital:
    1. **Risk 1:** Specific threat, quantified financial/balance sheet impact, and mitigating balance sheet cushion.
    2. **Risk 2:** Specific threat, quantified financial/balance sheet impact, and mitigating cushion.
    3. **Risk 3:** (If applicable).
- [ ] **6.11 Pre-Committed Observable Kill Triggers (Non-Negotiable Exit Rules):**
  - Define explicit, factual, non-negotiable tripwires in advance:
    - *Operational Kill Trigger:* Specific operational breakdown that invalidates the business engine (e.g., loss of key OEM vendor code, SPCB CTO revoked, plant commissioning delayed >4 quarters).
    - *Financial Kill Trigger:* Specific audited ledger breach confirming deteriorating economics (e.g., receivables >6m exceeding X% of revenue, Core Operating ROIC falling below WACC for 2 consecutive years, debtor days exceeding X days).
    - *Governance Kill Trigger:* Specific corporate action signaling unacceptable insider risk (e.g., mid-term resignation of CFO or statutory auditor, promoter pledging exceeding 5%, RPT fees expanding >5% of revenue).
- [ ] **6.12 Dated Catalysts & Value Realization Calendar (12 to 24 Months):**
  - Complete the milestone tracking calendar:
    | Target Date / Period | Specific Event / Milestone | What it Confirms or Tests | Expected Impact on Thesis |
    |---|---|---|---|
- [ ] **6.13 Final Investment Recommendation & Portfolio Sizing:**
  - Deliver the definitive Investment Committee decision:
    - **`APPLY TO OWN`:** Passes all forensic and governance screens, verified cash conversion, favorable Asymmetry Ratio ≥ 2.0:1, and adequate Margin of Safety.
      - *Sizing:* Tier 1 Core Position (5.0%–7.0%) / Tier 2 Tactical Position (3.0%–5.0%) / Starter Position (1.5%–2.5%).
    - **`APPLY TO FLIP`:** High subscription / anchor demand; purely a technical listing-gain play. Pre-commit to exit on listing day; allocate strictly small size.
    - **`WAIT FOR LOCK-IN CLIFF`:** High-quality fundamental business, but IPO price band offers zero margin of safety, or significant supply unlocks at 30/90 days. Pre-commit to secondary entry trigger: **"Buy Below ₹____ upon 30/90-Day Lock-in Expiry."**
    - **`PASS`:** Structural deal-breaker identified (governance compromise, negative cash treadmill, unappraised promoter bailout, or absurd valuation).
  - The One-Sentence Closing Declaration:
    > *"We recommend **[APPLY TO OWN / APPLY TO FLIP / WAIT FOR LOCK-IN CLIFF / PASS]** on [Company Name] at the upper price band of ₹[____], with a 3-year Base Case fair value target of ₹[____] ([____%] upside) and a Bear Case floor of ₹[____] ([____%] downside), because [1 core operational reason], with primary downside protection provided by [core balance-sheet/moat cushion]."*
