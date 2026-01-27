# Framer JSON 字段校验规则

> 所有字段的验证规则、约束条件和自动修复策略

## ⚠️ JSON 格式重要提示

**必须**：输出 JSON 必须是**数组格式** `[{...}]`，不能是单独对象 `{...}`

```json
// ✅ 正确 - 数组格式
[
  {
    "Slug": "...",
    "title": "..."
  }
]

// ❌ 错误 - 单独对象（Framer 会报错 "TypeError: o is not iterable"）
{
  "Slug": "...",
  "title": "..."
}
```

## 字段概览

| 字段 | 必需 | 类型 | 约束 | 自动修复 |
|------|------|------|------|----------|
| `Slug` | ✅ | string | `^[a-z0-9\-]+$`, 20-100 chars | ✅ |
| `title` | ✅ | string | 10-100 chars | ❌ |
| `sub_title` | ❌ | string | max 200 chars | ✅ 自动生成 |
| `TLNR` | ✅ | string | 50-300 chars | ✅ 自动生成 |
| `cover.url` | ✅ | string | HTTPS URL | ❌ |
| `Date` | ✅ | string | ISO 8601 | ✅ |
| `read_time` | ✅ | string | `^\d+ min$` | ✅ |
| `main_category` | ✅ | enum | tutorial/list/news | ✅ |
| `recommend_category` | ❌ | string | - | ✅ 默认空 |
| `article_body_content` | ✅ | string | HTML, ≥1000 chars | ✅ 转换生成 |
| `CTA_alici_link` | ✅ | string | URL | ✅ 默认值 |
| `CTA button` | ✅ | string | - | ✅ 默认值 |
| `meta_title` | ✅ | string | max 60 chars | ✅ 截断 |
| `meta_description` | ✅ | string | max 160 chars | ✅ 截断 |
| `tag_for_SEO` | ✅ | string | 逗号分隔 | ✅ 自动生成 |

---

## 详细字段规则

### 1. Slug

**规则**：
- 正则：`^[a-z0-9\-]+$`（仅小写字母、数字、连字符）
- 长度：20-100 字符
- 不能以连字符开头或结尾

**自动修复**：
```
输入: "Best AI Video Generators 2025!"
步骤:
1. 转小写: "best ai video generators 2025!"
2. 空格→连字符: "best-ai-video-generators-2025!"
3. 移除非法字符: "best-ai-video-generators-2025"
输出: "best-ai-video-generators-2025"
```

**错误条件**：
- 修复后仍少于 20 字符 → ERROR
- 源字段 `slug` 不存在 → ERROR

---

### 2. title

**规则**：
- 长度：10-100 字符
- 必须是英文
- 不能包含 Markdown 语法

**自动修复**：无（必需字段，不自动生成）

**错误条件**：
- 字段不存在 → ERROR: "frontmatter 缺少 title 字段"
- 少于 10 字符 → ERROR: "title 太短，至少需要 10 字符"

---

### 3. sub_title

**规则**：
- 最大 200 字符
- 可选字段

**自动生成策略**：
```
优先级:
1. 如果 frontmatter 有 sub_title → 使用它
2. 否则，从正文首段提取第二句
3. 否则，从 tags 生成: "A comprehensive guide to {tag1}, {tag2}, and {tag3}"
```

---

### 4. TLNR (Too Long; Not Reading)

**规则**：
- 长度：50-300 字符
- 必须直接回答标题中的问题
- 用于 AI 答案引擎（AEO）

**自动生成策略**：
```
1. 提取正文首段（H1 之后的第一段）
2. 如果首段 > 300 字符，智能截断到完整句子
3. 如果首段 < 50 字符，追加 meta_description 内容
```

---

### 5. cover.url

**规则**：
- 必须是 HTTPS URL
- 正则：`^https://`
- JSON 格式：`{ "url": "https://..." }`
- **不包含 `alt` 属性**（Framer CMS 不支持）

**正确格式** ✅：
```json
"cover": {
  "url": "https://example.com/image.png"
}
```

**错误格式** ❌（不要这样写）：
```json
"cover": {
  "url": "https://example.com/image.png",
  "alt": "Image description"
}
```

**自动修复**：无法自动修复（URL 必须由 blog-cover-generator 或 frontmatter 提供）

**错误条件**：
- 字段不存在 → ERROR: "缺少封面图 URL，请先运行 /edit-article 生成图片"
- 不是 HTTPS → ERROR: "封面图 URL 必须使用 HTTPS 协议"
- 包含 alt 字段 → WARNING: 移除 alt 字段（Framer 不支持）

---

### 6. Date

**规则**：
- 格式：ISO 8601 (`YYYY-MM-DDTHH:mm:ss.000Z`)

**自动修复**：
```
输入: "2026-01-15"
输出: "2026-01-15T00:00:00.000Z"

输入: "January 15, 2026"
输出: "2026-01-15T00:00:00.000Z"

输入: 缺失
输出: "[当天日期]T00:00:00.000Z"
```

---

### 7. read_time

**规则**：
- 格式：`^\d+ min$`（如 "8 min"）

**自动生成策略**：
```
1. 如果 frontmatter 有 read_time → 使用它
2. 否则计算：ceil(wordCount / 200) + " min"
   - wordCount = 正文英文单词数
   - 200 = 平均阅读速度（词/分钟）
```

---

### 8. main_category

**规则**：
- 枚举值：`tutorial` | `list` | `news`

**自动修复**（映射表）：
```
frontmatter.category → main_category
----------------------------------
"tutorial" → "tutorial"
"how-to" → "tutorial"
"guide" → "tutorial"
"list" → "list"
"comparison" → "list"
"best" → "list"
"top" → "list"
"news" → "news"
"announcement" → "news"
"update" → "news"
```

**错误条件**：
- 无法映射到有效枚举 → ERROR: "category '{value}' 无法映射，请使用 tutorial/list/news"

---

### 9. article_body_content

**规则**：
- 必须是有效 HTML
- 最小长度：1000 字符（HTML 包含标签）
- 遵循 `CONVERSION_RULES.md` 中的格式

**自动生成**：从 Markdown body 转换

---

### 10. CTA_alici_link

**规则**：
- 必须是有效 URL

**自动生成策略**（基于关键词）：
```
if title/body 包含 "video" → "https://app.alici.ai/pages/videoGen"
if title/body 包含 "image" → "https://app.alici.ai/pages/imageGen"
if title/body 包含 "portrait" → "https://app.alici.ai/pages/imageGen"
if title/body 包含 "thumbnail" → "https://app.alici.ai/"
else → "https://app.alici.ai/"
```

---

### 11. CTA button

**规则**：
- 按钮文字

**自动生成策略**：
```
if category == "tutorial" → "Try It FREE"
if category == "list" → "Compare Now"
if category == "news" → "Learn More"
if CTA_alici_link 包含 "videoGen" → "Create AI Videos Now"
if CTA_alici_link 包含 "imageGen" → "Generate AI Images Free"
else → "Try It NOW"
```

---

### 12. meta_title

**规则**：
- 最大 60 字符（SEO 标准）
- 包含主关键词

**自动修复（智能截断）**：
```python
def truncate_meta_title(text, max_length=60):
    if len(text) <= max_length:
        return text

    # 找到 max_length-3 之前的最后一个空格
    truncated = text[:max_length-3]
    last_space = truncated.rfind(' ')

    if last_space > 0:
        return truncated[:last_space] + "..."
    else:
        return truncated + "..."

# 示例
输入: "10 Best AI Video Generators in 2025: Complete Comparison Guide for Creators"
输出: "10 Best AI Video Generators in 2025: Complete..."
```

**自动生成**（如果缺失）：使用 `title` 字段，然后截断

---

### 13. meta_description

**规则**：
- 最大 160 字符（SEO 标准）
- 包含主关键词和价值主张

**自动修复（智能截断）**：
```python
def truncate_meta_description(text, max_length=160):
    if len(text) <= max_length:
        return text

    # 找到 max_length-3 之前的最后一个句号或空格
    truncated = text[:max_length-3]

    # 优先在句号处截断
    last_period = truncated.rfind('.')
    if last_period > max_length * 0.7:  # 如果句号在 70% 之后
        return truncated[:last_period+1]

    # 否则在空格处截断
    last_space = truncated.rfind(' ')
    if last_space > 0:
        return truncated[:last_space] + "..."
    else:
        return truncated + "..."
```

**自动生成**（如果缺失）：使用 TLNR 的前 160 字符

---

### 14. tag_for_SEO

**规则**：
- 逗号分隔的关键词列表
- 4-6 个关键词为佳

**自动生成策略**：
```
1. 如果 frontmatter.tags 存在 → tags.join(", ")
2. 否则，从 title 提取关键词（移除停用词）
```

---

## 校验执行顺序

```
1. 检查必需字段存在
   └─ title, slug, category, featured_image.url

2. 应用字段映射
   └─ frontmatter → Framer JSON

3. 自动生成缺失的可选字段
   └─ sub_title, TLNR, read_time, etc.

4. 自动修复约束违规
   └─ 长度截断、格式转换

5. 最终验证
   └─ 所有字段符合规则

6. 输出或报错
```

---

## 错误级别

| 级别 | 描述 | 处理 |
|------|------|------|
| **ERROR** | 无法自动修复 | 停止并报告 |
| **WARNING** | 已自动修复 | 继续并记录 |
| **INFO** | 自动生成 | 继续并记录 |

**报告示例**：
```
=== Field Validation Report ===

ERRORS (0):
(none)

WARNINGS (2):
- meta_title: 截断 72 → 60 字符
- Date: 格式化 "2026-01-15" → "2026-01-15T00:00:00.000Z"

INFO (3):
- sub_title: 自动生成从正文首段
- TLNR: 自动生成从开篇段落
- tag_for_SEO: 从 frontmatter.tags 生成

Status: ✅ VALID (ready for output)
```

---

## 追加字段（与 blog_scheme_example.json 对齐）

> 说明：以下为在 `blog_scheme_example.json` 中出现、但本文件原先未明确定义的字段。为保持兼容与完整性，这些字段的规则在此补充。遵循项目约定：除“视频插入阶段新增字段”外，任何 example 中存在而源 JSON 缺失的字段都不可使用示例默认值或空值填充，必须来自源 JSON；否则应中止并提示。

### 元数据补充字段

| 字段 | 必需 | 类型 | 约束 | 值来源 |
|------|------|------|------|--------|
| `:draft` | ❌ | boolean | 草稿标记 | 仅可来自源 JSON（不可默认） |
| `Author` | ❌ | string | 作者名（可为空字符串，但值需来自源） | 仅可来自源 JSON（不可默认） |
| `hasTiktokVideo` | ❌ | boolean | 是否含 TikTok 视频 | 仅可来自源 JSON（不可默认） |
| `VideoURL1` | ❌ | string | 视频 URL（HTTPS 建议） | 仅可来自源 JSON（不可默认） |
| `IsDrafts` | ❌ | boolean | 备用草稿标记（与 `:draft` 并存时按来源保持） | 仅可来自源 JSON（不可默认） |
| `TLNR 2` | ❌ | string | TLNR 补充文案 | 仅可来自源 JSON（不可默认） |

补充说明：
- 上述字段若 example 中存在而源 JSON 缺失，不得以示例值或空值补齐，应“阻断并提示”。
- 字段名区分大小写，输出应与 example 的命名形式一致（值取自源 JSON 的等义字段）。

### 视频插入阶段新增字段（仅由本 Skill 生成）

> 这些字段不要求出现在输入的源 JSON 中，由“视频插入”流程根据用户确认的插入点生成；当未使用某一插入点时，可按 example 约定输出空字符串以占位。

| 字段 | 必需 | 类型 | 约束 | 说明 |
|------|------|------|------|------|
| `video_link_1` | ❌ | string | 建议 HTTPS URL | 表示“正文之前”的视频链接（若用户选择该插入点） |
| `article_body_content_2` | ❌ | string | HTML | 拆分后正文的第二段；未使用可为空字符串 |
| `video_link_2` | ❌ | string | 建议 HTTPS URL | 插入在 `article_body_content` 与 `_2` 之间；未使用可为空字符串 |
| `article_body_content_3` | ❌ | string | HTML | 拆分后第三段；未使用可为空字符串 |
| `video_link_3` | ❌ | string | 建议 HTTPS URL | 插入在 `_2` 与 `_3` 之间；未使用可为空字符串 |
| `article_body_content_4` | ❌ | string | HTML | 拆分后第四段；未使用可为空字符串 |
| `video_link_4` | ❌ | string | 建议 HTTPS URL | 插入在 `_3` 与 `_4` 之间；未使用可为空字符串 |
| `article_body_content_5` | ❌ | string | HTML | 拆分后第五段；未使用可为空字符串 |
| `video_link_5` | ❌ | string | 建议 HTTPS URL | 插入在 `_4` 与 `_5` 之间；未使用可为空字符串 |

严格要求（视频阶段）：
- 不注入任何 `<iframe>`/`<video>` HTML 到正文；正文仅拆分为多段。
- `article_body_content` 作为第一段，后续段依次为 `article_body_content_2`、`_3`、`_4`、`_5`。
- 有多少插入点，就输出对应数量的 `video_link_N`；未使用的段/链接可用空字符串占位（与 example 一致）。
- 其余所有字段必须逐字复制自源 JSON，值不得改动。

---

## 完整字段清单（以 example 为准）

> 输出字段集 = 源 JSON 字段 ∪ example 字段。对于 example 中出现的“元数据字段”，值必须来自源 JSON；对于“视频插入阶段新增字段”，值来源于用户提供的视频链接与正文拆分结果。

按示例包含（示例顺序）：
- `Slug`
- `:draft`
- `Author`
- `hasTiktokVideo`
- `VideoURL1`
- `IsDrafts`
- `title`
- `sub_title`
- `TLNR`
- `TLNR 2`
- `cover`（对象，需包含 `url`）
- `Date`
- `read_time`
- `main_category`
- `recommend_category`
- `video_link_1`
- `article_body_content`
- `video_link_2`
- `article_body_content_2`
- `video_link_3`
- `article_body_content_3`
- `video_link_4`
- `article_body_content_4`
- `video_link_5`
- `article_body_content_5`
- `CTA_alici_link`
- `CTA button`
- `meta_title`
- `meta_description`
- `tag_for_SEO`

校验与失败策略：
- 若上述“元数据补充字段”在 example 中存在而源 JSON 缺失 → 直接报错并中止（禁止使用示例默认值）。
- “视频插入阶段新增字段”由本 Skill 生成；未使用的插入点允许输出空字符串以占位。
