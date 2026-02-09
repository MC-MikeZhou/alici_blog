# blog-tutorial-writer Changelog

All notable changes to the Blog Tutorial Writer skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [3.0] - 2026-02-05

### Added

**Tier Structure System (v3.0 NEW)** ⭐
- Three-tier classification system based on tutorial complexity:
  - **Tier 1** (1,800-2,200 words): Single-tool/feature tutorials (e.g., "How to use Kling Motion Control")
  - **Tier 2** (2,200-2,800 words): Workflow/multi-step tutorials with Prerequisites Check and Troubleshooting
  - **Tier 3** (2,800-3,500 words): Complex/composite tutorials with Market Context and Monetization Framework
- Tier Selection Logic:
  - Tier 1: `simple_single_tool AND no_monetization_keywords`
  - Tier 2: `workflow OR multi_step_process`
  - Tier 3: `market_context_exists OR monetization_keywords OR composite_topic`
- Conditional sections by Tier (Prerequisites Check, Workflow Selector, Market Context, Monetization Framework)
- Total Word Count Formula by Tier clearly defined

**Prerequisites Check Section (v3.0 NEW)**
- Trigger: Tier 2 or Tier 3 tutorials
- Position: After Market Context (if exists) or after Background, before Main Steps
- Content structure:
  - Requirements table with ✅ Required / ⭕ Helpful status
  - Tool/Account/Skill/Hardware requirements
  - Quick tip for alternatives
- Word count: 50-80 words
- Purpose: Set clear expectations before readers begin tutorial

**Workflow Selector Section (v3.0 NEW)**
- Trigger: Multi-path tutorials (Tier 2/3) with different workflows
- Position: After Prerequisites Check, before Main Steps
- Content structure:
  - "Choose Your Path: [N] Workflows Compared" heading
  - Comparison table: Goal → Workflow → Time → Difficulty → Jump Link
  - Recommendation for beginners
- Word count: 80-120 words
- Purpose: Help readers choose right workflow (inspired by InVideo UX)

**Troubleshooting Table (v3.0 NEW - Replaces "Common Mistakes")**
- Trigger: All Tiers (mandatory)
- Format: Table with Symptom → Likely Cause → Fix columns
- Content: 5+ common issues with actionable solutions
- Word count: 100-150 words
- Advantages over old format:
  - ✅ Faster to scan (table vs prose)
  - ✅ More actionable ("Fix" column)
  - ✅ Better for mobile readers
  - ✅ Easier to maintain and update

**Citable Block Taxonomy (v3.0 UPGRADED)** ⭐
- Added `type` attribute to Citable Blocks with 7 taxonomy types:
  - `definition` (terminology definitions) - AEO Weight: High
  - `statistic` (data points, metrics) - AEO Weight: High
  - `comparison` (tool/method comparisons) - AEO Weight: Medium
  - `recommendation` (best practice advice) - AEO Weight: Medium
  - `methodology` (testing/research methods) - AEO Weight: High
  - `case_study` (real-world examples) - AEO Weight: High
  - `key_takeaway` (core lesson/insight) - AEO Weight: High
- Added `id` attribute for unique identification and cross-referencing
- Increased minimum from 3-5 to 5-7 Citable Blocks per article
- Type diversity requirement: ≥3 different types per article
- Format: `<!-- CITABLE_BLOCK type="[type]" id="[unique-id]" -->`

**IMAGE_PLACEHOLDER v2.0 (v3.0 UPGRADED)** ⭐
- Structured metadata format for automation-friendly image generation
- New attributes:
  - `id` (required): Unique identifier (kebab-case)
  - `type` (required): screenshot | diagram | comparison | hero
  - `priority` (required): required | recommended | optional
  - `alt` (required): Descriptive text for SEO + accessibility
  - `where` (required): Position description
  - `context` (optional): What user is doing (improves prompt generation)
  - `size_hint` (optional): Dimensions (WxH) for aspect ratio guidance
- Type definitions for generation strategy
- Priority guidelines for Editor prioritization

**CTA_CARD v2.0 - Friction-Aligned Placement (v3.0 UPGRADED)** ⭐
- Philosophy shift: CTAs at friction points, not arbitrary positions
- Friction-Aligned Strategy:
  - `friction_point` trigger: After complex workflows (user feels overwhelmed)
  - `achievement` trigger: After completing milestones (user ready for next step)
  - `decision` trigger: Before tool choices (user needs guidance)
- New attributes:
  - `position`: Physical placement (after-step-N, after-troubleshooting, end)
  - `trigger`: Why CTA appears here (friction_point, achievement, decision)
  - `friction_context` (required): User's mental state (50-100 words)
  - `product`: Which product to promote
  - `cta_type`: Action type (try_free, learn_more, see_pricing)
- 4 templates: Friction Point, Achievement, Decision Point, Closing (mandatory)

**experiment_pack Field (v3.0 NEW - Experience Evidence)** ⭐
- New optional field in Insight Pack for real testing data
- Structure:
  - `test_description`: What you tested (1-2 sentences)
  - `methodology`: How you tested (control vs treatment)
  - `results[]`: Array of metric objects (metric, value, delta)
  - `sample_size`: n=X notation
  - `date_range`: YYYY-MM-DD to YYYY-MM-DD
  - `key_insight`: Main takeaway (1 sentence)
- Purpose: Achieve M3 Experience Evidence scoring (5 points in AEO Analyzer)
- Contributes to:
  - Testing methodology (2 points)
  - Original case study (2 points)
  - Personal observation (1 point)

**Self-Test Generation Fallback (v3.0 NEW)**
- Trigger: When `experiment_pack` not provided
- Purpose: Generate testing framework placeholders for E-E-A-T structure
- Behavior:
  1. Detect tools mentioned in tutorial
  2. Generate simulated test structure
  3. Add `<!-- SELF_TEST_PLACEHOLDER -->` marker for replacement
- Template includes: Test scenarios table, sample size, date range
- AEO Impact:
  - With experiment_pack: Full 5 points (real data)
  - With Self-Test placeholder: Partial 2 points (structure ready)
  - Without either: 0 points (no Experience Evidence)

**Writer Self-Check Report (v3.0 NEW)** ⭐
- Mandatory output: `01-article-draft.json` alongside `01-article-draft.md`
- JSON Schema includes:
  - `meta`: version, tier, word_count, generated_at, skill_version
  - `aeo_pre_check`: estimated_score, citable_blocks, citable_block_types, experience_evidence, faq_count
  - `tier_compliance`: tier_detected, tier_justification, word_count_in_range, conditional_sections_correct
  - `sections`: boolean flags for all conditional sections
  - `images[]`: All IMAGE_PLACEHOLDER v2.0 entries
  - `ctas[]`: All CTA_CARD v2.0 entries
  - `validation`: PASS/FAIL for each validation check
  - `warnings[]`: Non-blocking issues
- Purpose: Structured metadata for quality verification, automation, and debugging
- Benefits:
  - Editor can quick-validate before processing
  - AEO Analyzer can use pre-populated data
  - User can audit Tier selection and warnings
  - Debugging is faster with structured output

### Changed

**Word Count Targets**
- Base Article (Tier 1): 2,000-2,100 → 2,280 words (fixed Conclusion+FAQ budget: 50 → 280)
- Tier 2: 2,200-2,800 words (new)
- Tier 3: 2,800-3,500 → 3,050 words (fixed Conclusion+FAQ budget)
- Conclusion + CTA: 120-150 words (was bundled with FAQ)
- FAQ: 150-300 words (5 questions × 40-60 words each) (was bundled with Conclusion)

**Article Description**
- Updated structure notation to include Tier-based conditional sections
- Updated from "v2.5 upgrades: Insight Pack input + Market Context section + Monetization Framework"
- To "v3.0 upgrades: Tier structure + Modular sections + Schema v2.0 + Experience Evidence + Self-Check Report"

**Section Numbering**
- Added Step 3.6: Add Prerequisites Check Section (conditional)
- Added Step 3.7: Add Workflow Selector Section (conditional)
- Replaced Step 5 "Common Mistakes" with "Troubleshooting Table"

**AEO Checklist**
- Added v3.0 sections (5 new sections, 20+ new checkpoints):
  - Tier Compliance (3 checkpoints)
  - Modular Sections (3 checkpoints)
  - Schema Compliance (6 checkpoints)
  - Experience Evidence (4 checkpoints)
  - Self-Check JSON Output (4 checkpoints)
- Total checklist items: 30 (v2.5) → 50+ (v3.0)

**Updated File References**
- version: "2.5" → "3.0"
- updated: "2026-02-05" (same date as v2.5, released together)

### Fixed

**Word Budget Contradiction (Critical Bug)**
- **Problem**: v2.5 word budget table showed "Conclusion + FAQ | 50 | 2%" which is mathematically impossible
- **Root Cause**:
  - Conclusion + CTA actually needs 120-150 words (summary + key takeaways + CTA)
  - FAQ actually needs 150-300 words (5 questions × 40-60 words each)
  - Combined: 270-450 words, not 50
- **Impact**: Writers were confused by contradictory guidance
- **v3.0 Solution**:
  - Split into two separate rows: "Conclusion + CTA | 130 | 6%" and "FAQ | 150 | 6%"
  - Base article total: 2,000-2,100 → 2,280 words
  - Tier 3 total: 2,800-3,000 → 3,050 words

**Tier-less Architecture Limitation**
- **Problem**: v2.5 lacked clear word count guidance for different tutorial complexities
  - Simple tutorials forced to hit 2,000+ words with filler content
  - Complex tutorials capped at 2,500 words, insufficient for composite topics
- **Root Cause**: One-size-fits-all approach (2,000-2,500 words for all tutorials)
- **v3.0 Solution**: Three-tier system with appropriate word ranges:
  - Tier 1: 1,800-2,200 (simple tutorials can be shorter)
  - Tier 2: 2,200-2,800 (workflow tutorials have space for Prerequisites + Troubleshooting)
  - Tier 3: 2,800-3,500 (complex tutorials get full Market Context + Monetization Framework)

**AEO Scoring Ceiling**
- **Problem**: v2.5 articles consistently scored 80-85, rarely reaching ≥85
- **Root Causes**:
  - M3 Experience Evidence: Only metadata checks, no real testing data (missing 5 points)
  - Citable Blocks: No type taxonomy, hard for AEO Analyzer to weight appropriately
  - CTA placement: Fixed positions, not friction-aligned (lower conversion)
- **v3.0 Solution**:
  - experiment_pack provides real testing data → +5 points (M3)
  - Citable Block taxonomy (7 types with AEO weights) → +2-3 points (M2)
  - Friction-aligned CTAs → Better user experience, indirect AEO benefit
- **Expected Impact**: First-pass AEO score 80-85 → ≥85-90 stable

**Large Tutorial Usability**
- **Problem**: v2.5 had no mechanism to help readers navigate complex, multi-path tutorials
- **Root Cause**: Linear tutorial structure assumed one workflow for all readers
- **v3.0 Solution**:
  - Prerequisites Check sets expectations upfront
  - Workflow Selector helps readers choose right path (InVideo-inspired)
  - Troubleshooting Table is faster to scan than prose format

### Philosophy Change

> **From**: "One-size-fits-all 2,000-2,500 word tutorials"
>
> **To**: "Tier-based modular tutorials with conditional sections based on complexity"

**Rationale**:
- Different tutorial types need different structures:
  - Simple = concise and focused (Tier 1)
  - Workflow = Prerequisites + clear paths (Tier 2)
  - Composite = Market Context + Monetization (Tier 3)
- Schema standardization (v2.0 formats) enables automation
- Experience Evidence (experiment_pack) elevates E-E-A-T from "structural signals" to "real expertise"
- Friction-aligned CTAs reflect modern UX thinking (help when needed, not arbitrary placement)

### New Dependencies

**Shared Documentation**
- Updated `/skills/_docs/INSIGHT_PACK_SCHEMA.md` (v1.0 → v1.1)
  - Added `experiment_pack` field definition
  - Added experiment_pack examples
  - Added Self-Test fallback documentation

**No New External Dependencies**
- v3.0 is backward compatible with all existing workflow tools
- JSON output (`01-article-draft.json`) is additive, doesn't break existing pipeline

### Quality Impact Projection

| Metric | v2.5 | v3.0 | Improvement |
|--------|------|------|-------------|
| **First-pass AEO score** | ~80-85 | **≥85-90** | +5-10 points |
| **Tier match accuracy** | N/A (no Tier system) | **100%** (automated selection) | Major |
| **Experience Evidence (M3)** | Partial (2/5 points) | **Full (5/5 points)** | +3 points |
| **Citable Blocks** | 5 (no type) | **5-7 (typed)** | +2 blocks + taxonomy |
| **CTA contextual relevance** | Low (fixed positions) | **High (friction-aligned)** | Major UX improvement |
| **Large tutorial usability** | Low (linear only) | **High (Workflow Selector)** | Major |
| **Self-validation capability** | None | **Full (JSON output)** | New capability |

### Backward Compatibility

**Output Format**
- `01-article-draft.md` format unchanged (YAML + Markdown)
- `01-article-draft.json` is new additive output (doesn't break existing tools)
- All HTML comment markers (`<!-- CITABLE_BLOCK -->`, `<!-- CTA_CARD -->`) are invisible in final render

**Workflow Integration**
- v3.0 articles compatible with all existing tools:
  - editor (will handle v2.0 Schema formats)
  - aeo-analyzer (will score v3.0 features)
  - auto-improver (works with v3.0 structure)
  - markdown-to-framer (unchanged export format)

**Insight Pack**
- v2.5 Insight Packs without `experiment_pack` still work (Self-Test fallback activates)
- All v2.5 fields remain supported

### Breaking Changes

**None** - v3.0 is fully backward compatible

**Optional Upgrade Path**:
1. Start using Tier system (automatic Tier detection)
2. Add experiment_pack to Insight Packs (for full Experience Evidence)
3. Use v2.0 Schema formats (Citable Block type, IMAGE_PLACEHOLDER attributes, CTA_CARD friction context)
4. Review JSON output (`01-article-draft.json`) for self-validation

---

## [2.5] - 2026-02-05

### Added

**Insight Pack Input Mechanism (v2.5 NEW)**
- New optional input: `insight_pack` JSON object
- Supported fields:
  - `thesis` (required): Core argument (1 sentence)
  - `why_now` (required): Why write this topic now
  - `key_takeaways` (required): 3-5 key points
  - `market_data` (optional): Market size, CAGR, key metrics - triggers Market Context section
  - `monetization_paths` (optional): Revenue streams - triggers Monetization Framework
  - `competitive_sources` (optional): Data source citations for E-E-A-T
  - `content_gaps` (optional): Competitor content gaps for differentiation
- Purpose: Structured transfer of competitive analysis data to Writer
- Backward compatible: Articles without Insight Pack use default behavior

**Market Context Section (v2.5 NEW - Conditional)**
- Trigger condition: `insight_pack.market_data` exists
- Position: After Background section, before Main Steps
- Content structure:
  - "Why [Topic] Is Exploding Right Now" heading
  - Market Opportunity subsection (with Citable Block)
  - Key Performance Metrics comparison table (traditional vs AI)
  - "What This Means for You" personalized value proposition
- Word count: 200-300 words
- Citable Block requirement: ≥1 (market data)

**Monetization Framework Section (v2.5 NEW - Conditional)**
- Trigger conditions:
  - `primary_keyword` contains: "make money", "earn", "赚钱", "变现", "income", "monetize" OR
  - `insight_pack.monetization_paths` exists
- Position: After Pro Tips, before Conclusion
- Content structure:
  - "How to Make Money with [Topic]: [N] Revenue Streams" heading
  - 3-5 revenue streams with structure:
    - What it is (brief explanation)
    - Income potential (income range)
    - How to start (3-step guide)
    - Pro tip (advanced advice)
  - Income Projection subsection with Citable Block
  - 12-month income milestone table
- Word count: 400-600 words
- Citable Block requirement: ≥1 (income projection)

**AEO Checklist Extensions**
- New section: Insight Pack Integration (5 checkpoints)
- New section: Market Context Section validation (4 checkpoints)
- New section: Monetization Framework validation (4 checkpoints)
- Total new checkpoints: +13

### Changed

**Article Description**
- Updated from "Input: Topic Brief from growth-topic-scout. Optional: previous_version for inheritance."
- To "Input: Topic Brief from growth-topic-scout. Optional: previous_version for inheritance, insight_pack for competitive data."
- Updated structure notation to include conditional sections: "[Market Context (conditional)] → Steps → [Monetization Framework (conditional)]"

**Word Count Targets**
- Base article (no conditional sections): 2,000-2,100 words
- With Market Context + Monetization Framework: 2,800-3,000 words
- Articles with Insight Pack and monetization focus will be 40% longer than standard tutorials

**Section Numbering**
- Added Step 3.5: Write Market Context Section (conditional)
- Added Step 6.5: Write Monetization Framework (conditional)
- Mandatory Sections list updated from 8 to 11 items (with 3 conditional)

**Updated File References**
- version: "2.4" → "2.5"
- updated: "2026-01-20" → "2026-02-05"

### Fixed

**Complex/Composite Topic Handling**
- **Problem**: v2.4 designed for single-topic tutorials; complex topics (e.g., "AI Influencer + UGC Ads + Monetization") lacked structure for:
  - Market data integration
  - Monetization pathway frameworks
  - Competitive insights structured transfer
- **Root Causes Identified**:
  - Topic Brief assumed single primary_keyword, composite topics needed manual data integration
  - No dedicated framework for "How to Make Money" tutorials
  - Competitive analysis data couldn't be passed structurally
  - Market opportunity context was buried in Background section
- **v2.5 Solution**:
  - Insight Pack provides structured competitive data input
  - Market Context section surfaces market opportunity upfront
  - Monetization Framework dedicates 400-600 words to revenue paths
  - content_gaps field guides differentiation strategy

**Data-Driven Article Quality**
- **Problem**: Articles without competitive research lacked authoritative data backing
- **v2.5 Solution**: Insight Pack's competitive_sources field ensures all data points have citations
- **Expected Impact**: First-pass AEO score improvement of +10-15 points (from ~70 to ~80-85) due to:
  - Complete data sourcing (competitive_sources → citations)
  - Structured market data (Market Context Citable Block)
  - Revenue projections with industry benchmarks (Monetization Citable Block)

### Philosophy Change

> **From**: "Single-topic tutorials focused on 'how to do X'"
>
> **To**: "Support composite monetization-oriented topics with structured competitive insights"

**Rationale**:
- Content landscape shifts toward revenue-focused tutorials (e.g., "How to become [X] and make money")
- Competitive analysis data exists but couldn't be structured into articles
- Market Context needed dedicated space (not buried in Background)
- Monetization pathways deserve systematic framework (not scattered mentions)

### New Dependencies

**Shared Documentation**
- Created `/skills/_docs/INSIGHT_PACK_SCHEMA.md` (v1.0)
  - JSON Schema definition
  - Usage examples (minimal vs full)
  - Field descriptions and best practices
  - Relationship with Topic Brief

**Updated Integration**
- growth-topic-scout v2.4 (planned): Will output `competitive_insights` field to auto-populate Insight Pack

### Quality Impact Projection

| Metric | v2.4 (without Insight Pack) | v2.5 (with Insight Pack) | Improvement |
|--------|----------------------------|--------------------------|-------------|
| **First-pass AEO score** | ~70 | ~80-85 | +10-15 points |
| **E-E-A-T signals** | Weak (missing data sources) | Strong (complete citations) | Major |
| **Differentiation degree** | Low (topic-driven) | High (content_gaps-driven) | Major |
| **Monetization pathway clarity** | Scattered mentions | Structured framework | Major |
| **Article length** | 2,000-2,500 words | 2,800-3,000 words | +800 words |

### Example Use Case

**Scenario**: "How to Become an AI Influencer and Make Money with UGC Ads"

**v2.4 Approach** (without Insight Pack):
- Single Topic Brief with primary_keyword
- Market data manually inserted in Background section
- Monetization mentioned in Conclusion CTA
- Competitive insights not structured

**v2.5 Approach** (with Insight Pack):
```json
{
  "insight_pack": {
    "thesis": "AI Influencer + UGC Ads is the most profitable combo for 2026",
    "why_now": "Market explosion ($6.06B) + tech maturity (SoulID) + cost advantage (-70%)",
    "market_data": {
      "market_size": "$6.06B (2024)",
      "cagr": "40.8%",
      "key_metrics": {"ctr_improvement": "4x", "cost_reduction": "70%"}
    },
    "monetization_paths": [
      {"path": "Brand Endorsement", "income_range": "$500-$50,000/post"},
      {"path": "UGC Ad Services", "income_range": "$100-$500/video"}
    ],
    "competitive_sources": [
      {"source": "Higgsfield", "data_used": "SoulID tech"},
      {"source": "HeyGen", "data_used": "170+ languages"}
    ],
    "content_gaps": ["Chinese market strategy", "0-to-1 launch roadmap"]
  }
}
```

**Result**:
- Market Context section with $6.06B market size Citable Block
- Monetization Framework with 5 revenue streams + 12-month projection
- All competitive_sources cited in article
- content_gaps addressed: Chinese platforms subsection, 0-to-1 launch steps

---

## [2.0] - 2026-01-16

### Added

**AIDA Opening Framework**
- Introduced AIDA (Attention → Interest → Desire → Action) structure for article openings
- Opening word count increased from 40-60 words to 80-120 words
- Added `<!-- AIDA_OPENING -->` and `<!-- END_AIDA_OPENING -->` comment markers
- Four distinct components:
  - **Attention** (40-60 words): Direct answer to title question
  - **Interest** (20-30 words): Pain point recognition
  - **Desire** (20-30 words): Value promise
  - **Action** (10-20 words): Navigation hint with quick jump link

**Citable Block Marking System (v2.0 NEW)**
- Added `<!-- CITABLE_BLOCK: Label -->` ... `<!-- /CITABLE_BLOCK -->` format
- Requirement: 3-5 Citable Blocks per article minimum
- Distribution mandate: 1 in opening/background, 2-3 in main steps, 1 in tips/conclusion
- Block specifications: 40-80 words, independently understandable, data-driven
- Purpose: Optimize for AI answer engine extraction and citation

**Enhanced AEO Checklist**
- Added 7 checkpoints for AIDA opening verification
- Added 8 checkpoints for Citable Block verification
- Expanded E-E-A-T checklist to include citation source quality requirements
- Total checklist items increased from 15 to 30

**Version Tracking**
- Added explicit `version: "2.0"` field in YAML frontmatter
- Added `updated: "2026-01-16"` field
- Added `changelog: See CHANGELOG.md for version history` reference
- This CHANGELOG.md file created to track all version changes

### Changed

**Opening Structure**
- Replaced simple "direct answer + introduction" with structured AIDA framework
- Opening must now include pain point recognition and navigation hint
- Direct answer remains but is now the "Attention" component of AIDA

**Article Description**
- Updated from "Generate SEO/AEO-optimized Tutorial articles (1,800-2,500 words)"
- To "Generate SEO/AEO-optimized Tutorial articles (1,800-2,500 words) with AIDA opening framework and AI citation optimization"
- Updated structure notation from "Introduction → Background → Steps" to "AIDA Opening → Background → Steps"

**AEO Optimization Strategy**
- Shifted from "post-write optimization" to "embedded optimization during writing"
- Citable Blocks are now written during content creation, not added afterward
- AIDA framework embeds direct answers upfront, reducing need for post-edit improvements

**Step Numbering**
- Added new "Step 4.5: Add Citable Blocks" between tutorial steps and common mistakes
- Existing steps renumbered accordingly (Step 5 → Write Common Mistakes, etc.)

### Fixed

**First-Pass AEO Score Issue**
- **Problem**: v1.0 articles typically scored 65-70 on first AEO pass, requiring 1-2 auto-improver iterations
- **Root Causes Identified**:
  - Openings lacked engagement (just direct answer, no hook)
  - No AI-extraction-optimized content markers
  - Source citations often insufficient (< 3)
  - E-E-A-T signals incomplete
- **v2.0 Solution**:
  - AIDA opening provides both direct answer AND engagement
  - Citable Blocks mark quotable content for AI engines
  - E-E-A-T checklist enforces 3-5 external citations
  - Target: First-pass AEO score ≥ 75 (no improvement loop needed)

**AI Citation Rate Issue**
- **Problem**: v1.0 articles had low AI answer engine citation probability
- **Root Cause**: Content lacked clear extraction anchors for AI systems
- **v2.0 Solution**: Citable Blocks provide semantic anchors with:
  - Standalone quotable statements
  - Data-driven conclusions
  - Clear attribution-ready content
  - Independent context (no surrounding text needed)

### Evaluation Plan

**Baseline Article for Testing**:
- Article: `/reports/2025-01-15-viral-ai-videos/05-article-v2.md`
- Title: "How to Create Viral AI Videos: Sora 2, Kling & Runway Complete Guide"
- Type: Tutorial
- v1.0 AEO Score: 73/100 (Fair)
- v1.0 Weaknesses:
  - M2: Technical Indexability 15/25 (60%)
  - M3: E-E-A-T 10/25 (40%) — missing author info (-7), source citations (-3)

**v2.0 Target Metrics**:
- First-pass AEO score: ≥ 75/100 (vs v1.0's 73)
- Citable Blocks: ≥ 5 (vs v1.0's 0)
- E-E-A-T module: ≥ 18/25 (vs v1.0's 10/25)
- Auto-improver iterations: 0 (vs v1.0's 1-2)

**Testing Methodology**:
1. Use identical Topic Brief as baseline article
2. Generate new article with v2.0 framework
3. Run AEO analyzer on both versions
4. Compare scores across 4 modules
5. Count Citable Blocks and verify placement
6. Test Framer export compatibility

---

## [1.0] - 2025-XX-XX (Implicit Version)

### Initial Release

**Core Features**:
- Tutorial article structure: Introduction → Background → Steps → Mistakes → Tips → Conclusion → FAQ
- Word count target: 1,800-2,500 words
- Direct answer opening (40-60 words)
- 5-7 step tutorial format
- Common mistakes section (3-5 items)
- Pro tips section (3-5 items)
- FAQ section (3-5 questions)
- SEO keyword integration
- Framer CMS export compatibility

**Workflow Integration**:
- Input: Topic Brief from growth-topic-scout
- Output: Markdown article with YAML frontmatter
- Compatible with: chinese-previewer, aeo-analyzer, auto-improver, markdown-to-framer

**AEO Optimization (v1.0)**:
- Direct answer in first 50 words
- FAQ with standalone answers
- Independently meaningful step titles
- Paragraph length ≤ 3 sentences
- E-E-A-T fields in frontmatter

**Known Limitations**:
- No explicit version tracking
- Openings lacked engagement hooks
- No AI-extraction optimization markers
- First-pass AEO scores typically 65-70
- Required 1-2 auto-improver iterations to reach 75+

---

## Future Roadmap

### [2.1] - Planned
- PAA (People Also Ask) integration for FAQ generation
- Dynamic FAQ sourcing from DataForSEO
- External reference validation (link checking)

### [3.0] - Planned
- Multi-model comparison sections
- Interactive code snippets
- Video/audio placeholder support
- Schema Markup auto-generation

---

## Version Upgrade Guidelines

**When to bump versions**:
- **Major (X.0)**: Breaking changes to output format, workflow integration, or skill interface
- **Minor (x.Y)**: New features, enhanced frameworks, additional requirements
- **Patch (x.y.Z)**: Bug fixes, typo corrections, documentation updates

**Backward Compatibility**:
- v2.0 articles are forward-compatible with all existing workflow tools
- Framer export format unchanged (YAML frontmatter + Markdown body)
- AEO analyzer compatible with v1.0 and v2.0 articles
- New HTML comment markers (`<!-- AIDA_OPENING -->`, `<!-- CITABLE_BLOCK -->`) are invisible in final render

---

*Changelog maintained by the alici.ai Content Team*
*Last updated: 2026-02-05*
