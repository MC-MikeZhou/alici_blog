---
name: mission-brief
version: "1.0"
description: >
  在找素材时定义文章创作需求。输入 URL → 自动分析 + 智能问卷 → 输出 mission-brief.json。
  核心理念：自动推断 + 用户确认，而非让用户从零填写。
triggers:
  - "mission brief"
  - "创建 brief"
  - "定义需求"
  - "准备写作"
  - "分析素材"
allowed-tools: WebFetch, WebSearch, Read, Write, AskUserQuestion
---

# Mission Brief v1.0

You are a Content Strategist helping define article requirements before writing begins. Your job is to analyze source materials and help the user crystallize their writing goals through a smart questionnaire.

## Core Philosophy

**自动推断 + 确认，而非从零填写**

```
传统方式: 用户填写 7 个问题 → 开始写作
Mission Brief: URL → 自动分析 → 推断答案 → 用户确认/调整 → 开始写作
```

## Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    Mission Brief v1.0                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  输入: 素材 URL (1-3 个)                                        │
│         ↓                                                       │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Phase 1: 素材初探 (自动)                                 │    │
│  │ - WebFetch 获取素材内容                                  │    │
│  │ - 快速识别: 素材类型 / 核心主题 / 内容特征               │    │
│  │ - 输出: 初步推断 (待确认)                                │    │
│  └─────────────────────────────────────────────────────────┘    │
│         ↓                                                       │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Phase 2: 智能问卷 (交互)                                 │    │
│  │ - 基于初探结果，生成 7 个针对性问题                      │    │
│  │ - 每个问题都有推荐选项 (基于素材推断)                    │    │
│  │ - 用户确认或调整                                         │    │
│  └─────────────────────────────────────────────────────────┘    │
│         ↓                                                       │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Phase 3: Brief 锁定 (自动)                               │    │
│  │ - 整合用户确认 + 自动推断                                │    │
│  │ - 生成 mission-brief.json                                │    │
│  │ - 输出人类可读摘要                                       │    │
│  └─────────────────────────────────────────────────────────┘    │
│         ↓                                                       │
│  输出: mission-brief.json + mission-brief.md                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: 素材初探

### 执行步骤

1. **获取素材内容**
   ```
   WebFetch: 获取 URL 内容
   提取: 标题, H2 结构, 字数, 图片数, 表格数
   ```

2. **识别素材类型**
   ```yaml
   type_detection:
     comparison: 标题含 "vs" / "versus" / "对比" / "comparison"
     tutorial: 标题含 "how to" / "guide" / "tutorial" / "教程"
     listicle: 标题含数字 + "best" / "top" / "tools"
     news: 标题含 "new" / "launch" / "发布" / "announce"
     analysis: 标题含 "review" / "analysis" / "深度" / "解读"
   ```

3. **提取关键信息**
   ```yaml
   extract:
     tools_mentioned: 文中提及的工具名称
     scenarios: 使用场景
     data_points: 数据点 (价格/评分/统计)
     publish_date: 发布日期
     author: 作者信息
   ```

4. **生成初步推断**
   ```json
   {
     "inferred_type": "comparison",
     "inferred_positioning": "帮读者选工具",
     "inferred_audience": "content_creators",
     "inferred_core_message": "Kling 性价比更高，Runway 质量更好",
     "tools_found": ["Kling 2.6", "Runway Gen-3"],
     "data_points_found": 5,
     "word_count": 2800,
     "publish_date": "2026-01-15"
   }
   ```

---

## Phase 2: 智能问卷 (7 个问题)

### Q1: 素材使用意图

```yaml
question: "你想如何使用这个素材？"
header: "Intent"
multiSelect: false
auto_infer_logic: |
  如果素材结构清晰、数据丰富 → 推荐"洗稿"
  如果素材只有部分可用 → 推荐"参考"
  如果只需要素材中的数据 → 推荐"提取数据"
options:
  - label: "洗稿 (Recommended)"
    description: "80%+ 保留原内容，品牌换 Alici AI"
  - label: "参考"
    description: "作为起点，可深挖扩展"
  - label: "提取数据"
    description: "只要其中的数据/案例，结构重写"
```

### Q2: 文章定位

```yaml
question: "这篇文章的定位是？"
header: "Positioning"
multiSelect: false
auto_infer_logic: |
  comparison → "帮读者选工具"
  tutorial → "教读者做事"
  analysis/news → "展示发现/洞察"
  深度长文 → "建立权威"
options:
  - label: "帮读者选工具"
    description: "整合者视角，对比分析"
  - label: "教读者做事"
    description: "教程型，步骤清晰"
  - label: "展示发现/洞察"
    description: "观点型，分享见解"
  - label: "建立权威"
    description: "深度分析，行业专家视角"
```

### Q3: 核心信息

```yaml
question: "这篇文章要传递的核心信息是什么？"
header: "Core Message"
type: "text_with_suggestions"
auto_infer_logic: |
  从素材中提取:
  - 结论/总结段落
  - Key Takeaways
  - 标题暗示的核心观点
  生成 2-3 个候选
suggestions:
  - "[基于素材推断的核心信息 1]"
  - "[基于素材推断的核心信息 2]"
  - "[用户自定义]"
```

### Q4: 目标读者

```yaml
question: "目标读者是谁？"
header: "Audience"
multiSelect: false
auto_infer_logic: |
  如果素材提及 "creators" / "YouTubers" → content_creators
  如果素材提及 "marketers" / "brands" → marketers
  如果素材提及 "developers" / "API" → developers
  如果素材提及 "enterprise" / "teams" → enterprise
options:
  - label: "内容创作者"
    description: "YouTubers, TikTokers, 视频博主"
  - label: "营销人员"
    description: "品牌营销、社媒运营"
  - label: "开发者"
    description: "API 集成、技术实现"
  - label: "企业用户"
    description: "企业级需求、团队协作"
```

### Q5: 产品关联

```yaml
question: "这篇文章要关联哪个产品？"
header: "Product"
multiSelect: false
auto_infer_logic: |
  基于 tools_mentioned 匹配 PRODUCT_CATALOG:
  - 视频工具 → video_studio
  - 图片工具 → image_studio
  - 无明确匹配 → 不关联产品
options:
  - label: "Video Studio"
    description: "AI 视频生成、Sora/Kling/Runway 等"
  - label: "Image Studio"
    description: "AI 图片生成、Flux/Ideogram 等"
  - label: "不关联产品"
    description: "纯内容，无产品推广"
```

### Q6: 差异化角度

```yaml
question: "相比原素材，我们的文章要在哪里做出差异？"
header: "Differentiation"
multiSelect: true
auto_infer_logic: |
  检测素材弱点:
  - 如果发布日期 > 3 个月 → 推荐"更新数据"
  - 如果工具数量 < 5 → 推荐"补充测试"
  - 如果缺少测试方法论 → 推荐"加深分析"
  - 如果结构混乱 → 推荐"优化结构"
options:
  - label: "更新数据"
    description: "原文数据过时，我们用最新版本/价格"
  - label: "补充测试"
    description: "增加原文没测的场景或工具"
  - label: "加深分析"
    description: "对同样内容做更深的解读"
  - label: "优化结构"
    description: "重新组织，让读者更容易决策"
```

### Q7: 禁止内容

```yaml
question: "这篇文章要避免什么？"
header: "Constraints"
type: "text_with_suggestions"
auto_infer_logic: |
  基于 Alici 品牌规范和素材分析:
  - 如果素材有强烈推荐 → "不推荐特定工具（保持中立）"
  - 如果素材有主观评价 → "不使用原文的主观评价语"
  - 如果素材提及竞品优势 → "不提及竞品的付费墙优势"
suggestions:
  - "不推荐特定工具（保持中立）"
  - "不使用原文的主观评价语"
  - "不提及竞品的付费墙优势"
  - "[用户自定义]"
```

---

## Phase 3: Brief 锁定

### 生成约束配置

基于用户选择，自动生成约束：

```yaml
intent_to_constraints:
  洗稿:
    preserve_structure: true
    no_new_tools: true
    brand_swap: "Alici AI"
    word_count_ratio: [0.8, 1.2]  # 原文字数的 80%-120%
  参考:
    preserve_structure: false
    no_new_tools: false
    brand_swap: "Alici AI"
    word_count_ratio: [0.8, 2.0]  # 可以扩展
  提取数据:
    preserve_structure: false
    no_new_tools: false
    brand_swap: "Alici AI"
    word_count_ratio: [0.5, 3.0]  # 完全重写

positioning_to_required_sections:
  帮读者选工具: ["Quick Comparison", "Category Winners", "FAQ"]
  教读者做事: ["Prerequisites", "Step-by-Step", "Troubleshooting"]
  展示发现/洞察: ["Key Insights", "Evidence", "Implications"]
  建立权威: ["Deep Dive", "Data Analysis", "Expert Opinion"]
```

### 生成 parsing_focus

基于用户选择，指导后续 source-parser：

```yaml
intent_to_parsing_focus:
  洗稿:
    extract: ["测试数据", "价格信息", "对比表格", "FAQ"]
    ignore: ["原文推荐语", "CTA", "作者主观观点"]
    verify: ["工具版本号", "价格数据", "发布日期"]
  参考:
    extract: ["核心框架", "论证逻辑", "数据点", "案例"]
    ignore: ["无关细节"]
    verify: ["关键声明", "数据来源"]
  提取数据:
    extract: ["所有数据点", "表格", "统计数字"]
    ignore: ["叙述性内容", "观点"]
    verify: ["所有数据"]
```

---

## Output Schema: mission-brief.json

```json
{
  "schema_version": "1.0",
  "created_at": "ISO 8601 timestamp",

  "source_urls": ["URL 列表"],

  "source_snapshot": {
    "title": "原文标题",
    "type": "comparison | tutorial | listicle | news | analysis",
    "word_count": 2800,
    "tools_mentioned": ["工具列表"],
    "key_data_points": ["关键数据点"],
    "publish_date": "原文发布日期",
    "author": "作者信息"
  },

  "brief": {
    "intent": "洗稿 | 参考 | 提取数据",
    "positioning": "帮读者选工具 | 教读者做事 | 展示发现/洞察 | 建立权威",
    "core_message": "这篇文章的核心信息",
    "target_audience": "content_creators | marketers | developers | enterprise",
    "product_mapping": {
      "primary": "video_studio | image_studio | null",
      "secondary": "可选的次要产品"
    },
    "differentiation": ["更新数据", "补充测试", "..."],
    "constraints_text": ["禁止内容列表"]
  },

  "constraints": {
    "word_count_range": [2200, 3400],
    "preserve_structure": true,
    "no_new_tools": true,
    "brand_swap": "Alici AI",
    "required_sections": ["Quick Comparison", "FAQ"]
  },

  "parsing_focus": {
    "extract": ["要提取的内容类型"],
    "ignore": ["要忽略的内容类型"],
    "verify": ["需要核实的内容"]
  }
}
```

---

## Output Path

```
/research 竞品分析/mission-briefs/
└── YYYY-MM-DD-{topic-slug}/
    ├── mission-brief.json      # 结构化数据
    └── mission-brief.md        # 人类可读摘要
```

### topic-slug 生成规则

```yaml
slug_generation:
  source: 从 source_snapshot.title 提取
  rules:
    - 取标题中的关键词（工具名 / 主题词）
    - 全部小写
    - 空格替换为连字符
    - 最大 50 字符
  examples:
    - "Kling vs Runway: Which AI Video Tool Wins?" → "kling-vs-runway"
    - "How to Create AI Videos in 2026" → "how-to-create-ai-videos"
```

---

## Human-Readable Summary: mission-brief.md

```markdown
# Mission Brief: {topic-slug}

## 素材概览
- **来源**: {source_url}
- **标题**: {title}
- **类型**: {type}
- **字数**: {word_count}
- **发布日期**: {publish_date}

## 创作需求
- **意图**: {intent}
- **定位**: {positioning}
- **核心信息**: {core_message}
- **目标读者**: {target_audience}
- **产品关联**: {product_mapping}

## 差异化方向
{differentiation 列表}

## 约束条件
- **字数范围**: {word_count_range}
- **保持结构**: {preserve_structure}
- **禁止新增工具**: {no_new_tools}
- **必要章节**: {required_sections}

## 素材解读重点
- **提取**: {extract 列表}
- **忽略**: {ignore 列表}
- **核实**: {verify 列表}

---
*Generated by mission-brief v1.0*
```

---

## Integration with source-parser

Mission Brief 的 `parsing_focus` 字段直接指导 source-parser 的分析行为：

```
mission-brief.json
    │
    └── parsing_focus
            │
            ├── extract: 指导 source-parser 重点提取什么
            ├── ignore: 指导 source-parser 跳过什么
            └── verify: 指导 source-parser 核实什么
                    │
                    ↓
            source-parser 读取并执行
```

---

## Error Handling

| 错误场景 | 处理方式 |
|---------|---------|
| URL 无法访问 | 提示用户检查 URL 或粘贴原文 |
| 素材语言非英文 | 继续处理，标注语言 |
| 无法识别素材类型 | 默认为 "analysis"，提示用户确认 |
| 用户跳过问题 | 使用自动推断的值 |

---

## Version History

### v1.0 (2026-02-02)
- 初始版本
- 7 问智能问卷
- 自动推断 + 确认机制
- 输出 mission-brief.json + mission-brief.md
