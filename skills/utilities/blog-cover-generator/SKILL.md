---
name: blog-cover-generator
version: "1.0"
description: >
  Generate minimalist blog cover images for Alici.AI using Nano Banana Pro.
  6 background types (Gradient Glow, Fluid Shape, Geometric, Typography-Led, Data Abstract, Grid)
  with teal brand color palette and text hierarchy system.
  Triggers on: 生成封面, blog cover, 封面图, generate cover, create thumbnail.
allowed-tools: Bash, Read, Write, Grep, Glob
env-required: FAL_API_KEY
dependencies:
  - path: "/skills/_docs/BRAND_VISUAL_GUIDE.md"
    purpose: "Color palette consistency (teal colors align with brand guide)"
  - path: "/scripts/fal_image_generator.py"
    purpose: "FAL.ai image generation and CDN upload"
---

# Blog Cover Generator Skill v1.0

> **Purpose**: Generate minimalist, professional blog cover images for Alici.AI using Nano Banana Pro AI image generation.

## Trigger Conditions

- User invokes `/generate-cover`
- SmartLauncher full auto flow (after competitive-validator, before markdown-to-framer)
- Keywords: "生成封面", "blog cover", "封面图", "generate cover", "create thumbnail"
- Auto-trigger condition: AEO >= 75 AND competitive-validator = PASS

## Design Principles

| Principle | Description |
|-----------|-------------|
| **Color Unity** | Teal color family as primary, black base, white text |
| **Form Diversity** | Vary background forms within unified color palette |
| **Minimal Restraint** | One visual focus per image, ≥50% negative space |
| **Text Clarity** | Titles readable at thumbnail size |

---

## Color Specification

### Primary Colors (90% usage)

| Name | Hex | Usage |
|------|-----|-------|
| Core Teal | #4FD1C5 | Default gradient |
| Light Teal | #81E6D9 | Lighter, airy feel |
| Deep Teal | #319795 | Deeper, stable feel |

### Secondary Colors (10% usage)

| Name | Hex | Usage |
|------|-----|-------|
| Slate | #64748B | Neutral/comparison content |
| Cool Gray | #9CA3AF | Technical/documentation |

### Fixed Colors

| Name | Value | Usage |
|------|-------|-------|
| Background | #000000 | All cover bases |
| Text Primary | #FFFFFF | Main titles |
| Text Secondary | #FFFFFF 70% | Subtitles |

---

## 6 Background Types

### Type 1: Gradient Glow
Soft gradient flowing from corner/edge into black.
- **Best for**: Model releases, version updates, general content
- **Template**: See `references/PROMPT_TEMPLATES.md` Type 1

### Type 2: Fluid Shape
Abstract liquid/ribbon shape floating on black.
- **Best for**: Feature introductions, creative tools, motion-related content
- **Template**: See `references/PROMPT_TEMPLATES.md` Type 2

### Type 3: Geometric Minimal
Simple geometric elements (lines, circles, dots).
- **Best for**: Technical docs, precision features, structured content
- **Template**: See `references/PROMPT_TEMPLATES.md` Type 3

### Type 4: Typography-Led
Text hierarchy as primary visual, minimal background glow.
- **Best for**: Major releases, brand/product emphasis
- **Template**: See `references/PROMPT_TEMPLATES.md` Type 4

### Type 5: Data Abstract
Abstract curves/waves suggesting data visualization.
- **Best for**: Comparisons, performance analysis, trend content
- **Template**: See `references/PROMPT_TEMPLATES.md` Type 5

### Type 6: Grid/Matrix
Sparse dot grid or line patterns.
- **Best for**: Deep technical content, AI/algorithm topics
- **Template**: See `references/PROMPT_TEMPLATES.md` Type 6

---

## Typography Rules

### Hierarchy

| Level | Content | Weight | Relative Size | Opacity |
|-------|---------|--------|---------------|---------|
| H1 | Main title/product | Bold/Black | 100% | 100% |
| H2 | Subtitle/feature | Bold | 50-60% | 100% |
| H3 | Description | Regular | 25-30% | 70% |
| Tag | "Officially on Alici.AI" | Regular | 20% | 60% |

### Text Length Rules
- **H1**: ≤3 words (optimal for AI text rendering)
- **Longer titles**: Split into H1 + H2 combination

### Position
- Default: Vertically centered, slight bias toward lower third
- Adjust based on background element position (text opposite to visual element)

---

## Content Type → Background Type Mapping

| Content Scenario | Primary Type | Alternative | Color |
|-----------------|--------------|-------------|-------|
| New model launch | Type 1 Gradient / Type 4 Typography | Type 2 Fluid | Core Teal |
| Feature tutorial | Type 2 Fluid / Type 3 Geometric | Type 1 Gradient | Core Teal |
| Motion/dynamic features | Type 2 Fluid | Type 5 Data | Core Teal |
| Comparison/review (vs) | Type 5 Data | Type 3 Geometric | Slate |
| Technical deep-dive | Type 6 Grid / Type 3 Geometric | Type 1 Gradient | Core Teal |
| Workflow/tutorial | Type 3 Geometric / Type 5 Data | Type 2 Fluid | Core Teal |
| Major announcement | Type 4 Typography | Type 1 Gradient | Core Teal |
| Audio features | Type 2 Fluid (wave) | Type 5 Data | Light Teal |

---

## Execution Workflow

### Phase 1: Extract Title from Article

```python
# Pseudocode
def extract_cover_text(article_path):
    """
    从文章提取封面所需的标题层级
    """
    # 读取 YAML frontmatter
    frontmatter = parse_yaml(article_path)

    # 获取完整标题
    full_title = frontmatter.get("title", "")

    # 标题分解逻辑
    if word_count(full_title) <= 3:
        h1_text = full_title.upper()
        h2_text = None
    else:
        # 智能分解：找到核心产品名/动作词
        h1_text, h2_text = smart_split_title(full_title)

    # 可选 H3 从 subtitle 或 tags 生成
    h3_text = frontmatter.get("subtitle") or generate_from_tags(frontmatter.get("tags", []))

    return {
        "h1": h1_text,    # ≤3 words, UPPERCASE
        "h2": h2_text,    # 补充信息
        "h3": h3_text     # 可选描述
    }
```

**Title Split Examples**:

| Original Title | H1 | H2 |
|---------------|----|----|
| "Kling 2.6 Complete Guide" | "KLING 2.6" | "Complete Guide" |
| "Best AI Video Generators 2026" | "AI VIDEO" | "Best Generators 2026" |
| "Sora vs Runway vs Kling" | "SORA vs RUNWAY" | "vs Kling" |
| "Motion Control Tutorial" | "MOTION CONTROL" | "Tutorial" |

### Phase 2: Detect Content Type

```python
def detect_content_type(frontmatter, article_body):
    """
    从文章元数据和内容检测内容类型
    """
    title_lower = frontmatter.get("title", "").lower()
    category = frontmatter.get("category", "")
    tags = frontmatter.get("tags", [])

    # 检测规则（优先级从高到低）
    if "vs" in title_lower or "对比" in title_lower or "comparison" in title_lower:
        return "comparison"

    if any(word in title_lower for word in ["2.0", "2.5", "2.6", "launch", "release", "新版"]):
        return "model_release"

    if category == "tutorial" or "how to" in title_lower or "guide" in title_lower:
        return "tutorial"

    if category == "list" or "best" in title_lower or "top" in title_lower:
        return "list_article"

    if any(tag in ["motion", "video", "动态"] for tag in tags):
        return "motion_feature"

    if any(tag in ["api", "developer", "技术"] for tag in tags):
        return "technical"

    return "general"
```

### Phase 3: Select Background Type

```python
def select_background_type(content_type):
    """
    根据内容类型选择背景类型和颜色
    """
    TYPE_MAP = {
        "model_release": {"type": "gradient-glow", "alt": "typography-led", "color": "#4FD1C5"},
        "tutorial": {"type": "fluid-shape", "alt": "geometric", "color": "#4FD1C5"},
        "comparison": {"type": "data-abstract", "alt": "geometric", "color": "#64748B"},
        "list_article": {"type": "gradient-glow", "alt": "data-abstract", "color": "#4FD1C5"},
        "motion_feature": {"type": "fluid-shape", "alt": "data-abstract", "color": "#4FD1C5"},
        "technical": {"type": "grid-matrix", "alt": "geometric", "color": "#4FD1C5"},
        "general": {"type": "gradient-glow", "alt": "fluid-shape", "color": "#4FD1C5"}
    }
    return TYPE_MAP.get(content_type, TYPE_MAP["general"])
```

### Phase 4: Build Prompt from Template

```python
def build_cover_prompt(background_type, cover_text, color):
    """
    从模板构建完整 prompt
    """
    # 读取模板
    template = read_template(f"references/PROMPT_TEMPLATES.md", background_type)

    # 替换变量
    prompt = template.replace("[H1_TEXT]", cover_text["h1"])
    prompt = prompt.replace("[H2_TEXT]", cover_text.get("h2", ""))
    prompt = prompt.replace("[H3_TEXT]", cover_text.get("h3", ""))
    prompt = prompt.replace("[COLOR]", color)

    # 清理未使用的可选行
    prompt = clean_optional_lines(prompt)

    return prompt
```

### Phase 5: Generate Image via FAL.ai

```bash
# 使用项目统一脚本生成封面
python /Users/H/Documents/AliciBlog/scripts/fal_image_generator.py \
  --prompt "[generated_prompt]" \
  --role cover \
  --aspect-ratio 16:9 \
  --resolution 2K \
  --output-dir /reports/YYYY-MM-DD-{topic-slug}/assets \
  --filename cover.png
```

**API Parameters**:
- **Model**: fal-ai/nano-banana
- **Aspect Ratio**: 16:9 (fixed for blog covers)
- **Resolution**: 2K
- **num_inference_steps**: 35
- **guidance_scale**: 7.5

### Phase 6: Upload to CDN

```bash
# 自动上传到 CDN
rsync -avz /reports/YYYY-MM-DD-{topic-slug}/assets/cover.png \
  root@45.76.70.215:/var/www/static/static/image/other/gen_images/

# CDN URL 格式
# https://ct2.alici.ai/static/image/other/gen_images/cover.png
```

### Phase 7: Generate Metadata

```json
// 06-cover-metadata.json
{
  "background_type": "gradient-glow",
  "color": "#4FD1C5",
  "h1_text": "KLING 2.6",
  "h2_text": "Complete Guide",
  "h3_text": null,
  "prompt_used": "[full prompt text]",
  "cdn_url": "https://ct2.alici.ai/static/image/other/gen_images/{slug}-cover.png",
  "local_path": "/reports/YYYY-MM-DD-{slug}/assets/cover.png",
  "generated_at": "2026-01-22T14:30:00Z",
  "model": "fal-ai/nano-banana",
  "aspect_ratio": "16:9",
  "resolution": "2K"
}
```

---

## Output Files

```
/reports/YYYY-MM-DD-{topic-slug}/
├── ...existing files...
├── assets/
│   └── cover.png                   # 封面图片 (1920x1080)
├── 06-cover-metadata.json          # 封面元数据
└── 07-article-final.json           # Framer JSON (含 cover_image_url)
```

---

## Integration with SmartLauncher Flow

```
SmartLauncher (目标+组合)
       ↓
   Writer → Editor → AEO → [Improver] → Competitive Validator
       ↓
┌──────────────────────────────────┐
│  blog-cover-generator (全自动)    │
│  └── 读取文章标题                 │
│  └── 选择背景类型                 │
│  └── 生成 Prompt                  │
│  └── FAL.ai 生成                  │
│  └── CDN 上传                     │
│  └── 输出 06-cover-metadata.json  │
└──────────────────────────────────┘
       ↓
   markdown-to-framer (读取 cover_image_url)
       ↓
   framer-previewer
```

---

## Key Prompt Techniques for Minimalism

| Technique | Description |
|-----------|-------------|
| **Negative description** | Include "no texture, no noise, no decorative elements" |
| **Light source** | Use "soft diffused glow" not "dramatic lighting" |
| **Whitespace emphasis** | Specify "generous negative space" or "60% of frame remains black" |
| **Text control** | Keep text ≤3 words for best results |
| **Gradient description** | Use "organic gradient" / "aurora-like" / "liquid light" |

---

## Error Handling

| Error | Action |
|-------|--------|
| FAL_API_KEY not set | ERROR: "请设置 FAL_API_KEY 环境变量" |
| Article missing title | ERROR: "文章缺少 title 字段，无法生成封面" |
| Generation failed | Log error, retry once, then suggest manual generation |
| CDN upload failed | Save locally, log warning, continue with local path |

---

## Quick Start

**Command**:
```bash
/generate-cover [path/to/01-article-edited.md]
```

**Expected Flow**:
1. Read article, extract title and metadata
2. Detect content type from title/category/tags
3. Select background type from mapping table
4. Extract H1/H2/H3 text (H1 ≤3 words)
5. Build prompt from template
6. Generate image via FAL.ai
7. Upload to CDN
8. Output `06-cover-metadata.json`
9. Update `00-implementation.md`

**Auto-trigger in SmartLauncher**:
```
After competitive-validator = PASS:
→ Auto-invoke blog-cover-generator
→ Read 01-article-edited.md
→ Generate cover
→ Pass cover_image_url to markdown-to-framer
```

---

## Changelog

**v1.0** (2026-01-22):
- Initial release
- 6 background types with teal brand colors
- Auto content type detection
- Title smart split (H1 ≤3 words)
- FAL.ai integration via shared script
- CDN upload automation
- Metadata output for markdown-to-framer integration
