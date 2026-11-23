# Headwind / Tailwind & Catalyst Diagnostic — Agent Playbook (Force-Field Analysis)
*A deterministic, machine-executable runbook for evaluating headwinds, tailwinds, and catalysts across Indian listed companies, industries, and sectors. Written for an AI agent to execute end-to-end; readable by an institutional research analyst.*

**Scope:** Applicable polymorphically to any Indian listed company (NSE/BSE), industry, or sector. **Not** a superficial retail pros/cons list; an institutional diagnostic of transmission mechanisms, operating leverage multipliers, subsidy fragility, consensus pricing, and net vector synthesis.

---

## 0. Operating Principles (The Agent Invariants)

1. **No Untransmitted Forces:** Naming a macro phenomenon (e.g., "China+1", "urbanization", "interest rates") without tracing its physical **transmission line** to the P&L or balance sheet is a failure. Every force must map directly to: Volume, Gross Spread / Realization, Operating Overheads, Working Capital / Bank Guarantees, or Terminal Multiple.
2. **The Leverage Multiplier (Asymmetry Invariant):** Volume growth does not equal profit growth. A 10% volume tailwind hitting a high-fixed-cost business (hotels, hospitals, precision manufacturing) can trigger a 30% to 50% surge in operating profit via operating leverage. Conversely, a 10% volume headwind hitting a company with heavy debt (>1.0x D/E) can completely wipe out net profit. Always state the operating and financial leverage sensitivity.
3. **Priced-in vs. Variant Perception:** If an industry headwind or tailwind is universally known to the consensus, the market has already factored it into the stock's valuation multiple. The analytical edge lives exclusively in **Variant Perception**: where consensus miscalculates the magnitude, misjudges the duration, or misses an impending inflection.
4. **The Subsidy Cliff & Regulatory Fragility:** In India, many powerful tailwinds are artificial creations of statutory policy (PLI incentives, FAME subsidies, Anti-Dumping Duties, BIS Quality Control Orders). Every policy-driven tailwind must be subjected to a **Fragility Audit**: statutory expiry dates, sunset review risk, and whether the business model survives "naked" without government protection.
5. **Tailwind Commoditization & Free-Lunch Fallacy:** A massive, obvious tailwind attracts aggressive capital, new entrants, and capacity doubling. An agent must evaluate whether the tailwind is protected by high barriers to entry (patents, 3-year OEM qualifications, statutory licenses) or will be commoditized into a price war within 12–24 months.
6. **Reflexive Feedback Loops:** Forces are reflexive. A booming sector tailwind leads to aggressive equity dilution (QIPs/IPOs) and simultaneous industry-wide capex, actively creating the next oversupply headwind. An agent must identify the negative feedback loop triggered by current tailwinds.
7. **Strictly Top 3–5 Dominant Forces:** Never generate exhaustive 15-item laundry lists. Restrict analysis to the **Top 3–5 Dominant Tailwinds** and **Top 3–5 Dominant Headwinds** that move operating profit by >=5%.
8. **STRICTLY NO LaTeX Formatting:** Use plain Markdown formulas and standard arithmetic symbols (`*`, `/`, `+`, `-`, `>=`, `<=`). Never use `$$`, `\frac`, `\times`, or LaTeX tags.
9. **Provenanced & Dated Facts:** Every capacity figure, duty rate, raw material price move, and market share trend must cite its source and reference period (e.g., `FY25`, `Q2 FY26`). If unverified, label it `[UNVERIFIED]`.

---

## 1. Input & Polymorphic Invocation

**How to invoke:**
```text
RUN HEADWIND TAILWIND target="<Ticker | Company Name | Industry | Sector>" [as_of_date="YYYY-MM-DD"]
```

*Examples:*
- Company Target: `RUN HEADWIND TAILWIND target="Tata Motors Ltd"` or `target="Poly Medicure"`
- Industry Target: `RUN HEADWIND TAILWIND target="Indian Commercial Real Estate"` or `target="Specialty Chemicals"`
- Sector Target: `RUN HEADWIND TAILWIND target="Indian Power Transmission & Distribution"`

### Polymorphic Detection Logic:
The agent automatically detects the entity type and routes the analytical scope:
- **If Company Target:** Evaluates all 3 layers: Micro / Idiosyncratic (Company Execution, Moat, Debt) + Meso (Industry Arena) + Macro (Exogenous). Traces transmission to company EPS, ROCE, and debt covenants. Output routes to `tmp/company/adhoc/<slug>-headwinds-tailwinds.md`.
- **If Industry / Sector Target:** Evaluates 2 layers: Meso (Industry Capacity, Competitive Conduct, Value Chain) + Macro (Trade, Policy, Commodity Cycles). Traces transmission to industry aggregate capacity utilization, median gross spreads, and return on capital. Output routes to `tmp/general/industry/<slug>-headwinds-tailwinds.md`.

---

## 2. The 4-Dimensional Anatomy of Every Force

Every single candidate force admitted into the analysis must be characterized across four mandatory dimensions:

| Dimension | Classification Categories | Analytical Meaning |
|---|---|---|
| **1. Locus & Controllability** | **Exogenous (Macro)** / **Arena (Industry)** / **Endogenous (Micro)** | Determines management agency. Macro = hedge/pass-through only; Arena = competitive response; Micro = direct operational control. |
| **2. Horizon & Velocity** | **Transitory (<12M)** / **Cyclical (1–3Y)** / **Secular (3–10Y)** | Transitory = mean-reverting noise/buying opportunity; Cyclical = capital cycle supply wave; Secular = permanent structural shift. |
| **3. Financial Transmission Line** | **Volume** / **Gross Spread** / **Overheads** / **Working Capital** / **Terminal Multiple** | Where the force hits the numbers. No force exists without an explicit line item impact. |
| **4. Market Pricing Status** | **Fully Priced (Consensus)** / **Underappreciated** / **Variant Perception** | Identifies whether the force offers alpha or is already discounted in the valuation multiple. |

---

## 3. The 6 Analytical Stages

```
+-----------------------------------------------------------------------------------------+
| Stage 0: Target Framing, Baseline Fundamentals & Leverage Check                         |
+-----------------------------------------------------------------------------------------+
                                            │
                                            ▼
+-----------------------------------------------------------------------------------------+
| Stage 1: Deconstruct & Filter the Top 3–5 Dominant Tailwinds                           |
+-----------------------------------------------------------------------------------------+
                                            │
                                            ▼
+-----------------------------------------------------------------------------------------+
| Stage 2: Deconstruct & Filter the Top 3–5 Dominant Headwinds                           |
+-----------------------------------------------------------------------------------------+
                                            │
                                            ▼
+-----------------------------------------------------------------------------------------+
| Stage 3: The Fragility & Commoditization Audit (Subsidies, Entry & Reflexivity)         |
+-----------------------------------------------------------------------------------------+
                                            │
                                            ▼
+-----------------------------------------------------------------------------------------+
| Stage 4: Force Collision & Net Vector Synthesis (The Directional Clash)                 |
+-----------------------------------------------------------------------------------------+
                                            │
                                            ▼
+-----------------------------------------------------------------------------------------+
| Stage 5: Inflection Triggers, Asymmetry Stress-Test & Kill Conditions                   |
+-----------------------------------------------------------------------------------------+
```

---

### STAGE 0 — Target Framing, Baseline Fundamentals & Leverage Check

**Objective:** Establish the financial baseline, cost structure, and leverage ratios that govern how strongly forces are magnified.

**Procedure:**
1. **Identify Target & Scope:** State whether target is a Company, Industry, or Sector. Extract ticker / ISIN and taxonomy bucket from `data/indian_market_taxonomy_5_tier.md`.
2. **Cost Structure & Operating Leverage Baseline:**
   - Fixed vs. Variable Cost Split: Estimate Fixed Costs (Depreciation, Employee Expenses, Other Fixed Overheads) as a % of total operating costs.
   - Operating Leverage Degree: High (>40% fixed costs; e.g., manufacturing, hotels, hospitals), Medium (20%–40%), Low (<20%; asset-light distributors, software).
3. **Balance Sheet & Financial Leverage Baseline:**
   - Net Debt to EBITDA and Debt to Equity (D/E).
   - Cash Conversion Cycle (CCC in days) and Non-Fund-Based (NFB) Bank Guarantee utilization.
   - Financial Fragility Flag: Is D/E > 1.0x or Net Debt/EBITDA > 2.5x? (If yes, negative forces carry lethal bankruptcy/covenant risks).

---

### STAGE 1 — Deconstruct & Filter the Top 3–5 Dominant Tailwinds

**Objective:** Isolate the 3 to 5 most powerful tailwinds, map their transmission lines, and test whether consensus has already priced them in.

**Procedure:**
1. **Identify Candidates:** Scan across Macro (policy, demographics), Industry (capacity shortages, market expansion, formalization), and Micro (market share gains, new plant commissioning, customer empanelment).
2. **Filter & Select Top 3–5:** Eliminate any tailwind that moves operating profit by <5%. Retain only the dominant growth engines.
3. **Deconstruct Each Tailwind:** For each selected tailwind, document:
   - *Title & Concrete Mechanism:* What is physically happening in the real world?
   - *4-D Vector:* Locus (Macro / Arena / Micro), Horizon (Transitory / Cyclical / Secular), Transmission Line (Volume / Spread / Overheads / Working Capital / Multiple), Market Pricing (Priced-in / Underappreciated / Variant).
   - *Operating Leverage Impact:* How much does a 10% volume or spread gain expand EBIT/PAT?
   - *Magnitude & Duration:* High / Medium / Low magnitude over expected duration (months/years).

---

### STAGE 2 — Deconstruct & Filter the Top 3–5 Dominant Headwinds

**Objective:** Isolate the 3 to 5 most severe headwinds, trace where they inflict financial damage, and identify if the market is underestimating their severity.

**Procedure:**
1. **Identify Candidates:** Scan across Macro (FX, interest rates, commodity spikes), Industry (Chinese dumping, competitor greenfield supply, aggressive unorganized discounting), and Micro (customer concentration, audit/regulatory actions, plant outages, cost inflation).
2. **Filter & Select Top 3–5:** Eliminate transitory noise that resolves in one quarter. Keep the structural and capital-cycle headwinds that depress earnings power.
3. **Deconstruct Each Headwind:** For each selected headwind, document:
   - *Title & Concrete Friction:* What is choking revenue, margins, or cash flow?
   - *4-D Vector:* Locus, Horizon, Transmission Line, Market Pricing.
   - *Downside Sensitivity:* Does this headwind threaten debt service, breach banking covenants, or permanently compress gross conversion spreads?
   - *Mitigation Capability:* Can management pass this on contractually (e.g., formulaic Price Variation Clauses), or must the company absorb 100% of the margin hit?

---

### STAGE 3 — The Fragility & Commoditization Audit

**Objective:** Stress-test whether the tailwinds are durable economic moats or fragile illusions that will evaporate or attract destructive competition.

**Procedure:**
1. **The Subsidy & Protectionist Cliff Audit:**
   - Are any tailwinds dependent on government policy (PLI, FAME subsidies, export incentives, Anti-Dumping Duties, BIS QCOs)?
   - For each policy support: State the statutory expiry date, budget allocation trends, and whether the business model generates positive economic profit without it.
2. **Tailwind Commoditization Test:**
   - Does this tailwind have high barriers to entry (patents, 18–36 month customer qualification cycles, statutory environmental CTO caps)?
   - Or does it have zero barriers, allowing capital to flood the arena and trigger a destructive price war within 12–24 months?
3. **Reflexive Feedback Loop Check:**
   - Is current tailwind success breeding future headwinds? (e.g., massive sector-wide equity raising funding duplicate greenfield capacity; raw material shortages caused by industry-wide boom; aggressive hiring triggering wage inflation).

---

### STAGE 4 — Force Collision & Net Vector Synthesis

**Objective:** Slam the tailwinds and headwinds against each other to calculate the Net Directional Vector.

**Procedure:**
1. **Direct Force Collision Table:** Map opposing forces directly against each other:
   - Top-Line Growth Drivers vs. Top-Line Frictions.
   - Margin Expansion Drivers vs. Margin Compression Pressures.
   - Cash Generation Drivers vs. Working Capital Drags.
2. **The Net Vector Verdict:** Synthesize into one of three definitive regimes:
   - **Regime A: Overwhelming Tailwinds Prevail.** Structural growth and margin expansion overpower cyclical headwinds. Earnings compound rapidly.
   - **Regime B: Balanced Friction / Treadmill Economy.** Top-line grows, but margin compression or working capital stretch neutralizes earnings growth. The company is running fast just to stay in the same place.
   - **Regime C: Structural Headwinds Dominate.** Headwinds choke margins and cash flows; tailwinds are insufficient or illusory. High risk of earnings de-rating.
3. **Variant Perception Summary:** State in 2–3 sentences exactly what the consensus believes vs. what this evidence-backed diagnostic concludes.

---

### STAGE 5 — Inflection Triggers, Asymmetry Stress-Test & Kill Conditions

**Objective:** Establish forward-looking triggers that indicate when forces are peaking, reversing, or breaking.

**Procedure:**
1. **Inflection Triggers (When does a Headwind flip into a Tailwind?):**
   - In cyclical businesses, prolonged headwinds cause capacity exits, halting capex and creating the next supply shortage.
   - Name the exact data print that signals a headwind is exhausting itself (e.g., plant shutdown announcements, inventory-to-sales ratio hitting historical lows, raw material price crashing below cash cost of production).
2. **Asymmetry Stress-Test:**
   - *Bear Scenario:* If the primary tailwind is delayed by 12 months AND the primary headwind intensifies by 20%, what happens to EBITDA, cash flow, and debt service?
3. **Pre-Committed Kill Conditions:**
   - List 2–3 observable, verifiable events that would completely invalidate the positive thesis (e.g., "Loss of Anti-Dumping Duty protection without renewal", "Gross spread contracting below ₹X per ton for 2 consecutive quarters", "Net Debt to EBITDA exceeding 3.0x").

---

## 4. Structured Output Document Template

The agent must output the final report using this exact markdown schema:
- If Company: `tmp/company/adhoc/<target-slug>-headwinds-tailwinds.md`
- If Industry/Sector: `tmp/general/industry/<target-slug>-headwinds-tailwinds.md`

```markdown
# Force-Field & Catalyst Diagnostic: [Target Name]

**Entity Type:** [Listed Company / Industry / Sector]
**Taxonomy Anchor:** [L1: Macro] > [L2: Sector] > [L3: Industry] > [L4: Basic Industry]
**Report Date:** YYYY-MM-DD
**Analyst Engine:** Antigravity Equity Research Framework

---

## Executive Diagnostic & The Net Vector Verdict

- **The Net Vector:** [Overwhelming Tailwinds Prevail / Balanced Friction (Treadmill) / Structural Headwinds Dominate]
- **The Core Asymmetry:** [1–2 sentences explaining the interaction between operating leverage and dominant forces]
- **Variant Perception:** [Where our conclusion diverges from the consensus market narrative]

---

## 1. Baseline Financial Architecture & Leverage

- **Fixed vs. Variable Cost Profile:** [X]% Fixed Costs | Operating Leverage Degree: [High / Medium / Low]
- **Balance Sheet Leverage:** Net Debt/EBITDA = [X]x | Debt/Equity = [Y]x
- **Working Capital Baseline:** Cash Conversion Cycle = [X] days | Bank Guarantee / NFB Intensity: [High / Medium / Low]
- **Financial Fragility Verdict:** [Robust / Moderate / Fragile (Vulnerable to volume contractions)]

---

## 2. The Dominant Tailwinds (Top 3–5)

### Tailwind 1: [Title]
- **Mechanism:** [Detailed physical description of what is happening in the real world]
- **4-D Vector:**
  - *Locus:* [Exogenous Macro / Arena Industry / Endogenous Micro]
  - *Horizon:* [Transitory (<12M) / Cyclical (1–3Y) / Secular (3–10Y)]
  - *Transmission Line:* [Volume / Gross Spread / Overheads / Working Capital / Multiple]
  - *Consensus Status:* [Fully Priced / Underappreciated / Variant Perception]
- **Earnings Multiplier:** [Estimated operating leverage impact on EBIT/PAT]
- **Magnitude:** [High (>20% PAT impact) / Medium (5%–20%) / Low (<5%)]

### Tailwind 2: [Title]
[Repeat structure]

### Tailwind 3: [Title]
[Repeat structure]

---

## 3. The Dominant Headwinds (Top 3–5)

### Headwind 1: [Title]
- **Friction Mechanism:** [Detailed description of the friction, regulatory bottleneck, or competitive threat]
- **4-D Vector:**
  - *Locus:* [Exogenous Macro / Arena Industry / Endogenous Micro]
  - *Horizon:* [Transitory (<12M) / Cyclical (1–3Y) / Secular (3–10Y)]
  - *Transmission Line:* [Volume / Gross Spread / Overheads / Working Capital / Multiple]
  - *Consensus Status:* [Fully Priced / Underappreciated / Variant Perception]
- **Downside Damage:** [Margin contraction or cash flow drag impact]
- **Contractual Pass-Through:** [100% Absorbed by Company / Partial Lagged Pass-Through / Formulaic PVC Protection]
- **Magnitude:** [High / Medium / Low]

### Headwind 2: [Title]
[Repeat structure]

### Headwind 3: [Title]
[Repeat structure]

---

## 4. The Fragility & Commoditization Audit

### Policy & Subsidy Cliff Audit
| Policy / Protection Support | Statutory Expiry Date | Fiscal Budget Risk | "Naked" Business Viability Without It |
|---|---|---|---|
| [e.g., PLI Scheme] | [YYYY-MM] | [Low/Med/High] | [Viable / Marginally Profitable / Unviable] |
| [e.g., Anti-Dumping Duty] | [YYYY-MM] | [Sunset review risk] | [Gross margin contracts by X bps] |

### Tailwind Commoditization Risk
- **Barriers to Entry Protecting Tailwinds:** [High / Moderate / Low]
- **New Entrant / Capacity Threat:** [Are new entrants flooding the space? Describe capacity pipeline]

### Reflexive Feedback Loops
- **The Self-Defeating Reaction:** [How does current success create future headwinds? E.g., capex oversupply, input cost spikes]

---

## 5. Force Collision & Synthesis Matrix

| Financial Parameter | Dominant Tailwind Push | Dominant Headwind Drag | Net Directional Vector |
|---|---|---|---|
| **Volume / Revenue** | [Tailwind description] | [Headwind description] | [Expanding / Flat / Contracting] |
| **Gross Margin / Spread** | [Tailwind description] | [Headwind description] | [Expanding / Flat / Compressing] |
| **Cash Conversion & OCF** | [Tailwind description] | [Headwind description] | [Positive / Stretched / Negative] |
| **Valuation Multiple** | [Tailwind description] | [Headwind description] | [Re-rating / Fair / De-rating] |

---

## 6. Inflection Triggers, Asymmetry Stress-Test & Kill Conditions

- **The Primary Inflection Canary:** [The specific data print signaling a headwind is exhausting or tailwind peaking]
- **Asymmetry Bear Stress-Test:**
  - *Scenario:* Primary tailwind delayed by 12 months + Primary headwind intensifies by 20%.
  - *Impact:* EBITDA changes by [X]%, Cash Flow from Operations impact = ₹[Y] Cr, Debt Covenants [Safe / Breached].
- **Pre-Committed Kill Conditions:**
  1. *Kill Trigger 1:* [Verifiable event that breaks the positive thesis]
  2. *Kill Trigger 2:* [Verifiable event]

---

## Research Audit & Provenance Log
- **Primary Sources Consulted:** [List concalls, filings, trade data, ministry circulars]
- **Unverified Assumptions:** [List any assumptions lacking direct filing confirmation]
```

---

## 5. Execution Summary (One-Line Workflow)

> **Frame target and operating leverage baseline (Stage 0) -> dissect and filter top 3–5 tailwinds with 4-D vectors (Stage 1) -> dissect top 3–5 headwinds with transmission lines (Stage 2) -> audit policy subsidy cliffs, entry commoditization, and reflexivity (Stage 3) -> collide forces to determine the net vector and variant perception (Stage 4) -> define inflection triggers, bear stress-test, and pre-committed kill conditions (Stage 5) -> compile into structured markdown report.**
