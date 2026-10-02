# Listed Company Analysis Workflow (Steps 1–3)

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

### 3. Moat
- **Checklist:** `src/company/listed/checklists/3-moat.md`
- **Output:** `tmp/company/listed/<company-slug>/3-moat-analysis.md`

```text
i want to do moat analysis of <company name>. for the analysis strictly follow src/company/listed/checklists/3-moat.md.
- Output file: tmp/company/listed/<company-slug>/3-moat-analysis.md (reuse existing company folder in tmp/company/listed/ if present, else create it).
- Process: Pick 1 question at a time from the checklist. Do websearch, process findings, and immediately append to the file BEFORE searching for the next question. Do not batch searches.
- Format: Use "### Point X.Y: <Exact Question from checklist>" with "- **Status / Claim Type:** Confirmed (source) / Inferred / Assumed" on the first line. End each section with "### Section X Red Flag Evaluation:" (Assessment: PASS / FLAG).
- Do not make assumptions, if in doubt, ask away.
```
