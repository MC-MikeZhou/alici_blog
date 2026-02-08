# UGC Ads 对标研究成本记录（InVideo ↔ Alici use cases）

日期：2026-02-06  
范围：英文内容线；目标受众偏 UGC creators；平台偏 TikTok/Reels（短视频竖屏广告）

---

## 1) 研究目标

- 验证：InVideo 的“已验证成功”的 AEO/SEO 内容形态里，**是否存在**与我们“小 use case（单条创意/脚本/镜头）”等价的对标载体。
- 产出：一份“可立刻落地”的选题清单（含 InVideo 对标文章）+ 一份“可直接放进大拼盘 Examples/Swipe file”的 Alici 用例候选清单。

---

## 2) 方法与数据来源

### A. 本地竞品研究资料（repo 内已有）

- `research 竞品分析/invideo-blog/00-executive-summary.md`（AEO/SEO 结构总结）
- `research 竞品分析/invideo-blog/03-aeo-opening-patterns.md`（开篇模式/Key Takeaways 等）
- `research 竞品分析/invideo-blog/05-benchmark-articles.md`（标杆文章拆解）

### B. 在线对标文章（直接引用 InVideo 实站 URL）

用途：用于“选题 → 对标文章形态”的映射（examples/ideas/templates/workflow 等）。

### C. Alici 现有用例池（聚合页 + 明细页）

- 聚合页：`https://alici.ai/video-super-agent/use-cases`
- 明细页：逐个抓取 `<title>` 与页面内标签（如 “Product Ads / Stories / Mode / TikTok / Instagram / YouTube Shorts”）做快速归类。

---

## 3) 执行量（可复用的“成本指标”）

### A. Alici 用例抓取与归类

- 扫描聚合页并抽取 slug：45 条 use case（可复现：从聚合页 HTML 抽链接）。
- 抓取明细页并打标签：
  - **明确标注 “Product Ads” 的用例：12 条**
  - “ad-ish”（未标 Product Ads，但标题/文案明显是 ad/promo/spot）：额外 7 条左右
  - 合计“可用于 UGC ads 大拼盘”的候选：**19 条（MVP 足够）**
- 同时做了粗略垂直分桶（Beauty/Skincare、Food、Fashion/Luxury、Auto、Tech、Outdoor、Entertainment、Info product、Other）。

### B. InVideo 对标库确认（“小颗粒”在哪里）

核心结论：InVideo 的“小颗粒内容”更多出现在：

1) **Examples/Ideas/Templates 类长文的中部模块**（每条 idea/example 颗粒很小，但容器是长文）  
2) **Landing（/make）与 Help center**（更接近“小页面打法”）

因此，对标路径不是“写很多 300–600 词 blog 小文”，而是：

- Blog：写 InVideo 成功形态（Examples/Ideas/Workflow），把 Alici use case 当“卡片化 example”塞进去；
- Use case：作为资产页承接（脚本/镜头/字幕/变体/提示词）。

---

## 4) 关键中间产物（本次已产出）

### A. 计划文档（已落盘）

- `research 竞品分析/2026-02-06-ugc-ads-usecase-plan.md`

### B. 候选用例清单（本次从现有池里筛出的“可用 UGC ads 资产”）

**优先级 P0（明确 Product Ads 标签，适合直接当 Examples 卡片）：**

- Marilyn Glam Makeup Tutorial Video Concept  
  https://alici.ai/video-super-agent/use-cases/marilyn-monroe-masterclass-vintage-glam-meets-modern-beauty-brands
- Fruit Rollercoaster Sip | Gen-Z Soda Ad Short  
  https://alici.ai/video-super-agent/use-cases/fruit-rollercoaster-soda-ad
- Family SUV Road Trip Ad | Bring Home On the Road  
  https://alici.ai/video-super-agent/use-cases/family-suv-bring-home-on-road
- Smart Home Comfort Video Storyboard  
  https://alici.ai/video-super-agent/use-cases/fresh-start-tech-tour-cozy-gadgets-for-mindful-living
- Icebreaking Kayak POV Ad | Rugged Action Cam Short  
  https://alici.ai/video-super-agent/use-cases/icebreaking-kayak-action-cam
- Luxury Tennis Fashion Video for Viral Reels  
  https://alici.ai/video-super-agent/use-cases/court-couture-spotlight-game-set-match-fashion-film
- K-pop Christmas Fashion Drop Video Guide  
  https://alici.ai/video-super-agent/use-cases/k-pop-christmas-capsule-three-street-looks-one-epic-finale
- Luxury Animal Mascot Studio Video Outline  
  https://alici.ai/video-super-agent/use-cases/luxury-icons-reimagined-as-animal-mascots
- Spotify Playlist Morph Walk Video Concept  
  https://alici.ai/video-super-agent/use-cases/spotify-playlist-portal-one-walk-seven-worlds
- M&M Detective Short | Colorful Viral Mini-Mystery  
  https://alici.ai/video-super-agent/use-cases/mnm-detective-color-case
- Mayan Roots Rising Spiritual Course Video Brief  
  https://alici.ai/video-super-agent/use-cases/new-year-new-spirit-mayan-roots-awakening-guide
- Akira Sanctuary Luxury Retreat Video Storyboard  
  https://alici.ai/video-super-agent/use-cases/akira-sanctuary-retreat-where-whales-meet-waterfalls

**优先级 P1（未标 Product Ads，但“广告意图”明显，可补齐大拼盘的行业多样性）：**

- Uji Matcha Morning Ritual Ad  
  https://alici.ai/video-super-agent/use-cases/uji-matcha-morning-ritual-ad
- Sony Walkman Cyberpunk Rooftop | 20s Synthwave Ad  
  https://alici.ai/video-super-agent/use-cases/sony-walkman-cyberpunk-rooftop
- Bear-Ear Selfie Flash | 10s App Promo Short  
  https://alici.ai/video-super-agent/use-cases/bear-ear-selfie-flash
- Mermaid Volleyball Shades Ad | Fantasy Unicorn Spot  
  https://alici.ai/video-super-agent/use-cases/mermaid-volleyball-unicorn-sunglasses
- City Pop Mini Adventure | 10 Micro Worlds for Shorts  
  https://alici.ai/video-super-agent/use-cases/city-pop-miniature-adventure
- LEGO Horror Bloopers Short Video Outline  
  https://alici.ai/video-super-agent/use-cases/adorably-terrifying-lego-horror-bloopers-reel

---

## 5) 选题 ↔ InVideo 对标（本次确定的“已验证容器”）

> 目的：保证我们不是“另起炉灶”，而是复刻 InVideo 已验证的内容形态（examples/ideas/workflow）。

1) **大拼盘 Swipe file：UGC Ad Examples (Across Industries)**  
对标：
- https://invideo.io/blog/instagram-ads-examples/  
- https://invideo.io/blog/facebook-ad-ideas/  
- https://invideo.io/blog/product-video-ideas-with-templates/

2) **模板/创意库：Product Video Ideas with Templates（UGC-Style）**  
对标：
- https://invideo.io/blog/product-video-ideas-with-templates/  
- https://invideo.io/blog/how-to-create-commercial-product-video/

3) **方法论：A/B Test UGC Hooks（hook matrix + scorecard）**  
对标：
- https://invideo.io/blog/how-to-ab-test-product-ads/  
- https://invideo.io/blog/create-scroll-stopping-ads-with-kling-on-invideo/

4) **UGC ads 主题底层解释 + 入口页**  
对标：
- https://invideo.io/blog/ai-ugc-ads/  
- https://invideo.io/make/ugc-ads/  
- https://help.invideo.io/en/articles/10959388-how-can-i-create-a-ugc-ad-video

5) **“更人味”的 AI 广告叙事（品牌向）**  
对标：
- https://invideo.io/blog/how-to-build-soul-into-ai-ads/

6) **Testimonial/Review 类（下一批缺口方向）**  
对标：
- https://invideo.io/blog/testimonial-video-ideas/

---

## 6) 限制与风险（成本相关）

- **聚合页抓取可行，但没有结构化 JSON**：页面不暴露 `__NEXT_DATA__`，只能靠 HTML 抽链接 + 明细页关键字打标签（可用，但后续若要规模化建议给用例加结构化字段/站内标签）。
- **现有 Beauty/Skincare 用例偏少**：如果后续要做“垂直赛道系列”，需要新增一批“证言/测评/前后对比/开箱”等更典型 UGC archetype 的用例页（否则文章只能做成大拼盘，不容易形成垂直主题权威）。

---

## 7) 下一步建议（按投入产出排序）

1) 先用 P0/P1 候选做一篇 **UGC Ad Examples（大拼盘）**，快速验证曝光与点击链路（blog → use case）。
2) 同时把 “Testimonial/Review/Before-after” 作为 next batch 用例新增方向（对齐 InVideo testimonial ideas 的需求面）。
3) 等大拼盘跑出数据后，再决定是否拆出 Beauty/Skincare 的垂直系列（避免一开始就“赛道过窄”的焦虑）。

