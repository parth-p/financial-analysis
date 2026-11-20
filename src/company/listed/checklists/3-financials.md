# Financial Forensics & Valuation Collision — Analyst's Checklist

*Stage 3 of the 4-Stage Equity Research Framework.*

> **The Mandate for Stage 3:** Put the business and its valuation on trial against the hard evidence of the audited ledger.
>
> **The Epistemological Discipline:**
> - **The Clean Separation: Part A is Operating Reality; Part B is Price. They never mix.** In Part A, the stock price, market cap, enterprise value, and valuation multiples are strictly forbidden. You are an auditor dissecting the physical cash engine, forensic integrity, and capital treadmill of the business. Price is introduced only in Part B to collide market expectations against Part A's reality.
> - **Actual Numbers over Textbook Ratios.** Do not compute dozens of formulaic textbook ratios. Focus on absolute rupees, multi-year cash movements, notes to accounts, aging schedules, and capital requirements.
> - **Primary Calculation Invariant.** Compute and verify the numbers yourself from audited annual report schedules and primary filings. Do not treat portal aggregates (e.g., Screener.in) as unquestioned truth.
> - **Strict 3-Year Forward Horizon.** Discard 10-year DCF hand-waving. Confine all valuation scenarios to a rigorous 3-year operational window (FY+1 to FY+3) anchored to observable capex, announced capacity additions, and audited cycle baselines.

---

### The Flag Convention
When you encounter a fact that requires testing or decision-making in subsequent stages, tag it inline:
- **Format:** `Fact → Stage N (Action required)`
- ✅ *"Cumulative 5-year FCF is negative (-₹340 Cr) due to working capital blowout → Stage 4 (size dilution risk & pre-mortem failure mode)."*
- ✅ *"Contingent liabilities represent 28% of Net Worth, driven by disputed excise tax notices → Stage 4 (governance / legal kill trigger)."*

---

# PART A: FINANCIAL FORENSICS & OPERATING REALITY (NO PRICE ALLOWED)

*Audit the economic machine solely from the audited ledger. Zero mention of stock price, market cap, or valuation multiples.*

---

## 1. The Capital Treadmill & Self-Funding Audit (The Dilution Check)

*The central economic question: Can this business fund its own growth, or is it a cash furnace that constantly forces debt spikes or equity dilution?*

- [ ] **The Incremental Growth Capital Appetite:**
  - Over the trailing 5 to 10 years, for every **₹100 of incremental revenue**, how many actual rupees of capital were consumed?
    - Rupees consumed by Net Working Capital = Change in Receivables + Change in Inventory - Change in Payables
    - Rupees consumed by Fixed Capital = Change in Gross Block
  - Is the business model a **Cash Generator** (throws off cash as it grows), a **Working Capital Absorber** (every ₹100 of growth traps ₹30–₹50 in debtors/inventory), or a **Heavy Capex Guzzler** (requires continuous machine additions just to grow)?
- [ ] **The 10-Year Free Cash Flow (FCF) Equation:**
  - Compute the cumulative 10-year cash reality:
    Cumulative 10-Yr Operating Cash Flow (CFO) - Cumulative 10-Yr Capex = Cumulative 10-Yr Free Cash Flow (FCF)
  - Calculate the FCF conversion efficiency: Cumulative FCF / Cumulative PAT
- [ ] **The Financing Gap & Dilution Trap:**
  - If Cumulative 10-Year FCF is **negative or near-zero**, how did the company survive and fund its expansion?
    - *Debt Escalation:* Did long-term and short-term bank borrowings increase to plug the gap?
    - *Equity Dilution:* Did management repeatedly tap equity markets (QIPs, preferential share issues, rights issues, warrant conversions)?
  - **The Dilution Invariant:** If net profit grew at 15% CAGR but share count expanded by 4% CAGR via repeated equity dilution, underlying EPS growth was diluted to ~11%. Document the exact 10-year share count trajectory:
    | Year | FY-9 | FY-7 | FY-5 | FY-3 | FY-1 | Current | 10-Yr Dilution CAGR (%) |
    |---|---|---|---|---|---|---|---|
    | Outstanding Shares (Cr) | | | | | | | |

---

## 2. Capital Allocation Verification in the Ledger

*In Stage 2, management made forward promises and strategic assertions. Audit whether those actions actually materialized in the financial statements.*

- [ ] **Auditing Words Against Hard Numbers:**
  Complete the ledger verification table for all major strategic claims made by management over the last 3–5 years:
  | Management Claim (from Stage 2) | Stated Target / Commitment | Actual Ledger Outcome (Audited Statements) | Status (Verified / Contradicted / Stalled) |
  |---|---|---|---|
  | **Capex Execution** | E.g., *"Invested ₹150 Cr in new plant capacity"* | Check Gross Block additions, CWIP capitalization, and incremental depreciation line | |
  | **Debt Reduction** | E.g., *"Using cash flows to de-leverage balance sheet"* | Check absolute borrowings line AND verify that P&L interest expense collapsed in tandem | |
  | **Working Capital Discipline** | E.g., *"Tightened customer credit terms to 60 days"* | Check absolute trade receivables and debtor days trend in the balance sheet notes | |
  | **Operating Efficiencies** | E.g., *"Realizing operational leverage & cost savings"* | Check power/fuel, raw material consumption %, and other expenses as % of sales | |
- [ ] **The Disconnect Check:**
  - If debt dropped on the balance sheet but P&L interest expense stayed flat or increased, hunt for hidden bank charges, letter of credit (LC) discounting costs, or off-balance-sheet vendor financing.
  - If capex was reported as completed but Gross Block did not rise and depreciation did not step up, determine where the cash was actually capitalized.

---

## 3. Forensic Integrity & The Accounting Smell Test

*Hunt for where reported accounting profits diverge from cash reality, whether cash on the balance sheet is real, and where expenses are concealed.*

- [ ] **Cumulative PAT vs. Cumulative CFO (The 10-Year Reality Gap):**
  - Reconcile cumulative 10-year Net Profit against Operating Cash Flow:
    Cumulative 10-Year PAT vs. Cumulative 10-Year CFO
  - If Cumulative PAT substantially exceeds Cumulative CFO (Cumulative CFO < 0.80 * Cumulative PAT), **reported profits did not convert into real cash.** Identify where the difference is trapped: uncollected receivables, unsellable inventory, or capitalized overheads.
- [ ] **The Cash Existence & Treasury Yield Check:**
  - Extract total cash, bank balances, fixed deposits, and liquid investments from the balance sheet.
  - Extract **Interest Income** and dividend income from Note on Other Income.
  - Compute the implied treasury yield:
    Implied Treasury Yield = Interest Income / Average Cash & Liquid Investments
  - **The Red Flag:** If the company reports ₹300 Cr of cash but interest income is only ₹6 Cr (~2.0% yield in a 7% interest rate environment), that cash is **encumbered** (pledged as collateral/margin money for group entities), held in non-interest-bearing current accounts, or fabricated.
- [ ] **The Cash-to-Debt Paradox:**
  - Does the company simultaneously carry large cash balances AND large, high-cost bank borrowings?
  - Why would a prudent management borrow at 9.5%–11.0% interest while keeping equivalent cash in bank FDs earning 6.5% pre-tax (negative carry)? *(Classic red flag in Indian corporate accounting history).*
- [ ] **Tax Rate Integrity (Cash Tax vs. P&L Tax):**
  - Check the effective tax rate in the P&L against the statutory corporate rate (25.17% under Section 115BAA).
  - Compare P&L tax expense against **Direct Taxes Actually Paid** in the Cash Flow Statement.
  - If effective tax is persistently <20% without verified SEZ/tax holiday benefits, or if cash tax paid is consistently lower than P&L tax expense, scrutinize deferred tax asset build-ups and MAT credit recognitions.
- [ ] **Depreciation Policy & Useful Life Games:**
  - Has the company switched depreciation methods (WDV to SLM) or extended the "estimated useful lives" of plant and machinery in the notes to accounts over the last 5 years?
  - Artificially extending useful lives reduces annual depreciation charges, cosmetically boosting reported PAT without generating cash.
- [ ] **The CWIP Parking Lot (Capital Work-in-Progress Aging):**
  - Audit the mandatory CWIP Aging Schedule from the notes to accounts:
    | CWIP Aging | Less than 1 Year | 1 to 2 Years | 2 to 3 Years | More than 3 Years | Total CWIP |
    |---|---|---|---|---|---|
    | Projects in Progress (₹ Cr) | | | | | |
    | Projects Temporarily Suspended (₹ Cr) | | | | | |
  - CWIP aging **>2–3 years** is a prime indicator of stalled projects, unviable technology, or regular operating expenses improperly capitalized to avoid P&L hits.
- [ ] **Other Income Bloat & Operating Earnings Core:**
  - Calculate: Other Income / Profit Before Tax (PBT).
  - If Other Income represents >15%–20% of PBT, strip it out to isolate core operating earnings. Audit what constitutes Other Income: genuine treasury income vs. scrap sales, forex gains, fair-value MTM adjustments, or one-off asset sales.
- [ ] **Forensic Screens as Tripwires:**
  - Run the quantitative screens via `financial_calculator.py`:
    - **Altman Z-Score:** Solvency/distress tripwire (Z > 2.9 Safe, 1.8 < Z < 2.9 Grey, Z < 1.8 Distress).
    - **Beneish M-Score:** Earnings manipulation tripwire (M > -1.78 indicates high probability of accounting manipulation).

---

## 4. Balance Sheet Asset Quality & Real Working Capital Health

*Look at the actual schedules in the notes to accounts, not formulaic current/quick ratios.*

- [ ] **Trade Receivables Aging Schedule (Mandatory Schedule in Notes):**
  - Extract the audited Trade Receivables Aging Table:
    | Receivables Category | < 6 Months | 6 Months – 1 Year | 1 – 2 Years | 2 – 3 Years | > 3 Years | Total |
    |---|---|---|---|---|---|---|
    | Undisputed — Considered Good (₹ Cr) | | | | | | |
    | Undisputed — Significant Credit Risk (₹ Cr) | | | | | | |
    | Disputed Dues (₹ Cr) | | | | | | |
  - **The Receivables Test:** Are receivables aging **>6 months growing faster than total sales**? What is the provision for expected credit losses (ECL) against aging debts?
- [ ] **Inventory Breakdown & Demand Signals:**
  - Audit the inventory note: Raw Materials vs. Work-in-Progress (WIP) vs. Finished Goods vs. Stores & Spares.
  - If **Finished Goods inventory is ballooning** while raw material purchases and sales are flat, the business is facing customer pushback, order cancellations, or channel stuffing.
- [ ] **Treasury Portfolio Quality & Counterparty Safety:**
  - Audit the exact instruments where cash is parked in the Investment Schedule:
    - Scheduled commercial bank fixed deposits (verify if any are marked under lien or bank guarantee margins).
    - Liquid / overnight mutual funds (sovereign / AAA paper).
    - Risky credit-risk debt mutual funds, unlisted preference shares, or commercial paper of NBFCs.
    - Inter-Corporate Deposits (ICDs) to third parties or group entities.
  - **Treasury Drag Calculation:** Compare the post-tax return on treasury cash (~5%) against the company's cost of capital (12%+). If treasury cash exceeds 20% of total assets, quantify the return dilution on overall ROCE.

---

## 5. Solvency, Debt Structure & Banking Headroom

*Can the company survive a sharp 2-year downcycle without defaulting or emergency dilution?*

- [ ] **Borrowing Structure & Maturity Profile:**
  - Breakdown of total borrowings:
    - *Short-Term Borrowings (Working Capital CC/OD limits):* ₹____ Cr.
    - *Long-Term Borrowings (Term Loans):* ₹____ Cr.
    - *Lease Liabilities (Ind AS 116):* ₹____ Cr.
  - Foreign currency borrowings (ECBs): What percentage is unhedged against INR depreciation?
  - Fixed vs. floating interest rate exposure: What is the impact of a 100 bps repo rate hike on annual PBT?
- [ ] **Non-Fund-Based (NFB) Bank Line Utilization:**
  - What are the total sanctioned **Non-Fund-Based banking limits** (Letters of Credit and Bank Guarantees)?
  - What is the current limit utilization percentage? (Utilization >85%–90% leaves zero liquidity buffer if a customer payment is delayed).
- [ ] **Off-Balance-Sheet Financing & Vendor Financing:**
  - Are receivables discounted with banks with recourse (bills discounted)?
  - Does the company use channel financing or reverse-factoring vendor programs that mask operational liabilities as trade payables?
- [ ] **Warranty Provisions Trend (Product Quality Red Flag):**
  - Audit the Note on Provisions for Warranties over the last 3–5 years:
    | Financial Year | Opening Provision | Additions during Year | Utilizations / Reversals | Closing Provision | Additions as % of Revenue |
    |---|---|---|---|---|---|
    | FY-3 | | | | | |
    | FY-2 | | | | | |
    | FY-1 | | | | | |
    | Current | | | | | |
  - If warranty additions as a % of sales are expanding rapidly, it signals escalating manufacturing defects, field failures, or looming product recall liabilities.
- [ ] **Contingent Liabilities as % of Net Worth:**
  - Extract the Note on Contingent Liabilities and Commitments:
    - Disputed Income Tax demands: ₹____ Cr.
    - Disputed GST / Excise / Customs demands: ₹____ Cr.
    - Outstanding corporate guarantees issued: ₹____ Cr.
    - Total Contingent Liabilities: **₹____ Cr**.
  - Calculate: (Total Contingent Liabilities / Net Worth) * 100.
  - **Threshold:** If contingent liabilities exceed **15%–20% of Net Worth**, quantify the worst-case capital erosion and tag `Fact → Stage 4 (Pre-Mortem Failure Mode)`.

---

## 6. Economic Returns & The Moat Falsification Test

*Strip out accounting noise to measure real economic productivity and test Stage 1's hypothesis.*

- [ ] **Core Operating ROCE & ROIC (Stripping Out Cash):**
  - Calculate Core Operating Return on Invested Capital:
    Operating Capital Employed = Net PPE + Capital Work-in-Progress + Core Working Capital
    *(Strictly exclude Cash, Bank Balances, Liquid Investments, and Non-Operating Assets).*
    Operating EBIT = Reported EBIT - Other Income
    Core Operating ROIC = [Operating EBIT * (1 - Effective Tax Rate)] / Operating Capital Employed
- [ ] **Incremental Capital Efficiency (5-to-10 Year Horizon):**
  - Over the trailing 5 to 10 years:
    Incremental ROIC = Change in Operating EBIT / Change in Operating Capital Employed
  - Has management generated acceptable incremental returns on new capital deployed (>18%–20%), or has incremental capital yielded subpar economic returns (<12%)?
- [ ] **DuPont Decomposition of ROE:**
  - Break down Return on Equity into its three operational drivers:
    ROE = Net Profit Margin (PAT / Revenue) * Asset Turnover (Revenue / Total Assets) * Financial Leverage (Total Assets / Net Worth)
  - Is high ROE driven by **pricing power/margins** (moat indicator), **efficient asset turnover**, or **dangerous financial leverage**?
- [ ] **The Moat Falsification Test (Explicit Contract with Stage 1):**
  - Compare audited 10-year ledger results against the explicit falsification conditions formulated in Stage 1 Section 9:
    1. *Return Durability:* Did Operating ROIC stay comfortably above cost of capital (WACC) across the deepest industry downcycle?
    2. *Margin Defense:* Did gross conversion spread / gross margin hold within guided bands during sharp raw material spikes?
    3. *Customer Power:* Did working capital days remain disciplined, or did customers stretch credit terms?
  - **The Formal Moat Verdict:**
    - [ ] **MOAT CONFIRMED:** Audited numbers fully validate Stage 1 structural advantage.
    - [ ] **MOAT FALSIFIED:** High historical returns were driven by temporary tailwinds, leverage, or subsidies; numbers refute the moat hypothesis.
    - [ ] **NO MOAT / COMMODITY:** Returns fluctuate with commodity cycles; company is a price-taker.

---

# PART B: VALUATION COLLISION (PRICE INTRODUCED)

*Bring in the market price to reverse-engineer consensus expectations, test them against Part A's reality, and determine the margin of safety.*

---

## 7. Current Price, Capital Structure & Enterprise Reality

*Establish the exact market capitalization and enterprise value on a fully diluted basis.*

- [ ] **The Fully Diluted Share Base:**
  - Current basic equity shares outstanding: `________` shares.
  - Dilution check (from Stage 2):
    - Outstanding promoter convertible warrants: `________` shares.
    - Outstanding employee stock options (ESOPs): `________` shares.
    - Compulsorily convertible debentures (CCDs) / preference shares: `________` shares.
  - **Fully Diluted Share Count:** `________` shares.
- [ ] **The Enterprise Value (EV) Bridge:**
  Current Market Cap = Current Market Price (CMP) * Fully Diluted Shares
  Enterprise Value (EV) = Market Cap + Total Debt (incl. Lease Liabilities) - Verified Unencumbered Cash
  *(Do NOT subtract encumbered cash, margin money, or illiquid ICDs identified in Part A).*

---

## 8. The 3-Year Inversion (What is the Market Pricing In?)

*Invert! Do not ask "what is it worth?" Ask what the market price assumes must happen over the next 3 years to deliver a target return.*

- [ ] **Grounded Growth Anchors (No Made-Up Projections):**
  - Define forward 3-year revenue and operating profit trajectory strictly using verified anchors:
    - *Anchor 1 (Management Guidance):* Quantitative targets from Stage 2 Section 2 (if verifiable).
    - *Anchor 2 (Industry / Macro Benchmark):* Underlying industry volume growth from Stage 1 Section 8.
    - *Anchor 3 (Unverified Rule):* If neither management guidance nor reliable industry data exists, **do not invent numbers.** State that forward visibility is unverified and evaluate strictly on normalized through-cycle earnings.
- [ ] **Select Sector-Native Valuation Multiple:**
  - Select the primary metric suited to the business archetype (per `src/common/docs/valuation-guide.md`):
    - *Manufacturing / Precision Components / Cyclicals:* **EV/EBITDA** or **EV/EBIT** (neutralizes capital structure and cash).
    - *Lenders / NBFCs / Financials:* **P/B** or **P/ABV** (adjusted for NNPA).
    - *Asset-Light / FMCG / Specialty Pharma:* **P/E** and **FCF Yield**.
    - *Loss-Making / Hyper-Growth Platforms:* **EV/Sales** (cross-checked against contribution margins).
- [ ] **The 3-Year Multiple Inversion Equation:**
  - Set your required investor hurdle rate: **12.0% to 15.0% CAGR** (standard Indian equity hurdle).
  - Target Market Cap in Year 3 to deliver hurdle rate:
    Target Market Cap (Year 3) = Current Market Cap * (1 + Hurdle Rate)^3
  - Compute: If the company delivers its 3-year grounded growth anchor, **what exit multiple is the market implicitly demanding in Year 3 to justify today's CMP?**
    Implied Exit Multiple (Year 3) = Target Enterprise Value (Year 3) / Projected Year 3 Operating Metric (EBITDA / PAT)
  - **The Inversion Verdict:**
    - Is the implied exit multiple lower than, equal to, or substantially higher than the company's 10-year historical median?
    - If delivering a 15% return requires the stock to trade at an all-time high exit multiple 3 years from today, **the market is pricing in multiple expansion that has zero margin of safety.**

---

## 9. The Operational Physics & Reality Collision

*Collide the market-implied growth and margins against the physical and financial realities established in Stages 1, 2, and Part A.*

- [ ] **Collision with Stage 1 (Physical Capacity & Addressable SAM):**
  - What rupee revenue must the company achieve in Year 3 to satisfy the market price?
  - Can the company's existing plants, plus announced and funded brownfield expansions, **physically produce that volume**?
  - Does the implied volume exceed the company's Serviceable Addressable Market (SAM) or require winning unrealistic market share from entrenched incumbents?
- [ ] **Collision with Stage 2 (Execution Track Record & Say-Do Baseline):**
  - Does the market price assume sustainable EBITDA margins (e.g., 14%+) that management has never achieved over a full cycle?
  - If Customer Concentration in Stage 1 showed that 2 OEMs control 80% of purchases, does the market price assume pricing power that the value chain prohibits?
- [ ] **Collision with Part A (The Capital Realism Check):**
  - Based on Part A's Capital Treadmill: How many ₹ Cr of working capital and capex are required to support the market-implied revenue?
  - Can internal operating cash flows (CFO) fund that expansion, or does the market price quietly assume the company will take on massive bank debt or dilute shareholders via QIPs?

---

## 10. Historical Valuation Bands & Cycle Position (10-Year Percentiles)

*Multiples are meaningless without full-cycle historical context.*

- [ ] **The 10-Year Percentile Distribution:**
  - Compute the 10-year historical valuation distribution for the primary sector multiple:
    | Valuation Metric | 10-Yr Min | 25th Percentile | 10-Yr Median | 75th Percentile | 10-Yr Max | Current Multiple | Current Percentile Rank |
    |---|---|---|---|---|---|---|---|
    | **P/E Ratio** | | | | | | | |
    | **EV/EBITDA** | | | | | | | |
    | **P/B Ratio** | | | | | | | |
- [ ] **The Cyclical Inversion Trap:**
  - Is the current multiple optically "cheap" (low P/E) because the company is at the peak of a cyclical commodity boom with peak earnings?
  - Or is the multiple optically "expensive" (high P/E) because earnings are temporarily depressed at a cyclical trough?
- [ ] **Optical Balance-Sheet Distortions:**
  - For cash-rich companies: Compare P/E vs. EV/EBITDA. Does large treasury cash make the business look deceptively expensive on P/E while EV/EBITDA reveals an attractively priced operating core?

---

## 11. Deterministic Peer Comparison (ROIC-Adjusted)

*Assemble true comparable peers using the peer-finder runbook, not generic portal presets.*

- [ ] **Assemble True Comparable Peers:**
  - Execute `src/company/listed/peer-finder.md` to identify 3 to 5 true business model peers across the 5-tier taxonomy, business model archetype, customer concentration, and market cap tier.
- [ ] **The Peer Valuation Matrix (Adjusted for Returns on Capital):**
  | Company Name | Market Cap (₹ Cr) | Primary Multiple (EV/EBITDA or P/E) | 3-Yr Revenue CAGR (%) | Operating ROIC (%) | Net Debt / EBITDA | Quality / Valuation Verdict |
  |---|---|---|---|---|---|---|
  | **Target Company** | | | | | | |
  | **Peer 1** | | | | | | |
  | **Peer 2** | | | | | | |
  | **Peer 3** | | | | | | |
- [ ] **The Relative Justification Test:**
  - If the target company trades at a premium to peers: Is that premium economically justified by superior Operating ROIC, cleaner balance sheet, and stronger moat?
  - If it trades at a discount: Is the discount an unjustified market inefficiency, or a fair penalty for governance friction, customer concentration, or RPT value leakage?

---

## 12. 3-Year Scenario Valuation Distribution & Downside Floor

*Valuation is an asymmetric probability distribution across a strict 3-year horizon. Run `valuation_calculator.py`.*

- [ ] **Define the 3 Grounded Operational Scenarios (Horizon: FY+3):**
  - **Bear Case (Downturn / Thesis-Strained):**
    - Revenue growth drops to downcycle baseline / GDP rate.
    - Operating margin compresses to 10-year historical cycle trough (from Part A).
    - Valuation multiple de-rates to 10-year **25th percentile or minimum**.
  - **Base Case (Realistic Grounded Execution):**
    - Revenue growth matches Stage 1 capacity constraints and Stage 2 say-do baseline.
    - Operating margin reflects sustainable, normalized through-cycle levels.
    - Valuation multiple stays at **10-year historical median**.
  - **Bull Case (Optimal Operating Execution):**
    - Capacity debottlenecking commissions on schedule; full utilization achieved.
    - Operating margin expands to upper guided band due to operating leverage.
    - Valuation multiple re-rates toward **75th percentile**.
- [ ] **Scenario Outputs Table:**
  | Dimension | Bear Case (Year 3) | Base Case (Year 3) | Bull Case (Year 3) |
  |---|---|---|---|
  | **Revenue (₹ Cr)** | | | |
  | **EBITDA / PAT (₹ Cr)** | | | |
  | **Exit Multiple (EV/EBITDA or P/E)** | | | |
  | **Target Enterprise Value (₹ Cr)** | | | |
  | **Net Debt / (Net Cash) (₹ Cr)** | | | |
  | **Target Equity Value (₹ Cr)** | | | |
  | **Target Price per Share (₹)** | | | |
  | **Expected 3-Yr Return CAGR (%)** | | | |
- [ ] **The Downside Floor & Risk-Reward Asymmetry:**
  - Compute the maximum drawdown from Current Market Price to the Bear Case floor:
    - Downside to Bear Floor (%) = [(Bear Case Price - CMP) / CMP] * 100%
    - Upside to Base Case (%) = [(Base Case Price - CMP) / CMP] * 100%
    - Risk-Reward Asymmetry Ratio = Upside to Base Case (%) / |Downside to Bear Floor (%)|
  - **The Asymmetry Rule:** Avoid investments where downside risk exceeds upside potential (Asymmetry < 1.0). Require an Asymmetry Ratio >= 2.0 for entry.
- [ ] **Dynamic Margin of Safety Assessment:**
  - Margin of Safety (%) = [(Base Case Fair Value - CMP) / Base Case Fair Value] * 100%
  - Scale required cushion inversely to business durability and cyclicality:
    - *Tier 1 (High-Grade Compounder, Net Cash, Confirmed Moat):* Requires **15%–20% margin of safety**.
    - *Tier 2 (Cyclical / High Customer Concentration / Medium Moat):* Requires **25%–35% margin of safety**.
    - *Tier 3 (High Leverage / High Contingent Liabilities / RPT Friction):* Requires **40%+ margin of safety** (or immediate PASS).

---

## 13. The Financials & Valuation Verdict (Do this last)

State the verdict across three objective, evidence-backed axes:

> ### 1. Financial & Forensic Integrity: **[Clean / Monitorable / Fragile / Dangerous]**  
> *Basis:* 10-year Cumulative CFO converted to [____%] of Cumulative PAT; treasury yield on cash is [____%] ([normal / unencumbered / suspicious]); tax paid matches [statutory / low] rates; CWIP aging is [clean / stalled]; and contingent liabilities represent [____%] of Net Worth.
>
> ### 2. Capital Treadmill & Self-Funding Reality: **[Self-Funder / Moderate Absorber / Dilution Furnace]**  
> *Basis:* Each ₹100 of incremental revenue consumed ₹[____] of working capital and ₹[____] of capex. 10-year cumulative FCF was ₹[____] Cr. The company [funds its own growth / relies on bank debt / repeatedly dilutes equity]. Core Operating ROIC is [____%] vs. WACC of [____%], resulting in Moat Status: **[CONFIRMED / FALSIFIED / NO MOAT]**.
>
> ### 3. Valuation Collision & Margin of Safety: **[Significant Cushion / Fairly Valued / Over-Priced / Euphoric]**  
> *Basis:* At CMP of ₹[____], the 3-year inversion requires an exit multiple of [____x] (vs. 10-yr median of [____x]). Base Case intrinsic value is ₹[____] ([____%] upside/downside). Downside to Bear Case floor is [____%], yielding an Asymmetry Ratio of [____:1]. Margin of safety is [adequate / inadequate] for this business tier.

---

## 14. Handoff to Stage 4 (The Investment Decision)

*All load-bearing quantitative findings tagged `Fact → Stage 4` collect here:*

- **Variant Perception Arithmetic:** The quantitative gap between what the market price implies (from Section 8 Inversion) vs. what the company can physically and financially deliver (from Section 9 Collision).
- **Pre-Mortem Failure Modes:** Quantified balance-sheet vulnerabilities to feed directly into the Stage 4 Pre-Mortem:
  - Contingent liabilities >15%–20% of Net Worth.
  - Capital treadmill financing deficit (dilution risk).
  - Working capital bloat or debtor concentration in aging buckets >6 months.
- **Observable Kill Triggers:** Quantitative tripwires that invalidate the thesis:
  - Core Operating ROIC dropping below WACC (`____%`).
  - Receivables aging >6 months exceeding `____%` of total revenue.
  - Warranty additions expanding above `____%` of sales.
  - Sanctioned bank line utilization exceeding 90%.
- **Dated Investment Catalysts:** Verified capex commissioning dates (from Section 2 ledger check) and debt retirement milestones to populate the Stage 4 catalyst clock.
- **Position Sizing Guidance:** Risk-Reward Asymmetry Ratio and Margin of Safety percentage to dictate final recommendation (`BUY`, `WATCHLIST`, or `PASS`) and portfolio sizing in Stage 4.
