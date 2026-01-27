# Implementation Plan: Sora 2 vs Runway Gen-4.5 vs Veo 3.1 Image-to-Video Showdown

**Created**: 2026-01-22
**Project**: AliciBlog v2.73.2
**Article Type**: Tool Showdown (Extended to 12 Headings)
**Target**: 4,000-5,000 words, AEO ≥ 75

---

## Project Overview

### Article Spec
- **Title**: Sora 2 vs Runway Gen-4.5 vs Veo 3.1: Which Image-to-Video AI Wins for Professional Creators? (2026)
- **Focus**: Image-to-Video (I2V) deep evaluation
- **Target Audience**: Professional creators (film/video/social media)
- **Core Differentiator**: 8 Category Winners + Prompt Techniques comparison
- **Opening Pattern**: Pattern 4 (Reframe) - "Demos vs Production Reality"

### Structure Extension (10 → 12 Headings)
Standard Tool Showdown: 10 headings
Extended additions:
- **Heading 5**: Prompt Techniques (600 words) - NEW
- **Heading 8**: Professional Workflow Integration (400 words) - NEW

Total: 12 headings

---

## Execution Progress

### ✅ Phase 1: Setup
- [x] Create project directory: `/reports/2026-01-22-sora-vs-runway-vs-veo-i2v/`
- [x] Read template files:
  - [x] TOOL_SHOWDOWN_TEMPLATE.md
  - [x] OPENING_PATTERNS.md
  - [x] PRODUCT_CATALOG.md
  - [x] BLOG_WRITING_PRINCIPLES_v2.md
  - [x] Reference sample: 2026-01-21-ai-video-generator-comparison/01-article-v2.2-showdown.md
- [x] Create 00-implementation.md

### ⏳ Phase 2: Content Creation
- [ ] Create 00-topic-brief.json
- [ ] Write 01-article-draft.md (4,780 words target)
  - [ ] Quick Answer (180 words) + CTA #1
  - [ ] Snapshot Table (150 words)
  - [ ] How We Tested (400 words)
  - [ ] Category Winners (1,200 words, 8 categories) + CTA #2
  - [ ] **Prompt Techniques (600 words)** - NEW
  - [ ] Scorecard Table (200 words)
  - [ ] Deep Dives (900 words, 3 tools × 300)
  - [ ] **Professional Workflow Integration (400 words)** - NEW
  - [ ] Which Tool for Your Project? (400 words)
  - [ ] Quick Decision Guide (200 words)
  - [ ] Limitations & Gotchas (300 words)
  - [ ] FAQ + Final Verdict (850 words) + CTA #3

### ⏳ Phase 3: Quality Assurance
- [ ] Editor: Image generation + 4 mandatory rules check
- [ ] AEO Analyzer: Target ≥ 75 score
- [ ] Auto-Improver: If needed (<75)
- [ ] Competitive Validator: Benchmarking

### ⏳ Phase 4: Output
- [ ] Generate 07-article-final.json (Framer CMS format)

---

## Key Decisions

### Testing Dimensions (100-point scale)
| Dimension | Weight | Notes |
|-----------|--------|-------|
| Image Fidelity | 25% | Consistency with original photo |
| Motion Quality | 25% | Natural movement, physics accuracy |
| Prompt Control | 20% | Predictability, iteration efficiency |
| Production Speed | 15% | Generation time, batch capability |
| Value & Integration | 15% | Cost-effectiveness, API, workflow fit |

### 8 Category Winners
1. **Portrait Animation**: Sora 2 (physics simulation)
2. **Product Photography**: Veo 3.1 (Ingredients 3-image reference)
3. **Cinematic Camera**: Sora 2 (world state persistence)
4. **Production Speed**: Runway Gen-4.5 (45-90 sec)
5. **Audio Integration**: Veo 3.1 (native audio sync)
6. **Creative Control**: Runway Gen-4.5 (Motion Brush/masks)
7. **Vertical Video**: Veo 3.1 (native 9:16)
8. **Overall Value**: Runway / alici.ai (cost-performance / multi-model)

### CTA Strategy
| Position | Type | Content |
|----------|------|---------|
| After Quick Answer | Soft | Multi-model testing platform |
| After Category Winners | Contextual | Side-by-side comparison feature |
| Final Verdict | Strong | Immediate signup + free trial |

### Prompt Techniques Section (NEW)
Comparison table structure:
- Sora 2: Segmented format (Visual/Motion/Audio zones)
- Runway Gen-4.5: `[Camera] shot of [subject] [action] in [environment]`
- Veo 3.1: `[Cinematography] + [Subject] + [Action] + [Context] + [Style]` + 3-image ordering

---

## Files Generated

1. ✅ `00-implementation.md` - This file
2. ⏳ `00-topic-brief.json` - Metadata for writer
3. ⏳ `01-article-draft.md` - Initial draft (4,780 words)
4. ⏳ `01-article-edited.md` - Post-editor version
5. ⏳ `03-aeo-score.md` - AEO evaluation report
6. ⏳ `04-editor-report.md` - Editor findings
7. ⏳ `07-article-final.json` - Framer CMS output

---

## Next Steps

1. Create topic brief JSON with:
   - Verified tool versions (Sora 2, Runway Gen-4.5, Veo 3.1)
   - Product mapping (primary: video_studio, secondary: video_prompt)
   - Extended structure metadata (12 headings)

2. Write draft following TOOL_SHOWDOWN_TEMPLATE + 2 new sections

3. Run quality pipeline: Editor → AEO → Improver (if needed)

---

**Session State**: In progress
**Current Phase**: Phase 2 - Content Creation
**Blocking Issues**: None
