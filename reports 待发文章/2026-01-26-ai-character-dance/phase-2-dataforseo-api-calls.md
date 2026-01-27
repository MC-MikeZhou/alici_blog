# Phase 2: DataForSEO API 调用清单

## API 1: Keywords Data (批量关键词验证)

### 目标
验证 25 个代表性关键词的搜索量、竞争度、CPC 数据

### Endpoint
`dataforseo.keywords_data`

### 参数
```json
{
  "location_code": 2840,
  "language_code": "en",
  "keywords": [
    "AI character animation for marketing",
    "how to make AI character dance videos",
    "AI character dance videos for TikTok",
    "bulk create character animations",
    "professional AI character animation",
    "best AI character animation tools",
    "AI character animation trends 2026",
    "make money with AI character videos",
    "animated mascot videos for brands",
    "create animated character videos",
    "Instagram character animation ideas",
    "automate character video production",
    "realistic character dance movements",
    "AI mascot creator comparison",
    "character video marketing trends",
    "AI dance videos for social media marketing",
    "animate characters with AI",
    "TikTok mascot dance trends",
    "fast AI character animation",
    "high quality AI mascot videos",
    "character dance video maker reviews",
    "future of animated marketing content",
    "monetize character animation content",
    "character animation for product demos",
    "AI character animation tutorial"
  ]
}
```

### 预期成本
~$0.45 (25 keywords × ~$0.018)

### 输出字段
- `keyword` - 关键词
- `search_volume` - 月搜索量
- `competition` - 竞争度 (0-1)
- `cpc` - 点击成本
- `keyword_difficulty` - SEO 难度 (0-100)

---

## API 2: AI Keyword Data (LLM 搜索量) - Optional

### 目标
验证关键词在 AI 搜索引擎（ChatGPT, Perplexity）中的被查询频率

### Endpoint
`dataforseo.ai_keyword_data`

### 参数
```json
{
  "keywords": [
    "AI character animation",
    "character dance videos",
    "animated mascot creation",
    "AI video character animation",
    "character animation tools"
  ]
}
```

### 预期成本
~$0.30 (5 keywords × ~$0.06)

### 输出字段
- `keyword` - 关键词
- `ai_search_volume` - AI 搜索引擎查询量
- `ai_sources` - 被引用的 AI 数据源
- `trend_direction` - 趋势方向 (up/stable/down)

---

## API 3: LLM Mentions (AI 引用分析) - Optional

### 目标
分析关键词在 LLM 回答中的被提及频率和上下文

### Endpoint
`dataforseo.llm_mentions`

### 参数
```json
{
  "keywords": [
    "AI character animation",
    "character dance videos",
    "animated mascot creation",
    "AI video character animation",
    "character animation tools"
  ],
  "llm_sources": ["chatgpt", "perplexity", "claude"]
}
```

### 预期成本
~$0.75 (5 keywords × ~$0.15)

### 输出字段
- `keyword` - 关键词
- `mention_count` - 被提及次数
- `context_relevance` - 上下文相关性评分
- `recommended_tools` - LLM 推荐的工具列表

---

## 三级筛选标准

### Tier 1: 高价值关键词 (High-Volume)
- `search_volume` ≥ 1,000
- `keyword_difficulty` ≤ 60
- `competition` ≤ 0.7
- **目标**: 10-15 个关键词

### Tier 2: 中等价值关键词 (Mid-Tail)
- `search_volume` 500-999
- `keyword_difficulty` ≤ 70
- **目标**: 15-20 个关键词

### Tier 3: 长尾关键词 (Long-Tail)
- `search_volume` 100-499
- `keyword_difficulty` ≤ 50
- `competition` ≤ 0.5
- **目标**: 20-30 个关键词

---

## 方向级聚合规则

### 聚合维度
1. **意图模式** - 来自 Phase 0.5 的 8 种模式
2. **产品映射** - alici.ai 核心功能对应
3. **数据强度** - 搜索量 × 商业价值

### 聚合公式
```
Direction Score = (Search Volume × 0.4) + (Business Value × 0.3) + (Low Difficulty × 0.3)

Business Value:
- Tier 1 (Industry Use Case, Tutorial, Platform-Specific) = 10
- Tier 2 (Workflow, Quality) = 7
- Tier 3 (Comparison, Trend, Business Opportunity) = 4

Low Difficulty = (100 - keyword_difficulty) / 100
```

### Top 10 方向筛选
- 按 Direction Score 降序排列
- 取前 10 个方向
- 每个方向包含 3-8 个关键词

---

## 下一步: Phase 2.5 Scope 裁剪

输入: 60-80 个验证后的关键词
输出: 10 个方向
- Gate 1: Demand validation (volume ≥ 100)
- Gate 2: Business alignment (产品映射明确)
- Gate 3: Cluster deduplication (去重相似方向)
