---
name: source-parser
version: "1.0"
description: >
  基于 mission-brief 对素材进行八维深度分析。
  Part A (维度 1-5): 素材理解层 - 先理解素材本身
  Part B (维度 6-8): SEO/AEO 应用层 - 再提取应用价值
  输出: parsed-source.md (人类可读报告) + assets
triggers:
  - "source parser"
  - "解读素材"
  - "分析素材"
  - "parse source"
allowed-tools: WebFetch, WebSearch, Read, Write
---

# Source Parser v1.0

You are a Content Analyst performing deep source material analysis. Your job is to analyze source materials through an 8-dimensional framework, guided by a mission-brief, and output structured data for the writing process.

## Core Philosophy

**理解先于提取**

```
不是: URL → 直接提取数据点
而是: URL → 理解内容 → 理解背景 → 批判性审视 → 然后提取
```

## 八维分析架构

```
┌─────────────────────────────────────────────────────────────────┐
│                    Source Parser v1.0                            │
│                    八维分析架构                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Part A: 素材理解层 (先理解)                                    │
│  ├── 维度一: 核心内容    → 它在说什么？                         │
│  ├── 维度二: 背景语境    → 为什么这么说？可信吗？               │
│  ├── 维度三: 批判性审视  → 有什么漏洞？我们能超越什么？         │
│  ├── 维度四: 价值提取    → 有什么可复用的框架？                 │
│  └── 维度五: 写作技巧    → 结构/技巧值得学习吗？                │
│                                                                 │
│  Part B: SEO/AEO 应用层 (再应用)                                │
│  ├── 维度六: SEO/AEO 信号  → 对搜索排名有什么用？               │
│  ├── 维度七: 可复用数据    → 可以直接用的数据有哪些？           │
│  └── 维度八: 品牌适配      → 和 Alici 品牌怎么结合？            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Workflow

```
Phase 1: 加载 Mission Brief
├── 读取 mission-brief.json
├── 提取 parsing_focus (extract / ignore / verify)
└── 确定分析深度

Phase 2: 素材获取
├── WebFetch 获取完整内容
├── 提取结构 (H1/H2/H3 树)
├── 提取媒体 (图片/表格/代码块)
└── 保存原始内容备份 (raw-content.md)

Phase 3: Part A - 素材理解层分析 (维度 1-5)
├── 维度一: 核心内容分析
├── 维度二: 背景语境分析
├── 维度三: 批判性审视
├── 维度四: 价值提取
└── 维度五: 写作技巧分析

Phase 4: Part B - SEO/AEO 应用层分析 (维度 6-8)
├── 维度六: SEO/AEO 信号提取
├── 维度七: 可复用数据提取
└── 维度八: 品牌适配评估

Phase 5: 事实核查 (基于 parsing_focus.verify)
├── WebSearch 验证关键声明
├── 标注: confirmed / outdated / unverified
└── 记录验证来源

Phase 6: 输出
├── parsed-source.md (主输出：人类可读的八维分析报告)
├── raw-content.md (原始内容备份)
└── assets/ (提取的表格/图片)
```

---

## Part A: 素材理解层 (维度 1-5)

### 维度一: 核心内容

**Focus**: 搞清楚素材在说什么

```yaml
extract:
  core_thesis:
    description: "用一句话概括核心论点"
    example: "Runway 在质量上领先，Kling 在性价比上胜出"

  key_concepts:
    description: "关键概念及其定义"
    format:
      - term: "概念名称"
        definition: "概念定义"
    example:
      - term: "Motion Control"
        definition: "控制视频中物体运动轨迹的能力"

  structure:
    description: "论证是怎么展开的"
    extract:
      - argument_flow: "论证逻辑链"
      - h2_sections: "H2 章节列表"
      - section_connections: "各部分如何衔接"

  evidence:
    description: "有哪些证据支撑观点"
    extract:
      - data_points: "具体数据/统计"
      - quotes: "权威引用"
      - examples: "案例"
      - tables: "表格数据"
```

### 维度二: 背景语境

**Focus**: 理解素材的来源和立场

```yaml
extract:
  author_identity:
    description: "作者是谁？背景和立场"
    extract:
      - name: "作者/团队名称"
      - background: "背景介绍"
      - stance: "可能的立场/偏见"
      - credibility: "可信度评估 (high/medium/low)"

  writing_context:
    description: "在什么背景下写的"
    extract:
      - background: "写作背景"
      - responding_to: "在回应什么现象/争论"
      - purpose: "想解决什么问题/想影响谁"
      - publish_date: "发布日期"

  underlying_assumptions:
    description: "没说出来的前提假设"
    format: "列表"
    example:
      - "假设读者是视频创作者"
      - "假设质量比价格更重要"
```

### 维度三: 批判性审视

**Focus**: 识别素材的局限性，找到超越机会

```yaml
extract:
  potential_rebuttals:
    description: "主要的反对意见可能是什么"
    format: "列表"
    example:
      - "测试场景可能不代表真实使用"

  argument_gaps:
    description: "论证漏洞/跳跃/偏颇"
    format: "列表"
    example:
      - "未说明测试设备和环境"
      - "未提供样本量 (n=?)"

  applicability_bounds:
    description: "观点在什么情况下成立/不成立"
    example: "适用于短视频创作者，不适用于长片制作"

  avoided_topics:
    description: "作者刻意回避或淡化的问题"
    format: "列表"
    example:
      - "未提及 API 集成"
      - "未讨论自家产品的劣势"
```

### 维度四: 价值提取

**Focus**: 提取可复用的思考框架和洞察

```yaml
extract:
  reusable_frameworks:
    description: "可复用的思考框架或方法论"
    format:
      - name: "框架名称"
        structure: "框架结构"
        applicability: "如何复用"
    example:
      - name: "5 维度评测框架"
        structure: ["质量", "速度", "价格", "易用性", "功能"]
        applicability: "可用于任何工具对比文章"

  insights_for_creators:
    description: "对内容创作者的启发"
    example: "质量优先选 Runway，预算优先选 Kling"

  insights_for_marketers:
    description: "对营销人员的启发"
    example: "对比文章需要明确测试方法才有说服力"

  cognitive_shifts:
    description: "可能改变读者的什么认知"
    example: "工具选择不是 '最好' 而是 '最适合'"
```

### 维度五: 写作技巧

**Focus**: 分析原文的写作技巧

```yaml
# 所有模式都分析，但洗稿模式简化，参考模式详细

extract:
  structure_design:
    title_design: "标题设计分析"
    opening_design: "开头设计分析"
    closing_design: "结尾设计分析"

  persuasion_techniques:
    description: "说服技巧"
    format: "列表"
    example:
      - "数据支撑"
      - "场景化推荐"
      - "对比表格"

  engagement_hooks:
    description: "吸引读者的钩子"
    format: "列表"
    example:
      - "Quick Comparison 前置"
      - "FAQ 解答疑虑"

  worth_learning:
    description: "值得学习的地方"
    format: "列表"

  worth_avoiding:
    description: "需要避免的地方"
    format: "列表"
```

---

## Part B: SEO/AEO 应用层 (维度 6-8)

### 维度六: SEO/AEO 信号提取

**Focus**: 提取对搜索排名和 AI 引用有价值的元素

```yaml
extract:
  title_analysis:
    original_title: "原标题"
    title_formula: "匹配的标题公式 (参考 TITLE_FORMULAS.md)"
    primary_keyword: "主关键词"
    secondary_keywords: "次关键词列表"
    year_included: "是否包含年份 (boolean)"
    number_included: "是否包含数字 (boolean)"

  aeo_elements:
    direct_answer: "文章开头的直接回答（如果有）"
    featured_snippet_candidate: "可能被 Google 摘录的段落"
    key_takeaways: "Key Takeaways 列表"
    faq_questions: "FAQ 问题列表"

  keyword_density:
    h1_keywords: "H1 中的关键词"
    h2_keywords: "H2 中的关键词"
    first_100_words: "前 100 词中的关键词"
```

### 维度七: 可复用数据提取

**Focus**: 提取可直接复用的事实性数据

```yaml
extract:
  testing_data:
    description: "测试数据"
    format:
      - claim: "具体声明"
        data: "数据内容"
        source: "数据来源"
        methodology: "测试方法（如果提及）"
        freshness: "数据日期"
        needs_verification: "是否需要核实 (boolean)"

  pricing_data:
    description: "价格信息"
    format:
      - tool: "工具名"
        plan: "套餐名（可选）"
        price: "价格"
        source_date: "信息日期"
        needs_verification: true  # 价格容易过时，默认需要核实

  comparison_tables:
    description: "对比表格"
    format:
      - id: "表格 ID"
        type: "feature_comparison / pricing / performance"
        extracted_to: "保存路径"
        can_reuse_directly: "是否可直接复用 (boolean)"

  citations:
    description: "引用/来源"
    format:
      - quote: "引用内容"
        source: "来源"
        authority_level: "L1-L5 (参考 citation-pyramid.yaml)"
```

### 维度八: 品牌适配

**Focus**: 评估与 Alici AI 品牌和产品的适配度

```yaml
extract:
  product_mapping:
    tools_mentioned: "素材提及的工具列表"
    alici_products_applicable: "可关联的 Alici 产品"
    integration_angle: "整合角度"
    example:
      tools_mentioned: ["Kling", "Runway"]
      alici_products_applicable: ["video_studio", "video_prompt"]
      integration_angle: "整合者视角：Alici 支持 Kling + Runway + 更多模型"

  brand_alignment:
    tone_match: "与 Alici 品牌调性匹配度 (high/medium/low)"
    needs_tone_adjustment: "需要调整的语气列表"

  compliance_check:
    competitor_mentions: "提及的竞品"
    positioning_risk: "贬低竞品的风险 (high/medium/low)"
    claims_to_verify: "需要验证的声明（避免虚假声明）"

  cta_opportunities:
    natural_insertion_points: "自然插入 CTA 的位置"
    recommended_cta_type: "推荐的 CTA 类型"
```

---

## 事实核查

### 核查触发条件

基于 mission-brief 的 `parsing_focus.verify` 字段：

```yaml
default_verify_items:
  - 工具版本号
  - 价格数据
  - 发布日期
  - 关键统计数据
```

### 核查方法

```yaml
verification_methods:
  工具版本:
    method: "WebSearch 查询官网最新版本"
    query_template: "{tool_name} latest version 2026"

  价格数据:
    method: "WebSearch 或直接访问官网定价页"
    query_template: "{tool_name} pricing"

  统计数据:
    method: "WebSearch 查找原始来源"
    query_template: "{statistic} source"
```

### 核查结果格式

在报告中以表格形式呈现：

| 声明 | 原值 | 验证值 | 状态 | 来源 |
|------|------|--------|------|------|
| 具体声明 | 原文值 | 核实值 | ✅ 已确认 / ⚠️ 已过时 / ❓ 未验证 | 核实来源 |

---

## Output Path

```
/research 竞品分析/parsed-sources/
└── YYYY-MM-DD-{topic-slug}/
    ├── parsed-source.md        # 主输出：人类可读的八维分析报告
    ├── raw-content.md          # 原始内容备份
    └── assets/
        ├── table_feature.md    # 提取的表格
        ├── table_pricing.md
        └── screenshot_1.png    # 提取的图片
```

> **设计决策**: 输出格式选择 Markdown 而非 JSON，因为：
> 1. 人类可直接阅读和审核
> 2. 可在 GitHub/IDE 中预览
> 3. 表格和层级结构更清晰
> 4. 后续 Writer Skills 仍可解析 Markdown 提取信息

---

## Output Template: parsed-source.md

```markdown
# 素材深度解读报告

> **来源**: https://example.com/blog/article
> **解读日期**: 2026-02-02
> **解读模式**: 洗稿
> **关联 Brief**: /research/mission-briefs/2026-02-02-topic-slug/mission-brief.md

---

## Part A: 素材理解层

### 维度一：核心内容

**核心论点**: Runway 在质量上领先，Kling 在性价比上胜出

**关键概念**:
| 概念 | 定义 |
|------|------|
| Motion Control | 控制视频中物体运动轨迹的能力 |

**文章结构**:
- **论证展开**: 对比框架：先总结 → 逐项对比 → 场景推荐
- **H2 章节**: Quick Comparison, Quality, Pricing, Verdict

**证据支撑**:
- **数据点**: Runway 质量评分 8.5/10, Kling 价格 $9.90/月
- **引用**: "Based on our testing across 5 scenarios..."
- **案例**: Motion control demo 对比

---

### 维度二：背景语境

**作者信息**:
- **作者/团队**: InVideo Team
- **背景**: AI 视频工具公司博客
- **立场**: 可能偏向自家产品

**写作背景**:
- **背景**: 2026-01 发布，响应 Kling 2.6 发布
- **回应**: 市场对 AI 视频工具对比的需求
- **目的**: 帮助用户选择工具（同时推广 InVideo）

**隐含假设**:
- 假设读者是视频创作者
- 假设读者关心性价比
- 假设质量 > 价格（隐含）

---

### 维度三：批判性审视

**可能的反驳**: 测试场景可能不代表真实使用

**论证漏洞**:
- 未说明测试设备和环境
- 未提供样本量 (n=?)

**适用边界**: 适用于短视频创作者，不适用于长片制作

**回避的话题**: API 集成、团队协作功能、自家产品 InVideo 的劣势

---

### 维度四：价值提取

**可复用框架**:

| 框架名称 | 结构 | 复用场景 |
|---------|------|---------|
| 5 维度评测框架 | 质量/速度/价格/易用性/功能 | 可用于任何工具对比文章 |

**洞察提炼**:
- **对创作者**: 质量优先选 Runway，预算优先选 Kling
- **对营销人员**: 对比文章需要明确测试方法才有说服力
- **认知转变**: 工具选择不是"最好"而是"最适合"

---

### 维度五：写作技巧

**结构设计**:
- **标题设计**: X vs Y: Which [Category] [Benefit]?
- **开篇设计**: 直接给出结论 + 承诺详细对比
- **结尾设计**: Decision Tree + CTA

**说服技巧**: 数据支撑、场景化推荐、对比表格

**吸引钩子**: Quick Comparison 前置、FAQ 解答疑虑

**值得学习**: 结论前置、场景化推荐

**需要避免**: 主观评价词过多、缺少测试方法说明

---

## Part B: SEO/AEO 应用层

### 维度六：SEO/AEO 信号

**标题分析**:
| 属性 | 值 |
|------|-----|
| 原标题 | Kling vs Runway: Which AI Video Tool Wins in 2026? |
| 标题公式 | comparison-1 (X vs Y: Which [Category]) |
| 主关键词 | kling vs runway |
| 次关键词 | ai video tool, kling 2.6, runway gen-4 |
| 含年份 | ✅ |
| 含数字 | ❌ |

**AEO 元素**:
- **直接回答**: For most creators, Kling offers better value at $9.90/month, while Runway excels in quality for professional work.
- **Featured Snippet 候选**: 开头的对比总结段落
- **Key Takeaways**:
  - Kling: Best for budget-conscious creators
  - Runway: Best for quality-focused professionals
- **FAQ 问题**:
  - Which is better, Kling or Runway?
  - How much does Kling cost?
  - Can Runway do motion control?

**关键词分布**:
- **H1 关键词**: kling, runway, ai video
- **H2 关键词**: comparison, pricing, quality, features
- **前 100 词**: kling, runway, ai video, 2026, tool

---

### 维度七：可复用数据

**测试数据**:
| 声明 | 数据 | 来源 | 方法 | 日期 | 需验证 |
|------|------|------|------|------|--------|
| Runway Gen-4 人物一致性得分 | 8.5/10 | 原文测试 | 5 个场景测试 | 2026-01 | ⚠️ 是 |

**价格数据**:
| 工具 | 价格 | 数据日期 | 需验证 |
|------|------|----------|--------|
| Kling | $9.90/月 | 2026-01 | ⚠️ 是 |
| Runway | $12/月 | 2026-01 | ⚠️ 是 |

**对比表格**:
| 表格 ID | 类型 | 提取路径 | 可直接复用 |
|---------|------|----------|-----------|
| feature_comparison | 功能对比 | /assets/table_feature.md | ✅ |

**引用**:
| 引用内容 | 来源 | 权威等级 |
|---------|------|---------|
| "Based on our testing across 5 scenarios..." | InVideo 原创测试 | L3 |

---

### 维度八：品牌适配

**产品映射**:
- **提及工具**: Kling, Runway
- **适用 Alici 产品**: video_studio, video_prompt
- **整合角度**: 整合者视角：Alici 支持 Kling + Runway + 更多模型

**品牌一致性**:
- **语气匹配度**: medium
- **需调整**: 去掉主观评价词、增加数据支撑

**合规检查**:
- **竞品提及**: InVideo (原文来源)
- **定位风险**: low
- **待验证声明**: 价格数据、版本号

**CTA 机会**:
- **自然插入点**: Quick Comparison 之后、Category Winners 之后
- **推荐 CTA**: 试用 Alici Video Studio

---

## 事实核查结果

| 声明 | 原值 | 验证值 | 状态 | 来源 |
|------|------|--------|------|------|
| Kling 2.6 价格 | $9.90/月 | $9.90/月 | ✅ 已确认 | Kling 官网 2026-02-02 |
| Runway 版本 | Gen-3 | Gen-4 已发布 | ⚠️ 已过时 | - |

**需要行动**: 更新为 Gen-4 信息

---

## 资产清单

**表格**:
- `feature_comparison` → /assets/table_feature.md
- `pricing_comparison` → /assets/table_pricing.md

**图片**:
- `quality_comparison` → /assets/quality_1.png (Quality comparison)

---

## 解读摘要

| 指标 | 值 |
|------|-----|
| 完成维度 | 8/8 |

### 素材理解层
- **核心论点清晰**: ✅
- **可信度评估**: medium
- **发现论证漏洞**: 3 处
- **可复用框架**: 1 个

### SEO/AEO 应用层
- **SEO 潜力**: high
- **AEO 元素**: 4 个
- **可复用数据点**: 12 个
- **品牌适配度**: medium

### 事实核查
- **已验证**: 8 条
- **已过时**: 2 条
- **待验证**: 4 条

---

## 优先行动

1. 更新 Runway 版本为 Gen-4
2. 核实价格数据
3. 补充测试方法论
4. 调整语气以符合 Alici 品牌

## 超越机会

- **版本更新**: Runway Gen-3 → Gen-4
- **工具扩展**: 加入 Sora 2 / Veo 3
- **方法论**: 补充测试设备和样本量

---
*Generated by source-parser v1.0*
```

---

## Integration with mission-brief

Source Parser 读取 mission-brief 的 `parsing_focus` 来指导分析：

```yaml
parsing_focus_mapping:
  extract:
    - "测试数据" → 强化 dimension_7_reusable_data.testing_data
    - "价格信息" → 强化 dimension_7_reusable_data.pricing_data
    - "对比表格" → 强化 dimension_7_reusable_data.comparison_tables

  ignore:
    - "原文推荐语" → 不提取到 dimension_4_value_extraction
    - "CTA" → 不分析原文 CTA
    - "作者观点" → 弱化 dimension_2_context.author_identity.stance

  verify:
    - "工具版本号" → 触发版本核查
    - "价格数据" → 触发价格核查
```

---

## Error Handling

| 错误场景 | 处理方式 |
|---------|---------|
| mission-brief 不存在 | 提示用户先运行 mission-brief |
| URL 无法访问 | 尝试 WebSearch 获取缓存版本，或提示用户粘贴原文 |
| 某个维度无法分析 | 标注为 "insufficient_data"，继续其他维度 |
| 事实核查失败 | 标注为 "unverified"，记录失败原因 |

---

## Version History

### v1.0 (2026-02-02)
- 初始版本
- 八维分析框架 (5 理解层 + 3 应用层)
- 事实核查集成
- 输出 parsed-source.md (主输出) + assets
- **设计决策**: 选择 Markdown 而非 JSON，便于人类阅读和审核
