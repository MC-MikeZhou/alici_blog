# Thumbnail Mode — 扩展参考版（v0.2）

> 本链路专门用于“Thumbnail 主题博客”的生产搭建：原始素材仅作为起点，允许充分扩写、加厚与补充多来源证据；对对象与校验项做了适配。与既有三条链路（全自动/手动/Seed）剥离，作为第四条独立链路执行；末端继续复用 Editor → AEO → Framer 能力。 
> 本链路 Thumbnail 主题博客 生产的blog，最终会导量到我们网站的 Alici.ai Thumbnail 创作工具产品。
### Alici.ai Thumbnail 产品背景
Alici.ai 是一个 AI 内容创作平台，其中 **Thumbnail 生成** 是核心产品之一。
### Thumbnail 产品核心功能
| 功能 | 描述 | 竞品对比 |
|------|------|---------|
| **AI 快速生成** | 从创意/脚本快速生成缩略图 | 与 Canva/vidIQ 类似 |
| **Script → Thumbnail** | 输入视频脚本，自动生成匹配的缩略图
| **URL Reference** | 输入参考视频 URL，生成类似风格缩略图
| **One-Face** | 上传 1 张照片，所有缩略图自动使用你的脸
### 目标用户
**主要用户**: 小 YouTuber / 小视频创作者 / 新手创作者
————————
产品Landing Page：https://alici.ai/youtube-thumbnail




注意，充分扩写，加厚，但
不可增加一些【附录】，【习题集】等，和主线内容偏离较大的内容
不可增加一些【附录】，【习题集】等，和主线内容偏离较大的内容
不可增加一些【附录】，【习题集】等，和主线内容偏离较大的内容
---



---

定位与范围（顶层规划）

- 目标内容：关于缩略图/封面图设计的“方法论与模式”型文章（如 0→1 指南、12 类高 CTR 模式、对比与案例网格等）。
- 基线模式：参考扩展（原始素材占比 20%–50%，在不造数据的前提下大量扩写、做厚、补充多来源证据；品牌换 Alici AI）。
- 非目标：原创测试数据、主观打分/排名、虚构 CTR/点击差异等（均禁止）。

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
这里停止，第2步结束，重新查看thumbnail.md（文档随时变更，每次完成一步查看一次），确认自己执行到哪一步，下一步是什么。
用户说继续后才能进入下一步


###  第三步 重要 ，完整阅读素材 + 方向建议（Agent）
重要 ，完整阅读素材 + 方向建议（Agent）
重要 ，完整阅读素材 + 方向建议（Agent）
重要 ，完整阅读素材 + 方向建议（Agent）
一定要输出链接内容，讨论方向建议，才能动手
一定要输出链接内容，讨论方向建议，才能动手
一定要输出链接内容，讨论方向建议，才能动手

3.1 刚下载到本地的内容（网页 Markdown、assets 图片、YouTube transcript 与 metadata、thumbnails），
先输出每个素材链接的主要内容总结。
先输出每个素材链接的主要内容总结。
先输出每个素材链接的主要内容总结。
3.2  
输出完链接的总结后，给出下列建议：
写作方向建议 综合考虑提出 4–5 个建议
选题方向建议。 综合考虑提出 4–5 个建议
内容的视角建议。综合考虑提出 4–5 个建议
等等其他维度你能考虑到在列出一些，综合考虑提出 4–5个建议
是否需要图文案例进行内容扩充？

3.3  根据3.2的选项，确认blog 标题
给出4-5个建议

3.4 前置讨论完毕，设定计划
重新查看thumbnail.md（文档随时变更，每次完成一步查看一次），确认自己执行到哪一步，后面都有哪些详细步骤。
根据详细的步骤，列出规划plan list给用户查看
然后按照plan list 依次连续执行



### 第4步，writer模式 开始介入，进行整体撰写
撰写前查看 AGENTS.md内关联的skill。
形成初稿：
- `/reports 待发文章/YYYY-MM-DD-{topic}/01-article-draft.md`
第4步结束，重新查看thumbnail.md（文档随时变更，每次完成一步查看一次），确认自己执行到哪一步，下一步是什么。
然后输出一下自己的进度，完成了什么，下一步做什么。然后进入下一步。


### 第5步，editor 创意扩写介入
阅读 editor skill（路径：/docs\项目文档/exports/editor-skill\ v2.9） 对上一版进行修改
步骤不能跳过，必须使用editor skill，基于路径内的文档， 对文章进行新增创意内容 ，修改+其他相关维度扩充。 

不可增加一些【附录】，【习题集】等，和主线内容偏离较大的内容
不可增加一些【附录】，【习题集】等，和主线内容偏离较大的内容
不可增加一些【附录】，【习题集】等，和主线内容偏离较大的内容

关于文章配图：
规划文中配图，穿插在文章当中，不要排在一起.
如果是图文案例，图片和案例要在一起。

关于配图来源，：
1 优先，查看前面使用 https://r.jina.ai/${要抓的页面链接} 抓取的页面，assets/中对应的图片，是否有合适，如果合适可以直接使用。填入对应位置。

2 其次，否则由后续生图来实现。
  当前是否生图：本步骤不需要生成图片，占位即可

- `/reports 待发文章/YYYY-MM-DD-{topic}/01-article-draft-2.md`
记住不需要生成图片，占位即可，不需要再询问用户

验证：
写完后，对比 01-article-draft.md 01-article-draft-2.md ，直接输出二者的size，字节数，进行比较。看看size 大小是否有增加一倍，如果没有，重新进行这一步。

第5步结束，重新查看thumbnail.md（文档随时变更，每次完成一步查看一次），确认自己执行到哪一步，下一步是什么。
然后输出一下自己的进度，完成了什么，下一步做什么。然后进入下一步。



### 第6步，学习竞品模版，对草稿进行整体改造。 至关重要的一步，一定要一一执行
模仿竞品的行文结构，重写草稿，新增维度内容，深挖扩写原有内容 
模仿竞品的行文结构，重写草稿，新增维度内容，深挖扩写原有内容 

列出todo list
依次查看重点行文参考文档，每个文档阅读完成算一个todo
查看 /research 竞品分析/invideo-blog/00-executive-summary.md
查看 /research 竞品分析/invideo-blog/01-content-framework.md
查看 /research 竞品分析/invideo-blog/02-citation-techniques.md
查看 /research 竞品分析/invideo-blog/03-aeo-opening-patterns.md
查看 /research 竞品分析/invideo-blog/04-product-integration.md
查看 /research 竞品分析/invideo-blog/05-benchmark-articles.md
查看 /research 竞品分析/invideo-blog/data/invideo-article-samples.json

这里面是重要的文章结构，文章厚度，行文指南。是你重写上一个草稿 01-article-draft-2.md 的重要参考。
目标：文章深度，维度，厚度，明显提升。 
不可为凑字数一味增加一些和主线内容偏离较大的内容，附录，习题集等
不可为凑字数一味增加一些和主线内容偏离较大的内容，附录，习题集等
不可为凑字数一味增加一些和主线内容偏离较大的内容，附录，习题集等

阅读todo完成后，
对照竞品文章模版，对原草稿进行深度展开，内容扩展
对照竞品文章模版，对原草稿进行深度展开，内容扩展
- `/reports 待发文章/YYYY-MM-DD-{topic}/01-article-draft-3.md`

验证：
写完后，对比 01-article-draft-2.md 01-article-draft-3.md ，直接输出二者的size，字节数，进行比较。看看size 大小是否有增加30%，如果没有，重新再写。
写完后，对比 01-article-draft-2.md 01-article-draft-3.md ，直接输出二者的size，字节数，进行比较。看看size 大小是否有增加30%，如果没有，重新再写。

第6步结束，重新查看thumbnail.md（文档随时变更，每次完成一步查看一次），确认自己执行到哪一步，下一步是什么。
然后输出一下自己的进度，完成了什么，下一步做什么。然后进入下一步。



### 第7步，调整部分过于AI化，模版化，结构化的描述。进行详细化，人性化的修改
重要：文章子模块中的观点描述，切勿过于结构化，看起来像AI写的文章，要更人性的描述文本。
先完整看一遍 01-article-draft-3.md ， 输出你认为过于AI化，结构化的部分，
然后列出方案，如何针对性调整。
然后实施修改，
对原来过于AI化，模版化，结构化的写法进行调整，换成几段详细的描述来表达，不可删减内容或增加新内容，只能把原来的内容换一种说法。
同一个文案结构反复使用，一定要修改，避免它出现。



反面教材如下：
1）问题钩子（知识/答案类）
**适用：**用来回答一个尖锐、明确的问题。
**避免：**已经尘埃落定的新闻（不需要制造悬念的那种）。
**构图：**画面中心放短文本；背景干净；对比强烈。

问题钩子 — 示例
2）前 / 后（改造/测试/教程类）
**适用：**变化和结果一眼能看出来的内容。
**避免：**差异太细微、乍看读不出来的对比。
**构图：**左右分屏或上下分屏；标签尽量少且简短。
前/后 — 示例

3）对比（评测/替代方案类）
**适用：**两个可直接比较的产品或方法。
**避免：**完全不同维度、硬拉在一起的对比（“苹果对橘子”）。
**构图：**两侧主体对称摆放；中间用低调的“VS”连接。

上面反例都是 适用、 避免 、 构图 ，千篇一律
上面反例都是 适用、 避免 、 构图 ，千篇一律

下面是调整上述反面教材后，正确的写法：
1 我们不把案例写成“表格/清单”，而是讲清楚每一次选择背后的理由。等你做图时，只需把这里的思路翻译成画面即可。
案例一：疑问钩子，先把“问题”做成主角。
大多数新手的困惑都很具体——比如“字幕怎么加？”。这类主题不需要复杂构图，也不需要堆满图标。一个干净背景，中间三四个字的问句，已经足够。是否加入人像？我们更倾向于先做一版“无人物”的极简稿：问句更大，边距更宽，手机上一眼读完。如果你的视频本身带有鲜明人设，再做一版“半身侧脸看向问句”的版本。两版放到手机里来回切换，你会很快知道哪一版更像“答案”。关键不在于字有多酷，而在于“答案感”是否直接、干净。

2 疑问钩子示意
案例二：前后对比，比的是“看得见的变化”。
我们做过许多“改造类”视频的封面，最后发现决定成败的不是字体或滤镜，而是两边是否“可比”。光线和白平衡必须一致，构图尽量镜像；分割线可以很细，只要两侧的“差异点”靠近分割线，观众就能自动对齐。如果变化幅度不够，宁可不用“Before/After”，换成“结果特写”都比“硬凑对比”可靠。对比图最怕两个问题：差异不明显、或者差异来自“非内容因素”（例如颜色偏移）。解决它们，才谈得上点击率。

3 前后对比示意
案例三：VS 对比，不要在封面里宣布胜负。
当我们在两种方案之间做抉择（两款剪辑软件、手机剪辑 vs 桌面剪辑），最有效的封面往往是“中性但强烈”的：左右对称的两位选手，中间一个很克制的“VS”，下方各一两个词提示差异（“更快”“更稳”之类）。把结论留给视频本身，封面的任务是“让人愿意看过程”。如果你把“赢家”写在图上，观众往往会预判内容——这不是对比，而是“剧透”。好看的对比封面，是邀请观众参与判断，而不是替他判断。


验证目标：
写完后，对比 01-article-draft-3.md 01-article-draft-4.md ，直接输出二者的size，字节数，进行比较。看看size 大小是否有增加，如果没有，重新再写。
记得，以01-article-draft-3.md 为基础，再继续修改。

- `/reports 待发文章/YYYY-MM-DD-{topic}/01-article-draft-4.md`


这里停止，第7步结束，重新查看thumbnail.md（文档随时变更，每次完成一步查看一次），确认自己执行到哪一步，下一步是什么。
这里停止，第7步结束，重新查看thumbnail.md（文档随时变更，每次完成一步查看一次），确认自己执行到哪一步，下一步是什么。
用户说继续后才能进入下一步

### 第8步，清理debug文案，更新错误链接。 
严格执行：
1  清理 01-article-draft-4.md 文中的debug文案
2  thumbnail 所有导流，链接统一换成： https://alici.ai/youtube-thumbnail  ， 而不是  https://app.alici.ai/ ,
3  生成
- `/reports 待发文章/YYYY-MM-DD-{topic}/01-article-draft-5.md`

### 第9步，执行AEO 评分检测
目标，达到75分以上，
没有达到，修改blog，如此反复。

### 第10步，  文中配图环节 
10.1
注意，优先使用 source/  中的来源网页配图
先查看一遍source/ 中所有的图片，全部用文字描述出图片内容，列出来给用户，
然后提出一版配图方案，对应之前规划的占位，列出来给用户，让用户选择。
使用source/  图片，可以上传到 cdn获得云端链接，后续使用

10.2
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
查看 /skills/utilities/blog-cover-generator/SKILL.md  了解封面的要求，prompt的要求
请使用英语prompt，生成最终版的英文内容图片。





### 第12步，生成预览网页和json
然后基于01-article-draft-5.md，生成 framer.json 和 preview.html
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


