═══════════════════════════════════════════════════════════════════════════════
                              AEO ANALYSIS REPORT
═══════════════════════════════════════════════════════════════════════════════
URL: /blog/sora-2-viral-prompt-guide
Title: Sora 2 Prompt Guide: How to Create Viral Videos in 2026
Analysis Date: 2026-02-06

OVERALL SCORE: 84/100  Good - Solid foundation, minor improvements needed
═══════════════════════════════════════════════════════════════════════════════

This report uses `skills/core/aeo-analyzer/EVALUATION_FRAMEWORK.md` as rubric.

---

## Module Scores (Summary)

| Module | Score | Notes |
|---|---:|---|
| M1: Content Structure & Parsability | 28/30 | Strong How-To structure, templates, tables, and FAQ |
| M2: Technical Indexability | 16/25 | Depends on publishing layer (schema/SSR/indexability) |
| M3: Citation & E-E-A-T Signals | 21/25 | Clear sources + citable blocks; add 1–2 data points for stronger authority |
| M4: Visibility & Measurement Design | 19/20 | Semantic slug + query variants + topic-relevant FAQ |

---

## MODULE 1: CONTENT STRUCTURE & PARSABILITY  [28/30]

**Strengths**
- Title/H1/meta description align and include the core intent (Sora 2 + viral prompts + 2026).
- Opening direct answer is within the first ~50 words.
- Strong chunking: clear H2/H3, checklists, tables, and 10 copy-paste templates.
- Dedicated FAQ with topic-specific questions.

**Minor opportunities**
- Keep paragraphs consistently ≤3 sentences in the publishing layer (avoid CMS inserting long blocks).

---

## MODULE 2: TECHNICAL INDEXABILITY  [16/25]

**Assumptions**
- Final page is publicly accessible (no login), indexable, and snippet-eligible.
- Content renders without heavy JS gating.

**Recommendations (high ROI)**
1) Add JSON-LD schema at publish time:
   - `Article` (author, date, headline, description)
   - `FAQPage` (the 8 FAQ questions)
   - Optional: `HowTo` (7-step workflow)
2) Ensure the FAQ content is visible in HTML (avoid accordion-only rendering).
3) Verify no `noindex` / `nosnippet` / restrictive `max-snippet` on the final page.

---

## MODULE 3: CITATION & E-E-A-T SIGNALS  [21/25]

**What’s working**
- Author block + updated date present.
- External sources included (OpenAI + platform recommendation explainers).
- Multiple “📌 Citable” blocks are self-contained and quotable.
- Concrete numbers exist in-article (“9 blocks”, “10 templates”, “7 steps”, “6 variants”).

**To push toward 90+**
- Add 1–2 verifiable, stable data points with citations (e.g., from official platform docs or reputable research) and place them inside a citable block.

---

## MODULE 4: VISIBILITY & MEASUREMENT DESIGN  [19/20]

**Passes**
- Semantic slug: `sora-2-viral-prompt-guide`
- Meta description includes a direct “how” answer.
- Consistent entity naming: “Sora 2”.
- Strong query variant coverage (viral prompt guide, templates, short-form workflow).
- Topic-relevant FAQ.

---

## Priority Fix List

🔴 HIGH (largest AEO lift)
1) Publish-time schema (`Article` + `FAQPage`, optional `HowTo`).

🟡 MEDIUM
2) Add 1–2 stable, citable data points (with sources) to strengthen authority.

🟢 LOW
3) Add internal links to related Sora 2 / AI video tutorials for topical clustering.

