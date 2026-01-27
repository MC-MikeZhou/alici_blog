# AEO Analysis Report: AI Video Generator Showdown v2.2

**Article**: `01-article-v2.2-showdown.md`
**Analysis Date**: 2026-01-21
**Framework Version**: AEO Evaluation Framework v2.3

---

## Overall Score: 88/100 (Good)

| Module | Score | Max | Percentage |
|--------|-------|-----|------------|
| M1: Content Structure & Parsability | 30 | 30 | 100% |
| M2: Technical Indexability | 23 | 25 | 92% |
| M3: Citation & E-E-A-T Signals | 16 | 25 | 64% |
| M4: Visibility & Measurement Design | 19 | 20 | 95% |
| **Total** | **88** | **100** | **88%** |

**Rating**: Good - Solid foundation, minor improvements needed

---

## Module 1: Content Structure & Parsability (30/30)

| Criterion | Score | Notes |
|-----------|-------|-------|
| 1.1 Title/H1/Description Alignment | 4/4 | ✅ All three aligned, clear keywords |
| 1.2 Heading Hierarchy | 4/4 | ✅ Clear H2/H3 structure, 14 sections |
| 1.3 Opening Direct Answer | 4/4 | ✅ "Sora 2 delivers the most realistic results" in first 50 words |
| 1.4 Q&A Format Presence | 4/4 | ✅ 8 topic-specific FAQs |
| 1.5 List/Table Usage | 4/4 | ✅ 3 tables + strategic bullet lists |
| 1.6 Paragraph Length | 3/3 | ✅ ≤3 sentences per paragraph |
| 1.7 Key Information Visibility | 4/4 | ✅ No hidden content |
| 1.8 Text-Based Facts | 3/3 | ✅ All data in text format |

**Strength**: The tool_showdown template structure is highly AEO-optimized. Tables, decision trees, and category winners create multiple extraction points for AI systems.

---

## Module 2: Technical Indexability (23/25)

| Criterion | Score | Notes |
|-----------|-------|-------|
| 2.1 Page Indexability | 4/4 | ✅ No blocking directives |
| 2.2 Snippet Eligibility | 4/4 | ✅ No nosnippet |
| 2.3 JavaScript Dependency | 5/5 | ✅ Static Markdown content |
| 2.4 Schema Markup Presence | 2/4 | ⚠️ YAML frontmatter only, needs Article/FAQPage Schema |
| 2.5 Schema-Content Consistency | 4/4 | ✅ Frontmatter matches content |
| 2.6 Semantic HTML Structure | 4/4 | ✅ Proper Markdown semantics |

**Gap**: Missing full Schema.org markup. When published, ensure Article and FAQPage Schema are added.

**Recommendation**:
```json
{
  "@type": "Article",
  "headline": "Kling vs Sora vs Veo vs Runway...",
  "author": {"@type": "Organization", "name": "alici.ai"},
  "datePublished": "2026-01-21"
}
```

---

## Module 3: Citation & E-E-A-T Signals (16/25) ⚠️

### Part A: Structural Signals (11/12)

| Criterion | Score | Notes |
|-----------|-------|-------|
| 3.1 Self-Contained Blocks | 4/4 | ✅ Category Winners are quotable |
| 3.2 Specific Data & Statistics | 4/4 | ✅ "$5/month", "2-minute videos", "4.4/5 score" |
| 3.3 Source Attribution | 3/4 | ⚠️ Sources listed but few inline citations |

### Part B: Content Depth (5/13) ⚠️

| Criterion | Score | Notes |
|-----------|-------|-------|
| 3.4 Experience Evidence | 2/5 | ❌ Claims "20 prompts tested" but shows no specific test results |
| 3.5 Author Credibility | 1/4 | ❌ "alici.ai Content Team" - generic, no named author |
| 3.6 Transparency & Trustworthiness | 2/4 | ⚠️ No n=X sample sizes, no conflict disclosure |

**Critical Gap**: The article claims testing methodology but doesn't demonstrate it. This is the biggest E-E-A-T weakness.

**What's Missing**:
1. **No case studies**: No "We tested prompt X and got result Y"
2. **No named author**: "Content Team" lacks individual credibility
3. **No sample sizes**: "20 prompts" claimed but not shown
4. **No conflict disclosure**: alici.ai recommends its own product without disclosure

**Recommendations**:

1. **Add a test case example**:
   > "We tested the prompt 'A chef in a busy kitchen, steam rising from pots' across all four tools. Sora rendered the steam with physically accurate turbulence (visible light scattering), while Kling produced the result in 47 seconds but with simplified steam animation."

2. **Add named author**:
   ```yaml
   author:
     name: "[Name]"
     title: "AI Video Researcher, alici.ai"
     url: "https://linkedin.com/in/..."
   ```

3. **Add disclosure**:
   > "**Disclosure**: alici.ai is a video generation platform that integrates multiple AI models. We have financial relationships with some tools reviewed."

4. **Add sample sizes**:
   > "Testing conducted by alici.ai Content Team, January 2026. n=20 prompts per tool, 80 total generations."

---

## Module 4: Visibility & Measurement Design (19/20)

| Criterion | Score | Notes |
|-----------|-------|-------|
| 4.1 Semantic URL | 4/4 | ✅ "kling-vs-sora-vs-veo-vs-runway-2026" |
| 4.2 Meta Description | 3/4 | ⚠️ Descriptive but doesn't give winner answer |
| 4.3 Brand Consistency | 4/4 | ✅ Consistent naming throughout |
| 4.4 Query Variant Coverage | 4/4 | ✅ FAQs cover variant phrasings |
| 4.5 Topic-Relevant FAQ | 4/4 | ✅ 8 on-topic questions |

**Minor Improvement**: Meta description could lead with the answer:
> "Kling 2.6 is best for speed, Sora 2 for realism, Veo 3.1 for free quality, Runway Gen-4.5 for editing control. Our hands-on comparison of all four 2026 AI video generators."

---

## Score Comparison: v2.2 Showdown vs. Original Draft

| Module | v2.2 Showdown | Original Draft | Delta |
|--------|---------------|----------------|-------|
| M1: Structure | 30/30 | 28/30 | +2 |
| M2: Technical | 23/25 | 22/25 | +1 |
| M3: E-E-A-T | 16/25 | 18/25 | -2 |
| M4: Visibility | 19/20 | 17/20 | +2 |
| **Total** | **88/100** | **85/100** | **+3** |

**Analysis**: The v2.2 template improves structure and visibility but M3 drops because the stricter v2.3 evaluation framework penalizes generic authorship and undemonstrated testing claims.

---

## AEO Extractability Assessment

### High-Value Extraction Points (AI will likely quote)

1. **Quick Answer** (lines 18-33): Direct "Best for X: Tool Y" format
2. **Snapshot Table** (lines 35-48): Side-by-side comparison data
3. **Scorecard Table** (lines 154-167): Numeric scores for each tool
4. **Category Winners** (lines 76-152): 8 standalone recommendation blocks
5. **FAQ Section** (lines 336-362): 8 self-contained Q&A pairs
6. **Decision Tree** (lines 292-308): If/Then recommendations

### Citation Probability by Section

| Section | Citation Probability | Reason |
|---------|---------------------|--------|
| Quick Answer | ⭐⭐⭐⭐⭐ (95%) | Direct answer format, high AEO value |
| Category Winners | ⭐⭐⭐⭐⭐ (90%) | Standalone, quotable conclusions |
| FAQ | ⭐⭐⭐⭐⭐ (90%) | Q&A format matches user queries |
| Scorecard | ⭐⭐⭐⭐ (80%) | Structured data, easily extractable |
| Deep Dives | ⭐⭐⭐ (60%) | Longer prose, harder to extract |
| Limitations | ⭐⭐ (40%) | Negative content, AI may skip |

---

## Improvement Roadmap

### Quick Wins (+5 points potential)

1. **Add conflict disclosure** (+1 M3)
   - Add "Disclosure" section before FAQ

2. **Add sample sizes to testing** (+1 M3)
   - "n=20 prompts per tool, 80 total generations"

3. **Improve meta description** (+1 M4)
   - Lead with winner answer

### Medium Effort (+4 points potential)

4. **Add one case study example** (+2 M3)
   - Show actual test prompt → result comparison

5. **Add named author** (+2 M3)
   - Individual with verifiable credentials

### Total Potential: 88 → 97/100

---

## Conclusion

**Current State**: The article scores 88/100, placing it in the "Good" tier. The tool_showdown template provides excellent structural AEO optimization (M1: 100%, M4: 95%).

**Primary Weakness**: M3 Content Depth (40%) - the article claims expertise but doesn't demonstrate it through specific test results or named authorship.

**Recommendation**: Before publishing, add:
1. One concrete test case comparison
2. Conflict disclosure for alici.ai promotion
3. Sample size notation for testing claims

This would elevate the score to ~92-95/100 (Excellent tier).

---

*Analysis conducted using AEO Evaluation Framework v2.3*
*alici.ai Content Team, 2026-01-21*
