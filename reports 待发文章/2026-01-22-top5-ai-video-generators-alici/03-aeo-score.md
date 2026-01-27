# AEO Analysis Report

> **Article**: Top 5 AI Video Generator Tools on Alici: A Complete Guide (2026)
> **Date**: 2026-01-22
> **Analyzer Version**: v2.3

---

## Overall Score: 89/100 ⭐ Good

| Module | Score | Max | Percentage |
|--------|-------|-----|------------|
| M1: Content Structure & Parsability | 30 | 30 | 100% |
| M2: Technical Indexability | 21 | 25 | 84% |
| M3: Citation & E-E-A-T Signals | 19 | 25 | 76% |
| M4: Visibility & Measurement Design | 19 | 20 | 95% |
| **TOTAL** | **89** | **100** | **89%** |

**Rating**: Good - Solid foundation, minor improvements needed

---

## Module 1: Content Structure & Parsability (30/30) ✅ Perfect

| Item | Score | Assessment |
|------|-------|------------|
| 1.1 Title/H1/Description Alignment | 4/4 | ✅ Title clearly describes content, includes "Top 5 AI Video Generator" + year |
| 1.2 Heading Hierarchy | 4/4 | ✅ Clear H2/H3 structure: Tool sections → Features → Limitations |
| 1.3 Opening Direct Answer | 4/4 | ✅ First 50 words answer "which to pick" with specific recommendations |
| 1.4 Q&A Format Presence | 4/4 | ✅ Dedicated FAQ section with 8 topic-relevant questions |
| 1.5 List/Table Usage | 4/4 | ✅ Comparison table + bullet lists for features + numbered methodology |
| 1.6 Paragraph Length | 3/3 | ✅ Short paragraphs throughout, high scannability |
| 1.7 Key Information Visibility | 4/4 | ✅ All content visible, no accordions/tabs |
| 1.8 Text-Based Facts | 3/3 | ✅ All data in text format (1,247 Elo, 195%, 4K specs) |

**AEO Expert Insight**: This article has exceptional structural AEO. The direct answer opening, comparison table, and FAQ section make it highly extractable for AI answer engines.

---

## Module 2: Technical Indexability (21/25) ⚠️ Minor Gaps

| Item | Score | Assessment |
|------|-------|------------|
| 2.1 Page Indexability | 4/4 | ✅ No blocking directives expected |
| 2.2 Snippet Eligibility | 4/4 | ✅ Content qualifies for rich snippets |
| 2.3 JavaScript Rendering | 5/5 | ✅ Static content, no JS dependencies |
| 2.4 Schema Markup Presence | 2/4 | ⚠️ No Schema in markdown (needs Framer implementation) |
| 2.5 Schema-Content Consistency | 2/4 | ⚠️ N/A until Schema added |
| 2.6 Semantic HTML Structure | 4/4 | ✅ Markdown generates proper semantic HTML |

**Action Required**: Add Article Schema + FAQ Schema when converting to Framer. Expected to gain +4 points.

---

## Module 3: Citation & E-E-A-T Signals (19/25) ⚠️ Content Depth Gaps

### Part A: Structural Signals (12/12) ✅ Perfect

| Item | Score | Assessment |
|------|-------|------------|
| 3.1 Self-Contained Blocks | 4/4 | ✅ Conclusions are quotable ("Kling 2.6 offers the easiest learning curve") |
| 3.2 Specific Data & Statistics | 4/4 | ✅ Multiple data points: 1,247 Elo, 195% improvement, 4K resolution, 25 sec |
| 3.3 Source Attribution | 4/4 | ✅ 5 official sources (OpenAI, Runway, Google, Kuaishou, Alibaba) |

### Part B: Content Depth (7/13) ⚠️ Needs Improvement

| Item | Score | Assessment |
|------|-------|------------|
| 3.4 Experience Evidence | 3/5 | ⚠️ Claims "50+ test videos" but no specific case studies shown |
| 3.5 Author Credibility | 1/4 | ❌ No named author - uses implicit team attribution |
| 3.6 Transparency | 3/4 | ⚠️ Sources cited, but Alici relationship not explicitly disclosed |

**Critical Gap**: The article claims testing methodology but doesn't demonstrate it with specific examples. No named author reduces credibility signal.

**Recommendations**:
1. Add named author with verifiable background
2. Add 1-2 specific test case examples (prompt + result + what we learned)
3. Add explicit disclosure: "Alici is our product. We tested all models on our platform."
4. Add methodology specifics: "n=50 videos, 10 prompts × 5 models"

---

## Module 4: Visibility & Measurement Design (19/20) ✅ Excellent

| Item | Score | Assessment |
|------|-------|------------|
| 4.1 Semantic URL | 4/4 | ✅ Slug: top-5-ai-video-generators-alici-2026 (descriptive, 7 words) |
| 4.2 Meta Description | 3/4 | ⚠️ Implied from opening but needs explicit meta |
| 4.3 Brand Consistency | 4/4 | ✅ "Alici" used consistently throughout |
| 4.4 Query Variant Coverage | 4/4 | ✅ Covers: "best AI video", "which model", "compare", "2026" |
| 4.5 Topic-Relevant FAQ | 4/4 | ✅ 8 questions directly address AI video tool selection |

---

## Citable Blocks Identified

These content pieces are most likely to be quoted by AI answer engines:

| Block | Content | Recommended Schema |
|-------|---------|-------------------|
| **Direct Answer** | "If you're new to AI video generation, start with Kling 2.6..." | HowTo step 1 |
| **Kling Speed Claim** | "195% quality improvement over previous versions" | StatisticalData |
| **Veo 4K Claim** | "first mainstream AI video generator to output true 4K" | Product feature |
| **Comparison Table** | Full 8-row comparison | Table Schema |
| **FAQ Answers** | 8 self-contained answers | FAQPage Schema |

---

## Priority Recommendations

### High Priority (Expected: +6 points)

1. **Add Named Author** (3.5: +3 points)
   - Add author YAML with name, role, company, background
   - Link to verifiable profile (LinkedIn/Twitter)
   - Example: "Hans Chen, CEO of Alici.ai, tested 10,000+ AI video prompts"

2. **Add Explicit Disclosure** (3.6: +1 point)
   ```markdown
   > **Disclosure**: Alici.ai is our product. All tests were conducted on our platform
   > to ensure fair comparison across models. (January 2026, n=50 videos)
   ```

3. **Add Schema in Framer** (2.4: +2 points)
   - Article Schema with author, datePublished, dateModified
   - FAQPage Schema for 8 questions

### Medium Priority (Expected: +2 points)

4. **Add Testing Evidence** (3.4: +2 points)
   - Add 1-2 side-by-side comparison screenshots
   - Include specific prompt that was tested
   - Show results from 2+ models

5. **Add Meta Description** (4.2: +1 point)
   ```
   Compare Sora 2, Runway Gen 4.5, Veo 3.1, Kling 2.6, and Wan 2.6 — the top 5 AI
   video generators of 2026. Find which is best for your use case, all on Alici.
   ```

---

## Score Projection After Improvements

| Scenario | Score | Change |
|----------|-------|--------|
| Current | 89 | - |
| After High Priority | 95 | +6 |
| After All Recommendations | 97 | +8 |

---

## Conclusion

**Current Status**: This article scores 89/100, which is "Good" and **publishable**. It has excellent structural AEO (M1 perfect) and strong visibility design (M4 near-perfect).

**Main Weakness**: Content depth signals in M3. The article claims expertise but doesn't demonstrate it with specific testing evidence or named authorship.

**Recommendation**: Publish with the understanding that E-E-A-T improvements should be made post-launch if the article is intended for high-competition keywords.

---

*AEO Analyzer v2.3 | Evaluation Framework: 4 Modules, 100 Points*
