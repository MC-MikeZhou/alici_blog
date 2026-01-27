# 11 - 数据契约系统

> Writer ↔ Editor 之间的标准化数据传递规范

---

## 概述

数据契约系统定义了 Skills 之间标准化的数据传递格式，确保各组件能够正确地协作。本文档重点描述 Writer → Editor 的数据流。

---

## Writer → Editor 契约 (v1.3/v2.6)

### 输出目录结构

**Writer v1.3 输出**:
```
/reports/YYYY-MM-DD-{topic}/
├── 01-article-draft.md          # 正文（含图片占位符）
├── asset_plan.json              # 给 Editor 的生成清单
└── prompt_pack.md               # 给读者的 copy-paste 包
```

**Editor v2.6 输出**:
```
/reports/YYYY-MM-DD-{topic}/
├── /assets/{slug}/              # 图片文件
│   ├── hero-image.png
│   ├── inline-1.png
│   └── comparison-grid.png
├── asset_manifest.json          # 资产清单
├── prompts_used.md              # 使用的 prompts
└── 01-article-edited.md         # 回填后的文章
```

---

## asset_plan.json 规范

由 Writer 生成，供 Editor 读取执行图片生成。

### 结构定义

```json
{
  "images": [
    {
      "id": "hero-image",
      "prompt": "detailed prompt for image generation",
      "role": "hero",
      "placeholder": "![Image description](placeholder)",
      "context": "where this image appears in article"
    }
  ],
  "metadata": {
    "total_images": 5,
    "article_slug": "topic-slug",
    "generated_at": "2026-01-20T10:00:00Z"
  }
}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `images` | Array | 是 | 图片生成任务列表 |
| `images[].id` | String | 是 | 图片唯一标识，用于回填 |
| `images[].prompt` | String | 是 | 图片生成 Prompt |
| `images[].role` | Enum | 是 | `hero` / `inline` / `comparison` |
| `images[].placeholder` | String | 是 | 文章中的占位符文本 |
| `images[].context` | String | 否 | 图片在文章中的上下文说明 |
| `metadata.total_images` | Number | 是 | 总图片数量 |
| `metadata.article_slug` | String | 是 | 文章 slug |
| `metadata.generated_at` | String | 是 | ISO 8601 时间戳 |

### Role 类型说明

| Role | 用途 | 典型尺寸 |
|------|------|----------|
| `hero` | 文章封面图 | 16:9 |
| `inline` | 文章内插图 | 4:3 |
| `comparison` | 对比图/表格配图 | 1:1 |

---

## asset_manifest.json 规范

由 Editor 生成，记录图片生成结果。

### 结构定义

```json
{
  "images": [
    {
      "id": "hero-image",
      "original_prompt": "from asset_plan.json",
      "final_prompt": "potentially adjusted prompt",
      "file_path": "/assets/slug/hero-image.png",
      "cdn_url": "https://ct2.alici.ai/static/image/...",
      "generation_model": "fal-ai/banana-pro",
      "status": "success"
    }
  ],
  "summary": {
    "total_planned": 5,
    "total_generated": 5,
    "success_rate": "100%"
  }
}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `images` | Array | 是 | 图片生成结果列表 |
| `images[].id` | String | 是 | 对应 asset_plan 中的 id |
| `images[].original_prompt` | String | 是 | 原始 Prompt |
| `images[].final_prompt` | String | 是 | 实际使用的 Prompt（可能调整） |
| `images[].file_path` | String | 是 | 本地文件路径 |
| `images[].cdn_url` | String | 是 | CDN URL |
| `images[].generation_model` | String | 是 | 使用的模型 |
| `images[].status` | Enum | 是 | `success` / `failed` / `skipped` |
| `summary.total_planned` | Number | 是 | 计划生成数量 |
| `summary.total_generated` | Number | 是 | 实际生成数量 |
| `summary.success_rate` | String | 是 | 成功率 |

---

## prompt_pack.md 规范

由 Writer 生成，供读者直接复制使用。

### 结构

```markdown
## Visual Prompt Pack

### Hero Image Prompt
A futuristic AI dashboard with holographic displays...
[Style: modern, professional | Ratio: 16:9]

### Workflow Diagram Prompt
Step-by-step flowchart showing the AI workflow...
[Style: clean, minimalist | Ratio: 4:3]
```

### 用途

- 读者可复制 Prompt 到 Midjourney, DALL-E 等工具
- 记录文章配图的生成方法
- 便于后续修改或重新生成

---

## 错误处理

### Editor 错误处理流程

1. **图片生成失败**
   - 保留占位符在文章中
   - 在 manifest 中标记状态为 `failed`
   - 在 `prompts_used.md` 中记录失败原因

2. **部分成功**
   - 继续处理其他图片
   - 生成汇总报告显示成功率
   - 文章输出包含已成功的图片

3. **全部失败**
   - 输出无图片版本的文章
   - 在报告中标注需要手动处理

---

## 验证规则

### Writer 输出验证

- [ ] `asset_plan.json` 存在且格式正确
- [ ] 每个图片有唯一的 `id`
- [ ] `placeholder` 在 `01-article-draft.md` 中存在
- [ ] `total_images` 与 `images` 数组长度一致

### Editor 输出验证

- [ ] 每个 `asset_plan` 中的图片都有对应的 manifest 记录
- [ ] 所有 `success` 状态的图片 CDN URL 可访问
- [ ] 文章中的占位符已被实际 URL 替换
- [ ] `success_rate` 计算正确

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-01-20 | 初始版本，定义基本数据契约 |

---

**相关文档**:
- [06-SKILL-ARCHITECTURE.md](./06-SKILL-ARCHITECTURE.md) - Skills 架构
- [CLAUDE.md](../CLAUDE.md) - 主配置文件
