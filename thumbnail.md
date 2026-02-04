# Easy Mode — 扩展参考版（v0.3）

> 本链路用于 Alici.ai 产品线博客的生产搭建：原始素材仅作为起点，允许充分扩写、加厚与补充多来源证据；对校验项做了适配。与既有三条链路（全自动/手动/Seed）剥离，作为第四条独立链路执行；末端继续复用 Editor → AEO → Framer 能力。

---

## Alici.ai 平台背景

Alici.ai 是一个 AI 内容创作平台，包含三条核心产品线：

| 产品线 | 定位 | 核心能力 | 目标用户 |
|--------|------|---------|---------|
| **Thumbnail** | YouTube 缩略图生成 | Script→Thumbnail、URL 参考风格、One-Face 一致性 | YouTuber、视频创作者 |
| **AI Video** | AI 视频生成 | 多模型选择（Kling/Runway/Sora 等）、一站式生成 | 短视频创作者、营销人员 |
| **AI Image** | AI 图片生成 | 多模型选择（DALL-E/Midjourney/SD 等）、风格迁移 | 设计师、内容运营 |

---

## 第 0 步：选择目标产品线（启动前必选）⭐

在开始前，请确认本次博客目标导量的产品线：

| 选项 | 产品线 | 典型博客主题 | CTA 导向 |
|------|--------|-------------|---------|
| **A** | Thumbnail | 缩略图设计、CTR 优化、封面图模式 | alici.ai/youtube-thumbnail |
| **B** | AI Video | AI 视频生成教程、模型对比、工作流 | 对应模型页面（运行时指定）|
| **C** | AI Image | AI 图片生成教程、风格迁移、Prompt 技巧 | 对应模型页面（运行时指定）|

**交互问句**：
> "请选择本次博客的目标产品线：A. Thumbnail / B. AI Video / C. AI Image"

选择后，后续流程中的产品植入、CTA 链接将自动对齐该产品线。

---

## 定位与范围（顶层规划）

- **目标内容**：关于 {选定产品线} 的"方法论与模式"型文章（如 0→1 指南、模型对比、工作流案例等）。
- **基线模式**：参考扩展（原始素材占比 20%–50%，在不造数据的前提下大量扩写、做厚、补充多来源证据；品牌换 Alici AI）。
- **非目标**：原创测试数据、主观打分/排名、虚构数据等（均禁止）。

---


第0步  plan 启动（重要）
将下面的1-9，所有步骤阅读完整，并总结输出一遍给用户，做一个plan概述，然后再进行第一步，项目初始化。
将下面的1-9，所有步骤阅读完整，并总结输出一遍给用户，做一个plan概述，然后再进行第一步，项目初始化。
将下面的1-9，所有步骤阅读完整，并总结输出一遍给用户，做一个plan概述，然后再进行第一步，项目初始化。



## 第一步 项目初始化

目的：当用户丢入素材（网页 URL / YouTube URL）并与用户对齐项目目录名后，立即在“待发文章”下创建项目目录与每个链接的子目录，并直接抓取可离线浏览的素材包（网页 HTML+静态资源；YouTube 缩略图 + 字幕 + 元信息占位），保证首次运行后即可本地打开查看。




### 1.1) 项目目录命名确认（与用户交互）

目标：在创建目录前，与用户确认“项目目录名”，做到可读、可批量、可追溯。


目录：
/reports 待发文章/YYYY-MM-DD-{topic-or-batch}/

命名权与交互原则
- 项目目录名由用户最终决定；Agent 仅根据素材生成 2–3 个“建议名”供参考，不得自行拍板。
- 未得到用户明确选择/输入前，不得创建目录（无默认自动回退）。
- 自动化/非交互场景：必须显式提供名称（如脚本的 `--name` 参数）；否则终止并提示用户指定名称。

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


### 第二步，从网络获取素材链接的内容
1) 为每个链接创建子目录（sources/*）
- 网页：`web-{domain}-{slug}`（domain 取主域，slug 取路径末段 20 字内，非字母数字转 `-`）。
- YouTube：`yt-{videoId}`（解析 videoId，写入 `transcript.json`/`metadata.json`/`thumbnails/` 占位）。

1) 立即抓取素材（首次运行即离线可读）
  - 目标：获取“可离线复现”。
  下面是3个资源的抓取方式：重要

-1  网页抓取方法：
  优先使用 https://r.jina.ai/${要抓的页面链接}
  获取md， 即为 网页文本内容。

-2 网页中的图片
  https://r.jina.ai/${要抓的页面链接} 获取到上述网页md后，
  查看md，找到图片类型的内容，进行下载，放到.md文件夹中，对应assets/ 下

-3 youtube Transcript 获取（）：
必须获取，不要使用现有的脚本获取，字幕一定要用Supadata curl获取再进行下一步
必须获取，不要使用现有的脚本获取，字幕一定要用Supadata curl获取再进行下一步
必须获取，不要使用现有的脚本获取，字幕一定要用Supadata curl获取再进行下一步

使用 Supadata 获取字幕，保存到 `transcript.json`（保留时间戳、语言、完整行）。
查看 /skills/utilities/youtube-transcript-fetcher/SKILL.md 
使用以下 curl 命令格式：
curl -X GET "https://api.supadata.ai/v1/youtube/transcript?videoId=VIDEO_ID" \
  -H "x-api-key: sd_fe238b5804c459d03740695389a2eb25"

-4 youtube metadata 抓取：
使用 YouTube Data API v3 获取视频基础信息，保存到 `metadata.json`。
YouTube Data API v3  api key 这两个都可以: 
 [
   'AIzaSyCYXZkBE65AKFgESXFc6Vhc7zxtQRUGCFE',
   'AIzaSyAHJM1mA_cV4ge8T9j0Jh7zZyJL38K_hNI'
 ]
  - 解析 videoId（支持 watch/short/embed/youtu.be）：
    - `watch?v=VIDEO_ID`、`youtu.be/VIDEO_ID`、`embed/VIDEO_ID`、`shorts/VIDEO_ID`
  - API 请求（示例）：
    - `GET https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,statistics&id=VIDEO_ID&key=API_KEY`
  - 字段建议：id、title、channelTitle、publishedAt、tags、categoryId、thumbnails（各尺寸）、contentDetails（duration）、statistics（view/like/comment）
  - 同步下载最大分辨率缩略图到 `thumbnails/`（从 snippet.thumbnails.maxres 或默认 fallback）。

用上述方法将所有链接内容获取完毕
第2步结束，重新查看thumbnail.md（文档随时变更，每次完成一步查看一次），确认自己执行到哪一步，下一步是什么。
用户说继续后才能进入下一步


###  第三步 重要 ，完整阅读素材 + 确认写作方向
用growth topic scout的Mode A: URL Analysis对url做一层理解，并输出
用source-parser做一层理解，并输出


根据上面2份输出的内容，确认blog 标题
给出4-5个建议

前置讨论完毕，设定计划
重新查看thumbnail.md（文档随时变更，每次完成一步查看一次），确认自己执行到哪一步，后面都有哪些详细步骤。
根据详细的步骤，列出规划plan list给用户查看
然后按照plan list 依次连续执行



### 第4步，writer模式 开始介入，进行整体撰写
撰写前查看 AGENTS.md内关联的skill。
形成初稿：
- `/reports 待发文章/YYYY-MM-DD-{topic}/01-article-draft.md`
第4步结束，重新查看thumbnail.md（文档随时变更，每次完成一步查看一次），确认自己执行到哪一步，下一步是什么。
然后输出一下自己的进度，完成了什么，下一步做什么。然后进入下一步。


### 第5步，editor 介入
阅读 editor skill（路径：/skills/core/editor/SKILL.md） 对上一版进行修改
步骤不能跳过，必须使用editor skill，基于路径内的文档， 对文章进行新增创意内容 ，修改+其他相关维度扩充。 

关于文章配图：
规划文中配图，穿插在文章当中，不要排在一起.
如果是图文案例，图片和案例要在一起。

关于配图来源，：
1 优先，查看前面使用 https://r.jina.ai/${要抓的页面链接} 抓取的页面，assets/中对应的图片，是否有合适，如果合适可以直接使用。填入对应位置。

2 其次，否则由后续生图来实现。
  当前是否生图：本步骤不需要生成图片，占位即可

- `/reports 待发文章/YYYY-MM-DD-{topic}/01-article-draft-2.md`
记住不需要生成图片，占位即可，不需要再询问用户


第5步结束，重新查看thumbnail.md（文档随时变更，每次完成一步查看一次），确认自己执行到哪一步，下一步是什么。
然后输出一下自己的进度，完成了什么，下一步做什么。然后进入下一步。



### 第6步，不同视角编辑 接入
模仿参考文档的内容，检查是否有需要需要优化的地方

列出todo list
依次查看重点行文参考文档，每个文档阅读完成算一个todo
查看 /research 竞品分析/invideo-blog/00-executive-summary.md
查看 /research 竞品分析/invideo-blog/01-content-framework.md
查看 /research 竞品分析/invideo-blog/02-citation-techniques.md
查看 /research 竞品分析/invideo-blog/03-aeo-opening-patterns.md
查看 /research 竞品分析/invideo-blog/04-product-integration.md
查看 /research 竞品分析/invideo-blog/05-benchmark-articles.md

这里面是重要的文章标题、结构等。是你编辑上一个草稿 01-article-draft-2.md 的重要参考。

阅读todo完成后，输出
- `/reports 待发文章/YYYY-MM-DD-{topic}/01-article-draft-3.md`

第6步结束，重新查看thumbnail.md（文档随时变更，每次完成一步查看一次），确认自己执行到哪一步，下一步是什么。
然后输出一下自己的进度，完成了什么，下一步做什么。然后进入下一步。


### 第7步，执行human-review-checklist skill。 

生成
- `/reports 待发文章/YYYY-MM-DD-{topic}/01-article-draft-4.md`

### 第8步，执行AEO 评分检测
执行aeo-analyzer skill check
目标，达到75分以上，
没有达到，修改blog，如此反复。

### 第9步，  文中配图环节 
9.1
注意，优先使用 source/  中的来源网页配图
先查看一遍source/ 中所有的图片，全部用文字描述出图片内容，列出来给用户，
然后提出一版配图方案，对应之前规划的占位，列出来给用户，让用户选择。
使用source/  图片，可以上传到 cdn获得云端链接，后续使用

9.2
没有使用source/ 中图片的占位，则使用AI生图的方式得到图片 和 fal的云端链接，后续使用，
具体如下
生图会扣费，因此生图前，请告知用户本次会生成多少张配图。用户确认后再继续。
查看 /skills/utilities/youtube-transcript-fetcher/SKILL.md 

具体如何生成配图，上传图片，请参考AGENTS.md 相关介绍

**图片生成**: FAL.ai 
- 脚本: `/scripts/fal_image_generator.py`
- API Key 配置: `.mcp.json` → `mcpServers.fal.env.FAL_API_KEY`
- 读取优先级: 环境变量 > .mcp.json 配置文件
- 持久化: 会话压缩后自动加载，无需手动 export
- 生成的图片会返回 fal的图片链接，可以直接使用

**图片上传**: 
- 上传视频，如果用户使用本地的图片，请通过以下方式上传获得云端链接。
首先要有本地图片的路径
比如 ：前置目录/${name}_${时间戳}.png
上传使用ssh命令：
ssh命令：
rsync -a -r -v -p -e 'ssh -p 22'  --exclude='.DS_Store'  --progress ${完整前置路径}/${name}_${时间戳}.png root@45.76.70.215:/var/www/static/static/image/other/gen_images/
password:  5A_p@cjpX74H(LJM

最终获得的链接如下：
https://ct2.alici.ai/static/image/other/gen_images/${name}_${时间戳}.png
请使用命令上传图片，不要让用户自己上传。


### 第11步，生成文章封面图
生图会扣费，因此生图前，请告知用户
封面语言要求： 英语。
查看 /skills/utilities/blog-cover-generator/SKILL.md  使用thumbnail mode 了解封面的要求，prompt的要求
cover上的文案、人物形象（具体的性别、年龄、国籍）、人物发型发色、服饰和配色、人物的表情（尽可能夸张）和动作（表情和动作十分重要，必须细化）
请使用英语prompt，生成最终版的英文内容图片。




### 第12步，生成预览网页和json
然后基于01-article-draft-4.md，生成 framer.json 和 preview.html
图片的链接，填入framer.json 和 preview.html当中
（生成 framer.json  对应的skill： markdown-to-framer | **v1.3** 🔧 | convert to framer | Framer CMS JSON (**修复**: 图片格式 + 特殊字符) |）
路径： skills/utilities/markdown-to-framer/  文件夹内所有文档

### 第13步，讨论和推荐给用户，英文标题，修改Slug
输出4-5个英文标题，用户确认后
完整翻译 06-article-final.json , 内部字段填入对应的英文，包括标题，
Slug、sub title，也根据最新的标题，进行调整
注意，翻译不能用脚本，需要你作为AI Agent，自行进行翻译。

生成新的  
- `/reports 待发文章/YYYY-MM-DD-{topic}/06-article-final-en.json`

===========================================
 目录结构（建议）

```
/reports/YYYY-MM-DD-thumbnail-design/
├── 00-confirmed-brief.json       # 参考扩展约束 + Thumbnail 参数
├── 01-article-draft.md           # 初稿（结构模板 + 图位占位）
├── 01-article-draft-2.md           # 修改稿，大幅调整，字数大幅增加
├── 01-article-draft-3.md           # 修改稿，大幅调整重构，增加字数，和【/research 竞品分析/invideo-blog/】 内的要求对齐。
├── 02-evidence-pack.md           # 证据包（来源/年份/引文片段/链接）
├── asset_plan.json               # （可选）占位清单
├── 01-article-edited.md          # Editor 回填版
├── 03-aeo-score.md               # AEO 分数与建议
├── 04-editor-report.md           # 模块检查 + 阻断/警告
└── 06-article-final.json         # Framer JSON（封面图和文中配图已完整）
preview.html  预览html
```


