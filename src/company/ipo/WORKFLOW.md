# IPO Analysis Workflow

Workflow rules, pre-requisite scripts, and execution prompts for IPO research (Quick Triage & Full Analysis).

---

## Execution & Output Rules

1. **Output Path:**
   - Check `tmp/company/ipo/` for an existing folder matching `<company-slug>` (e.g. `tmp/company/ipo/fusion-cx/`). If none exists, create it.
   - Artifacts stored in `tmp/company/ipo/<company-slug>/`:
     - `details.json` — IPO metadata, timetable, price band, issue structure, document URLs.
     - `rhp.md` — Red Herring Prospectus converted to Markdown.
     - `quick-review.md` — Output of Mode 1 (Quick Review).
     - `full-analysis.md` — Output of Mode 2 (Full Analysis).
2. **Mandatory Pre-requisite (Data Ingestion):**
   - Before starting analysis in **either mode**, ensure `details.json` and `rhp.md` exist in the company folder.
   - If missing, run the ingestion commands listed in the [Pre-requisite Ingestion Commands](#pre-requisite-ingestion-commands) section.
3. **Primary Data Source & Context Handling:**
   - The primary source of truth is `rhp.md`, supplemented by `details.json`.
   - **Do not read the entire `rhp.md` into context at once.** It is typically 300–800 pages.
   - Target relevant chapters using text search / grep based on standard RHP landmarks:
     - *Objects of the Offer · Capital Structure* → The Deal / Issue Structure
     - *Our Business* → Business Model & Moat
     - *Industry Overview* → Industry Structure (commissioned report)
     - *Our Management · Promoters · Outstanding Litigation* → Management & Governance
     - *Restated Financial Information · MD&A* → Financials & Forensics
     - *Basis for Issue Price* → Valuation & Listed Peers
     - *Risk Factors* → Top risks & deal-breakers
4. **Incremental Research & Write:**
   - Work through the checklist probes sequentially.
   - Extract facts from `rhp.md` and append findings immediately to the output file before moving to the next probe or section.
   - Never batch searches or synthesize from memory.
5. **Format & Citation Standard:**
   - **Mode 1 (Quick Review):** Follow §1 through §6 matching `quick-ipo.md`. Cite page numbers inline `(p.XX)`. Includes the 5 Knockout Kill Gates and final Triage Verdict (`Apply / Wait / Pass` + 3–4 load-bearing reasons + `Worth full deep-dive? [Yes/No]`).
   - **Mode 2 (Full Analysis):** Open with the **Verdict Box** and **Key Facts table** at the top (synthesized last, placed first). Follow the 6-Stage Deep-Dive Architecture: `§1 Deal Anatomy & Proceeds → §2 Business Model & Operations → §3 Industry & Moat → §4 Management & Governance → §5 Restated Forensics (Zero Price) → §6 Valuation Collision & Decision (With Price)`. Every probe answered with a bold lead-in and inline status `[confirmed p.X] / [inferred] / [assumed]`. End each section with its one-line section verdict.
6. **No Assumptions:**
   - All factual statements must be sourced from the RHP. If an item is not disclosed, write `"not disclosed in the RHP"`. Never guess or fill gaps from outside memory.

---

## Pre-requisite Ingestion Commands

Always execute python scripts using the project's virtual environment: `.venv/bin/python`.

### Step 1: Find the IPO ID (Deterministic Tool Search)
**Never do ad-hoc web searches for RHP PDFs or Chittorgarh IDs.** Always use `ipo_client.py search` to query live databases across both mainboard and SME boards:
```bash
.venv/bin/python src/company/ipo/scripts/ipo_client.py search "<company name>"
```
This prints the matching IPO(s), board type (Mainboard/SME), dates, issue size, Chittorgarh ID, and the exact one-step command to run.

*(Note: `data/mainboard_ipos.csv` and `data/sme_ipos.csv` are frozen historical snapshots up to October 2026. For active or newly announced IPOs, always use `ipo_client.py search` instead of searching the CSVs).*

### Step 2: One-Step Ingestion (Metadata + RHP Download + Markdown Conversion)
Once you have the numerical ID or Chittorgarh URL from Step 1, run the unified ingestion command:
```bash
.venv/bin/python src/company/ipo/scripts/ipo_client.py details <id> --fetch-rhp --to-markdown
```
This automatically:
1. Fetches metadata, issue dates, band, size, and KPIs into `tmp/company/ipo/<company-slug>/details.json`.
2. Downloads the official RHP (PDF or ZIP archive from SEBI/NSE/BSE).
3. Converts the RHP into Markdown (`tmp/company/ipo/<company-slug>/rhp.md`) and cleans up intermediate PDFs/ZIPs.

*(Fallback: If the RHP URL is not present in Chittorgarh metadata, locate the official exchange/SEBI filing link and convert via:  
`.venv/bin/python src/company/ipo/scripts/fetch_rhp.py <rhp_url> -c <company-slug> --to-markdown`)*

### Discovery & Ingestion Guardrails
1. **Never bypass `ipo_client.py`:** Do not search Google or third-party tracking portals (Tapetide, IPOWatch, etc.) for PDFs. Third-party sites often host outdated draft prospectuses (DRHPs from prior years) or unrelated article IDs that cause multi-hop failures.
2. **If search returns zero rows:**
   - Verify spelling or try a shorter keyword (e.g. `search watrana` instead of full legal name).
   - Verify year filter if searching a historical deal: `search "<query>" --year <YYYY>`.
   - Never assume an IPO is missing before checking query terms.

---

## Mode Prompts

### Mode 1: Quick Review (Triage)
- **Checklist:** `src/company/ipo/checklists/quick-ipo.md`
- **Output:** `tmp/company/ipo/<company-slug>/quick-review.md`
- **Pre-requisite:** `details.json` and `rhp.md` must exist in `tmp/company/ipo/<company-slug>/`.

```text
i want to do a quick ipo review of <company name>. for the analysis strictly follow src/company/ipo/checklists/quick-ipo.md.
- Output file: tmp/company/ipo/<company-slug>/quick-review.md (reuse existing company folder in tmp/company/ipo/ if present, else create it).
- Pre-requisites: verify that details.json and rhp.md exist in the company folder. If missing, stop and run ipo_client.py and fetch_rhp.py first.
- Data sources: rhp.md is the primary source, supplemented by details.json. Navigate rhp.md via targeted search for relevant chapters (Objects of the Offer, Our Business, Industry Overview, Restated Financials, Basis for Issue Price, Risk Factors). Do not attempt to load the entire RHP at once.
- Process: Follow the 6 core triage modules in quick-ipo.md: §1 The Deal & Insider Arbitrage, §2 Business Model & Operating Machine, §3 Industry Arena & Moat Assessment, §4 Pre-IPO Accounting Forensics, §5 True Peer Benchmarking & Valuation Reality, and §6 Supply Cliffs & Triage Verdict. Answer each probe factually with inline page citations (p.XX). Use structured tables for segments, cash conversion, and peer comparisons.
- Format: Clean section headings matching quick-ipo.md deliverable template. Complete the 5 Knockout Kill Gates scan. Exactly one verdict at the end with 3–4 load-bearing reasons, top 2 kill tripwires, and explicit decision on: Worth the full deep-dive? [Yes/No].
- Do not make assumptions. If not disclosed in the RHP, explicitly state "not disclosed in the RHP".
```

---

### Mode 2: Full IPO Analysis (Deep-Dive)
- **Checklist:** `src/company/ipo/checklists/full-ipo.md`
- **Output:** `tmp/company/ipo/<company-slug>/full-analysis.md`
- **Pre-requisite:** `details.json` and `rhp.md` must exist in `tmp/company/ipo/<company-slug>/`.
- **Optional Tools:**
  - For listed peers named in *Basis for Issue Price*, fetch live peer metrics if needed via:
    ```bash
    .venv/bin/python src/company/listed/scripts/screener_scrape.py <peer_screener_url>
    ```
  - For DuPont, forensic screens (Altman Z, Beneish M) or band multiples inversion from RHP restated financials:
    ```bash
    .venv/bin/python src/company/listed/scripts/financial_calculator.py <input.json>
    .venv/bin/python src/company/listed/scripts/valuation_calculator.py <input.json>
    ```

```text
i want to do a full deep-dive ipo analysis of <company name>. for the analysis strictly follow src/company/ipo/checklists/full-ipo.md.
- Output file: tmp/company/ipo/<company-slug>/full-analysis.md (reuse existing company folder in tmp/company/ipo/ if present, else create it).
- Pre-requisites: verify that details.json and rhp.md exist in the company folder. If missing, stop and run ipo_client.py and fetch_rhp.py first. Read quick-review.md in the company folder if it exists.
- Data sources: rhp.md is the primary source of truth, supplemented by details.json. Navigate rhp.md via targeted chapter searches. For listed peers named in Basis for Issue Price, scrape Screener via screener_scrape.py if external comparison is needed.
- Process: Answer every probe across the 6 stages without dropping any. Work section by section:
  §1 Deal Anatomy, Capital Structure & Proceeds -> §2 Business Model & Operations -> §3 Industry & Moat -> §4 Promoter Ecosystem & Governance -> §5 Restated Financial Forensics (PART A: ZERO PRICE) -> §6 Valuation Collision & Decision (PART B: WITH PRICE).
  Write each section incrementally into the output file.
- Format: Open the file with the Verdict Box and Key Facts table (synthesized last, placed first). For each probe, use bold lead-ins with terse inline status labels [confirmed p.X] / [inferred] / [assumed]. End each section with its one-line section verdict.
- Do not make assumptions. If not disclosed in the RHP, explicitly state "not disclosed in the RHP".
```
