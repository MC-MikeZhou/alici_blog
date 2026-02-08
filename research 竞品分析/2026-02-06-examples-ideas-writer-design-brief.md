# Examples & Ideas Writer v3.0 — Skill 设计规范

> **创建日期**: 2026-02-06
> **更新日期**: 2026-02-06（完成 28 篇标杆分析后升级为正式规范）
> **文档性质**: 正式设计规范（基于 28 篇 InVideo 标杆文章分析 + v3 Writer 架构对齐）
> **数据支撑**: `2026-02-06-examples-ideas-writer-research.md`（同目录，含 SEO 数据 + 28 篇文章分析）
> **实施位置**: `skills/writers/standalone-blog-examples-writer-v3/`

---

## 1. 背景：为什么需要这个 Skill

### Writer 矩阵缺口

AliciBlog 现有 4 个 Writer，覆盖 3 种搜索意图：

| 搜索意图 | Writer | 基本单元 | 状态 |
|---------|--------|---------|------|
| "帮我选工具" | List Writer v3 (standalone) + v2.4 (AliciBlog) | Tool Card (评测卡片) | 已有 |
| "教我怎么做" | Tutorial Writer v3 (standalone) + v2.4 (AliciBlog) | Step Card (步骤卡片) | 已有 |
| **"给我看例子/模板"** | **无** | **Concept Card (创意概念卡片)** | **缺口** |
| "快速了解案例" | Case Roundup v1.5 | Case Card (300-600词) | 已有(辅助) |

### 数据验证

- **SEO 搜索量**: "Examples" + "Ideas" + "Scripts" 合计 ~22,000+/月，与 Tutorial / List 品类同一量级
- **AEO 引用价值**: "show me examples of X" / "give me a script for X" 是 AI 高频查询模式
- **InVideo 增长验证**: InVideo 500+ 篇博客中 Examples/Ideas/Templates 格式估计占 20-30%
- **竞争难度**: 绝大部分关键词 KD = LOW，容易切入

详细数据见：`2026-02-06-examples-ideas-writer-research.md`

---

## 2. 定位

**Examples & Ideas Writer = 第三种核心长文内容格式**

```
搜索意图              Writer              基本单元              词数
──────────────────────────────────────────────────────────────────
"帮我选工具"      →  List Writer        →  Tool Card          →  4,500-9,500
"教我怎么做"      →  Tutorial Writer    →  Step Card          →  1,800-3,500
"给我看例子/模板"  →  Examples Writer 🆕 →  Concept Card       →  3,000-7,000 (预估)
"快速了解案例"    →  Case Roundup       →  Case Card          →  300-600
```

**核心原则**：品类不限于 UGC Ads。UGC Ads 只是第一个应用场景，就像"Kling Motion Brush 教程"只是 Tutorial Writer 的一个应用。

---

## 3. 核心抽象：Creative Concept Card

### 为什么现有 Writer 不能写 Examples/Ideas 文章

**Tutorial Writer 不行** — 基本单元是 Step（操作步骤），强制 Step 1 → Step 2 → ... 的顺序结构。Examples 文章的 15 个创意概念不是步骤，是并列的独立卡片。

**List Writer 不行** — 基本单元是 Tool Card，固定字段是 `Best for / Why it stands out / Key features / Pros / Cons / Pricing / Notes`。Examples 文章的卡片不需要 Pros/Cons/Pricing（创意概念不是工具），需要的是 Script / Why it works / Variations。字段结构完全不匹配，且 List Writer 的 Python 验证器会因字段缺失直接 FAIL。

**Case Roundup 不行** — 300-600 词太短，装不下 15 个概念 + 脚本。

### Concept Card 字段结构草案

基于 InVideo 标杆文章提炼 + `ugc-ads-usecase-plan.md` 中 Template 1/2 定义：

```
Concept #N: {创意名称}
├── Scenario          — 场景描述（谁、在哪、做什么，50-80词）
├── Why it works      — 为什么有效（心理机制 / 平台算法逻辑，30-50词）
├── Script            — 脚本（Hook → Claim → Proof → CTA，可选）
├── Shot list         — 镜头表（逐镜头，可选，Ideas+Templates 型需要）
├── Variations        — 2-3 个变体（换 hook / 换 offer / 换 proof）
├── Real example      — 真实品牌案例 / Alici use case 链接 / 嵌入视频
└── Try it CTA        — 行动号召（链接到产品页 / use case 页）
```

**与 Tool Card 的关键区别**：
- 无 Pros/Cons（创意概念没有优缺点）
- 无 Pricing（不是工具评测）
- 有 Script + Variations（可复制的实操模板）
- 有 Why it works（心理/营销学分析）

### Concept Card 可能的必填/选填字段（待设计确认）

| 字段 | Examples 型 | Ideas+Templates 型 | 必填/可选 |
|------|------------|-------------------|----------|
| Scenario | 必填 | 必填 | 必填 |
| Why it works | 必填 | 必填 | 必填 |
| Script | 可选 | 必填 | 按 Profile |
| Shot list | 可选 | 推荐 | 可选 |
| Variations | 推荐 | 必填 | 按 Profile |
| Real example | 必填 | 推荐 | 必填 |
| Try it CTA | 必填 | 必填 | 必填 |

---

## 4. InVideo 对标：已验证的文章结构

### 对标文章 A：instagram-ads-examples（Examples 大拼盘型）

- **结构**：按广告格式分类（Video / In-Feed / Carousel / Story / Shopping / Explore）
- **每个 example 的卡片结构**：编号标题 → 说明段落 → 嵌入 Instagram 帖子/图片 → 分析段（为什么有效） → "Use This Template" CTA 链接
- **数量**：21 个 examples
- **词数**：6,000-7,000
- **CTA 模式**：每个 example 后都有 "Use This Template" 链接（分布式 CTA）
- **FAQ**：7 个问题（schema.org FAQPage 标记）
- **开篇**：Data Hook（"90% of users follow at least one business"）

### 对标文章 B：product-video-ideas-with-templates（Ideas + Templates 型）

- **结构**：两大部分 — "Top 7 product video ideas" + "10 tips to create effective product videos"
- **每个 idea 的卡片结构**：概念解释 → 品牌案例视频 → 实操建议 → 模板链接 → CTA
- **数量**：7 个 ideas + 10 个 tips
- **词数**：3,500-4,000
- **与 Examples 型区别**：更偏教学 + 可操作（含模板链接），案例更少但更深

### 对标文章 C：fashion-clothing-ads（垂直行业 Examples 型）

- **结构**：15 个广告 idea → Pro Tips → How to Make（InVideo 教程） → Wrapping Up
- **每个 ad 的卡片结构**：品牌名 + 策略描述 → 分析段 → 嵌入视频 → 3-5 条可操作步骤 → "Use this template" 链接
- **定位**：垂直行业（服装/时尚品牌），不是通用营销
- **特点**：没有脚本/镜头表，偏展示灵感而非可复制模板

---

## 5. 可能的 Profile 系统（待设计确认）

参考 List Writer v3 的 4 Profile 系统和 Tutorial Writer v3 的 3 Tier 系统：

| Profile | 名称 | 卡片数 | 词数(预估) | 用途 | Concept Card 深度 |
|---------|------|--------|-----------|------|------------------|
| **A** | **Examples / Swipe File** | 15-25 | 5,000-7,000 | 灵感展示型大拼盘 | 轻量：Scenario + Why + Example + CTA |
| **B** | **Ideas + Templates** | 7-15 | 3,500-5,500 | 可操作的创意 + 脚本 | 深度：+ Script + Shot list + Variations |
| **C** | **Cookbook / Patterns** | 5-10 | 3,000-4,500 | 可复制的模式集 | 最深：+ 完整脚本 + 变体矩阵 |

### Profile 选择逻辑草案

```
用户输入
  │
  ├─ 卡片数 ≥ 15？                    → Profile A (Examples/Swipe File)
  ├─ 强调 "templates" / "scripts"？   → Profile B (Ideas + Templates)
  ├─ 强调 "patterns" / "cookbook"？    → Profile C (Cookbook)
  └─ 其他                             → Profile A (默认)
```

---

## 6. 设计方向提示

### 6.1 输出文件（参考 v3 Tutorial/List Writer 模式）

```
01-article-draft.md        — 文章正文
02-plan.json              — 规划数据（选了哪些 concepts、评估维度、CTA 计划）
03-assets.json            — 图片/视频资产清单
04-validator-report.json  — 自检报告 (PASS/FAIL)
```

### 6.2 H2 章节顺序（待设计，参考 InVideo 结构）

Profile A (Examples) 草案：
```
# 标题
## Quick Answer (120-180 词)
## Key Takeaways
## [Category 1]（如果有分类）
  ### Concept 1: ...
  ### Concept 2: ...
## [Category 2]
  ### Concept 3: ...
  ...
## How to Recreate These [Topic] with [Product]（产品教程嵌入）
## Pro Tips
## FAQ (≥6 个)
## Conclusion + Final CTA
```

### 6.3 标记系统（复用 v3 标记）

- `<!-- CITABLE_BLOCK type="..." id="..." -->` — 复用，≥5 个
- `<!-- IMAGE_PLACEHOLDER ... -->` — 复用 v2.0 格式
- `<!-- CTA_CARD ... -->` — 复用 friction-aligned 格式，≥2 个
- `<!-- CONCEPT_CARD ... -->` — 可能需要新增的标记（标记每个 concept 边界）

### 6.4 与 ugc-ads-usecase-plan.md 的对齐

`/research 竞品分析/2026-02-06-ugc-ads-usecase-plan.md` 中定义了：

- **Template 1 (Swipe File / Examples)** → 对齐 Profile A
- **Template 2 (Ideas + Templates)** → 对齐 Profile B
- **Template 3 (Use Case Page)** → 不在 Writer 范围内（是网站页面，不是博客）

### 6.5 素材来源

这类文章的 Concept Card 内容来源多样：
- Alici.ai 现有 use case 页面（19 个可用候选，见 `2026-02-06-ugc-ads-benchmark-research-cost.md`）
- 竞品文章结构学习（不是洗稿，是学框架）
- 新创作的创意概念
- 真实品牌案例（嵌入视频/图片）

Writer 的输入设计需要考虑如何接收这些素材（可能需要一个 `concept_pack` 类似 `insight_pack` 的结构）。

---

## 7. 已有相关研究文件索引

| 文件 | 路径 | 内容 |
|------|------|------|
| **SEO 关键词数据** | `research 竞品分析/2026-02-06-examples-ideas-writer-research.md` | 本文档的数据支撑 |
| **UGC Ads 选题计划** | `research 竞品分析/2026-02-04-ai-ugc-ads-topic-plan.md` | 关键词资产库 + Use Case 选题矩阵 |
| **UGC Ads 对标打法** | `research 竞品分析/2026-02-06-ugc-ads-usecase-plan.md` | InVideo 对标 + Template 1/2/3 定义 + Phase 0-4 |
| **UGC Ads 研究成本** | `research 竞品分析/2026-02-06-ugc-ads-benchmark-research-cost.md` | 19 个可用 Alici use case 候选清单 |
| **InVideo 内容框架** | `research 竞品分析/invideo-blog/01-content-framework.md` | 8 大内容类型 + 37 种标题公式 + 文章结构模板 |
| **InVideo 执行摘要** | `research 竞品分析/invideo-blog/00-executive-summary.md` | 50 篇标杆分析 + 20 层植入体系 |
| **InVideo AEO 开篇** | `research 竞品分析/invideo-blog/03-aeo-opening-patterns.md` | 24 种开篇模式 |
| **现有 Tutorial Writer v3** | `skills/writers/standalone-blog-tutorial-writer-v3/` | 可参考的 Tier/自检/Validator 架构 |
| **现有 List Writer v3** | `skills/writers/standalone-blog-list-writer-v3/` | 可参考的 Profile/Plan/Assets 架构 |

---

## 8. 正式设计：Profile 系统（基于 28 篇文章分析）

### 3 个 Profile

| Profile | 名称 | 卡片数 | 词数 | 卡片深度 | InVideo 对标 |
|---------|------|--------|------|---------|-------------|
| **A** | **Showcase** | 10-25 | 3,500-7,000 | 轻-中 | Instagram Ads Examples, Fashion Clothing Ads, Infomercials |
| **B** | **Ideas + Templates** | 5-15 | 3,000-5,500 | 深(含Script) | Product Video Ideas, Testimonial Ideas, Kling Ads |
| **C** | **Mega Gallery** | 25-60+ | 6,000-10,000 | 极轻 | YouTube Video Ideas, Instagram Story Ideas |

### Profile 选择逻辑

```
用户输入:
  ├─ 25+ 个？          → C (Mega)
  ├─ templates/scripts? → B (Ideas+Templates)
  ├─ workflow/playbook? → B (Ideas+Templates)
  ├─ ≤7 + 深度？       → B (Ideas+Templates)
  ├─ 10-25 展示型？     → A (Showcase)
  └─ 默认              → A (Showcase)
```

## 9. 正式设计：Concept Card 字段定义

| 字段 | Profile A | Profile B | Profile C |
|------|-----------|-----------|-----------|
| Concept Name | ✅ | ✅ | ✅ |
| Scenario | ✅ 50-100词 | ✅ 50-100词 | ✅ 20-40词 |
| Why it works | ✅ 30-60词 | ✅ 30-60词 | 可选 |
| Embed | ✅ | ✅ | 推荐 |
| Key elements (≥3) | ✅ | ✅ | ❌ |
| Script (Hook→Claim→Proof→CTA) | 可选 | ✅ 必填 | ❌ |
| Variations (≥2) | 可选 | ✅ 必填 | ❌ |
| Try it CTA | ✅ | ✅ | ✅ |

## 10. 正式设计：H2 Blueprint

### Profile A — Showcase
```
# {Title}
## Key Takeaways
## Quick Overview (Table)
## [Category 1]
  ### Concept 1: ...
## [Category 2]
  ### Concept N: ...
## How to Recreate These with {Product}
## Pro Tips
## FAQ (≥6)
## Conclusion
```

### Profile B — Ideas + Templates
```
# {Title}
## Key Takeaways
## {N} {Topic} Ideas
  ### Idea 1: ... (含 Script + Variations)
  ### Idea N: ...
## How to Prompt for {Topic}
## Pro Tips
## FAQ (≥6)
## Conclusion
```

### Profile C — Mega Gallery
```
# {Title}
## Key Takeaways
## Master List (Table)
## [Category 1]
  ### Concept 1: ... (轻量)
## [Category N]
## How to Get Started with {Product}
## FAQ (≥6)
## Conclusion
```

## 11. 输出文件与 Pipeline

```
Step 1: Planner → 02-plan.json
Step 2: Assets  → 03-assets.json
Step 3: Writer  → 01-article-draft.md
Step 4: Validator → 04-examples-validator-report.json
```

## 12. 实施状态

- [x] SEO 关键词数据验证 (2026-02-06)
- [x] 28 篇 InVideo 标杆文章分析 (2026-02-06)
- [x] 设计规范定稿 (2026-02-06)
- [ ] Skill 文件创建 (`standalone-blog-examples-writer-v3/`)
- [ ] 测试验证 (UGC Ads Examples 测试选题)

---

*本文档已从设计启动 Brief 升级为正式设计规范（2026-02-06）。*
