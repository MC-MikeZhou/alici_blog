---
name: formula-integrator
version: "1.0"
type: skill
provides: formula-ecosystem-scanning
dependencies:
  - tool: WebFetch
  - tool: WebSearch
description: >
  Formula Integrator v1.0 - Alici Formulas 生态扫描。
  输入文章主题 → 扫描 alici.ai 工具页 + Formulas 生态 → 输出结构化 Formula Integration Pack。
  用于 Route E: Formula-Driven Pipeline 的 Phase 0。
allowed-tools: WebFetch, WebSearch, Read, Write
metadata:
  author: H
  created: 2026-03-22
  route: "E (Formula-Driven)"
---

# Formula Integrator v1.0

## Purpose

从 Alici Formulas 生态中自动提取与文章主题相关的 templates、creators、prompts、sub-niches，
为 Formula-Driven 写作流程提供结构化数据支撑。

**核心理念**: Formula 驱动选题和写作 — 不是从关键词出发，而是从已有的 Formulas 生态出发，
找到内容与产品的天然连接点。

---

## Trigger Words

```yaml
triggers:
  - "formula integrator"
  - "formula scan"
  - "扫描 formulas"
  - "formula 生态"
  - "templates 提取"
```

---

## Input

| 参数 | 必需 | 说明 |
|------|------|------|
| `topic` | ✅ | 文章主题 (e.g., "AI dance", "AI cat video") |
| `tool_page_url` | 推荐 | Alici 工具页 URL (e.g., `/ai-dance-generator`) |
| `formulas_guide_url` | 可选 | Formulas guide 页面 URL |
| `formulas_charts_url` | 可选 | Formulas charts 页面 URL |

---

## Execution Steps

### Step 1: 工具页扫描

```
WebFetch alici.ai 工具页 (如 /ai-dance-generator)
  → 提取全部 templates:
    - template 名称
    - template URL
    - 预览截图描述
    - 适用场景标签
```

### Step 2: Formulas Guide 扫描

```
WebFetch Formulas guide 页面
  → 提取创作者信息:
    - 创作者名称 + handle
    - 参与数据 (likes, views)
    - 创作技巧/方法论
    - Formula URL
```

### Step 3: Formulas Charts 扫描

```
WebFetch Formulas charts 页面
  → 提取排名数据:
    - 创作者排名
    - 增长趋势
    - 热门 Formula 类别
```

### Step 4: 相关性评分

```
对每个提取的 template/creator/prompt 按主题相关性评分:
  - high: 直接相关，必须引用
  - medium: 间接相关，可作为扩展
  - low: 弱相关，仅供参考
```

### Step 5: 输出 Formula Integration Pack

将结果写入 `formula-integration-pack.json`。

---

## Output Structure

**文件**: `formula-integration-pack.json`

```json
{
  "metadata": {
    "topic": "AI dance",
    "tool_page": "/ai-dance-generator",
    "generated_at": "2026-03-22T10:00:00Z",
    "version": "1.0"
  },
  "templates": [
    {
      "name": "Cute Animal Hip-Hop",
      "url": "/formulas/templates/cute-animal-hip-hop",
      "relevance": "high",
      "suggested_section": "Method 1: Template-Based Dance",
      "engagement_proof": "16,732 likes"
    }
  ],
  "creators": [
    {
      "name": "Hugh",
      "handle": "@hugh.yellownine",
      "likes": 140700,
      "technique": "累积角色IP",
      "formula_url": "/formulas/creators/hugh",
      "relevance": "high"
    }
  ],
  "prompts": [
    {
      "name": "Cute Animal Hip-Hop",
      "source_creator": "Hugh",
      "prompt_text": "A cute [animal] dancing hip-hop in [location]...",
      "engagement_proof": "16,732 likes",
      "relevance": "high"
    }
  ],
  "video_embeds": [
    {
      "position": "After Step 2",
      "description": "Hugh's cat dance formula result",
      "creator": "Hugh",
      "likes": 14980,
      "embed_type": "formula_result"
    }
  ],
  "sub_niches": [
    {
      "name": "Cat Dance",
      "templates_count": 9,
      "search_volume": "estimated from DataForSEO",
      "competition": "low",
      "opportunity_score": "high"
    }
  ],
  "integration_summary": {
    "total_templates": 12,
    "high_relevance": 5,
    "recommended_embeds": 3,
    "top_creator": "Hugh (@hugh.yellownine)"
  }
}
```

---

## Error Handling

| 场景 | 处理 |
|------|------|
| 工具页无法访问 | 跳过 Step 1，仅执行 Steps 2-5，标记 `tool_page_status: "unavailable"` |
| Formulas guide 无法访问 | 使用 WebSearch 搜索 `site:alici.ai formulas {topic}` 作为替代 |
| 无相关 templates | 输出空 templates 数组，标记 `no_templates_found: true` |
| 创作者数据不完整 | 填充可获取的字段，缺失字段标记 `null` |

---

## Usage in Route E Pipeline

```
Route E Phase 0: Formula 生态扫描
  ├── [formula-integrator] ← THIS SKILL
  ├── [link-architect]
  └── DataForSEO 验证
```

Formula Integration Pack 的数据流向：
- `templates` → Writer: 引用到文章各段落的 template 链接
- `creators` → Writer: 作为 social proof 和案例引用
- `prompts` → Writer: 嵌入 "Prompts to Try" 或 "Ready-Made Templates" 章节
- `video_embeds` → Editor: 视频嵌入位置建议
- `sub_niches` → growth-topic-scout: 补充选题方向

---

## Changelog

### v1.0 (2026-03-22)
- 初始版本: 3 源扫描 (工具页 + guide + charts) + 相关性评分 + JSON 输出
