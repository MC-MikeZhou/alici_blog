---
name: markdown-to-framer
version: "1.3"
description: >
  Convert Markdown articles to Framer CMS JSON format with automatic validation and fixing.
  Zero human intervention—converts, validates, and auto-fixes formatting issues.
  v1.3: 修复图片格式 (无 figure, alt 在 src 前) + 特殊字符处理 + cover 字段简化
  Triggers on: convert to framer, export json, publish ready, 生成 JSON.
allowed-tools: Read, Write
dependencies:
  - path: "06-cover-metadata.json"
    purpose: "Cover image URL from blog-cover-generator (optional)"
---

# Markdown to Framer Skill v1.3

> **Zero Human Intervention** - 自动转换、自动校验、自动修复

## 触发条件

- 用户调用 `/convert-to-framer`
- `/full-workflow` Phase 6 自动调用
- 关键词："convert to framer", "export json", "publish ready", "生成 JSON"

## 输入要求

- Markdown 文件路径（通常是 `01-article-edited.md`）
- 文件必须包含 YAML frontmatter
- AEO 评分必须 ≥ 75（前置条件）

### 必需的 Frontmatter 字段

```yaml
---
title: "文章标题"           # 必需
slug: "url-safe-slug"        # 必需
category: "list|tutorial|news"  # 必需
featured_image:
  url: "https://..."         # 必需（封面图）
  alt: "描述"
meta_title: "SEO 标题"       # 可选，默认使用 title
meta_description: "SEO 描述" # 可选，默认从正文生成
tags: ["tag1", "tag2"]       # 可选
date: "YYYY-MM-DD"           # 可选，默认当天
read_time: "X min"           # 可选，默认从字数计算
---
```

## 执行流程

### Phase 1: 解析输入

```
1. 读取 Markdown 文件
2. 分离 YAML frontmatter 和 Markdown body
3. 检查 cover metadata (v1.2 NEW):
   - 尝试读取同目录下的 06-cover-metadata.json
   - 如果存在，使用 cdn_url 作为 featured_image.url
4. 验证必需字段存在：
   - title → 缺失则 ERROR
   - slug → 缺失则 ERROR
   - category → 缺失则 ERROR
   - featured_image.url → 缺失则检查 cover metadata，仍缺失则 ERROR
```

### Phase 1.5: Cover Metadata Integration (v1.2+)

```python
# Pseudocode
def load_cover_metadata(article_dir):
    """
    从 blog-cover-generator 输出加载封面 URL
    注意: cover 字段只需要 url，不需要 alt（Framer CMS 不支持）
    """
    cover_metadata_path = os.path.join(article_dir, "06-cover-metadata.json")

    if os.path.exists(cover_metadata_path):
        with open(cover_metadata_path) as f:
            cover_data = json.load(f)
        return {
            "url": cover_data.get("cdn_url")
            # 注意: 不要添加 alt 字段！
        }
    return None
```

**优先级**:
1. `06-cover-metadata.json` 中的 `cdn_url` (如果存在)
2. YAML frontmatter 中的 `featured_image.url`
3. ERROR (两者都缺失)

### Phase 2: 字段映射与转换

按照 `FIELD_SCHEMA.md` 中的规则将 frontmatter 映射到 Framer JSON 字段。

**核心转换**：
- Markdown body → Framer HTML（按 `CONVERSION_RULES.md` 执行）
- 移除 H1 标题（title 已是单独字段）
- 所有链接添加 `target="_blank"`
- 所有 `<li>` 添加 `data-preset-tag="p"` 属性
- **图片标签**：`<img alt="..." src="...">`（不用 figure 包裹，alt 在 src 前）
- **特殊字符**：替换 em dash `—` 为 ` - `（空格+连字符+空格）

### Phase 3: 校验 + 自动修复

| 字段 | 校验规则 | 自动修复 |
|------|----------|----------|
| `Slug` | `^[a-z0-9\-]+$`，20-100字符 | 转小写，空格→连字符 |
| `meta_title` | ≤ 60 字符 | 智能截断到 57 + "..." |
| `meta_description` | ≤ 160 字符 | 智能截断到 157 + "..." |
| `Date` | ISO 8601 格式 | `YYYY-MM-DD` → `YYYY-MM-DDTHH:mm:ss.000Z` |
| `main_category` | enum: tutorial/list/news | 映射 category 字段 |
| `read_time` | `^\d+ min$` | 从字数计算：`ceil(wordCount/200) + " min"` |

**智能截断逻辑**：
```
输入: "10 Best AI Video Generators in 2025: Complete Comparison Guide for Creators"
处理: 找到第 57 字符前的最后一个完整单词
输出: "10 Best AI Video Generators in 2025: Complete..."
```

### Phase 4: 生成 JSON 并输出

> **⚠️ 重要格式要求**：
> 1. JSON 必须是**数组格式** `[{...}]`，不能是单独对象 `{...}`
> 2. `cover` 字段只有 `url`，**不要添加 `alt`**
> 3. `article_body_content` 中的图片用 `<img alt="..." src="...">`，不用 `<figure>` 包裹

**输出结构**：
```json
[
  {
    "Slug": "...",
    "title": "...",
    "sub_title": "...",
    "TLNR": "...",
    "cover": { "url": "..." },
    "Date": "...",
    "read_time": "...",
    "main_category": "...",
    "recommend_category": "",
    "article_body_content": "...",
    "CTA_alici_link": "...",
    "CTA button": "...",
    "meta_title": "...",
    "meta_description": "...",
    "tag_for_SEO": "..."
  }
]
```

**输出路径**：
`/reports/[date]-[topic]/06-article-final.json`

### Phase 5: 更新进度追踪

更新 `00-implementation.md`：
```markdown
## Phase 6: Export ✅
- [x] Markdown → Framer JSON 转换完成
- [x] 校验通过，自动修复 N 项
- [x] 输出位置：`/reports/.../06-article-final.json`
- 状态：**PUBLISH READY**
```

## 字段映射详表

| Framer JSON | 来源 | 默认值/生成规则 |
|-------------|------|-----------------|
| `Slug` | `frontmatter.slug` | 自动 sanitize |
| `title` | `frontmatter.title` | 必需，无默认 |
| `sub_title` | 正文首段第二句 或 tags 生成 | 自动生成 |
| `TLNR` | 正文首段（40-150字符） | 从开篇提取 |
| `cover.url` | `frontmatter.featured_image.url` | 必需，无默认 |
| `Date` | `frontmatter.date` | 当天日期 |
| `read_time` | `frontmatter.read_time` | `ceil(wordCount/200) min` |
| `main_category` | `frontmatter.category` | 必需，无默认 |
| `recommend_category` | - | 空字符串 |
| `article_body_content` | Markdown body 转换 | 按 CONVERSION_RULES |
| `CTA_alici_link` | PRODUCT_CATALOG 映射 | `https://app.alici.ai/` |
| `CTA button` | 按 category | "Try It NOW" |
| `meta_title` | `frontmatter.meta_title` | 使用 title（截断到60） |
| `meta_description` | `frontmatter.meta_description` | 从 TLNR 生成 |
| `tag_for_SEO` | `frontmatter.tags.join(", ")` | 从 title 提取关键词 |

## CTA 映射规则

根据文章关键词自动选择 CTA（参考 `PRODUCT_CATALOG.md`）：

| 关键词包含 | CTA_alici_link | CTA button |
|-----------|----------------|------------|
| video, 视频 | `https://app.alici.ai/pages/videoGen` | "Create AI Videos Now" |
| image, 图片, portrait | `https://app.alici.ai/pages/imageGen` | "Generate AI Images Free" |
| thumbnail | `https://app.alici.ai/` | "Create Thumbnails Now" |
| 其他 | `https://app.alici.ai/` | "Try It NOW" |

## 错误处理

### 可自动修复的错误
- meta_title 超长 → 智能截断
- meta_description 超长 → 智能截断
- Slug 格式错误 → 自动 sanitize
- Date 格式错误 → 自动转 ISO 8601
- read_time 缺失 → 自动计算

### 需要人工干预的错误
- `title` 缺失 → ERROR: "frontmatter 缺少 title 字段"
- `slug` 缺失 → ERROR: "frontmatter 缺少 slug 字段"
- `category` 缺失 → ERROR: "frontmatter 缺少 category 字段"
- `featured_image.url` 缺失 → ERROR: "缺少封面图 URL，请先运行 /edit-article"

## 输出示例

**转换报告**：
```
=== Markdown to Framer Conversion ===

Input: /reports/2026-01-15-best-ai-video-tools/01-article-edited.md
Status: ✅ SUCCESS

Auto-fixes applied:
- meta_title: 截断 72 → 60 字符
- Date: 格式化 2026-01-15 → 2026-01-15T00:00:00.000Z
- Special chars: em dash → hyphen (3 instances)

Validation:
✅ Slug: best-ai-video-generators-2025 (27 chars)
✅ meta_title: 60 chars
✅ meta_description: 142 chars
✅ main_category: list
✅ cover.url: HTTPS valid (no alt)
✅ Images: <img alt="..." src="..."> format (no figure)

Output: /reports/2026-01-15-best-ai-video-tools/06-article-final.json

Ready for Framer CMS import!
```

## 相关文件

- `CONVERSION_RULES.md` - Markdown → Framer HTML 详细规则
- `FIELD_SCHEMA.md` - 字段验证规则
- `../PRODUCT_CATALOG.md` - CTA 产品映射
- `/blog_new_sam 11.20.2025/doc/blog.json` - Framer JSON 参考模板
- `../blog-cover-generator/SKILL.md` - 封面生成 Skill (v1.2 集成)

---

## Changelog

**v1.3** (2026-01-22):
- **修复**: 图片格式 - `<img alt="..." src="...">` (无 figure 包裹，alt 在 src 前)
- **新增**: 特殊字符处理 - em dash/en dash/smart quotes/ellipsis 替换
- **修复**: cover 字段只保留 `url`，移除 `alt` 和 `cover_image_metadata`
- **简化**: 单路径输出 (`/reports/[date]-[topic]/06-article-final.json`)
- **新增**: JSON 格式强制要求提示（数组格式、cover 无 alt、图片无 figure）

**v1.2** (2026-01-22):
- NEW: 集成 blog-cover-generator 封面元数据
  - 自动读取 `06-cover-metadata.json`
  - 使用 `cdn_url` 作为 `cover.url`
- 优先级：cover-metadata > frontmatter > ERROR
- 向后兼容：无 cover-metadata 时仍使用 frontmatter

**v1.1** (2026-01-15):
- Initial release with auto-fix capabilities
