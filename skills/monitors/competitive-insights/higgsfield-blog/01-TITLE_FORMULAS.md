# 标题设计公式 - Higgsfield 竞品洞察

> 来源: Higgsfield Blog 内容分析 (2026-01-18)
> 适用 Skills: blog-tutorial-writer, blog-list-writer, growth-topic-scout

---

## 核心发现

Higgsfield 使用**极度公式化**的标题，几乎每篇文章都严格遵循固定模板。

---

## 三大内容类型标题公式

### 1. Listicles (榜单类)

**公式**:
```
[Best/Top N] + [具体品类] + in/for [年份] + [平台定语(可选)]
```

**真实示例**:
```
✅ "Best AI Video Generators in 2026"
✅ "Top 5 AI Video Generators for 2025: After Wan 2.5"
✅ "5 AI Video Generator Tools Rated Best for High-Quality Results on Higgsfield"
✅ "Testing Top 5 AI Video Generator Models with Higgsfield's Prompt Team"
✅ "Best Image-to-Video AI Tools for 2025 on Higgsfield"
```

**关键要素**:
- 数字 (Best, Top 5, Top 10)
- 年份 (2025, 2026) - **必须带**
- 品类关键词 (AI Video Generators, AI Tools)
- 平台定语 (on Higgsfield, with Higgsfield)

---

### 2. How-to Guides (教程类)

**公式**:
```
[How to/Guide to] + [动词性目标] + with/using [工具名] + [效果承诺(可选)]
```

**真实示例**:
```
✅ "SORA 2 Prompt Guide: How to Create Viral Videos Like a Pro"
✅ "How to Make Money with Sora 2: A Beginner's Guide to AI Monetization"
✅ "How to Make Your Product Go Viral in 2026 with Sora 2 Trends?"
✅ "Turn Child's Art into AI Animated Cartoon with Sketch-to-Video"
✅ "A Guide to High Quality AI Videos Using Higgsfield Enhancer & Sora 2 MAX"
```

**关键要素**:
- How to/Guide to 开头
- 动词性目标 (Create, Make Money, Make Viral)
- 工具名 (Sora 2, Higgsfield Enhancer)
- 效果承诺 (Like a Pro, Go Viral)

---

### 3. Future Insights (预测/思想领导力)

**公式**:
```
[数字] + [Bold/Key] + [Predictions/Insights] + for [品类] + in [年份]
```
或
```
[产品/技术名] + [动作/状态] + [影响/变化]
```

**真实示例**:
```
✅ "5 Bold Predictions for AI Video Generation in 2026"
✅ "Alibaba Enters the AI Video Race with Wan 2.5"
✅ "Kling 2.6 is Here: What's New in AI Video Generation?"
✅ "How AI Video & Photo Generator Platforms are Affecting the Creative Job Market"
```

**关键要素**:
- 数字预测 (5 Bold Predictions)
- 新闻式标题 (Alibaba Enters, Kling is Here)
- 趋势话题 (Affecting Job Market)
- 年份标注

---

## 关键设计原则

### 原则 1: 年份是强制性的

**为什么有效**:
- SEO: 搜索引擎偏好新鲜内容
- AEO: AI 答案引擎判断时效性
- 用户: 用户搜索时会主动加年份 ("best AI video 2026")

**实施方法**:
- 榜单类: 必须带年份 (2025, 2026)
- 教程类: 可选，但新技术必须带 (Sora 2, Kling 2.6)
- 预测类: 必须带年份

**更新策略**:
- 每年更新版本 ("Best 2025" → "Best 2026")
- 保留旧版本，做内部链接

---

### 原则 2: 数字提升点击率

**为什么有效**:
- 人脑偏好具体数字而非泛泛形容
- "Top 5" 比 "Best" 更具体
- "3 个方法" 比 "几个方法" 更吸引

**实施方法**:
- Listicles: Top 5, Top 10, Best 7
- How-to: 5 Steps, 3 Methods
- Insights: 5 Predictions, 3 Trends

**禁止**:
- 避免 "Several", "Some", "Many"
- 避免无数字的泛泛标题

---

### 原则 3: 品类关键词精准匹配

**为什么有效**:
- SEO: 搜索引擎通过关键词匹配
- 用户: 搜索时用的就是这些词

**实施方法**:
```
用户搜索词 → 标题必须包含
"AI video generator" → "Best AI Video Generators"
"Sora prompt" → "Sora 2 Prompt Guide"
"make money AI" → "How to Make Money with Sora 2"
```

**关键词库**:
- AI Video Generator/Creation/Tools
- AI Image Generator/Creation
- Prompt Guide/Tips/Examples
- Tutorial/Guide/How-to

---

### 原则 4: 效果承诺 (适度使用)

**为什么有效**:
- 承诺具体结果吸引点击
- "Like a Pro", "Go Viral" 是强信号

**实施方法**:
- How-to 类适合加效果承诺
- Listicle 类不需要 (数字已是承诺)

**好的承诺**:
- "Like a Pro" (专业级)
- "Go Viral" (病毒传播)
- "High-Quality Results" (高质量)
- "A Beginner's Guide" (新手友好)

**避免**:
- "Revolutionary" (过度营销)
- "Game-Changing" (夸张)
- "Ultimate" (除非真的详尽)

---

## 应用到 AliciBlog Skills

### blog-list-writer v1.0 升级建议

**当前问题**: 标题公式不够严格，年份有时缺失

**升级方案**:
```yaml
title_generation:
  formula: "[Best/Top N] + [category] + in [YYYY] + [optional_qualifier]"
  required_elements:
    - number: true
    - year: true  # 强制年份
    - category_keyword: true
  validation:
    - must_include_year: true
    - must_include_number: true
    - length: 40-70 characters
```

**示例输出**:
```
❌ "Best AI Video Tools" (缺年份)
✅ "Best AI Video Tools in 2026" (标准)
✅ "Top 5 AI Video Tools for 2026: Complete Guide" (优秀)
```

---

### blog-tutorial-writer v2.0 升级建议

**当前问题**: 标题有时过于创意，不够公式化

**升级方案**:
```yaml
title_generation:
  formula: "How to [action] with [tool] + [outcome_promise]"
  required_elements:
    - how_to_prefix: true
    - action_verb: true (Create, Make, Generate, Build)
    - tool_name: true (Sora 2, alici.ai, etc.)
  optional_elements:
    - outcome_promise: "Like a Pro", "Step-by-Step", "A Beginner's Guide"
```

**示例输出**:
```
❌ "Creating Amazing Videos with AI" (太泛)
✅ "How to Create Viral Videos with Sora 2: A Beginner's Guide" (标准)
✅ "Sora 2 Prompt Guide: How to Make Professional AI Videos" (优秀)
```

---

### growth-topic-scout v1.1 升级建议

**选题时的标题预判**:

在生成 Topic Brief 时，直接给出建议标题:

```json
{
  "suggested_titles": [
    {
      "type": "listicle",
      "title": "Best AI Video Generators in 2026",
      "seo_score": 95,
      "ctr_prediction": "high"
    },
    {
      "type": "how-to",
      "title": "How to Create Cinematic Videos with Sora 2 Like a Pro",
      "seo_score": 88,
      "ctr_prediction": "medium-high"
    }
  ]
}
```

---

## 标题测试清单

在生成标题后，用以下清单验证:

```
☐ 是否包含数字? (Top 5, 3 Methods, etc.)
☐ 是否包含年份? (2026, 2025)
☐ 是否包含核心关键词? (AI Video, Sora 2, etc.)
☐ 是否有效果承诺? (如适用)
☐ 长度是否 40-70 字符?
☐ 是否避免营销词汇? (revolutionary, ultimate, etc.)
```

---

## 竞品对标

| 竞品 | 标题风格 | 我们的策略 |
|------|----------|-----------|
| **Higgsfield** | 极度公式化，年份必带 | 学习公式化，保持一定灵活性 |
| **未来可能的竞品** | 待分析 | - |

---

## 版本历史

- v1.0 (2026-01-18): 初始版本，基于 Higgsfield 分析
