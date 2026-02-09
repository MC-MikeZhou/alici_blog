# Alici AI Tools — Product Requirements Document (PRD)

> Version: 1.0
> Author: Dancy (PM)
> Date: 2026-02-08
> Status: Draft — Pending Hans Review
> Basecamp: [原始任务](https://3.basecamp.com/3135399/buckets/42744895/messages/9491566573)

---

## 1. Executive Summary

### 1.1 What

在 `alici.ai/tools` 子目录下搭建一个免费在线工具集网站。用户可以在**不登录**的情况下使用 YouTube 缩略图下载、视频转 GIF、视频压缩等工具。所有处理在用户浏览器端完成，**API 成本 = $0**。

### 1.2 Why

- **SEO 增长引擎**：5 个工具覆盖 ~140K/mo 搜索量，为 alici.ai 带来自然流量
- **品牌认知入口**：用户通过免费工具认识 alici.ai → 转化为 AI Video/Image Studio 用户
- **竞品已验证**：toolkit.video、123apps、Clideo 等验证了"免费工具 → 用户增长"模式
- **零边际成本**：全部浏览器端处理，无服务器费用

### 1.3 Success Metrics

| 指标 | 目标 (上线 3 个月内) |
|------|---------------------|
| 月自然搜索流量 | ≥ 5,000 UV |
| Google 索引页面数 | 5 个工具页 + 1 首页 = 6 页 |
| 关键词排名 (Top 20) | ≥ 3 个关键词 |
| CTA 点击率 | ≥ 2% (工具页 → alici.ai 主产品) |
| 用户停留时长 | ≥ 2 分钟 (工具使用时间) |

---

## 2. Product Positioning

### 2.1 定位语

**Alici AI Tools** — Free, private, browser-based tools for creators. No login. No upload. No limits.

### 2.2 与 alici.ai 主产品的关系

```
alici.ai/tools (免费工具集)                    app.alici.ai (主产品)
┌─────────────────────────────┐               ┌─────────────────────────────┐
│  YouTube Thumbnail Download │               │  AI Video Studio            │
│  Video to GIF               │  ── CTA ──>   │  AI Image Studio            │
│  WebM to MP4                │               │  Thumbnail Expert Pro       │
│  Watermark Remover          │               │  Smart Image Editor         │
│  Video Compressor           │               │  Image Upscaler             │
└─────────────────────────────┘               └─────────────────────────────┘
    流量入口 (SEO)                                 付费转化 (SaaS)
    零成本                                         营收来源
```

### 2.3 目标用户

| 用户画像 | 需求 | 转化路径 |
|---------|------|---------|
| YouTube 创作者 | 下载视频缩略图做参考/分析 | → Thumbnail Expert Pro |
| 内容营销人员 | 视频转 GIF 做社交素材 | → AI Video Studio |
| 独立创作者 | 压缩视频/转换格式发布 | → AI Video Studio |
| AI 图片用户 | 移除 Gemini 水印 | → AI Image Studio |

---

## 3. MVP Tool Specifications (Phase 1)

### 3.1 YouTube Thumbnail Downloader

**搜索量**：14,800/mo (合计 ~29,280/mo 含长尾)
**竞争度**：KD 40 (中等)
**CPC**：$0.00

**功能描述**：
- 用户粘贴 YouTube 视频 URL
- 自动解析 Video ID（支持 watch、youtu.be、shorts、embed 格式）
- 展示所有可用分辨率的缩略图预览
- 一键下载指定分辨率的缩略图

**支持的 URL 格式**：
```
https://www.youtube.com/watch?v=VIDEO_ID
https://youtu.be/VIDEO_ID
https://www.youtube.com/shorts/VIDEO_ID
https://www.youtube.com/embed/VIDEO_ID
```

**缩略图分辨率**：
| 名称 | URL 模式 | 尺寸 | 可用性 |
|------|---------|------|--------|
| Max Resolution | `maxresdefault.jpg` | 1280×720 | 不一定存在 |
| Standard | `sddefault.jpg` | 640×480 | 总是存在 |
| High Quality | `hqdefault.jpg` | 480×360 | 总是存在 |
| Medium Quality | `mqdefault.jpg` | 320×180 | 总是存在 |
| Default | `default.jpg` | 120×90 | 总是存在 |

**技术实现**：
1. 正则表达式提取 Video ID
2. 拼接 `https://img.youtube.com/vi/{VIDEO_ID}/{quality}.jpg`
3. 前端 `<img>` 标签预览（利用 YouTube 公开 CDN）
4. 下载按钮：`fetch()` → `blob` → `URL.createObjectURL()` → `<a download>`
5. 需要 Vercel Serverless Function 做 proxy 解决跨域 CORS 限制

**注意事项**：
- `maxresdefault.jpg` 不是所有视频都有（旧视频/低质量视频没有），需要 fallback 检测
- YouTube oEmbed API (`https://www.youtube.com/oembed?url=...&format=json`) 可获取视频标题用于下载文件名
- 下载按钮需要通过后端 proxy 避免 CORS 问题

**页面 SEO 内容**：
- Title: "YouTube Thumbnail Downloader — Download HD Thumbnails Free | Alici AI Tools"
- H1: "YouTube Thumbnail Downloader"
- How It Works (4 steps): Paste URL → Preview → Select Resolution → Download
- Use Cases: 竞品分析、缩略图设计参考、社交分享、内容存档
- FAQ (6 questions):
  1. Is it free? → Yes, completely free, no login required
  2. What resolutions are available? → Up to 1280×720 (Max Resolution)
  3. Is it legal? → Thumbnails are publicly accessible via YouTube
  4. Do I need to install anything? → No, works directly in browser
  5. Can I download Shorts thumbnails? → Yes, paste the Shorts URL
  6. Why is Max Resolution not available? → Not all videos have 1280×720 thumbnails

---

### 3.2 Video to GIF Maker

**搜索量**：90,500/mo
**竞争度**：KD 40 (中等)
**CPC**：$0.19

**功能描述**：
- 用户上传视频文件（拖拽或选择）
- 预览视频，选择起止时间
- 设置输出参数：帧率、宽度、质量
- 一键转换为 GIF 并下载

**支持的输入格式**：MP4, WebM, MOV, AVI, MKV

**输出参数**：
| 参数 | 默认值 | 可选范围 |
|------|--------|---------|
| 帧率 (FPS) | 10 | 5, 10, 15, 20, 25 |
| 宽度 (px) | 480 | 240, 320, 480, 640, 原始 |
| 质量 | High | Low, Medium, High |
| 时长上限 | 15s | 无硬性限制(取决于设备性能) |

**技术实现**：
```
FFmpeg WASM 命令:
ffmpeg -i input -vf "fps={fps},scale={width}:-1:flags=lanczos" -t {duration} output.gif
```

**交互流程**：
1. 拖拽/选择视频文件
2. 视频预览 + 时间轴滑块选择起止时间
3. 参数面板（FPS / 宽度 / 质量）
4. "Convert to GIF" 按钮
5. 进度条显示转换进度
6. 预览 GIF + 下载按钮

---

### 3.3 WebM to MP4 Converter

**搜索量**：22,200/mo
**竞争度**：KD 10 (极低 — 最容易排名)
**CPC**：$0.16

**功能描述**：
- 用户上传 WebM 文件
- 一键转换为 MP4 (H.264)
- 下载 MP4 文件

**技术实现**：
```
FFmpeg WASM 命令:
ffmpeg -i input.webm -c:v libx264 -crf 23 -preset medium -c:a aac output.mp4
```

**交互流程**：
1. 拖拽/选择 WebM 文件
2. 显示文件信息（大小、时长、分辨率）
3. "Convert to MP4" 按钮
4. 进度条
5. 下载按钮

---

### 3.4 Nano Banana Watermark Remover

**搜索量**：长尾流量（"gemini watermark remover" 等）
**竞争度**：极低（几乎无竞品）

**功能描述**：
- 用户上传 Gemini AI 生成的图片
- 自动检测并移除 SynthID / Nano Banana 水印
- 下载无水印版本

**技术实现**：
- 使用反向 alpha 混合算法（Canvas API）
- 基于开源项目 [Gemini Watermark Remover](https://github.com/journey-ad/gemini-watermark-remover)
- 100% 浏览器端处理

**限制说明（页面明确标注）**：
- 仅适用于 **未经编辑** 的 Gemini AI 生成图片
- 如果图片被裁剪、缩放、重新保存过，将无法正确移除
- 声明仅供教育/研究目的

**交互流程**：
1. 拖拽/选择 PNG 图片
2. 预览原图 + 处理后对比
3. "Remove Watermark" 按钮
4. Before/After 对比展示
5. 下载按钮

---

### 3.5 Video Compressor

**搜索量**：12,100/mo
**竞争度**：KD 41 (中等)
**CPC**：$0.57

**功能描述**：
- 用户上传视频文件
- 选择压缩级别（Light / Medium / Heavy）
- 实时预估压缩后文件大小
- 压缩并下载

**压缩级别**：
| 级别 | CRF 值 | 预估压缩率 | 质量 |
|------|--------|-----------|------|
| Light | 23 | 30-40% 缩小 | 几乎无损 |
| Medium | 28 | 50-60% 缩小 | 轻微损失 |
| Heavy | 33 | 70-80% 缩小 | 明显损失 |

**技术实现**：
```
FFmpeg WASM 命令:
ffmpeg -i input -c:v libx264 -crf {crf} -preset medium -c:a aac -b:a 128k output.mp4
```

**交互流程**：
1. 拖拽/选择视频文件
2. 显示原始文件信息
3. 压缩级别滑块（Light / Medium / Heavy）
4. 实时预估输出大小
5. "Compress" 按钮 + 进度条
6. 显示压缩结果（原始大小 vs 压缩后大小 vs 压缩率）
7. 下载按钮

---

## 4. Information Architecture

### 4.1 页面结构

```
alici.ai/tools/                          ← 首页（工具目录）
├── alici.ai/tools/youtube-thumbnail-downloader  ← 工具页 1
├── alici.ai/tools/video-to-gif                  ← 工具页 2
├── alici.ai/tools/webm-to-mp4                   ← 工具页 3
├── alici.ai/tools/watermark-remover             ← 工具页 4
└── alici.ai/tools/video-compressor              ← 工具页 5
```

### 4.2 首页设计 (alici.ai/tools/)

```
┌──────────────────────────────────────────────────────────┐
│  [Alici AI Logo]                              [alici.ai] │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Free Online Tools for Creators                          │
│  No login. No upload to servers. 100% private.           │
│                                                          │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐     │
│  │ 🎬 YouTube   │ │ 🎞️ Video    │ │ 🔄 WebM to  │     │
│  │ Thumbnail    │ │ to GIF      │ │ MP4          │     │
│  │ Downloader   │ │ Maker       │ │ Converter    │     │
│  │              │ │              │ │              │     │
│  │ Download HD  │ │ Convert any │ │ Convert WebM │     │
│  │ thumbnails   │ │ video to    │ │ files to MP4 │     │
│  │ from YouTube │ │ animated GIF│ │ instantly     │     │
│  └──────────────┘ └──────────────┘ └──────────────┘     │
│  ┌──────────────┐ ┌──────────────┐                      │
│  │ 🧹 Watermark│ │ 📦 Video    │                      │
│  │ Remover      │ │ Compressor  │                      │
│  │              │ │              │                      │
│  │ Remove AI    │ │ Reduce video│                      │
│  │ watermarks   │ │ file size   │                      │
│  │ from images  │ │ up to 80%   │                      │
│  └──────────────┘ └──────────────┘                      │
│                                                          │
│  ── How It Works ──                                      │
│  1. Choose a tool  2. Upload/paste  3. Process  4. Done  │
│                                                          │
│  ── Why Alici AI Tools? ──                               │
│  ✅ 100% Free     ✅ No Login    ✅ Private              │
│  ✅ No File Limits ✅ No Watermarks ✅ Fast               │
│                                                          │
│  ── Need More Power? ──                                  │
│  Try Alici AI's full creative suite: Video Studio,       │
│  Image Studio, Thumbnail Expert, and more.               │
│  [Explore alici.ai →]                                    │
│                                                          │
├──────────────────────────────────────────────────────────┤
│  © 2026 Alici AI  |  Privacy  |  Terms  |  Blog          │
└──────────────────────────────────────────────────────────┘
```

### 4.3 工具页通用模板

```
┌──────────────────────────────────────────────────────────┐
│  [← All Tools]  [Alici AI Logo]               [alici.ai] │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  H1: {Tool Name}                                         │
│  Subtitle: {One-line description}                        │
│                                                          │
│  ┌──────────────────────────────────────────────────┐    │
│  │                                                    │    │
│  │              [Tool Interactive Area]               │    │
│  │         (Upload / Paste URL / Process)             │    │
│  │                                                    │    │
│  └──────────────────────────────────────────────────┘    │
│                                                          │
│  ── How It Works ──                                      │
│  Step 1 → Step 2 → Step 3 → Step 4                       │
│                                                          │
│  ── Use Cases ──                                         │
│  • Use case 1   • Use case 2                             │
│  • Use case 3   • Use case 4                             │
│                                                          │
│  ── CTA Banner ──                                        │
│  Need more creative power? Try {related product}         │
│  [Try {Product} Free →]                                  │
│                                                          │
│  ── More Free Tools ──                                   │
│  [Tool 2] [Tool 3] [Tool 4] [Tool 5]                     │
│                                                          │
│  ── FAQ ──                                               │
│  ▶ Question 1?  Answer...                                │
│  ▶ Question 2?  Answer...                                │
│  ▶ Question 3?  Answer...                                │
│  ▶ Question 4?  Answer...                                │
│  ▶ Question 5?  Answer...                                │
│                                                          │
│  ── About This Tool ──                                   │
│  {2-3 sentences about the tool and privacy}              │
│                                                          │
├──────────────────────────────────────────────────────────┤
│  © 2026 Alici AI  |  Privacy  |  Terms  |  Blog          │
└──────────────────────────────────────────────────────────┘
```

---

## 5. SEO / AEO Strategy

### 5.1 On-Page SEO

每个工具页必须包含：

| 元素 | 规格 | 目的 |
|------|------|------|
| Title Tag | `{Tool Name} — Free Online | Alici AI Tools` | 搜索结果标题 |
| Meta Description | 含主关键词 + "free" + "no login" + "browser-based" | 搜索结果描述 |
| H1 | 工具名称（含关键词） | 页面主题 |
| H2 sections | How It Works / Use Cases / FAQ / About | 结构化内容 |
| Internal Links | 交叉推荐其他工具 + 链接到 alici.ai 博客 | 内部链接 |
| Canonical URL | `https://alici.ai/tools/{slug}` | 避免重复 |

### 5.2 Schema.org 结构化数据

每个工具页添加 3 种 Schema：

```json
// 1. WebApplication
{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "YouTube Thumbnail Downloader",
  "url": "https://alici.ai/tools/youtube-thumbnail-downloader",
  "applicationCategory": "MultimediaApplication",
  "operatingSystem": "Any (Browser-based)",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "ratingCount": "1250"
  }
}

// 2. FAQPage
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Is this tool free?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes, completely free. No login or payment required."
      }
    }
    // ... more questions
  ]
}

// 3. HowTo
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to Download YouTube Thumbnails",
  "step": [
    {
      "@type": "HowToStep",
      "name": "Paste YouTube URL",
      "text": "Copy the YouTube video URL and paste it into the input field."
    }
    // ... more steps
  ]
}
```

### 5.3 Hub & Spoke 增长策略

```
alici.ai/blog/                          alici.ai/tools/
┌─────────────────────────┐             ┌─────────────────────────┐
│ "How to Download YouTube│ ── link ──> │ YouTube Thumbnail       │
│  Thumbnails in 2026"    │             │ Downloader              │
│ (informational intent)  │ <── link ── │ (transactional intent)  │
└─────────────────────────┘             └─────────────────────────┘
                                                │
                                           CTA link
                                                │
                                                ▼
                                        app.alici.ai
                                        (conversion)
```

每个工具配套一篇博客文章（由 AliciBlog 系统生产），形成：
- **博客** → 捕获 informational intent 搜索（"how to download youtube thumbnail"）
- **工具页** → 捕获 transactional intent 搜索（"youtube thumbnail downloader"）
- **博客 ↔ 工具页** 互相链接 → 提升两者的 SEO 权重
- **工具页 CTA** → 引导至 alici.ai 主产品

---

## 6. Technical Architecture

### 6.1 Tech Stack

| 层级 | 技术 | 理由 |
|------|------|------|
| Framework | **Next.js 14+** (App Router) | SSR/SSG 优化 SEO，React 生态 |
| Styling | **Tailwind CSS** | 快速开发，暗色主题 |
| Video Processing | **@ffmpeg/ffmpeg** (FFmpeg WASM) | 浏览器端处理，零服务器成本 |
| Image Processing | **Canvas API** | Watermark removal 算法 |
| Deployment | **Vercel** | 免费 Hobby 计划，全球 CDN |
| DNS/Routing | **Cloudflare Workers** | `/tools/*` 路由到 Vercel |
| Analytics | **Google Analytics 4** | 免费，与主站一致 |

### 6.2 Subdirectory Routing: alici.ai/tools → Vercel

alici.ai 当前使用 **Cloudflare DNS**（NS: donna/arnold.ns.cloudflare.com）。

**实现方案：Cloudflare Workers 路径路由**

```javascript
// Cloudflare Worker: route /tools/* to Vercel
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  const url = new URL(request.url)

  // Route /tools/* to Vercel deployment
  if (url.pathname.startsWith('/tools')) {
    const vercelUrl = new URL(request.url)
    vercelUrl.hostname = 'alici-tools.vercel.app' // Vercel 部署域名

    const response = await fetch(vercelUrl, {
      method: request.method,
      headers: request.headers,
      body: request.body,
    })

    return response
  }

  // Everything else goes to Framer (default origin)
  return fetch(request)
}
```

**配置步骤**：
1. 在 Cloudflare Workers 中创建上述 Worker
2. 在 Cloudflare Dashboard 中设置 Route: `alici.ai/tools/*` → Worker
3. Next.js 项目中设置 `basePath: '/tools'`（在 `next.config.js`）
4. Vercel 部署 Next.js 项目，域名为 `alici-tools.vercel.app`

**优势**：
- 主站 Framer 完全不受影响
- `/tools/*` 继承 alici.ai 域名的 SEO 权重
- Cloudflare Workers 免费计划 100K 请求/天，完全够用

### 6.3 FFmpeg WASM Loading Strategy

FFmpeg WASM 核心文件约 ~25MB，需要优化加载策略：

```
首页 (alici.ai/tools/)
├── 不加载 FFmpeg WASM（只是工具目录页，无需重处理）
│
└── 工具页 (alici.ai/tools/video-to-gif)
    ├── 页面渲染（SSR）→ 即时显示 UI
    ├── 用户选择文件 → 此时才开始加载 FFmpeg WASM
    ├── 加载提示："Preparing video engine... (first time only)"
    └── Service Worker 缓存 WASM 文件 → 第二次使用秒加载
```

```javascript
// Lazy load FFmpeg only when user uploads a file
const loadFFmpeg = async () => {
  const { FFmpeg } = await import('@ffmpeg/ffmpeg')
  const { fetchFile } = await import('@ffmpeg/util')
  const ffmpeg = new FFmpeg()
  await ffmpeg.load({
    coreURL: '/ffmpeg/ffmpeg-core.js',
    wasmURL: '/ffmpeg/ffmpeg-core.wasm',
  })
  return { ffmpeg, fetchFile }
}
```

### 6.4 YouTube Thumbnail Proxy (Serverless Function)

YouTube 图片直接 `fetch()` 会遇到 CORS 限制。用 Vercel Serverless Function 做 proxy：

```typescript
// app/api/thumbnail/route.ts
import { NextResponse } from 'next/server'

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  const videoId = searchParams.get('id')
  const quality = searchParams.get('q') || 'maxresdefault'

  if (!videoId || !/^[a-zA-Z0-9_-]{11}$/.test(videoId)) {
    return NextResponse.json({ error: 'Invalid video ID' }, { status: 400 })
  }

  const imageUrl = `https://img.youtube.com/vi/${videoId}/${quality}.jpg`
  const response = await fetch(imageUrl)

  if (!response.ok) {
    // Fallback to sddefault if maxresdefault not available
    if (quality === 'maxresdefault') {
      const fallback = await fetch(
        `https://img.youtube.com/vi/${videoId}/sddefault.jpg`
      )
      const buffer = await fallback.arrayBuffer()
      return new NextResponse(buffer, {
        headers: {
          'Content-Type': 'image/jpeg',
          'Content-Disposition': `attachment; filename="${videoId}_sd.jpg"`,
        },
      })
    }
    return NextResponse.json({ error: 'Thumbnail not found' }, { status: 404 })
  }

  const buffer = await response.arrayBuffer()
  return new NextResponse(buffer, {
    headers: {
      'Content-Type': 'image/jpeg',
      'Content-Disposition': `attachment; filename="${videoId}_${quality}.jpg"`,
    },
  })
}
```

**成本**：Vercel Hobby 计划 Serverless Function 免费额度：100GB-Hours/月，足够处理每天数千次请求。

### 6.5 Project Structure

```
alici-tools/
├── app/
│   ├── layout.tsx                    # 全局 Layout (Nav + Footer + GA)
│   ├── page.tsx                      # 首页 (工具目录)
│   ├── youtube-thumbnail-downloader/
│   │   └── page.tsx                  # YT Thumbnail Downloader
│   ├── video-to-gif/
│   │   └── page.tsx                  # Video to GIF
│   ├── webm-to-mp4/
│   │   └── page.tsx                  # WebM to MP4
│   ├── watermark-remover/
│   │   └── page.tsx                  # Watermark Remover
│   ├── video-compressor/
│   │   └── page.tsx                  # Video Compressor
│   ├── api/
│   │   └── thumbnail/
│   │       └── route.ts              # YT Thumbnail proxy API
│   └── sitemap.ts                    # Dynamic sitemap
├── components/
│   ├── ui/                           # Shared UI components
│   │   ├── ToolCard.tsx              # 首页工具卡片
│   │   ├── FileDropzone.tsx          # 文件拖拽上传区
│   │   ├── ProgressBar.tsx           # 进度条
│   │   ├── BeforeAfter.tsx           # Before/After 对比
│   │   └── CTABanner.tsx             # CTA 推广条
│   ├── tools/                        # Tool-specific components
│   │   ├── ThumbnailDownloader.tsx
│   │   ├── VideoToGif.tsx
│   │   ├── WebmToMp4.tsx
│   │   ├── WatermarkRemover.tsx
│   │   └── VideoCompressor.tsx
│   ├── seo/                          # SEO components
│   │   ├── SchemaMarkup.tsx          # JSON-LD Schema
│   │   ├── FAQSection.tsx            # FAQ accordion
│   │   └── HowItWorks.tsx            # Step-by-step section
│   └── layout/
│       ├── Header.tsx
│       └── Footer.tsx
├── lib/
│   ├── ffmpeg.ts                     # FFmpeg WASM loader
│   ├── youtube.ts                    # YouTube URL parser
│   └── watermark.ts                  # Watermark removal algorithm
├── public/
│   └── ffmpeg/                       # FFmpeg WASM binaries (self-hosted)
├── next.config.js                    # basePath: '/tools'
├── tailwind.config.ts
└── package.json
```

---

## 7. Design Specifications

### 7.1 Visual Style

与 alici.ai 主站保持一致：

| 属性 | 值 |
|------|-----|
| 主题 | Dark (暗色) |
| 品牌色 | #97e989 (Alici Green) |
| 背景色 | #000000 / #0a0a0a |
| 卡片背景 | #1a1a1a / #222222 |
| 文字色 | #ffffff (主) / #a0a0a0 (次) |
| 字体 | Manrope (标题) / Inter (正文) |
| 圆角 | 12px (卡片) / 8px (按钮) |

### 7.2 响应式断点

| 断点 | 宽度 | 布局 |
|------|------|------|
| Mobile | < 640px | 单列 |
| Tablet | 640-1023px | 双列工具卡片 |
| Desktop | ≥ 1024px | 三列工具卡片 |

---

## 8. CTA Strategy (工具页 → 主产品)

### 8.1 CTA 映射表

| 工具 | 推荐主产品 | CTA 文案 |
|------|-----------|---------|
| YT Thumbnail Downloader | Thumbnail Expert Pro | "Need to create thumbnails? Try our AI Thumbnail Generator →" |
| Video to GIF | AI Video Studio | "Create professional AI videos with Kling, Runway & Veo →" |
| WebM to MP4 | AI Video Studio | "Generate AI videos in multiple formats →" |
| Watermark Remover | AI Image Studio | "Generate watermark-free AI images directly →" |
| Video Compressor | AI Video Studio | "Create optimized AI videos from text or images →" |

### 8.2 CTA 位置

1. **工具区下方**（使用工具后自然看到）— 主 CTA
2. **More Free Tools 区块旁边** — 辅助 CTA
3. **Footer** — 品牌链接

---

## 9. Phase 2 Roadmap (MVP 后扩展)

| 优先级 | 工具 | 搜索量 | 技术方案 | 成本 |
|--------|------|--------|---------|------|
| P1 | AI Watermark Remover (通用) | 12,100 (+62%) | ONNX Runtime in browser | $0 |
| P1 | Image Upscaler | 49,500 | 复用 alici.ai API (内部) | ~$0 |
| P2 | Background Remover | 60,500 | ONNX (rembg port) | $0 |
| P2 | Video Trimmer | 5,400 | FFmpeg WASM | $0 |
| P3 | Aspect Ratio Calculator | — | 纯 JS | $0 |
| P3 | Audio Extractor | — | FFmpeg WASM | $0 |
| P3 | Video Rotator/Flipper | — | FFmpeg WASM | $0 |

---

## 10. Risk & Mitigation

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| FFmpeg WASM 加载慢 | 用户流失 | Lazy load + SW 缓存 + 加载提示 |
| YouTube CORS 限制 | 无法下载缩略图 | Vercel Serverless proxy |
| YouTube 改变缩略图 URL 结构 | 工具失效 | 监控 + 快速修复 |
| 大文件处理导致浏览器崩溃 | 用户体验差 | 显示文件大小建议 + 分片处理 |
| Cloudflare Worker 路由配置错误 | 主站受影响 | 充分测试 + 灰度发布 |
| Gemini 水印算法更新 | 水印工具失效 | 社区跟踪 + 工具声明"educational" |

---

## 11. Timeline Estimate

| Phase | 工作内容 | 预计时间 |
|-------|---------|---------|
| Phase 0 | 竞品调研 + PRD | ✅ Done |
| Phase 1a | Next.js 框架 + 首页 + 1 个工具 (YT Thumbnail) | 3-5 天 |
| Phase 1b | 剩余 4 个工具开发 | 5-7 天 |
| Phase 1c | SEO 优化 + Schema.org | 2-3 天 |
| Phase 1d | Cloudflare 路由 + 部署 | 1-2 天 |
| Phase 2 | 配套博客文章 x5 | 3-5 天 |
| **Total** | **MVP 上线** | **~2-3 周** |

---

## Appendix A: Keyword Research Data

### YouTube Thumbnail Keywords (合计 ~29,280/mo)
| Keyword | Volume | KD | CPC |
|---------|--------|-----|-----|
| youtube thumbnail downloader | 14,800 | 40 | $0.00 |
| youtube thumbnail download | 4,400 | 20 | $0.00 |
| download youtube thumbnail | 4,400 | 40 | $0.00 |
| youtube thumbnail grabber | 3,600 | 14 | $0.00 |
| yt thumbnail downloader | 1,600 | 18 | $0.00 |
| youtube video thumbnail download | 480 | 36 | $0.00 |

### Video Tool Keywords
| Keyword | Volume | KD | CPC |
|---------|--------|-----|-----|
| video to gif | 90,500 | 40 | $0.19 |
| webm to mp4 | 22,200 | 10 | $0.16 |
| video compressor online | 12,100 | 41 | $0.57 |

### Watermark Keywords (Phase 2 opportunity)
| Keyword | Volume | KD | CPC | Trend |
|---------|--------|-----|-----|-------|
| watermark remover | 135,000 | 52 | $1.67 | +39% |
| ai watermark remover | 12,100 | 33 | $1.63 | +62% |
| remove watermark from image | 5,400 | 34 | $1.92 | +23% |

### Image Tool Keywords (Phase 2)
| Keyword | Volume | KD | CPC |
|---------|--------|-----|-----|
| image upscaler | 49,500 | 52 | $1.40 |
| remove background from image | 60,500 | 57 | $1.63 |

---

## Appendix B: Competitor Quick Reference

| 竞品 | 工具数 | 年收入 | 模式 | 技术 |
|------|--------|--------|------|------|
| 123apps.com | 48 | $1-5M | 免费+广告+$6/mo | Server-side |
| Clideo.com | 40+ | $300K+ | 免费(水印)+$9/mo | Server-side |
| ezGIF.com | 40+ | 高 | 纯广告 | Server-side |
| toolkit.video | 15 | $0 | 免费 | Client-side WASM |
| ThumbnailDown.com | 1 | $0 | 免费 | Server-side |
