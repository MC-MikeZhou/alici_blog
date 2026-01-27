# AEO Score Report

**Article**: How to Create AI Baby Dance Videos with Kling AI (2026 Guide)
**Type**: tutorial
**Evaluation Date**: 2026-01-21
**Target Score**: ≥75 (tutorial standard)

---

## Total Score: 82/100 ✅ PASS

| Module | Score | Weight |
|--------|-------|--------|
| M1: Content Structure & Parsability | 28/30 | 30% |
| M2: Technical Indexability | 20/25 | 25% |
| M3: Citation & E-E-A-T Signals | 16/25 | 25% |
| M4: Visibility & Measurement Design | 18/20 | 20% |

---

## Module 1: Content Structure & Parsability (28/30)

| Item | Score | Notes |
|------|-------|-------|
| 1.1 Title/H1/Description Alignment | 4/4 | ✅ Title, H1, meta_description perfectly aligned on "AI Baby Dance + Kling AI + 2026" |
| 1.2 Heading Hierarchy | 4/4 | ✅ Clean H1→H2→H3 hierarchy, logical section flow |
| 1.3 Opening Direct Answer | 4/4 | ✅ DIRECT_ANSWER block in first 50 words with step-by-step answer |
| 1.4 Q&A Format Presence | 4/4 | ✅ FAQ section with 6 topic-relevant questions |
| 1.5 List/Table Usage | 4/4 | ✅ Multiple lists + tool comparison table present |
| 1.6 Paragraph Length | 3/3 | ✅ Short paragraphs, high scannability |
| 1.7 Key Information Visibility | 3/4 | ⚠️ Tutorial progress markers use HTML comments (not visible to readers) |
| 1.8 Text-Based Facts | 2/3 | ⚠️ Most data is text-based, but some key settings in lists could be clearer |

**Strengths**:
- Excellent DIRECT_ANSWER block with specific numbers (70-80%, 60-70%, 1-5 minutes)
- Tool comparison table provides clear value
- 6 FAQs cover common user questions

**Minor Improvement**: Convert `<!-- TUTORIAL_PROGRESS -->` comments to visible progress indicators in Framer.

---

## Module 2: Technical Indexability (20/25)

| Item | Score | Notes |
|------|-------|-------|
| 2.1 Page Indexability | 4/4 | ✅ Assuming normal publication, no blocking directives |
| 2.2 Snippet Eligibility | 4/4 | ✅ Assuming no nosnippet restrictions |
| 2.3 JavaScript Rendering | 5/5 | ✅ Pure Markdown, no JS dependencies |
| 2.4 Schema Markup Presence | 2/4 | ⚠️ YAML frontmatter present but not complete Schema (missing @type, @context) |
| 2.5 Schema-Content Consistency | 2/4 | ⚠️ frontmatter consistent with content, but featured_image.url is placeholder |
| 2.6 Semantic HTML Structure | 3/4 | ⚠️ Markdown to HTML conversion needs semantic verification |

**Improvement Needed**:
1. Generate complete JSON-LD Schema during Framer conversion (HowTo schema for tutorial)
2. Fill featured_image URL before publication
3. Add HowTo schema with step markup

---

## Module 3: Citation & E-E-A-T Signals (16/25)

### Part A: Structural Signals (10/12)

| Item | Score | Notes |
|------|-------|-------|
| 3.1 Self-Contained Info Blocks | 4/4 | ✅ 5 CITABLE_BLOCK sections, each quotable independently |
| 3.2 Specific Data & Statistics | 3/4 | ✅ Good data points (70-80%, 1-5 min, 1024x1024 pixels) |
| 3.3 Source Attribution | 3/4 | ⚠️ Psychology concepts referenced but no academic citations |

### Part B: Content Depth (6/13)

| Item | Score | Notes |
|------|-------|-------|
| 3.4 Experience Evidence | 3/5 | ⚠️ "After analyzing dozens of viral videos" - good but lacks specific methodology |
| 3.5 Author Credibility | 1/4 | ❌ "Content Team" byline, no named author, generic bio |
| 3.6 Transparency & Trustworthiness | 2/4 | ⚠️ Product recommendations present but no affiliate disclosure |

**M3 is the main score gap**. Improvement suggestions:
1. **Named Author**: Change "Content Team" to named author + detailed bio (+3 points)
2. **Testing Evidence**: Add "Based on alici.ai testing, n=50 generations" (+2 points)
3. **External Sources**: Add 2-3 external citations for psychology claims (+1 point)
4. **Disclosure**: Add affiliate/sponsorship disclosure if applicable (+1 point)

---

## Module 4: Visibility & Measurement Design (18/20)

| Item | Score | Notes |
|------|-------|-------|
| 4.1 Semantic URL | 4/4 | ✅ "ai-baby-dance-tutorial-2026" - descriptive and keyword-rich |
| 4.2 Meta Description | 4/4 | ✅ Directly answers core question, mentions key tools |
| 4.3 Brand/Entity Consistency | 4/4 | ✅ "Alici", "Kling 2.6", "Motion Control" naming consistent |
| 4.4 Query Variant Coverage | 3/4 | ⚠️ Covers main queries but could add more variants ("how to make baby dance AI video") |
| 4.5 Topic-Relevant FAQ | 3/4 | ⚠️ FAQs relevant but could add "Is AI baby dance safe?" for ethics angle |

---

## Citable Blocks Identified

The following content is most likely to be cited by AI:

1. **DIRECT_ANSWER Block** (Highest Priority)
   > "To create an AI baby dance video, you need three things: Kling 2.6 Motion Control, a source dance video, and a target baby image. Upload your character image and reference motion video..."
   - Recommended Schema: Article.description + HowTo.step

2. **Contrast Effect Definition** (High Priority)
   > "The core mechanism behind AI Baby Dance is what psychologists call the contrast effect or incongruity theory of humor. When we see something that violates our expectations—like a baby performing complex adult movements—our brains experience a moment of surprise followed by delight."
   - Recommended Schema: Article.articleBody

3. **Recommended Settings** (High Priority)
   > "Recommended starting settings: Motion Intensity 70-80%, Face Preservation 60-70%, Keep original background: Yes"
   - Recommended Schema: HowTo.tool

4. **Ethical Solution** (Medium Priority)
   > "The most ethical approach is to use AI-generated baby images rather than photos of real children. This approach eliminates consent issues, creates no permanent digital footprint..."
   - Recommended Schema: Article.articleBody

5. **FAQ Answers** (High Priority for Voice Search)
   - "How much does it cost?" → Credit-based system
   - "Can I use this with pets?" → Yes, works wonderfully
   - "How long does generation take?" → 1-5 minutes

---

## Score Breakdown by Category

| Category | Current | Target | Status |
|----------|---------|--------|--------|
| Structure | 28/30 | 21/30 | ✅ Exceeds |
| Technical | 20/25 | 18/25 | ✅ Meets |
| E-E-A-T | 16/25 | 15/25 | ✅ Meets (barely) |
| Visibility | 18/20 | 14/20 | ✅ Exceeds |
| **TOTAL** | **82/100** | **≥75** | ✅ **PASS** |

---

## Next Steps

| Priority | Action | Expected Gain |
|----------|--------|---------------|
| High | Add named author + detailed bio | M3 +3 points |
| Medium | Add testing methodology note | M3 +2 points |
| Medium | Fill featured_image URL | M2 +1 point |
| Low | Add external psychology citations | M3 +1 point |
| Low | Add ethics-focused FAQ | M4 +1 point |

**If High priority improvements completed, estimated score: 85-87 points**

---

## Score Interpretation

| Score Range | Grade | Current Status |
|-------------|-------|----------------|
| 90-100 | Excellent | - |
| 75-89 | Good | ✅ **82 points - Current Position** |
| 60-74 | Fair | - |
| 40-59 | Poor | - |
| 0-39 | Critical | - |

**Conclusion**: Article AEO score of 82/100 exceeds the tutorial target (≥75), achieving "Good" grade. Main score gap is in M3 E-E-A-T section (author information and testing evidence). Article is **APPROVED FOR PUBLICATION** without requiring Auto-Improver intervention.

---

## Decision

**AEO Score: 82 ≥ 75 → PASS**

**Auto-Improver: NOT REQUIRED**

Proceed directly to Phase 5 (Framer Conversion).

---

*Generated by aeo-analyzer v2.3 | 2026-01-21*
