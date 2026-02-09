---
name: image-sourcer
version: "1.0"
description: >
  Analyzes article content, searches the web for real relevant images,
  collects 10-15 candidates, scores them on 5 dimensions, and presents
  top picks for expert selection and placement.
  Triggers on: 找配图, source images, find images, 配图, image research.
allowed-tools: Read, Write, Bash, WebSearch, WebFetch, AskUserQuestion, Glob, Grep, Edit
env-required: []
---

# Image Sourcer Skill v1.0

> **Purpose**: Find real, web-sourced images for article illustration — search, score, and present top candidates for expert selection and placement.

## Trigger Conditions

- Keywords: "找配图", "source images", "find images", "配图", "image research"
- Manual invocation on any article with `![...](placeholder)` slots
- **When to use this skill vs others**:
  - **image-sourcer** → Real photos, screenshots, brand assets from the web
  - **image-generator / Editor / FAL.ai** → AI-generated illustrations, diagrams, cover art
  - **image-placeholder-filler** → Bulk fill placeholders with already-sourced URLs

---

## Architecture: 4-Phase Funnel

```
Article (with placeholder images)
       ↓
┌──────────────────────────────────────────┐
│  Phase 1: ANALYZE                        │
│  └── Extract image slots from markdown   │
│  └── Parse alt text for visual intent    │
│  └── Rank slots by hook impact           │
│  └── Select top 3 targets               │
│  └── Output: image_brief.json           │
├──────────────────────────────────────────┤
│  Phase 2: SEARCH                         │
│  └── Build search queries per slot       │
│  └── WebSearch + WebFetch for sources    │
│  └── Download candidates with curl       │
│  └── Output: candidates_raw.json        │
├──────────────────────────────────────────┤
│  Phase 3: SCORE                          │
│  └── Read each image (multimodal)        │
│  └── Score on 5 dimensions (100 pts)     │
│  └── Filter: >= 60/100 advances          │
│  └── Output: image_candidates.json      │
├──────────────────────────────────────────┤
│  Phase 4: SELECT                         │
│  └── Present top picks to user           │
│  └── User confirms final selections     │
│  └── Output: image_sourcing_report.md   │
└──────────────────────────────────────────┘
```

---

## Phase 1: ANALYZE

Extract visual needs from the article and rank by hook impact.

### Steps

1. **Read article** — Parse markdown for `![alt text](placeholder)` patterns
2. **Extract slots** — For each match, record:
   - Line number
   - Alt text (describes desired visual)
   - Surrounding context (section heading, adjacent paragraphs)
3. **Rank by hook impact** — Score each slot:
   - **Critical** (must have): Hero image, social proof visuals, comparison graphics
   - **High**: Tool screenshots, workflow diagrams
   - **Medium**: Conceptual illustrations, decorative images
4. **Select targets** — Top 3 slots by hook impact become search targets; remaining slots flagged for FAL.ai fallback

### Output: `image_brief.json`

```json
{
  "article_path": "/reports 待发文章/2026-01-27-batch-ai-influencer/01-article-edited-v2.2.md",
  "article_title": "How to Create AI Influencers in 2026",
  "total_slots": 6,
  "target_slots": 3,
  "slots": [
    {
      "id": "img-1",
      "line": 30,
      "alt_text": "Hero Image: AI influencer batch production dashboard...",
      "section": "Introduction",
      "hook_impact": "critical",
      "target": true,
      "search_priority": 2
    }
  ],
  "generated_at": "2026-01-28T..."
}
```

---

## Phase 2: SEARCH

For each target slot, run web searches and download candidate images.

### Search Strategy

1. **Build queries** — 2-4 specific queries per slot, mixing:
   - Exact entity names (e.g., "Lil Miquela Instagram official photo")
   - Descriptive terms (e.g., "AI influencer creation workflow")
   - Tool-specific (e.g., "Kling AI video interface screenshot")
2. **Execute WebSearch** — Run queries, collect result URLs
3. **Inspect sources** — Use WebFetch to verify image availability and context
4. **Download** — Use `curl` to save candidates to `candidates/` directory
   - Naming convention: `{slot-id}_{source}_{index}.{ext}` (e.g., `img-2_miquela_01.jpg`)
   - Target: 3-5 candidates per slot, 10-15 total

### Source Priority

| Priority | Source Type | Example |
|----------|-----------|---------|
| 1 | Official brand/product pages | Product screenshots, press kits |
| 2 | News outlets with CC/editorial images | TechCrunch, The Verge |
| 3 | Social media (public posts) | Instagram embeds, Twitter |
| 4 | Stock photo (free tier) | Unsplash, Pexels |

### Output: `candidates_raw.json`

```json
{
  "search_date": "2026-01-28",
  "total_candidates": 12,
  "slots": {
    "img-2": {
      "queries_run": [
        "Lil Miquela Instagram official photo",
        "Aitana Lopez AI influencer"
      ],
      "candidates": [
        {
          "filename": "img-2_miquela_01.jpg",
          "source_url": "https://...",
          "source_type": "social_media",
          "page_context": "Official Instagram profile image",
          "download_status": "success"
        }
      ]
    }
  }
}
```

---

## Phase 3: SCORE

Read each downloaded image using Claude's multimodal capability and score on 5 dimensions.

### Scoring Dimensions (100 points total)

| Dimension | Weight | Criteria |
|-----------|--------|----------|
| **Relevance** | 30 | Does the image match the alt text intent? Does it illustrate the article's point? |
| **Quality** | 25 | Resolution, clarity, professional appearance. No watermarks, compression artifacts, or cropping issues. |
| **Hook Power** | 20 | Would this image stop a reader scrolling? Visual impact, emotional resonance, curiosity trigger. |
| **Legal Safety** | 15 | Source reliability: official press kit (15), editorial use (12), CC license (10), unknown (5), clearly restricted (0). |
| **Brand Fit** | 10 | Aligns with Alici.AI visual tone: clean, modern, tech-forward. No cluttered, outdated, or off-brand aesthetics. |

### Thresholds

- **>= 75/100**: Strong candidate, advance to Phase 4 with priority
- **60-74/100**: Acceptable candidate, advance as backup
- **< 60/100**: Rejected, not shown to user

### Output: `image_candidates.json`

```json
{
  "scoring_date": "2026-01-28",
  "threshold": 60,
  "candidates": [
    {
      "filename": "img-2_miquela_01.jpg",
      "slot_id": "img-2",
      "scores": {
        "relevance": 28,
        "quality": 22,
        "hook_power": 18,
        "legal_safety": 12,
        "brand_fit": 8
      },
      "total_score": 88,
      "tier": "strong",
      "notes": "Official press image, high resolution, immediately recognizable"
    }
  ],
  "summary": {
    "total_scored": 12,
    "advanced": 8,
    "rejected": 4
  }
}
```

---

## Phase 4: SELECT

Present top candidates to user and finalize selections.

### Presentation

For each target slot, show:
1. The alt text (desired visual)
2. Top 2-3 candidates with scores and source info
3. Ask user to pick one or request more search

Use `AskUserQuestion` for selection:
- Option per candidate image (filename + score + source)
- "Search for more" option
- "Flag for AI generation" option (falls back to image-generator/FAL.ai)

### Final Output: `image_sourcing_report.md`

```markdown
# Image Sourcing Report

**Article**: How to Create AI Influencers in 2026
**Date**: 2026-01-28
**Sourced by**: image-sourcer v1.0

## Selected Images

| Slot | Line | Selected Image | Score | Source | Attribution |
|------|------|---------------|-------|--------|-------------|
| img-2 | 76 | img-2_miquela_01.jpg | 88/100 | Instagram press | Credit: @lilmiquela |
| img-1 | 30 | img-1_dashboard_02.png | 72/100 | Alici AI | Internal asset |
| img-3 | 102 | img-3_kling_01.png | 75/100 | Kling AI | Screenshot, fair use |

## Attribution Requirements

- All images require source credit in alt text or caption
- Editorial use images: add source link in article Sources section
- Screenshots: ensure fair use compliance (commentary/review context)

## Slots Not Sourced (FAL.ai Fallback Recommended)

| Slot | Line | Alt Text | Reason |
|------|------|----------|--------|
| img-4 | 150 | Variable Library diagram | Conceptual — better as AI-generated illustration |
```

---

## Output Files

```
/reports 待发文章/YYYY-MM-DD-{topic-slug}/
├── ...existing article files...
├── image_brief.json              # Phase 1 output
├── candidates_raw.json           # Phase 2 output
├── candidates/                   # Downloaded images
│   ├── img-1_dashboard_01.png
│   ├── img-2_miquela_01.jpg
│   └── ...
├── image_candidates.json         # Phase 3 scored output
└── image_sourcing_report.md      # Phase 4 final report
```

---

## Integration with Pipeline

| Image Need | Skill to Use | When |
|-----------|-------------|------|
| Real photos, screenshots, brand assets | **image-sourcer** (this skill) | Article has real-world subjects (people, products, tools) |
| AI-generated illustrations, diagrams | **image-generator** / Editor + FAL.ai | Conceptual visuals, custom diagrams, abstract concepts |
| Blog cover image | **blog-cover-generator** | After competitive-validator PASS |
| Bulk placeholder replacement | **image-placeholder-filler** | After images are sourced/generated |

---

## Error Handling

| Risk | Mitigation |
|------|-----------|
| No relevant images found for a slot | Flag slot for FAL.ai fallback in report |
| Download fails (403, timeout) | Retry once, skip with warning in candidates_raw.json |
| All candidates score < 60 for a slot | Expand search queries, try alternative terms; if still failing, flag for AI generation |
| Image has watermark | Score 0 on Quality, auto-reject |
| Copyright concern | Score low on Legal Safety; prefer official press kits and CC-licensed sources |
| Too many candidates (>20) | Pre-filter by source reliability before scoring phase |

---

## Quick Start

**Command**:
```
找配图 [path/to/01-article-edited.md]
```

**Expected Flow**:
1. Read article, extract image placeholder slots
2. Rank slots by hook impact, select top 3
3. Search web for real images matching each slot
4. Download 10-15 candidates
5. Score all candidates on 5 dimensions
6. Present top picks to user for selection
7. Generate sourcing report with attribution

---

## Changelog

**v1.0** (2026-01-28):
- Initial release
- 4-phase funnel: Analyze → Search → Score → Select
- 5-dimension scoring system (relevance/quality/hook power/legal safety/brand fit)
- WebSearch + WebFetch + curl download pipeline
- AskUserQuestion-based selection flow
- Integration table with image-generator and blog-cover-generator
