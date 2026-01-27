---
name: image-placeholder-filler
version: "1.1"
status: DEPRECATED
deprecated_since: "2026-01-15"
replacement: "editor v2.0"
description: >
  ⚠️ DEPRECATED - This skill is no longer maintained. Use Editor Skill v2.0 instead.
  All image generation functionality has been consolidated into Editor Skill v2.0
  with nano-banana-pro model and strategic image selection.
  Triggers on: fill images, generate images, image placeholders, add images.
allowed-tools: Bash, Read, Write, Grep, Glob
env-required: FAL_API_KEY
---

# ⚠️ DEPRECATED - Image Placeholder Filler

> **此 Skill 已于 2026-01-15 废弃**
>
> **替代方案**: 使用 [Editor Skill v2.0](../editor/SKILL.md)
>
> **迁移理由**:
> - Editor v2.0 使用更高质量的 nano-banana-pro 模型
> - 采用战略性图片选择（3-5 张）而非机械填充
> - 使用 ICS Prompt 框架提升图片信息密度
> - 统一的可执行脚本 (`/scripts/fal_image_generator.py`)

---

## 原有功能说明（仅供参考）

You are an Image Generation Specialist responsible for filling image placeholders in blog articles with AI-generated images using FAL.ai.

## When to Use This Skill

- Article contains `[IMAGE: ...]` placeholders
- User requests "fill images" or "generate images"
- After blog-writer skill outputs draft with placeholders
- User wants to add visual content to article

## Placeholder Format

### Input Format (in Markdown)

```markdown
## Step 1: Choose Your Tool

[IMAGE: Screenshot of AI video tool selection interface]
<!-- alt: "AI video tool selection interface showing available options" -->
<!-- size: 1200x630 -->

The first step is...
```

### Placeholder Regex Pattern

```
\[IMAGE:\s*(.+?)\]
```

Optional metadata (HTML comments after placeholder):
- `<!-- alt: "..." -->` - Alt text for SEO
- `<!-- size: WxH -->` - Image dimensions (default: 1200x630)
- `<!-- style: ... -->` - Style modifier (modern, minimal, etc.)

## Generation Workflow

### Phase 1: Placeholder Extraction

1. Read the input Markdown file
2. Find all `[IMAGE: ...]` patterns
3. Extract metadata from HTML comments
4. Build generation queue

**Output Structure**:

```json
{
  "placeholders": [
    {
      "id": 1,
      "original": "[IMAGE: AI video generation interface]",
      "description": "AI video generation interface",
      "alt": "AI video generation interface showing prompt input and preview",
      "size": {"width": 1200, "height": 630},
      "style": "modern tech",
      "line_number": 45
    }
  ]
}
```

### Phase 2: Prompt Engineering

Transform placeholder descriptions into optimized FAL.ai prompts:

**Prompt Template**:

```
[Style Prefix] + [Description] + [Technical Suffix]
```

| Image Type | Style Prefix | Technical Suffix |
|------------|--------------|------------------|
| UI Screenshot | "Clean modern UI design," | "high resolution, professional, product screenshot" |
| Concept Art | "Digital illustration," | "vibrant colors, professional artwork" |
| Diagram | "Clean technical diagram," | "minimalist, clear lines, labeled" |
| Cover Image | "Editorial photography style," | "cinematic lighting, 8k quality" |

**Auto-Style Detection**:

| Keywords in Description | Auto Style |
|------------------------|------------|
| screenshot, interface, UI, dashboard | UI Screenshot |
| diagram, flowchart, architecture | Diagram |
| concept, illustration, art | Concept Art |
| cover, hero, featured | Cover Image |

### Phase 3: FAL.ai API Calls

**API Configuration**:

```bash
# Environment variable required
export FAL_API_KEY='your-api-key'

# Endpoint
URL: https://api.fal.ai/v1/flux/dev

# Alternative (nano-banana for faster generation)
URL: https://queue.fal.run/fal-ai/nano-banana
```

**Request Payload**:

```json
{
  "prompt": "[generated prompt]",
  "image_size": {
    "width": 1200,
    "height": 630
  },
  "num_inference_steps": 28,
  "guidance_scale": 7.5,
  "enable_safety_checker": true
}
```

**Rate Limiting**:
- Max 5 concurrent requests
- 2 second delay between requests
- Retry 3 times on failure

### Phase 4: Image Upload

**Upload to CDN**:

```bash
# Local save path
./gen_images/[article-slug]-[id].png

# Upload command
rsync -avz ./gen_images/*.png root@45.76.70.215:/var/www/static/static/image/other/gen_images/

# Final URL format
https://ct2.alici.ai/static/image/other/gen_images/[filename]
```

### Phase 5: Markdown Update

Replace placeholders with actual images:

**Before**:
```markdown
[IMAGE: AI video generation interface]
<!-- alt: "AI video generation interface" -->
```

**After**:
```markdown
![AI video generation interface](https://ct2.alici.ai/static/image/other/gen_images/ai-video-guide-1.png)
```

## Output Requirements

### Success Report

```markdown
## Image Generation Report

| # | Description | Status | URL |
|---|-------------|--------|-----|
| 1 | AI video interface | ✅ | [link] |
| 2 | Comparison chart | ✅ | [link] |
| 3 | Workflow diagram | ❌ Failed (retry 3/3) | - |

**Summary**: 2/3 images generated successfully
**API Cost**: ~$0.02
**Total Time**: 45 seconds
```

### Updated Markdown File

- Save to same location with `.filled.md` suffix
- Or overwrite original if user confirms

## Error Handling

| Error | Action |
|-------|--------|
| FAL_API_KEY not set | Prompt user to set environment variable |
| API rate limited | Wait 30s and retry |
| Generation failed | Log error, keep placeholder, mark for manual |
| Upload failed | Keep local file, provide manual upload command |
| Prompt too long | Truncate to 500 chars with warning |

## Quality Guidelines

### Image Requirements

| Aspect | Requirement |
|--------|-------------|
| Resolution | Min 1200x630 for blog images |
| Format | PNG preferred, JPEG for photos |
| File Size | < 500KB after compression |
| Alt Text | Descriptive, include keywords |

### Content Safety

- Enable safety checker by default
- Avoid: faces, celebrities, copyrighted characters
- Prefer: abstract concepts, UI elements, diagrams

## Integration with Other Skills

**Upstream**:
- `blog-tutorial-writer` → Outputs placeholders
- `blog-list-writer` → Outputs placeholders

**Downstream**:
- `framer-publisher` → Receives filled article

## Quick Start Example

**User Input**:
```
Fill images in /reports/2025-01-15-ai-video-guide/01-article-draft.md
```

**Expected Flow**:
1. Read article, find 5 placeholders
2. Generate 5 optimized prompts
3. Call FAL.ai 5 times (with rate limiting)
4. Download images to ./gen_images/
5. Upload to CDN
6. Update Markdown with real URLs
7. Save as `01-article-draft.filled.md`
8. Output generation report

## Environment Setup

```bash
# Required
export FAL_API_KEY='your-fal-api-key'

# Optional: SSH key for upload
# Ensure SSH access to root@45.76.70.215

# Test FAL.ai connection
curl -X POST https://api.fal.ai/v1/flux/dev \
  -H "Authorization: Key $FAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "test", "image_size": {"width": 256, "height": 256}}'
```

## Batch Processing

For multiple articles:

```bash
# Find all articles with placeholders
grep -l "\[IMAGE:" /reports/*/01-article-draft.md

# Process each
for file in $(grep -l "\[IMAGE:" /reports/*/01-article-draft.md); do
  echo "Processing: $file"
  # Invoke skill for each file
done
```

---

*Skill Version 1.0 - FAL.ai Integration*
