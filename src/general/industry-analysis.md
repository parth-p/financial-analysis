# Industry & Sector Analysis — Agent Playbook (Indian Markets)
*A deterministic, machine-executable runbook for deep industry arena diagnostics across Indian equities (NSE/BSE). Written for an AI agent to execute end-to-end; readable by an institutional research analyst.*

**Scope:** Indian industries and sub-segments across Level 3 (Industry), Level 4 (Basic Industry), and Level 5 (Product / Niche) of the Indian Market Taxonomy. **Not** generic macro commentary or investment advice; a grounded diagnostic of supply-demand dynamics, value chain economics, capital cycles, and competitive structure.

---

## 0. Operating Principles (Agent Invariants)

1. **Supply > Demand (The Capital Cycle Invariant):** High demand growth does not equal high equity returns. If demand grows at 12% but industry capacity expands at 25%, realizations collapse and economic profit vanishes. Always prioritize the **supply-side pipeline** (under-construction capex, plant additions, import volumes) over demand projections.
2. **End-Market Determinism:** An industry does not control its own destiny in isolation. In B2B and process industries, the industry inherits the cyclicality, working capital terms, and pricing power of its customer end-markets. Always decompose who buys, how much of their Bill of Materials (BOM) this product represents, and who holds the pricing leverage.
3. **No Vendor TAM Hype:** Third-party paid research press releases (*"Market to reach $50B by 2030 at 18% CAGR"*) are marketing material, not evidence. Treat them as `[UNVERIFIED TAM]`. Rely strictly on verified data: Industry Associations (SIAM, IEEMA, CMA, FAI, TMA, CEAMA), Regulators & Ministries (CEA, PPAC, DGCA, Ministry of Commerce, RBI), Credit Rating Rationales (CRISIL, ICRA, CARE, India Ratings), and statutory filings (RHP/DRHP industry chapters, annual reports).
4. **The China Invariant:** In manufacturing, chemicals, APIs, metals, and electronics, evaluate global trade reality. If China controls >40% of global capacity, Indian domestic pricing is dictated by **Import Parity Pricing (IPP)** and dumping risk, not domestic cost structures.
5. **No Academic Fluff:** Skip generic Porter's Five Forces checklists with adjective soup ("supplier power is moderate"). Identify the **Single Binding Bottleneck** that caps industry returns.
6. **STRICTLY NO LaTeX Formatting:** Use plain Markdown formulas and standard arithmetic symbols (`*`, `/`, `+`, `-`, `>=`, `<=`). Never use `$$`, `\frac`, `\times`, or LaTeX tags.
7. **Provenanced & Dated Facts:** Every capacity figure, market share, utilization percentage, and regulatory duty must cite its source and reference period (e.g., `FY25`, `CY24`). If unverified, label it `[UNVERIFIED]`.

---

## 1. Input & Invocation

**How to invoke:**
```text
RUN INDUSTRY ANALYSIS industry="<Industry / Sub-segment Name>" [scope="<optional notes>"] [as_of_date="YYYY-MM-DD"]
```

*Examples of actionable industries:*
- `Indian Power Transformers (Transmission & Distribution)`
- `Agrochemical Formulations & Active Ingredients`
- `Cables & Wires (Power Cables, Building Wires, Communication)`
- `Diagnostic Healthcare (Pathology & Radiology Chains)`
- `City Gas Distribution (CNG & Piped Natural Gas)`
- `Flexible Packaging (BOPET & BOPP Films)`
- `Commercial Refrigeration & Cold Chain Equipment`

**Default Parameters:**
| Parameter | Default | Meaning |
|---|---|---|
| `industry` | Required | Target industry, basic industry, or product niche |
| `scope` | Auto-detected | Specific focus within the value chain (e.g., "high-voltage only") |
| `as_of_date` | Current Date (IST) | Cutoff date for recent data and filings |
| `output_path` | `tmp/general/industry/<industry-slug>.md` | Storage path for final analysis |

---

## 2. Research & Data Source Protocol

The agent must execute research across four independent tiers before drafting:

```
[Tier 1: Industry Bodies & Ministries]
  - CEA, PPAC, DGCA, NHAI, Ministry of Commerce, Ministry of Chemicals & Fertilizers
  - SIAM, IEEMA, CMA (Cement), FAI (Fertilizer), CEAMA, TMA (Tractors), OPPI/IDMA
      │
[Tier 2: Credit Rating Sector Primers & Reports]
  - CRISIL MI&A, ICRA Industry Outlines, CARE Ratings, India Ratings Rationales
      │
[Tier 3: Regulatory Filings & Primary Prospectuses]
  - RHP/DRHP Section: "Industry Overview" of recent IPOs in this sector (last 1–3 years)
  - Annual Reports & Investor Presentations of top 3–5 listed pure-plays
  - Earnings Concall Transcripts across the last 4 quarters (track utilization & commentary)
      │
[Tier 4: Financial & Valuation Baskets]
  - Screener.in peer basket for 10-year median ROCE, EBITDA margins, and CCC
```

---

## 3. The 6 Analytical Stages

```
+-----------------------------------------------------------------------------------------+
| Stage 0: Taxonomy, Scope & Economic Archetype (Boundary Setting)                        |
+-----------------------------------------------------------------------------------------+
                                            │
                                            ▼
+-----------------------------------------------------------------------------------------+
| Stage 1: Value Chain Architecture & End-Market Matrix (Who Squeezes Whom?)             |
+-----------------------------------------------------------------------------------------+
                                            │
                                            ▼
+-----------------------------------------------------------------------------------------+
| Stage 2: The Capital Cycle & Capacity Pipeline (Supply Diagnostic)                      |
+-----------------------------------------------------------------------------------------+
                                            │
                                            ▼
+-----------------------------------------------------------------------------------------+
| Stage 3: Competitive Conduct, Formalization & The China Invariant                      |
+-----------------------------------------------------------------------------------------+
                                            │
                                            ▼
+-----------------------------------------------------------------------------------------+
| Stage 4: Cost Structure, Working Capital & Statutory Sandbox                            |
+-----------------------------------------------------------------------------------------+
                                            │
                                            ▼
+-----------------------------------------------------------------------------------------+
| Stage 5: The Cycle Clock, Core KPIs & The Graveyard (Historical Failure Modes)          |
+-----------------------------------------------------------------------------------------+
```

---

### STAGE 0 — Taxonomy, Scope & Economic Archetype

**Objective:** Anchor the industry in the statutory Indian market hierarchy, set strict boundaries (what is in vs. out), and classify the underlying economic engine.

**Procedure:**
1. **Taxonomy Match:** Map the industry to `data/indian_market_taxonomy_5_tier.md`:
   - Level 1: Macro-Economic Sector (e.g., *Capital Goods*)
   - Level 2: Sector (e.g., *Electrical Equipment*)
   - Level 3: Industry (e.g., *Electrical Equipment*)
   - Level 4: Basic Industry (e.g., *Transformers*)
   - Level 5: Investable Sub-Segment / Niche (e.g., *Power & Distribution Transformers >220 kV*)
2. **Boundary Definition:** Explicitly write:
   - *Included in scope:* Specific product categories, voltage classes, chemistry types, or business models.
   - *Excluded from scope:* Adjacent or downstream products that trade on different economics (e.g., "Includes Power Transformers; excludes Distribution Transformers <33 kV and dry-type transformers").
3. **Economic Archetype Classification:** Classify into one primary archetype:
   - *Cyclical Commodity:* Standardized product, price-taker on global/domestic spreads, heavy fixed capex (e.g., Cement, Steel, BOPP films).
   - *B2B Process Compounder:* High engineering content, customer-specific customization, long qualification cycles, stable margins (e.g., Auto precision forgings, specialized chemical intermediates).
   - *Working Capital Absorber / Contractor:* High tender gross margins, but heavy retention money, bank guarantees, and stretched receivables (e.g., Power T&D EPC, Water infrastructure).
   - *Consumer / Distribution Moat:* High marketing spend, dealer network lock-in, negative/low working capital, strong retail pricing power (e.g., Decorative paints, branded wires & switches).
   - *Regulated / Tariff-Protected Utility:* Capex returns capped or regulated by statutory authorities, captive demand (e.g., CGD, Power transmission lines).

**Gate:** Proceed only after establishing explicit IN/OUT boundaries.

---

### STAGE 1 — Value Chain Architecture & End-Market Matrix

**Objective:** Map how the industry connects from raw materials to final consumption, where profit pools accumulate, and the economic profile of customer end-markets.

**Procedure:**
1. **Value Chain Node Mapping:** Trace the 4–6 discrete nodes along the chain:
   ```text
   Raw Material Inputs -> Primary Processing / Intermediates -> Component / Specialized Formulation -> Final Assembly / Equipment -> Distribution Channel -> End-User
   ```
2. **Profit Pool & Margin Migration:**
   - For each node, estimate typical EBITDA margin ranges (%) and asset intensity.
   - **Where does economic profit pool?** Name the node that captures outsized returns and state why (e.g., proprietary chemistry, patent protection, high capital barrier).
   - **Where does margin compression occur?** Name the node caught between rising input costs and powerful downstream buyers.
3. **End-Market & Customer Arena Architecture:**
   - Fill the **End-Market Matrix**:
     | End-User Industry | % of Total Industry Demand | Cyclicality (High / Med / Low) | Typical Payment Terms | Customer Buying Power (High / Med / Low) |
     |---|---|---|---|---|
   - **BOM Cost Asymmetry (The "Who Cares?" Test):**
     - Does this product account for **<3% of the customer's total project/product Bill of Materials (BOM)** while carrying catastrophic operational risk if it fails? (High pricing power; customer values reliability over lowest price).
     - Or is it **>20% of the customer's BOM**? (Low pricing power; customer runs reverse e-auctions to grind every rupee).
   - **Customer Decision-Maker vs. Payer:** Does the end-client specify the approved vendor code (e.g., PGCIL, NTPC, global auto OEM), leaving the EPC contractor or Tier-1 assembler with zero discretion to switch?

---

### STAGE 2 — The Capital Cycle & Capacity Pipeline (Supply Diagnostic)

**Objective:** Determine whether the industry is heading into a supply deficit (pricing power) or an impending supply glut (margin destruction).

**Procedure:**
1. **Current Utilization Landscape:**
   - Estimate industry-wide capacity utilization (%) in India:
     - *Seller's Market (>80%–85%):* Order backlogs stretch, lead times lengthen, conversion spreads expand.
     - *Balanced (70%–80%):* Normal competitive pricing, steady volume growth.
     - *Buyer's Market (<65%–70%):* Unorganized price wars, fixed-cost under-absorption, discounting.
2. **The Capex & Supply Pipeline (The Next 12–36 Months):**
   - Identify all material under-construction greenfield and brownfield capacity additions across listed and unlisted players:
     | Company / Group | Addition Type (Brownfield / Greenfield) | New Capacity (in MT / units / MVA) | Capex (₹ Cr) | Expected Commissioning Date |
     |---|---|---|---|---|
   - **Supply Additions vs. Demand Run-Rate:** Will aggregate industry capacity expand faster than domestic demand growth + realistic export growth? (e.g., "Demand growing at 10% YoY, but capacity expanding by 28% across FY26–27 -> high risk of margin compression post-commissioning").
3. **Capex Physics & Asset Turnover:**
   - What is the typical asset turnover on new capex? (`Net Revenue / Gross Block`).
   - What is the minimum capital outlay required for an economically viable plant?
   - How long does it take from board approval to commercial production (capex gestation lead time)?

---

### STAGE 3 — Competitive Conduct, Formalization & The China Invariant

**Objective:** Assess how rivals compete (price wars vs. non-price barriers), measure formalization velocity, and evaluate import threats.

**Procedure:**
1. **Market Sizing & Concentration:**
   - Current market size in volume (units/tonnes) and value (₹ Crore).
   - Top 4 Concentration Ratio (CR4) and aggregate market shares of Tier-1 players.
   - Characterize the market: Monopolistic, Tight Oligopoly (3–4 disciplined players), Fragmented, or Cut-throat Commodity.
2. **Pricing Mechanism & Conduct:**
   - How are prices set across the industry?
     - *Formulaic PVC (Price Variation Clause):* Contractually linked to indices (e.g., LME copper/aluminium, ICIS chemical prices, wholesale price indices).
     - *L1 Tender Bidding:* Lowest bidder wins public/institutional procurement. (Frequent winner's curse; low structural returns).
     - *Import Parity Pricing (IPP):* Domestic price = Landed cost of imported goods (FOB price + ocean freight + customs duty + port handling).
     - *Brand / Retail Pricing Power:* Sticky retail MRP, dealer margins protected.
3. **The China Invariant & Import Threat:**
   - What percentage of global manufacturing capacity resides in China?
   - Is there a material price gap between landed Chinese imports and Indian domestic production costs?
   - Trade defense mechanisms in place:
     - Anti-Dumping Duty (ADD) or Countervailing Duty (CVD): Specify active rates and expiry dates.
     - Bureau of Indian Standards (BIS) Quality Control Orders (QCO): Are foreign plants required to obtain BIS licenses to export to India? Has enforcement restricted low-cost imports?
4. **Organized vs. Unorganized Split & Formalization Velocity:**
   - Current split: % Organized vs. % Unorganized / Regional players.
   - What is driving formalization? (Check for real catalysts: tightening GST e-invoicing thresholds, strict BIS compliance enforcement, institutional builder procurement requiring quality warranties).
   - Is the unorganized sector actually shrinking, or holding market share via cash discounts and local logistics advantages?

---

### STAGE 4 — Cost Structure, Working Capital & Statutory Sandbox

**Objective:** Dissect the operational cost anatomy, cash absorption realities, and regulatory approvals governing survival.

**Procedure:**
1. **Cost Structure & Raw Material Anatomy:**
   - Bill of Materials (BOM) breakdown: Top 3 input costs as % of total revenue (e.g., specialized steel, copper, natural gas, crude derivatives, labor).
   - Operating leverage threshold: What is the estimated fixed vs. variable cost split? At what capacity utilization does the median player achieve EBITDA break-even?
   - Pass-Through Lag: If raw materials spike by 20%, how many weeks/months does it take the industry to pass this on to customers? (State the historical gross margin contraction during sudden input rallies).
2. **Working Capital Dynamics & Banking Line Bottlenecks:**
   - **Cash Conversion Cycle (CCC):** Debtor days + Inventory days - Creditor days.
   - Is the industry a cash generator (negative working capital, customer advances) or a working capital sponge (every ₹100 of new sales locks up ₹35 in receivables and buffer stock)?
   - **Non-Fund-Based (NFB) Bank Guarantee Intensity:**
     - Does the industry require heavy Bank Guarantees (Performance BGs, Advance BGs) or Letters of Credit (LCs) to execute orders?
     - Are bank limits a ceiling on growth?
3. **Statutory & Environmental Sandbox:**
   - **Environmental Approvals:** Does the industry require Consent to Establish (CTE) and Consent to Operate (CTO) from State Pollution Control Boards (SPCB)? Are plants mandated to operate with Zero Liquid Discharge (ZLD)?
   - **Policy Subsidies & PLI:** Is the sector benefiting from Production-Linked Incentive (PLI) schemes? State total scheme outlay, disbursed amounts to date, and whether the incentives artificially prop up operating margins.
   - **Price Controls & Statutory Caps:** Does the government regulate end-prices (e.g., NPPA drug price caps, APM gas allocation, fertilizer subsidy formulas, power tariff caps)?

---

### STAGE 5 — The Cycle Clock, Core KPIs & The Graveyard

**Objective:** Pinpoint where the industry sits on its cycle today, identify the critical operating metrics, and document how companies in this sector historically blow up.

**Procedure:**
1. **The Cycle Clock (Current Status):**
   - Classify the current industry position into one of 4 phases:
     - *Phase 1: Trough / Rationalization:* Depressed margins, capacity shutdowns, zero capex announcements, distressed asset sales.
     - *Phase 2: Mid-Cycle Expansion:* Demand absorbs idle capacity, utilization crosses 75%, conversion spreads firm, operating leverage drives margin expansion.
     - *Phase 3: Late-Cycle Peak:* Plants at 90%+ utilization, record EBITDA margins, industry-wide multi-thousand-crore greenfield capex announcements, aggressive management guidance.
     - *Phase 4: Downcycle / Supply Collision:* New capex hits the market simultaneously, supply outpaces demand, discounting starts, inventory write-downs occur.
2. **The Single Leading Indicator (The 6-to-12 Month Canary):**
   - Name the single best high-frequency or forward-looking data series that signals an inflection in this industry 6–12 months in advance (e.g., *monthly CEA transmission line tender awards*, *domestic commercial vehicle wholesale dispatches*, *global caustic soda-chlorine spread*, *bauxite/alumina spot price ratio*).
3. **The 3–5 Core Sector KPIs:**
   - List the exact operational metrics tracked by institutional analysts for this sector (e.g., *Spread per Ton*, *Plant Load Factor / PLF*, *RevPAR & ARR*, *Asset Turnover*, *EBITDA per Ton*, *Order Book-to-Bill Ratio*). Provide recent benchmark values.
4. **Structural Return on Capital (ROCE vs. WACC Hurdle):**
   - What is the 10-year median ROCE across the listed peer basket?
   - Compare to the Indian equity cost of capital hurdle (**12%**):
     - If 10-year median ROCE > 18%: **Structural Wealth Compounder** (industry structure protects economic rents).
     - If 10-year median ROCE between 12%–16%: **Cyclical Capital Preserver** (earns returns only during the upcycle).
     - If 10-year median ROCE < 12%: **Structural Capital Destroyer** (industry destroys economic value across cycles; only low-cost outliers or turnaround plays work).
5. **The Industry Graveyard (Historical Failure Modes):**
   - How have companies in this sector historically gone bankrupt, entered NCLT/IBC, or permanently destroyed shareholder capital?
   - Detail the top 2–3 failure modes (e.g., *taking on heavy debt for greenfield capex at the peak of the cycle right before Chinese dumping hit*; *unhedged foreign currency debt for imported equipment*; *bidding aggressively at fixed L1 tender prices right before a steel/copper commodity spike*).

---

## 4. Structured Output Document Template

The agent must output the final report to `tmp/general/industry/<industry-slug>.md` using this exact structure:

```markdown
# Industry Diagnostic: [Industry Name]

**Taxonomy Code:** [L1: Macro] > [L2: Sector] > [L3: Industry] > [L4: Basic Industry] > [L5: Sub-segment]
**Economic Archetype:** [Cyclical Commodity / B2B Process Compounder / Working Capital Absorber / Consumer Brand / Regulated Utility]
**Cycle Clock Phase:** [Trough / Mid-Cycle Expansion / Late-Cycle Peak / Supply Collision]
**Report Date:** YYYY-MM-DD
**Analyst Engine:** Antigravity Equity Research Framework

---

## Executive Diagnostic & Thesis
[2–3 paragraphs summarizing the fundamental state of the industry: supply-demand balance, where profit pools accumulate, current cycle status, and whether this industry structurally compounds or destroys capital.]

---

## 1. Industry Scope & Boundary
- **Included:** [Specific products, chemistries, ratings, or models]
- **Excluded:** [Adjacent segments excluded from this analysis]
- **Market Sizing:**
  - Total Indian Market: ₹[X] Crore (Value) | [Y] [Units/Tonnes] (Volume) [Year/Source]
  - Estimated 3–5 Year Volume Growth: [X]% CAGR
  - Export vs. Domestic Split: [X]% Domestic | [Y]% Exports

---

## 2. Value Chain & End-Market Matrix

### Value Chain Architecture
`[Node 1: Raw Materials] -> [Node 2: Processing] -> [Node 3: Manufacturing/Assembly] -> [Node 4: Distribution] -> [Node 5: End-User]`
- **Profit Pool Winner:** [Which node captures outsized margins and why]
- **Margin Squeeze Node:** [Which node faces perpetual margin pressure]

### End-Market Matrix
| Customer Industry | % of Total Demand | Cyclicality | Payment Terms | Customer Buying Power |
|---|---|---|---|---|
| [Industry A] | [X]% | [High/Med/Low] | [Days / Advances / LC] | [High/Med/Low] |
| [Industry B] | [Y]% | [High/Med/Low] | [Days / Advances / LC] | [High/Med/Low] |

- **BOM Cost Asymmetry:** [Does this product cost <3% of customer BOM with catastrophic failure risk, or >20% with heavy price negotiations?]
- **Payer vs. Specifier:** [Who specifies the vendor code vs. who writes the cheque]

---

## 3. The Capital Cycle & Capacity Pipeline (Supply Diagnostic)
- **Current Industry Utilization:** [X]% across India
- **Market Balance:** [Seller's Market (>80%) / Balanced / Buyer's Market (<65%)]
- **Upcoming Capacity Pipeline (Next 12–36 Months):**
  | Company | Project Type | Capacity Added | Capex (₹ Cr) | Expected Commissioning |
  |---|---|---|---|---|
- **Supply vs. Demand Verdict:** [Will new supply outpace demand growth? State risk of margin compression.]
- **Capex Economics:** Asset Turnover on new capex = [X]x | Gestation Lead Time = [X] months.

---

## 4. Competitive Landscape & Trade Dynamics
- **Market Structure:** [Monopolistic / Tight Oligopoly / Fragmented]
- **CR4 Ratio:** Top 4 players hold [X]% combined market share.
  - *Tier-1 Players:* [Company A (X%), Company B (Y%), Company C (Z%)]
- **Pricing Mechanism:** [Formulaic PVC / L1 Tenders / Import Parity Pricing (IPP) / Brand MRP]
- **The China Invariant & Import Threat:**
  - China's Global Capacity Share: [X]%
  - Landed Import Cost Differential: [Cheaper by X% / Domestic parity]
  - Trade Protections: [Active ADD/CVD rates and expiry | BIS QCO enforcement status]
- **Organized vs. Unorganized Split:** [X]% Organized vs [Y]% Unorganized. [Is formalization occurring? State exact drivers.]

---

## 5. Cost Structure, Working Capital & Statutory Sandbox
- **BOM Anatomy:**
  - Raw Material 1: [X]% of cost
  - Raw Material 2: [Y]% of cost
  - Power / Energy / Fuel: [Z]% of cost
- **Operating Leverage & Pass-Through:** Fixed vs. Variable split = [X:Y]. Raw material pass-through lag = [X] days/months.
- **Working Capital Profile:**
  - Cash Conversion Cycle: [X] days (Debtors: [D] days, Inventory: [I] days, Creditors: [C] days).
  - Non-Fund-Based (NFB) Bank Guarantee Intensity: [High / Medium / Low]. [Are bank limits a bottleneck?]
- **Statutory Sandbox:**
  - Pollution / Environmental: [SPCB CTO requirements, ZLD status]
  - Government Subsidies / PLI: [Active schemes, status of disbursements]
  - Regulatory Price Controls: [None / Capped / Subsidized]

---

## 6. The Cycle Clock, Sector KPIs & The Graveyard
- **Current Cycle Phase:** [Trough / Mid-Cycle Expansion / Late-Cycle Peak / Supply Collision]
- **The Single Leading Indicator:** [Name the 6–12 month leading indicator and its latest trend/print]
- **Core Sector KPIs:**
  1. [KPI 1]: [Recent Value] (Historical range: [X] to [Y])
  2. [KPI 2]: [Recent Value]
  3. [KPI 3]: [Recent Value]
- **Structural ROCE vs. Cost of Capital (12%):**
  - 10-Year Median ROCE across listed basket: [X]%
  - Verdict: [Structural Wealth Compounder (>18%) / Cyclical Capital Preserver (12-16%) / Structural Capital Destroyer (<12%)]
- **The Industry Graveyard (Historical Failure Modes):**
  1. *[Failure Mode 1]:* [Description of how past players blew up]
  2. *[Failure Mode 2]:* [Description]

---

## 7. Listed Pure-Play & Proxy Universe
| Company Name | Ticker | Market Cap (₹ Cr) | Core Revenue Exposure (%) | Net Debt/Equity | 3-Yr Median ROCE (%) |
|---|---|---|---|---|---|
| [Company 1] | [NSE: TICKER] | [X] | [Y]% | [Z] | [W]% |
| [Company 2] | [NSE: TICKER] | [X] | [Y]% | [Z] | [W]% |

---

## Research Audit & Provenance Log
- **Primary Sources Checked:** [List associations, ministries, filings, concalls actually read]
- **Unverified Items Tagged:** [List any metrics that could not be corroborated from primary filings]
```

---

## 5. Execution Summary (One-Line Workflow)

> **Map taxonomy and boundaries (Stage 0) -> dissect value chain and end-market BOM leverage (Stage 1) -> evaluate capital cycle and supply additions pipeline (Stage 2) -> test competitive conduct, formalization, and China import parity (Stage 3) -> inspect cost anatomy, pass-through lags, and NFB working capital limits (Stage 4) -> diagnose the cycle clock, track the 6-month leading indicator, compare 10-year ROCE against the 12% hurdle, and study historical graveyard blowups (Stage 5) -> compile into `tmp/general/industry/<industry-slug>.md`.**
