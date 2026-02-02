---
name: human-review-checklist
version: "1.1"
type: skill
description: >
  Human Review Checklist v1.1 - 人工审核层，实现"读者视角"的检查 + 自动修复 + Writer Feedback Loop。
  在 Editor Gate 之后执行，作为发布前最终审核。
  核心理念：先理解目标读者是谁，再从他们的视角审视文章。
  10 个 Check Module，8 个可自动修复，2 个需要 Writer Feedback。
  v1.1 新增：Reader Persona Check + Internal Language Leak Check
allowed-tools: Read, Write, Grep, Glob
triggers:
  - "human review"
  - "人工审核"
  - "发布前检查"
  - "/human-review"
  - "最终检查"
required-docs:
  - path: "/skills/core/human-review-checklist/prompts/COMPETITOR_WORDBANK.yaml"
    purpose: "竞品词库 + 推荐模式检测"
  - path: "/skills/core/human-review-checklist/prompts/BRAND_VOICE_RULES.yaml"
    purpose: "品牌调性规则"
  - path: "/skills/core/human-review-checklist/prompts/TERM_REPLACEMENTS.yaml"
    purpose: "术语替换词库"
  - path: "/skills/core/human-review-checklist/prompts/READER_PERSONA_TEMPLATE.yaml"
    purpose: "目标读者画像模板 (v1.1 NEW)"
  - path: "/skills/core/human-review-checklist/prompts/INTERNAL_LANGUAGE_PATTERNS.yaml"
    purpose: "内部语言泄露检测规则 (v1.1 NEW)"
  - path: "/skills/_docs/BLOG_CONTENT_REGISTRY.md"
    purpose: "内链选择用的内容索引"
outputs:
  - "09-human-review-checklist.md"
  - "01-article-reviewed.md"
---

# Human Review Checklist v1.1

> **核心理念**: 先理解目标读者是谁，再从他们的视角审视文章。不是"我想说什么"，而是"读者需要听到什么"。

## 工作流程

```
01-article-edited.md (Editor 输出)
         ↓
┌────────────────────────────────────────┐
│     Human Review Checklist v1.1        │
│                                        │
│  Step 0: 识别目标读者 (NEW in v1.1)    │
│  ┌──────────────────────────────────┐  │
│  │ Who / Pain / Search / Language   │  │
│  │ / Goal → Reader Persona 卡片     │  │
│  └──────────────────────────────────┘  │
│         ↓                              │
│  10 个 Check Module (用 Persona 审视)  │
│         ↓                              │
│  ┌──────────────────────────────────┐  │
│  │ 可自动修复 (8个) → 直接修复      │  │
│  │ 不可自动修复 (2个) → Feedback    │  │
│  │                     给 Writer    │  │
│  └──────────────────────────────────┘  │
│         ↓                              │
│  Writer 收到 Feedback → 重写部分内容   │
│         ↓                              │
│  再次检查 (最多 2 轮)                  │
└────────────────────────────────────────┘
         ↓
输出:
├── 09-human-review-checklist.md  (检查 + 修复报告)
└── 01-article-reviewed.md        (修复后版本)
```

---

## 10 个 Check Module 概览

| # | Module | 读者视角问题 | 级别 | 自动修复 |
|---|--------|-------------|------|----------|
| 1 | Title CTR Check | 标题能让人点吗？ | ⚠️ WARNING | ✅ 是 |
| 2 | Title-Reader Alignment | 读者会这样搜吗？ | ⚠️ WARNING | ✅ 是 |
| 3 | **Competitor Mention Scan** | 在帮竞品打广告吗？ | ⛔ **BLOCKING** | ⚠️ 部分 |
| 4 | Internal Link Audit | 有没有留住读者？ | ⚠️ WARNING | ✅ 是 |
| 5 | H2 AEO Citable Check | AI 能引用章节吗？ | ⚠️ WARNING | ✅ 是 |
| 6 | Promise-Delivery Check | 说到做到了吗？ | ⚠️ WARNING | ❌ Feedback |
| 7 | TL;DR Value Statement | 读者知道能得到什么吗？ | ⚠️ WARNING | ✅ 是 |
| 8 | Brand Voice Check | 这是 alici.ai 的声音吗？ | ⚠️ WARNING | ✅ 是 |
| **9** | **Reader Persona Check** ⭐ | **读者是谁？能看懂吗？** | ⚠️ WARNING | ⚠️ 部分 |
| **10** | **Internal Language Leak** ⛔ | **有内部语言泄露吗？** | ⛔ **BLOCKING** | ✅ 是 |

---

## Module 1: Title CTR Check (标题吸引力)

### 检查项 (0-100 分)

| 检查项 | 分值 | 检测方式 |
|--------|------|----------|
| Power Word | +20 | 包含: best, top, ultimate, proven, free, easy, how to, complete |
| 数字 | +20 | 正则: `\d+` (5 Ways, Top 10) |
| 年份 | +15 | 正则: `202[6-9]` |
| 长度 | +15 | 50-60 字符 (SERP 最佳) |
| 主关键词 | +15 | 文章核心词在标题中 |
| 问题/承诺式 | +15 | How to / What / Why / Complete Guide |

### 自动修复规则

```python
def auto_fix_title_ctr(title, article_content):
    suggestions = []

    # 1. 缺少年份 → 添加 "in 2026"
    if not re.search(r'202[6-9]', title):
        suggestions.append(f"{title} in 2026")

    # 2. 缺少数字 → 从 H2 计数
    if not re.search(r'\d+', title):
        h2_count = len(re.findall(r'^## ', article_content, re.MULTILINE))
        if h2_count >= 3:
            suggestions.append(f"{h2_count} {title}")

    # 3. 缺少 Power Word → 添加 "Best/Complete"
    power_words = ['best', 'top', 'ultimate', 'complete', 'proven', 'free']
    if not any(pw in title.lower() for pw in power_words):
        topic = extract_topic(title)
        suggestions.append(f"The Complete Guide to {topic}")

    return suggestions[:3]  # 返回最多 3 个候选
```

### 输出格式

```markdown
### Module 1: Title CTR Check

**Current Title**: "AI Video Generator Comparison"
**CTR Score**: 45/100 ⚠️ WARNING

| Check | Status | Details |
|-------|--------|---------|
| Power Word | ❌ | Missing (suggest: Best/Complete) |
| Number | ❌ | Missing |
| Year | ❌ | Missing (add "in 2026") |
| Length | ✅ | 32 chars |
| Keyword | ✅ | "AI Video" present |

**Auto-Fix Applied**:
- Original: "AI Video Generator Comparison"
- Fixed: "5 Best AI Video Generators in 2026: Complete Comparison"
```

---

## Module 2: Title-Reader Alignment (标题接地气)

### 检查项

1. **术语检测**: 使用 `TERM_REPLACEMENTS.yaml` 中的术语词库
2. **搜索模式匹配**: "how to", "best X for", "X vs Y"
3. **利益点检测**: "in 5 minutes", "for free", "without coding"

### 自动修复规则

直接使用 `TERM_REPLACEMENTS.yaml` 进行替换：

```yaml
# TERM_REPLACEMENTS.yaml 示例
replacements:
  "i2v": "image to video"
  "t2v": "text to video"
  "temporal consistency": "smooth transitions"
```

### 输出格式

```markdown
### Module 2: Title-Reader Alignment

**Alignment Score**: 70/100 ⚠️ WARNING

| Check | Status | Details |
|-------|--------|---------|
| Jargon Found | ⚠️ | "i2v" detected |
| Search Pattern | ✅ | "how to" format |
| Benefit Point | ❌ | Missing clear benefit |

**Auto-Fix Applied**:
- Replaced "i2v" → "image to video"
```

---

## Module 3: Competitor Mention Scan (竞品推荐检测) ⛔ BLOCKING

### 检测逻辑

1. **扫描全文**: 匹配 `COMPETITOR_WORDBANK.yaml` 中的竞品名称
2. **上下文分析**: 对每个匹配提取前后 200 字符
3. **推荐模式检测**: 检查是否包含推荐语句

### 推荐模式分类

**⛔ BLOCKING (必须修复)**:
- "we recommend (using)? {competitor}"
- "you should (try|use) {competitor}"
- "the best (choice|option) is {competitor}"
- "{competitor} is (the )?best"
- CTA 链接指向竞品网站

**✅ ALLOWED (中性比较)**:
- "{competitor} offers/features/costs"
- "{competitor} vs"
- "compared to {competitor}"
- "{competitor} excels at / struggles with"

### 自动修复 vs Feedback

| 问题类型 | 处理方式 |
|---------|---------|
| CTA 链接到竞品 | ✅ 自动删除链接 |
| 竞品官网链接 | ✅ 自动删除 |
| 推荐语句 | ❌ **Feedback 给 Writer** |

### Feedback 模板

```markdown
## Writer Feedback: Competitor Recommendation

**Issue**: Line {line_number} contains competitor recommendation
**Original**: "{original_text}"
**Problem**: Direct recommendation to competitor

**Required Fix** (choose one):
- Option A: 改为中性描述 "{competitor} offers {feature}"
- Option B: 添加 alici.ai 替代 "...or use alici.ai which integrates all tools"

Please rewrite this paragraph and return only the revised text.
```

---

## Module 4: Internal Link Audit (内链检查)

### 检查项

| 检查项 | 标准 | 状态 |
|--------|------|------|
| 数量 | 2-4 个 alici.ai/blog/* 链接 | ⚠️ 不足时自动补充 |
| 锚文本 | 3-5 词描述性 (非 "click here") | ⚠️ 质量差时警告 |
| Pillar 链接 | 应有指向主题 Hub 的链接 | ⚠️ 缺失时建议 |

### 自动修复规则

```python
def auto_fix_internal_links(content, registry, target_count=3):
    current_links = find_alici_blog_links(content)

    if len(current_links) >= 2:
        return content  # 已满足最低要求

    # 从 BLOG_CONTENT_REGISTRY.md 选择相关文章
    keywords = extract_keywords(content)
    related_articles = find_related(registry, keywords)

    for article in related_articles[:target_count - len(current_links)]:
        # 找到最佳插入位置
        position = find_best_paragraph(content, article.keywords)
        # 生成自然锚文本
        anchor = generate_anchor(article.title)
        # 插入链接
        content = insert_link_at(content, position, anchor, article.url)

    return content
```

---

## Module 5: H2 AEO Citable Check (章节框架)

### 每个 H2 评分 (0-100)

| 检查项 | 分值 | 检测 |
|--------|------|------|
| 有明确承诺 | +25 | 数字/How-to/问题式 |
| 首段可独立 | +25 | 20-100 词，非 "This section..." |
| 有可引用语句 | +25 | 数据/明确观点 |
| 有结构化数据 | +25 | 列表/表格/步骤 |

**目标**: ≥60% 的 H2 达到 75+ 分

### 自动修复规则

| 原 H2 | 问题 | 修复后 |
|-------|------|--------|
| "Pricing" | 无承诺 | "AI Video Tool Pricing: $5-$100/Month Comparison" |
| "Our Recommendation" | 无数据 | "Our Top Pick: Why [Tool] Wins in 2026" |
| "Conclusion" | 无价值 | "Final Verdict: Best AI Video Tool by Use Case" |

---

## Module 6: Promise-Delivery Check (承诺兑现) ❌ Feedback

### 检查项

| 承诺类型 | 检测方式 | 验证方式 |
|---------|---------|---------|
| 数字承诺 | 标题 "5 Ways" | 正文 H2 ≥ 5 |
| 年份承诺 | 标题 "2026" | 正文有 2026 数据 |
| 范围承诺 | "Complete Guide" | 字数 ≥ 2000 |
| 动作承诺 | "How to" | 有清晰步骤 |

### 处理方式

**此 Module 不自动修复**，因为涉及内容创作。

当检测到不匹配时，生成 Feedback 给 Writer：

```markdown
## Writer Feedback: Promise-Delivery Mismatch

**Title Promise**: "5 Best AI Video Generators"
**Actual Content**: Only 4 tools covered in detail

**Required Action** (choose one):
- Option A: 添加第 5 个工具的详细介绍
- Option B: 修改标题为 "4 Best AI Video Generators"

Please address this mismatch.
```

---

## Module 7: TL;DR Value Statement (价值陈述)

### 弱开篇检测

```regex
^(In this article|This guide|Today we|Let's explore|Welcome to|Have you ever)
```

### 自动修复规则

```python
def auto_fix_tldr(opening, article_content):
    # 检测弱开篇
    weak_patterns = [
        r'^In this (article|guide|post)',
        r'^Today we',
        r'^Let\'s (explore|dive)',
        r'^Welcome to',
    ]

    if not any(re.match(p, opening, re.I) for p in weak_patterns):
        return opening  # 开篇正常，不修改

    # 提取文章信息
    tool_count = count_tools(article_content)
    key_insight = extract_first_takeaway(article_content)

    # 生成强开篇
    new_opening = f"""Looking for the best AI video generator in 2026?

After comparing {tool_count} leading tools, the key insight is: {key_insight}.

By the end of this guide, you'll know exactly which tool fits your budget, workflow, and creative needs—with real pricing and quality comparisons."""

    return new_opening
```

---

## Module 8: Brand Voice Check (品牌调性)

### 品牌调性定义

| 维度 | 是 | 不是 |
|------|-----|------|
| 专业度 | 专业但平易近人 | 学术/炫技 |
| 语气 | 友好、实用 | 销售腔、夸大 |
| 视角 | 帮助用户选择 | 推销自家产品 |
| 数据 | 有据可查 | 虚假声明 |

### 自动修复规则

使用 `BRAND_VOICE_RULES.yaml` 中的替换词库：

```yaml
# 禁止词汇 → 替换
forbidden_replacements:
  "revolutionary": "effective"
  "game-changing": "useful"
  "best ever": "highly rated"
  "industry-leading": "popular"
  "#1 tool": "top-rated tool"
```

---

## Writer Feedback Loop

### 触发条件

当以下问题无法自动修复时，生成 Feedback：
1. **Module 3**: 竞品推荐语句需要改写
2. **Module 6**: Promise-Delivery 不匹配

### 循环控制

```python
def run_human_review(article_path, max_rounds=2):
    article = read_file(article_path)

    for round in range(max_rounds):
        # 执行 8 个 Module 检查
        report = execute_all_modules(article)

        # 应用自动修复
        article = apply_auto_fixes(article, report)

        # 检查是否需要 Writer Feedback
        if not report.needs_feedback:
            break  # 所有问题已解决

        # 生成并发送 Feedback
        feedback = generate_feedback(report.feedback_items)
        revised = request_writer_revision(article, feedback)
        article = apply_revisions(article, revised)

    # 输出结果
    write_report(report, "09-human-review-checklist.md")
    write_article(article, "01-article-reviewed.md")

    return report
```

### 最大轮次

- **默认**: 2 轮
- **超过后**: 标记为 `MANUAL_REVIEW_REQUIRED`，需人工介入

---

## 输出格式

### 09-human-review-checklist.md

```markdown
# Human Review Report v1.0

**Article**: [标题]
**Date**: YYYY-MM-DD
**Revision Rounds**: N

## Executive Summary

| Module | Status | Auto-Fixed | Writer Feedback |
|--------|--------|------------|-----------------|
| 1. Title CTR | ✅/⚠️ | Yes/No | - |
| 2. Title-Reader | ✅/⚠️ | Yes/No | - |
| 3. Competitor Scan | ✅/⛔ | Partial | N items |
| 4. Internal Links | ✅/⚠️ | Yes/No | - |
| 5. H2 AEO Citable | ✅/⚠️ | Yes/No | - |
| 6. Promise-Delivery | ✅/⚠️ | - | N items |
| 7. TL;DR Value | ✅/⚠️ | Yes/No | - |
| 8. Brand Voice | ✅/⚠️ | Yes/No | - |

**Overall Status**: ✅ PASS / ⚠️ WARNING / ⛔ BLOCKING / 🔍 MANUAL_REVIEW

## Auto-Fix Log
[所有自动修复的详细记录]

## Writer Feedback Resolution
[Feedback 发送和解决的记录]

## Final Checklist (Human Confirm)
- [ ] 标题看起来想点击吗？
- [ ] 读者能快速知道这篇文章的价值吗？
- [ ] 没有在推荐竞品吗？
- [ ] 这是 alici.ai 的声音吗？
```

### 01-article-reviewed.md

包含所有自动修复 + Writer 修订的最终版本。

---

## 触发方式

```bash
# 命令方式
/human-review "path/to/01-article-edited.md"

# 自然语言
"帮我做发布前检查"
"人工审核这篇文章"
"检查是否可以发布"
```

---

## Module 9: Reader Persona Check (目标读者识别) ⭐ NEW in v1.1

### 核心理念

> **先理解目标读者是谁，再从他们的视角审视文章。**

### Step 1: 提取 Reader Persona

从文章标题 + Key Takeaways + 前 500 字提取目标读者画像：

| 维度 | 问题 | 示例 (YouTube CTR Guide) |
|------|------|--------------------------|
| **Who** | 他们是谁？ | 小型 YouTube 创作者，订阅 <10K |
| **Pain** | 他们的痛点？ | 视频曝光多但点击少，不知道怎么改进 |
| **Search** | 他们会怎么搜索？ | "how to improve youtube ctr", "why my videos don't get clicks" |
| **Language** | 他们用什么词汇？ | thumbnail, click rate, views (不是 CTR, APV, AEO) |
| **Goal** | 他们想得到什么？ | 具体可执行的改进方法，而不是理论 |

### Step 2: 用 Persona 审视文章

| 检查项 | 问题 | 判断标准 |
|--------|------|---------|
| Title-Search Match | 标题匹配读者的搜索习惯吗？ | 匹配 Search 维度 |
| Terminology Clarity | 术语是读者能理解的吗？ | 匹配 Language 维度 |
| Opening-Pain Response | 开篇直接回应痛点吗？ | 匹配 Pain 维度 |
| Content-Goal Alignment | 内容帮读者达成目标吗？ | 匹配 Goal 维度 |

### 自动修复

- **术语替换**: 使用 `TERM_REPLACEMENTS.yaml` 将行业术语替换为读者友好的词汇
- **其他项**: 生成 Warning，供人工审核

### 配置文件

- `prompts/READER_PERSONA_TEMPLATE.yaml`

---

## Module 10: Internal Language Leak Check (内部语言泄露检测) ⛔ BLOCKING NEW in v1.1

### 核心理念

> **读者打开文章是为了解决问题，不是为了看编辑流程。任何"写给编辑/写给AI"而不是"写给读者"的内容都应该删除。**

### 检测类型

| 类型 | 示例 | 问题 | 严重级别 |
|------|------|------|---------|
| **编辑注释** | "Based on v3", "改掉AI痕迹" | 读者不需要知道版本迭代 | ⛔ BLOCKING |
| **内部术语** | "AEO", "Data Hook", "洗稿" | 读者不懂行业黑话 | ⛔ BLOCKING |
| **AI设计暴露** | "(easy for AI to cite)" | 暴露优化意图 | ⛔ BLOCKING |
| **H2写作指导** | "(putting the problem into human terms)" | 这是给作者的，不是给读者的 | ⚠️ WARNING |

### 检测规则示例

```regex
# 编辑注释
/based on v\d+/i
/AI-like writing/i
/reference expansion/i

# 内部术语
/\bAEO\b/
/\bData Hook\b/

# H2括号指导
/^##\s+.+\s+\(.{10,}\)$/  # H2 后跟长括号
```

### 自动修复策略

| 问题类型 | 处理方式 |
|---------|---------|
| 编辑注释段落 | 完全删除 |
| 内部术语 | 替换为读者友好词汇，或删除 |
| AI设计暴露 | 删除括号内内容 |
| H2写作指导 | 删除括号及内容 |

### 触发背景

基于 **YouTube CTR Guide** 文章审核发现的问题：

| 原文 | 问题分析 |
|------|---------|
| "Based on v3, this version changed several AI-like writing methods..." | 读者不关心这是第几版 |
| "AEO quick answers" | 读者不知道AEO是什么 |
| "Opening data hook (Data Hook)" | "Data Hook"是写作框架术语 |
| "(putting the problem into human terms)" | 这是作者的写作目标 |

### 配置文件

- `prompts/INTERNAL_LANGUAGE_PATTERNS.yaml`

---

## 版本历史

### v1.1 (2026-02-01) ⭐
- **核心理念升级**: 从"技术检查"到"读者视角审视"
- **新增 Module 9**: Reader Persona Check (目标读者识别)
- **新增 Module 10**: Internal Language Leak Check (内部语言泄露检测) ⛔ BLOCKING
- **新增配置文件**:
  - `prompts/READER_PERSONA_TEMPLATE.yaml`
  - `prompts/INTERNAL_LANGUAGE_PATTERNS.yaml`
- **新增 CHANGELOG.md**: 记录版本变更
- 模块数量: 8 → 10
- 自动修复数量: 6 → 8

### v1.0 (2026-01-31)
- 初始版本
- 8 个 Check Module
- 6 个自动修复 + 2 个 Writer Feedback
- 最多 2 轮 Feedback Loop
