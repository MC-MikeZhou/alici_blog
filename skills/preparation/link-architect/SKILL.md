---
name: link-architect
version: "1.0"
type: skill
provides: internal-link-architecture
dependencies:
  - tool: WebFetch
  - tool: Read
description: >
  Link Architect v1.0 - 内链架构规划。
  输入新文章主题 → 扫描 alici.ai/blog 全站 → 输出内链地图 + 防蚕食策略。
  确保每篇新文章与已有内容生态正确互联。
allowed-tools: WebFetch, WebSearch, Read, Write
metadata:
  author: H
  created: 2026-03-22
  route: "E (Formula-Driven)"
---

# Link Architect v1.0

## Purpose

在写作前规划新文章与 alici.ai 已有内容的互联关系，包括：
- **出链** (新文章 → 已有文章): 增强读者深度阅读
- **入链** (已有文章 → 新文章): 为新文章导流
- **蚕食检测**: 避免新旧文章关键词竞争
- **Template 链接**: 嵌入 Alici Formulas templates 到文章段落

**核心理念**: 内链先于写作 — 在动笔前就规划好文章在内容生态中的位置。

---

## Trigger Words

```yaml
triggers:
  - "link architect"
  - "内链规划"
  - "link map"
  - "内链地图"
  - "防蚕食"
  - "cannibalization check"
```

---

## Input

| 参数 | 必需 | 说明 |
|------|------|------|
| `new_article_slug` | ✅ | 新文章 slug (e.g., "ai-cat-dancing-tutorial") |
| `primary_keyword` | ✅ | 主关键词 (e.g., "AI cat dance") |
| `secondary_keywords` | 推荐 | 次要关键词列表 |
| `formula_pack` | 可选 | formula-integrator 的输出 (用于 template 链接) |

---

## Execution Steps

### Step 1: 扫描已有文章

```
WebFetch alici.ai/blog
  → 列出所有已发布文章:
    - slug
    - 标题
    - 主关键词 (从标题推断)
    - 发布日期
```

补充: 读取本地 `/reports 待发文章/` 中已完成的文章 (即将发布)。

### Step 2: 关键词重叠分析

```
对每篇已有文章:
  - 计算与新文章关键词的重叠度
  - 标记蚕食风险等级: high / medium / low / none
  - 制定内容边界策略
```

### Step 3: 出链规划 (新 → 已有)

```
识别新文章中可以链接到已有文章的位置:
  - 目标文章 slug
  - 锚文本建议
  - 插入位置 (哪个章节)
  - 链接类型: contextual / see-also / comparison
```

### Step 4: 入链规划 (已有 → 新)

```
识别已有文章中可以链接到新文章的位置:
  - 来源文章 slug
  - 插入位置建议
  - 锚文本建议
  - 优先级: high / medium / low
```

### Step 5: Template 链接匹配

```
如有 formula_pack 输入:
  - 将 templates 匹配到文章各段落
  - 生成 template 链接列表
```

### Step 6: 输出 Link Architecture

将结果写入 `link-architecture.json`。

---

## Output Structure

**文件**: `link-architecture.json`

```json
{
  "metadata": {
    "new_article": {
      "slug": "ai-cat-dancing-tutorial",
      "primary_keyword": "AI cat dance",
      "secondary_keywords": ["cat dance video AI", "AI pet dance"]
    },
    "scan_date": "2026-03-22",
    "existing_articles_scanned": 15
  },
  "outbound_links": [
    {
      "target_slug": "best-ai-dance-video-generators",
      "target_title": "5 Best AI Dance Video Generators",
      "context": "When mentioning tool comparison",
      "anchor_text": "best AI dance video generators",
      "section": "FAQ or Tool Recommendation",
      "link_type": "contextual",
      "priority": "high"
    }
  ],
  "inbound_links": [
    {
      "source_slug": "best-ai-dance-video-generators",
      "source_title": "5 Best AI Dance Video Generators",
      "insert_location": "FAQ section",
      "anchor_text": "AI cat dance tutorial",
      "priority": "high",
      "action_required": "manual_edit"
    }
  ],
  "cannibalization_check": [
    {
      "existing_article": "ai-dance-video-tutorial",
      "overlap_keyword": "AI dance tutorial",
      "overlap_level": "medium",
      "strategy": "link_dont_repeat",
      "boundary": "This article focuses on CAT dance specifically; existing covers general dance",
      "risk": "medium"
    }
  ],
  "template_links": [
    {
      "template_name": "Cute Cat Hip-Hop",
      "template_url": "/formulas/templates/cute-cat-hip-hop",
      "section": "Method 1: Using Ready-Made Templates",
      "link_type": "product_integration"
    }
  ],
  "summary": {
    "outbound_links_planned": 4,
    "inbound_links_planned": 2,
    "cannibalization_risks": 1,
    "template_integrations": 3,
    "action_items": [
      "After publishing: add inbound link from 'best-ai-dance-video-generators' FAQ"
    ]
  }
}
```

---

## Cannibalization Strategies

| 风险级别 | 策略 | 说明 |
|---------|------|------|
| **high** | `differentiate_angle` | 必须明确不同角度，可能需要调整标题/关键词 |
| **medium** | `link_dont_repeat` | 链接到已有文章，不重复相同内容 |
| **low** | `complementary` | 互补关系，互相链接即可 |
| **none** | `independent` | 无重叠，独立内容 |

---

## Usage in Route E Pipeline

```
Route E Phase 0: Formula 生态扫描
  ├── [formula-integrator]
  ├── [link-architect] ← THIS SKILL
  └── DataForSEO 验证
```

Link Architecture 的数据流向：
- `outbound_links` → Writer: 在指定章节插入内链
- `inbound_links` → 发布后 TODO: 更新已有文章
- `cannibalization_check` → Writer: 遵循内容边界策略
- `template_links` → Writer: 嵌入 Alici template 链接

---

## Changelog

### v1.0 (2026-03-22)
- 初始版本: 全站扫描 + 出入链规划 + 蚕食检测 + template 匹配
