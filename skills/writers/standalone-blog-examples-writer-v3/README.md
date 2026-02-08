# Standalone Blog Examples & Ideas Writer v3.0

> Third core long-form Writer for alici.ai — produces "Examples / Ideas / Templates" showcase articles.

## What It Does

Generates AEO-friendly articles that showcase creative concepts, ideas, or templates — the kind of content triggered by searches like "instagram ad examples", "UGC ad ideas with scripts", or "product video ideas with templates".

## Basic Unit: Concept Card

Unlike Tutorial Writer (Step Cards) or List Writer (Tool Cards), this writer's basic unit is the **Concept Card**:

```
Concept Card fields:
- Scenario (who, where, what)
- Why it works (psychology / algorithm logic)
- Visual embed (video / social post / screenshot)
- Key elements (actionable bullets)
- Script (Hook -> Claim -> Proof -> CTA)  [Profile B only]
- Variations (>=2 alternatives)            [Profile B only]
- Try it CTA
```

## 3 Profiles

| Profile | Name | Concepts | Words | Use Case |
|---------|------|----------|-------|----------|
| A | Showcase | 10-25 | 3,500-7,000 | "15 UGC Ad Examples" |
| B | Ideas + Templates | 5-15 | 3,000-5,500 | "10 Product Video Ideas with Scripts" |
| C | Mega Gallery | 25-60+ | 6,000-10,000 | "50 Instagram Story Ideas" |

## Output Bundle

```
01-article-draft.md                — Article with all markers
02-plan.json                       — Planning data (concept_pool, categorization, brand_sources)
03-assets.json                     — Image/embed asset queue
04-examples-validator-report.json  — Self-check (PASS/FAIL)
```

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Main specification |
| `EXAMPLES_BLUEPRINT_v3.md` | Structure contract (H2 order, markers, tables, source attribution, "How to Recreate" spec) |
| `PLAN_SCHEMA_MIN_v3.json` | Plan JSON schema (with flex column + brand_sources) |
| `ASSETS_SCHEMA_MIN_v3.json` | Assets JSON schema |
| `SELF_CHECK_SCHEMA_MIN_v3.json` | Validator report schema (15 checks) |
| `PROMPT_CLAUDE_WEB.md` | One-paste version for Claude Web |
| `examples_validator.py` | Python validator for deterministic structural checks |
| `references/` | Shared dependency docs |
| `references/CONCEPT_PACK_SCHEMA.md` | Input schema for pre-curated concepts |

## Design Basis

- **28 InVideo benchmark articles** analyzed for structure patterns
- **DataForSEO keyword validation**: ~22,000+/mo search volume for "examples/ideas/templates" queries
- **Architecture alignment** with Tutorial Writer v3 (markers) and List Writer v3 (pipeline + profiles)

See: `research 竞品分析/2026-02-06-examples-ideas-writer-research.md` for full data.
