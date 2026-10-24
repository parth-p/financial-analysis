# Indian Stock Market Digest: Agent Protocol

**What this does:** Produces a disciplined, high-signal intelligence report on Indian equities and macroeconomic developments. Operates in two modes:
1. **Daily Pre-Market Delta:** Strictly captures developments from the preceding 24 hours (market close, evening corporate filings, overnight global moves, pre-market cues).
2. **Weekly Synthesis:** Evaluates the preceding 7 days, tabulates cumulative flows and sectoral performance, extracts structural themes, and maps the week ahead.

**Scope:** Indian listed equities (NSE / BSE), Indian macroeconomic indicators, RBI policy & circulars, government regulations, and cross-asset global transmission.

**The Core Invariant:** Every edition is a **delta, not a snapshot**. Zero recaps of previously reported news. Sections with nothing new or falling below materiality thresholds are **omitted completely** — no empty headings, no placeholder text, and no "nothing to report" filler.

---

## 1. Input & Parameters

- **Mode:** `daily` (default) | `weekly`
- **As-of Date:** `YYYY-MM-DD` (defaults to current date in IST)
- **Output Routing:**
  - Daily: `tmp/general/market-digest/YYYY-MM-DD.md`
  - Weekly: `tmp/general/market-digest/weekly-YYYY-WXX.md`

---

## 2. Operating Principles & Materiality Thresholds

### 2a. Operational Principles

1. **Delta-Only (Zero Recaps):**
   - Each daily edition captures only what occurred in the preceding 24 hours.
   - If an event was reported yesterday (e.g., RBI rate decision, US inflation print), do not repeat it today unless a distinct follow-up action or circular was issued.
   - Never write narrative recaps (e.g., *"Markets continued to feel pressure from last week's geopolitical events"*). If there is no new event, omit the section.
2. **Dynamic Omission (Silence is Signal):**
   - If a section has no events exceeding the thresholds below, drop the section heading entirely.
   - A 100-word daily digest on a quiet trading day indicates the filter is functioning correctly.
3. **Evidence-First with Units:**
   - Every financial number, percentage move, and deal value must be verified in the search results of the current run.
   - Always state explicit units: ₹ Crore (`₹X cr`), basis points (`bp`), percentage (`%`), or US Dollars (`$`).
   - Earnings updates must include both revenue and net profit/margin, plus forward guidance or management commentary where disclosed.
4. **Factual & Non-Advisory:**
   - Report actions, filings, and numbers neutrally.
   - Never classify stocks as "buys", "sells", or "top picks".
   - Avoid emotional adjectives ("stellar", "bloodbath", "skyrocketed"). Use exact figures ("gained 3.4%", "fell 5.1%").

### 2b. Materiality Matrix

| Stream / Section | Inclusion Threshold | Omission Condition |
|---|---|---|
| **Market Snapshot** | Always included on trading days. Format: single compact line with Nifty, Bank Nifty, Advance:Decline ratio, and net FII/DII cash flows. | On exchange holidays or weekends, state: `Market Closed: [Reason]`. |
| **Global Cues** | Any of the following overnight moves:<br>• S&P 500 / Nasdaq > ±1.5%<br>• Brent Crude > ±3.0%<br>• US 10-Yr Treasury yield > ±10 bps<br>• USD/INR > ±0.5%<br>• US Dollar Index (DXY) > ±1.0%<br>• Hang Seng / China index > ±2.0%<br>• India VIX or CBOE VIX spike > +15%<br>• Major central bank policy decision (Fed, ECB, BOJ) or geopolitical/trade shock | Omit entire section if all global moves remain within threshold bands and no macro shock occurred. |
| **RBI & Macro Data** | Official release in the last 24h of: CPI, WPI, GDP, IIP, PMI (Mfg/Services), GST collections, Trade Balance, Bank Credit growth, Forex reserves, RBI policy rate/stance, or new regulatory circulars. | Omit if no primary economic print or RBI circular was issued in the 24h window. |
| **Policy & SEBI** | Cabinet decisions, customs/duty changes, PLI updates, export/import restrictions, FTAs, or major SEBI circulars/consultation papers. | Omit routine bureaucratic gazette notices or non-actionable administrative notes. |
| **Sector Developments** | Structural developments affecting an entire sector (e.g., duty revisions, raw material price caps, regulatory mandates). | Omit single-company developments masquerading as sector news; omit speculative trade articles. |
| **IPO Tracker** | DRHP/RHP filed with SEBI, IPO opening/closing subscription milestones, or listing day price performance. | Omit if no primary market action occurred in the window. |
| **Company News** | Last 24h material corporate filings:<br>• Quarterly financial results (revenue, PAT, margin, guidance)<br>• M&A, demergers, spin-offs, joint ventures<br>• Capital raises (QIP, preferential allotment, rights issue)<br>• Promoter stake changes (>1.0%) or large insider transactions (>₹5 Cr)<br>• Key Management Personnel changes (MD, CEO, CFO)<br>• Material regulatory actions, IT raids, CBI/ED probes, SEBI show-cause orders<br>• Significant credit rating revisions<br>• Material order wins (explicitly highlighted as transformative or >10-15% of annual revenue)<br>• SEBI ASM/GSM surveillance inclusion/exclusion | Omit routine compliance filings, AGM notices, board meeting notices without outcomes, minor vendor contracts, brokerage target price changes, and generic PR statements. |
| **Earnings Today** | Notable companies scheduled to report results on `as_of_date` or next trading day. | Omit outside earnings season or on days with no major reporting companies. |

---

## 3. Daily Protocol: Search & Assembly

Execute the following search sweeps sequentially using the active date parameters (`{date_yesterday}` for previous trading session, `{date_today}` for current date).

**Minimum coverage floors (hard rules):**
- **Company News during results season** (Oct–Nov, Jan–Feb, Apr–May, Jul–Aug): minimum **15–20 items**. If initial sweeps yield fewer, run additional sector-by-sector earnings queries until the floor is met or all sectors are exhausted.
- **Company News outside results season:** minimum **5–10 items**. Corporate actions, order wins, regulatory events, and management changes should fill this even without earnings.
- **Sector / Policy / Regulatory:** If initial sweeps return zero items, run the dedicated sector and regulator sweeps in Sweep 3b and 3c below before omitting the section. A genuinely quiet day is fine — but confirm it by checking, not by running one broad query.

### Sweep 1: Market Close & Institutional Flows
- **Queries:**
  - `India stock market close FII DII flow {date_yesterday}`
  - `Nifty 50 Sensex advance decline ratio {date_yesterday}`
- **Extract:** Nifty 50 close & %, Bank Nifty close & %, NSE Advance:Decline ratio, FII net cash (₹ cr), DII net cash (₹ cr).

### Sweep 2: Overnight Global Moves & Pre-Market Signals
- **Queries:**
  - `US stock market S&P 500 Nasdaq crude oil Brent yield close {date_yesterday}`
  - `USD INR exchange rate Dollar Index DXY Asian markets Hang Seng {date_today}`
- **Test:** Compare each asset against the thresholds in §2b.
- **Extract (only if triggered):** Asset name, move (% or bps), current level, and 1-line cause.

### Sweep 3a: RBI & Macro Data Releases
- **Queries:**
  - `RBI notification circular press release {date_yesterday}`
  - `India CPI WPI inflation GDP IIP trade deficit GST release {date_yesterday}`
  - `India PMI manufacturing services {date_yesterday}`
  - `India forex reserves bank credit growth weekly RBI {date_yesterday}`
- **Extract:** Indicator name, actual print, prior/consensus comparison, and direct sector/market impact.

### Sweep 3b: Government Policy & SEBI Regulatory Actions
Run these as **separate targeted queries** — a single broad query misses most sector-specific regulatory actions.
- **Queries:**
  - `site:pib.gov.in press release {date_yesterday}` (Press Information Bureau — cabinet decisions, ministry announcements)
  - `SEBI circular consultation paper order {date_yesterday}`
  - `India customs duty tariff notification {date_yesterday}`
  - `India PLI scheme notification update {date_yesterday}`
  - `India export import restriction ban policy {date_yesterday}`
  - `India FTA trade agreement notification {date_yesterday}`
- **Extract:** Ministry/authority, action/notification summary, affected sectors/products, and specific rule/duty change.

### Sweep 3c: Sector-Level Developments
Run **sector-specific queries** to catch regulatory, pricing, and structural developments affecting entire industries. Do not rely on a single generic query.
- **Queries (run at least 6–8 of these, prioritize sectors with active policy/pricing changes):**
  - `India telecom TRAI tariff spectrum regulation {date_yesterday}`
  - `India auto sales FADA SIAM monthly data {date_yesterday}`
  - `India pharma USFDA approval warning letter import alert {date_yesterday}`
  - `India power tariff CERC electricity regulation coal {date_yesterday}`
  - `India real estate RERA housing policy {date_yesterday}`
  - `India oil gas petroleum OMC fuel price revision {date_yesterday}`
  - `India banking NPA RBI directive lending norms {date_yesterday}`
  - `India agriculture MSP APMC export ban commodity {date_yesterday}`
  - `India steel cement metals anti-dumping duty price {date_yesterday}`
  - `India aviation DGCA airline fare slot allocation {date_yesterday}`
  - `India insurance IRDAI circular regulation {date_yesterday}`
  - `India defence DRDO order procurement policy {date_yesterday}`
- **Filter:** Include only developments that affect the sector structurally (pricing, regulation, capacity, trade policy). Exclude single-company events and speculative trade articles.

### Sweep 4a: Quarterly Earnings (Expanded — Results Season Protocol)
During results season (Oct–Nov, Jan–Feb, Apr–May, Jul–Aug), replace the single broad earnings query with **sector-by-sector sweeps** to meet the 15–20 item minimum.
- **Step 1 — Master list query:**
  - `India companies reported quarterly results {date_yesterday}`
  - `Moneycontrol quarterly results {date_yesterday}`
  - `BSE quarterly results announcements {date_yesterday}`
- **Step 2 — Sector-specific results queries (run until the coverage floor is met):**
  - `India banking NBFC quarterly results Q[X] FY[XX] {date_yesterday}`
  - `India IT services quarterly results {date_yesterday}`
  - `India auto ancillary quarterly results {date_yesterday}`
  - `India cement building materials quarterly results {date_yesterday}`
  - `India pharma healthcare quarterly results {date_yesterday}`
  - `India FMCG consumer quarterly results {date_yesterday}`
  - `India chemical specialty quarterly results {date_yesterday}`
  - `India capital goods engineering quarterly results {date_yesterday}`
  - `India real estate quarterly results {date_yesterday}`
  - `India metal mining quarterly results {date_yesterday}`
  - `India energy oil gas quarterly results {date_yesterday}`
  - `India telecom media quarterly results {date_yesterday}`
- **Extract per result:** Revenue (₹ cr, % YoY), PAT (₹ cr, % YoY), EBITDA margin (% and bps change), and management guidance/commentary if available. Include beat/miss vs consensus where stated.

**Outside results season:** Run only the Step 1 master list queries from Sweep 4a.

### Sweep 4b: Corporate Actions, Orders & Regulatory Events
- **Queries:**
  - `BSE NSE corporate announcements acquisition demerger QIP {date_yesterday}`
  - `India large order win contract award {date_yesterday}`
  - `India promoter stake change insider buying selling {date_yesterday}`
  - `SEBI penalty order show cause notice {date_yesterday}`
  - `India CEO CFO MD resignation appointment management change {date_yesterday}`
  - `India credit rating upgrade downgrade CRISIL ICRA CARE {date_yesterday}`
  - `India ASM GSM surveillance list change {date_yesterday}`
- **Filter:** Strictly discard routine compliance filings, minor vendor contracts, and brokerage target price changes. Extract:
  - *Deals / Orders:* Deal size (₹ cr), counterparty, timeline.
  - *Stake changes:* Buyer/seller, % change, transaction value.
  - *Regulatory:* Authority, nature of action, financial impact.
  - *Management:* Name, role, incoming/outgoing, reason if stated.

### Sweep 5: IPO Status & Today's Earnings Calendar
- **Queries:**
  - `India IPO subscription listing DRHP filed SEBI {date_yesterday}`
  - `India IPO allotment listing date {date_yesterday}`
  - `companies reporting earnings today India {date_today}`
  - `India earnings calendar results schedule {date_today}`
- **Extract:** Primary market updates (subscription multiples, allotment, listing premium/discount) and names of key reporting companies today/tomorrow.

### Coverage Verification (Post-Sweep Gate)
After completing all sweeps, count the items in each section:
- If **Company News < minimum floor**, go back and run additional sector-specific earnings or corporate action queries from Sweep 4a/4b that were not yet executed.
- If **Sector Developments** is empty, confirm by reviewing Sweep 3c results — a genuinely quiet day is acceptable only after the sector-specific queries have been run.
- If **Policy & Regulatory** is empty, confirm by reviewing Sweep 3b results — same rule applies.

---

## 4. Daily Output Template

Save output to: `tmp/general/market-digest/YYYY-MM-DD.md`

```markdown
# India Market Daily Digest — [DD Mon YYYY]
*Window: Preceding 24 hours as of 07:30 AM IST. Pure delta; non-triggered sections omitted.*

**Market Snapshot ([DD Mon YYYY]):** Nifty [XX,XXX] ([+X.X%]) · Bank Nifty [XX,XXX] ([+X.X%]) · A:D [XXXX:XXXX] · FII [-₹X,XXX cr] · DII [+₹X,XXX cr]

## Global Cues
- **Brent Crude:** Up 3.4% to $78.20/bbl on Middle East supply disruption concerns.
- **US 10-Yr Yield:** Rose 12 bps to 4.28% following higher-than-expected US core PPI.

## RBI & Macro
- **India CPI (Sep):** 5.49% YoY vs 3.65% in Aug (consensus 5.1%), driven by higher vegetable prices; food inflation rose to 9.24%.

## Policy & Regulatory
- **Ministry of Finance:** Increased basic customs duty on crude palm, soybean, and sunflower oil from 0% to 20% to support domestic oilseed farmers.

## Sector Developments
- **Telecom:** Department of Telecommunications waived requirement for bank guarantees on spectrum auctions conducted prior to 2022, easing sector liquidity.

## Company News
- **HDFC Bank (HDFCBANK):** Q2 FY25 NII ₹30,110 cr (+10.0% YoY), PAT ₹16,820 cr (+5.3% YoY). GNPA stable at 1.36%. Mgmt reported loan-to-deposit ratio improved to 100% from 104% QoQ.
- **Larsen & Toubro (LT):** Secured mega offshore order valued between ₹10,000–15,000 cr from Middle East client for gas processing. Execution window 36 months.
- **Tata Motors (TATAMOTORS):** Board approved commercial paper issuance up to ₹3,000 cr for working capital requirements.

## IPO Tracker
- **Hyundai Motor India:** Subscribed 2.37× on final day; QIB 6.97×, retail 0.50×. Allotment on Oct 18.

## Earnings Today
- **Reporting today ([DD Mon YYYY]):** Infosys, Wipro, Axis Bank, LTIMindtree.
```

---

## 5. Weekly Protocol: Synthesis & Forward Look

Executed at the end of the trading week (Saturday morning). Synthesizes weekly cumulative metrics, structural themes, and the calendar ahead without re-listing daily news items.

### Sweep 1: Cumulative Weekly Performance
- **Queries:**
  - `Nifty weekly performance FII DII weekly flow {week_start_date} to {week_end_date}`
  - `Nifty sectoral indices weekly performance top gainers losers {week_end_date}`
- **Extract:** Nifty 50 and Bank Nifty weekly % change, top 3 sectoral gainers/losers (%), weekly cumulative FII and DII cash flows (₹ cr).

### Sweep 2: Weekly Synthesis ("So What?")
- Review the daily digest files generated during the week in `tmp/general/market-digest/`.
- Identify the 3–5 structural narratives that drove the market (e.g., FII allocation rotation, margin compression trends in consumer durables, regulatory interventions).
- Formulate high-density synthesis bullets focusing on implications rather than event logs.

### Sweep 3: Weekly Earnings Scorecard (During Results Season)
- Tabulate major index and coverage companies that reported during the week:
  - Company, Revenue YoY %, PAT YoY %, Operating Margin change, and key business read-through.

### Sweep 4: Week Ahead Calendar
- **Queries:**
  - `India economic calendar next week RBI data releases {next_week_start}`
  - `Global economic calendar next week Fed meeting US CPI {next_week_start}`
  - `Major earnings results next week India {next_week_start}`
  - `Upcoming IPOs next week India {next_week_start}`
- **Extract:** Key economic dates, scheduled major company earnings, and IPO listing/bidding dates.

---

## 6. Weekly Output Template

Save output to: `tmp/general/market-digest/weekly-YYYY-WXX.md`

```markdown
# India Market Weekly Digest — Week [XX], [YYYY]
*Period: [DD Mon] – [DD Mon YYYY]. Synthesis, weekly cumulative flows, and calendar ahead.*

---

## 1. The Week in Numbers

| Index / Metric | Weekly Close | Weekly Change (%) | Cumulative Net Flow (₹ Cr) |
|---|---|---|---|
| **Nifty 50** | 24,854 | -1.2% | — |
| **Bank Nifty** | 51,280 | -0.8% | — |
| **India VIX** | 13.80 | +6.2% | — |
| **FII Flow (Cash)** | — | — | -₹14,250 cr |
| **DII Flow (Cash)** | — | — | +₹12,890 cr |

**Sectoral Heatmap:**
- **Top Gainers:** Nifty IT (+2.4%), Nifty Pharma (+1.1%), Nifty FMCG (+0.6%)
- **Top Losers:** Nifty Realty (-4.2%), Nifty Auto (-3.1%), Nifty Metal (-2.8%)

---

## 2. Key Weekly Themes & Synthesis

- **FII Outflows vs DII Absorption:** FIIs logged net sales of ₹14,250 cr in cash equities, driven by capital reallocation toward stimulus-backed Chinese markets. Domestic institutions absorbed ~90% of selling.
- **Consumption Moderation in Earnings:** Early Q2 reports from private banks and retail giants indicate continued urban demand softness and mild margin compression, while asset quality remains resilient.
- **Rate Cut Timing Shift:** Brent crude firming above $78/bbl alongside domestic CPI rising to 5.49% has pushed market consensus for the first RBI repo rate reduction out to Q4 FY25.

---

## 3. Weekly Earnings Scorecard

| Company | Revenue YoY (%) | PAT YoY (%) | Operating Margin | Key Read-through |
|---|---|---|---|---|
| **HDFC Bank** | +10.0% | +5.3% | Stable | NIMs flat; deposit accretion continues to outpace credit growth to repair LDR. |
| **TCS** | +7.6% | +5.0% | 24.1% (-30 bps) | Gradual recovery; BFSI returning to positive growth, European demand subdued. |
| **DMart** | +14.4% | +5.8% | 8.1% (-60 bps) | Metro store throughput experiencing margin drag from quick-commerce competition. |

---

## 4. The Week Ahead ([DD Mon] – [DD Mon YYYY])

### Key Economic & Policy Dates
- **Mon, [Date]:** India WPI Inflation (Sep)
- **Wed, [Date]:** US Retail Sales, China Q3 GDP
- **Thu, [Date]:** ECB Monetary Policy Meeting
- **Fri, [Date]:** India Bank Credit & Forex Reserves update

### Major Earnings Scheduled
- **Financials:** ICICI Bank, Kotak Mahindra Bank, Bajaj Finance
- **Auto / Industrials:** Maruti Suzuki, UltraTech Cement
- **Tech / Pharma:** Sun Pharma, Tech Mahindra

### IPOs & Primary Market
- **New Listings:** Hyundai Motor India (Tue, Oct 22)
- **Bidding Opening:** Waaree Energies (Opens Mon, closes Wed; Issue size ₹4,321 cr)
```

---

## 7. Quality Checklist & Self-Audit Gate

Before saving the output file, verify:

- [ ] **Strict 24-hour window:** No news item, data print, or circular older than 24 hours is included in the daily edition.
- [ ] **Minimum coverage met:** Company News has ≥15 items during results season, ≥5 items otherwise. If below the floor, additional sector-specific queries from §3 Sweep 4a/4b were run before accepting the shortfall.
- [ ] **Sector & Policy sweeps completed:** The dedicated sector-specific (Sweep 3c) and policy/regulatory (Sweep 3b) queries were actually executed — not skipped because the broad query returned nothing.
- [ ] **Zero empty sections:** Every section present in the output has at least one qualifying item exceeding the threshold. No empty headers or placeholder notices exist.
- [ ] **Quantitative thresholds confirmed:** Every global move or index variation cited meets the numerical criteria in §2b.
- [ ] **Units explicit:** Every figure has explicit units (₹ cr, %, bps, $/bbl).
- [ ] **Results anatomy complete:** Earnings entries include revenue, PAT, margin change, and management commentary if available.
- [ ] **Neutral voice:** No speculative, advisory, or promotional language.
- [ ] **Correct routing:** Output saved strictly in `tmp/general/market-digest/`.

---

## 8. Failure Modes to Avoid

- **Recap Bloat:** Re-reporting yesterday's news as if it were a fresh event today.
- **Compliance Noise:** Citing routine disclosures (loss of share certificates, trading window closures, minor board meeting notices).
- **Ghost Headings:** Rendering section titles without qualifying items beneath them.
- **Isolated Margin Figures:** Reporting profit without revenue or operational context.
- **Macro Staleness:** Reporting economic data published days ago because an opinion piece covered it today.
- **Fabricated Breadth:** Using unverified advance-decline numbers instead of verified NSE closing breadth.
- **Thin Coverage During Results Season:** Stopping at 3–5 earnings items when 20+ companies reported. The broad query returns a curated summary; sector-by-sector sweeps (Sweep 4a) are mandatory to reach the coverage floor.
- **Skipping Sector & Policy Sweeps:** Omitting the Sector Developments or Policy & Regulatory sections without first running the dedicated targeted queries in Sweeps 3b and 3c. A single generic query is insufficient confirmation that nothing happened.
- **Source Laziness:** Running only broad portal-agnostic queries. The protocol mandates source-specific queries (PIB, SEBI circulars, sector regulators) because generic searches under-index regulatory and policy actions.
