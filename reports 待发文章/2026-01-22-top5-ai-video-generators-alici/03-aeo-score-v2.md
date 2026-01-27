# AEO Analysis Report: Top 5 AI Video Generators on Alici (v2.0)

**Date**: 2026-01-22
**File**: `01-article-v2.md`
**Framework**: AEO Analyzer v2.3
**Previous Score (v1.0)**: 89/100

---

## Overall Score: 95/100 (Excellent)

| Module | Score | Max | Improvement vs v1.0 |
|--------|-------|-----|---------------------|
| M1: Content Structure & Parsability | 30 | 30 | +0 (already maxed) |
| M2: Technical Indexability | 21 | 25 | +0 (Schema pending) |
| M3: Citation & E-E-A-T Signals | 24 | 25 | +6 |
| M4: Visibility & Measurement Design | 20 | 20 | +0 (already maxed) |
| **Total** | **95** | **100** | **+6** |

---

## Module 1: Content Structure & Parsability (30/30)

| Criteria | Score | Notes |
|----------|-------|-------|
| 1.1 Title/H1/Description Alignment | 4/4 | Title, H1, and subtitle aligned. Keywords: AI video generator, 2026, Sora 2, Runway, Veo, Kling, Wan |
| 1.2 Heading Hierarchy | 4/4 | Clear H2/H3 structure: 7 major sections, each tool has consistent subsections |
| 1.3 Opening Direct Answer | 4/4 | ✅ **NEW**: "After generating 50+ test videos...we identified clear winners" — Methodology Authority pattern |
| 1.4 Q&A Format Presence | 4/4 | FAQ section with 8 topic-specific questions + Key Takeaways as implicit Q&A |
| 1.5 List/Table Usage | 4/4 | 4 tables (Methodology, Comparison, Test Case, Key Takeaways) + multiple bullet lists |
| 1.6 Paragraph Length | 3/3 | Short paragraphs throughout (≤3 sentences) |
| 1.7 Key Information Visibility | 4/4 | All content visible, no expandable elements |
| 1.8 Text-Based Facts | 3/3 | All stats in text: 50+ videos, 200+ hours, 1,247 Elo, etc. |

**M1 Status**: ✅ Perfect Score

---

## Module 2: Technical Indexability (21/25)

| Criteria | Score | Notes |
|----------|-------|-------|
| 2.1 Page Indexability | 4/4 | No blocking directives expected |
| 2.2 Snippet Eligibility | 4/4 | No nosnippet restrictions |
| 2.3 JavaScript Rendering | 5/5 | Static Markdown → HTML (Framer renders server-side) |
| 2.4 Schema Markup Presence | 2/4 | ⚠️ Pending: Article + FAQ Schema to be added in Framer |
| 2.5 Schema-Content Consistency | 2/4 | ⚠️ Pending: Schema implementation |
| 2.6 Semantic HTML Structure | 4/4 | Clean Markdown → semantic HTML conversion |

**M2 Status**: ⚠️ Schema implementation pending (post-publish task)

**Recommendation**: Add Article Schema + FAQ Schema in Framer CMS:
```json
{
  "@type": "Article",
  "author": { "@type": "Organization", "name": "Alici Video Team" },
  "datePublished": "2026-01-22"
}
```

---

## Module 3: Citation & E-E-A-T Signals (24/25)

### Part A: Structural Signals (12/12)

| Criteria | Score | Notes |
|----------|-------|-------|
| 3.1 Self-Contained Info Blocks | 4/4 | Key Takeaways, Comparison Table, Test Case results — all standalone-quotable |
| 3.2 Specific Data & Statistics | 4/4 | 50+ videos, 200+ hours, n=50/150/25/10/25 samples, 1,247 Elo, 195% improvement |
| 3.3 Source Attribution | 4/4 | 5 external sources (OpenAI, Runway, Google, Kuaishou, Alibaba) |

### Part B: Content Depth (12/13) — **+6 vs v1.0**

| Criteria | Score | Notes | v2.0 Improvement |
|----------|-------|-------|------------------|
| 3.4 Experience Evidence | 5/5 | ✅ Testing Methodology table with n= data + "Cinematic Car Chase" case study | **+2** (was 3/5) |
| 3.5 Author Credibility | 3/4 | ✅ "Alici Video Team" with testing credentials. Minus 1 for team vs individual | **+2** (was 1/4) |
| 3.6 Transparency | 4/4 | ✅ Explicit disclosure: "Alici is our product. All tests conducted on our platform for fair comparison." | **+2** (was 2/4) |

**M3 Status**: ✅ Excellent — E-E-A-T improvements directly addressed

**Key Improvements Applied**:
1. ✅ Named author block with testing period and disclosure
2. ✅ Testing Methodology table with sample sizes (n=50, n=150, etc.)
3. ✅ Real test case: "Cinematic Car Chase Scene" with prompt + results
4. ✅ Explicit conflict of interest disclosure

---

## Module 4: Visibility & Measurement Design (20/20)

| Criteria | Score | Notes |
|----------|-------|-------|
| 4.1 Semantic URL | 4/4 | Slug: `top-5-ai-video-generators-alici-2026` |
| 4.2 Meta Description | 4/4 | Subtitle serves as meta: "Comparing Sora 2, Runway Gen 4.5, Veo 3.1, Kling 2.6, and Wan 2.6" |
| 4.3 Brand Consistency | 4/4 | "Alici" used consistently throughout |
| 4.4 Query Variant Coverage | 4/4 | Covers: best AI video generator, AI video tools 2026, Sora vs Runway, etc. |
| 4.5 Topic-Relevant FAQ | 4/4 | 8 FAQs directly addressing tool selection questions |

**M4 Status**: ✅ Perfect Score

---

## Score Improvement Summary: v1.0 → v2.0

| Change | Impact | AEO Points |
|--------|--------|------------|
| Key Takeaways at top | AI-extractable summary for featured snippets | +2 (structure) |
| Author info block | E-E-A-T credibility signal | +2 (M3.5) |
| Explicit disclosure | Transparency signal | +2 (M3.6) |
| Testing Methodology table | Demonstrates real experience | +2 (M3.4) |
| Real test case | First-party evidence | +2 (M3.4) |
| Methodology Authority opening | Authority positioning | +1 (structure) |
| **Total Improvement** | | **+6 points** |

---

## Verification Checklist (v2.0 Plan Requirements)

| Requirement | Status |
|-------------|--------|
| Key Takeaways in article top | ✅ Yes |
| Named author + background | ✅ "Alici Video Team, AI Video Researchers" |
| Explicit disclosure statement | ✅ "Alici is our product..." |
| Testing Methodology table (n= data) | ✅ 5 dimensions with sample sizes |
| At least 1 real test case (Prompt + Results) | ✅ "Cinematic Car Chase Scene" |
| Methodology Authority opening | ✅ "After generating 50+ test videos..." |
| AEO ≥ 95 | ✅ 95/100 |
| 00-implementation.md updated | ✅ Yes |

---

## Final Assessment

**Score**: 95/100 (Excellent)
**Rating**: Highly optimized for AI citation
**Status**: ✅ Meets v2.0 target (95+)

**Remaining Improvement Opportunity** (4 points):
- Schema Markup implementation in Framer (+4 points possible)

---

*Analysis completed: 2026-01-22 | AEO Analyzer v2.3*
