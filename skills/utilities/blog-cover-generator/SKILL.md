---
name: blog-cover-generator
version: "2.0"
description: >
  Generate blog cover images for Alici.AI using Nano Banana Pro.
  Supports TWO cover categories:
  - Category A: Professional (6 types - minimalist, teal, abstract)
  - Category B: Thumbnail Style (4 types - vibrant, person-centered, YouTube aesthetic)
  Auto-detects category based on article content.
  Triggers on: 生成封面, blog cover, 封面图, generate cover, create thumbnail.
allowed-tools: Bash, Read, Write, Grep, Glob
env-required: FAL_API_KEY
dependencies:
  - path: "/skills/_docs/BRAND_VISUAL_GUIDE.md"
    purpose: "Color palette consistency for Professional covers"
  - path: "/skills/utilities/blog-cover-generator/THUMBNAIL_VISUAL_GUIDE.md"
    purpose: "Visual specs for Thumbnail Style covers (v2.0 NEW)"
  - path: "/scripts/fal_image_generator.py"
    purpose: "FAL.ai image generation and CDN upload"
---

# Blog Cover Generator Skill v2.0

> **Purpose**: Generate blog cover images for Alici.AI using Nano Banana Pro AI image generation.
> **v2.0 NEW**: Dual-category system - Professional (minimalist) + Thumbnail Style (vibrant, person-centered)

## Trigger Conditions

- User invokes `/generate-cover`
- SmartLauncher full auto flow (after competitive-validator, before markdown-to-framer)
- Keywords: "生成封面", "blog cover", "封面图", "generate cover", "create thumbnail"
- Auto-trigger condition: AEO >= 75 AND competitive-validator = PASS

---

## Two-Category Architecture (v2.0 NEW)

```
blog-cover-generator v2.0
│
├── Category A: Professional Cover (现有 6 种)
│   ├── Gradient Glow
│   ├── Fluid Shape
│   ├── Geometric Minimal
│   ├── Typography-Led
│   ├── Data Abstract
│   └── Grid/Matrix
│   └── 特点: 极简、留白 40%+、绿色系、抽象隐喻
│
└── Category B: Thumbnail Style Cover (v2.0 新增) 🆕
    ├── T1: Creator Showcase (作品展示)
    ├── T2: Money/Success (收益变现)
    ├── T3: Tutorial Hero (教程指南)
    └── T4: Reaction Shot (惊喜评测)
    └── 特点: 人脸核心、高饱和、动感背景、装饰元素
```

### Category Detection (Phase 1.5)

```python
def detect_cover_category(frontmatter, article_path):
    """
    判断使用 Professional 还是 Thumbnail 风格
    """
    thumbnail_signals = [
        "thumbnail", "缩略图", "封面设计",
        "youtube", "视频封面", "点击率"
    ]

    title = frontmatter.get("title", "").lower()
    tags = [t.lower() for t in frontmatter.get("tags", [])]

    # 检测文章路径是否在 thumbnail 相关目录
    if "thumbnail" in article_path.lower():
        return "thumbnail"  # → Category B

    # 检测标题或标签
    if any(signal in title for signal in thumbnail_signals):
        return "thumbnail"
    if any(signal in tags for signal in thumbnail_signals):
        return "thumbnail"

    return "professional"  # → Category A (默认)
```

### Thumbnail Subtype Selection (Phase 2.5)

```python
def select_thumbnail_subtype(frontmatter, article_body):
    """
    选择 Thumbnail 子类型 T1-T4
    """
    title_lower = frontmatter.get("title", "").lower()
    tags = [t.lower() for t in frontmatter.get("tags", [])]

    # T2: Money/Success
    if any(kw in title_lower for kw in ["money", "earn", "monetize", "$", "income", "revenue"]):
        return "T2-money-success"

    # T4: Reaction Shot
    if any(kw in title_lower for kw in ["vs", "comparison", "best", "review", "shocking", "amazing"]):
        return "T4-reaction-shot"

    # T1: Creator Showcase
    if any(kw in title_lower for kw in ["generated", "created", "showcase", "examples", "gallery"]):
        return "T1-creator-showcase"

    # T3: Tutorial Hero (default for thumbnail content)
    return "T3-tutorial-hero"
```

### Person Source Selection

```python
ALICI_LUCY_URL = "https://ct2.alici.ai/static/image/other/design/aliciLucy.png"
ALICI_ANDY_URL = "https://ct2.alici.ai/static/image/other/design/aliciAndy.png"

def select_person_source(user_input, preferences):
    """
    选择人物来源: Alici 模特 / AI 生成 / 用户自定义
    """
    # 1. 用户明确指定照片
    if user_input.has_photo:
        photo_url = upload_to_cdn(user_input.photo)
        return {"source": "custom", "url": photo_url}

    # 2. 用户指定使用模特
    if "lucy" in user_input.lower():
        return {"source": "alici", "url": ALICI_LUCY_URL, "name": "Lucy"}
    if "andy" in user_input.lower():
        return {"source": "alici", "url": ALICI_ANDY_URL, "name": "Andy"}

    # 3. 根据内容自动选择模特
    if preferences.get("gender") == "female":
        return {"source": "alici", "url": ALICI_LUCY_URL, "name": "Lucy"}
    elif preferences.get("gender") == "male":
        return {"source": "alici", "url": ALICI_ANDY_URL, "name": "Andy"}

    # 4. 默认使用 AI 生成通用人物
    return {"source": "ai_generated", "description": "friendly content creator"}
```

---

## Category A: Professional Cover

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

---

## Category B: Thumbnail Style Cover (v2.0 NEW)

> **详细规范**: 见 `THUMBNAIL_VISUAL_GUIDE.md`

### Thumbnail 子类型总览

| 子类型 | 代码 | 适用场景 | 背景色 | 人物姿态 | 装饰元素 |
|--------|------|---------|--------|---------|---------|
| **T1** | `creator-showcase` | AI 生成作品展示 | Red/Pink | 展示手势 | 设备框+闪光 |
| **T2** | `money-success` | 收益、变现 | Purple/Gold | 双手举物 | 金币+箭头 |
| **T3** | `tutorial-hero` | 教程、How-to | Blue/Green | 竖拇指 | 清单+播放键 |
| **T4** | `reaction-shot` | 评测、惊喜 | Red/Orange | 惊讶表情 | VS符号+截图 |

### Thumbnail 色彩规范

| 名称 | 色值 | 用途 |
|------|------|------|
| Electric Purple | `#7C3AED` | T2 背景 |
| Vibrant Red | `#EF4444` | T1/T4 背景 |
| Bright Blue | `#3B82F6` | T3 背景 |
| Golden Yellow | `#FBBF24` | 装饰强调 |

### Alici 模特库

| 模特 | URL | 适用场景 |
|------|-----|---------|
| 👩 AliciLucy | `https://ct2.alici.ai/static/image/other/design/aliciLucy.png` | 女性向、创作者 |
| 👨 AliciAndy | `https://ct2.alici.ai/static/image/other/design/aliciAndy.png` | 男性向、技术 |

---

## Execution Workflow (v2.0 Updated)

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

### Phase 1.5: Detect Cover Category (v2.0 NEW)

```python
def detect_cover_category(frontmatter, article_path):
    """
    判断使用 Professional (A) 还是 Thumbnail (B) 风格
    """
    thumbnail_signals = ["thumbnail", "缩略图", "封面设计", "youtube", "视频封面", "点击率"]

    title = frontmatter.get("title", "").lower()
    tags = [t.lower() for t in frontmatter.get("tags", [])]

    if "thumbnail" in article_path.lower():
        return "thumbnail"
    if any(signal in title or signal in tags for signal in thumbnail_signals):
        return "thumbnail"

    return "professional"
```

**分支逻辑**:
- `professional` → Phase 2 (原有流程)
- `thumbnail` → Phase 2-T (Thumbnail 子类型选择)

### Phase 2: Detect Content Type (Category A: Professional)

```python
def detect_content_type(frontmatter, article_body):
    """
    从文章元数据和内容检测内容类型 (仅用于 Professional 类型)
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

### Phase 2-T: Select Thumbnail Subtype (Category B: Thumbnail) (v2.0 NEW)

```python
def select_thumbnail_subtype(frontmatter):
    """
    选择 Thumbnail 子类型 T1-T4
    """
    title_lower = frontmatter.get("title", "").lower()

    if any(kw in title_lower for kw in ["money", "earn", "monetize", "$", "income"]):
        return "T2-money-success"
    if any(kw in title_lower for kw in ["vs", "comparison", "best", "review", "shocking"]):
        return "T4-reaction-shot"
    if any(kw in title_lower for kw in ["generated", "created", "showcase", "examples"]):
        return "T1-creator-showcase"

    return "T3-tutorial-hero"  # 默认
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

### Phase 4: Build Prompt from Template (v2.0 Updated)

```python
def build_cover_prompt(category, subtype, cover_text, color, person_source=None):
    """
    从模板构建完整 prompt (支持双类型)
    """
    # 根据类型选择模板文件
    if category == "thumbnail":
        template = read_template("THUMBNAIL_VISUAL_GUIDE.md", subtype)
        # Thumbnail 需要额外的人物信息
        if person_source and person_source.get("url"):
            prompt = template.replace("[PERSON_DESC:", f"Reference image: {person_source['url']}\n[PERSON_DESC:")
        else:
            prompt = template.replace("[PERSON_DESC:", "[PERSON_DESC: friendly content creator,")
    else:
        template = read_template("references/PROMPT_TEMPLATES.md", subtype)
        prompt = template

    # 替换通用变量
    prompt = prompt.replace("[H1_TEXT]", cover_text["h1"])
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
python scripts/fal_image_generator.py \
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

## Integration with SmartLauncher Flow (v2.0 Updated)

```
SmartLauncher (目标+组合)
       ↓
   Writer → Editor → AEO → [Improver] → Competitive Validator
       ↓
┌──────────────────────────────────────────────────────────┐
│  blog-cover-generator v2.0 (全自动)                       │
│                                                          │
│  Phase 1: 读取文章标题                                    │
│       ↓                                                  │
│  Phase 1.5: 判断封面类型 (v2.0 NEW)                       │
│       ├── thumbnail 关键词? → Category B (Thumbnail)     │
│       └── 其他 → Category A (Professional)               │
│       ↓                                                  │
│  ┌─────────────────┬─────────────────┐                   │
│  │ Category A      │ Category B      │                   │
│  │ (Professional)  │ (Thumbnail)     │                   │
│  ├─────────────────┼─────────────────┤                   │
│  │ Phase 2:        │ Phase 2-T:      │                   │
│  │ 检测内容类型    │ 选择 T1-T4      │                   │
│  │ (6 种背景)      │ 选择人物来源    │                   │
│  ├─────────────────┼─────────────────┤                   │
│  │ Phase 3:        │ Phase 3-T:      │                   │
│  │ 选择背景类型    │ 选择背景+装饰   │                   │
│  └────────┬────────┴────────┬────────┘                   │
│           └────────┬────────┘                            │
│                    ↓                                     │
│  Phase 4: 从模板构建 Prompt                               │
│       ↓                                                  │
│  Phase 5: FAL.ai 生成                                     │
│       ↓                                                  │
│  Phase 6: CDN 上传                                        │
│       ↓                                                  │
│  Phase 7: 输出 06-cover-metadata.json                     │
└──────────────────────────────────────────────────────────┘
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

**v2.0** (2026-01-30):
- **Two-Category Architecture**: Professional (A) + Thumbnail Style (B)
- **Category B: Thumbnail Style** - 4 subtypes (T1-T4)
  - T1 Creator Showcase: 作品展示
  - T2 Money/Success: 收益变现
  - T3 Tutorial Hero: 教程指南
  - T4 Reaction Shot: 惊喜评测
- **Alici 模特库**: Lucy + Andy 预设模特
- **Person Source System**: Alici 模特 / AI 生成 / 用户自定义
- **THUMBNAIL_VISUAL_GUIDE.md**: 完整 Thumbnail 视觉规范
- **Phase 1.5**: 自动检测封面类型
- **Phase 2-T**: Thumbnail 子类型选择
- **高饱和色彩系统**: Purple/Red/Blue/Green + Gold/Pink/Orange

**v1.0** (2026-01-22):
- Initial release
- 6 background types with teal brand colors
- Auto content type detection
- Title smart split (H1 ≤3 words)
- FAL.ai integration via shared script
- CDN upload automation
- Metadata output for markdown-to-framer integration
