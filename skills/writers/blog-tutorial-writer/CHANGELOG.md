# blog-tutorial-writer Changelog

All notable changes to the Blog Tutorial Writer skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
*Last updated: 2026-01-16*
