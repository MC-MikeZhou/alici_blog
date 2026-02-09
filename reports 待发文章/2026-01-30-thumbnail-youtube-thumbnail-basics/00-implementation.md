具体步骤内容，以easy_mode.md 为准，每次确认步骤请重新查看

# 00-Implementation — Thumbnail Mode 执行记录（v0.2）

- 项目目录：/reports 待发文章/2026-01-30-thumbnail-youtube-thumbnail-basics
- 建议目录名（记录）：
  - ① 2026-01-30-thumbnail-youtube-thumbnail-basics
  - ② 2026-01-30-invideo-youtube-thumbnail-basics
  - ③ 2026-01-30-batch-1
- 最终选择：2026-01-30-thumbnail-youtube-thumbnail-basics（用户已存在目录）

## 执行总览（Step 0 计划概述）
- Step 1 初始化：确认目录名 → 建立项目目录与 sources 子目录 → 记录候选与最终选择。
- Step 2 抓取素材：
  - 网页：优先 r.jina.ai 生成 markdown；保存 `content.md` + `metadata.json`。
  - YouTube：用 Supadata 获取 `transcript.json`；用 YouTube Data API 获取 `metadata.json` + `thumbnails/` 占位。
- Step 3 素材研读与方向建议（当前进行）：
  - 输出每条素材的主要内容总结；
  - 给出 4–5 个写作方向/选题/视角等综合建议；
  - 等待确认后进入写作。
- Step 4 Writer 初稿：输出 `01-article-draft.md`（结构完整，图位占位）。
- Step 5 Editor 改写：按 editor skill 输出 `01-article-draft-2.md`（显著加厚），并比较 size 增幅。
- Step 6 深挖扩写：研读 `/research 竞品分析/invideo-blog/` 文档体系 → 输出 `01-article-draft-3.md`，要求再增厚并对齐模版；比较 size。
- Step 7 去AI化润色：弱化过度结构化的“AI腔”，输出 `01-article-draft-4.md`；比较 size。
- Step 8 生成配图与封面：依据 `asset_plan` 生成/上传图片 → `markdown-to-framer` 产出最终 JSON 与 preview.html。
- Step 9 AEO/Editor Gate：AEO 评分与 Editor 最终回填，准备发布。

当前进度：
- Step 1-2 已满足（目录存在，sources 已建立并含 2 条网页素材）。
- 进入 Step 3：素材总结与方向建议（见下）。

用户确认（2026-01-30）
- 写作方向：YouTube 缩略图入门：12 种高 CTR 模式的正确打开方式（beginner guide 类型）
- 选题/视角：由 Agent 统筹（采用“点击即答案 + 模式-示例-反例”视角）
- 图文案例：需要，先提供 3 组（疑问钩子/前后对比/VS 或结果特写）

下一步
- 执行 Step 4：输出 `01-article-draft.md`（结构完整 + 图位占位 + 3 组图文案例占位）。

## Step 4 完成
- 已生成：`01-article-draft.md`
- 特点：12 模式骨架 + 3 组图文案例 + Source Attribution

## Step 5（Editor）执行与验证
- 已生成：`01-article-draft-2.md`（加厚与重构 + 年份标题 + AEO/CTA/可读性清单 + Visual Prompt Pack + 模板库 + A/B 方法）
- 配图：添加 3 个占位（hero-question-hook / inline-before-after / inline-vs）
- 字节对比：
  - 01-article-draft.md = 9527 bytes
  - 01-article-draft-2.md = 19230 bytes
 - 增长 ≈ 2.02x（满足“至少翻倍”验证）

这里停止，第5步结束，等待继续指令。

## Step 6（深挖扩写）TODO 与执行
- 阅读 TODO（均已完成）：
  - [x] /research 竞品分析/invideo-blog/00-executive-summary.md
  - [x] /research 竞品分析/invideo-blog/01-content-framework.md
  - [x] /research 竞品分析/invideo-blog/02-citation-techniques.md
  - [x] /research 竞品分析/invideo-blog/03-aeo-opening-patterns.md
  - [x] /research 竞品分析/invideo-blog/04-product-integration.md
  - [x] /research 竞品分析/invideo-blog/05-benchmark-articles.md
  - [x] /research 竞品分析/invideo-blog/data/invideo-article-samples.json（如有）

- 扩写方向（已执行）：
  - 新增“内容类型×模式建议（文字矩阵）”
  - 新增“开篇模板建议（AEO）与协作规则”
  - 新增“Citation 标准（不造数据、年份与来源金字塔）”
  - 新增“产品整合建议（中性、场景化、少形容多场景）”
  - 新增图文案例 2 组（结果特写、产品特写）
  - 新增“Benchmark 成功要素”、“A/B 方法与实验日志模板”

- 输出：`01-article-draft-3.md`
  - 01-article-draft-2.md = 19230 bytes
  - 01-article-draft-3.md = 23123 bytes（已提升，满足“明显增加”）
  
这里停止，第6步结束，等待继续指令。

## Step 7（去 AI 化 + 人性化）执行与验证（按新版要求）
新版要求要点：
- 先标记“过于 AI 化/结构化”的段落 → 给出调整方案 → 再实施修改；尽量以“改写”替代“新增板块”。

识别到的过度结构化部分（来自 01-article-draft-3.md）：
- 模式 1/3/4（疑问钩子/前后对比/VS）的小节，只有“用/避/构图/模板/坑/检查”条目，缺少人性化描述。
- “标题 × 缩略图 6 规则”“小屏 10 检查”“模板库”“A/B 方法”“常用短语库”“最终出片 12 步”均为强清单式表达。

调整方案：
- 在模式 1/3/4 内加入“人性化小贴士”（叙事化 2–3 句），不改动原有结构信息。
- 为清单型小节添加过桥句/口语化引导，说明“为什么看/怎么用/常犯错”。
- 将“时间线示例/复盘样例/误区改造/自检三问”分别内嵌到已有对应板块（执行清单/A-B 方法/Benchmark/频道风格），而非新增独立板块。

已实施的修改：
- 删除“每个模式包含…”格式提示，改为自然引导句。
- 模式 1/3/4 已有人性化小贴士，本次新增 2/5/12 的小贴士（仅换表达，不增信息）。
- 标题×封面/小屏 10/模板库/A-B 方法/常用短语库/最终 12 步均加口语过桥句，统一语气。
- 将“时间线”合并到“执行清单”，去除重复标题；将“复盘样例/误区/自检”分别内嵌到 A/B、Benchmark、频道风格。
- 最终 12 步重排为“视觉/文字/流程”三组，保持 12 条原信息不变。

字节对比（以改写为主，仍 ≥10%）：
- 01-article-draft-3.md = 23123 bytes
- 01-article-draft-4.md = 25980 bytes（+12.4%）

这里停止，第7步结束，等待继续指令。
## 素材清单
1) web-vidiq-types-youtube-thumbn
   - URL: https://vidiq.com/blog/post/types-youtube-thumbnails/
   - 格式: markdown（r.jina.ai 抓取）
2) web-invideo-how-to-add-thumbnail
   - URL: https://invideo.io/blog/how-to-add-thumbnail-to-youtube-video/
   - 格式: markdown（r.jina.ai 抓取）

## 第3步：素材主要内容总结

— Source #1: vidIQ《12 Best YouTube Thumbnails》要点 —
- 核心：12 类高点击缩略图格式（Question、Stats、Before/After、Versus、Quotes、Close-up Reaction、Action、Product Feature、Humor、Landscape、Emotional、Tutorial）。
- 原则：单一主体、高对比、少字/强关键词、与标题语义强绑定、做 2–3 个版本做测试。
- 亮点：给出每类示例与应用场景，强调情绪与好奇心在点击中的作用。
- 落地：根据视频类型挑选对应“可读性强”的模式（如教程类突出“结果图”，评测类做“产品阵列 + 暗示差异”）。

— Source #2: InVideo《How to Add a Thumbnail》要点 —
- 核心：缩略图添加与替换的操作路径（上传时/发布后在 Studio 修改）。
- 规范：尺寸与清晰度、在 feed/小图下的可读性、品牌一致性、避免 oversell（反对误导/标题党）。
- 方法：截图法 vs 自定义图；文本叠加与人物抠图的常见组合；文字简短直给，关键词高可读。
- 提示：技术步骤 + 品牌一致性策略 + 不误导用户的内容与外观对齐。

## 第3步：方向建议（供确认后进入写作）

写作方向（4–5 选 1）
1. 《YouTube 缩略图入门：12 种高 CTR 模式的正确打开方式》— 以 vidIQ 的 12 类为骨架，配中文示例与“何时用/何时不用”。
2. 《从入门到实战：新手 0→1 的缩略图制作与替换全流程》— InVideo 的操作规范 + 常见错误 + 最小可行版模板。
3. 《教程/评测/ vlog 各怎么做封面？》— 按内容类型给出最稳妥的模式映射与坑点清单。
4. 《少字高对比：新频道 30 天封面改造计划》— 给 3 套通用模板（问句、对比、结果特写），附执行清单。
5. 《避免 7 个常见雷区：模糊、堆字、用错人像、误导承诺…》— 纠错导向的入门篇。

选题聚焦建议（4–5 选 1）
1. “基础规范 + 12 类模式”合并型：一篇带走“怎么做”和“做成什么样”。
2. “内容类型映射”型：不同视频类型挑不同封面套路（新手易执行）。
3. “模板驱动”型：提供 3–5 个可套用的封面构图与文案格式。
4. “改造实录”型：同一视频做 2–3 张对比图，讲清为什么这张更像“答案”。
5. “小屏可读性”型：只盯手机端，把字数/对比/构图做对。

视角建议（4–5 选 1）
1. “点击即答案”视角：封面是“答案感”强化器，不是情节剧透。
2. “最小信息量”视角：一个主体 + 一行词 + 高对比，专治信息拥堵。
3. “反模式”视角：拆解常见失败封面（堆图标、字太多、色彩脏）。
4. “类型-模式-示例”视角：教程/评测/vlog 各 2 套优先模板。
5. “制作-替换-一致性”视角：从制作到 Studio 替换与品牌一致性闭环。

补充维度（可选并行）
- 图文案例扩充：每类模式 1–2 个中文示例（文字描述 + 占位图说明），后续用于配图指引。
- 版式模板：给出 16:9/1:1/9:16 的安全区与构图示意（文字居中区、标题区）。
- 文案模板：问句模板、对比模板、结果模板各 3 条（少字 + 强对比）。
- 质检清单：尺寸/清晰度/对比度/小图可读/与标题一致/无误导。

待确认问题（进入 Step 4 前）
1) 以上“写作方向/选题/视角”各选 1（或指定自定义组合）。
2) 是否需要“图文案例扩充”？若需要，优先覆盖“问句/对比/结果特写”。
3) 是否对接后续配图（仅占位，Step 8 再生成/上传）？

确认后，将按所选方案输出 `01-article-draft.md` 初稿（Step 4）。
