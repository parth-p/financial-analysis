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
   - **Mode 1 (Quick Review):** Plain headings (`## The Deal`, `## Business`, etc.). Cite page numbers inline `(p.XX)`. No metadata header block or summary table. One final `## Verdict` at the end (`Apply / Wait / Pass` + 3–4 load-bearing reasons + `Worth full deep-dive? [Yes/No]`).
   - **Mode 2 (Full Analysis):** Open with the **Verdict Box** and **Key Facts table** at the top. Follow with `## §1 The Deal` through `## §9 The Decision`. Every probe answered with a bold lead-in and inline status `[confirmed p.X] / [inferred] / [assumed]`. End each section with its one-line section verdict.
6. **No Assumptions:**
   - All factual statements must be sourced from the RHP. If an item is not disclosed, write `"not disclosed in the RHP"`. Never guess or fill gaps from outside memory.

---

## Pre-requisite Ingestion Commands

Run these before starting an analysis to populate `details.json` and `rhp.md`:

```bash
# 1. Fetch IPO details metadata (issue dates, band, size, URLs) -> details.json
.venv/bin/python src/company/ipo/scripts/ipo_client.py details <id_or_url> --output tmp/company/ipo/<company-slug>/details.json

# 2. Download RHP PDF and convert to Markdown -> rhp.md
.venv/bin/python src/company/ipo/scripts/fetch_rhp.py <rhp_url> -c <company-slug> --to-markdown
```

*(Note: If the RHP URL is present in the Chittorgarh listing, `ipo_client.py details <id_or_url> --fetch-rhp --to-markdown` handles both in a single step).*

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
- Process: Follow the sections in quick-ipo.md: The Deal, Business, Industry, Moat, Financials & Valuation, Risks, and Verdict. Answer each probe factually with inline page citations (p.XX). Append each section to the file immediately before moving to the next.
- Format: No metadata header and no duplicate summary table. Clean section headings. Exactly one verdict at the end with 3–4 load-bearing reasons and explicit decision on: Worth the full deep-dive? [Yes/No].
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
- Process: Answer every probe from §1 to §9 without dropping any. Work section by section:
  §1 The Deal -> §2 Business Model -> §3 Industry & Moat -> §4 Management & Governance -> §5 Financials & Forensics -> §6 Valuation -> §7 Demand & Mechanics -> §8 Risks (ranked top 3) -> §9 Decision.
  Write each section incrementally into the output file.
- Format: Open the file with the Verdict Box and Key Facts table (synthesized last, placed first). For each probe, use bold lead-ins with terse inline status labels [confirmed p.X] / [inferred] / [assumed]. End each section with its one-line section verdict.
- Do not make assumptions. If not disclosed in the RHP, explicitly state "not disclosed in the RHP".
```
