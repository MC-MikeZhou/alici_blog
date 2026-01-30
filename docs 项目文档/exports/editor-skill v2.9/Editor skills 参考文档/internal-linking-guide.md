# 内部链接指南

> **版本**: v1.0
> **基于**: Editor Skill v2.9 Module 8 + BLOG_CONTENT_REGISTRY.md + PRODUCT_CATALOG.md
> **最后更新**: 2026-01-23
> **文档用途**: 内部链接策略和 Pillar-Cluster 架构参考

---

## 核心目标

建立基于 **Pillar-Cluster** 架构的内容网络，实现：

1. **SEO 权重传递**: Cluster 文章向 Pillar 页传递链接权重
2. **用户导航**: 引导读者发现相关内容
3. **转化路径**: 最终引导用户到 alici.ai 产品页

---

## Pillar-Cluster 架构说明

### 什么是 Pillar-Cluster？

```
                    ┌─────────────────┐
                    │   Pillar Page   │  ← 核心支柱页 (如 AI Video Guide)
                    │  (全面指南)      │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ Cluster       │   │ Cluster       │   │ Cluster       │
│ Article 1     │   │ Article 2     │   │ Article 3     │
│ (工具对比)     │◄──►│ (教程)        │◄──►│ (新闻)        │
└───────┬───────┘   └───────┬───────┘   └───────┬───────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ Product Page  │  ← 转化目标页
                    │ (alici.ai)    │
                    └───────────────┘
```

### 架构层级

| 层级 | 类型 | 内容特点 | 链接策略 |
|------|------|----------|----------|
| **Pillar** | 支柱页 | 3000-5000 词全面指南 | 接收所有 Cluster 链接 |
| **Cluster** | 集群文章 | 1500-3000 词专题内容 | 链接到 Pillar + 相关 Cluster |
| **Product** | 产品页 | 转化目标 | 接收文章 CTA 链接 |

---

## 链接类型与数量规范

### 链接方向规则

| 链接方向 | 数量 | 位置 | 锚文本要求 |
|----------|------|------|-----------|
| **Cluster → Pillar** | 1-2 | 导言或结论 | 描述性，3-5 词 |
| **Cluster ↔ Cluster** | 2-3 | 相关章节内 | 自然融入正文 |
| **Article → Product** | 1-2 | CTA 位置 | 行动导向 |

### 总链接数目标

- **每篇文章**: 3-6 个内部链接
- **最低要求**: 1 Pillar + 1 Product
- **最高限制**: 不超过 8 个（避免过度链接）

---

## 锚文本规范

### 基本规则

- **长度**: 3-5 词
- **风格**: 描述性，告诉读者链接目标
- **自然**: 融入正文，不堆砌

### 正确示例 ✅

| 链接类型 | 锚文本示例 |
|----------|-----------|
| Pillar | "complete guide to AI video generation" |
| Pillar | "comprehensive AI video tutorial" |
| Cluster | "best AI video generators for 2026" |
| Cluster | "Motion Control tutorial" |
| Cluster | "master Sora 2 prompting" |
| Product | "Try AI Video Studio free" |
| Product | "create your first AI video" |

### 错误示例 ❌

以下锚文本应**避免使用**：

- "click here"
- "read more"
- "this article"
- "here"
- "link"
- 单个词锚文本

---

## 当前内容索引

### Pillar Pages（支柱页）

| ID | 标题 | URL | Cluster | 状态 |
|----|------|-----|---------|------|
| pillar-001 | Complete Guide to AI Video Generation | /blog/ai-video-guide | AI Video | Draft |
| pillar-002 | Complete Guide to AI Image Generation | /blog/ai-image-guide | AI Image | Draft |

### AI Video Cluster

| ID | 标题 | URL | 类型 | 状态 |
|----|------|-----|------|------|
| video-001 | 10 Best AI Video Generators in 2025 | /blog/best-ai-video-generators-2025 | List | Draft |
| video-002 | How to Make AI Videos in 5 Minutes | /blog/how-to-make-ai-videos | Tutorial | Draft |
| video-003 | Sora 2 Prompt Guide | /blog/sora-2-prompt-guide-cinematic-ai-videos-2026 | Tutorial | Draft |
| video-004 | Kling 2.6 Motion Control Tutorial | /blog/kling-2-6-motion-control-tutorial-2026 | Tutorial | **Published** |
| video-005 | Nano Banana + Motion Control | /blog/nano-banana-motion-control-2026-01 | Roundup | Draft |
| video-006 | Kling 2.6 is Here | /blog/kling-2-6-is-here | News | **Published** |

### AI Image Cluster

| ID | 标题 | URL | 类型 | 状态 |
|----|------|-----|------|------|
| image-001 | Best AI Image Generators 2026 | /blog/best-ai-image-generators-2026 | List | Planned |
| image-002 | Nano Banana Pro Guide | /blog/nano-banana-guide | Tutorial | Planned |

### Product Landing Pages

| 产品 | URL | Cluster | CTA 上下文 |
|------|-----|---------|------------|
| AI Video Studio | https://alici.ai/pages/videoGen | AI Video | "Try all models free" |
| AI Image Studio | https://alici.ai/pages/imageGen | AI Image | "Generate your first image" |
| alici.ai Homepage | https://alici.ai | All | "Get started with alici.ai" |

---

## 产品链接参数规则 (v2.9.3)

### 基础 URL

```yaml
videoGen: "https://app.alici.ai/pages/videoGen"
imageGen: "https://app.alici.ai/pages/imageGen"
home: "https://alici.ai"
```

### 上下文参数映射

根据文章关键词自动添加参数，让用户跳转后直接看到相关模型：

| 文章关键词 | 产品 | 添加参数 | 说明 |
|-----------|------|---------|------|
| kling, motion control | videoGen | `?model=kling_2_6_s_mc` | Kling 2.6 Motion Control |
| sora, sora 2 | videoGen | `?model=sora_2` | Sora 2 预设 |
| runway, gen-3, gen-4 | videoGen | `?model=runway_gen3` | Runway 预设 |
| veo, veo 2, veo 3 | videoGen | `?model=veo_2` | Google Veo 预设 |
| pika, pika labs | videoGen | `?model=pika_2` | Pika Labs 预设 |
| minimax, hailuo | videoGen | `?model=minimax` | MiniMax 预设 |
| (默认) | videoGen | (无参数) | 用户自选 |
| (所有) | imageGen | (无参数) | 无预设 |

### 参数应用示例

**文章标题**: "How to Create Viral Videos with Kling 2.6 Motion Control"

**检测到关键词**: "kling", "motion control"

**CTA 链接**:
```markdown
[Try Motion Control Free →](https://app.alici.ai/pages/videoGen?model=kling_2_6_s_mc)
```

---

## 内部链接示例表格

### Kling Motion Control 文章链接配置

假设文章: `/blog/kling-2-6-motion-control-tutorial-2026`

| # | 类型 | 目标 | 锚文本 | 位置 |
|---|------|------|--------|------|
| 1 | Pillar | /blog/ai-video-guide | complete AI video generation guide | Introduction |
| 2 | Cluster | /blog/best-ai-video-generators-2025 | compare the best AI video tools | Comparison Section |
| 3 | Cluster | /blog/sora-2-prompt-guide-cinematic-ai-videos-2026 | master Sora 2 prompting | Pro Tips Section |
| 4 | Product | /pages/videoGen?model=kling_2_6_s_mc | Try Motion Control free | Quick Start |
| 5 | Product | /pages/videoGen?model=kling_2_6_s_mc | create your first video | Conclusion CTA |

### 链接插入位置指南

| 位置类型 | 适合链接 | 识别方法 |
|----------|----------|----------|
| **导言** (前 200 词) | Pillar 链接 | 文章开头段落 |
| **Quick Start/TL;DR** | 产品链接 | `> **Quick` 或 `> **In a hurry` |
| **相关章节** | Cluster 链接 | H2/H3 标题含匹配 keywords |
| **结论** | Pillar + 产品链接 | `## Conclusion` 或最后一个 H2 |
| **CTA Section** | 产品链接 | `[Try` 开头的链接文本 |

---

## BLOG_CONTENT_REGISTRY.md 维护指南

### 文件位置

```
/.claude/skills/_shared/BLOG_CONTENT_REGISTRY.md
```

### 如何添加新内容

1. **发布后更新**: 文章发布后，添加到对应 Cluster 表格
2. **分配 ID**: `{cluster}-{number}`（如 video-007）
3. **填写字段**:
   - Title: 文章标题
   - URL: 相对路径（/blog/slug）
   - Type: List / Tutorial / News / Roundup / Guide
   - Pillar: 关联的 Pillar ID
   - Status: Draft → Published
   - Keywords: 主要关键词（用于匹配）

### 状态定义

| 状态 | 含义 |
|------|------|
| Planned | 计划中，尚未开始写作 |
| Draft | 草稿已完成，未发布 |
| Published | 已发布到 alici.ai/blog |
| Updated | 已发布且近期更新过 |

### 更新频率

- **新文章发布时**: 立即更新
- **Pillar 页发布时**: 立即更新并调整关联
- **定期审核**: 每月检查链接有效性

---

## 不添加链接的情况

以下情况**跳过**内部链接添加：

| 情况 | 原因 | 处理 |
|------|------|------|
| 文章 < 500 词 | 内容太短，链接会显得突兀 | 仅添加 1 个产品 CTA |
| 无匹配 Cluster | 无法确定关联内容 | 仅添加 1 个产品 CTA |
| Registry 为空/不可用 | 无参考数据 | 跳过 Module 8，记录 WARNING |
| 已有 ≥5 个内部链接 | 避免过度链接 | 检查现有链接，优化锚文本 |

---

## Editor Report 输出格式

`04-editor-report.md` 中的 Module 8 章节：

```markdown
## Module 8: Internal Linking

**Registry Version**: 2026-01-21
**Article Cluster**: AI Video
**Links Added**: 5

### Link Inventory

| # | Type | Target | Anchor Text | Position | Status |
|---|------|--------|-------------|----------|--------|
| 1 | Pillar | /blog/ai-video-guide | complete AI video generation guide | Introduction | ✅ Added |
| 2 | Cluster | /blog/kling-2-6-motion-control-tutorial-2026 | Motion Control tutorial | Pro Tips Section | ✅ Added |
| 3 | Cluster | /blog/best-ai-video-generators-2025 | top AI video tools | Comparison Section | ✅ Added |
| 4 | Product | /pages/videoGen?model=kling_2_6_s_mc | Try AI Video Studio | Quick Start | ✅ Added |
| 5 | Product | /pages/videoGen?model=kling_2_6_s_mc | create your first video | Conclusion CTA | ✅ Added |

### Link Parameter Application

| Link Type | Base URL | Applied Params | Final URL |
|-----------|----------|----------------|-----------|
| videoGen CTA | app.alici.ai/pages/videoGen | ?model=kling_2_6_s_mc | ✅ |
| imageGen mention | app.alici.ai/pages/imageGen | (none) | ✅ |

**Context Match**: "kling" keyword detected → applied kling_2_6_s_mc model

### Validation

| Check | Status |
|-------|--------|
| Anchor text 3-5 words | ✅ PASS |
| Natural integration | ✅ PASS |
| No duplicate targets | ✅ PASS |
| Link count 3-6 | ✅ PASS (5 links) |

**Module 8 Status**: ✅ PASS
```

---

## Cluster 关键词映射

用于自动匹配文章所属 Cluster：

| Cluster | 关键词 |
|---------|--------|
| AI Video | video, sora, kling, runway, veo, motion control, video generation |
| AI Image | image, flux, ideogram, midjourney, dalle, nano banana, image generation |
| Marketing | marketing, seo, content, social media, automation |

### 匹配优先级

1. 从 YAML frontmatter 的 `category` 字段匹配
2. 从 `tags` 字段匹配关键词
3. 从标题和 H1/H2 提取关键词
4. 无匹配时默认为 "AI Video" Cluster

---

## 错误处理

| 错误 | 处理 |
|------|------|
| BLOG_CONTENT_REGISTRY.md 不存在 | ⚠️ WARNING - 跳过 Module 8，继续其他模块 |
| Registry 解析失败 | ⚠️ WARNING - 记录错误，跳过 Module 8 |
| 无匹配内容 | ⚠️ WARNING - 仅添加产品 CTA |
| 链接插入失败 | 记录失败原因，继续下一个链接 |

---

## 相关文档

- [Editor v2.9 能力总览](./editor-v2.9-capabilities.md)
- [E-E-A-T 强化指南](./eeat-optimization-guide.md)
- [版本管理标准](./content-version-standard.md)
- Registry 文件: `/.claude/skills/_shared/BLOG_CONTENT_REGISTRY.md`
- 产品目录: `/.claude/skills/_shared/PRODUCT_CATALOG.md`
- 链接参数规则: `/.claude/skills/_shared/editor/prompts/link-parameter-rules.yaml`

---

*文档维护: Editor Skill v2.9.3 | 最后同步: 2026-01-23*
