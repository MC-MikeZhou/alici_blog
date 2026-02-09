# Listicle v3.0 Overview (Blog List Writer)

This document is a **project-level index** for AliciBlog’s Listicle v3.0 system.

**Primary skill**: `skills/writers/blog-list-writer/SKILL.md`  
**Blueprint spec**: `skills/_docs/LISTICLE_BLUEPRINTS_v3.md`  
**Validator gate**: `scripts/listicle_validator.py`  
**Changelog**: `skills/writers/blog-list-writer/CHANGELOG.md`  

---

## What changed in v3.0 (why it exists)

Listicle v3.0 upgrades list-mode from “guideline writing” to “compile-like writing”:
- Blueprints define a fixed structure (headings, tables, CTAs, tool cards)
- A Plan Pack is produced **before** long-form writing (so domain-unknown cases don’t become “tool listings”)
- A Validator runs as a **hard gate** (structure PASS/FAIL) before downstream steps

---

## Inputs (upstream compatibility)

Upstream inputs commonly come from `growth-topic-scout` Topic Briefs. v3.0 is designed to accept both:
- `selected_topic` shaped briefs (common in `00-topic-brief.json`)
- “flat” briefs (older topic-brief formats)

When fields are missing, v3.0 should infer safe defaults and record them in:
- `02-plan.json.assumptions`

---

## Outputs (v3.0 Plan Pack bundle)

For `content_type=list`, v3.0 must produce these files in the output folder:
- `01-article-draft.md` — the blueprint-compliant article draft (downstream-compatible)
- `02-plan.json` — Plan Pack: tool pool, selection, evidence, tables, FAQ, CTAs, assumptions
- `03-assets.json` — Assets queue: featured image + diagrams + optional tool images (editor-safe defaults)
- `04-listicle-validator-report.json` — PASS/FAIL + errors/warnings (machine-readable)

Optional:
- `01-article.md` — a copy of `01-article-draft.md` for v3-friendly naming (downstream should not depend on it)

---

## Profile selection (blueprints)

v3.0 uses `listicle_profile` to choose a Blueprint:
- `standard` — 10–13 items, 4,500–5,500 words
- `prompt_workflow` — 14–20 items + prompting/templates modules, 5,500–6,500 words
- `mega` — 20+ tools, **grouped**, plus Category Winners + Update Strategy, 8,000–9,500 words
- `alternatives` — competitor alternatives, deep comparison, 6,500–10,000 words

Details (exact H2 order, required tables/columns, CTA markers, tool card fields):
- `skills/_docs/LISTICLE_BLUEPRINTS_v3.md`

---

## Validator gate (PASS before downstream)

Run the validator against the output folder:

```bash
python3 scripts/listicle_validator.py --dir "<output_dir>"
```

Policy:
- **FAIL (blocking)**: missing/incorrect headings order, missing tables or wrong columns, missing CTA markers, tool-card field issues, Quick Answer word count, freshness mismatch, plan/assets missing or invalid.
- **WARNING (non-blocking)**: evidence gaps such as Top5 missing third-party links; list_size mismatch; freshness older than policy threshold.

Downstream tools (editor / aeo / export) should only run when validator status is PASS.

---

## Methodology-level trust rules (no “fake testing”)

`02-plan.json.meta.methodology_level` controls allowed claims:
- `research_only`: must disclose no hands-on tests; must not claim “we tested/lab/sample size”
- `hybrid`: must mention limited hands-on checks + desk research
- `hands_on`: must include test period + sample size + scenarios + evaluation dimensions

The validator enforces the trust boundary.

---

## Assets queue vs Editor image policy (isolation)

Editor’s default policy remains: **3–5 high-information-density images**.

`03-assets.json` is an **execution queue**, not a mandate:
- Defaults to `meta.recommended_generate_max=5` to stay compatible with editor cost/quality constraints
- May list `tool_images` for every tool as **low priority** candidates
- Must include: featured image + at least 2 diagrams (comparison infographic + decision tree recommended)

