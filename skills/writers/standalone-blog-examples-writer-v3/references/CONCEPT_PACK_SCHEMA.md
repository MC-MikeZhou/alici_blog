# Concept Pack Schema (Examples & Ideas Writer v3.0)

> Input schema for pre-curated concepts. Optional -- if not provided, the Writer researches and curates concepts independently.

---

## When to Use a Concept Pack

- You already have a curated list of examples/ideas (from source-parser, user research, or Alici use cases)
- You want the Writer to use specific brand cases or campaigns
- You're feeding output from another skill (e.g., source-parser → concept_pack)

If no concept_pack is provided, the Planner step discovers and curates concepts from public research.

---

## Schema

```json
{
  "concept_pack": {
    "source_context": {
      "origin": "source_parser | user_research | alici_use_cases | competitor_analysis | mixed",
      "source_urls": ["https://..."],
      "parsed_at": "2026-02-08T10:00:00Z"
    },
    "thesis": "Why UGC-style ads outperform studio-produced content on TikTok and Instagram",
    "audience": "DTC brand marketers spending $5k-50k/mo on paid social",
    "concepts": [
      {
        "name": "The Unboxing Reaction",
        "scenario": "A creator films their genuine first reaction to opening a product package, capturing authentic surprise and delight. The raw, unscripted nature builds trust with viewers who are tired of polished ads.",
        "why_it_works": "Taps into social proof and parasocial relationships. Viewers feel they're getting an honest opinion rather than a scripted endorsement.",
        "category_hint": "Authenticity-Driven",
        "embed_hint": {
          "type": "tiktok",
          "url_or_source": "Brand: Glossier unboxing series"
        },
        "key_elements": [
          "Genuine first reaction (not rehearsed)",
          "Close-up of product reveal",
          "Natural lighting, phone camera feel"
        ],
        "script_hint": {
          "hook": "Wait till you see what just arrived...",
          "claim": "This [product] has been all over my feed and I finally got one",
          "proof": "[Show genuine reaction to product quality/features]",
          "cta": "Link in bio if you want to try it yourself"
        },
        "source_type": "brand_case",
        "source_url": "https://www.tiktok.com/@glossier/example",
        "alici_use_case_url": null
      }
    ],
    "categorization_hint": {
      "method": "by_format",
      "suggested_categories": ["Authenticity-Driven", "Social Proof", "Educational", "Trend-Jacking"]
    },
    "brand_sources": [
      {
        "brand": "Glossier",
        "source_url": "https://www.tiktok.com/@glossier",
        "data_used": "Unboxing video format and engagement metrics"
      }
    ]
  }
}
```

---

## Field Reference

### Top-Level Fields

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `source_context` | Required | object | Where concepts came from |
| `thesis` | Required | string | Core argument / angle for the article |
| `audience` | Required | string | Target reader description |
| `concepts` | Required | array | Pre-curated concept entries (minimum 3) |
| `categorization_hint` | Optional | object | Suggested grouping strategy |
| `brand_sources` | Optional | array | External brand references for attribution |

### source_context

| Field | Required | Type | Values |
|-------|----------|------|--------|
| `origin` | Required | enum | `source_parser`, `user_research`, `alici_use_cases`, `competitor_analysis`, `mixed` |
| `source_urls` | Optional | string[] | Original URLs analyzed |
| `parsed_at` | Optional | ISO-8601 | When analysis was done |

### concepts[]

| Field | Required | Type | Notes |
|-------|----------|------|-------|
| `name` | Required | string | Short, memorable concept name |
| `scenario` | Required | string | 50-100 words describing who/where/what |
| `why_it_works` | Optional | string | 30-60 words on psychology / mechanism |
| `category_hint` | Optional | string | Suggested category for grouping |
| `embed_hint` | Optional | object | Type + source for visual embed |
| `key_elements` | Optional | string[] | Actionable bullet points |
| `script_hint` | Optional | object | Hook/Claim/Proof/CTA structure (Profile B) |
| `source_type` | Required | enum | `alici_use_case`, `brand_case`, `original_concept`, `competitor_reference` |
| `source_url` | Optional | string | URL for attribution |
| `alici_use_case_url` | Optional | string | Link to alici.ai use case page |

### source_type Values

| Value | Meaning | Attribution Rule |
|-------|---------|-----------------|
| `alici_use_case` | From alici.ai use case pages | Link to use case page in CTA |
| `brand_case` | Real brand campaign / content | Must cite brand name + source in article |
| `original_concept` | Newly created by writer/user | No external attribution needed |
| `competitor_reference` | Structure learned from competitor article | Do NOT copy wording; cite as inspiration only |

---

## Mapping to Planner Step

When concept_pack is provided, the Planner maps fields directly:

| concept_pack field | plan.json field | Mapping |
|-------------------|-----------------|---------|
| `concepts[].name` | `selected_concepts[].name` | Direct copy |
| `concepts[].scenario` | `selected_concepts[].scenario_summary` | May shorten |
| `concepts[].category_hint` | `selected_concepts[].category` | Use as-is or re-categorize |
| `concepts[].embed_hint.type` | `selected_concepts[].embed_type` | Direct copy |
| `concepts[].source_type` | `selected_concepts[].source_type` | Direct copy (new field) |
| `categorization_hint.method` | `categorization.method` | Use as-is or override |
| `brand_sources` | `brand_sources` | Direct copy to plan top-level |

The Planner MAY:
- Add additional concepts beyond those in the pack (research + pack = hybrid)
- Re-rank concepts based on SEO/AEO analysis
- Override categorization_hint if a better grouping emerges
- Remove concepts that don't fit the target profile

The Planner MUST:
- Preserve all `brand_sources` entries for attribution
- Preserve `source_type` for each concept (do not change)
- Set `meta.concept_pack_used = true` in the plan

---

## Integration with Other Skills

```
source-parser → parsed-source.json
                     ↓ (extract concepts)
              concept_pack.json
                     ↓
           Examples Writer v3 (Planner step)
                     ↓
              02-plan.json (concept_pack_used: true)
```

The concept_pack can be created manually (user provides JSON) or extracted from source-parser output. There is no automated pipeline yet -- the user copies relevant concepts from parsed-source.json into concept_pack format.
