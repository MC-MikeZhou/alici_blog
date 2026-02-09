# alici.ai 产品目录

> 用于 Blog Writer Skills 的产品关联和动态 CTA 生成

---

## 产品分类

### 1. AI 视频工具

| 产品名称 | 产品 ID | 功能描述 | URL 路径 | 支持的模型 |
|---------|---------|----------|----------|------------|
| **AI Video Studio** | `video_studio` | 一站式 AI 视频生成平台 | `/pages/videoGen` | Kling 2.0, Runway Gen-4, Veo 3 |
| **Any Script 2 AI Video** | `script_to_video` | 文字脚本一键转病毒视频 | `/chat?agent_id=alici_anyscript2video_zo7ayx` | - |
| **Image to AI Video** | `image_to_video` | 静态图片转动态视频 | `/chat?agent_id=alici_video_prompt` | - |
| **Viral Video Cloner** | `viral_cloner` | 复刻热门视频成功模式 | `/chat?agent_id=alici_hitclone_lab_p_n8959hb` | - |
| **Video Prompt Assistant** | `video_prompt` | 优化视频生成提示词 | `/chat?agent_id=alici_video_prompt` | - |

### 2. AI 图像工具

| 产品名称 | 产品 ID | 功能描述 | URL 路径 | 支持的模型 |
|---------|---------|----------|----------|------------|
| **AI Image Studio** | `image_studio` | 一站式 AI 图像生成平台 | `/pages/imageGen` | Flux, Ideogram, Imagen 4 |
| **Smart Image Editor** | `smart_editor` | 自然语言指令编辑图片 | `/chat?agent_id=alici_image_editor_v2_fjpad3j` | - |
| **Image Prompt Assistant** | `image_prompt` | 生成完美图像提示词 | `/chat?agent_id=alici_image_generator` | - |
| **Image Resizer** | `resizer` | 一键调整多平台尺寸 | `/chat?agent_id=alici_resize_finfj4l` | - |
| **Image Upscaler** | `upscaler` | 图像高清放大增强 | `/chat?agent_id=alici_upscale_jof1n4` | - |
| **SwapFace** | `swap_face` | AI 人脸替换 | `/chat?agent_id=alici_swap_face_nd3oid` | - |

### 3. 专业创意工具

| 产品名称 | 产品 ID | 功能描述 | URL 路径 |
|---------|---------|----------|----------|
| **Thumbnail Expert Pro** | `thumbnail_pro` | 高点击率 YouTube 缩略图生成 | `/chat?agent_id=alici_thumbnail_pro_fn38b2o` |

### 4. 通用入口

| 入口名称 | 用途 | URL 路径 |
|---------|------|----------|
| **主应用** | 默认 CTA | `/` |
| **注册页** | 用户注册 | `/pages/signIn` |
| **Chat 中心** | AI Agent 对话 | `/pages/chat` |

---

## 关键词-产品映射表

用于根据文章主题自动匹配最相关的产品。

### 视频相关

| 关键词模式 | 主要产品 | 辅助产品 | CTA 文案 |
|-----------|---------|---------|---------|
| `AI video`, `create video`, `generate video` | video_studio | video_prompt | "Create AI Videos Now" |
| `Sora`, `Sora 2`, `OpenAI video` | video_studio | video_prompt | "Try Sora Alternatives" |
| `Kling`, `Kling 2.0`, `Kuaishou` | video_studio | - | "Access Kling 2.0" |
| `Runway`, `Gen-4`, `Gen-3` | video_studio | - | "Try Runway in alici.ai" |
| `Veo`, `Veo 3`, `Google video` | video_studio | - | "Access Google Veo 3" |
| `viral video`, `trending video`, `clone` | viral_cloner | video_studio | "Clone Viral Videos" |
| `script to video`, `text to video` | script_to_video | video_prompt | "Turn Script into Video" |
| `image to video`, `animate image` | image_to_video | - | "Animate Your Images" |
| `video prompt`, `prompt engineering` | video_prompt | video_studio | "Optimize Video Prompts" |

### 图像相关

| 关键词模式 | 主要产品 | 辅助产品 | CTA 文案 |
|-----------|---------|---------|---------|
| `AI image`, `generate image`, `create image` | image_studio | image_prompt | "Generate AI Images" |
| `Flux`, `Flux Dev`, `Flux Pro` | image_studio | - | "Access Flux Models" |
| `Ideogram`, `text in image` | image_studio | - | "Try Ideogram" |
| `Imagen`, `Google image` | image_studio | - | "Access Google Imagen 4" |
| `upscale`, `enhance`, `high resolution`, `HD` | upscaler | - | "Upscale Images Free" |
| `resize`, `social media size`, `aspect ratio` | resizer | - | "Resize for All Platforms" |
| `edit image`, `remove background`, `change` | smart_editor | - | "Edit with AI Commands" |
| `face swap`, `replace face` | swap_face | - | "Try AI Face Swap" |
| `image prompt`, `prompt for image` | image_prompt | image_studio | "Generate Perfect Prompts" |

### YouTube / 创作者相关

| 关键词模式 | 主要产品 | 辅助产品 | CTA 文案 |
|-----------|---------|---------|---------|
| `thumbnail`, `YouTube thumbnail`, `CTR` | thumbnail_pro | image_studio | "Create Click-Worthy Thumbnails" |
| `YouTube`, `content creator`, `viral` | thumbnail_pro, viral_cloner | - | "Boost Your YouTube Game" |

### 通用

| 关键词模式 | 主要产品 | CTA 文案 |
|-----------|---------|---------|
| `AI tools`, `best AI`, `AI platform` | (default) | "Explore alici.ai" |
| `free AI`, `free tools` | (default) | "Start Free" |

---

## CTA 模板库

### 1. Opening CTA (开篇后使用)

```markdown
> 💡 **Quick Start**: [Product Name] lets you [key benefit] in minutes. [Try it free →](URL)
```

### 2. Mid-Article CTA (步骤/列表中间)

```markdown
> **Pro Tip**: Use alici.ai's [Product Name](URL) to [specific benefit]. Users report [specific metric] improvement.
```

### 3. Closing CTA (结论部分)

**标准版**:
```markdown
Ready to [achieve goal]? alici.ai's [Product Name] gives you [key features].

**[CTA Text →](URL)**
```

**强化版**:
```markdown
## Start Creating Today

alici.ai brings together [Product 1], [Product 2], and [Product 3] in one platform—no switching between tools.

🚀 **[CTA Text →](URL)** | Free tier available
```

### 4. In-List CTA (List 文章中某项使用)

```markdown
## 1. alici.ai [Product Name]

**Why it stands out**: [Unique value proposition]

**Best for**: [Target user]

**Try it**: [CTA Text →](URL)
```

---

## 产品特性标签

用于在文章中自然植入产品特性。

### AI Video Studio
- 支持模型: Kling 2.0, Runway Gen-4, Google Veo 3
- 核心优势: 多模型一站式、无需切换工具
- 定价提及: "Free tier available"
- 使用场景: 病毒视频、营销视频、内容创作

### AI Image Studio
- 支持模型: Flux, Ideogram, Imagen 4
- 核心优势: 多风格选择、高质量输出
- 定价提及: "Start free"
- 使用场景: 社交媒体图片、营销素材、艺术创作

### Thumbnail Expert Pro
- 核心优势: 高 CTR 设计、YouTube 优化
- 定价提及: "Free trial"
- 使用场景: YouTube 创作者、内容营销

### Viral Video Cloner
- 核心优势: 一键复刻热门视频模式
- 使用场景: 趋势跟随、快速内容生产

### Image Upscaler
- 核心优势: 最高 4x 放大、保持细节
- 使用场景: 打印输出、高清需求

---

## 使用指南

### 在 Blog Writer 中使用

1. **选题阶段**: growth-topic-scout 根据关键词自动匹配 `product_mapping`

2. **写作阶段**: blog-tutorial-writer / blog-list-writer 根据 `product_mapping` 生成动态 CTA

3. **CTA 位置规则**:
   - Tutorial: 开篇 1 次 + 中间 1-2 次 (Pro Tip) + 结论 1 次
   - List: 首项后 1 次 + 中间 1 次 + How to Choose 1 次 + 结论 1 次
   - News: 每 300-400 词 1 次 (最密集)

### Topic Brief 中的 product_mapping 格式

```json
{
  "product_mapping": {
    "primary_product": {
      "id": "video_studio",
      "name": "AI Video Studio",
      "url": "https://app.alici.ai/pages/videoGen",
      "cta_text": "Create AI Videos Now",
      "features": ["Kling 2.0", "Runway Gen-4", "Veo 3"]
    },
    "secondary_products": [
      {
        "id": "video_prompt",
        "name": "Video Prompt Assistant",
        "url": "https://app.alici.ai/chat?agent_id=alici_video_prompt",
        "use_case": "优化提示词获得更好效果"
      }
    ],
    "cta_templates": {
      "opening": "💡 **Quick Start**: AI Video Studio lets you create professional videos in minutes. [Try it free →](URL)",
      "mid": "> **Pro Tip**: Use alici.ai's Video Prompt Assistant to optimize your prompts.",
      "closing": "Ready to create viral AI videos? **[Create AI Videos Now →](URL)**"
    }
  }
}
```

---

## 更新记录

| 日期 | 更新内容 |
|------|----------|
| 2025-01-14 | 初始版本：12 个产品 + 关键词映射 + CTA 模板 |
