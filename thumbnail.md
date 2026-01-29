# Thumbnail Mode — 洗稿基线版（v0.1）

> 本链路专门用于“Thumbnail 主题博客”的生产，基于洗稿模式（rewrite_mode）搭建，但对对象与校验项做了适配。与既有三条链路（全自动/手动/Seed）剥离，作为第四条独立链路执行；末端继续复用 Editor → AEO → Framer 能力。

---

定位与范围

- 目标内容：关于缩略图/封面图设计的“方法论与模式”型文章（如 0→1 指南、12 类高 CTR 模式、对比与案例网格等）。
- 基线模式：洗稿（40%+ 保留原素材结论与模式，新增大量内容做厚；品牌换 Alici AI）。
- 非目标：原创测试数据、主观打分/排名、虚构 CTR/点击差异等（均禁止）。

---

## 第一步 项目初始化与素材归档

目的：当用户丢入素材（网页 URL / YouTube URL）并与用户对齐项目目录名后，立即在“待发文章”下创建项目目录与每个链接的子目录，并直接抓取可离线浏览的素材包（网页 HTML+静态资源；YouTube 缩略图 + 字幕 + 元信息占位），保证首次运行后即可本地打开查看。


### 1.1) 项目目录命名确认（与用户交互）

目标：在创建目录前，与用户确认“项目目录名”，做到可读、可批量、可追溯。


目录：
/reports 待发文章/YYYY-MM-DD-{topic-or-batch}/

命名权与交互原则
- 项目目录名由用户最终决定；Agent 仅根据素材生成 2–3 个“建议名”供参考，不得自行拍板。
- 未得到用户明确选择/输入前，不得创建目录（无默认自动回退）。
- 自动化/非交互场景：必须显式提供名称（如脚本的 `--name` 参数）；否则终止并提示用户指定名称。
- 记录与可追溯：在 `00-implementation.md` 中记录建议名列表与最终选定名、时间与操作者标识。

- 候选模板（按优先顺序给出 2–3 个供选择）：
  1) `YYYY-MM-DD-thumbnail-{short-topic}`
  2) `YYYY-MM-DD-{publisher-or-source}-{short-topic}`（如 `youtube`/`invideo`/`higgsfield`）
  3) `YYYY-MM-DD-batch-{n}`（多链接批处理）

- `{short-topic}` 生成规则：
  - 从首个素材标题/URL 提取，转小写，非字母数字转 `-`，连续连字符合并，最多 30 字符。
  - 保留关键词 2–4 个为佳（例：`youtube-thumbnail-0-to-1`）。

- 交互问句（示例）：
  - “检测到素材主题为 ‘{auto_topic}’，建议目录名：
    - ① `{d1}`
    - ② `{d2}`
    - ③ 自定义（输入英文/连字符）
    请选择 1/2/3 或输入自定义（留空将再次询问）：”



确认完项目目录和名称后，
初始化流程（单/批量）：
1) 创建项目目录（按当天批次或主题名）
- 规则：`/reports 待发文章/YYYY-MM-DD-{topic-or-batch}`；`topic-or-batch` 尽量短小写、连字符。
- 写入/追加 `00-implementation.md`（记录素材清单、时间、操作者、候选名与最终名）。
存在目录则不在新建


1) 为每个链接创建子目录（sources/*）
- 网页：`web-{domain}-{slug}`（domain 取主域，slug 取路径末段 20 字内，非字母数字转 `-`）。
- YouTube：`yt-{videoId}`（解析 videoId，写入 `transcript.json`/`metadata.json`/`thumbnails/` 占位）。

1) 立即抓取素材（首次运行即离线可读）
- 目标：获取“可离线复现。
  下面是3个资源的抓取方式：重要

-1  网页抓取方法：
  优先使用 https://r.jina.ai/${要抓的页面链接}
  获取md，然后再将md内的资源，如图片，下载到对应的assets文件夹中，
  md 即为 网页内容。

-2 youtube Transcript抓取：使用 Supadata 获取字幕（接口/SDK 以团队现有方案为准），保存到 `transcript.json`（保留时间戳、语言、完整行）。
使用以下 curl 命令格式（注意：你需要告诉用户执行此命令，或者使用可用的工具）：
curl -X GET "https://api.supadata.ai/v1/youtube/transcript?videoId=VIDEO_ID" \
  -H "x-api-key: sd_fe238b5804c459d03740695389a2eb25"
```
supadata.ai 其他功能和api，如需要可自行搜索它的文档

-3 youtube metadata 抓取：
使用 YouTube Data API v3 获取视频基础信息，保存到 `metadata.json`。
YouTube Data API v3  api key 这两个都可以: 
▌ [
▌   'AIzaSyCYXZkBE65AKFgESXFc6Vhc7zxtQRUGCFE',
▌   'AIzaSyAHJM1mA_cV4ge8T9j0Jh7zZyJL38K_hNI'
▌ ]
  - 解析 videoId（支持 watch/short/embed/youtu.be）：
    - `watch?v=VIDEO_ID`、`youtu.be/VIDEO_ID`、`embed/VIDEO_ID`、`shorts/VIDEO_ID`
  - API 请求（示例）：
    - `GET https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,statistics&id=VIDEO_ID&key=API_KEY`
  - 字段建议：id、title、channelTitle、publishedAt、tags、categoryId、thumbnails（各尺寸）、contentDetails（duration）、statistics（view/like/comment）
  - 同步下载最大分辨率缩略图到 `thumbnails/`（从 snippet.thumbnails.maxres 或默认 fallback）。


至此，链路中用户提供的素材准备完毕，即完成第一步。

后面待修改











## 2) 执行链路（Thumbnail Pipeline）

```
输入（URL/参考文档）
  ↓  Step 0: 项目初始化与素材归档（本地快照/字幕/元数据）
  ↓  Step 1.5: 素材使用意图 = 洗稿（rewrite_mode）
  ↓  Step 2: 快速问卷（受众/平台/是否包含案例网格）
  ↓  Step 3: 内容抓取与要素抽取（pattern 列表、Do/Don't、示例、用词上限、尺寸规范）
  ↓  Step 4: Writer 生成（Thumbnail 结构模板，洗稿约束生效）
  ↓  Step 5: Editor Gate（InVideo 六原则 + 标题/开篇/CTA 强制）
  ↓  Step 6: AEO 分析（≥75 理想；<75 触发改进）
  ↓  Step 7: Framer JSON（可选：预览）
```

---

## 3) 洗稿基线 → Thumbnail 适配

### 3.1 rewrite_mode 约束映射

```yaml
rewrite_mode:
  enabled: true
  reference_ratio: 0.8            # 80%+ 内容参考原素材
  word_count_ratio: [0.8, 1.2]    # 字数相对原素材
  brand_swap: "Alici AI"

  # Thumbnail 特化（以“模式/规范”替代“工具/场景”锁定）
  lock_pattern_catalog: true       # 不新增原素材未提及的模式类型/数量
  lock_design_rules: true          # 不新增原素材未给出的强规则（如尺寸/用词上限/安全边距）
  no_fabricated_metrics: true      # 禁止编造 CTR/点击率/排名/评分

validation:
  check_pattern_set_match: true    # 原素材的模式清单一致（名称允许同义改写）
  check_word_count_range: true
  check_claim_accuracy: true       # 评分/排名/百分比→必须有来源，否则阻断
  strict: true
```

说明：
- “工具/场景锁定”在 Thumbnail 语境中改为“模式目录/设计规则锁定”。
- 允许结构化重写、表达优化与品牌位（CTA）植入，但不新增事实性主张与测试数据。

### 3.2 InVideo 六原则（仍然适用）

- Key Takeaways 前置（⛔）
- Reframe 开篇（⛔）：示范“演示好看 ≠ CTR 高”，重定义为“低信息量、强对比、可读性优先”。
- Source Attribution 专章（⛔）：声明来源/方法与披露。
- 无虚假声明（⛔）：评分/排名/CTR 百分比必须注明来源与年份。
- L4 整合者定位（⚠️）：定位为“整合能力/一站式起步”，非与竞品对立。
- 引用密度（⚠️）：≥3/千字（Thumbnail 类文章推荐值；可按项目上调）。

---

## 4) 结构模板（Thumbnail 洗稿版）

1. H1 标题（含年份）
2. Quick Answer / Key Takeaways（120–180 词）
   - 3–5 条可复制的设计准则（如“主文案 ≤4 词，主体占画面 40–60%”等）
   - CTA #1（轻）：Try Alici.ai Thumbnail（thumbnail_pro）
3. Source Attribution / About This Guide（100–150 词，⛔ 必须）
   - Testing/Review Source、Date、Method（如“基于 [Source] 的模式归纳”）
   - Disclosure：“alici.ai 未独立验证全部结果，具体表现与素材相关”
   - 原始来源链接
4. Thumbnail Pattern Catalog（模式 × N，小节模式：Why it works / When to use / Text limit / Pitfalls）
5. Case Grid（可选）：模式对比网格（文字极简、强对比的占位图或引用示例的文字描述）
6. How to Try（最小步骤：选模式→2–4 词文案→主体/背景对比→10–15% 缩放自检）+ CTA #2（中）
7. Mini FAQ（6–8 题）
8. Final Advice + L4 Integrator（“不必只选一种，先用一站式起步做 AB 版”）+ CTA #3（强）

注：为保持洗稿边界，默认不新增外部图片生成；如确需插图，请使用 Editor 的占位/清单并在 manifest 披露“来源/生成/是否可替代”。

---

## 5) 验证与阻断（Thumbnail 专项）

Blocking（任一触发即阻断）：
- Key Takeaways 未在 H1 后 500 字符内出现。
- 开篇未符合 Reframe 模式；包含弱开篇（In this article…）。
- 缺少 Source Attribution/Disclosure/来源链接。
- 出现无来源评分/排名/CTR 声称；第一人称“我们测试/我们的研究”。
- 新增原素材未包含的“模式类别/强规则”。

Warning（保留并提示）：
- 引用密度 < 3/千字；L4 定位缺失。
- 字数超出 120% 或低于 80%（模板需求可放宽并在报告中解释）。

附加检查：
- Pattern Set Match：名称可重述，但模式数与核心定义需一致。
- 文案长度约束：建议主文案 ≤ 4 词（或 ≤ 12 字母），超过则提示。
- 10–15% 缩放可读性（人工/半自动打点）。

---

## 6) 数据契约与输出

输入（参考标准）：
- `/reports/YYYY-MM-DD-{topic}/01-article-draft.md`
- `/reports/YYYY-MM-DD-{topic}/asset_plan.json`（可选：若保留占位符）
- `/reports/YYYY-MM-DD-{topic}/prompt_pack.md`（可选）

Editor 输出（复用现有）：
- `/reports/YYYY-MM-DD-{topic}/01-article-edited.md`
- `/reports/YYYY-MM-DD-{topic}/asset_manifest.json`（新增字段可选：`text_length_ok`, `safe_margin_ok`, `readability_score`, `brand_match`）
- `/reports/YYYY-MM-DD-{topic}/prompts_used.md`

说明：Thumbnail Mode 基线下，图片生成默认 SKIP（洗稿边界）；如启用资产生成，需在 manifest 中完整披露来源/生成方法与可读性自检结果。

---

## 7) 目录结构（建议）

```
/reports/YYYY-MM-DD-thumbnail-design/
├── 00-confirmed-brief.json       # 洗稿约束 + Thumbnail 参数
├── 01-article-draft.md           # 初稿（结构模板 + 图位占位）
├── asset_plan.json               # （可选）占位清单
├── 01-article-edited.md          # Editor 回填版
├── 03-aeo-score.md               # AEO 分数与建议
├── 04-editor-report.md           # 模块检查 + 阻断/警告
└── 06-article-final.json         # Framer JSON（封面图可为空或占位）
```

---

## 8) 版本与后续

- v0.1（当前）：确立洗稿基线与 Thumbnail 适配映射、结构模板与阻断清单。
- v0.2（计划）：
  - 可读性半自动评分（10–15% 缩放 + OCR 文本长度/对比度检测）写入 manifest。
  - Pattern 小组件库（模板化片段与对比网格占位）。
  - 产品映射：CTA 自动映射到 `thumbnail_pro`（PRODUCT_CATALOG）。
