# growth-topic-scout Changelog

All notable changes to the Growth Topic Scout skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.4] - 2026-02-05

### Added

**Competitive Insights Output Field (v2.4 NEW)**
- New output field: `competitive_insights` in Topic Brief
- Purpose: Structure competitive analysis data for blog-tutorial-writer v2.5 Insight Pack input
- Trigger: Automatically generated when Mode A analyzes competitor URLs
- Sub-fields:
  - `top_competitors` (3-5 entries): Competitor name, URL, unique strength
  - `content_gaps` (2-5 entries): Topics/angles competitors don't cover
  - `data_points` (3-10 entries): Quantitative metrics with source attribution
- Integration: Feeds directly into blog-tutorial-writer v2.5 Insight Pack mechanism

**Extraction Guidelines**
- **top_competitors**: Extract from competitor article citations, identify differentiation
- **content_gaps**: Identify unanswered questions, missing markets, pricing details
- **data_points**: Extract market size, growth rates, performance metrics with sources

### Changed

**Mode A Enhancement**
- Updated from "output growth-oriented topic briefs with SEO/AEO signals"
- To "output growth-oriented topic briefs with SEO/AEO signals + competitive_insights"
- Mode A now provides structured competitive data for downstream writers

**Topic Brief Structure**
- Expanded from 7 output fields to 8 output fields
- New field #8: Competitive Insights (optional, empty if no competitor analysis)

**Version Number**
- version: "2.3" → "2.4"
- updated: "2026-02-05"

### Integration Impact

**With blog-tutorial-writer v2.5**:

```
growth-topic-scout v2.4
    ↓ outputs competitive_insights
blog-tutorial-writer v2.5
    ↓ auto-converts to Insight Pack
Article with Market Context + Monetization Framework
```

**Conversion mapping**:
- `top_competitors` → `insight_pack.competitive_sources`
- `data_points` → `insight_pack.market_data.key_metrics`
- `content_gaps` → differentiation strategy in article

### Example Output

```json
{
  "topic_brief": {
    "primary_keyword": "how to become ai influencer",
    "... other fields ...",
    "competitive_insights": {
      "top_competitors": [
        {
          "name": "Higgsfield",
          "url": "https://higgsfield.ai/blog/ugc-factory",
          "strength": "SoulID technology for character consistency"
        },
        {
          "name": "HeyGen",
          "url": "https://heygen.com/blog/avatar-iv",
          "strength": "170+ language localization"
        },
        {
          "name": "Invideo",
          "url": "https://invideo.io/blog/ugc-ads",
          "strength": "4x CTR performance benchmarks"
        }
      ],
      "content_gaps": [
        "Chinese market strategy (Douyin/XiaoHongShu)",
        "Specific income ranges for monetization",
        "0-to-1 launch roadmap for beginners"
      ],
      "data_points": [
        {
          "metric": "Market size",
          "value": "$6.06B (2024)",
          "source": "Invideo"
        },
        {
          "metric": "CTR improvement",
          "value": "4x vs traditional ads",
          "source": "HeyGen"
        },
        {
          "metric": "Cost reduction",
          "value": "70% vs traditional shooting",
          "source": "HeyGen"
        }
      ]
    }
  }
}
```

### Backward Compatibility

- ✅ competitive_insights is optional field - empty if not applicable
- ✅ Mode B (Keyword Matrix) doesn't generate competitive_insights (no competitor URLs)
- ✅ Mode D (Seed Mode) can optionally include competitive_insights if competitor analysis performed
- ✅ Existing workflows without blog-tutorial-writer v2.5 ignore this field

### Philosophy Change

> **From**: "Output topic briefs with SEO/AEO validation"
>
> **To**: "Output topic briefs with SEO/AEO validation + structured competitive intelligence"

**Rationale**:
- Competitive analysis data exists but wasn't structured for downstream use
- blog-tutorial-writer v2.5 needs Insight Pack data
- Extracting competitive insights during topic scouting (Mode A) is more efficient than separate competitive analysis step
- Structured data > unstructured notes in competitor reports

---

## [2.3] - 2026-01-25

### Added

**Mode D2: Diversity Seed Mode**
- Seed decomposition into 5 orthogonal dimensions
- Multi-strategy divergence (3 strategies, ~45 topics)
- Semantic clustering + diversity gate
- DataForSEO validation (8-15 topics)
- Portfolio scoring (SEO + AEO + Diversity Bonus)
- Output: 3 ready-to-write directions + diversity report

**diversity_report Output**
- Cosine similarity matrix
- Cluster distribution analysis
- Diversity score calculation

### Changed

**Mode Architecture**
- Added Seed Mode variant: D1 (Competitor-Anchored) vs D2 (Diversity Engine)
- D1 outputs 2 directions, D2 outputs 3 directions

**DataForSEO Integration**
- Added 3 AEO/LLM-related data dimensions (Mode C)

---

## [2.2] - 2026-01-25

### Added

**Mode D1: Seed Mode (Competitor-Anchored)**
- 6-Phase funnel: Mission Config → Competitor Anchors → Intent Patterns → Expansion → Validation → Title Lock
- Output: 2 executable directions with locked titles + evidence chains
- Direction object schema with `locked_title`, `evidence_chain`, `recommended_skill`, `outline`
- Mission Config schema (3 questions: seed, intent, outcome)

**Phase 0: Mission Config**
- Interactive questionnaire (seed keyword, intended usage, expected outcome)
- Competitor anchor detection (5 competitors, default; supports 3-5)

**Phase 0.5: Competitor Intent Pattern Discovery**
- Extract 5-8 intent patterns from competitor blogs
- Intent-driven keyword expansion (60-80 keywords)

**Phase 2: DataForSEO Validation**
- Three-level filtering (search volume, KD score, trend direction)
- Cost optimization: ~$0.47 (standard) / ~$1.52 (deep)

**Phase 2.5: Scope Pruning**
- 60 keywords → 10 directions
- Removes duplicate intents, low-potential keywords

**Phase 3: Title Lock**
- Verified titles with SERP evidence
- 2 final directions ready to write

### Changed

**Mode B Evolution**
- From "50-100 keyword expansion" to "Direction-oriented funnel"
- Human confirmation effort reduced: 50-100 keywords → 2 directions

---

## [2.1] - 2026-01-18

### Added

**Recommended Titles Enhancement**
- 3 title options by content type (Listicle / How-to / Insights)
- Year validation (2026 or 2025 required)
- CTR prediction (high / medium-high / medium)
- Formula enforcement:
  - Listicle: Must include number
  - How-to: Must start with "How to" or "Guide to"

---

## [2.0] - 2026-01-XX

### Added

**Mode B: Keyword Matrix**
- Input seed keywords, generate 50-100 keyword matrix
- Gap analysis report
- SERP analysis (Top 20)
- Competitor crawl (WebFetch)

**Mode C: AEO Validation Layer**
- Phase C1: AI Keyword Data (LLM platform search volume)
- Phase C2: LLM Mentions (Competitor AI citation analysis)
- Phase C3: LLM Responses (AI answer content analysis)
- Dual Scoring: SEO Score (100) + AEO Score (100)

---

## [1.0] - 2025-XX-XX

### Initial Release

**Mode A: URL Analysis**
- Input competitor URLs
- Extract topics
- DataForSEO validation
- Output: Top 10 topics with SEO signals

**Topic Brief Structure**
- Recommended Titles
- Target Query (primary keyword)
- Content Type (Tutorial / List / News / Comparison)
- H2/H3 Outline
- AEO Answer Block
- Differentiation Angle
- Product Mapping

---

## Version Upgrade Guidelines

**When to bump versions**:
- **Major (X.0)**: New modes, breaking output changes
- **Minor (x.Y)**: New output fields, enhanced features
- **Patch (x.y.Z)**: Bug fixes, documentation updates

**Backward Compatibility**:
- v2.4 competitive_insights is optional field (empty if not used)
- All downstream tools must handle missing/empty competitive_insights gracefully

---

*Changelog maintained by the alici.ai Content Team*
*Last updated: 2026-02-05*
