# Convert to Framer Command (v1.1)

Convert a completed Markdown article to Framer CMS JSON format with automatic validation and repair.

## Usage

```
/convert-to-framer [path/to/article.md]
```

**Example:**
```
/convert-to-framer /reports/2026-01-15-best-ai-video-tools/01-article-edited.md
```

## What This Command Does

1. **Parses** YAML frontmatter and Markdown body
2. **Maps** frontmatter fields to Framer JSON structure
3. **Converts** Markdown body to Framer HTML format
4. **Validates** all fields against schema constraints
5. **Auto-fixes** constraint violations (length, format)
6. **Outputs** JSON to two locations

## Prerequisites

- Article must have YAML frontmatter with:
  - `title` (required)
  - `slug` (required)
  - `category` (required)
  - `featured_image.url` (required)
- AEO score should be ≥ 75 (recommended)
- Recommend running `/edit-article` first

## Auto-Fix Capabilities

| Issue | Auto-Fix Strategy |
|-------|-------------------|
| `meta_title` > 60 chars | Smart truncate to 57 + "..." |
| `meta_description` > 160 chars | Smart truncate to 157 + "..." |
| Invalid `Slug` characters | Lowercase + hyphenate + sanitize |
| `Date` wrong format | Convert to ISO 8601 |
| Missing `read_time` | Calculate from word count |
| Missing `TLNR` | Generate from opening paragraph |
| Missing `sub_title` | Generate from context |
| Missing `tag_for_SEO` | Extract from tags array |

## Errors That Require Manual Fix

| Error | Solution |
|-------|----------|
| Missing `title` | Add title to frontmatter |
| Missing `slug` | Add slug to frontmatter |
| Missing `category` | Add category: tutorial/list/news |
| Missing `featured_image.url` | Run `/edit-article` first |

## Output Files

JSON file created in reports directory:

```
/reports/[date]-[topic]/06-article-final.json
```

> **Note**: JSON is in array format `[{...}]` as required by Framer CMS.

## Framer HTML Format

The command converts Markdown to Framer-specific HTML:

| Markdown | Framer HTML |
|----------|-------------|
| `## H2` | `<h6><strong>...</strong></h6>` |
| `- item` | `<li data-preset-tag="p"><p>item</p></li>` |
| `[text](url)` | `<a href="url" target="_blank">text</a>` |
| Tables | Wrapped in `<figure>` |
| Images | `<img alt="..." src="...">` (no figure wrapper, alt before src) |
| Em dash `—` | ` - ` (space + hyphen + space) |

## Output JSON Structure

```json
[
  {
    "Slug": "best-ai-video-generators-2025",
    "title": "10 Best AI Video Generators in 2025",
    "sub_title": "Compare top AI video tools...",
    "TLNR": "The best AI video generator depends...",
    "cover": { "url": "https://..." },
    "Date": "2026-01-15T00:00:00.000Z",
    "read_time": "12 min",
    "main_category": "list",
    "recommend_category": "",
    "article_body_content": "<p>...</p>",
    "CTA_alici_link": "https://app.alici.ai/pages/videoGen",
    "CTA button": "Create AI Videos Now",
    "meta_title": "10 Best AI Video Generators 2025...",
    "meta_description": "Compare the 10 best AI video...",
    "tag_for_SEO": "ai video generator, best ai tools..."
  }
]
```

## CTA Auto-Mapping

CTA links are automatically selected based on article content:

| Keywords in Article | CTA Link | CTA Text |
|--------------------|----------|----------|
| video, 视频 | `/pages/videoGen` | "Create AI Videos Now" |
| image, 图片, portrait | `/pages/imageGen` | "Generate AI Images Free" |
| Other | `/` | "Try It NOW" |

## Example Output

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
✅ Images: <img alt="..." src="..."> format

Output: /reports/2026-01-15-best-ai-video-tools/06-article-final.json

Ready for Framer CMS import!
```

## Integration with Full Workflow

This command is automatically invoked in `/full-workflow` as Phase 6:

```
Phase 1: Scout → Phase 2: Write → Phase 3: Preview →
Phase 4: Score → Phase 5: Edit → Phase 6: Convert ← This command
Phase 7 (optional): Video Integration → /convert-to-video-framer-json 06-article-final.json
```

## Related Skills

- `/edit-article` - Should run before this command
- `/analyze-aeo` - Verify AEO score before converting
- `/full-workflow` - Includes this as Phase 6

## Skill Reference

See detailed rules in:
- `skills/utilities/markdown-to-framer/SKILL.md`
- `skills/utilities/markdown-to-framer/CONVERSION_RULES.md`
- `skills/utilities/markdown-to-framer/FIELD_SCHEMA.md`
