# Alici AI Toolkit - 调研总结

> 日期：2026-02-08
> 任务来源：Basecamp - "✨ 神奇的小工具站：toolkit.video——AEO向、免费、易用"
> 负责人：Dancy

---

## Basecamp 原始任务

**Hans 的 Message**：
- 参考竞品：[toolkit.video](https://toolkit.video/)
- 提到的工具：YouTube Thumbnail Downloader、Nano Banana Watermark Remover
- 有一个 GPT5 Pro 谈增长的 ChatGPT 对话链接

**Hans 给 Dancy 的 Comment (2026-01-31)**：
> "@dancy 来驱动下这个小工具落地，我仔细看了 Youtube thumbnail Download/downloader 这些关键词，流量相当可观"
- 附带 3 张截图（关键词数据 + VIDIQ 数据）

---

## 竞品分析

### toolkit.video (直接对标)
- **15 个工具**，全部浏览器端处理 (FFmpeg WASM + Canvas API)
- 零登录、零广告、零收费、零水印
- 隐私优先：文件不离开用户设备
- 暗色主题，响应式设计
- SEO 中等：有独立页面但无 Schema.org、无博客、无多语言

### 市场格局

| 竞品 | 工具数 | 年收入 | 商业模式 | 登录要求 |
|------|--------|--------|---------|---------|
| 123apps.com | 48 | $1-5M | 免费+广告+会员$6/mo | 可选 |
| Clideo.com | 40+ | $300K+ | 免费(加水印)+会员$9/mo | 需要 |
| ezGIF.com | 40+ | 高 | 纯广告 | 不需要 |
| toolkit.video | 15 | $0 | 无 | 不需要 |
| ThumbnailDown.com | 1 | $0 | 无 | 不需要 |

### YouTube Thumbnail Downloader 专项竞品
- **ThumbnailDown.com**：Schema.org (HowTo + FAQPage)、Chrome 扩展、支持 Vimeo/Dailymotion
- **YouTubeThumbnailDownloader.com**：有博客内容、提供 1080p
- **YouTube-Thumbnail-Saver.com**：4K 支持、标题含年份

### 技术实现参考
- **FFmpeg WASM**：C/C++ 编译为 WebAssembly，浏览器端运行 FFmpeg
- **YouTube 缩略图**：公开 URL `img.youtube.com/vi/{ID}/{quality}.jpg`
- **Gemini 水印移除**：反向 alpha 混合算法，开源 JS 实现

---

## 关键词数据 (DataForSEO 2026-02-08)

### TOP 10 关键词（按搜索量排序）

| 排名 | 关键词 | 月搜索量 | 难度 | CPC | 趋势 |
|------|--------|---------|------|-----|------|
| 1 | watermark remover | 135,000 | 52 | $1.67 | +39% |
| 2 | video to gif | 90,500 | 40 | $0.19 | +13% |
| 3 | remove background from image | 60,500 | 57 | $1.63 | -6% |
| 4 | image upscaler | 49,500 | 52 | $1.40 | +14% |
| 5 | ai image enhancer | 22,200 | 65 | $2.01 | 0% |
| 6 | webm to mp4 | 22,200 | 10 | $0.16 | 0% |
| 7 | youtube thumbnail downloader | 14,800 | 40 | $0.00 | 0% |
| 8 | ai watermark remover | 12,100 | 33 | $1.63 | +62% |
| 9 | video compressor online | 12,100 | 41 | $0.57 | -23% |
| 10 | remove watermark from image | 5,400 | 34 | $1.92 | +23% |

### YouTube Thumbnail 关键词组合计
- youtube thumbnail downloader: 14,800
- youtube thumbnail download: 4,400
- download youtube thumbnail: 4,400
- youtube thumbnail grabber: 3,600
- yt thumbnail downloader: 1,600
- youtube video thumbnail download: 480
- **合计：~29,280/mo**

### 关键发现
1. **Watermark removal 是最大机会** — 155K 合计搜索量，全部上涨
2. **YouTube Thumbnail 关键词 CPC = $0** — 无广告价值，但流量可观
3. **WebM to MP4 最容易排名** — KD=10，新站几周内可排名
4. **"AI" 前缀关键词增长最快** — ai watermark remover +62%
5. **视频工具类关键词多数下降** — compressor -23%, trimmer -34%

---

## MVP 工具清单 (推荐)

### Phase 1: 5 个零成本工具
1. **YouTube Thumbnail Downloader** — Hans 指定，YouTube 创作者定位
2. **Video to GIF** — 最大流量池 90.5K/mo
3. **WebM to MP4** — 最低竞争度，最快排名
4. **Nano Banana Watermark Remover** — Hans 指定，独特性
5. **Video Compressor** — 刚需工具

**全部 API 成本 = $0**（浏览器端处理）

### Phase 2: 扩展工具
6. AI Watermark Remover (客户端 ML)
7. Image Upscaler (复用 alici.ai API)
8. Background Remover (客户端 ML)
9. Video Trimmer (FFmpeg WASM)
10. Aspect Ratio Calculator (纯前端)
