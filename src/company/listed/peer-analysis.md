# Peer Selection — Agent Runbook (Indian Equities)
*A deterministic, machine-executable procedure for assembling a comparable-company set for relative valuation. Written for an AI agent to run end-to-end; readable by a human reviewer.*

**Scope:** Indian listed equities (NSE / BSE mainboard and SME). **Not** investment advice; a methodology for constructing comps.

---

## 0. Operating principles (the agent must obey these at every stage)

1. **Purpose-binding.** No peer is "correct" in the abstract. Every peer is admitted *for a named use* (the multiple being estimated, or competitive context). A peer good for one use may be invalid for another. Carry the use-tag on every peer.
2. **Source neutrality / fail-closed on bias.** Issuer- or sell-side-selected peer lists (RHP, analyst initiation, company IR decks) are **hypotheses to be falsified, never ground truth** (see Stage 2). Independent reconstruction always takes precedence.
3. **Operational ≠ economic.** Competing for the same customer does **not** make two firms valuation-comparable. Operational peers must independently pass the economic-peer test (Stage 4) before entering the valuation set.
4. **Determinism + provenance.** Every inclusion/exclusion is a rule firing on a value, with the source and value logged. No unexplained judgment. Where a true judgment call is unavoidable, emit it as a flagged `analyst_review_required` item rather than deciding silently.
5. **Fail-closed on thin data.** If a required field is missing or stale for a candidate, the candidate cannot enter the Core set; it is routed to a `data_gap` bucket. Prefer a smaller clean set over a larger dirty one.
6. **Confidence scoring.** Every output peer and the set as a whole carry a 0–1 confidence derived from data completeness, source independence, and dispersion tightness.

---

## 1. Core concepts the agent must distinguish (this is the backbone)

Classify **every** candidate into exactly one of three buckets. These drive which multiple-set it is allowed to influence.

| Bucket | Definition | Admitted for | Forbidden for |
|---|---|---|---|
| **Core economic peer** | Operationally comparable **AND** passes the fundamental-similarity + multiple-consistency test (Stage 4) | The valuation multiple | — |
| **Operational-only peer** | Competes for the same customers/products but trades on different fundamentals (growth, margin, returns, capital structure) | Competitive context, market-share read, sentiment | **Must not** enter the multiple calculation |
| **Valuation analog** | Not an operational competitor, but trades on the **same value driver** and has a matching financial signature (incl. cross-sector / cross-border / unlisted) | The valuation multiple, with an adjustment + caveat | Competitive-context claims |

> The defect in naive peer analysis is collapsing these into one list. The agent keeps them separate and only the **Core economic peers (+ adjusted Valuation analogs)** feed the multiple.

---

## 2. STAGE 0 — Resolve the mandate

**Objective:** fix what is being held constant before any ticker is fetched.

**Procedure**
1. Identify the **target company** (ISIN + NSE/BSE symbol).
2. Identify the **valuation question** → sets the control variable:
   - "cheap for its growth?" → hold growth profile constant
   - "fair IPO / takeout price?" → M&A + primary-market comparables
   - "sector sentiment?" → wide classification group (context only, never the headline multiple)
3. Select the **primary multiple** appropriate to the business (see §9 selection rules), e.g. P/E, EV/EBITDA, EV/Sales, P/B (banks/NBFCs), EV/Subscriber, GMV-based, AUM-based.
4. Emit `mandate` object.

**Output**
```
mandate = {target_isin, target_symbol, control_variable, primary_multiple, secondary_multiples[], as_of_date}
```
**Gate:** cannot proceed without a chosen `primary_multiple` justified by business model.

---

## 3. STAGE 1 — Build the candidate universe (India sources)

**Objective:** assemble a broad, source-diverse candidate pool with provenance — *before* any filtering.

**Data source registry (query in this priority; log which fired):**
- **Neutral / structural:** NSE & BSE industry classification; **AMFI/SEBI four-tier classification** (Macro-Economic Sector → Sector → Industry → Basic Industry); **NIC codes**; annual reports (MD&A, segment notes).
- **Independent aggregators:** screener.in, Trendlyne, Tickertape, Tijori; professional: Capitaline, Ace Equity, CMIE Prowess.
- **Behavioural / revealed:** sector & thematic ETF / index-fund holdings (e.g., Nifty sectoral indices constituents); daily price co-movement; M&A and PE/VC deal comparables (for private/unlisted analogs).
- **Issuer/sell-side (quarantined — see Stage 2):** RHP/DRHP "Basis for Issue Price", broker comps tables, IR decks.

**Procedure**
1. Read the target's **business description + segment notes + "Competition"/risk factors** from the latest annual report. Extract: products, revenue mechanics, end-markets, geography, customer type.
2. Derive the **value driver(s)** the multiple keys off (recurring revenue, same-store sales, ARPU, AUM, order book/backlog, transaction volume × take-rate, units × realisation × utilisation).
3. Pull candidates from **each neutral + aggregator + behavioural source**.
4. Tag every candidate with `{source, classification_codes, business_summary}`. Do **not** filter yet.

**Output:** `candidate_universe[]` with provenance. Issuer/sell-side names are tagged `source_class = "issuer_or_sellside"` and held for Stage 2.

---

## 4. STAGE 2 — RHP / sell-side bias protocol  ⚠ (critical for Indian primary market)

**Why:** In the **RHP "Basis for Issue Price"** section, merchant bankers select the comparison peer set. The selection is structurally biased toward **justifying the issue price** — convenient high-multiple names get included, obvious lower-multiple competitors get omitted. The same bias (milder) affects broker initiation comps. Treating these as ground truth imports sell-side inflation directly into the valuation.

**Rule:** issuer/sell-side peer lists may **never** seed the Core set. They are only cross-checked *against* an independently reconstructed set.

**Procedure**
1. **Reconstruct independently.** Using only neutral + aggregator + behavioural sources (Stage 1), build the independent operational set. Ignore the RHP list while doing this.
2. **Diff the two sets:**
   - `convenient_inclusions` = in RHP, absent from independent set.
   - `convenient_omissions` = obvious competitors in independent set, absent from RHP.
3. **Cherry-pick signature test:** compute median of the issuer's chosen multiple across (a) RHP peers and (b) independent peers.
   - If `median(RHP_peers) > (1 + CHERRYPICK_TOL) × median(independent_peers)` → raise `flag: upward_pricing_bias` and record the gap in bps/×.
   - Inspect `convenient_inclusions`: if they skew high-multiple, and `convenient_omissions` skew low-multiple → confirms deliberate inflation.
4. **Admission rule:** an RHP-listed name enters candidacy **only** if it is *independently corroborated* by ≥1 neutral/behavioural source. Uncorroborated RHP-only names are dropped and logged.
5. For an **IPO target itself**, do not anchor on the RHP implied multiple; derive the fair multiple from the independent Core set and report the RHP premium/discount to it.

**Output:** `bias_report = {convenient_inclusions[], convenient_omissions[], rhp_median_multiple, independent_median_multiple, bias_flag, bias_magnitude}` and a cleaned candidate pool.

---

## 5. STAGE 3 — Operational peer identification (rings + drivers)

**Objective:** from the cleaned pool, isolate genuine operational competitors by the innermost viable ring.

**Ring model (stay innermost with ≥ `MIN_PEERS` names; step outward only on scarcity, logging each step):**
- R1 direct competitors (same product, same customer) → R2 same sub-industry → R3 broader industry → R4 same business model, different industry/geography (→ cross-border analog) → R5 same financial signature only.

**Procedure**
1. Score each candidate for **operational similarity** on: value-driver match, end-market overlap, customer type, business model mechanics. Keep those above `OP_SIM_MIN`.
2. Distinguish **demand-side twins** (same customer) from **supply-side twins** (same cost/production structure, capital intensity, cyclicality). Tag each; weight toward the twin that drives the chosen multiple.
3. If `count(operational_peers) < MIN_PEERS`, step one ring outward and repeat; record `rings_traversed`.

**Output:** `operational_peers[]` with `{ring, twin_type, op_sim_score}`.
**Note:** this is **not** the valuation set yet — it must pass Stage 4.

---

## 6. STAGE 4 — Economic peer test (the quantitative gate)

**Objective:** test whether each operational peer actually trades on the same fundamentals — i.e., is an *economic* peer, not merely a competitor. Also promote qualifying **valuation analogs**.

**Feature vector (compute for target and every candidate, same `as_of_date`, same accounting basis):**
`[revenue_CAGR, EBITDA_margin, ROCE (or ROE/RoA for financials), net_leverage, reinvestment/capital_intensity, size (mcap or revenue)]`

**Procedure**
1. **Normalise** each feature (z-score or robust scaling across the candidate pool).
2. **Fundamental distance** `d_i` = weighted Euclidean/Gower distance from target. Weights emphasise the drivers of the chosen multiple (e.g., for P/E: growth + margin + ROCE + leverage).
3. **Multiple-consistency check:** compute each candidate's own `primary_multiple`. Fit the pool's central tendency (median + MAD).
4. **Classify:**
   - **Core economic peer** if operational **AND** `d_i ≤ FUND_DIST_MAX` **AND** its multiple lies within `± DISP_TOL × MAD` of pool median (or the deviation is *explained* by its position on the value driver — e.g., higher growth justifying higher P/E, verified by a monotonic growth↔multiple relationship).
   - **Operational-only peer** if operational but `d_i > FUND_DIST_MAX` (competitive context only; excluded from the multiple).
   - **Valuation analog** if **not** operational but value-driver-matched AND `d_i ≤ FUND_DIST_MAX`; carry a required adjustment (sector/market).
5. **Explain divergence, don't just exclude.** For every operational-only demotion, log *which* feature broke similarity (e.g., "40% CAGR vs target 12% → different multiple regime"). This is itself an analytical finding.

**Output:** each candidate labelled with bucket (§1), `fund_distance`, own `multiple`, and `divergence_reason` if demoted.

---

## 7. STAGE 5 — India-specific adjustments & red flags

**Objective:** correct for structural features of Indian markets that distort comparability.

**Per-candidate screens (flag or exclude):**
- **Promoter pledge** high/rising → governance/overhang flag.
- **Free float / liquidity:** very low free float, or presence on **ASM/GSM surveillance lists** → multiples unreliable; demote from Core or widen caveat.
- **Related-party transactions** material relative to revenue → earnings-quality flag.
- **SME-platform vs mainboard:** do not mix SME-board liquidity/valuation regimes with mainboard without adjustment.
- **Standalone vs consolidated / segment mix:** compare like basis; for multi-segment firms use **segment-level / SOTP** comps, not consolidated.
- **Accounting:** ensure Ind-AS consistency; normalise one-offs, ESOP, exceptional items.

**Scarcity handling (common in India — many sectors have 1–2 listed players):**
- Use **unlisted comps** via PE/VC & M&A deal multiples.
- Use **cross-border analogs** (R4): take the foreign peer as evidence of *business economics* (achievable margins/growth of the model), then apply an **India valuation lens** — adjust for India's higher cost of capital/risk-free rate, structural growth premium, governance/disclosure and liquidity differences, currency, tax. Never lift a foreign multiple wholesale.

**Output:** adjusted set with `india_flags[]` and any `cross_border_adjustment` notes.

---

## 8. STAGE 6 — Dispersion & validation (quantitative)

**Procedure**
1. Final Core set size should be in `[MIN_PEERS, MAX_PEERS]`.
2. Compute multiple dispersion: `coefficient_of_variation` and IQR.
   - `CV ≤ DISP_OK` → coherent; proceed.
   - `CV > DISP_OK` → set too loose or outlier present.
3. **Outliers:** for each name beyond `OUTLIER_Z`, investigate the driver before acting; decide `exclude / adjust / keep-with-footnote` and log the reason. A real outlier may indicate the market disputes the grouping — record that as a finding, don't silently drop.
4. Recompute until coherent or escalate `analyst_review_required`.

**Output:** `validated_core_set[]`, dispersion stats, outlier decisions.

---

## 9. Multiple-selection rules (reference)

- Positive, stable earnings, non-financial → **P/E**, **EV/EBITDA**.
- Capital-light / high-growth / pre-profit → **EV/Sales** (+ growth-adjusted).
- Banks / NBFCs / insurers → **P/B**, **P/ABV**, **P/EV** (life insurers); never EV/EBITDA.
- Real estate / infra / cyclicals → **P/B**, **EV/EBITDA**, asset-based.
- Platforms / telecom / subscription → **EV/Subscriber, EV/GMV, EV/Sales**, cohort/unit economics.
- Commodities → mid-cycle / normalised multiples, not spot-peak.

---

## 10. STAGE 7 — Output assembly (structured)

```json
{
  "mandate": { "target_isin": "", "control_variable": "", "primary_multiple": "", "as_of_date": "" },
  "bias_report": {
    "rhp_median_multiple": null, "independent_median_multiple": null,
    "bias_flag": false, "bias_magnitude": null,
    "convenient_inclusions": [], "convenient_omissions": []
  },
  "peers": [
    {
      "symbol": "", "isin": "", "bucket": "core_economic|operational_only|valuation_analog",
      "ring": 1, "twin_type": "demand|supply",
      "op_sim_score": 0.0, "fund_distance": 0.0, "own_multiple": 0.0,
      "india_flags": [], "cross_border_adjustment": null,
      "divergence_reason": null, "sources": [], "confidence": 0.0
    }
  ],
  "valuation_set": ["<core_economic + adjusted valuation_analogs only>"],
  "context_set": ["<operational_only, for competitive read>"],
  "dispersion": { "cv": 0.0, "iqr": 0.0, "outlier_decisions": [] },
  "set_confidence": 0.0,
  "analyst_review_required": [],
  "audit_log": ["rule fired → value → decision, per candidate"]
}
```

**Documentation requirements (auto-generated):** one line per inclusion (why), per exclusion (why), per ring stepped beyond R2 (why + adjustment), per RHP flag, and the weakest links in the Core set.

---

## 11. Parameters (single tuning surface — expose these as config)

| Param | Meaning | Suggested default |
|---|---|---|
| `MIN_PEERS` / `MAX_PEERS` | Core set size bounds | 5 / 12 |
| `OP_SIM_MIN` | Min operational-similarity score to be a competitor | 0.6 |
| `FUND_DIST_MAX` | Max normalised fundamental distance for economic peer | 1.0 (≈1 SD) |
| `DISP_TOL` | Allowed multiple deviation from pool median (× MAD) | 1.5 |
| `DISP_OK` | Max coefficient of variation for a coherent set | 0.35 |
| `OUTLIER_Z` | Z-score beyond which a name is an outlier | 2.0 |
| `CHERRYPICK_TOL` | RHP-vs-independent median gap that triggers bias flag | 0.15 (15%) |
| `SIZE_BAND` | Acceptable market-cap/revenue multiple vs target | [0.25×, 4×] |
| `STALENESS_MAX` | Max age of financial data before `data_gap` | 2 quarters |

*Defaults are starting points, not law — tune per sector and backtest.*

---

## 12. Execution summary (the loop, in one line)

> **Resolve the mandate → build a source-diverse universe → quarantine & falsify RHP/sell-side lists → isolate operational competitors by innermost ring → gate them through the economic-peer test (operational ≠ economic) → apply India structural adjustments and cross-border/unlisted analogs where listed comps are scarce → validate by dispersion → emit a structured, provenance-logged set where only Core economic peers (plus adjusted analogs) touch the multiple.**