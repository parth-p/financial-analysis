# IPO Analysis — Analyst's Checklist

*Adapted from the 8-step equity framework (Business Model → Thesis) for Indian primary-market offerings (DRHP / RHP). Self-contained — you can run this end-to-end without opening the other files. It carries **every probe** from the eight equity checklists, remapped into nine deal-first sections, plus the IPO-specific probes the equity framework never had.*

> **The one rule for this whole checklist:** an IPO is a **sale by an informed insider who picked the date and set the price**. The promoter, the selling shareholders, the merchant bankers and the pre-IPO investors all know the business better than you, all chose to sell *now*, and all had a hand in the band. The offer document is a **sales exhibit wrapped around a legally-mandated confession** (the risk section). Every probe below exists to **neutralise that information-and-timing asymmetry**. Default answer to "should I apply?" is *no*; the burden of proof is on the deal.

> **Decide which game you are playing before you read a page.** Two, and they don't mix:
> - **Listing-gain flip** — a bet on demand, subscription, anchor quality and grey-market froth. Technical, short-horizon. This checklist can *inform* it but isn't built for it.
> - **Long-term ownership** — a bet on the business and the price. What the checklist is built for. Test: *would you buy this on the open market at the band price the week after listing?* If not, the "opportunity" isn't one.

### The flag convention

Notice something a later section owns? Write the fact, tag the section, move on: `Fact → §N`. Flags **collect once in §8 (Risks) and the Verdict** — never re-explained in every section they touch.
- ✅ `90% of revenue from one client → §8 (risk), §6 (valuation cap)`
- ✅ `Fresh issue mostly repays a promoter-group loan → §4 (character), §5 (forward maths)`

**Who owns which judgment:** the transaction → §1 · what the business *is* → §2 · pond + durability → §3 · the people/cleanup → §4 · whether the numbers are real → §5 · worth vs. the ask → §6 · whether it clears + trades → §7 · what causes permanent loss → §8 · flip/own/wait/pass → §9.

**A note on SEBI specifics:** allocation buckets, anchor lock-in, promoter lock-in, monitoring thresholds are set by SEBI ICDR and change often. Every rule-bound number here is tagged *(verify in RHP / current ICDR)*. Take it from the offer document, not memory — including this checklist's.

---

## The output — structure & house rules

> **This checklist is a collection tool; the finished analysis is a decision document. Gather in any order — present in the order below, answer first. The goal is compression of *form*, not loss of *information*: every probe below must be answered, but each in 1–3 lines, not paragraphs.**

1. **Answer every probe — drop none.** Each `- [ ]` line below gets addressed in the output, even if the answer is "not disclosed" or "n/a for this sector" (a gap is itself a finding). Coverage is non-negotiable; length is controlled by *shortening answers*, never by *cutting questions*.
2. **1–3 lines per probe.** Render each as a **bold lead-in** + terse answer + inline cite. Example:
   `- **Job-to-be-done:** eliminate line-halt risk — the customer buys zero-defect torque, not the shaft. [confirmed p.301]`
3. **Verdict first.** The document opens with the **Verdict Box** (template at the end): call (Apply-own / Apply-flip / Wait / Pass) + 4–6 load-bearing reasons + the price/condition that flips the call + size. Derived last, placed first.
4. **Key Facts once.** A table under the Verdict Box (issue size, fresh/OFS, band + m-cap, normalized earnings, net debt/leverage, top-client concentration, biggest anomaly, eligibility route, nearest lock-in). Everything downstream **references** it; nothing re-derives it. The one-off gain / RPT / leverage get one full explanation, not seven.
5. **Terse status labels.** Confirmed facts carry an inline `[confirmed p.X]`. Deductions carry `[inferred]`; guesses `[assumed: …]`. That is the whole label — no "Status / Claim Type" blocks.
6. **Per-section verdict line.** Each section ends with its one-line verdict (templates are inside each section) — the crisp conclusion that makes the analysis a worked judgment, not notes.
7. **One ranked risk section — no per-section red-flag boxes.** Flags collect in §8, which ranks: **top 3 permanent-loss risks** (probability · severity · permanence · tripwire), everything else **one line**. Reserve "kill/existential" for things that actually kill the thesis; a ₹1 cr tax notice and 4× leverage must not read at the same volume.
8. **Deal-first order:** Verdict → Key Facts → §1 Deal → §2 Business → §3 Industry & Moat → §4 Management → §5 Financials → §6 Valuation → §7 Demand & Mechanics → §8 Risks → §9 Decision. Collection guidance (below) is analyst prep, not deliverable content.
9. **Measured tone.** Analyst, not prosecutor. State the fact and its magnitude; let it carry the weight.

---

## Before you start — sourcing & read-map *(analyst prep — not part of the deliverable)*

- Get the doc from the company's **Investor Relations** page, **SEBI**, or an aggregator's "Docs" section (e.g. Chittorgarh). Confirm latest version. Use `fetch_rhp.py` to pull + text-convert.
- **Read the RHP, not the DRHP** (RHP ≈ a week before open: updated financials, final issue size, final capital structure — saves 50–60%).
- Skip boilerplate; read in order of leverage: **Our Business · Objects of the Offer · Financial Information (Restated) · Basis for Issue Price · Capital Structure · Risk Factors** (Section 2), plus **Promoter & Management** and the **Industry Overview** (CRISIL/CareEdge/independent report).
- Supplement: IPO name + "management interview" (CNBC-TV18, NDTV Profit). Treat as management *claim* (weigh in §4), not fact.
- Named examples in this checklist are **illustrative patterns, not verified data** — recognise the shape, don't trust the number.

---

## §1. The Deal — *what's being sold, by whom, why now, and where the money goes*

**Fresh issue vs. OFS**
- [ ] Fresh Issue vs. Offer for Sale — split in ₹ and %. Fresh = new shares, cash to company (dilutive); OFS = existing holders sell, cash to them.
- [ ] Economic OFS vs. headline — is a "fresh issue" whose proceeds buy promoter-connected assets an OFS in disguise? Compute the true insider-cash-out %.
- [ ] Dilution — new shares vs. pre-issue base; % dilution of existing equity.

**Who's selling, and why now**
- [ ] Who sells in the OFS, and how much of *their own* stake? (a float-rule slice vs. a promoter shedding a large fraction — different signals.)
- [ ] WACA of the selling shareholders — the multiple they book at the band vs. their cost.
- [ ] Why now? growth capital · PE fund end-of-life (calendar-forced) · peak sentiment / hot window · cash need / debt distress. Name it.
- [ ] Prior withdrawn/deferred filings, recent secondary sales or pre-IPO placements at what price — a private mark vs. the public ask.

**Use of proceeds (grade each rupee of the fresh issue)**
- [ ] Capex/expansion (value-building) · working capital (why is the cycle long? → §5) · debt repayment (→ §5 forward maths) · R&D · GCP (SEBI-capped; flag a large slice).
- [ ] Related-party payments in the proceeds — money to buy assets from / repay loans to promoter entities. Record ₹ and % here once; *character* → §4, *risk* → §8. **Independently appraised, by whom?** An unappraised RPT buyout is a flag.
- [ ] Is the raise sized to a real need, or to a valuation window?
- [ ] Monitoring agency appointed (Reg 41 threshold — verify) and its remit.

**What the promoter keeps**
- [ ] Promoter holding pre vs. post issue; retained control %.
- [ ] Encumbrance — any promoter shares pledged / under NDU, and post-listing re-encumbrance risk. → §4 / §8.
- [ ] Lock-in: minimum promoters' contribution % and period; balance promoter + non-promoter lock-in *(verify current ICDR)*. → §7.

**Structure**
- [ ] Eligibility route — profitable **Reg 6(1)** vs. **Reg 6(2)** (fails NTA/profit test → ≥75% to QIB, deal aborts if QIB short). *(verify split.)* → §7.
- [ ] Mainboard vs. SME — SME = lighter disclosure, thin float, manipulated GMP; raise the bar and treat the RHP as mandatory.

**Watch for (→ §8):** promoter + PE + employees all exiting at once; OFS-dominated raise; proceeds funding losses or repaying promoter loans; a "need" that appears only because the multiple is rich.

> **Deal verdict:** fresh ___% / OFS ___% (economic OFS ___%); primary seller ______; why now **[growth / fund-exit / peak-window / cash need]**; proceeds **[build value / neutral / extract]**.

---

## §2. Business Model — *how it makes money* (describe the machine; don't judge it yet)

**Unit of value**
- [ ] Atomic transaction — one customer, one purchase: what changed hands and why.
- [ ] What the product/service actually is + concrete use cases (full, specific description lives here).
- [ ] Job-to-be-done — what the customer hires it for (the hole, not the drill).
- [ ] Criticality — mission-critical (line halts/batch ruined) ↔ nice-to-have (record the fact; switching-cost judgment → §3).
- [ ] Which end-user industry buys it (fact; attractiveness → §3).
- [ ] What the company *sells* vs. what the customer *buys* — same thing?
- [ ] Real competition for that job (often a different product — status-quo manual process, in-house make-vs-buy).

**Revenue model & quality**
- [ ] Recurring (contractual) / repeating (habitual) / one-time (re-won each sale)?
- [ ] Usage-based or fixed? Does the relationship deepen or reset to zero?
- [ ] On day 1 of the year, how much revenue is already "in hand" (order book/contracts) vs. must be won again?
- [ ] Place it on the quality hierarchy: recurring > repeating > one-time.

**Customer & concentration**
- [ ] Segment the customers; who's the *marginal* (next) customer; is that pool easier or harder to reach?
- [ ] Concentration on every axis — customer / product / geography / channel (top-1, top-5, top-10 %). → §8 if any >20–30%.
- [ ] Is the payer the same as the user? (CFO vs. plant manager vs. the downstream OEM auditor.)

**Cost structure & unit economics**
- [ ] Fixed vs. variable cost split (drives operating leverage + downturn cyclicality).
- [ ] The model's *native* unit metric — LTV:CAC + payback (subscription) / per-store or per-sq-ft (retail) / take rate (marketplace) / per-tonne, per-bed, etc.
- [ ] CAC and payback — cost to acquire one customer, time to earn it back.

**Scalability**
- [ ] Cost of the *next* unit as it grows — near-zero (software) or linear (locations/headcount)?
- [ ] To double revenue, what must double? Compounds vs. just gets bigger.

**Capital intensity & cash cycle**
- [ ] Asset-light or asset-heavy — capital sunk per rupee of revenue.
- [ ] Cash conversion cycle — paid *before* or *after* it pays its own costs?
- [ ] The big one: does growth *consume* cash or *throw it off*? (Look for the negative-working-capital / float gem.)

**Value-chain position & power**
- [ ] Where it sits input → end customer; does itself vs. outsources.
- [ ] Dependencies — single supplier / platform landlord / single distributor.
- [ ] Who can compress its margins without retaliation?

**Growth mechanics**
- [ ] Which levers — more customers / revenue per customer / new products / new geographies.
- [ ] Name the specific lever + its economics and durability.
- [ ] Strip out M&A and price hikes — is the underlying (same customers, same products) business growing?

**Watch for (→ §8):** revenue not traceable to a paying customer; only works at unreached scale; uncontrolled platform dependence; a "solution provider" that's a low-margin trader in jargon.

> **Business verdict (two-sentence test):** ______________ / ______________. If you can't state it in two plain sentences, you don't understand it — stop.

---

## §3. Industry & Moat — *is the pond good, and will the returns last?*

### Industry — judge the average player, not the company
- [ ] Define the industry by the *job* + set of players (not the product label); market it serves vs. market that constrains it; test — if the company vanished, where do customers go?
- [ ] Lifecycle & growth — S-curve position; how fast the *industry* grows.
- [ ] Cyclicality — demand secular or cyclical, and where in the cycle now; what drives industry demand (GDP/rates/commodity/scheme). (Trap: growth ≠ profitability.)
- [ ] Five forces at industry level — rivalry · new entrants · substitutes · buyer power (govt L1 tendering is the extreme) · supplier power; **name the one binding force**.
- [ ] Structure & rationality — fragmented vs. consolidated + trajectory; price discipline vs. race to the bottom; when demand softens, cut price or hold?
- [ ] Profit pools — map the vertical chain; where profit *accumulates* (revenue pool vs. profit pool); which slice the company sits in.
- [ ] Key success factors — what determines winners (scale/tech/distribution/relationships/cost/brand); hardest thing to replicate = raw material of the moat.
- [ ] Regulation & policy — created / governed / threatened by the state; durability of the policy.
- [ ] Structural trajectory & disruption — disruption vectors; are barriers/profit pools stronger or weaker over ~5 years?

> **Industry verdict:** **[structurally attractive / mediocre / value-destroying]**, binding reason ______.

### Moat — company-specific durability of *excess* returns (numbers before narrative)
- [ ] Evidence — ROIC persistently > cost of capital and stable (through a downturn); pricing power (passed inflation, held margin); durable/rising share, esp. in downturns; gross margin stable & above peers. (Short public record = weaker evidence, not proof.)
- [ ] Source — name which of five: switching costs · network effects · intangibles (brand/patents/licences/approvals — brand counts only if it moves WTP or churn) · structural cost advantage · efficient scale. Stacked?
- [ ] Width — how much of the business the moat shields.
- [ ] Depth — size of the edge, quantified (margin points, price premium, months of switching pain, share).
- [ ] Direction — **widening / stable / eroding** over ~5 years (the whole ballgame; shrinking moat + great filing-year numbers = value trap).
- [ ] Durability & replicability — half-life of the source; what money/years for a well-capitalised rival to replicate, and *why haven't they?*
- [ ] Reinvestment runway — reinvestment moat (redeploy at high ROIC) vs. static fortress; growth *inside* the moat vs. outside.
- [ ] Rule out imposters — execution/management (→ §4) · sheer size · fast growth · cyclical/one-off peak masquerading as a moat.

> **Moat verdict:** **[none / narrow / wide]**, sourced from ______, currently **[widening / stable / eroding]**, durable ~______, because ______.

---

## §4. Management & Governance — *the people, and the pre-IPO cleanup* (behavior over words)

**Capital allocation track record (the heart)**
- [ ] Reinvestment — organic capex/R&D above cost of capital?
- [ ] M&A — prices, integration, earned its cost of capital? (base rate: most M&A destroys value; a debt-fuelled roll-up is engineering, not compounding.)
- [ ] Buybacks — cheap/accretive vs. at peaks / offsetting SBC; real net share reduction?
- [ ] Dividends — appropriate given the reinvestment opportunity set?
- [ ] Debt — sensible given the balance sheet and cost of debt?
- [ ] Meta-tell — counter-cyclical (good) vs. pro-cyclical (bad). Where did *every* rupee go over 5–10 yrs?

**Incentives**
- [ ] Paid on what — EPS / size / share price (gameable) vs. ROIC / per-share value / multi-year TSR (aligned)?
- [ ] Targets stretching or sandbagged; vesting/time horizon.

**Ownership & skin in the game**
- [ ] Meaningful ownership relative to net worth; **bought vs. granted**.
- [ ] Founder/promoter-led (long-term positive; key-person/promoter-governance risk); insider buy/sell pattern.

**Operating competence & candor**
- [ ] Execution vs. peers; the say-do ratio (3–5-yr-old guidance vs. actuals); handling adversity — candor or spin.
- [ ] Accounting character — honest incl. bad news; substance vs. promotional fluff; non-GAAP stripping real recurring costs / aggressive revenue recognition (deep math → §5).

**Governance & the pre-IPO cleanup (scrutinise hardest)**
- [ ] Board independence/quality; dual-class or control structures.
- [ ] **Promoter pledging**; related-party transactions / tunnelling (reference §1's figure, judge character here).
- [ ] Auditor quality; any **resignation/qualification** (a klaxon).
- [ ] Shareholder-hostile history (dilution, sweetheart deals); integrity/legal overhang (litigation, regulatory action, FIRs — including anything buried deep in the risk section → §8).
- [ ] Pre-IPO / preferential allotment prices — recent private marks to sanity-check the band (→ §6).
- [ ] Executive/board churn — CFO, Company Secretary, independent-director resignations right before filing (an IPO-specific tell).

**Skill vs. tailwind**
- [ ] Rule out that results came from a great industry (§3) / moat / cyclical tailwind / predecessor. Which outcomes trace to *discretionary decisions* (capital allocation is cleanest)?
- [ ] PE/institutional holders — exiting or staying? (Staying = confidence, unless paired with cash extraction elsewhere in §1.)

> **Management verdict:** operators **[strong/adequate/weak]** ; capital allocators **[strong/adequate/weak]** ; incentives & ownership **[aligned/mixed/misaligned]** — each backed by a specific decision, not a vibe.

---

## §5. Financials & Forensics — *is the reported profit real?* (the courtroom: test §2–§4 against the ledger)

**Read as one system**
- [ ] Set the sector mindset first (what "normal" margin and cash cycle look like).
- [ ] Trace income statement → balance sheet → cash flow as one machine; 3-yr+ run (not a snapshot); common-size (% of revenue/assets); always vs. peers + own history. Read the Restated Consolidated Summary (auditor → P&L → BS → CFS → Notes).

**Earnings quality (the central test)**
- [ ] Net income vs. operating cash flow over years (persistent NI > OCF = red flag); FCF = OCF − capex; conversion ratio; accruals level.
- [ ] Don't be sold by the top line — interrogate **Exceptional Items** and **Other Income** (where one-offs hide when loosely business-related). Strip them → normalized core earnings.
- [ ] Was the gain **manufactured** — a core revenue-producing asset sold right before the IPO to book an exceptional gain? Note the recurring revenue given up.
- [ ] Abnormal **Other Expenses** jump → find its note number → **Notes to Accounts** (below the CFS) → it bifurcates the line (2–3-min drill).

**Returns, margins, growth**
- [ ] ROIC vs. WACC over many years (stability = moat evidence); DuPont ROE (margin × turnover × leverage — margin-driven ≠ leverage-driven fragility); incremental ROIC.
- [ ] Gross/operating/net margins — levels and trends vs. peers/history; operating leverage; margin trajectory and *why*.
- [ ] Decompose growth — volume vs. price vs. acquisitions vs. FX (organic vs. inorganic); profitable vs. bought; throws off or consumes cash.
- [ ] Standalone vs. proforma — if acquisitions were injected pre-listing, separate them; proforma combines entities not historically together (a construction, not a track record).

**Balance sheet, working capital, drivers**
- [ ] Solvency — net debt/EBITDA, D/E, interest coverage; maturity profile, fixed/floating, refi risk; liquidity (current/quick, cash); off-balance-sheet & contingent (leases/guarantees/pledges/pension/litigation); goodwill & intangibles % of assets. (*Fact* of leverage here; thesis-breaking severity → §8.)
- [ ] Working capital / cash cycle — CCC = receivable + inventory − payable days; the *trend* in each matters more than the level (rising receivables = channel stuffing / non-payment; building inventory = softening demand). A receivables spike right before the IPO is a manufactured-revenue tell (distinguish from a genuinely long export cycle).
- [ ] Key drivers — build the driver tree (operational primitives); isolate the **2–3** that dominate; sensitivity / swing factor. → §6.
- [ ] Debt repayment → forward profit → forward multiple — find the finance-cost rate; repaying high-rate debt lifts next-year post-tax profit, which the market prices now. Re-run §6 on normalized *forward* earnings.

**Forensic red flags**
- [ ] NI up while cash stalls · revenue up while receivables rise faster / rising DSO · recurring "one-time" charges · widening GAAP-vs-adjusted gap · capitalised costs that should be expensed / changed estimates / auditor changes · related-party revenue · screens (Altman Z, Beneish M).
- [ ] MD&A cross-check — management's own explanation of *why* numbers moved, vs. what the statements show.

> **Financials verdict:** numbers **[confirm/contradict]** the §2–§4 story, key divergence ______; 2–3 drivers ______; earnings **[do/don't]** convert to cash (≈__), ROIC **[does/doesn't]** clear WACC (__ vs __).

---

## §6. Valuation — *the band is the seller's ask, not the market's verdict*

- [ ] Precondition — from §2–§5, can you state roughly what it earns and *why*? If not, **stop**.
- [ ] Normalize earnings — through-cycle sustainable power; strip one-offs (§5); prefer owner earnings (NI + D&A − maint capex ± WC); value on **forward normalized** profit where debt is repaid; watch the cyclical trap (trough looks dear, peak looks cheap).
- [ ] "Basis for Issue Price" is largely useless as a valuation (band not set at DRHP stage) — mine it for the **peer list + qualitative factors**, and find the *true* peers yourself if the RHP flatters or claims "no listed peer."
- [ ] Reverse the band — what growth / margin / return-on-capital / duration does the implied m-cap require? Judge vs. §2–§5: conservative, reasonable, or heroic? What has to go right, how likely?
- [ ] Intrinsic value as a range — bear / base / bull, probability-weighted; terminal value = where the moat feeds in (competitive-advantage period; §3 direction sets the fade); sensitivity on the §5 key drivers.
- [ ] Right multiple for the sector — EV/EBIT across capital structures · P/B for financials · EV/Sales for pre-profit · P/E, P/FCF, EV/EBITDA · plus operating metric (ARPU / ARPB / occupancy / take rate / per-tonne). Use EV to compare across balance sheets.
- [ ] Compare like with like (the TTM trap) — peer screens default to TTM; on a fiscal-year number, recompute peer = `current m-cap ÷ same-period profit`.
- [ ] Private-mark cross-check — the last pre-IPO transaction price (promoter buy, latest placement/conversion, NAV) vs. the band. Why sell higher to the public than to insiders?
- [ ] NAV / tangible-book — for asset-heavy/financials; strip goodwill & intangibles created by RPT acquisitions (§1) — tangible book can be well below stated NAV.
- [ ] Triangulate & sanity-check — do methods converge; reality tests (what share/margin does the price imply — has anyone in the industry achieved it?); reverse stress test (obviously cheap/expensive at what price?); recent sector-IPO post-listing behaviour; sum-of-the-parts if multi-segment.
- [ ] Margin of safety — discount to the value *range*, scaled inversely to quality/predictability, and **wider for an IPO** (the seller has the information + timing edge). A great company at an absurd price is a bad investment.

> **Valuation verdict:** the band implies **[conservative/reasonable/heroic]** expectations; vs. peers **[cheap/fair/rich]**; margin of safety **[adequate/thin/none]** for an IPO's asymmetry.

---

## §7. Demand & Mechanics — *who clears the book, and when the float cliff hits* (IPO-only)

- [ ] Subscription by category — QIB / NII / Retail buckets + oversubscription in each; **QIB demand is the informed-money read** *(allocation split differs for Reg 6(1) vs 6(2); under 6(2) the deal aborts if QIB doesn't clear — verify)*.
- [ ] Anchor book — who anchored, at what price, and **quality** (long-only institutions/MFs > known flippers; FPI vs. domestic); anchor lock-in split *(verify periods)*.
- [ ] Grey Market Premium — sentiment only, not fundamental; unofficial, manipulable, vanishes for SME. Never apply on GMP alone.
- [ ] Lock-in expiry calendar — anchor (short + long tranche), non-promoter, promoter excess, minimum promoters' contribution; map each release as a supply cliff *(verify periods)*. A 1-year cliff releasing a majority of shares is the big one.
- [ ] Free float post-listing — Day-1 tradeable % (thin float = volatile, easy to move; acute for SME/micro-cap).
- [ ] Greenshoe / stabilisation — over-allotment mechanism and window, or its absence (no price support).

> **Mechanics verdict:** QIB/anchor quality **[strong/mixed/weak]**; nearest lock-in cliff ______; Day-1 float **[deep/thin]**.

---

## §8. Risks — *ranked: what actually causes permanent loss*

- [ ] **Reframe (the gate):** two questions govern — how likely am I wrong, how much do I lose *permanently* if so? Exclude volatility-that-recovers. Every entry must be *observable* if it starts happening.
- [ ] **Read the top 15–25 risk factors in detail, then skim the headline of *every* remaining one** — killers get buried deep (a regulatory ban on a promoter-group entity, a killer concentration) where they hope you stop reading.
- [ ] **Sweep the taxonomy (collect every `→ §8` flag):** competitive/disruption (§3) · financial/balance-sheet (§5 — weight heavily, the most common cause of permanent loss) · operational (key-person, single-site, supply chain, attrition spike in the prep year) · regulatory/legal/political · governance/integrity (§4) · cyclical/macro · tail/exogenous · **IPO-specific** (lock-in overhang, promoter dilution, proceeds misuse, thin-float volatility, unproven-as-public-company, reversal of pre-IPO window-dressing).
- [ ] **Thesis risks (the neglected half):** list the load-bearing assumptions from §2–§6; for each, what would prove it wrong; the priced-in filter (what the market already worries about vs. what your thesis *uniquely* depends on); interrogate your variant perception hardest.
- [ ] **Pre-mortem:** it's 3–5 yrs out and you lost money — write the story; what early signal would have warned you.
- [ ] **Correlation & single points of failure:** independent or correlated (a downturn hits demand + financing + counterparty at once)? A single dependency (one client, one state) that appears as revenue + cash-flow + covenant risk counts once but hits everywhere — rank it as one big risk, not three small.
- [ ] **Permanence & magnitude (master cut):** permanent impairment vs. temporary noise; weight probability × severity; separate existential from drawdown.
- [ ] **Kill criteria — make it monitorable:** convert the top risks into observable tripwires (rising DSO, share loss, covenant breach, competitor launch, regulatory filing), defined *in advance*.

**Output (rank, don't list):**
> **Top 3 permanent-loss risks:** 1. ______ — prob [ ], severity [ ], **[permanent/temporary]**, tripwire ______. 2. … 3. …
> **Everything else:** one line each.
> **Pre-mortem — most likely way this fails:** ______. **Implication for margin of safety / size:** ______.

*Do not tag five things "severe." A long undifferentiated list is risk theater — rank it.*

---

## §9. The Decision — *flip, own, wait, or pass* (the thesis + the two IPO games)

- [ ] **State the differentiated view** — in 1–2 sentences: what you believe, how it differs from the band/consensus, why you're right ("*market believes X; I believe Y; §2–§5 say I'm right; §6 says that's worth [gap]*"). If it matches consensus, there's no ownership opportunity — go to the pass test.
- [ ] **Name the edge** — informational / analytical / behavioral (hold through discomfort — the most durable); why the mispricing persists (small/boring/controversial/forced selling/complexity). Can't name it → pass / index.
- [ ] **Which game?** **Flip** — driven by §7 (subscription, anchor quality, GMP): a technical bet; if you play it, size small and pre-commit to exit on/near listing. **Own** — driven by §2–§6; the ownership test: *would you buy this on the open market at the band price the week after listing?*
- [ ] **Catalyst** (for the ownership case) — operational / corporate action / external / re-rating; hard (dated) vs. soft; cheap+great lets time be the catalyst, cheap+mediocre needs an external one or it's a value trap.
- [ ] **Time horizon & IRR** — state it; match to your capital; being right too slowly is a mediocre return.
- [ ] **Wait** — often best: let hype fade and a lock-in cliff (§7) hit, then buy the same asset cheaper with a real trading history. The seller's timing edge decays once public.
- [ ] **Pass — the honest default.** Most IPOs underperform; the seller chose the date and price. In a hot market the task is to avoid the bad ones; passing is free.
- [ ] **Sell discipline (both exits, pre-committed):** thesis-achieved (band/target reached, re-rated, better opportunity) vs. thesis-broken (§8 kill criteria). "Price fell" ≠ sell if thesis intact.
- [ ] **Position sizing** — edge × margin of safety (§6) ÷ risk & permanence (§8). Up with a nameable edge + wide margin; down with a fat left tail, thin float, or a sentiment-only case.
- [ ] **Write it down before you apply** — thesis, game, the price you'd stop being a buyer, and the exit (flip target or §8 tripwires).

> **Decision verdict:** **[Apply to own / Apply to flip (exit on listing) / Wait and buy post-listing / Pass]**, because ______. If flip: size ______, exit ______. — OR — **Pass:** ______ (no edge / fairly priced / outside competence).

---

## Traps specific to IPOs (re-read before you finish)

- [ ] **Dropping probes to save length** — the failure this rewrite exists to prevent. Compress the *answer*, never cut the *question*.
- [ ] **GMP investing** — a coin toss that leaves no conviction to hold.
- [ ] **The filing-year mirage** — a one-off-flattered, receivables-pumped best-ever year treated as the run-rate.
- [ ] **Trailing-multiple laziness** — IPO period earnings vs. peers' TTM multiples; the RHP's cherry-picked peer set.
- [ ] **Ignoring OFS vs. fresh** — cheering a raise that's mostly insiders cashing out, including via RPT asset drop-ins dressed as "fresh issue."
- [ ] **Jargon acceptance** — decode the business to what it actually does.
- [ ] **Stopping at risk #15** — missing the buried bomb at #60+.
- [ ] **Bull-market extrapolation** — "7 of 10 IPOs work" is a regime, not a law.
- [ ] **Severity inflation** — everything a klaxon until nothing is. Rank.
- [ ] **Blurring flip and own** — the single most common way IPO money is lost.

---

## The Verdict Box — *fill last, present first*

> **Call: [Apply to own / Apply to flip (exit on listing) / Wait / Pass]** — because ______ (4–6 load-bearing reasons, most decisive first).
> **The call flips if:** ______ (the price or condition that changes your answer).
> **Position size:** ______; **exit / kill trigger:** ______.

**Key Facts** *(state once; everything references these):*

| | |
|---|---|
| Issue size / type | ₹______ · Fresh ___% / OFS ___% (economic OFS incl. RPT: ___%) |
| Price band / implied m-cap | ₹______ · ₹______ |
| Normalized (fwd) earnings | ₹______ (vs. reported ₹______; anomaly: ______) |
| Net debt / leverage | ₹______ · ___× D/E · ___× net debt/EBITDA · ___× interest coverage |
| Customer concentration | top-1 ___% · top-5 ___% · top-10 ___% |
| Biggest accounting anomaly | ______ (p.___) |
| Eligibility route | [Reg 6(1) / 6(2)] · QIB ___% |
| Nearest lock-in cliff | ______ (release of ___% of shares) |

*If you can't fill a row or answer a probe, you haven't done the section that owns it — go back. If the honest answer is "Pass," that is a complete and successful analysis.*

---

*The 8-step framework judges a business you can buy at a market price. An IPO judges a business someone chose to sell you, on their date, at their price. Everything above is one discipline: **find out what the seller knows that you don't — and refuse to pay for the difference.***
