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
