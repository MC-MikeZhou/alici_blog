# SmartLauncher v2.2 - 全自动路线 (Full-Auto Route)

> 适用场景: 有竞品 URL 或 YouTube 视频，根据素材使用意图（洗稿/参考）执行

---

## 核心理念

```
全自动模式 v2.2 = 意图驱动执行
├── Step 1.5 意图前置 (v2.2 NEW): 用户明确选择"洗稿"或"参考"
├── 洗稿模式: 80%+ 保留原内容，禁止新增，品牌替换
├── 参考模式: 作为起点，可扩展，调用选题发现
├── 素材本地化: 自动抓取竞品中的图片等素材
├── 自动决策: 基于内容特征 + 意图约束自动选择 Writer
├── 质量保障: 必须通过 Editor Gate + invideo 洞察
└── Seed Mode 集成: 参考模式可选调用选题漏斗发现新方向
```

---

## 流程概览

```
全自动路线流程 (v2.2 Updated):
┌─────────────────────────────────────────────────────────────────┐
│ Step 1: 输入                                                     │
│ └── URL (竞品文章 / YouTube 视频)                                │
│                      ↓                                          │
│ Step 1.5: 素材使用意图 (v2.2 NEW) ⭐                             │
│ ├── Q: 你想如何使用这个素材？                                    │
│ ├── [A] 洗稿 → 启用 rewrite_mode 约束                           │
│ └── [B] 参考 → 启用 reference_mode 约束                         │
│                      ↓                                          │
│ Step 2: 快速问卷 (1-2 个问题)                                    │
│ ├── 目标: 帮人选择 / 教人做事 / 展示发现                         │
│ └── (可选) 产品聚焦: Alici AI 专属 / 中立多工具                  │
│                      ↓                                          │
│ Step 3: 内容分析 + 素材抓取                                      │
│ ├── 获取竞品内容 (WebFetch / fetch-transcript)                   │
│ ├── 抓取图片等素材到本地                                         │
│ ├── 分析内容结构和核心观点                                       │
│ ├── 根据 intent 应用约束配置 (v2.2 NEW)                         │
│ └── 自动选择 Writer + 生成 Brief                                 │
│                      ↓                                          │
│ Step 4: 全自动执行 (无需干预)                                    │
│ ├── Writer 执行 (根据 intent: 洗稿/参考)                        │
│ ├── 意图验证 (v2.2 NEW): 洗稿检查新增 / 参考检查扩展             │
│ ├── Editor Gate (强制 + invideo 洞察)                            │
│ ├── AEO Analyzer                                                 │
│ ├── Auto-Improver (如需要)                                       │
│ ├── Framer JSON                                                  │
│ └── Preview HTML                                                 │
│                      ↓                                          │
│ Step 5: 呈现结果                                                 │
│ └── 直接展示 Preview HTML + 报告摘要                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## Step 1: 输入

### 1.1 支持的输入类型

| 输入类型 | 示例 | 处理方式 |
|----------|------|----------|
| 竞品文章 URL | `https://competitor.com/blog/ai-video` | WebFetch 获取内容 |
| YouTube 视频 | `https://youtube.com/watch?v=xxx` | fetch-transcript 获取字幕 |
| 多个 URL | URL1 URL2 URL3 | 批量模式 (batch-processor) |

### 1.2 URL 检测

```python
def detect_url_type(url):
    """
    检测 URL 类型，决定处理方式
    """
    if is_youtube_url(url):
        return "youtube", "fetch-transcript"
    else:
        return "article", "webfetch"
```

---

## Step 1.5: 素材使用意图 (v2.2 NEW) ⭐

### 1.5.1 意图问卷

当检测到用户输入包含 URL 时，首先询问素材使用意图：

```json
{
  "questions": [
    {
      "question": "你想如何使用这个素材？",
      "header": "Intent",
      "multiSelect": false,
      "options": [
        {
          "label": "洗稿 (Recommended)",
          "description": "80%+ 保留原内容，品牌换成 Alici AI，禁止新增"
        },
        {
          "label": "参考",
          "description": "作为起点，可以深挖扩展、补充新内容"
        }
      ]
    }
  ]
}
```

### 1.5.2 洗稿模式配置 (intent = "洗稿")

```yaml
rewrite_mode:
  enabled: true
  constraints:
    preserve_structure: true       # 保持原结构
    no_new_tools: true             # 禁止新增工具
    no_new_scenarios: true         # 禁止新增场景
    brand_swap: "Alici AI"         # 品牌替换目标
    word_count_ratio: [0.8, 1.2]   # 字数约束 80%-120%
  validation:
    strict: true                   # 严格验证
    check_tool_list_match: true    # 验证工具列表与原素材一致
    check_scenario_match: true     # 验证测试场景与原素材一致
    check_word_count_range: true   # 验证字数在允许范围内
  recommendation:
    mode: "full_auto"              # 推荐全自动模式
    reason: "洗稿无需扩展调研，快速执行"
```

### 1.5.3 参考模式配置 (intent = "参考")

```yaml
reference_mode:
  enabled: true
  constraints:
    preserve_structure: false      # 可重组结构
    allow_new_tools: true          # 允许新增工具
    allow_expansion: true          # 允许扩展内容
    research_required: true        # 需要额外调研
  execution:
    call_growth_topic_scout: true  # 调用选题扩展
    call_dataforseo: true          # 验证关键词数据
    suggest_directions: true       # 建议扩展方向
  recommendation:
    mode: "manual"                 # 推荐手动模式
    alternative: "seed"            # 或 Seed 模式（需选题发现时）
    reason: "参考模式需确认扩展方向"
```

### 1.5.4 意图检测逻辑

```python
def should_ask_intent(user_input):
    """
    判断是否需要询问素材使用意图
    """
    # 包含 URL 时询问意图
    if contains_url(user_input):
        return True

    # 以下情况跳过意图问卷
    # - 用户未提供 URL（仅提供标题/方向）
    # - 用户使用 Seed Mode 触发词
    # - 用户使用直通命令 (/)
    return False

def apply_intent_constraints(intent, features):
    """
    根据意图应用约束配置
    """
    if intent == "洗稿":
        return {
            "mode_config": "rewrite_mode",
            "preserve_structure": True,
            "no_new_tools": True,
            "no_new_scenarios": True,
            "brand_swap": "Alici AI",
            "word_count_ratio": [0.8, 1.2],
            "strict_validation": True,
            "source_tools": features.get("compared_tools", []),
            "source_scenarios": features.get("test_scenarios", [])
        }
    elif intent == "参考":
        return {
            "mode_config": "reference_mode",
            "preserve_structure": False,
            "allow_new_tools": True,
            "allow_expansion": True,
            "research_required": True,
            "call_growth_topic_scout": True,
            "call_dataforseo": True
        }
```

---

## Step 2: 快速问卷 (1-2 个问题)

### 2.1 目标问卷

```json
{
  "questions": [
    {
      "question": "这篇文章的目标是？",
      "header": "Goal",
      "multiSelect": false,
      "options": [
        {
          "label": "帮人选择工具 (Recommended)",
          "description": "对比/榜单，帮读者做决策"
        },
        {
          "label": "教人做事",
          "description": "教程/指南，帮读者学技能"
        },
        {
          "label": "展示发现",
          "description": "新功能/趋势，快速分享洞察"
        }
      ]
    }
  ]
}
```

### 2.2 可选: 产品聚焦

仅当内容涉及工具推荐时询问:

```json
{
  "questions": [
    {
      "question": "产品植入方式？",
      "header": "Product",
      "multiSelect": false,
      "options": [
        {
          "label": "Alici AI 专属推荐",
          "description": "以 Alici AI 为主要推荐工具"
        },
        {
          "label": "中立多工具",
          "description": "公正对比多个工具"
        }
      ]
    }
  ]
}
```

---

## Step 3: 内容分析 + 素材抓取

### 3.1 获取竞品内容

**竞品文章**:
```python
def fetch_article_content(url):
    """
    获取竞品文章内容
    """
    content = webfetch(url)
    return {
        "title": extract_title(content),
        "body": extract_body(content),
        "headings": extract_headings(content),
        "images": extract_images(content),
        "key_points": extract_key_points(content)
    }
```

**YouTube 视频**:
```python
def fetch_youtube_content(url):
    """
    获取 YouTube 视频内容
    """
    transcript = fetch_transcript(url)
    return {
        "title": extract_video_title(url),
        "transcript": transcript,
        "key_points": extract_key_points_from_transcript(transcript),
        "timestamps": extract_timestamps(transcript)
    }
```

### 3.2 素材抓取到本地

**图片抓取流程**:
```python
def extract_and_save_assets(content, output_dir):
    """
    抓取竞品中的图片等素材到本地
    """
    assets = []

    for img in content.get("images", []):
        # 下载图片
        local_path = download_image(img["src"], output_dir)

        assets.append({
            "original_url": img["src"],
            "local_path": local_path,
            "alt_text": img.get("alt", ""),
            "context": img.get("context", "")
        })

    return assets
```

**保存路径**:
```
/reports/YYYY-MM-DD-{topic}/
├── /assets/
│   ├── source-image-1.png   # 抓取的竞品图片
│   ├── source-image-2.png
│   └── ...
├── 00-source-content.md      # 原始内容备份
└── 00-asset-manifest.json    # 素材清单
```

### 3.3 内容分析

```python
def analyze_content(content, goal):
    """
    分析内容结构，自动决策 Writer
    """
    # 检测内容特征
    features = {
        "has_comparison": detect_comparison_intent(content),
        "comparison_tool_count": count_compared_tools(content),  # v2.1.1 新增: 对比工具数量
        "compared_tools": extract_tool_list(content),            # v2.1.1 新增: 提取工具列表
        "has_list_format": detect_list_format(content),
        "has_tutorial_steps": detect_tutorial_structure(content),
        "word_count": count_words(content),
        "heading_count": len(content.get("headings", [])),
        "test_scenarios": extract_test_scenarios(content)        # v2.1.1 新增: 测试场景列表
    }

    # 基于目标 + 特征决策
    return auto_decide_writer(features, goal)

def count_compared_tools(content):
    """
    v2.1.1 新增: 统计内容中对比的工具数量
    检测方式:
    - 标题中的 "A vs B vs C" 模式
    - 内容中反复出现的工具名称
    - 对比表格中的工具列表
    """
    tools = extract_tool_list(content)
    return len(tools)

def extract_tool_list(content):
    """
    v2.1.1 新增: 提取内容中提及的工具列表
    返回: ["Runway", "Kling", ...]
    """
    # 从标题提取 (A vs B vs C)
    # 从章节标题提取 ([Tool] Overview)
    # 从对比表格提取
    pass

def extract_test_scenarios(content):
    """
    v2.1.1 新增: 提取原素材中的测试场景
    返回: ["text_animation", "camera_movement", ...]
    """
    pass
```

### 3.4 自动选择 Writer

```python
def auto_decide_writer(features, goal):
    """
    全自动模式下的 Writer 选择逻辑
    v2.1.1 更新: 根据工具数量区分 Tool Showdown vs Listicle
    """
    # 帮人选择 → 优先对比/榜单
    if goal == "帮人选择工具":
        if features["has_comparison"]:
            # v2.1.1 新增: 根据工具数量决定模式
            tool_count = features.get("comparison_tool_count", 0)

            if tool_count <= 3:
                # A vs B 或 A vs B vs C → Tool Showdown (洗稿)
                return {
                    "writer": "blog-list-writer",
                    "mode": "tool_showdown",
                    "reason": f"检测到 {tool_count} 个工具对比，使用 Tool Showdown 洗稿模式",
                    "rewrite_constraints": {
                        "tool_list_locked": True,      # 工具列表锁定为原素材
                        "scenarios_locked": True,       # 测试场景锁定为原素材
                        "source_tools": features.get("compared_tools", []),
                        "source_scenarios": features.get("test_scenarios", [])
                    }
                }
            else:
                # Top 5+, Top 8 等 → Listicle (可扩展)
                return {
                    "writer": "blog-list-writer",
                    "mode": "standard",
                    "reason": f"检测到 {tool_count} 个工具榜单，使用 Listicle 模式（可扩展）"
                }
        else:
            return {
                "writer": "blog-list-writer",
                "mode": "standard",
                "reason": "帮人选择目标，使用榜单模式"
            }

    # 教人做事 → 教程
    elif goal == "教人做事":
        return {
            "writer": "blog-tutorial-writer",
            "mode": None,
            "reason": "教程目标，使用 Tutorial Writer"
        }

    # 展示发现 → 案例汇总
    elif goal == "展示发现":
        return {
            "writer": "case-roundup-writer",
            "mode": None,
            "reason": "展示发现目标，使用 Case Roundup Writer"
        }

    # 默认
    return {
        "writer": "blog-tutorial-writer",
        "mode": None,
        "reason": "默认使用 Tutorial Writer"
    }
```

### 3.5 文章类型确认 (条件触发) - v2.1.1 NEW

当自动分析结果处于**边界情况**时，使用 AskUserQuestion 确认：

**触发条件** (任一满足时触发):
- 检测到对比意图，但工具数量 = 2-4 (边界区间)
- 视频同时包含教程和对比内容 (混合意图)
- 检测置信度 < 80%

**确认问卷**:
```json
{
  "questions": [
    {
      "question": "基于内容分析，我检测到以下特征: [特征列表]。您希望生成什么类型的文章？",
      "header": "ArticleType",
      "multiSelect": false,
      "options": [
        {
          "label": "Tool Showdown 深度对比 (Recommended)",
          "description": "80%+ 保留原视频结构和内容，不添加新工具/场景"
        },
        {
          "label": "Listicle 广度覆盖",
          "description": "可扩展更多工具和场景，创作自由度更高"
        },
        {
          "label": "Tutorial 教程",
          "description": "聚焦使用方法，step-by-step 教学"
        }
      ]
    }
  ]
}
```

**确认逻辑**:
```python
def should_confirm_article_type(features):
    """
    v2.1.1 新增: 判断是否需要用户确认文章类型
    """
    tool_count = features.get("comparison_tool_count", 0)
    has_comparison = features.get("has_comparison", False)
    has_tutorial = features.get("has_tutorial_steps", False)

    # 边界情况 1: 工具数量在 2-4 之间
    if has_comparison and 2 <= tool_count <= 4:
        return True, f"检测到 {tool_count} 个工具对比，处于边界区间"

    # 边界情况 2: 混合意图
    if has_comparison and has_tutorial:
        return True, "内容同时包含对比和教程元素"

    return False, None
```

**用户选择后的行为**:
- Tool Showdown → 启用洗稿约束 (见 3.6)
- Listicle → 允许扩展创作
- Tutorial → 路由到 blog-tutorial-writer

---

### 3.6 意图约束强制执行 - v2.2 Updated

根据 Step 1.5 用户选择的意图，强制执行对应约束：

**洗稿意图 (intent = "洗稿")** - 当用户选择洗稿时：

```yaml
rewrite_mode:
  enabled: true
  reference_ratio: 0.8  # 80%+ 参考原素材

  # v2.2 意图驱动约束
  strict_constraints:
    no_new_tools: true              # 禁止添加原素材未提及的工具
    no_new_scenarios: true          # 禁止添加原素材未覆盖的场景
    preserve_original_structure: true  # 保留原素材的章节结构
    word_count_ratio: [0.8, 1.2]    # 字数在原素材的 80%-120% 之间
    brand_swap: "Alici AI"          # 品牌替换目标

  # 验证检查
  validation:
    check_tool_list_match: true     # 验证工具列表与原素材一致
    check_scenario_match: true      # 验证测试场景与原素材一致
    check_word_count_range: true    # 验证字数在允许范围内
    strict: true                    # 严格模式
```

**参考意图 (intent = "参考")** - 当用户选择参考时：

```yaml
reference_mode:
  enabled: true

  # v2.2 意图驱动约束
  flexible_constraints:
    allow_new_tools: true           # 允许添加新工具
    allow_new_scenarios: true       # 允许添加新场景
    preserve_structure: false       # 可重组结构
    allow_expansion: true           # 允许扩展内容

  # 扩展调研
  research:
    call_growth_topic_scout: true   # 调用选题扩展
    call_dataforseo: true           # 验证关键词数据
    suggest_directions: true        # 建议扩展方向

  # 宽松验证
  validation:
    check_expansion_quality: true   # 检查扩展内容质量
    strict: false                   # 非严格模式
```

**验证逻辑** (v2.2 Updated):
```python
def validate_output_by_intent(draft, source_features, intent):
    """
    v2.2 更新: 根据意图验证输出是否符合约束
    """
    if intent == "洗稿":
        return validate_rewrite_output(draft, source_features)
    elif intent == "参考":
        return validate_reference_output(draft, source_features)


def validate_rewrite_output(draft, source_features):
    """
    洗稿意图: 严格验证，禁止新增
    """
    errors = []

    # 检查 1: 工具列表 (BLOCKING)
    source_tools = set(source_features.get("compared_tools", []))
    draft_tools = set(extract_tools_from_draft(draft))

    new_tools = draft_tools - source_tools
    if new_tools:
        errors.append({
            "type": "BLOCKING",
            "message": f"洗稿模式禁止添加新工具: {new_tools}",
            "action": "移除未在原素材中出现的工具"
        })

    # 检查 2: 测试场景 (WARNING)
    source_scenarios = set(source_features.get("test_scenarios", []))
    draft_scenarios = set(extract_scenarios_from_draft(draft))

    new_scenarios = draft_scenarios - source_scenarios
    if new_scenarios:
        errors.append({
            "type": "WARNING",
            "message": f"检测到新增场景: {new_scenarios}",
            "action": "建议移除或改用原素材中的场景"
        })

    # 检查 3: 字数范围 (WARNING)
    source_word_count = source_features.get("word_count", 0)
    draft_word_count = count_words(draft)
    ratio = draft_word_count / source_word_count if source_word_count > 0 else 0

    if ratio > 1.2:
        errors.append({
            "type": "WARNING",
            "message": f"字数 ({draft_word_count}) 超出原素材 ({source_word_count}) 的 120%",
            "action": "洗稿模式应保持 80-120% 字数范围，请精简内容"
        })

    # 检查 4: 品牌替换 (WARNING)
    if "Alici AI" not in draft:
        errors.append({
            "type": "WARNING",
            "message": "未检测到 Alici AI 品牌植入",
            "action": "确保品牌替换完成"
        })

    return errors


def validate_reference_output(draft, source_features):
    """
    参考意图: 宽松验证，检查扩展质量
    """
    errors = []

    # 检查 1: 扩展内容质量 (INFO)
    source_word_count = source_features.get("word_count", 0)
    draft_word_count = count_words(draft)

    if draft_word_count < source_word_count * 0.5:
        errors.append({
            "type": "INFO",
            "message": f"参考模式输出字数 ({draft_word_count}) 较原素材 ({source_word_count}) 少很多",
            "action": "参考模式允许扩展，考虑添加更多内容"
        })

    # 检查 2: 是否有新增内容 (INFO)
    source_tools = set(source_features.get("compared_tools", []))
    draft_tools = set(extract_tools_from_draft(draft))

    new_tools = draft_tools - source_tools
    if new_tools:
        errors.append({
            "type": "INFO",
            "message": f"参考模式已添加新工具: {new_tools}",
            "action": "新增内容符合参考模式预期"
        })

    return errors
```

**BLOCKING 处理**:
- 如果检测到新增工具 → Writer Feedback Loop → 要求移除
- 最多 2 轮修正，超过则 MANUAL_REVIEW

---

### 3.7 生成 Brief

基于分析结果自动生成 Topic Brief:

```json
{
  "auto_generated": true,
  "source_url": "https://competitor.com/...",
  "source_type": "article | youtube",
  "goal": "帮人选择工具",
  "writer_decision": {
    "writer": "blog-list-writer",
    "mode": "tool_showdown",
    "reason": "检测到对比内容"
  },
  "title": {
    "auto_selected": "Sora vs Runway vs Kling: Which AI Video Model Wins in 2026?",
    "alternatives": [...]
  },
  "key_points_from_source": [
    "Sora 2 支持 4K 视频生成",
    "Runway Gen-4 专注运动控制",
    "Kling 2.6 价格最优"
  ],
  "assets_extracted": {
    "images": 5,
    "local_path": "/reports/.../assets/"
  },
  "rewrite_mode": true,
  "reference_ratio": "80%+",

  "source_attribution": {
    "source_name": "InVideo",
    "source_url": "https://invideo.io/blog/...",
    "test_date": "2026-01-XX",
    "methodology_summary": "5 tools tested across 8 scenarios",
    "disclosure_required": true
  },

  "invideo_validation": {
    "opening_pattern_required": "P4_Reframe",
    "key_takeaways_position": "within_500_chars_of_h1",
    "citation_density_target": "5_per_1000_words",
    "l4_integrator_required": true
  }
}
```

---

## Step 4: 全自动执行

### 4.1 洗稿模式 (Rewrite Mode)

**核心原则**:
- 80%+ 内容参考竞品原始内容
- 保留核心观点和论据
- 重新组织结构和表达
- 添加 invideo 洞察优化
- **Source Attribution 强制** (v2.3 NEW)

#### 4.1.1 InVideo 原则约束 (v2.3 NEW) ⭐

```yaml
# 洗稿模式 InVideo 标准约束
rewrite_constraints:

  # Source Attribution 强制
  source_attribution:
    required: true
    format: "According to [Source]..."
    disclosure: "This analysis is based on [Source]. alici.ai did not independently verify all results."
    dedicated_section: true  # 必须有专门的 Source Attribution 章节
    position: "After Key Takeaways, before main content"

  # 禁止编造数据
  no_fabricated_data:
    enabled: true
    banned_patterns:
      - "X/5 ratings without G2/Capterra source"
      - "ranks #N without citation"
      - "We tested..." (use "According to [Source] testing...")
      - "Our analysis found..." (use source attribution)
      - "Based on our research..." (cite actual source)
    allowed_patterns:
      - "Rated X/5 on G2 (N+ reviews)"
      - "According to [Source] testing..."
      - "[Source] found that..."
      - "Based on [Source] analysis..."

  # 声明准确性验证
  validate_claim_accuracy:
    enabled: true
    check_items:
      - tool_versions: "Verify via WebSearch before writing"
      - pricing_data: "Must cite official source or review date"
      - feature_claims: "Must have source attribution"
      - ranking_claims: "Must cite source (G2, Capterra, etc.)"
    validation_report: true  # 生成验证报告

  # L4 Showdown Integrator 定位
  l4_integrator_positioning:
    enabled: true
    description: "竞品对决中定位为整合者，而非竞品之一"
    must_contain:
      - "don't have to pick just one"
      - "one platform" or "single platform"
      - "all in one" or "access to multiple"
    must_not_contain:
      - "best tool" (关于 alici.ai)
      - "better than" (贬低竞品)
      - "beats" (贬低竞品)
      - "winner" (自称获胜者)
```

#### 4.1.2 Source Attribution 模板 (v2.3 NEW)

洗稿模式输出**必须包含**以下 Source Attribution 章节:

```markdown
## About This Comparison

**Testing Source**: [Source Name] (e.g., "InVideo.io")
**Test Date**: [Date from source]
**Methodology**: [N] tools tested across [M] scenarios

**What Was Tested**:
- [Scenario 1]
- [Scenario 2]
- [Scenario 3]

**Disclosure**: This analysis is based on [Source]'s testing methodology.
alici.ai did not independently verify all results. Tool versions and
pricing may have changed since the original test date.

[Link to Original Source](URL)
```

#### 4.1.3 禁止虚假声明验证函数 (v2.3 NEW)

```python
def validate_claim_accuracy(draft, source_features):
    """
    v2.3 新增: 验证文章中的声明准确性
    返回 BLOCKING 或 WARNING 级别错误
    """
    errors = []

    # 检查 1: 评分声明 (BLOCKING)
    rating_pattern = r'(\d+\.?\d*)/5|(\d+\.?\d*)/10'
    ratings_found = re.findall(rating_pattern, draft)

    for rating in ratings_found:
        # 检查是否有来源引用
        if not has_source_attribution(draft, rating):
            errors.append({
                "type": "BLOCKING",
                "message": f"发现无来源评分: {rating}",
                "action": "添加来源 (如 'Rated {rating} on G2') 或删除评分"
            })

    # 检查 2: 排名声明 (BLOCKING)
    ranking_pattern = r'ranks?\s*#?\d+|#\d+\s*(tool|choice|pick)'
    rankings_found = re.findall(ranking_pattern, draft, re.IGNORECASE)

    for ranking in rankings_found:
        if not has_source_attribution(draft, ranking):
            errors.append({
                "type": "BLOCKING",
                "message": f"发现无来源排名声明: {ranking}",
                "action": "添加来源或移除排名声明"
            })

    # 检查 3: 第一人称测试声明 (WARNING)
    first_person_patterns = [
        r'We tested',
        r'Our analysis',
        r'Our research',
        r'We found that',
        r'In our testing'
    ]

    for pattern in first_person_patterns:
        if re.search(pattern, draft, re.IGNORECASE):
            errors.append({
                "type": "WARNING",
                "message": f"检测到第一人称测试声明: {pattern}",
                "action": "改为来源归属: 'According to [Source] testing...'"
            })

    # 检查 4: Source Attribution 章节存在 (BLOCKING)
    if "## About This Comparison" not in draft and "## Source Attribution" not in draft:
        errors.append({
            "type": "BLOCKING",
            "message": "缺少 Source Attribution 章节",
            "action": "在 Key Takeaways 后添加 'About This Comparison' 章节"
        })

    return errors
```

**洗稿流程**:
```
竞品内容
    ↓
┌─────────────────────────────────────────────┐
│ 洗稿转换:                                    │
│ 1. 提取核心观点 (保留 80%+)                  │
│ 2. 重新组织结构 (应用模板)                   │
│ 3. 改写表达 (避免重复)                       │
│ 4. 添加品牌内容 (CTA/产品植入)               │
│ 5. 应用 invideo 洞察 (开篇/标题优化)         │
└─────────────────────────────────────────────┘
    ↓
新文章 (结构优化 + 表达不同 + 核心一致)
```

### 4.2 Writer 执行

根据自动决策的 Writer 执行:

```
Writer 输入:
├── source_content: 竞品原始内容
├── key_points: 提取的核心观点
├── assets: 本地素材路径
├── brief: 自动生成的 Brief
└── rewrite_mode: true
```

### 4.3 Editor Gate (强制)

**必须通过 Editor Gate**，应用 invideo 洞察:

| Editor Module | 全自动模式行为 |
|---------------|---------------|
| Module 3: 开篇优化 | 应用 24 种 AEO 开篇模式 |
| Module 5: 格式演化 | 验证 37 种标题公式 |
| Module 6: E-E-A-T | 确保引用和权威性 |
| Module 9: CTA | 强制文末 CTA 卡片 |

### 4.4 执行流程

```
═══════════════════════════════════════════════════
▶ 全自动执行中，无需干预
═══════════════════════════════════════════════════

[1/7] 素材准备...
├── 获取竞品内容: ✓
├── 抓取图片 (5 张): ✓
└── 生成 Brief: ✓

[2/7] 内容生成...
├── Writer: blog-list-writer (tool_showdown)
├── 洗稿模式: 80%+ 参考
└── 输出: 01-article-draft.md ✓

[3/7] Editor Gate...
├── Module 3 开篇: ✓ Data Hook 模式
├── Module 5 格式: ✓ 标题符合公式
├── Module 6 E-E-A-T: ✓ 引用充足
├── Module 9 CTA: ✓ 文末 CTA 已添加
└── 输出: 01-article-edited.md ✓

[4/7] AEO 评分...
└── 分数: 78/100 ✓ (目标: 75)

[5/7] 竞品验证...
└── 超越率: 35% ✓ (目标: 30%)

[6/7] Framer 转换...
└── 输出: 06-article-final.json ✓

[7/7] Preview 生成...
└── 输出: 07-preview.html ✓

═══════════════════════════════════════════════════
✅ 全自动执行完成
═══════════════════════════════════════════════════
```

---

## Step 5: 呈现结果

### 5.1 结果摘要

```
┌─────────────────────────────────────────────────────────────────┐
│ ✅ 全自动执行完成                                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 📄 输出文件:                                                    │
│    /reports/2026-01-23-sora-vs-runway-vs-kling/                │
│    ├── 01-article-edited.md (2,847 词)                         │
│    ├── 06-article-final.json (Framer CMS)                      │
│    └── 07-preview.html ← 点击预览                              │
│                                                                 │
│ 📊 质量指标:                                                    │
│    AEO 分数: 78/100 ✓                                          │
│    竞品超越率: 35% ✓                                            │
│    Editor 检查: PASS ✓                                         │
│                                                                 │
│ 🖼️ 素材抓取:                                                    │
│    图片: 5 张 → /assets/                                        │
│                                                                 │
│ ⏱️ 执行统计:                                                    │
│    来源: https://competitor.com/...                             │
│    模式: 洗稿模式 (80%+ 参考)                                   │
│    Writer: blog-list-writer (tool_showdown)                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 直接展示 Preview

全自动模式完成后，自动打开或展示 `07-preview.html`。

---

## 批量模式

### 多 URL 输入

当检测到多个 URL 时，自动进入批量模式:

```
输入: URL1 URL2 URL3
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 批量模式启动                                                     │
│                                                                 │
│ 统一问卷 (1 次):                                                │
│ - 目标: 帮人选择 / 教人做事 / 展示发现                           │
│                                                                 │
│ 并行执行:                                                       │
│ ├── [1/3] URL1 → blog-list-writer → Editor → Preview ✓         │
│ ├── [2/3] URL2 → blog-tutorial-writer → Editor → Preview ✓     │
│ └── [3/3] URL3 → case-roundup-writer → Editor → Preview ✓      │
│                                                                 │
│ 批量报告:                                                       │
│ └── batch-summary.md                                            │
└─────────────────────────────────────────────────────────────────┘
```

### 批量输出结构

```
/reports/batch-2026-01-23-abc123/
├── 00-batch-manifest.json
├── 00-batch-summary.md
├── 2026-01-23-topic-1/
│   ├── 01-article-edited.md
│   └── 07-preview.html
├── 2026-01-23-topic-2/
│   └── ...
└── 2026-01-23-topic-3/
    └── ...
```

---

## 与手动路线的区别

| 环节 | 全自动路线 | 手动路线 |
|------|-----------|----------|
| 输入 | URL (必需) | 标题/方向 + 可选素材 |
| 问卷 | 1-2 个问题 | 5 步多轮确认 |
| DataForSEO | 自动验证，不展示 | 展示数据，用户确认 |
| 写作方向 | 自动决策 (基于内容特征) | 自动识别 + 用户可选 |
| 标题选择 | 自动选择最佳 | 用户从 5+ 选项中选择 |
| 内容生成 | 洗稿模式 (80%+ 参考) | 原创为主 |
| 素材处理 | 自动抓取到本地 | 按需处理 |
| 执行过程 | 完全无需干预 | 每步可中断 |
| 适合场景 | 高速批量、竞品改写 | 精细控制、原创内容 |

---

## 配置

### 洗稿模式配置 (v2.1.1 Updated)

```yaml
rewrite_mode:
  enabled: true
  reference_ratio: 0.8  # 80%+ 参考竞品
  preserve_key_points: true
  reorganize_structure: true
  apply_invideo_insights: true

  # v2.1.1 新增: 严格约束 (Tool Showdown 模式强制启用)
  strict_constraints:
    no_new_tools: true              # 禁止添加原素材未提及的工具
    no_new_scenarios: true          # 禁止添加原素材未覆盖的场景
    preserve_original_structure: true  # 尽量保留原素材的章节结构
    word_count_ratio: [0.8, 1.2]    # 字数在原素材的 80%-120% 之间

  # v2.1.1 新增: 验证检查
  validation:
    check_tool_list_match: true     # 验证工具列表与原素材一致
    check_scenario_match: true      # 验证测试场景与原素材一致
    check_word_count_range: true    # 验证字数在允许范围内

  # v2.1.1 新增: 边界检测配置
  boundary_detection:
    tool_count_boundary: [2, 4]     # 工具数量在此范围内触发确认
    confidence_threshold: 0.8       # 置信度低于此值触发确认
```

### 素材抓取配置

```yaml
asset_extraction:
  enabled: true
  image_formats: ["png", "jpg", "jpeg", "gif", "webp"]
  max_images: 20
  save_original_urls: true
  generate_manifest: true
```

---

## Seed Mode 集成 (v2.1 NEW)

### 全自动模式调用 Seed Mode

当全自动模式**没有具体 URL** 但有**种子词**时，可切换到 Seed Mode:

```
检测逻辑:
├── 有 URL? → 标准全自动流程 (洗稿模式)
└── 只有种子词/主题? → 询问是否使用 Seed Mode
    ├── 是 → 调用 growth-topic-scout v2.2 Mode D
    └── 否 → 使用 growth-topic-scout Mode B (关键词矩阵)
```

### Seed Mode 默认配置

全自动模式调用 Seed Mode 时使用的默认 Mission Config:

```json
{
  "seed": "[从用户输入提取]",
  "anchors": {
    "competitors": [
      "https://invideo.io/blog",
      "https://higgsfield.ai/blog",
      "https://freepik.com/blog"
    ]
  },
  "scope": {
    "language": "en",
    "geo": "US",
    "audience": "content_creators",
    "forbidden_zones": ["gambling", "adult"],
    "validation_depth": "standard"
  },
  "growth": {
    "goal": "traffic_and_conversion",
    "product_relevance": "video_studio",
    "conversion_priority": "balanced"
  }
}
```

### Seed Mode 问卷 (简化版)

全自动模式下，Seed Mode 只问 3 个问题:

```json
{
  "questions": [
    {
      "question": "你的种子词是什么？",
      "header": "Seed",
      "type": "text_input",
      "placeholder": "例: ai video tools 2026"
    },
    {
      "question": "目标受众是？",
      "header": "Audience",
      "multiSelect": false,
      "options": [
        {"label": "内容创作者 (Recommended)", "description": "YouTubers, TikTokers"},
        {"label": "营销人员", "description": "品牌营销、社媒运营"},
        {"label": "企业用户", "description": "企业级需求"}
      ]
    },
    {
      "question": "内容目标是？",
      "header": "Goal",
      "multiSelect": false,
      "options": [
        {"label": "流量 + 转化 (Recommended)", "description": "SEO + 产品转化"},
        {"label": "建立权威", "description": "行业领导力"}
      ]
    }
  ]
}
```

### Seed Mode 完成后

Seed Mode 完成后，自动进入执行阶段:

1. 展示 2 个可执行方向
2. 自动选择 Rank 1 方向
3. 根据 recommended_skill 调用对应 Writer
4. 进入标准执行流程 (Editor Gate → AEO → Framer → Preview)

```
Seed Mode 完成
    ↓
选择 Rank 1 方向
    ↓
调用 recommended_skill (如 blog-list-writer)
    ↓
使用 locked_title 作为标题
    ↓
使用 outline 作为文章结构
    ↓
进入执行阶段
```

---

## 验证清单

全自动路线执行前/后检查:

**执行前**:
- [ ] URL 有效且可访问
- [ ] 用户已回答目标问卷 (1-2 问题)

**执行中**:
- [ ] 内容已成功抓取
- [ ] 素材已保存到本地
- [ ] Writer 已自动选择
- [ ] Editor Gate 已通过

**执行后**:
- [ ] AEO 分数 >= 目标
- [ ] Preview HTML 已生成
- [ ] 结果摘要已展示

---

---

## Changelog

### v2.3 (2026-01-26)

**InVideo 原则系统化集成**

1. **Source Attribution 强制**:
   - 洗稿模式必须包含 "About This Comparison" 章节
   - 声明测试来源、日期、方法论
   - 添加披露声明 (alici.ai 未独立验证)

2. **禁止虚假声明**:
   - `no_fabricated_data` 配置块
   - 禁止无来源评分 (X/5)
   - 禁止无来源排名声明 (ranks #N)
   - 禁止第一人称测试声明 (We tested...)

3. **声明准确性验证**:
   - `validate_claim_accuracy()` 验证函数
   - BLOCKING: 无来源评分/排名
   - WARNING: 第一人称测试声明
   - BLOCKING: 缺少 Source Attribution 章节

4. **L4 Integrator 定位强化**:
   - 竞品对决中定位为整合者
   - must_contain: "don't have to pick", "one platform"
   - must_not_contain: "best tool", "better than", "beats"

5. **Topic Brief 扩展**:
   - 新增 `source_attribution` 字段
   - 新增 `invideo_validation` 配置

**预期效果**:
- 虚假声明检测: 无 → 自动验证
- Source Attribution: 可选 → 强制
- L4 植入法: 隐含 → 显式验证

---

### v2.2 (2026-01-26)

**意图前置架构: 素材使用意图问卷**

1. **Step 1.5 素材使用意图 (NEW)**:
   - 用户输入 URL 后首先询问意图
   - 两种意图: 洗稿 (80%+ 保留) / 参考 (可扩展)
   - 意图问卷位于模式选择前

2. **洗稿模式配置 (intent = "洗稿")**:
   - `preserve_structure: true` - 保持原结构
   - `no_new_tools: true` - 禁止新增工具
   - `no_new_scenarios: true` - 禁止新增场景
   - `brand_swap: "Alici AI"` - 品牌替换
   - `strict: true` - 严格验证

3. **参考模式配置 (intent = "参考")**:
   - `preserve_structure: false` - 可重组结构
   - `allow_new_tools: true` - 允许新增工具
   - `allow_expansion: true` - 允许扩展内容
   - `call_growth_topic_scout: true` - 调用选题扩展
   - `call_dataforseo: true` - 验证关键词数据

4. **意图验证逻辑 (NEW)**:
   - `validate_output_by_intent()` - 根据意图选择验证策略
   - `validate_rewrite_output()` - 洗稿严格验证
   - `validate_reference_output()` - 参考宽松验证

5. **流程图更新**:
   - 新增 Step 1.5 素材使用意图
   - 显示意图 → 约束配置分支

**预期效果**:
- 洗稿模式: Runway vs Kling → 严格 Tool Showdown
- 参考模式: 同视频 → 可扩展 Listicle + 选题发现
- 用户明确选择，不再隐式决定

---

### v2.1.1 (2026-01-26)

**洗稿模式优化: 解决 Runway vs Kling → Top 8 错误路由问题**

1. **Step 3.3 增强**:
   - 新增 `comparison_tool_count` 特征
   - 新增 `compared_tools` 工具列表
   - 新增 `test_scenarios` 场景列表

2. **Step 3.4 更新**:
   - 工具数量 ≤3 → Tool Showdown (洗稿模式)
   - 工具数量 >4 → Listicle (可扩展模式)
   - 返回 `rewrite_constraints` 配置

3. **Step 3.5 新增**: 文章类型确认
   - 边界情况触发用户确认
   - 提供 Tool Showdown / Listicle / Tutorial 选项

4. **Step 3.6 新增**: 洗稿约束验证
   - `validate_rewrite_output()` 函数
   - 检查新工具 (BLOCKING)
   - 检查新场景 (WARNING)
   - 检查字数范围 (WARNING)

5. **配置更新**:
   - `strict_constraints` 配置块
   - `validation` 检查配置
   - `boundary_detection` 边界检测配置

---

*SmartLauncher v2.2 Full-Auto Route - 意图前置 × 洗稿/参考模式 × 约束验证*
