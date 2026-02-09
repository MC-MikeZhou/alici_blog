# Tool Showdown Template v1.2

> **⚠️ MIGRATED (2026-02-07)**: 此模板已迁移到独立技能目录。
> **新位置**: `/skills/writers/blog-showdown-writer/SHOWDOWN_TEMPLATE.md`
> **独立技能**: `blog-showdown-writer v1.0` (`/skills/writers/blog-showdown-writer/SKILL.md`)
>
> 本文件保留作为参考。新开发请使用迁移后的版本。

> High-contrast comparison structure for "vs" and "showdown" articles.
> This template enforces 11 mandatory headings with specific formats for tables, CTAs, and decision trees.
> **v1.2 NEW**: Source Attribution 章节 + Reframe 开篇强制 + L4 Integrator 定位

---

## Template Overview

| Aspect | Requirement |
|--------|-------------|
| **Total Headings** | 11 (固定，不可增减) ⭐ v1.2 Updated |
| **Tables** | 2 (Snapshot Table + Scorecard Table) |
| **CTAs** | 3 (固定位置) |
| **Word Count** | 2,500-3,500 词 |
| **AEO Target** | ≥ 75 |
| **Opening Pattern** | P4 Reframe (强制) ⭐ v1.2 NEW |
| **Source Attribution** | 必须章节 ⭐ v1.2 NEW |
| **Citation Density** | ≥ 5/千字 ⭐ v1.2 NEW |

---

## Strategic Positioning (v1.1 NEW) 🎯

### Target Audience

| Audience Segment | Target? | Why |
|------------------|---------|-----|
| **Beginners** (first AI tool) | ✅ YES | Primary conversion opportunity |
| **Explorers** (comparing options) | ✅ YES | Decision paralysis = our value prop |
| **Learners** (studying AI tools) | ✅ YES | Educational content builds trust |
| **Experts** (established workflow) | ❌ NO | Already committed to tools |

### Writing Philosophy

**Frame the problem, not just the solution**:
- Acknowledge that AI tools are confusing
- Validate that "best" depends on context
- Position alici.ai as "try everything first"

**Use personality, not scores**:
- Kling = "The Fast One" (not "4.5/5 speed")
- Sora = "The Perfectionist" (not "4.8/5 quality")
- Each tool gets a memorable character

### Conversion Funnel Design

| Stage | Section | Goal |
|-------|---------|------|
| **Awareness** | Opening | Empathize with decision paralysis |
| **Education** | Tool Personalities | Lower barrier with accessible framing |
| **Trust** | Real experiences | Build credibility through honesty |
| **Conversion** | "Why NOT 4 platforms" | Introduce alici.ai value prop |
| **Action** | 5-min tutorial | Concrete first step |
| **Retention** | FAQ | Answer remaining objections |

---

## Opening Pattern Requirement (v1.2 NEW) ⭐

### Reframe Pattern (P4) - MANDATORY for Showdown

Tool Showdown 文章**必须使用** Pattern 4 (Reframe) 开篇模式。

**结构**:
```
常规认知 → 现实揭露 → 问题重定义 → 新视角承诺
```

**模板**:
```markdown
[Commonly held belief about the tools].

[Reality check: what demos don't show].

The real question isn't '[old question like "which AI looks best?"].'
It's '[reframed question like "which one delivers in real workflows?"].'

Let's find out.
```

**示例**:
```markdown
Demos make every AI model look magical. Production reveals the truth.

You've probably seen stunning AI video demos—Sora's cinematic clips,
Runway's smooth transitions, Kling's realistic motion. But here's what
those demos don't show: actual production challenges.

The real question isn't "which AI looks best in demos?"
It's "which one delivers in real workflows?"

Let's find out.
```

**验证规则**:
- ✅ MUST reframe the comparison question
- ✅ MUST acknowledge demo vs reality gap
- ✅ MUST promise to answer the reframed question
- ❌ NEVER start with "In this article..." or "Welcome to..."
- ❌ NEVER use generic problem-solution opening

**备选模式** (仅当 Reframe 不适用时):
- P2 (Data Hook) - 必须有震撼数据支撑
- P11 (Methodology Authority) - 必须有真实测试数据

---

## Structure (11 Mandatory Headings)

### 1. Quick Answer (H2)

**位置**: 标题后立即出现
**字数**: 120-180 词
**格式要求**:

```markdown
## Quick Answer

[直接回答"哪个更好"的问题，2-3 句话]

**Best for [Use Case 1]**: [Tool A]
**Best for [Use Case 2]**: [Tool B]
**Best for [Use Case 3]**: [Tool C]
**Best overall value**: [Tool X]

[CTA #1 - 放在 Quick Answer 末尾]
```

**CTA #1 位置**: Quick Answer 最后一段

---

### 2. About This Comparison (H2) - v1.2 NEW ⭐

**位置**: Quick Answer 后，Snapshot Table 前
**字数**: 100-150 词
**目的**: Source Attribution + 方法论透明度

```markdown
## About This Comparison

**Testing Source**: This comparison is based on [Source Name]'s testing of [N] AI video generators.

**Test Methodology**:
- **Test Date**: [Month Year]
- **Tools Tested**: [Tool A], [Tool B], [Tool C]
- **Scenarios Covered**: [N] distinct scenarios (e.g., text animation, camera movement, character consistency)
- **Evaluation Criteria**: [Brief list]

**Disclosure**: This analysis is based on [Source]'s testing methodology. alici.ai did not independently verify all results. Tool versions and pricing may have changed since the original test date.

**Original Source**: [Source Name]([URL])
```

**必须包含**:
1. ✅ 测试来源声明 (e.g., "Based on [Source] testing")
2. ✅ 测试方法论摘要 (场景数、工具数、日期)
3. ✅ 披露声明 ("alici.ai did not independently verify...")
4. ✅ 原始来源链接

**验证规则**:
- ⛔ BLOCKING: 缺少 Source Attribution 章节
- ⛔ BLOCKING: 缺少披露声明
- ⚠️ WARNING: 缺少原始来源链接

---

### 3. Snapshot Table (H2) (原 #2)

**位置**: Quick Answer 后
**格式**: 必须是 Markdown 表格

```markdown
## At a Glance: [Tool A] vs [Tool B] vs [Tool C]

| Dimension | [Tool A] | [Tool B] | [Tool C] |
|-----------|----------|----------|----------|
| **Launch Date** | [Date] | [Date] | [Date] |
| **Latest Version** | [Version] ⚠️ | [Version] | [Version] |
| **Best For** | [5-10 words] | [5-10 words] | [5-10 words] |
| **Pricing** | [Price range] | [Price range] | [Price range] |
| **Video Length** | [X seconds] | [X seconds] | [X seconds] |
| **Resolution** | [Max res] | [Max res] | [Max res] |
| **Unique Strength** | [Differentiator] | [Differentiator] | [Differentiator] |
```

**版本标注**: 使用 ⚠️ 标注可能已更新的版本
**来源声明**: 表格下方注明 "Verified as of [Date]. Sources: [Official sites]."

---

### 4. How We Tested (H2) (原 #3)

**字数**: 200-300 词
**必须包含**:
- 测试日期/周期
- 测试方法 (相同 prompts, 相同场景)
- 评分维度说明
- 测试人员/团队声明

```markdown
## How We Tested

We evaluated [N] tools using [methodology] during [time period].

**Testing Approach**:
- Used [X] identical prompts across all tools
- Tested [specific scenarios: portraits, landscapes, actions, etc.]
- Measured [specific metrics]

**Scoring Dimensions** (5-point scale):
| Dimension | Weight | What We Measured |
|-----------|--------|------------------|
| [Dim 1] | 25% | [Specific criteria] |
| [Dim 2] | 25% | [Specific criteria] |
| [Dim 3] | 20% | [Specific criteria] |
| [Dim 4] | 15% | [Specific criteria] |
| [Dim 5] | 15% | [Specific criteria] |

*Testing conducted by alici.ai Content Team, [Month Year].*
```

---

### 5. Category Winners (H2) (原 #4)

**格式**: 6-10 个类别，每个类别包含 Winner + Why + Choose/Avoid
**这是核心差异化章节**

```markdown
## Category Winners

### Best for [Category 1]: [Winner Tool]

**Why it wins**: [2-3 句解释，具体技术原因]

**Choose [Winner] if**: [具体用户场景，1 句]
**Avoid [Winner] if**: [不适合场景，1 句]

---

### Best for [Category 2]: [Winner Tool]

**Why it wins**: [2-3 句解释]

**Choose [Winner] if**: [场景]
**Avoid [Winner] if**: [场景]

[重复 6-10 个类别...]
```

**示例类别** (AI Video):
- Best for Cinematic Realism
- Best for Character Consistency
- Best for Fast Iteration
- Best for Professional Editing
- Best for Budget-Conscious Creators
- Best for Beginners
- Best for Dialogue/Lip Sync
- Best for Motion Control

**CTA #2 位置**: Category Winners 章节结束后

---

### 6. Scorecard Table (H2) (原 #5)

**格式**: 0-5 分评分表，必须 Markdown 表格

```markdown
## Scorecard: Head-to-Head Comparison

| Dimension | [Tool A] | [Tool B] | [Tool C] | Notes |
|-----------|----------|----------|----------|-------|
| Visual Quality | 4.5/5 | 4.8/5 | 4.2/5 | [Brief note] |
| Motion Realism | 4.0/5 | 4.5/5 | 4.7/5 | [Brief note] |
| Speed | 3.5/5 | 4.0/5 | 4.8/5 | [Brief note] |
| Ease of Use | 4.2/5 | 3.8/5 | 4.5/5 | [Brief note] |
| Value | 4.0/5 | 3.5/5 | 4.3/5 | [Brief note] |
| **Overall** | **4.0** | **4.1** | **4.3** | |

*Scores based on [testing methodology reference].*
```

---

### 7. Deep Dives (H2 per tool) (原 #6)

**每个工具一个 H2**，结构一致:

```markdown
## [Tool Name]: Full Review

**Version Tested**: [Version] (as of [Date])
**Pricing**: [Detailed pricing info]

### Strengths
- [Strength 1 with specific example]
- [Strength 2 with specific example]
- [Strength 3 with specific example]

### Weaknesses
- [Weakness 1 with honest assessment]
- [Weakness 2 with honest assessment]

### Best Use Cases
1. [Use case 1]
2. [Use case 2]
3. [Use case 3]

### Sample Output
[Image placeholder or video embed]

---
```

---

### 8. Use-Case Recommendations (H2) (原 #7)

**格式**: 3-5 个具体场景推荐

```markdown
## Which Tool for Your Project?

### For Social Media Content Creators
**Recommended**: [Tool] because [reason].
Secondary option: [Tool] if [condition].

### For Professional Video Producers
**Recommended**: [Tool] because [reason].
Secondary option: [Tool] if [condition].

### For Beginners / First-Time Users
**Recommended**: [Tool] because [reason].
Secondary option: [Tool] if [condition].

### For Budget-Limited Projects
**Recommended**: [Tool] because [reason].
Secondary option: [Tool] if [condition].
```

---

### 9. Decision Tree (H2) (原 #8)

**格式**: If/Then 结构，帮助读者快速决策

```markdown
## Quick Decision Guide

**If you prioritize [Quality Factor]** → Choose [Tool A]
**If you prioritize [Speed Factor]** → Choose [Tool B]
**If you prioritize [Budget Factor]** → Choose [Tool C]
**If you need [Specific Feature]** → Choose [Tool X]
**If you're a beginner** → Start with [Tool Y]
**If you want to try multiple models** → Use [alici.ai platform]

### The 30-Second Decision

1. **Need cinematic quality?** → [Tool]
2. **Need fast turnaround?** → [Tool]
3. **On a tight budget?** → [Tool]
4. **Want flexibility?** → alici.ai (access multiple tools)
```

---

### 10. Limitations & Gotchas (H2) (原 #9)

**格式**: 诚实披露每个工具的限制

```markdown
## What We Couldn't Test (Limitations & Gotchas)

### Version Volatility
AI video tools update frequently. [Tool A] released [version] during our testing period.
**Our scores reflect [version] as of [date].**

### Platform-Specific Limitations
- **[Tool A]**: [Limitation, e.g., "Waitlist access only"]
- **[Tool B]**: [Limitation, e.g., "No API for automation"]
- **[Tool C]**: [Limitation, e.g., "China-only payment options"]

### Testing Constraints
- We tested primarily with [language/style] prompts
- Long-form video (>60s) was not extensively tested
- Results may vary based on subscription tier

### Known Issues (As of [Date])
- [Tool A]: [Known bug/issue]
- [Tool B]: [Known bug/issue]
```

---

### 11. FAQ + Final Verdict (H2) (原 #10)

**FAQ**: 6-10 个问题，每个 2-4 句回答
**Final Verdict**: 总结 + CTA #3

```markdown
## Frequently Asked Questions

### Which is better, [Tool A] or [Tool B]?
[2-4 sentence answer with nuance - "it depends on..."]

### Is [Tool] worth the price?
[2-4 sentence answer]

### Can I use [Tool] for commercial projects?
[2-4 sentence answer about licensing]

### How long does [Tool] take to generate a video?
[2-4 sentence answer with specific times]

### Does [Tool] support [specific feature]?
[2-4 sentence answer]

### What's the best free AI video generator?
[2-4 sentence answer]

[Add 4-6 more relevant FAQs...]

---

## Final Verdict

**For most creators**: [Tool X] offers the best balance of [quality/price/ease].

**For professionals**: [Tool Y] delivers [specific advantage].

### L4 Integrator Positioning (v1.2 NEW) ⭐

**核心定位**: 整合者，而非竞品之一

```markdown
But here's the thing: **You don't have to pick just one.**

[alici.ai] gives you access to [Tool A], [Tool B], and more—
all in one platform. No signup chaos, no switching tabs.

Instead of choosing between [Tool A]'s [strength] and [Tool B]'s [strength],
you can:
- Generate with any model from a single interface
- Compare outputs side-by-side
- Refine results without switching platforms

Think of it as a production layer on top of generation.
You provide direction; the AI handles execution.

> **[CTA: Try all models free →](https://alici.ai)**
```

**L4 验证规则**:
- ✅ MUST contain: "don't have to pick just one" 或等效表述
- ✅ MUST contain: "one platform" 或 "single platform"
- ✅ MUST position as integrator/aggregator
- ❌ MUST NOT: 声称 alici.ai 比任何工具更好
- ❌ MUST NOT: 贬低任何竞品
- ❌ MUST NOT: 将 alici.ai 放入排名对比

**定位话术规范**:
```
✅ "access to multiple tools"
✅ "all in one platform"
✅ "compare outputs side-by-side"
✅ "production layer on top of generation"

❌ "alici.ai is the best"
❌ "better than [competitor]"
❌ "beats [competitor] in..."
❌ "#1 choice"
```

[Final 2-3 sentences of advice]

**[CTA #3 - Strong call to action]**

> 💡 **Try it yourself**: [CTA text with link]

---

*Written by the alici.ai Content Team. Last updated: [Date].*
*Tool versions verified as of [Date]. AI tools update frequently—check official sites for latest features.*
```

---

## CTA Placement Summary

| Position | CTA Type | Suggested Format |
|----------|----------|------------------|
| **After Quick Answer** | Soft CTA | "Try [Tool] on alici.ai →" |
| **After Category Winners** | Contextual CTA | "Compare all [N] tools →" |
| **In Final Verdict** | Strong CTA | "Start creating with [Tool] today →" |

---

## Version Verification Requirements

**Before writing**, the writer MUST:

1. Receive `verified_tools` data from smart-root v2.2
2. Verify format:
```json
{
  "verified_tools": [
    {"name": "Tool A", "verified_version": "X.X", "source": "official site"},
    {"name": "Tool B", "verified_version": "X.X", "source": "WebSearch"}
  ],
  "verification_date": "YYYY-MM-DD",
  "unverified_tools": []
}
```

3. Use verified versions in:
   - Snapshot Table "Latest Version" column
   - Deep Dives "Version Tested" field
   - Limitations section "As of [Date]" statements

4. If versions are unverified, add disclaimer:
   > "⚠️ Version information could not be independently verified. Please check [official site] for the latest version."

---

## Checklist Before Publishing

### Structure
- [ ] All 10 headings present in correct order
- [ ] Quick Answer is 120-180 words
- [ ] Snapshot Table has all required dimensions
- [ ] 6-10 Category Winners with Choose/Avoid format
- [ ] Scorecard Table uses 0-5 scale
- [ ] Decision Tree has If/Then format
- [ ] 6-10 FAQs with 2-4 sentence answers

### Tables
- [ ] Snapshot Table present and complete
- [ ] Scorecard Table present with numeric scores
- [ ] Both tables use proper Markdown formatting

### CTAs
- [ ] CTA #1 after Quick Answer
- [ ] CTA #2 after Category Winners
- [ ] CTA #3 in Final Verdict

### Version Verification
- [ ] All tool versions verified or marked as unverified
- [ ] Verification date stated
- [ ] Sources cited (official sites)

### AEO Optimization
- [ ] Direct answer in first 60 words
- [ ] FAQ section with standalone answers
- [ ] Total word count 2,500-3,500

---

## Template Version History

### v1.2 (2026-01-26)
**InVideo 原则系统化集成** ⭐

1. **Source Attribution 章节 (NEW)**:
   - 新增 Heading #2: About This Comparison
   - 必须包含测试来源、方法论、披露声明
   - 强制原始来源链接

2. **Reframe 开篇强制**:
   - Tool Showdown 文章必须使用 P4 Reframe 模式
   - 备选: P2 Data Hook, P11 Methodology Authority
   - 禁止弱开篇 (In this article, Welcome to...)

3. **L4 Integrator 定位模板**:
   - Final Verdict 中的整合者定位
   - must_contain: "don't have to pick", "one platform"
   - must_not_contain: "best tool", "better than"

4. **引用密度标准**:
   - Tool Showdown: ≥ 5/千字
   - 所有数据必须有来源

5. **结构更新**:
   - 10 Headings → 11 Headings
   - 所有后续 Heading 编号顺延

**预期效果**:
- Source Attribution: 可选 → 强制
- 开篇模式: 任意 → Reframe 强制
- L4 植入法: 隐含 → 显式模板
- 引用密度: ≥3/千字 → ≥5/千字 (Showdown)

---

### v1.1 (2026-01-21)
**Strategic Positioning Integration** 🆕

1. **Target Audience Table**:
   - Explicit beginner/explorer/learner targeting
   - Clear exclusion of expert audience

2. **Writing Philosophy**:
   - "Personality, not scores" approach
   - Problem-framing before solution-providing

3. **Conversion Funnel Design**:
   - 6-stage funnel mapped to article sections
   - "Why NOT 4 platforms" conversion point

---

### v1.0 (2026-01-21)
- Initial release
- 10-heading structure
- Dual table requirement (Snapshot + Scorecard)
- 3-CTA placement system
- Decision Tree format
- Version verification integration

---

*This template is used by blog-list-writer v2.4 when `content_type = "tool_showdown"`*
*InVideo 原则集成: v1.2 (2026-01-26)*
