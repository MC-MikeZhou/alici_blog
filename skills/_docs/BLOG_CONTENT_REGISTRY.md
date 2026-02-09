# Alici Blog Content Registry

> **Version**: 1.0.0
> **Last Updated**: 2026-01-21
> **Purpose**: 维护所有已发布博客内容的索引，供 Editor Skill v2.7+ 进行内部链接匹配

---

## Pillar Pages (支柱页)

核心支柱页是每个 Cluster 的主入口，需要获得最多的内部链接。

| ID | Title | URL | Cluster | Status | Keywords |
|----|-------|-----|---------|--------|----------|
| pillar-001 | Complete Guide to AI Video Generation | /blog/ai-video-guide | AI Video | Draft | AI video, video generation, Sora, Kling, Runway, Veo |
| pillar-002 | Complete Guide to AI Image Generation | /blog/ai-image-guide | AI Image | Draft | AI image, image generation, Flux, Ideogram, Midjourney |

---

## Cluster Articles (集群文章)

### AI Video Cluster

| ID | Title | URL/Slug | Type | Pillar | Status | Keywords |
|----|-------|----------|------|--------|--------|----------|
| video-001 | 10 Best AI Video Generators in 2025: Tested & Compared | /blog/best-ai-video-generators-2025 | List | pillar-001 | Draft | AI video generator, best ai tools, Veo 3, Kling, Runway, video comparison |
| video-002 | How to Make AI Videos in 5 Minutes: A Complete Beginner's Guide | /blog/how-to-make-ai-videos | Tutorial | pillar-001 | Draft | AI video, video generation, how to, tutorial, beginner guide |
| video-003 | Sora 2 Prompt Guide: How to Create Cinematic AI Videos in 2026 | /blog/sora-2-prompt-guide-cinematic-ai-videos-2026 | Tutorial | pillar-001 | Draft | Sora 2, prompt engineering, cinematic AI, OpenAI Sora |
| video-004 | How to Create Viral Videos with Kling 2.6 Motion Control | /blog/kling-2-6-motion-control-tutorial-2026 | Tutorial | pillar-001 | Published | Kling motion control, motion transfer, dance videos, AI video generation |
| video-005 | Nano Banana + Motion Control: 病毒视频创作新范式 | /blog/nano-banana-motion-control-2026-01 | Roundup | pillar-001 | Draft | motion control, Kling 2.6, Nano Banana Pro, video generation |
| video-006 | Kling 2.6 is Here | /blog/kling-2-6-is-here | News | pillar-001 | **Published** | Kling 2.6, motion control, AI video news |
| video-007 | How to Write Sora 2 Prompts for Beginners (2026): Templates + Checklist + Fixes | /blog/sora-2-prompt-guide-beginners-templates-2026 | Tutorial | pillar-001 | Draft | Sora 2, prompt guide, prompt templates, prompt checklist, beginner, AI video prompts |

### AI Image Cluster

| ID | Title | URL/Slug | Type | Pillar | Status | Keywords |
|----|-------|----------|------|--------|--------|----------|
| image-001 | Best AI Image Generators 2026 | /blog/best-ai-image-generators-2026 | List | pillar-002 | Planned | image generators, Flux, Ideogram, AI art |
| image-002 | Nano Banana Pro: Advanced AI Image Generation | /blog/nano-banana-pro-guide | Tutorial | pillar-002 | Planned | Nano Banana Pro, AI image, character generation |

### Marketing Cluster

| ID | Title | URL/Slug | Type | Pillar | Status | Keywords |
|----|-------|----------|------|--------|--------|----------|
| mkt-001 | Best AI Marketing Tools 2026 | /blog/best-ai-marketing-tools-2026 | List | N/A | Draft | AI marketing, marketing automation, AI tools |

---

## Product Landing Pages (产品页)

这些是转化目标页，文章的 CTA 应指向这里。

| Product | URL | Cluster | Keywords | CTA Context |
|---------|-----|---------|----------|-------------|
| AI Video Studio | https://alici.ai/pages/videoGen | AI Video | video, Sora, Kling, Veo, Runway, Pika | "Try all models free", "Create your first video" |
| AI Image Studio | https://alici.ai/pages/imageGen | AI Image | image, Flux, Ideogram, Imagen, Nano Banana | "Generate your first image", "Try AI Image Studio" |
| alici.ai Homepage | https://alici.ai | All | AI platform, one-stop AI | "Get started with alici.ai" |

---

## Linking Rules (链接规则)

### 1. Cluster → Pillar 链接
每篇 Cluster 文章必须包含 **1-2 个** 指向其 Pillar 页的链接：
- **位置**: 导言或结论
- **锚文本**: 描述性，3-5 词（如 "complete AI video generation guide"）

### 2. Cluster ↔ Cluster 链接
同一 Cluster 内的文章互相链接 **2-3 个**：
- **位置**: 相关章节内自然融入
- **锚文本**: 与目标文章内容相关

### 3. Article → Product 链接
每篇文章包含 **1-2 个** 产品页链接：
- **位置**: CTA 位置（开头 Quick Start、结尾 Call to Action）
- **锚文本**: 行动导向（"try X free", "create your first Y"）

---

## URL Resolution Table (URL 解析表)

便于 Editor Skill 快速查找完整 URL：

| Short Reference | Full URL |
|-----------------|----------|
| /blog/ai-video-guide | https://alici.ai/blog/ai-video-guide |
| /blog/best-ai-video-generators-2025 | https://alici.ai/blog/best-ai-video-generators-2025 |
| /blog/how-to-make-ai-videos | https://alici.ai/blog/how-to-make-ai-videos |
| /blog/sora-2-prompt-guide-cinematic-ai-videos-2026 | https://alici.ai/blog/sora-2-prompt-guide-cinematic-ai-videos-2026 |
| /blog/kling-2-6-motion-control-tutorial-2026 | https://alici.ai/blog/kling-2-6-motion-control-tutorial-2026 |
| /blog/kling-2-6-is-here | https://alici.ai/blog/kling-2-6-is-here |
| /blog/nano-banana-motion-control-2026-01 | https://alici.ai/blog/nano-banana-motion-control-2026-01 |
| /pages/videoGen | https://alici.ai/pages/videoGen |
| /pages/imageGen | https://alici.ai/pages/imageGen |

---

## Anchor Text Examples (锚文本示例)

### Pillar Links
| Target | Good Anchor Text | Bad Anchor Text |
|--------|------------------|-----------------|
| AI Video Guide | "complete guide to AI video generation" | "click here" |
| AI Video Guide | "our comprehensive AI video tutorial" | "read more" |
| AI Image Guide | "full AI image generation guide" | "this article" |

### Cluster Links
| Target | Good Anchor Text | Bad Anchor Text |
|--------|------------------|-----------------|
| Best AI Video Generators | "compare the best AI video tools" | "here" |
| Kling Motion Control | "Motion Control tutorial" | "link" |
| Sora 2 Prompt Guide | "master Sora 2 prompting" | "see" |

### Product Links
| Target | Good Anchor Text | Bad Anchor Text |
|--------|------------------|-----------------|
| Video Studio | "Try AI Video Studio free" | "click" |
| Video Studio | "create videos with all top AI models" | "start" |
| Image Studio | "Generate your first AI image" | "here" |

---

## Maintenance Notes

### How to Add New Content

1. **新文章发布后**，添加到对应 Cluster 表格
2. **分配 ID**：`{cluster}-{number}` (如 video-007)
3. **标记 Status**：Draft → Published（发布后更新）
4. **更新 Keywords**：包含主要关键词供匹配

### Status Definitions

| Status | Meaning |
|--------|---------|
| Planned | 计划中，尚未开始写作 |
| Draft | 草稿已完成，未发布 |
| Published | 已发布到 alici.ai/blog |
| Updated | 已发布且近期更新过 |

---

*Registry maintained by Editor Skill v2.7+. Last sync: 2026-01-21*
