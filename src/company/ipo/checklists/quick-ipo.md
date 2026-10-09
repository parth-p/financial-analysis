# IPO Quick Review — Analyst's Triage Checklist

*The fast screen. Run this on every IPO in the window to decide apply / wait / pass, and whether the deal is worth the full deep-dive. It carries fewer probes than the full checklist, but answers each one properly. Compact sections, one verdict at the end.*

> **The one rule:** approach the IPO with informed skepticism — the seller has an information advantage and chose the timing. But present the analysis neutrally: state what the RHP shows, strengths and concerns alike, at their actual size, and let the facts drive the conclusion.

> **The question this answers:** would you buy this business on the open market at the band price the week after listing? Listing-day mechanics (subscription, GMP, anchor book) are a separate game this checklist does not play.

> **The source:** the RHP only. Every fact in the review comes from the RHP. If the RHP doesn't disclose something, say so. Don't fill the gap from memory, outside sources or assumption.

---

## The output — structure & house rules

1. **No metadata header.** The document opens with the title only (`# <Company> — IPO Quick Review`). Do **not** print CIN, registrar, BRLM roster, market maker, doc date, bidding dates as a header block — the facts that matter appear inside their sections.
2. **No Key Facts table.** State each number **once, in the section that owns it** — issue size / OFS in The Deal, band / m-cap / multiples in Financials & Valuation, leverage there too, concentration in Business. No standalone summary table (it only duplicates the body).
3. **Proper compact sections, not a scorecard.** Each section is a few **real insight-bullets** covering the highest-signal probes, not a metric restatement or a flag-table row. **The test for Business, Industry, Moat:** after reading these three sections, a reader unfamiliar with the industry should understand what the company physically does, why the industry's returns are what they are, and whether excess returns are evidenced in the RHP's numbers. Revenue segment percentages and margin numbers alone are data, not insight — explain the mechanism as the RHP describes it.
4. **Explain fully, without padding.** Every bullet either states a fact from the RHP or explains what that fact means for the business or the verdict. Cut restatement, preamble, and generic description that would be true of any company in the sector. Answer the follow-up parts of a probe only where the RHP gives relevant information.
5. **One verdict, at the end.** No verdict at the top. The document builds through the sections and closes with `## Verdict`: the call + **3–4 load-bearing reasons** + what changes the call + size + **worth the full deep-dive? [yes/no]**. Nothing else repeats the verdict.
6. **Clean headings.** Section headings are plain: `## The Deal`, `## Business`, `## Industry`, `## Moat`, `## Financials & Valuation`, `## Risks`, `## Verdict`. Never echo this checklist's internal notes into the output.
7. **Cite pages, don't infer.** Put `(p.XX)` on load-bearing numbers — that *is* the confirmation. Numbers you calculate from RHP figures show their inputs and cite their pages (e.g. `net debt/EBITDA 2.1× (p.312, p.318)`). Don't state facts the RHP doesn't contain; where something isn't disclosed, write "not disclosed in the RHP." Judgments — the moat conclusion, the risk ranking, the verdict — are presented as judgments and tied to the specific RHP facts behind them.
8. **Promote deal-breakers.** A red flag found in any section (a manufactured one-off, a promoter pledge, an auditor resignation or qualification, a buried regulatory action) must surface in **Risks** and drive the **Verdict** — never leave it stranded in a single line.
9. **Neutral, balanced tone.** State facts at their actual size and let them speak. Note strengths and concerns where the RHP evidence supports them — don't add either just to balance the picture. Don't overstate a point in either direction: no loaded language ('predatory,' 'siphoning,' 'tunneling'), and no promotional language ('market leader,' 'robust,' 'best-in-class') unless attributed to the RHP. The analysis is a clear-eyed assessment, not a prosecution or a pitch.
10. **SEBI numbers change** — take them from the RHP `(verify)`.

---

## Before you start *(prep — not in the deliverable)*
- Read the **RHP** (not DRHP); `fetch_rhp.py` pulls + text-converts it. Read the sections the probes draw on:
  - **Objects of the Offer · Capital Structure · Basis for Issue Price** → The Deal, Valuation
  - **Our Business** → Business, Moat
  - **Industry Overview** → Industry (attribute figures to the report — it is commissioned for the offer)
  - **Restated Financial Information (incl. notes) · MD&A** → Financials, Moat
  - **Our Promoters · Our Management · Outstanding Litigation** → Risks
  - **Risk Factors** — top ~25 in detail, then the headline of every remaining one (deal-breakers are often buried late)
- Skim, don't sweep.

---

## What to check — the compressed probe set

### The Deal
- [ ] Fresh vs. OFS + **economic OFS** — a "fresh issue" whose proceeds buy promoter assets / repay promoter loans is an OFS in disguise; and is the raise **growth capital or a balance-sheet bailout**?
- [ ] Who sells & **why now** (growth / fund-exit / peak-window / distress); WACA → gain multiple; any **down-round** vs. the last private mark.
- [ ] Proceeds — build value vs. extract; RPT + independent appraisal; GCP size; eligibility route (Reg 6(1)/6(2)/SME).
- [ ] Promoter keep post-issue + **lock-in** + **pledge/encumbrance**.

### Business
- [ ] **What the company actually does** — the production or service chain end-to-end (for a manufacturer: raw material → process steps → finished product; for services: how value is delivered step by step), as the RHP describes it. Explain the operation clearly enough that someone unfamiliar with the industry gets it.
- [ ] **Why this business exists** — who the customer is, what job they hire this product or service for, how critical it is to the customer, and where the company sits in the value chain (who supplies it, who it sells to).
- [ ] **Revenue quality & concentration** — recurring / repeating / one-time, and the reason the pattern holds as shown in the RHP (contract terms, repeat-customer data, order book) — *why* does this customer keep coming back, or why must the sale be re-won each time? Concentration (top-1/5/10 customer, geography, product) with trend direction.
- [ ] **One unit-economics fact** that characterises the business — the native metric (per-tonne spread, take rate, realization per unit, commission slab) that explains why margins are what they are, where the RHP discloses it. One number with context, not a margin table.

### Industry
- [ ] **How the industry works** — from the RHP's Industry Overview: how companies in this space make money, what a typical operation looks like, the structure (fragmented / consolidated, and the trajectory), lifecycle position, and whether demand is secular or cyclical. Describe the industry, don't judge it yet.
- [ ] **The one binding force** capping returns for the *average* player (supplier power / buyer power / rivalry / entry / substitutes), with evidence from the RHP. Name the listed peers from Basis for Issue Price, and note if they differ materially in business mix. *(If a claim is true of this company specifically but not the average player, it belongs in Moat.)*

### Moat
- [ ] **What structural advantages does this company have, if any?** Look at the numbers the RHP provides first: RoCE/ROIC across available years, margins vs. the RHP's peers, whether input-cost changes were passed through (MD&A), market-share data from the industry report. Describe what you find, then name the source (which of five, or **none**) + **direction** (widening / stable / eroding). If ≤3 years of numbers don't show a clear advantage, state "unproven."
- [ ] **The replication test** — what would a well-capitalised competitor need to build this position? Answer from what the RHP discloses (capacity, approvals, licences, customer qualification periods, relationships). If the RHP shows no real barrier, say so.

### Financials & Valuation
- [ ] **Is the reported profit real?** — strip one-offs / receivables spike / RPT / proforma; name the **anomaly** and the normalized number.
- [ ] Earnings → **cash** conversion; **leverage/solvency** (D/E, net-debt/EBITDA, interest coverage); **capital intensity & cash cycle** — does growth consume cash or throw it off? Asset-light or asset-heavy.
- [ ] **Band multiple on normalized earnings** (right metric for the sector); vs. the RHP's **listed peers** on the same-period basis (note the date and price basis the RHP uses); vs. **private mark / NAV** (strip RPT goodwill).
- [ ] **Margin of safety** — wider for an IPO's asymmetry; are the band's implied expectations conservative / reasonable / heroic against the RHP's track record?

### Risks
- [ ] **Governance scan** — check for: promoter pledge · RPT · auditor resignation or qualification · pre-IPO KMP churn (CFO / CS / independent directors) · litigation/tax demands exceeding annual PAT · buried regulatory action · capital-allocation red flags. Any finding must appear in the ranked risks below or be explicitly dismissed.
- [ ] **Rank the top 3 that can cause permanent loss** — each: probability · severity · permanence · a **monitorable tripwire**. Fold in governance findings and any deal-breaker surfaced above. Don't list 20; rank 3.

### Verdict *(the only verdict — at the end)*
- [ ] **Call** + **3–4 load-bearing reasons** (most decisive first) + **what changes the call** + size (none / small / standard). The call should follow from the sections above, not from a default stance:
  - **Apply** — the business holds up on the probes and the band is reasonable on normalized earnings.
  - **Wait** — the business may be worth owning, but the price or an open question doesn't clear yet. Name what you're waiting for (a price, a lock-in expiry, the next reported results).
  - **Pass** — a deal-breaker, or the band's implied expectations aren't supported by the RHP's numbers.
- [ ] **Worth the full deep-dive?** Apply, or Wait with an interesting business → **run `ipo-checklist.md`**. Clear pass → stop here.

---

## The output template

```
# <Company> — IPO Quick Review

## The Deal
## Business
## Industry
## Moat
## Financials & Valuation
## Risks               (governance scan + ranked 1–3, each with tripwire)

## Verdict
> Call: [Apply / Wait / Pass] — 3–4 reasons — what changes the call — size
> Worth the full deep-dive? [Yes → ipo-checklist.md / No]
```

---

*The full checklist judges everything. The quick review carries only the highest-signal probe from each section, states each fact once where it belongs, and builds to a single verdict. If the deal, the business, the numbers, and the three ways you lose money permanently all clear — escalate; if any is a deal-breaker, you already have your answer.*