# Listed Company Analysis Workflow (Steps 1–6)

Workflow rules and execution prompts for listed company research.

---

## Execution & Output Rules

1. **Output Path:**
   - Check `tmp/company/listed/` for an existing folder matching `<company name>`, its ticker, or slug (e.g. reuse `tmp/company/listed/kaynes-technology/` if present). If none exists, create `tmp/company/listed/<company-slug>/`.
   - File path: `tmp/company/listed/<company-folder>/<step-name>-analysis.md`.
2. **Incremental Research & Write (Strictly 1 point at a time):**
   - Pick 1 question from the checklist.
   - Run websearch for that specific question.
   - Process findings and immediately write/append the point to the file BEFORE searching for the next question.
   - Never batch searches across multiple questions or wait until the end to write the file.
3. **Format Standard:**
   - Section heading: `## <N>. <Section Title from Checklist>`
   - Point heading: `### Point <N.M>: <Exact Question from Checklist>`
   - First line of each answer: `- **Status / Claim Type:** Confirmed (source) / Inferred / Assumed`
   - End of each section: `### Section <N> Red Flag Evaluation:` with assessment (`PASS / FLAG`).
4. **No Assumptions:**
   - Do not guess. If information is not found or is ambiguous, state it as unverified or ask.

---

## Step Prompts

### 1. Business Model
- **Checklist:** `src/company/listed/checklists/1-business-model.md`
- **Output:** `tmp/company/listed/<company-slug>/1-business-model-analysis.md`

```text
i want to do business model analysis of <company name>. for the analysis strictly follow src/company/listed/checklists/1-business-model.md.
- Output file: tmp/company/listed/<company-slug>/1-business-model-analysis.md (reuse existing company folder in tmp/company/listed/ if present, else create it).
- Process: Pick 1 question at a time from the checklist. Do websearch, process findings, and immediately append to the file BEFORE searching for the next question. Do not batch searches.
- Format: For each question, use "### Point X.Y: <Exact Question from checklist>" with "- **Status / Claim Type:** Confirmed (source) / Inferred / Assumed" on the first line. End each section with "### Section X Red Flag Evaluation:" (Assessment: PASS / FLAG).
- Do not make assumptions, if in doubt, ask away.
```

---

### 2. Industry Structure
- **Checklist:** `src/company/listed/checklists/2-industry.md`
- **Output:** `tmp/company/listed/<company-slug>/2-industry-analysis.md`

```text
i want to do industry analysis of <company name>. for the analysis strictly follow src/company/listed/checklists/2-industry.md.
- Output file: tmp/company/listed/<company-slug>/2-industry-analysis.md (reuse existing company folder in tmp/company/listed/ if present, else create it).
- Process: Pick 1 question at a time from the checklist. Do websearch, process findings, and immediately append to the file BEFORE searching for the next question. Do not batch searches.
- Format: For each question, use "### Point X.Y: <Exact Question from checklist>" with "- **Status / Claim Type:** Confirmed (source) / Inferred / Assumed" on the first line. End each section with "### Section X Red Flag Evaluation:" (Assessment: PASS / FLAG).
- Do not make assumptions, if in doubt, ask away.
```

---

### 3. Moat and Guidance
- **Checklist:** `src/company/listed/checklists/3-moat-guidance.md`
- **Output:** `tmp/company/listed/<company-slug>/3-moat-guidance-analysis.md`
- **Pre-requisite:** `screener.md` must exist in the company folder. If missing, find the Screener.in link for the company via websearch, then run:
  ```
  .venv/bin/python src/company/listed/scripts/screener_scrape.py <screener_url>
  ```
  This creates `tmp/company/listed/<company-slug>/screener.md` with financials, ratios, and links to annual reports, concalls, and investor presentations.
- **PDF conversion:** To convert any downloaded PDF (annual report, concall transcript, investor presentation) to markdown:
  ```
  .venv/bin/python src/common/scripts/pdf_to_markdown.py <path-to-pdf>
  ```
  This converts the PDF to a `.md` file in the same directory and deletes the original PDF.

```text
i want to do moat and guidance analysis of <company name>. for the analysis strictly follow src/company/listed/checklists/3-moat-guidance.md.
- Output file: tmp/company/listed/<company-slug>/3-moat-guidance-analysis.md (reuse existing company folder in tmp/company/listed/ if present, else create it).
- Data sources: use screener.md in the company folder as the primary data source. For context, screener.md also has links to annual reports, concalls, and investor presentations — download and convert them to markdown using src/common/scripts/pdf_to_markdown.py, then search for context using grep within them only if needed. Do not unnecessarily download all of them. Additionally use websearch if needed. 
- Process: Pick 1 question at a time from the checklist. Find relevant info from the above sources, process findings, and immediately append to the file BEFORE moving to the next question. Do not batch searches.
- Format: For each question, use "### Point X.Y: <Exact Question from checklist>" with "- **Status / Claim Type:** Confirmed (source) / Inferred / Assumed" on the first line. End each section with "### Section X Red Flag Evaluation:" (Assessment: PASS / FLAG).
- Do not make assumptions, if in doubt, ask away.
```

---

### 4. Management & Capital Allocation
- **Checklist:** `src/company/listed/checklists/4-mgmt-capital-allocation.md`
- **Output:** `tmp/company/listed/<company-slug>/4-mgmt-capital-allocation-analysis.md`
- **Pre-requisites:**
  - `screener.md` must exist in the company folder. If missing, find the Screener.in link for the company via websearch, then run:
    ```
    .venv/bin/python src/company/listed/scripts/screener_scrape.py <screener_url>
    ```
  - `3-moat-guidance-analysis.md` should exist in the company folder — this step reads the say-do table (B2), commentary findings (B3), and metric choices (B5) from it. If missing, run Step 3 first.
- **PDF conversion:** To convert any downloaded PDF (annual report, concall transcript, investor presentation) to markdown:
  ```
  .venv/bin/python src/common/scripts/pdf_to_markdown.py <path-to-pdf>
  ```
  This converts the PDF to a `.md` file in the same directory and deletes the original PDF (use `--keep-pdf` to retain it).

```text
i want to do management and capital allocation analysis of <company name>. for the analysis strictly follow src/company/listed/checklists/4-mgmt-capital-allocation.md.
- Output file: tmp/company/listed/<company-slug>/4-mgmt-capital-allocation-analysis.md (reuse existing company folder in tmp/company/listed/ if present, else create it).
- Prior step input: read 3-moat-guidance-analysis.md in the company folder for the say-do table (B2), commentary findings (B3), and metric choices (B5) — reference them, do not rebuild.
- Data sources: use screener.md in the company folder as the primary data source. For additional context, use websearch. screener.md also has links to annual reports, concalls, and investor presentations — download and convert them to markdown using src/common/scripts/pdf_to_markdown.py, then search for context using grep within them only if needed. Do not unnecessarily download all of them.
- Process: Pick 1 question at a time from the checklist. Find relevant info from the above sources, process findings, and immediately append to the file BEFORE moving to the next question. Do not batch searches.
- Format: For each question, use "### Point X.Y: <Exact Question from checklist>" with "- **Status / Claim Type:** Confirmed (source) / Inferred / Assumed" on the first line. End each section with "### Section X Red Flag Evaluation:" (Assessment: PASS / FLAG).
- Do not make assumptions, if in doubt, ask away.
```

---

### 5. Financials & Key Drivers
- **Checklist:** `src/company/listed/checklists/5-financials.md`
- **Output:** `tmp/company/listed/<company-slug>/5-financials-analysis.md`
- **Pre-requisite:** `screener.md` must exist in the company folder. If missing, find the Screener.in link for the company via websearch, then run:
  ```
  .venv/bin/python src/company/listed/scripts/screener_scrape.py <screener_url>
  ```
  This creates `tmp/company/listed/<company-slug>/screener.md` with financials, ratios, and links to annual reports, concalls, and investor presentations.
- **Financial calculator:** Prepare a JSON input from screener.md financial data (use `--template` to see the expected schema), then run:
  ```
  .venv/bin/python src/company/listed/scripts/financial_calculator.py <input.json> --wacc <N> -o <output.md>
  ```
  This computes ratio tables, DuPont decomposition, forensic screens (Altman Z, Beneish M), and working capital analysis. Sections can be run individually via `--section <name>`.
- **PDF conversion:** To convert any downloaded PDF (annual report, concall transcript, investor presentation) to markdown:
  ```
  .venv/bin/python src/common/scripts/pdf_to_markdown.py <path-to-pdf>
  ```
  This converts the PDF to a `.md` file in the same directory and deletes the original PDF (use `--keep-pdf` to retain it).

```text
i want to do financials and key drivers analysis of <company name>. for the analysis strictly follow src/company/listed/checklists/5-financials.md.
- Output file: tmp/company/listed/<company-slug>/5-financials-analysis.md (reuse existing company folder in tmp/company/listed/ if present, else create it).
- Prior step input: read the prior analysis files in the company folder (if present).
- Financial calculator: prepare a JSON input from screener.md financial data (run with --template to see the expected schema), then run financial_calculator.py to compute ratio tables, DuPont decomposition, forensic screens, and working capital analysis. Incorporate its output into the analysis.
- Data sources: use screener.md in the company folder as the primary data source. For additional context, use websearch. screener.md also has links to annual reports, concalls, and investor presentations — download and convert them to markdown using src/common/scripts/pdf_to_markdown.py, then search for context using grep within them only if needed. Do not unnecessarily download all of them.
- Process: Pick 1 question at a time from the checklist. Find relevant info from the above sources, process findings, and immediately append to the file BEFORE moving to the next question. Do not batch searches.
- Format: For each question, use "### Point X.Y: <Exact Question from checklist>" with "- **Status / Claim Type:** Confirmed (source) / Inferred / Assumed" on the first line. End each section with "### Section X Red Flag Evaluation:" (Assessment: PASS / FLAG).
- Do not make assumptions, if in doubt, ask away.
```

---

### 6. Valuation
- **Checklist:** `src/company/listed/checklists/6-valuation.md`
- **Output:** `tmp/company/listed/<company-slug>/6-valuation-analysis.md`
- **Pre-requisite:** `screener.md` must exist in the company folder. If missing, find the Screener.in link for the company via websearch, then run:
  ```
  .venv/bin/python src/company/listed/scripts/screener_scrape.py <screener_url>
  ```
  This creates `tmp/company/listed/<company-slug>/screener.md` with financials, ratios, and links to annual reports, concalls, and investor presentations.
- **Valuation calculator:** Prepare a JSON input from screener.md financial data (use `--template` to see the expected schema), then run:
  ```
  .venv/bin/python src/company/listed/scripts/valuation_calculator.py <input.json> --hurdle <N> -o <output.md>
  ```
  This computes 3-year multiples-based valuation (P/E, EV/EBITDA, P/S, P/B), inversion analysis (implied growth for hurdle rate, breakeven exit multiple), and a 2D sensitivity grid (growth rate vs. exit multiple).
- **PDF conversion:** To convert any downloaded PDF (annual report, concall transcript, investor presentation) to markdown:
  ```
  .venv/bin/python src/common/scripts/pdf_to_markdown.py <path-to-pdf>
  ```
  This converts the PDF to a `.md` file in the same directory and deletes the original PDF (use `--keep-pdf` to retain it).

```text
i want to do valuation analysis of <company name>. for the analysis strictly follow src/company/listed/checklists/6-valuation.md.
- Output file: tmp/company/listed/<company-slug>/6-valuation-analysis.md (reuse existing company folder in tmp/company/listed/ if present, else create it).
- Valuation calculator: prepare a JSON input from screener.md financial data (run with --template to see the expected schema), then run valuation_calculator.py to compute multiples-based valuation, inversion analysis, and sensitivity grid. Incorporate its output into the analysis.
- Data sources: use screener.md in the company folder as the primary data source. For additional context, use websearch. screener.md also has links to annual reports, concalls, and investor presentations — download and convert them to markdown using src/common/scripts/pdf_to_markdown.py, then search for context using grep within them only if needed. Do not unnecessarily download all of them.
- Process: Pick 1 question at a time from the checklist. Find relevant info from the above sources, process findings, and immediately append to the file BEFORE moving to the next question. Do not batch searches.
- Format: For each question, use "### Point X.Y: <Exact Question from checklist>" with "- **Status / Claim Type:** Confirmed (source) / Inferred / Assumed" on the first line. End each section with "### Section X Red Flag Evaluation:" (Assessment: PASS / FLAG).
- Do not make assumptions, if in doubt, ask away.
```
