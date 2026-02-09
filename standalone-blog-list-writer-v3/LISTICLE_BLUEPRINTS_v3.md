# LISTICLE_BLUEPRINTS_v3 (Standalone)

This is a self-contained copy of AliciBlog’s v3.0 listicle blueprints for use outside the repo environment.

## Global Rules (All Profiles)

### Required Outputs (same folder)
- `01-article-draft.md` (required)
- `02-plan.json` (required)
- `03-assets.json` (required)
- `04-listicle-validator-report.json` (recommended)
- `01-article.md` (optional copy of draft)

### CTA Markers (lintable)
Use HTML comments, exactly:
- `<!-- CTA:1 -->` … `<!-- /CTA -->`
- `<!-- CTA:2 -->` … `<!-- /CTA -->`

### Tables (lintable)
All required tables must be valid Markdown tables (header row + separator row).

### Freshness Statement (lintable)
In **Quick Comparison (Table)** section, include:
`Verified as of YYYY-MM-DD`

### Tool Card (lintable fields, fixed order)

For Standard/Prompt/Alternatives tool items (H2):

`## {rank}. {Tool Name} — {One-line Positioning}`

Then, in order:
- `**Best for:**`
- `**Why it stands out:**`
- `**Key features:**` (≥3 bullets)
- `**Pros:**` (≥3 bullets)
- `**Cons:**` (≥2 bullets)
- `**Pricing:**` (must include an official pricing link)
- `**Notes / limitations:**`

For Mega tool items (H3 under a group H2):

`### {Tool Name} — {One-line Positioning}`

Then the same fields in the same order.

### FAQ Requirements (lintable)
In `## FAQ + Final Verdict`:
- ≥6 FAQ questions
- each answer is **2–4 sentences** (heuristic sentence check)

### Methodology Level Guardrails (lintable)
The declared `02-plan.json.meta.methodology_level` controls allowed claims:
- `research_only`: MUST disclose no hands-on tests; MUST NOT contain “we tested”, “lab”, “sample size” (the phrase “hands-on” is allowed only inside a negative disclosure)
- `hybrid`: MUST include “limited hands-on” + “desk research” (or equivalent) inside `## How We Picked & Tested`
- `hands_on`: MUST include test period + sample size + scenarios + evaluation dimensions inside `## How We Picked & Tested`

---

## Profile A — Standard Listicle (`standard`)

**Typical size**: 10–13 tools  
**Target words**: 4,500–5,500  

### Required H2 Order
1. `## Quick Answer`
2. `## Key Takeaways`
3. `## Quick Comparison (Table)`
4. `## How We Picked & Tested`
5. Tool items (H2): `## 1. ...` → `## N. ...`
6. `## Use Case Matching (Table)`
7. `## How to Choose`
8. `## FAQ + Final Verdict`

### Required Tables
**Quick Comparison (Table)** columns must be exactly:
- `Tool | Best For | Core Positioning | Price | Free Plan | Limitations`

**Use Case Matching (Table)** columns must be exactly:
- `Use Case | Recommended Tools | Why | Budget`

### CTA Positions
- CTA#1: at the end of **Quick Answer** section
- CTA#2: at the end of **FAQ + Final Verdict** section

---

## Profile B — Prompt/Workflow Listicle (`prompt_workflow`)

**Typical size**: 14–20 tools  
**Target words**: 5,500–6,500  

Same as Profile A, plus **two extra mandatory H2 modules** inserted **before** `## How to Choose`:
- `## How to Prompt (Copy-Paste Templates)`
- `## Free vs Paid Breakdown (Table)`

### Free vs Paid Table Columns
Must be exactly:
- `Tier | What You Really Get | Who It’s For | Hidden Limits`

---

## Profile C — Mega Listicle (`mega`)

**Typical size**: 20+ tools  
**Target words**: 8,000–9,500  

### Required H2 Order (top → bottom)
1. `## Quick Answer`
2. `## Key Takeaways`
3. `## Quick Comparison (Table)`
4. `## How We Picked & Tested`
5. `## Category Winners`
6. Group sections (one or more): `## {Group Name}` (H2)
7. `## Use Case Matching (Table)`
8. `## How to Choose`
9. `## FAQ + Final Verdict`
10. `## Update Strategy (Keeping This List Fresh)`

### Grouping Rule (lintable)
After each group H2, tools must be listed as **H3 tool cards** (`### Tool — Positioning`) with tool-card fields.

### CTA Positions
- CTA#1: end of **Quick Answer**
- CTA#2: end of **Category Winners** (not Final Verdict)

---

## Profile D — Alternatives Listicle (`alternatives`)

**Target words**: 6,500–10,000  

### Required H2 Order
1. `## Quick Answer`
2. `## Key Takeaways`
3. `## Ideal Solution Criteria`
4. `## Quick Comparison (Table)`
5. `## How We Picked & Tested`
6. Alternatives tool items (H2 tool cards)
7. `## Use Case Matching (Table)`
8. `## How to Choose`
9. `## FAQ + Final Verdict`

### Alternatives Mini-Table Rule (lintable)
Each alternative tool item must contain at least **one** Markdown table within its section.

