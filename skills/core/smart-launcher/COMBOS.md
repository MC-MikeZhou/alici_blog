# SmartLauncher v2.0 - Writer 路由配置

> v2.0 简化: 4 种核心写作方向，与 Writer 路由表对齐

---

## 路由总览

| 写作方向 | Writer | Mode | 输出字数 | AEO 目标 |
|----------|--------|------|----------|----------|
| **Tool Showdown** | blog-list-writer | tool_showdown | 2,500-3,500 | 75 |
| **Listicle** | blog-list-writer | standard | 2,500-3,500 | 75 |
| **Tutorial** | blog-tutorial-writer | - | 1,800-2,500 | 75 |
| **Case Study** | case-roundup-writer | - | 300-600 | 70 |

---

## 1. Tool Showdown (工具对决)

### 路由决策矩阵 (v2.1.1 NEW)

| 检测信号 | 工具数量 | 模式 | 洗稿约束 |
|---------|---------|------|---------|
| vs, 对比, 对决 | ≤3 | tool_showdown | **80%+ 原素材，禁止新增** |
| vs, 对比, 对决 | 4 | tool_showdown | 边界情况，需用户确认 |
| vs, 对比, 对决 | >4 | standard | 可扩展更多工具 |

### 洗稿约束 (v2.1.1 NEW)

**当 Tool Showdown 模式 + 工具数量 ≤3 时，强制启用**:

| 约束项 | 规则 | 违反后果 |
|--------|------|---------|
| **工具列表** | = 原素材提及的工具 (不可新增) | ⛔ BLOCKING |
| **测试场景** | = 原素材覆盖的场景 (不可新增) | ⚠️ WARNING |
| **字数范围** | 原素材长度的 80-120% | ⚠️ WARNING |
| **章节结构** | 尽量保留原素材结构 | 建议 |

**验证时机**: Writer 输出后，进入 Editor Gate 前

**违反处理**:
- ⛔ BLOCKING → Writer Feedback Loop (最多 2 轮)
- ⚠️ WARNING → 自动修复或记录到报告

### 配置

```yaml
id: tool_showdown
name: "工具对决"
name_en: "Tool Showdown"

# 检测信号
detection_signals:
  - "vs"
  - "对比"
  - "对决"
  - "comparison"
  - "versus"

# v2.1.1 新增: 工具数量阈值
tool_count_threshold:
  showdown_max: 3        # ≤3 工具 → Tool Showdown 洗稿模式
  boundary: 4            # = 4 工具 → 边界情况，需确认
  listicle_min: 5        # ≥5 工具 → Listicle 可扩展模式

# Writer 配置
writer: "blog-list-writer"
writer_mode: "tool_showdown"
word_count: [2500, 3500]
aeo_target: 75

# 标题公式
title_formula: "[A] vs [B] vs [C]: Which [Category] Wins in [Year]?"
title_examples:
  - "Sora vs Runway vs Kling: Which AI Video Model Wins in 2026?"
  - "Midjourney vs DALL-E vs Stable Diffusion: Which AI Art Tool Wins?"

# 特性
features:
  - version_verification: true    # 自动触发工具版本验证
  - comparison_table: true        # Snapshot 表格
  - scorecard_table: true         # 评分卡
  - category_winners: true        # Choose/Avoid 格式
  - decision_tree: true           # If/Then 格式
  - cta_count: 3                  # 3 个产品 CTA

# v2.1.1 新增: 洗稿约束 (工具数量 ≤3 时自动启用)
rewrite_constraints:
  enabled_when: "tool_count <= 3"
  rules:
    - no_new_tools: true          # 禁止添加新工具
    - no_new_scenarios: true      # 禁止添加新场景
    - word_count_ratio: [0.8, 1.2]  # 字数范围
  validation:
    tool_list_check: "BLOCKING"   # 新工具 = 阻断
    scenario_check: "WARNING"     # 新场景 = 警告
    word_count_check: "WARNING"   # 超字数 = 警告
```

### 10 固定 Headings

```markdown
1. ## Key Takeaways
2. ## Quick Comparison (Snapshot Table)
3. ## [Tool A] Overview
4. ## [Tool B] Overview
5. ## [Tool C] Overview
6. ## Head-to-Head Comparison (Scorecard Table)
7. ## Category Winners (Choose/Avoid)
8. ## Who Should Use What (Decision Tree)
9. ## FAQ
10. ## Final Verdict
```

---

## 2. Listicle (榜单/评测)

### 配置

```yaml
id: listicle
name: "榜单/评测"
name_en: "Listicle"

# 检测信号
detection_signals:
  - "best"
  - "top"
  - "榜单"
  - "评测"
  - 数字开头 (e.g., "10 Best...")

# Writer 配置
writer: "blog-list-writer"
writer_mode: "standard"
word_count: [2500, 3500]
aeo_target: 75

# 标题公式
title_formula: "[N] Best [Category] in [Year]"
title_examples:
  - "10 Best AI Video Generators in 2026"
  - "15 Best AI Writing Tools for Content Creators (2026)"

# 特性
features:
  - methodology_section: true     # "How We Tested" 章节
  - evaluation_criteria: true     # 评测标准
  - pros_cons_table: true         # 优缺点
  - pricing_comparison: true      # 定价对比
  - key_takeaways_top: true       # 顶部 Key Takeaways
```

---

## 3. Tutorial (教程/指南)

### 配置

```yaml
id: tutorial
name: "教程/指南"
name_en: "Tutorial"

# 检测信号
detection_signals:
  - "how to"
  - "如何"
  - "教程"
  - "guide"
  - "指南"

# Writer 配置
writer: "blog-tutorial-writer"
writer_mode: null
word_count: [1800, 2500]
aeo_target: 75

# 标题公式
title_formula: "How to [Action] with [Tool/Method] in [Year]"
title_examples:
  - "How to Create AI Videos with Sora 2 in 2026"
  - "How to Generate Product Photos Using AI (Step-by-Step)"

# 特性
features:
  - step_by_step: true            # 分步骤教学
  - prompts_to_try: true          # 可复用 Prompt
  - aida_opening: true            # AIDA 开篇框架
  - citable_blocks: true          # 可引用区块
  - faq_count: [3, 5]             # 3-5 个 FAQ
```

---

## 4. Case Study (案例汇总)

### 配置

```yaml
id: case_study
name: "案例汇总"
name_en: "Case Study"

# 检测信号
detection_signals:
  - "案例"
  - "case"
  - "roundup"
  - "汇总"
  - "洞察"

# Writer 配置
writer: "case-roundup-writer"
writer_mode: null
word_count: [300, 600]
aeo_target: 70

# 标题公式
title_formula: "[Feature] Is Here: [Key Benefit]"
title_examples:
  - "Kling Motion Control Is Here: Your Videos Just Got Smoother"
  - "Sora 2 Is Here: 4K Video Generation in Minutes"

# 特性
features:
  - requires_material: true       # 必须有真实素材
  - case_count: [2, 5]            # 2-5 个案例
  - prompts_to_try: true          # 可复用 Prompt
  - data_hook_opening: true       # Data Hook 开篇
  - mini_faq: true                # Mini FAQ
```

---

## 路由决策逻辑

### 手动路线

1. 检测用户输入中的信号词
2. 匹配到信号 → 自动选择对应方向
3. 未匹配 → 询问用户选择

```python
def route_manual(user_input):
    text = user_input.lower()

    # 优先级: Tool Showdown > Listicle > Tutorial > Case Study
    if any(s in text for s in ["vs", "对比", "对决", "comparison"]):
        return "tool_showdown"

    if any(s in text for s in ["best", "top", "榜单"]) or re.match(r'^\d+', text):
        return "listicle"

    if any(s in text for s in ["how to", "如何", "教程", "guide"]):
        return "tutorial"

    if any(s in text for s in ["案例", "case", "roundup", "汇总"]):
        return "case_study"

    return None  # 需要询问用户
```

### 全自动路线 (v2.1.1 Updated)

1. 分析竞品内容特征
2. **检测工具数量** (v2.1.1 新增)
3. 结合用户选择的目标
4. 自动决策最佳 Writer
5. **边界情况需用户确认** (v2.1.1 新增)

```python
def route_auto(content_features, goal):
    # 帮人选择 → 对比或榜单
    if goal == "帮人选择工具":
        if content_features["has_comparison"]:
            tool_count = content_features.get("comparison_tool_count", 0)

            # v2.1.1 新增: 根据工具数量决定模式
            if tool_count <= 3:
                # A vs B 或 A vs B vs C → Tool Showdown (洗稿模式)
                return "tool_showdown", {
                    "rewrite_mode": True,
                    "constraints": "strict",  # 禁止新增工具/场景
                    "source_tools": content_features.get("compared_tools", [])
                }
            elif tool_count == 4:
                # 边界情况 → 需要用户确认
                return "confirm_required", {
                    "options": ["tool_showdown", "listicle"],
                    "reason": "4 个工具处于边界区间"
                }
            else:
                # Top 5+ → Listicle (可扩展)
                return "listicle", {
                    "rewrite_mode": False,
                    "constraints": "flexible"  # 可以扩展更多工具
                }

        return "listicle", {"rewrite_mode": False}

    # 教人做事 → 教程
    if goal == "教人做事":
        return "tutorial", {}

    # 展示发现 → 案例
    if goal == "展示发现":
        return "case_study", {}

    return "tutorial", {}  # 默认
```

---

## 目标 → 写作方向映射

| 用户目标 | 推荐方向 | 备选方向 |
|----------|----------|----------|
| 帮人选择工具 | Tool Showdown | Listicle |
| 教人做事 | Tutorial | - |
| 展示发现 | Case Study | - |

---

## 配置 JSON 索引

用于程序化访问:

```json
{
  "routes": {
    "tool_showdown": {
      "writer": "blog-list-writer",
      "mode": "tool_showdown",
      "word_count": [2500, 3500],
      "aeo_target": 75,
      "signals": ["vs", "对比", "对决", "comparison"]
    },
    "listicle": {
      "writer": "blog-list-writer",
      "mode": "standard",
      "word_count": [2500, 3500],
      "aeo_target": 75,
      "signals": ["best", "top", "榜单", "评测"]
    },
    "tutorial": {
      "writer": "blog-tutorial-writer",
      "mode": null,
      "word_count": [1800, 2500],
      "aeo_target": 75,
      "signals": ["how to", "如何", "教程", "guide"]
    },
    "case_study": {
      "writer": "case-roundup-writer",
      "mode": null,
      "word_count": [300, 600],
      "aeo_target": 70,
      "signals": ["案例", "case", "roundup", "汇总"]
    }
  }
}
```

---

## Changelog

### v2.1.1 (2026-01-26)

**Tool Showdown 洗稿约束: 根据工具数量决策模式**

1. **新增路由决策矩阵**:
   - 工具数量 ≤3 → Tool Showdown + 洗稿约束
   - 工具数量 = 4 → 边界情况，需用户确认
   - 工具数量 >4 → Listicle 可扩展模式

2. **新增洗稿约束表**:
   - 工具列表锁定 (BLOCKING)
   - 测试场景锁定 (WARNING)
   - 字数范围约束 (WARNING)

3. **Tool Showdown 配置更新**:
   - 新增 `tool_count_threshold` 配置
   - 新增 `rewrite_constraints` 配置块

4. **route_auto() 函数更新**:
   - 增加工具数量判断逻辑
   - 返回洗稿约束配置

---

### v2.0 (2026-01-23)

**简化: 9 种组合 → 4 种核心方向**

- 移除冗余组合 (quick_showdown, deep_listicle, competitor_alternatives 等)
- 对齐 Writer 路由表
- 简化配置结构
- 添加路由决策逻辑

### v1.0 (2026-01-22)

- 初始版本: 9 种预设组合

---

*SmartLauncher v2.1.1 COMBOS - 4 种核心方向 × 工具数量检测 × 洗稿约束*
