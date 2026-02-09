# Insight Pack JSON Schema

> **Version**: 1.1
> **Created**: 2026-02-05
> **Last Updated**: 2026-02-05

## Overview

The **Insight Pack** is an optional JSON input for `blog-tutorial-writer` that structures competitive analysis data for knowledge transfer. It enables writers to incorporate market context, monetization frameworks, and experience evidence systematically.

**Purpose**:
- Structure competitive insights for blog-tutorial-writer
- Trigger conditional sections (Market Context, Monetization Framework)
- Provide E-E-A-T data sources (competitive_sources)
- Enable Experience Evidence (experiment_pack) for M3 AEO scoring

**When to use**:
- Complex/composite topics (e.g., "AI Influencer + UGC Ads + Monetization")
- Monetization-focused tutorials
- Articles requiring market data or revenue pathway frameworks
- You have real testing/experimentation data to share (v1.1 NEW)

**When NOT to use**:
- Simple single-tool tutorials
- No competitive research available
- Topic Brief already comprehensive

---

## JSON Schema v1.1

```json
{
  "insight_pack": {
    "thesis": "string (required)",
    "why_now": "string (required)",
    "key_takeaways": ["array of strings (required)", "3-5 items"],
    "market_data": {
      "market_size": "string (optional)",
      "cagr": "string (optional)",
      "key_metrics": {
        "metric_name": "string (optional)"
      }
    },
    "monetization_paths": [
      {
        "path": "string (optional)",
        "income_range": "string (optional)"
      }
    ],
    "competitive_sources": [
      {
        "source": "string (optional)",
        "data_used": "string (optional)"
      }
    ],
    "content_gaps": ["array of strings (optional)"],
    "experiment_pack": {
      "test_description": "string (optional)",
      "methodology": "string (optional)",
      "results": [
        {
          "metric": "string (optional)",
          "value": "string (optional)",
          "delta": "string (optional)"
        }
      ],
      "sample_size": "string (optional)",
      "date_range": "string (optional)",
      "key_insight": "string (optional)"
    }
  }
}
```

---

## Field Definitions

### Core Fields (Required)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `thesis` | string | Core argument (1 sentence) | "AI Influencer + UGC Ads is the most profitable combo for content creators in 2026" |
| `why_now` | string | Why write this topic now | "Market explosion ($6.06B) + tech maturity (SoulID) + cost advantage (-70%)" |
| `key_takeaways` | array[string] | 3-5 key points | ["SoulID technology maintains character consistency", "170+ language capability", "UGC ad CTR improves 4x"] |

### Optional Fields (Trigger Conditional Sections)

| Field | Type | Triggers | Description |
|-------|------|----------|-------------|
| `market_data` | object | Market Context section | Market size, growth rate, key metrics |
| `monetization_paths` | array[object] | Monetization Framework section | Revenue streams with income ranges |
| `competitive_sources` | array[object] | E-E-A-T citations | Data source attributions |
| `content_gaps` | array[string] | Differentiation strategy | Competitor content gaps to address |
| **`experiment_pack`** (v1.1 NEW) | **object** | **Experience Evidence** | **Real testing/experimentation data for M3 scoring** |

---

## market_data Object

**Purpose**: Provide market statistics to trigger Market Context section

**Structure**:
```json
"market_data": {
  "market_size": "$6.06B (2024)",
  "cagr": "40.8% (2025-2030)",
  "key_metrics": {
    "ctr_improvement": "4x vs traditional ads",
    "cost_reduction": "70% vs traditional shooting",
    "conversion_lift": "29% conversion rate improvement"
  }
}
```

**Generated Section**: "Why [Topic] Is Exploding Right Now"
- Market Opportunity subsection with Citable Block
- Key Performance Metrics comparison table
- "What This Means for You" personalization

**Word Count**: 200-300 words

---

## monetization_paths Array

**Purpose**: Structure revenue streams to trigger Monetization Framework section

**Structure**:
```json
"monetization_paths": [
  {"path": "Brand Endorsement", "income_range": "$500-$50,000/post"},
  {"path": "UGC Ad Services", "income_range": "$100-$500/video"},
  {"path": "Digital Products", "income_range": "Passive income"},
  {"path": "Livestream Commerce", "income_range": "Commission split"},
  {"path": "IP Licensing", "income_range": "Annual licensing fee"}
]
```

**Generated Section**: "How to Make Money with [Topic]: [N] Revenue Streams"
- 3-5 revenue streams with "What it is", "Income potential", "How to start", "Pro tip"
- Income Projection subsection with Citable Block
- 12-month income milestone table

**Word Count**: 400-600 words

---

## competitive_sources Array

**Purpose**: Provide data source citations for E-E-A-T

**Structure**:
```json
"competitive_sources": [
  {"source": "Higgsfield", "data_used": "SoulID tech, UGC Factory"},
  {"source": "HeyGen", "data_used": "Avatar IV, 170+ languages"},
  {"source": "Invideo", "data_used": "4x CTR, 29% conversion"}
]
```

**Usage**: All sources appear as citations in article

**Example Citation**:
```markdown
According to Higgsfield's SoulID technology documentation, virtual influencer character consistency...
([Higgsfield](https://higgsfield.ai))
```

---

## content_gaps Array

**Purpose**: Identify competitor content gaps for differentiation

**Structure**:
```json
"content_gaps": [
  "Chinese market strategy (Douyin/XiaoHongShu/Kuaishou)",
  "Specific monetization amount cases",
  "0-to-1 launch roadmap"
]
```

**Usage**: Writer addresses these gaps with dedicated content

**Example**:
- Gap: "Chinese market strategy"
- Generated subsection: "Targeting Chinese Platforms: Douyin & XiaoHongShu Strategies"

---

## experiment_pack Object (v1.1 NEW) ⭐

**Purpose**: Provide real testing/experimentation data for M3 Experience Evidence scoring (5 points in AEO Analyzer)

**Structure**:
```json
"experiment_pack": {
  "test_description": "We tested AI Influencer + UGC Ads workflow using Alici AI to generate 5 virtual influencer videos for a skincare brand",
  "methodology": "A/B test: AI influencer UGC ads vs traditional creator UGC ads, same product, same platform (TikTok)",
  "results": [
    {"metric": "Generation Time", "value": "3 minutes vs 2 hours", "delta": "-97%"},
    {"metric": "CTR", "value": "4.2% vs 1.1%", "delta": "+281%"},
    {"metric": "Cost per Video", "value": "$12 vs $450", "delta": "-97%"},
    {"metric": "Engagement Rate", "value": "6.8% vs 3.2%", "delta": "+112%"}
  ],
  "sample_size": "n=50 ad campaigns (25 AI, 25 traditional)",
  "date_range": "2026-01-15 to 2026-01-30",
  "key_insight": "AI influencers outperformed real creators in CTR due to hyper-optimized visual consistency"
}
```

### Field Definitions

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `test_description` | string | What you tested (1-2 sentences) | "We tested AI Influencer + UGC Ads workflow..." |
| `methodology` | string | How you tested (control vs treatment) | "A/B test: AI influencer vs traditional creator ads" |
| `results` | array[object] | Metric objects with name, value, delta | See structure above |
| `sample_size` | string | Sample size with n=X notation | "n=50 ad campaigns (25 AI, 25 traditional)" |
| `date_range` | string | Test period (YYYY-MM-DD to YYYY-MM-DD) | "2026-01-15 to 2026-01-30" |
| `key_insight` | string | Main takeaway (1 sentence) | "AI influencers outperformed real creators in CTR..." |

### M3 Experience Evidence Criteria

**How experiment_pack contributes to AEO Analyzer M3 scoring**:

| Criterion | Points | experiment_pack Contribution |
|-----------|--------|------------------------------|
| Original case studies | 2 | ✅ `results` with real data → Original case study |
| First-person testing methodology | 2 | ✅ `methodology` + `sample_size` → Testing methodology |
| Personal insights/observations | 1 | ✅ `key_insight` → Personal observation |
| **Total** | **5** | **Full Experience Evidence** |

### Generated Section

**"Our Testing Approach"** section:

```markdown
## Our Testing Approach

We tested the AI Influencer + UGC Ads workflow to validate the techniques in this guide.

### Test Setup

<!-- CITABLE_BLOCK type="methodology" id="test-setup" -->
We generated 5 AI influencer videos using Alici AI for a skincare brand and ran an A/B test
against traditional creator UGC ads. Test parameters: same product, same platform (TikTok),
n=50 campaigns (25 AI, 25 traditional) from January 15-30, 2026.
<!-- /CITABLE_BLOCK -->

### Results

| Metric | AI Influencer | Traditional Creator | Improvement |
|--------|---------------|---------------------|-------------|
| Generation Time | 3 minutes | 2 hours | -97% |
| CTR | 4.2% | 1.1% | +281% |
| Cost per Video | $12 | $450 | -97% |
| Engagement Rate | 6.8% | 3.2% | +112% |

<!-- CITABLE_BLOCK type="case_study" id="test-insight" -->
**Key insight**: AI influencers outperformed real creators in CTR due to hyper-optimized
visual consistency. Human creators had natural variation in lighting/angles across videos,
while AI maintained perfect brand alignment every time.
<!-- /CITABLE_BLOCK -->
```

### Fallback: Self-Test Generation

**If `experiment_pack` not provided**:

Writer generates Self-Test placeholder:

```markdown
## Our Testing Approach

<!-- SELF_TEST_PLACEHOLDER: Replace with real testing data -->

We tested [Tool/Method] across [N] scenarios to validate the techniques in this guide:

| Test Scenario | Setup | Observation |
|---------------|-------|-------------|
| [Scenario 1] | [Configuration] | [What we observed] |
| [Scenario 2] | [Setup 2] | [Observation 2] |
| [Scenario 3] | [Setup 3] | [Observation 3] |

**Test sample**: n=[Estimated sample size]
**Date range**: [Approximate timeframe]

> **Note to editor**: This testing framework is a template. Replace with actual experimentation data before publishing for full E-E-A-T credit.

<!-- /SELF_TEST_PLACEHOLDER -->
```

**AEO Impact**:
- With `experiment_pack`: Full 5 points (real data)
- With Self-Test placeholder: Partial 2 points (structure ready, needs data)
- Without either: 0 points (no Experience Evidence)

---

## Complete Example

**Minimal Insight Pack** (required fields only):

```json
{
  "insight_pack": {
    "thesis": "AI video tools democratize cinematic content creation for small businesses",
    "why_now": "2026 model quality reached professional standards at consumer prices",
    "key_takeaways": [
      "Kling 2.0 achieves 4K photorealistic output in 3 minutes",
      "Runway Gen-4 offers best creative control for stylized content",
      "Sora 2 excels at complex camera movements"
    ]
  }
}
```

**Full Insight Pack** (all optional fields):

```json
{
  "insight_pack": {
    "thesis": "AI Influencer + UGC Ads is the most profitable combo for content creators in 2026",
    "why_now": "Market explosion ($6.06B) + tech maturity (SoulID) + cost advantage (-70%)",
    "key_takeaways": [
      "SoulID technology maintains virtual influencer character consistency",
      "170+ language global capability without real human presence",
      "UGC ad CTR improves 4x, cost reduces 70%",
      "20 posts/day scalable production capability",
      "5 monetization modes: endorsement/service/product/livestream/licensing"
    ],
    "market_data": {
      "market_size": "$6.06B (2024)",
      "cagr": "40.8% (2025-2030)",
      "key_metrics": {
        "ctr_improvement": "4x vs traditional ads",
        "cost_reduction": "70% vs traditional shooting",
        "conversion_lift": "29% conversion rate improvement"
      }
    },
    "monetization_paths": [
      {"path": "Brand Endorsement", "income_range": "$500-$50,000/post"},
      {"path": "UGC Ad Services", "income_range": "$100-$500/video"},
      {"path": "Digital Products", "income_range": "Passive income"},
      {"path": "Livestream Commerce", "income_range": "Commission split"},
      {"path": "IP Licensing", "income_range": "Annual licensing fee"}
    ],
    "competitive_sources": [
      {"source": "Higgsfield", "data_used": "SoulID tech, UGC Factory"},
      {"source": "HeyGen", "data_used": "Avatar IV, 170+ languages"},
      {"source": "Invideo", "data_used": "4x CTR, 29% conversion"}
    ],
    "content_gaps": [
      "Chinese market strategy (Douyin/XiaoHongShu/Kuaishou)",
      "Specific monetization amount cases",
      "0-to-1 launch roadmap"
    ],
    "experiment_pack": {
      "test_description": "We tested AI Influencer + UGC Ads workflow using Alici AI to generate 5 virtual influencer videos for a skincare brand",
      "methodology": "A/B test: AI influencer UGC ads vs traditional creator UGC ads, same product, same platform (TikTok)",
      "results": [
        {"metric": "Generation Time", "value": "3 minutes vs 2 hours", "delta": "-97%"},
        {"metric": "CTR", "value": "4.2% vs 1.1%", "delta": "+281%"},
        {"metric": "Cost per Video", "value": "$12 vs $450", "delta": "-97%"},
        {"metric": "Engagement Rate", "value": "6.8% vs 3.2%", "delta": "+112%"}
      ],
      "sample_size": "n=50 ad campaigns (25 AI, 25 traditional)",
      "date_range": "2026-01-15 to 2026-01-30",
      "key_insight": "AI influencers outperformed real creators in CTR due to hyper-optimized visual consistency"
    }
  }
}
```

---

## Integration with growth-topic-scout

**growth-topic-scout v2.4** (planned) will output `competitive_insights` field that can auto-populate Insight Pack:

**growth-topic-scout Output**:
```json
{
  "competitive_insights": {
    "top_competitors": ["higgsfield.ai", "heygen.com", "invideo.io"],
    "content_gaps": ["Chinese platforms", "monetization specifics"],
    "data_points": [
      {"source": "Higgsfield", "metric": "SoulID consistency"},
      {"source": "HeyGen", "metric": "170+ languages"}
    ]
  }
}
```

**Auto-conversion to Insight Pack**:
```json
{
  "insight_pack": {
    "competitive_sources": [
      {"source": "Higgsfield", "data_used": "SoulID consistency"},
      {"source": "HeyGen", "data_used": "170+ languages"}
    ],
    "content_gaps": ["Chinese platforms", "monetization specifics"]
  }
}
```

---

## Best Practices

### Do's ✅

- **Provide thesis and why_now**: These frame the entire article's narrative
- **Include key_takeaways**: These become article's core structural points
- **Add experiment_pack when available**: Real data = +5 AEO points (M3)
- **Cite competitive_sources**: Builds E-E-A-T trust chain
- **Identify content_gaps**: Enables differentiation from competitors

### Don'ts ❌

- **Don't fabricate experiment_pack data**: Use Self-Test placeholder if no real data
- **Don't skip thesis/why_now**: These are required for coherent narrative
- **Don't provide market_data without sources**: Include in competitive_sources
- **Don't over-specify monetization_paths**: 3-5 is ideal, not 10+

### Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Providing market_data without competitive_sources | No E-E-A-T attribution | Add sources to competitive_sources array |
| Too many key_takeaways (10+) | Dilutes focus | Keep to 3-5 strongest points |
| Vague income_range ("varies") | Unhelpful to readers | Use specific ranges: "$100-$500/video" |
| Missing experiment_pack when data exists | Lose 5 AEO points | Always include if you have real testing data |
| Creating fake experiment_pack | Ethics violation + credibility damage | Use Self-Test placeholder instead |

---

## Version History

### v1.1 (2026-02-05)

**Added**:
- `experiment_pack` field for Experience Evidence
- experiment_pack field definitions (6 subfields)
- M3 Experience Evidence criteria mapping
- Self-Test generation fallback documentation
- AEO Impact comparison (experiment_pack vs Self-Test vs none)

**Philosophy Change**:
> From "Competitive insights only" to "Competitive insights + Real experimentation data"

### v1.0 (2026-02-05)

**Initial Release**:
- 7 field definitions (thesis, why_now, key_takeaways, market_data, monetization_paths, competitive_sources, content_gaps)
- Minimal and Full example Insight Packs
- Integration with growth-topic-scout
- Best practices and common mistakes

---

*Schema maintained by the alici.ai Content Team*
*Last updated: 2026-02-05*
