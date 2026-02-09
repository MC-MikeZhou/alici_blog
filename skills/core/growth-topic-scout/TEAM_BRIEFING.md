# Growth Topic Scout v2.3：团队简介

> 一句话：输入竞品 URL / 种子关键词（含发散选题），输出经过验证的选题机会清单（SEO+AEO）以及可直接开写的方向（Seed 模式）。

---

## v2.3 核心能力

### 多模式架构（A/B/C + Seed D1/D2）

```
Growth Topic Scout v2.3
├── 模式 A: URL 分析
│   └── 竞品 URL → 提取话题 → DataForSEO 验证 → Top 10 选题
│
├── 模式 B: 关键词矩阵
│   └── 种子词 → 矩阵扩展 (50-100) → DataForSEO 验证 → SERP/竞品差距报告
│
├── 模式 C: AEO 验证层
│   └── AI keyword heat + LLM mentions + LLM responses → AEO Score (100)
│
└── Seed 模式（两条路线）
    ├── D1: Anchored Seed Funnel（竞品锚定，2 方向）
    │   └── 竞品意图模式 → 扩散 → DataForSEO 验证 → Title Lock
    └── D2: Diversity Engine（发散引擎，3 方向）⭐ NEW
        └── 多策略发散 → 语义聚类去重 → 多样性门禁 → DataForSEO 验证 → Title Lock
```

| 版本 | 输入 | 能力 | 输出 |
|------|------|------|------|
| **v2.1** | 竞品 URL / 种子词 | + AEO 验证层（双评分） | SEO Score + AEO Score |
| **v2.2** | 种子词 | Seed D1（竞品锚定漏斗） | 2 个 Direction（可开写） |
| **v2.3** | 种子词（可无竞品） | Seed D2（多样性引擎） | 3 个 Direction + diversity_report |

---

## Legacy: v2.0 新特性（保留作为参考）

## 它是什么？

Growth Topic Scout 是一个「选题侦察」技能，帮助内容团队：

### 模式 A（URL 分析）
```
竞品文章 URL → 分析提取 → 市场验证 → 选题建议 + 内容大纲
```

### 模式 B（关键词矩阵）⭐ NEW
```
种子关键词 → 矩阵扩展 → 批量验证 → Top 20 选题 + 差距报告
```

**核心产出**：
- 模式 A: Top 10 选题机会 + 标题建议 + AEO 答案块
- 模式 B: 50-100 关键词矩阵 + Top 20 选题 + 竞品差距报告 + 批量执行计划

---

## 运作机制

### 模式 A: 三步流程（现有）

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  1. 提取    │ →  │  2. 验证    │ →  │  3. 输出    │
│  竞品内容   │    │  市场信号   │    │  选题简报   │
└─────────────┘    └─────────────┘    └─────────────┘
```

### 模式 B: 六步流程（新增）

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  1. 矩阵    │ →  │  2. 验证    │ →  │  3. 打分    │
│  扩展       │    │  DataForSEO │    │  排序       │
└─────────────┘    └─────────────┘    └─────────────┘
        │
        ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  4. SERP    │ →  │  5. 竞品    │ →  │  6. 差距    │
│  分析       │    │  爬取       │    │  报告       │
└─────────────┘    └─────────────┘    └─────────────┘
```

**模式 B 详细步骤**：

1. **矩阵扩展** - 从种子词生成 50-100 个关键词组合
   - 修饰词扩展 (best, free, top, online)
   - 意图词扩展 (how to, vs, alternatives, tutorial)
   - 用途扩展 (for YouTube, for TikTok, for marketing)
   - DataForSEO API 扩展

2. **DataForSEO 验证** - 获取精确搜索量和趋势数据
   - 搜索量 (search_volume)
   - 12个月趋势 (monthly_searches)
   - CPC (商业价值)
   - 竞争度 (competition)

3. **打分排序** - 按机会分排序 Top 20
   - 搜索量权重 30%
   - 趋势权重 20%
   - 竞争差距权重 25%
   - 商业价值权重 25%

4. **SERP 分析** - 检测 Top 20 关键词的 SERP 特性
   - AI Overview 存在
   - Featured Snippet
   - People Also Ask

5. **竞品爬取** - 用 WebFetch 抓取 Top 3 竞品
   - 标题、结构、字数
   - FAQ 存在、作者信息
   - 发布日期

6. **差距报告** - 识别竞品弱点
   - 内容过时 (+25分)
   - 缺少 FAQ (+10分)
   - 缺少作者信息 (+15分)
   - 字数过少 (+20分)

---

## 触发词

### 模式 A 触发（URL 分析）
- 竞品分析
- 选题发现
- content benchmark
- topic scout
- growth topics

### 模式 B 触发（关键词矩阵）⭐
- 生成关键词矩阵
- keyword matrix
- 批量关键词
- scale SEO
- pSEO
- 规模化选题
- programmatic SEO

### Seed D1 触发（竞品锚定漏斗，2 方向）
- seed mode
- 种子模式
- topic funnel
- 选题漏斗
- 帮我找选题
- find topics for

### Seed D2 触发（Diversity Engine，多样性发散，3 方向）⭐ NEW
- seed mode v2
- diversity seed
- 发散选题
- 多样性选题
- cosine
- 余弦相似度
- Mollick protocol

---

## 为什么有效？

### 1. 从「拍脑袋」到「有据可查」

| 传统选题 | Growth Topic Scout v2.0 |
|---------|------------------------|
| "我觉得这个话题不错" | "这个话题有 12K 搜索量，上升趋势" |
| "竞品写了，我们也写" | "竞品缺少 FAQ 和 2026 更新，差距分 72" |
| "应该能有流量吧" | "CPC $2.45 表明商业价值高" |

### 2. 规模化 SEO (pSEO)

模式 B 专为规模化内容生产设计：
- 一次分析生成 50-100 个关键词机会
- Top 20 选题可直接批量执行
- 差距报告提供具体超越策略

### 3. 竞品差距驱动

不是简单模仿，而是找到竞品的**结构性弱点**：
- 内容过时 6 个月以上？更新版机会
- 缺少作者信息？E-E-A-T 机会
- 缺少 FAQ？AEO 引用机会
- 字数太少？深度内容机会

---

## 评分体系（v2.3）

Growth Topic Scout 使用**双评分**，把“能排”与“能被 AI 推荐”分开衡量：

1) **SEO Score（0-100）**：需求/竞争/业务可赢性  
2) **AEO Score（0-100）**：AI 时代可见度窗口（AI search heat / LLM mentions / LLM responses）

并根据二者映射 `combined_priority`（excellent / high_seo_first / high_aeo_first / good / low）。

### D2（Diversity Engine）额外评分

Seed D2 在最终 3 个方向上新增：
- `diversity_bonus`（0-15）：与其它入选方向的语义差异度奖励
- `portfolio_score`：用于在“多样性约束”下做最终排序

---

## 输出文件

### 模式 A 输出
```
/reports/YYYY-MM-DD-{topic}/
├── 00-topic-scout-report.md   # 人可读报告
└── 00-topic-brief.json        # 给 Writer 的 Brief
```

### 模式 B 输出
```
/reports/YYYY-MM-DD-{seed-slug}/
├── 00-topic-scout-report.md   # 人可读报告 (矩阵格式)
├── keyword_matrix.json        # 完整矩阵数据
├── gap_analysis.json          # 差距分析数据
└── 00-topic-brief.json        # 给 Writer 的 Brief (Top 20)
```

### Seed D1 输出（2 方向）
```
/reports/YYYY-MM-DD-{seed-slug}/
├── 00-mission-config.json     # Mission Config
├── 00-directions-report.md    # 人可读漏斗报告
└── 00-topic-brief.json        # final_directions[2]
```

### Seed D2 输出（3 方向 + 多样性报告）⭐
```
/reports/YYYY-MM-DD-{seed-slug}/
├── 00-mission-config.json     # Mission Config (diversity.enabled=true)
├── 01-seed-dimensions.json    # 5 维解构 + query_seeds
├── 02-raw-topics.json         # 3 策略 raw pool
├── 03-diversity-report.json   # clustering + metrics + gate
├── 00-directions-report.md    # 人可读漏斗报告
└── 00-topic-brief.json        # final_directions[3] + diversity_report
```

---

## 产出示例

### 模式 A 示例

**输入**：
```
分析这个竞品：
https://perfectcorp.com/blog/best-ai-video-generators
```

**输出摘要**：

| # | 选题 | 分数 | 类型 | 洞察 |
|---|-----|-----|------|-----|
| 1 | Best AI Video Generators 2026 | 87 | Listicle | 竞品缺少 2026 更新 |
| 2 | Sora vs Runway 对比 | 84 | Showdown | 竞品没有专门对比文章 |

### 模式 B 示例

**输入**：
```
帮我生成 "ai video generator" 的关键词矩阵
```

**输出摘要**：

```
===============================================================================
                    KEYWORD MATRIX ANALYSIS REPORT
===============================================================================
种子词: ai video generator | 日期: 2026-01-24
生成关键词: 87 个 | Top 20 选题 | 差距分析完成

Top 20 选题 (按机会分排序):
-------------------------------------------------------------------------------
| # | 选题                              | 搜索量 | 趋势 | 差距分 | 机会分 |
|---|-----------------------------------|--------|------|--------|--------|
| 1 | best ai video generator 2026      | 12,000 | ↑    | 72     | 85     |
| 2 | free ai video generator online    | 8,500  | ↑    | 65     | 82     |
| 3 | sora vs runway vs kling 2026      | 6,200  | ↑    | 70     | 81     |

竞品普遍弱点:
- 65% 内容过时 (>6个月)
- 58% 缺少 FAQ
- 40% 缺少作者信息
===============================================================================
```

---

## 成本估算

### 模式 B 单次分析费用

| 操作 | 单价 | 用量 | 费用 |
|------|------|------|------|
| DataForSEO 关键词 | $0.015/词 | 100 词 | $1.50 |
| DataForSEO SERP | $0.002/查 | 20 查 | $0.04 |
| WebFetch | 免费 | 60 页 | $0.00 |
| **总计** | | | **~$1.54** |

---

## 如何使用

### 模式 A（URL 分析）

```
用户: 用 growth-topic-scout 分析这个竞品:
      https://competitor.com/blog/ai-video
```

### 模式 B（关键词矩阵）

```
用户: 帮我生成 "ai video generator" 的关键词矩阵
```

或者：

```
用户: 用 scale SEO 分析 "ai image generator" 这个领域
```

---

## 与其他技能的配合

```
growth-topic-scout（选题）
       ↓
  模式 A: Top 10          模式 B: Top 20 + 批量执行计划
       ↓                         ↓
blog-tutorial-writer /    batch-processor（批量执行）
blog-list-writer（生产）         ↓
       ↓                  多篇文章并行生产
aeo-analyzer（质检）
       ↓
发布
```

---

## 版本历史

### v2.0 (2026-01-24)
**关键词矩阵模式 (NEW)**:
- 新增模式 B: 关键词矩阵扩展
- 6 步工作流 (扩展 → 验证 → 打分 → SERP → 爬取 → 差距)
- 新输出文件: keyword_matrix.json, gap_analysis.json
- 竞品差距分析和评分
- 批量执行支持 (~$1.54/分析)

### v1.3 (Prior)
- DataForSEO LABS 和 ONPAGE 模块集成

### v1.2 (2026-01-18)
- 3 类型标题建议 (Listicle/How-to/Insights)
- 年份验证
- CTR 预测

### v1.1 (Prior)
- DataForSEO API 集成
- SERP 特性检测
- 精确搜索量数据

### v1.0 (Original)
- 初始版本
- WebSearch 验证
- 基础选题 Brief

---

## 一句话总结

> **Growth Topic Scout v2.0 = 竞品分析 + 关键词矩阵 + 差距报告**
>
> 把「我们写什么」从主观判断变成数据驱动 + 规模化的决策流程。

---

*Skill 版本：v2.0*
*最后更新：2026-01-24*
