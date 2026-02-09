# SmartLauncher v2.2 - 手动路线 (Manual Route)

> 适用场景: 已有明确标题/方向，或参考模式需要扩展调研

---

## 流程概览

```
手动路线流程 (v2.2 Updated - 5 步 + 参考模式扩展):
┌─────────────────────────────────────────────────────────────────┐
│ Step 1: 收集用户意图                                             │
│ ├── 想要的标题 (或标题方向)                                      │
│ ├── 想要的方向/角度                                              │
│ ├── 相关素材 (URL / 参考文章 / 关键词)                           │
│ └── 是否使用 Seed Mode 发现更多方向?                             │
│                      ↓                                          │
│ [可选] Step 1.5: 参考模式扩展调研 (v2.2 NEW) ⭐                  │
│ ├── 触发条件: 用户选择"参考"意图 + 手动模式                      │
│ ├── 调用 growth-topic-scout 扩展方向                            │
│ ├── 调用 DataForSEO 验证关键词                                  │
│ └── 建议 2-3 个扩展方向供用户选择                                │
│                      ↓                                          │
│ [可选] Step 1.6: Seed Mode 配置编辑                              │
│ ├── 编辑 Mission Config                                          │
│ ├── 调整竞品列表                                                 │
│ └── 设置 scope 约束                                              │
│                      ↓                                          │
│ Step 2: DataForSEO 数据验证 (强制)                               │
│ ├── 搜索量查询                                                   │
│ ├── 竞品分析                                                     │
│ └── 用户确认数据 (可调整关键词)                                  │
│                      ↓                                          │
│ Step 3: 识别写作方向 (路由决策)                                   │
│ ├── Tool Showdown → blog-list-writer (showdown mode)            │
│ ├── Listicle → blog-list-writer                                 │
│ ├── Tutorial → blog-tutorial-writer                              │
│ └── Case Study → case-roundup-writer                             │
│                      ↓                                          │
│ Step 4: 标题确认                                                 │
│ ├── 基于 growth-topic-scout 生成 5+ 标题选项                     │
│ ├── (如使用 Seed Mode) 展示 Title Lock 验证结果                  │
│ └── 用户选择或自定义                                             │
│                      ↓                                          │
│ Step 5: 确认执行                                                 │
│ ├── 显示完整配置摘要                                             │
│ ├── 显示意图约束配置 (v2.2 NEW)                                 │
│ └── 用户确认后进入执行阶段                                       │
│                      ↓                                          │
│ [执行阶段] Writer → Editor Gate → AEO → Framer → Preview         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Step 1: 收集用户意图

### 1.1 问卷设计

```json
{
  "questions": [
    {
      "question": "你想写什么标题？(可以是大概方向或完整标题)",
      "header": "Title",
      "multiSelect": false,
      "options": [
        {
          "label": "工具对比 (A vs B)",
          "description": "例: Sora vs Runway 对比"
        },
        {
          "label": "榜单/评测",
          "description": "例: 2026 年最佳 AI 视频工具"
        },
        {
          "label": "教程/指南",
          "description": "例: 如何用 AI 生成视频"
        },
        {
          "label": "案例/洞察",
          "description": "例: Kling Motion Control 使用案例"
        }
      ]
    }
  ]
}
```

### 1.2 追问素材

用户选择方向后，追问具体内容:

```json
{
  "questions": [
    {
      "question": "请提供更多细节",
      "header": "Details",
      "multiSelect": false,
      "options": [
        {
          "label": "我有具体标题想法",
          "description": "直接输入完整标题"
        },
        {
          "label": "我有参考 URL",
          "description": "竞品文章或 YouTube 视频链接"
        },
        {
          "label": "我有关键词",
          "description": "主要关键词或长尾词"
        },
        {
          "label": "只有大概方向",
          "description": "需要系统帮我发掘选题"
        }
      ]
    }
  ]
}
```

### 1.3 收集结果格式

```json
{
  "user_intent": {
    "direction": "工具对比",
    "title_idea": "Sora vs Runway 对比",
    "reference_urls": ["https://example.com/article"],
    "keywords": ["sora vs runway", "ai video generator"],
    "notes": "用户额外说明..."
  }
}
```

### 1.4 Seed Mode 选项

当用户只有方向但缺乏具体标题时，询问是否使用 Seed Mode:

```json
{
  "questions": [
    {
      "question": "是否需要发现更多选题方向？",
      "header": "Seed",
      "multiSelect": false,
      "options": [
        {
          "label": "直接写作",
          "description": "使用已有方向，跳过选题发现"
        },
        {
          "label": "使用 Seed Mode 发现方向",
          "description": "通过竞品锚定漏斗发现 2 个高潜力方向 (D1)"
        },
        {
          "label": "使用 Diversity Seed Mode (v2)",
          "description": "通过多策略发散 + 语义去重发现 3 个高潜力方向 (D2)"
        }
      ]
    }
  ]
}
```

---

## Step 1.5: 参考模式扩展调研 (v2.2 NEW) ⭐

当用户在 Step 1.5 (素材使用意图) 选择**参考**意图，并选择**手动模式**时，进入此步骤。

### 触发条件

```python
def should_trigger_reference_expansion(intent, mode):
    """
    判断是否触发参考模式扩展调研
    """
    return intent == "参考" and mode == "手动"
```

### 1.5.1 扩展调研流程

```
参考模式扩展调研:
┌─────────────────────────────────────────────────────────────────┐
│ 1. 调用 growth-topic-scout                                       │
│    ├── 输入: 用户提供的 URL + 方向                               │
│    ├── 模式: Mode B (关键词矩阵)                                │
│    └── 输出: 10-20 个相关关键词                                  │
│                      ↓                                          │
│ 2. 调用 DataForSEO 验证                                          │
│    ├── 验证关键词搜索量                                          │
│    ├── 验证竞争难度                                              │
│    └── 筛选高潜力关键词                                          │
│                      ↓                                          │
│ 3. 生成扩展方向建议                                              │
│    ├── 建议 1: 原素材扩展 (基于原内容深挖)                       │
│    ├── 建议 2: 横向拓展 (相关主题覆盖)                           │
│    └── 建议 3: 纵向深入 (特定场景聚焦)                           │
│                      ↓                                          │
│ 4. 用户选择扩展方向                                              │
│    └── 继续进入 Step 2 (DataForSEO 数据验证)                    │
└─────────────────────────────────────────────────────────────────┘
```

### 1.5.2 扩展方向选择问卷

```json
{
  "questions": [
    {
      "question": "基于参考素材，我发现以下扩展方向，您想选择哪个？",
      "header": "Expansion",
      "multiSelect": false,
      "options": [
        {
          "label": "原素材扩展",
          "description": "深挖原内容，添加更多工具/场景/案例"
        },
        {
          "label": "横向拓展",
          "description": "覆盖相关主题，扩大内容范围"
        },
        {
          "label": "纵向深入",
          "description": "聚焦特定场景，提供深度分析"
        }
      ]
    }
  ]
}
```

### 1.5.3 扩展调研配置

```yaml
reference_expansion:
  enabled: true

  # growth-topic-scout 配置
  topic_scout:
    mode: "B"                      # 关键词矩阵模式
    max_keywords: 20               # 最多 20 个关键词
    relevance_threshold: 0.7       # 相关性阈值

  # DataForSEO 验证配置
  dataforseo:
    min_volume: 100                # 最低搜索量
    max_difficulty: 0.6            # 最大难度
    verify_trend: true             # 验证趋势

  # 扩展方向配置
  directions:
    original_expansion:            # 原素材扩展
      add_tools: true
      add_scenarios: true
      add_cases: true
    horizontal:                    # 横向拓展
      cover_related_topics: true
      expand_scope: true
    vertical:                      # 纵向深入
      focus_scenario: true
      deep_analysis: true
```

### 1.5.4 扩展调研输出

```json
{
  "expansion_result": {
    "source_url": "https://...",
    "intent": "参考",
    "expansion_directions": [
      {
        "type": "original_expansion",
        "title": "原素材扩展: 添加 3 个新工具对比",
        "new_tools": ["Tool A", "Tool B", "Tool C"],
        "new_scenarios": ["Scene X", "Scene Y"],
        "estimated_word_count": 3500,
        "dataforseo_verified": true
      },
      {
        "type": "horizontal",
        "title": "横向拓展: 覆盖 AI 视频编辑工作流",
        "related_topics": ["AI editing", "workflow automation"],
        "estimated_word_count": 4000,
        "dataforseo_verified": true
      },
      {
        "type": "vertical",
        "title": "纵向深入: 聚焦 Motion Control 场景",
        "focus_area": "motion_control",
        "depth_level": "advanced",
        "estimated_word_count": 2500,
        "dataforseo_verified": true
      }
    ],
    "recommended": "original_expansion"
  }
}
```

---

## Step 1.6: Seed Mode 配置编辑 (可选)

当用户选择 "使用 Seed Mode 发现方向" 时，进入此步骤。

### 1.6.1 Mission Config 编辑界面

展示并允许用户编辑 Mission Config:

```
┌─────────────────────────────────────────────────────────────────┐
│ 🌱 Seed Mode 配置                                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 种子词: [ai video tools 2026]                    [编辑]         │
│                                                                 │
│ 竞品博客 (5 个，默认):                                          │
│   1. invideo.io/blog                            [更换]         │
│   2. higgsfield.ai/blog                         [更换]         │
│   3. freepik.com/blog                           [更换]         │
│   4. blog.fal.ai                                [更换]         │
│   5. wavespeed.ai/blog                          [更换]         │
│                                                                 │
│ Scope 设置:                                                     │
│   语言: en                                       [更换]         │
│   地区: US                                       [更换]         │
│   受众: 内容创作者                               [更换]         │
│   验证深度: standard ($0.47)                     [更换]         │
│                                                                 │
│ 增长目标:                                                       │
│   目标: 流量 + 转化                              [更换]         │
│   产品: Video Studio                             [更换]         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.6.2 竞品编辑问卷

```json
{
  "questions": [
    {
      "question": "更换竞品博客？",
      "header": "Competitor",
      "multiSelect": false,
      "options": [
        {"label": "使用默认竞品池", "description": "invideo.io, higgsfield.ai, freepik.com, blog.fal.ai, wavespeed.ai"},
        {"label": "输入自定义竞品", "description": "输入 3–5 个竞品博客 URL"}
      ]
    }
  ]
}
```

### 1.6.3 验证深度选择

```json
{
  "questions": [
    {
      "question": "选择验证深度",
      "header": "Depth",
      "multiSelect": false,
      "options": [
        {"label": "Quick (~$0.10)", "description": "仅关键词验证，跳过 AEO"},
        {"label": "Standard (~$0.47) (Recommended)", "description": "关键词 + SERP 验证"},
        {"label": "Deep (~$1.52)", "description": "完整 AEO 验证 + LLM 分析"}
      ]
    }
  ]
}
```

### 1.6.4 确认配置

配置完成后，展示完整 Mission Config 并请求确认:

```json
{
  "questions": [
    {
      "question": "确认 Seed Mode 配置？",
      "header": "Confirm",
      "multiSelect": false,
      "options": [
        {"label": "确认，开始选题发现", "description": "运行 Seed Mode 漏斗"},
        {"label": "返回修改", "description": "调整配置"}
      ]
    }
  ]
}
```

### 1.6.5 Seed Mode 执行

确认后，调用 `growth-topic-scout v2.3` 的 Seed 模式：
- 选择「使用 Seed Mode 发现方向」→ Mode D1（竞品锚定，输出 2 个方向）
- 选择「使用 Diversity Seed Mode (v2)」→ Mode D2（多样性引擎，输出 3 个方向）

```
═══════════════════════════════════════════════════
▶ 执行 Seed Mode 选题漏斗
═══════════════════════════════════════════════════

[D1/6] Phase 0: Mission Config 已保存...
[D1/6] Phase 0.5: 抓取竞品博客...
      ├── invideo.io: 15 篇文章
      ├── higgsfield.ai: 22 篇文章
      ├── freepik.com: 16 篇文章
      ├── blog.fal.ai: 12 篇文章
      └── wavespeed.ai: 14 篇文章
      发现 6 种意图模式 ✓

[D1/6] Phase 1: 意图模式扩散...
      └── 生成 64 个待验证关键词 ✓

[D1/6] Phase 2: DataForSEO 验证...
      ├── 高优先级: 10 个
      ├── 中优先级: 19 个
      └── 长尾: 35 个

[D1/6] Phase 2.5: Scope 裁剪...
      └── 64 → 10 个方向 ✓

[D1/6] Phase 3: Title Lock...
      └── 2 个可执行方向 ✓

═══════════════════════════════════════════════════
✅ Seed Mode 完成
═══════════════════════════════════════════════════

-----------------------------------------

[D2/7] Phase 0: Mission Config + Diversity Config ✓
[D2/7] Phase 0.2: Seed 解构（5 维 + query seeds）✓
[D2/7] Phase 1: 多策略发散（~45 topics）✓
[D2/7] Phase 2: 语义聚类去重 + 多样性门禁（avg_sim<0.50）✓
[D2/7] Phase 3: DataForSEO 验证（8-15 候选）✓
[D2/7] Phase 4: Portfolio Scoring（SEO+AEO+diversity_bonus）✓
[D2/7] Phase 5: Title Lock → 3 个可执行方向 ✓
```

### 1.6.6 方向选择

Seed Mode 完成后，展示 2 个方向（D1）或 3 个方向（D2）供用户选择:

```
┌─────────────────────────────────────────────────────────────────┐
│ 📊 Seed Mode 结果: 2-3 个可执行方向                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 🥇 方向 1: AI Video Tool Comparisons                            │
│    ─────────────────────────────────────────────                │
│    标题: Sora 2 vs Runway Gen-4 vs Kling 2.6: Best in 2026     │
│    SEO: 89 | AEO: 90 | 综合: Excellent                          │
│    搜索量: 12,200 | 趋势: ↑ 上升                                │
│    推荐 Writer: blog-list-writer (tool_showdown)                │
│                                                                 │
│ 🥈 方向 2: Tutorial - AI Video Creation                         │
│    ─────────────────────────────────────────────                │
│    标题: How to Create AI Videos for YouTube in 2026            │
│    SEO: 82 | AEO: 78 | 综合: High                               │
│    搜索量: 8,500 | 趋势: → 平稳                                 │
│    推荐 Writer: blog-tutorial-writer                            │
│                                                                 │
│ 🥉 方向 3 (D2 可选): Troubleshooting - Fix AI-looking Videos     │
│    ─────────────────────────────────────────────                │
│    标题: Why Your Sora Videos Look \"AI-ish\" (and How to Fix It)│
│    SEO: 76 | AEO: 84 | 综合: High (AEO-first)                   │
│    搜索量: 1,200 | 趋势: ↑ 上升                                 │
│    推荐 Writer: blog-tutorial-writer                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

```json
{
  "questions": [
    {
      "question": "选择要写的方向",
      "header": "Direction",
      "multiSelect": false,
      "options": [
        {"label": "方向 1: AI Video Tool Comparisons", "description": "SEO 89 | AEO 90 | blog-list-writer"},
        {"label": "方向 2: Tutorial - AI Video Creation", "description": "SEO 82 | AEO 78 | blog-tutorial-writer"},
        {"label": "两个都写 (批量模式)", "description": "依次执行两个方向"}
      ]
    }
  ]
}
```

用户选择后，继续进入 Step 2 (DataForSEO 数据验证)，但使用 Seed Mode 已验证的数据。

---

## Step 2: DataForSEO 数据验证 (强制)

### 2.1 关键词提取

从用户输入自动提取关键词:

```python
def extract_keywords(user_intent):
    """
    从用户意图提取待验证的关键词
    """
    keywords = []

    # 从标题提取
    if user_intent.get("title_idea"):
        keywords.append(user_intent["title_idea"].lower())

    # 用户提供的关键词
    if user_intent.get("keywords"):
        keywords.extend(user_intent["keywords"])

    # 自动扩展相关词
    expanded = expand_related_keywords(keywords)

    return list(set(keywords + expanded))[:10]  # 最多 10 个
```

### 2.2 DataForSEO 查询

```
mcp__dataforseo__keywords_data_search_volume
├── keywords: ["sora vs runway", "sora 2", "runway gen-4", ...]
├── location_code: 2840  // US
└── language_code: "en"
```

### 2.3 数据展示 (强制)

**必须**向用户展示以下数据并获得确认:

```
┌─────────────────────────────────────────────────────────────────┐
│ 📊 关键词数据验证                                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ | 关键词              | 月搜索量 | 趋势   | CPC    | 难度  |    │
│ |---------------------|----------|--------|--------|-------|    │
│ | sora vs runway      | 4,800    | ↑ 上升 | $2.45  | 中    |    │
│ | ai video comparison | 2,100    | → 平稳 | $1.80  | 中    |    │
│ | runway gen 4        | 3,200    | ↑ 上升 | $2.10  | 低    |    │
│ | sora 2 review       | 1,500    | ↑ 上升 | $1.95  | 中    |    │
│                                                                 │
│ 🎯 推荐主关键词: "sora vs runway"                                │
│    原因: 高搜索量 (4,800) + 上升趋势 + 中等竞争                   │
│                                                                 │
│ 📈 搜索量评估:                                                   │
│    ✅ >= 2,000: 高需求，推荐优先                                 │
│    ⚠️ 1,000-2,000: 中等需求，可选                               │
│    ❌ < 1,000: 低需求，建议调整关键词                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.4 用户确认问卷

```json
{
  "questions": [
    {
      "question": "确认关键词数据？",
      "header": "Confirm",
      "multiSelect": false,
      "options": [
        {
          "label": "确认，使用推荐关键词",
          "description": "使用 'sora vs runway' 作为主关键词"
        },
        {
          "label": "修改主关键词",
          "description": "选择其他关键词或输入新关键词"
        },
        {
          "label": "添加更多关键词",
          "description": "扩展查询范围"
        }
      ]
    }
  ]
}
```

### 2.5 确认检查清单

手动路线 Step 2 **必须**完成以下确认:

```
DataForSEO 确认清单:
[x] 主关键词搜索量 >= 500 (或用户明确接受低搜索量)
[x] 趋势不是下降
[x] 用户已确认关键词选择
[x] 数据已展示给用户
```

---

## Step 3: 识别写作方向 (路由决策)

### 3.1 自动识别规则

基于用户输入和关键词自动检测写作方向:

| 检测信号 | 写作方向 | 路由目标 |
|----------|----------|----------|
| 包含 "vs" / "对比" / "对决" / "comparison" | Tool Showdown | `blog-list-writer` (mode: tool_showdown) |
| 包含 "best" / "top N" / "榜单" / 数字开头 | Listicle | `blog-list-writer` (mode: standard) |
| 包含 "how to" / "如何" / "教程" / "guide" | Tutorial | `blog-tutorial-writer` |
| 包含 "案例" / "case" / "roundup" / "汇总" | Case Study | `case-roundup-writer` |
| 无明确信号 | 询问用户 | → Step 3.5 |

### 3.2 检测逻辑

```python
def detect_writing_direction(title_idea, keywords):
    """
    自动检测写作方向
    """
    text = (title_idea + " " + " ".join(keywords)).lower()

    # Tool Showdown
    showdown_signals = ["vs", "对比", "对决", "comparison", "versus"]
    if any(signal in text for signal in showdown_signals):
        return "tool_showdown", "blog-list-writer", "tool_showdown"

    # Listicle
    listicle_signals = ["best", "top ", "榜单", "评测"]
    if any(signal in text for signal in listicle_signals):
        return "listicle", "blog-list-writer", "standard"

    # 数字开头检测
    import re
    if re.match(r'^\d+\s', title_idea):
        return "listicle", "blog-list-writer", "standard"

    # Tutorial
    tutorial_signals = ["how to", "如何", "教程", "guide", "指南"]
    if any(signal in text for signal in tutorial_signals):
        return "tutorial", "blog-tutorial-writer", None

    # Case Study
    case_signals = ["案例", "case", "roundup", "汇总", "洞察"]
    if any(signal in text for signal in case_signals):
        return "case_study", "case-roundup-writer", None

    # 无法确定
    return None, None, None
```

### 3.3 自动识别成功

如果自动识别成功，直接显示结果:

```
┌─────────────────────────────────────────────────────────────────┐
│ 📝 写作方向识别                                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 检测到: "Sora vs Runway" 包含 "vs"                              │
│                                                                 │
│ ✅ 写作方向: Tool Showdown (工具对决)                            │
│ ✅ Writer: blog-list-writer                                     │
│ ✅ Mode: tool_showdown                                          │
│ ✅ 输出字数: 2,500-3,500 词                                      │
│                                                                 │
│ 特性:                                                           │
│ - 10 固定 Headings 高对比度结构                                  │
│ - Snapshot 表格 + Scorecard 表格                                │
│ - Category Winners (Choose/Avoid)                               │
│ - Decision Tree (If/Then)                                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.4 Step 3.5: 手动选择 (当自动识别不确定)

如果无法自动识别，询问用户:

```json
{
  "questions": [
    {
      "question": "这篇文章的类型是？",
      "header": "Type",
      "multiSelect": false,
      "options": [
        {
          "label": "工具对决 (Tool Showdown)",
          "description": "A vs B vs C 高对比度对比，帮读者做决策"
        },
        {
          "label": "榜单/评测 (Listicle)",
          "description": "N Best X 综合评测，覆盖多个选项"
        },
        {
          "label": "教程/指南 (Tutorial)",
          "description": "How to X 步骤教学，帮读者学技能"
        },
        {
          "label": "案例汇总 (Case Study)",
          "description": "多个案例展示洞察，快速分享发现"
        }
      ]
    }
  ]
}
```

---

## Step 4: 标题确认

### 4.1 调用 growth-topic-scout

基于已确认的关键词和写作方向，调用 growth-topic-scout 生成标题:

```
growth-topic-scout 输入:
├── keywords: ["sora vs runway", ...]
├── direction: "tool_showdown"
├── search_volume: 4800
└── trend: "上升"
```

### 4.2 生成 5+ 标题选项

```json
{
  "questions": [
    {
      "question": "选择文章标题",
      "header": "Title",
      "multiSelect": false,
      "options": [
        {
          "label": "Sora 2 vs Runway Gen-4 vs Kling 2.6: Which AI Video Model Wins in 2026?",
          "description": "Showdown 对比式 | 搜索量: 4,800 | CTR 预测: 高"
        },
        {
          "label": "3 Best AI Video Generators Compared: Sora, Runway, Kling (2026)",
          "description": "Listicle 式 | 搜索量: 2,100 | CTR 预测: 中高"
        },
        {
          "label": "Sora vs Runway: The Ultimate 2026 Comparison Guide",
          "description": "对比指南式 | 搜索量: 3,200 | CTR 预测: 中高"
        },
        {
          "label": "Sora vs Runway vs Kling: Which Should You Choose in 2026?",
          "description": "问题式 | 搜索量: 4,800 | CTR 预测: 高"
        }
      ]
    }
  ]
}
```

### 4.3 标题公式验证

生成的标题必须符合 TITLE_FORMULAS.md 中的 37 种公式之一:

| 公式 ID | 公式 | 示例 |
|---------|------|------|
| showdown-1 | [A] vs [B] vs [C]: Which [Category] Wins? | Sora vs Runway vs Kling: Which AI Video Model Wins? |
| listicle-1 | [N] Best [Category] in [Year] | 10 Best AI Video Generators in 2026 |
| howto-1 | How to [Action] with [Tool] in [Time] | How to Create AI Videos with Sora in 10 Minutes |

---

## Step 5: 确认执行

### 5.1 配置摘要

展示完整配置，等待用户确认:

```
┌─────────────────────────────────────────────────────────────────┐
│ ✅ 准备就绪 - 配置摘要                                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 📌 标题:                                                        │
│    Sora 2 vs Runway Gen-4 vs Kling 2.6: Which Wins in 2026?    │
│                                                                 │
│ 📊 数据验证:                                                    │
│    主关键词: sora vs runway                                     │
│    月搜索量: 4,800                                              │
│    趋势: ↑ 上升                                                 │
│    数据来源: DataForSEO                                         │
│                                                                 │
│ 📝 写作配置:                                                    │
│    类型: Tool Showdown                                          │
│    Writer: blog-list-writer (mode: tool_showdown)               │
│    目标字数: 2,500-3,500 词                                      │
│    AEO 目标: >= 75                                              │
│                                                                 │
│ 🔧 执行流程:                                                    │
│    Writer → Editor Gate → AEO → Improver → Framer → Preview     │
│                                                                 │
│ ⏱️ 预计输出:                                                    │
│    /reports/2026-01-23-sora-vs-runway-vs-kling/                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 确认问卷

```json
{
  "questions": [
    {
      "question": "确认开始写作？",
      "header": "Start",
      "multiSelect": false,
      "options": [
        {
          "label": "确认，开始写作",
          "description": "进入全自动执行阶段，无需进一步干预"
        },
        {
          "label": "返回修改标题",
          "description": "重新选择或自定义标题"
        },
        {
          "label": "返回修改关键词",
          "description": "调整 DataForSEO 关键词验证"
        },
        {
          "label": "取消",
          "description": "取消本次写作任务"
        }
      ]
    }
  ]
}
```

---

## 执行阶段

用户确认后，进入全自动执行阶段。详见 SKILL.md "执行阶段 (两条路线共享)" 章节。

```
═══════════════════════════════════════════════════
▶ 进入全自动执行模式，无需进一步干预
═══════════════════════════════════════════════════

Step 1: 素材准备 (如有 URL)
Step 2: 内容生成 (blog-list-writer, mode: tool_showdown)
Step 3: Editor Gate (强制)
Step 3.5: Writer Feedback Loop (如需要)
Step 4: 质量评估 (aeo-analyzer)
Step 5: 自动改进 (如需要)
Step 6: 竞品验证 (competitive-validator)
Step 7: 输出生成 (Framer JSON + Preview HTML)
```

---

## 验证清单

手动路线执行前，确保以下检查全部通过:

- [ ] Step 1: 用户已提供标题方向或具体标题
- [ ] Step 2: DataForSEO 数据已展示
- [ ] Step 2: 用户已确认关键词选择
- [ ] Step 2: 主关键词搜索量 >= 500 (或用户明确接受)
- [ ] Step 3: 写作方向已确定 (自动或用户选择)
- [ ] Step 3: Writer 和 Mode 已确定
- [ ] Step 4: 用户已从 5+ 选项中选择标题 (或自定义)
- [ ] Step 5: 配置摘要已展示
- [ ] Step 5: 用户已确认开始写作

---

## 与全自动路线的区别

| 环节 | 手动路线 | 全自动路线 |
|------|---------|-----------|
| 输入 | 标题/方向 + 可选素材 | URL (必需) |
| **推荐意图** | **参考** (可扩展) | **洗稿** (快速执行) |
| **参考模式扩展** | **有** (Step 1.5 扩展调研) | **无** (推荐切换手动) |
| DataForSEO | 展示数据，用户确认 | 自动验证，不展示 |
| 写作方向 | 自动识别 + 用户可选 | 自动决策 |
| 标题选择 | 用户从 5+ 选项中选择 | 自动选择最佳 |
| 配置确认 | 展示摘要，用户确认 | 无需确认 |
| 执行过程 | 每步可中断 | 完全无需干预 |
| **意图约束** | **reference_mode** (宽松) | **rewrite_mode** (严格) |

---

## Changelog

### v2.2 (2026-01-26)

**参考模式扩展调研: 意图驱动的深度探索**

1. **Step 1.5 参考模式扩展调研 (NEW)**:
   - 触发条件: 用户选择"参考"意图 + 手动模式
   - 调用 growth-topic-scout 扩展方向
   - 调用 DataForSEO 验证关键词
   - 建议 2-3 个扩展方向供用户选择

2. **扩展方向类型**:
   - 原素材扩展: 深挖原内容，添加更多工具/场景/案例
   - 横向拓展: 覆盖相关主题，扩大内容范围
   - 纵向深入: 聚焦特定场景，提供深度分析

3. **扩展调研配置**:
   - `reference_expansion.enabled` - 启用参考模式扩展
   - `topic_scout.mode: "B"` - 关键词矩阵模式
   - `dataforseo.min_volume: 100` - 最低搜索量
   - `directions.*` - 三种扩展方向配置

4. **流程图更新**:
   - 新增 Step 1.5 参考模式扩展调研
   - Seed Mode 配置编辑移至 Step 1.6
   - Step 5 显示意图约束配置

5. **与全自动路线的区别更新**:
   - 手动路线 + 参考意图 = 扩展调研
   - 全自动路线 + 参考意图 = 推荐切换到手动模式

**预期效果**:
- 参考意图用户获得扩展方向建议
- 扩展方向经过 DataForSEO 验证
- 用户可选择最适合的扩展策略

---

*SmartLauncher v2.2 Manual Route - 5 步流程 × 参考模式扩展调研 × DataForSEO 确认 × 精细控制*
