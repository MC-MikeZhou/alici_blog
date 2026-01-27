# AliciBlog 3 Writer Skills Deep Dive

**Analysis Date**: 2026-01-21
**Version Analyzed**: blog-tutorial-writer v2.3, blog-list-writer v2.2, case-roundup-writer v1.3

---

## 1. blog-tutorial-writer v2.3

### Overview

| Attribute | Specification |
|-----------|---------------|
| **Content Type** | Tutorial / How-to articles |
| **Word Count** | 1,800-2,500 words |
| **Target Keywords** | "how to", "guide", "steps", "tutorial" |
| **AEO Target** | >= 80 (with M3 content depth) |

### Core Features

#### 1.1 AIDA Opening Framework (v2.0)

```
Attention (40-60 words) → Direct answer to title question
Interest (20-30 words) → Pain point recognition
Desire (20-30 words) → Value promise
Action (10-20 words) → Navigation hint
```

**Impact**: 80-120 word opening optimized for AI extraction. First-draft AEO improved from 73 → 82.

#### 1.2 Citable Blocks System

- **Minimum**: 3-5 blocks per article
- **Distribution**: Opening (1), Main steps (2-3), Tips/Conclusion (1)
- **Format**: `<!-- CITABLE_BLOCK: Label -->` ... `<!-- /CITABLE_BLOCK -->`
- **Length**: 40-80 words each (independently quotable)

**AEO Impact**: 30-40% increase in AI citation probability per HubSpot research.

#### 1.3 Version Inheritance (v2.2)

**Problem Solved**: E-E-A-T content loss during rewrites (case studies, testing data, author info).

**Protected Content Categories**:
- Author YAML block (E-E-A-T credibility)
- Case studies with iteration narratives
- Testing methodology ("n=X" references)
- External source citations
- Disclosure statements
- FAQ sections
- Citable Blocks

**Validation Checklist**:
- Word count cannot decrease >20%
- All case studies must be present
- External source count >= previous version
- FAQ count >= previous version

#### 1.4 7-Element Prompt Structure (v2.1)

For AI generation tutorials, mandatory "Understanding Prompt Structure" section:

1. Format & Style
2. Camera & Lens
3. Location & Framing
4. Lighting & Color Palette
5. Motion & Action Beats
6. Dialogue Blocks (optional)
7. Audio Cues (optional)

**Impact**: Educational value + expertise signal + AI tool differentiation.

### Workflow Integration

```
Topic Brief → blog-tutorial-writer → Editor (REQUIRED) → AEO Analyzer → Auto-Improver (if <80) → Framer
```

### ROI Assessment

| Metric | Value | Notes |
|--------|-------|-------|
| Production Time | 15-25 min | Full auto with Editor |
| Human Review | Only if AEO < 75 | 3-round auto-improver first |
| First-Draft Quality | 73-82 AEO | Improved with v2.0 AIDA |
| Iteration Need | ~20% of articles | Most pass first-time |

---

## 2. blog-list-writer v2.2

### Overview

| Attribute | Specification |
|-----------|---------------|
| **Content Type** | Listicle / Comparison articles |
| **Word Count** | 2,500-3,500 words |
| **Target Keywords** | "best", "top", "alternatives", "vs", "showdown" |
| **AEO Target** | >= 75 (first draft >= 70) |

### Core Features

#### 2.1 Title Formula Enforcement

**Mandatory Pattern**:
```
[Number] Best [Topic] in [Year] ([Qualifier])
```

**Validation Rules**:
- MUST include number (Top 5, Best 10, 15 Best)
- MUST include year (2026)
- MUST use "Best" or "Top" prefix
- NEVER omit year
- Length: 40-70 characters

#### 2.2 Evaluation Methodology Section (v2.0)

5-dimension standardized testing framework (MANDATORY):

| Dimension | Weight | Testing Method |
|-----------|--------|----------------|
| Dimension 1 | 25% | Specific method |
| Dimension 2 | 30% | Specific method |
| Dimension 3 | 20% | Specific method |
| Dimension 4 | 15% | Specific method |
| Dimension 5 | 10% | Specific method |

**E-E-A-T Impact**: Transparent methodology = Authority signal.

#### 2.3 Enhanced Comparison Table

**NEW in v2.0**: "Core Positioning" column with one-line differentiation.

| Tool | Core Positioning | Price | Quality | Speed |
|------|-----------------|-------|---------|-------|
| Tool A | Best for [specific use case] | $XX | Rating | Rating |

**Positioning Rules**:
- 5-10 words maximum
- Highlight ONE key differentiator
- Pattern: "Best for [specific]" or "Industry leader in [capability]"

#### 2.4 Tool Showdown Mode (v2.2 NEW)

Triggered by "vs", "comparison", "showdown" keywords.

**10 Fixed Headings Structure**:
1. Quick Answer (120-180 words, 4 "Best for" bullets)
2. Snapshot Table
3. How We Tested
4. Category Winners (6-10, Choose/Avoid format)
5. Scorecard Table (0-5 scores)
6. Deep Dives (per tool, Version Tested)
7. Use-Case Recommendations
8. Decision Tree (If/Then format)
9. Limitations & Gotchas
10. FAQ + Final Verdict

**Required Outputs**:
- 2 Tables (Snapshot + Scorecard)
- 3 CTAs (Quick Answer / Category Winners / Final Verdict)
- Version Verification integration

### ROI Assessment

| Metric | Value | Notes |
|--------|-------|-------|
| Production Time | 20-35 min | Longer due to research |
| Human Review | Only if AEO < 75 | Methodology adds trust |
| First-Draft Quality | 70-78 AEO | Higher with 5-dim eval |
| Competitive Edge | High | Structured methodology |

---

## 3. case-roundup-writer v1.3

### Overview

| Attribute | Specification |
|-----------|---------------|
| **Content Type** | Case Roundup / Micro blog |
| **Word Count** | 300-600 words |
| **Target Use Case** | Quick insights, real-world examples |
| **AEO Target** | >= 70 (micro_roundup rubric) |

### Core Features

#### 3.1 Material Gate (v1.1 - MANDATORY)

**Critical Rule**: Real material required before proceeding. NO fabrication.

Acceptable materials:
- YouTube video URLs
- Video transcripts
- Observed/tested cases
- Reference articles/posts

**Failure Response**: STOP and request material. Refuse to fabricate.

#### 3.2 Multi-Dimensional Expansion (Single Source)

When only 1 video/source available, analyze from 4 angles:

1. **Workflow**: How to operate, steps
2. **Use Cases**: Application scenarios
3. **Quality Tips**: How to improve results
4. **Pitfalls**: What to avoid

**Impact**: Prevents fabrication, maintains Case-driven integrity.

#### 3.3 Visual Prompt Pack (v1.3 NEW)

1-3 characters with V1/V2/V3 evolution:

| Version | Purpose | Characteristics |
|---------|---------|-----------------|
| **V1 - Neutral Starter** | Motion Control friendly | Neutral pose, full body, clean background |
| **V2 - Style Boost** | Enhanced visuals | Costume, props, lighting, scene |
| **V3 - Viral/Series** | Shareability | High recognition, thumbnail-ready |

**Output Files**:
- `asset_plan.json` (for Editor)
- `prompt_pack.md` (for readers)

#### 3.4 Hook Module (v1.2)

Format: Phenomenon + Counter-intuitive conclusion

```markdown
<!-- HOOK -->
[Observable trend/problem - 1 sentence]
[Counter-intuitive insight: "关键不在...而在..." - 1 sentence]
<!-- /HOOK -->
```

#### 3.5 Source & Boundary (Transparency)

Structured format:
- 📹 Source: X YouTube tutorials (transcript saved)
- ⚠️ Boundary: What's verified vs unverified
- 🔗 Tool Version: Kling 2.6, Nano Banana Pro (2026-01)

### Article Structure

1. H1 Title (Query-format, 40-60 chars)
2. Hook (2 sentences)
3. Direct Answer (40-60 words)
4. Key Takeaways (3-5 bullets)
5. Case Studies (2-5 cases OR multi-dimensional)
6. Why it Works (mechanism attribution)
7. Visual Prompt Pack (1-3 characters)
8. Video Integration Slot
9. How to Try It (max 4 steps, UI-style)
10. Mini FAQ (3 questions)
11. Source & Boundary
12. Low-friction wrap-up

### ROI Assessment

| Metric | Value | Notes |
|--------|-------|-------|
| Production Time | 10-20 min | Shortest of 3 writers |
| Human Review | Minimal | Real material ensures quality |
| First-Draft Quality | 65-75 AEO | Micro rubric |
| Content Velocity | High | 3-5x faster than Tutorial |

---

## Cross-Writer Comparison

| Feature | Tutorial Writer | List Writer | Case Roundup |
|---------|-----------------|-------------|--------------|
| **Word Count** | 1,800-2,500 | 2,500-3,500 | 300-600 |
| **Production Time** | 15-25 min | 20-35 min | 10-20 min |
| **AIDA Opening** | Yes | Partial | Hook format |
| **Citable Blocks** | 3-5 | 3-5 | 1-2 |
| **Comparison Table** | Optional | Mandatory | No |
| **Version Inheritance** | Yes | No | No |
| **Visual Assets** | Placeholders | Tool screenshots | Prompt Pack |
| **Material Gate** | No | No | Yes (mandatory) |

---

## Version Evolution Summary

### blog-tutorial-writer

| Version | Key Addition | Impact |
|---------|--------------|--------|
| v1.0 | Basic structure | Baseline |
| v2.0 | AIDA + Citable Blocks | +9 AEO points |
| v2.1 | 7-Element Prompt Structure | Education value |
| v2.2 | Version Inheritance | E-E-A-T protection |
| v2.3 | Dependency validation | Quality gate |

### blog-list-writer

| Version | Key Addition | Impact |
|---------|--------------|--------|
| v1.0 | Basic listicle | Baseline |
| v2.0 | Eval Methodology + Core Positioning | Authority signal |
| v2.1 | Dependency validation | Quality gate |
| v2.2 | Tool Showdown mode | High-contrast comparison |

### case-roundup-writer

| Version | Key Addition | Impact |
|---------|--------------|--------|
| v1.0 | Basic case format | Baseline |
| v1.1 | Material Gate + Multi-dimensional | No fabrication |
| v1.2 | Hook + Query-format title | Engagement |
| v1.3 | Visual Prompt Pack + Asset Plan | Visual workflow |

---

*See 03-comparison-matrix.md for side-by-side competitive analysis*
