# Indian Listed Universe Discovery: Agent Protocol

**What this does:** Takes a **theme** (a sector, product, service, or one step in a supply chain) and returns two things:

1. **A plain-English explainer.** What the theme is, why it matters, where it sits in the value chain, what it replaces, how big it is, what impact it can have, and whether it is worth caring about.
2. **The full list of NSE/BSE-listed companies linked to it**, sorted by how much of each company the theme really is.

> Companion to the *Indian Equity Peer Analysis* protocol. That flow runs **company → peers**. This flow runs **theme → companies**.

---

## 1. Input

- **Theme:** `[Sector / Industry / Sub-segment / Product / Service / Value-chain step]`
- **Optional context:** `[Core players only vs. any exposure, size band, Main board / SME, sub-theme focus]`

*Examples:* `data center construction`, `trailer axles`, `GLP-1 / CDMO`, `railway wagons`, `solar EPC`, `quick commerce`, `defence electronics`, `agrochemical active ingredients`, `India GCCs`.

### Scope check (do this before any search)

- **Too broad** (e.g., "renewable energy", "manufacturing"): pick the sub-theme the user most likely means, or split into 2–3 sub-themes. Say which you chose.
- **Too narrow** (likely fewer than 3 listed names): widen by one step in the value chain. Say that you widened it.
- Write a one-line scope statement: *"Included: … Not included: …"*. It goes at the top of the output.

---

## 2. Ground Rules

### 2a. How to research

1. **Map the value chain before hunting for names.** A theme is never one thing. Break it into steps (raw material → component → assembly → brand/OEM → distribution → service). Companies sit at different steps, and different searches find different steps.
2. **Never trust one list.** Index lists, fund holdings, screeners, and broker reports each show a different slice. The real answer is all of them combined, with duplicates removed.
3. **Don't open PDFs.** No annual reports, sector primers, or fund documents. Portals, factsheet summaries, and news already carry the lists and segment splits.
4. **Sort by real exposure, not by label.** A company called an "EV play" that earns 2% from EVs is not the same as one that earns 80%.
5. **Announcements are not revenue.** MoUs, "plans to enter", and capex intent do not count as exposure. Look for actual sales or a reported segment.
6. **Name the listed company, not the brand.** The business may sit inside a listed parent, a holding company, or an unlisted subsidiary. Always give the ticker that actually trades.
7. **Look beyond the main board.** Include BSE, SME platforms (NSE Emerge / BSE SME), IPOs from the last 1–3 years, and the pipeline (DRHP filed). Hot themes are badly under-counted by older lists.
8. **Every number needs a source and a year.** If sources disagree, give the range and say who said what.
9. **Prefer trusted sources for market size.** In order: government ministries, NITI Aayog, IBEF, industry bodies, rating agencies (CRISIL, ICRA, CARE), industry sections of recent RHPs (as summarised by portals or news), and brokerages. Paid "market research" press releases (*"X market to reach $Y bn by 2032"*) are often inflated. Use them only if nothing else exists, and flag them.

### 2b. How to write (plain language)

- **Write for a smart reader who is new to this sector.** If a college student who reads business news cannot follow it, rewrite it.
- **Short sentences.** Aim for under 20 words. One idea per sentence.
- **Explain jargon the first time you use it**, in brackets. Example: *CDMO (a company that makes medicines for other drug companies on contract)*.
- **Use one everyday analogy** to explain the theme.
- **Give numbers context.** Write *"₹40,000 Cr (about $4.8 bn) in FY25"*, not just *"₹40,000 Cr"*. Always tag the year.
- **Say what you don't know plainly.** Write *"No reliable data found"* instead of hedging.
- **Never say the same thing twice.** Each fact lives in one place in the output.

**Word swaps:**

| Avoid | Write instead |
| :--- | :--- |
| Optionality | A small bet that could grow |
| Read-through | Indirect link |
| Tailwinds / headwinds | Things helping it / things hurting it |
| TAM | Total market size |
| Moat | What stops competitors from copying it |
| Secular growth | Long-term growth, not a one-time boom |
| Capex | Spending on new plants or equipment |
| Operating leverage | Profits growing faster than sales as fixed costs get spread out |
| De-rating | The stock's valuation falling |
| Pure-play | Core player (the company is mostly this business) |

**Good vs. bad:**

> ❌ *"CDMO players are well-positioned to capture secular tailwinds from China+1 de-risking of innovator supply chains."*
>
> ✅ *"CDMOs make medicines for big global drug companies on contract. Those drug companies want to depend less on China. That is sending more orders to Indian CDMOs."*

---

## 3. Search Playbook

**Budget: 10–15 searches.** Use the higher end for broad or "hot" themes.
- Stage 1 (understand the theme): 3–4 searches
- Stage 2 (find the companies): 5–8 searches
- Stage 3 (check and measure): 1–3 searches

### Stage 1: Understand the Theme

#### Q1. What is it, and what is its value chain?
```text
"[Theme]" India explained "how it works" value chain
```
*Alternative:*
```text
"[Theme]" India industry overview segments upstream downstream
```
**Extract:**
- A simple one-line definition.
- 3–6 value-chain steps, and which step the theme itself is.
- Which steps have Indian listed players vs. are imported or unlisted.
- Keywords and synonyms for each step (used in Q7).

#### Q2. How big is it, and how fast is it growing?
```text
"[Theme]" India market size crore OR billion CAGR [Current Year]
```
*Global variant:*
```text
"[Theme]" global market size India share
```
**Extract:**
- India market size today (with year).
- Projected size and target year.
- Growth rate (CAGR: the average yearly growth).
- Global market size and India's share.
- Source names. Aim for 2+ sources and report a range.

#### Q3. What is it replacing, and why now?
```text
"[Theme]" India replacing OR "shift from" OR "import substitution" OR "unorganised to organised"
```
*Policy variant:*
```text
"[Theme]" India PLI OR scheme OR policy OR mandate [Current Year]
```
**Extract:**
- The old way it replaces (imports, older technology, unorganised players, manual process).
- The trigger: policy, falling costs, new technology, regulation, or changing customer habits.
- How much is imported today (% if available).
- Government support (PLI, duties, mandates, budget allocations).

#### Q4. What could go wrong?
```text
"[Theme]" India risks OR challenges OR overcapacity OR "China competition" OR "margin pressure"
```
**Extract:**
- Top 3–5 risks.
- Signs of hype: rush of new entrants, IPO cluster, falling prices, unused capacity.
- Evidence on whether players actually make money.

### Stage 2: Find the Companies

#### Q5. Index and fund holdings
The richest single source. Index providers and thematic funds publish ready-made lists of companies with real exposure.
```text
"[Theme]" index constituents Nifty OR BSE thematic
```
*Fund/ETF variant (finds names not yet in any index):*
```text
"[Theme]" thematic fund OR ETF portfolio holdings India
```
**Extract:** names, tickers, and portfolio weights (a rough hint of how pure each name is).

#### Q6. Broker coverage list
When a broker starts covering a sector, it names the stocks it considers the investable set.
```text
"[Theme]" India "initiating coverage" OR "sector report" listed companies
```
**Extract:** the named stocks (usually 5–15), plus any "pure vs. diversified" split the analyst already made. Reuse it.

#### Q7. Step-by-step search for specialists *(repeat for each value-chain step from Q1)*
Index and broker lists lean towards large companies. This finds the small, mid-size, and SME specialists.
```text
"[Step / product / service]" manufacturers OR suppliers OR providers India listed "NSE" OR "BSE"
```
*Example for the inverter step in solar:* `"solar inverter" manufacturers India listed NSE`

**Extract:** 1–4 listed specialists per step. Record which step each belongs to. Companies at different steps are not direct competitors.

#### Q8. Recent IPOs, SME listings, and the pipeline
```text
"[Theme]" IPO listed NSE BSE [Current Year] [Current Year - 1]
```
```text
"[Theme]" SME IPO "NSE Emerge" OR "BSE SME" listed
```
```text
"[Theme]" DRHP filed SEBI IPO upcoming
```
**Extract and tag:**
- Listed in the last ~3 years → **Recent IPO**
- SME platform → **SME** (thin trading, less disclosure)
- Filed but not listed → **Pipeline**

#### Q9. Large diversified companies with a segment in the theme
These belong in the list, but not as core players.
```text
"[Theme]" segment revenue India listed company
```
**Extract:** company name, which segment, and the rough % of revenue it makes up.

### Stage 3: Check and Measure

#### Q10. Numbers for the shortlist
Batch 3–4 companies per search.
```text
"[Company A]" "[Company B]" "[Company C]" market cap revenue PE screener
```
**Extract:** market cap (₹ Cr), revenue (₹ Cr), EBITDA margin (%), RoCE (%), and P/E. Note the date of the data.

#### Q11. Exposure check *(only when needed)*
Run this for any Tier 1 or Tier 2 name whose theme share is still a guess.
```text
"[Company]" "[theme / segment]" revenue share OR segment revenue FY[latest]
```

---

## 4. Combine and Clean

1. **Merge** everything from Q5–Q9 into one list.
2. **Remove duplicates.** The same company shows up under different sources and names. Keep one row per ticker.
3. **Resolve to the listed company.** If a source names a brand or subsidiary, map it to the listed parent. Note whether exposure is direct or through a holding company.

---

## 5. Sort Into Tiers

Use theme share of revenue as the main test. Use segment reporting and fund weight as tie-breakers.

| Tier | Name | Test | Plain meaning |
| :--- | :--- | :--- | :--- |
| **1** | **Core Players** | Theme is the stated core business, or **>~60%** of revenue | The company *is* the theme |
| **2** | **Big Segment** | Theme is a separately reported segment, or **~15–60%** of revenue | A major part, but the company does other things too |
| **3** | **Side Bets** | **<~15%** of revenue, one product line, or just starting | Real but small. Not a proxy for the theme |

**If the % is unknown:** stated core business → Tier 1. Separately reported segment → Tier 2. Single product line or early stage → Tier 3.

**Mark how sure you are about each theme share:**
- **✓ Reported:** the company reports the segment or states the %.
- **≈ Estimated:** from a broker, news report, or fund note. Approximate.
- **? Unverified:** inferred from the product list. Check before relying on it.

Never place a **?** company in Tier 1 without a one-line reason.

---

## 6. Remove False Positives

Move a company to the **"Left Out"** list if any of these apply:

- **Announcement only:** tagged on an MoU, plan, or capex intent with no revenue yet. (You may keep it in Tier 3 with a **"pre-revenue"** flag.)
- **Wrong step:** in the broad ecosystem but not in the theme as scoped. Example: a generic fabricator showing up under a specialised component theme.
- **Not tradable:** unlisted, private, delisted, or suspended.
- **Holding company mix-up:** the operating unit is not listed, and the listed parent's overall exposure is tiny.
- **Fund filler:** held by a thematic fund for size or liquidity, with almost no real exposure. Test it against the tier rules. Don't inherit the fund's label.

---

## 7. "Is It Worth It?" Scorecard

Rate the **theme** (not individual stocks) on 8 factors. Use 🟢 Strong, 🟡 Mixed, or 🔴 Weak. The thresholds below are rough guides, not hard rules.

| Factor | Question it answers | 🟢 Strong looks like | 🔴 Weak looks like |
| :--- | :--- | :--- | :--- |
| **Size** | Is the market big enough to matter? | Over ~₹50,000 Cr, or a fast-growing slice of a large global market | Under ~₹5,000 Cr niche |
| **Growth** | How fast is it growing? | Over ~15% a year, expected for 5+ years | Slower than the economy (under ~10% a year) |
| **Staying power** | Is this a lasting shift or a short boom? | Driven by several forces at once (policy, cost, habits) | Depends on one subsidy, one cycle, or a fad |
| **Government push** | Is policy helping? | PLI, mandates, import duties, multi-year budgets | No support, or policy keeps changing |
| **India's edge** | Can Indian companies win this? | Cost or skill advantage, local supply chain | Key inputs or technology are imported or licensed |
| **Profits** | Do players actually make money? | Healthy margins, RoCE over ~15% for core players | Losses, or RoCE below ~12% |
| **Crowding** | How tough is the competition? | Few players, hard to enter | Rush of new entrants, IPO cluster, falling prices |
| **Price already paid** | Are the stocks already expensive? | Core players' P/E near their own history or the market | P/E far above the market, with years of growth already priced in |

**Pick one verdict that matches the scorecard:**

- **Real and still early:** strong basics, and stock prices are not stretched.
- **Real but priced in:** strong basics, but valuations are already high.
- **Real but tough:** growing, but crowded or low-margin.
- **Early and unproven:** mostly plans, little actual revenue yet.
- **Mostly hype:** weak basics, driven by stories.

Then add one line each on **what would make the view better** and **what would make it worse**.

Always end the section with: *"This rates the theme, not any single stock. It is not investment advice."*

---

## 8. Output Template

Every session must use this format.

```markdown
# [Theme]: Listed Universe Report
*Data as of [Month Year]. Sources listed at the end.*

## The Short Answer
- **What it is:** [One line, plain English]
- **How big:** [India size today → projected size by year, ~X% growth a year]
- **Verdict:** [Verdict label]: [one-line reason]
- **Listed companies found:** [N total: X core, Y big segment, Z side bets, W on watchlist]
- **Closest core players:** [2–3 names]
- **Scope:** Included: [...]. Not included: [...].

---

## Part 1: Understanding the Theme

### What is it?
[2–4 short sentences.]
**Think of it like:** [One everyday analogy.]

### Why does it matter?
- **Why now:** [What changed recently]
- **Who needs it:** [The end customer]
- **What it unlocks:** [What becomes possible or cheaper]

### Where does it sit in the value chain?
[Raw material] → [Component] → **[THIS THEME]** → [Assembly / OEM] → [End customer]

| Step | What happens here | India's position | Listed players |
| :--- | :--- | :--- | :--- |
| [Step 1] | [Plain description] | [Strong / Growing / Mostly imported] | [Names, or "none listed"] |
| **[Theme step] ← this theme** | [Plain description] | [...] | [Names] |
| [Step 3] | [Plain description] | [...] | [Names] |

### What is it replacing?
| Old way | New way | Why the switch is happening |
| :--- | :--- | :--- |
| [e.g., Imported from China] | [e.g., Made in India] | [e.g., PLI scheme + higher import duty] |

### How big is it?
| Measure | Figure | Source (year) |
| :--- | :--- | :--- |
| India market today | ₹X Cr (~$X bn) | [Source, year] |
| India market by [year] | ₹X Cr (~$X bn) | [Source, year] |
| Growth rate | ~X% a year | [Source, year] |
| Global market | ~$X bn | [Source, year] |
| India's share of global | ~X% | [Source / calculated] |

**In plain terms:** [One line on what these numbers mean. Flag if sources disagree.]

### What impact can it have?
- **Who wins:** [...]
- **Who loses:** [...]
- **Bigger picture:** [Jobs, imports saved, exports, cost to consumers]

### Is it worth it?
| Factor | Rating | Why |
| :--- | :--- | :--- |
| Size | 🟢 / 🟡 / 🔴 | [One line] |
| Growth | | |
| Staying power | | |
| Government push | | |
| India's edge | | |
| Profits | | |
| Crowding | | |
| Price already paid | | |

**Verdict: [Label].** [2–3 sentences.]
- **What would make this better:** [...]
- **What would make this worse:** [...]

*This rates the theme, not any single stock. It is not investment advice.*

---

## Part 2: The Listed Companies

### Tier 1: Core Players (the company *is* the theme, >60% of revenue)
| Company (Ticker) | What it does | Step | Theme share | Mkt Cap (₹ Cr) | Revenue (₹ Cr) | EBITDA % | P/E | Listing |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **[Name]** (`NSE: XXX`) | [≤8 words] | [Step] | ~75% ✓ | ~X,XXX | ~X,XXX | ~XX% | ~XX | Main |

**Why each is here:**
- **[Company]:** [One line: e.g., "Largest listed maker of X in India" or "Only listed company doing Y".]

### Tier 2: Big Segment (a major part of the business, ~15–60%)
| Company (Ticker) | Segment in this theme | Step | Theme share | Mkt Cap (₹ Cr) | Revenue (₹ Cr) | EBITDA % | P/E | Listing |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **[Name]** (`NSE: XXX`) | [Segment] | [Step] | ~30% ≈ | ~X,XXX | ~X,XXX | ~XX% | ~XX | Main |

### Tier 3: Side Bets (small part, <15%, or just starting)
| Company (Ticker) | What links it to the theme | Theme share | Mkt Cap (₹ Cr) | Flag |
| :--- | :--- | :--- | :--- | :--- |
| **[Name]** (`NSE: XXX`) | [One line] | ~5% ? | ~X,XXX | [Pre-revenue / New entry / —] |

### Watchlist: Not Yet Listed or SME
| Company | Status | Step | Why watch it |
| :--- | :--- | :--- | :--- |
| [Name] | [DRHP filed / SME: NSE Emerge] | [Step] | [One line] |

### Left Out (and why)
- **[Company]:** [One line, e.g., "Only an MoU so far, no revenue."]

---

## Part 3: Risks and What to Watch
- **Main risks:** [3–5 one-liners]
- **Signals to track:** [e.g., import data, policy deadlines, order wins, new capacity, price trends]

## Sources
- [Source name] — [what was taken from it] — [date]

*Legend: ✓ Reported · ≈ Estimated · ? Unverified*
```

---

## 9. Final Check Before Sending

- [ ] The Short Answer makes sense on its own, in under 60 seconds of reading.
- [ ] The scope statement is present.
- [ ] Every jargon word is explained or swapped out.
- [ ] Every number has a source and a year. Market data has an "as of" date.
- [ ] No company appears twice anywhere in the output.
- [ ] Every Tier 1 company has a ✓ or ≈, or a one-line reason if it is ?.
- [ ] No announcement-only company sits in Tier 1 or Tier 2.
- [ ] SME platforms, recent IPOs, and the DRHP pipeline were all checked.
- [ ] The verdict matches the scorecard (e.g., not "Real and still early" with four 🔴s).
- [ ] No PDFs were opened.