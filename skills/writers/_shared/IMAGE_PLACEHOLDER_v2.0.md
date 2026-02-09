# IMAGE_PLACEHOLDER v2.0 — Shared Component

> Structured image placeholder system for all Writer Skills.
> **Version**: 2.0
> **Updated**: 2026-02-07
> **Used by**: blog-tutorial-writer, blog-list-writer, blog-showdown-writer

---

## IMAGE_PLACEHOLDER v2.0 Format

```markdown
![Descriptive alt text](placeholder)
<!-- IMAGE_PLACEHOLDER
  id: "unique-kebab-case-id"
  type: "screenshot|diagram|comparison|hero|table|infographic"
  priority: "required|recommended|optional"
  alt: "Descriptive text with keywords for SEO + accessibility"
  where: "Position description (e.g., after paragraph 2 in Step 1)"
  context: "What user is doing at this point (optional)"
  size_hint: "1200x630"
-->
```

---

## Attributes

| Attribute | Required | Values | Purpose |
|-----------|----------|--------|---------|
| `id` | ✅ Yes | Unique string (kebab-case) | Identifies image for asset_plan.json |
| `type` | ✅ Yes | screenshot, diagram, comparison, hero, table, infographic | Determines generation strategy |
| `priority` | ✅ Yes | required, recommended, optional | Editor prioritizes "required" images first |
| `alt` | ✅ Yes | Descriptive text | SEO + accessibility |
| `where` | ✅ Yes | Position description | Helps Editor understand placement |
| `context` | ⭕ Optional | What user is doing | Improves prompt generation |
| `size_hint` | ⭕ Optional | Dimensions (WxH) | Guides aspect ratio |

---

## Type Definitions

| Type | Use Case | Example |
|------|----------|---------|
| `screenshot` | UI walkthrough, tool interface | "Kling 2.0 dashboard showing generation settings" |
| `diagram` | Workflow, process flow | "AI video generation pipeline: Input → Process → Output" |
| `comparison` | Side-by-side comparison | "Kling vs Runway output quality comparison" |
| `hero` | Article opener, featured image | "Cinematic AI-generated video showcasing Kling Motion Control" |
| `table` | Visual table / chart | "Pricing comparison chart across 5 AI video tools" |
| `infographic` | Data visualization | "AI video market growth 2024-2030 infographic" |

---

## Priority Guidelines

- **required**: Critical for understanding (e.g., Step 1 tool selection UI)
- **recommended**: Helpful but not blocking (e.g., workflow diagram)
- **optional**: Nice-to-have visual enhancement (e.g., decorative hero image)

---

## Placement Strategies (Per Skill)

### Tutorial Articles

| 位置 | 图片类型 | 频率 |
|------|----------|------|
| 标题下方 | 封面图 (hero) | 1x |
| 每个步骤 | 操作截图 (screenshot) | 5-7x |
| 对比章节 | 对比表格/图 (comparison) | 1x |
| CTA 区域 | 按钮图片 | 可选 |

**目标**: 5-7 张图片, 60% 文字 / 40% 视觉

### Listicle Articles

| 位置 | 图片类型 | 频率 |
|------|----------|------|
| 标题下方 | 封面图 (hero) | 1x |
| 每个工具/产品 | 界面截图 (screenshot) | 10-15x |
| 对比章节 | 对比表格 (table) | 1x |
| How to Choose | 决策流程图 (diagram) | 可选 |

**目标**: 10-15 张图片, 60% 文字 / 40% 视觉

### Showdown Articles

| 位置 | 图片类型 | 频率 |
|------|----------|------|
| 标题下方 | 封面图 (hero) | 1x |
| Deep Dives 每个工具 | 界面截图 (screenshot) | 1 per tool |
| Snapshot/Scorecard 附近 | 对比图 (comparison) | 1-2x |
| Decision Tree | 流程图 (diagram) | 可选 |

**目标**: 4-8 张图片, 60% 文字 / 40% 视觉

---

## Example: Complete Image Set

```markdown
<!-- Hero image -->
![AI video generation hero](placeholder)
<!-- IMAGE_PLACEHOLDER
  id: "hero-ai-video"
  type: "hero"
  priority: "recommended"
  alt: "Cinematic AI-generated video showcasing realistic human motion"
  where: "immediately after title, before Direct Answer"
  context: "First impression, sets tone for professional quality"
-->

<!-- Tool screenshot -->
![Tool comparison interface](placeholder)
<!-- IMAGE_PLACEHOLDER
  id: "step1-tool-comparison"
  type: "screenshot"
  priority: "required"
  alt: "Side-by-side comparison of Kling 2.0, Runway Gen-4, and Sora 2 interfaces"
  where: "in Step 1, after tool introduction paragraph"
  context: "User needs to see actual UI differences"
-->

<!-- Workflow diagram -->
![AI video workflow diagram](placeholder)
<!-- IMAGE_PLACEHOLDER
  id: "step3-workflow-diagram"
  type: "diagram"
  priority: "recommended"
  alt: "Step-by-step workflow: Upload → Configure → Generate → Download"
  where: "in Step 3, before detailed instructions"
  context: "Overview helps users understand full process"
-->
```

---

## Integration with Asset Pipeline

IMAGE_PLACEHOLDERs feed into the asset pipeline:

```
Writer → IMAGE_PLACEHOLDER v2.0 → asset_plan.json → Editor → asset_manifest.json
```

Each placeholder's `id` maps to an entry in `asset_plan.json` for automated image generation.

---

## Version History

### v2.0 (2026-02-05)
- Structured metadata format (6 types, 8 attributes)
- Automation-friendly for asset pipeline
- Per-skill placement strategies
- Extracted as shared component (2026-02-07)

### v1.0 (Prior)
- Simple `![alt](placeholder)` format
- No structured metadata
