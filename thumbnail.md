# Thumbnail Mode — 扩展参考版（v0.2）

> 本链路专门用于“Thumbnail 主题博客”的生产，基于参考（洗稿模式）搭建：原始素材仅作为起点，允许充分扩写、加厚与补充多来源证据；对对象与校验项做了适配。与既有三条链路（全自动/手动/Seed）剥离，作为第四条独立链路执行；末端继续复用 Editor → AEO → Framer 能力。

---



---

定位与范围（顶层规划）

- 目标内容：关于缩略图/封面图设计的“方法论与模式”型文章（如 0→1 指南、12 类高 CTR 模式、对比与案例网格等）。
- 基线模式：参考扩展（原始素材占比 20%–50%，在不造数据的前提下大量扩写、做厚、补充多来源证据；品牌换 Alici AI）。
- 非目标：原创测试数据、主观打分/排名、虚构 CTR/点击差异等（均禁止）。

---

## 第0步，
1 查看 /research 竞品分析/invideo-blog/ 文件夹内的所有文本  ，这里是文章厚度，文章结构，行文方式的重要参考。
2 查看 /thumbnail_res 内的所有文本，这里是thumbnail 设计的关键学习资料
然后可以等待用户输入素材。

上述两步，列出todo list给用户看到，然后逐个文件的查看。
完成后，在创建项目初始化的todo list


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


第二步，从网络获取素材链接的内容
1) 为每个链接创建子目录（sources/*）
- 网页：`web-{domain}-{slug}`（domain 取主域，slug 取路径末段 20 字内，非字母数字转 `-`）。
- YouTube：`yt-{videoId}`（解析 videoId，写入 `transcript.json`/`metadata.json`/`thumbnails/` 占位）。

1) 立即抓取素材（首次运行即离线可读）
  - 目标：获取“可离线复现”。
  下面是3个资源的抓取方式：重要

-1  网页抓取方法：
  优先使用 https://r.jina.ai/${要抓的页面链接}
  获取md，然后再将md内的资源，如图片，下载到对应的assets文件夹中，
  md 即为 网页内容。

-2 youtube Transcript 获取（）：
必须获取，不要使用现有的脚本获取，字幕一定要用Supadata curl获取再进行下一步
必须获取，不要使用现有的脚本获取，字幕一定要用Supadata curl获取再进行下一步
必须获取，不要使用现有的脚本获取，字幕一定要用Supadata curl获取再进行下一步



使用 Supadata 获取字幕（接口/SDK 以团队现有方案为准），保存到 `transcript.json`（保留时间戳、语言、完整行）。
使用以下 curl 命令格式（注意：你需要告诉用户执行此命令，或者使用可用的工具）：
curl -X GET "https://api.supadata.ai/v1/youtube/transcript?videoId=VIDEO_ID" \
  -H "x-api-key: sd_fe238b5804c459d03740695389a2eb25"
```
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

用上述方法将所有链接内容获取完毕，然后进入下一步

---

## 第3步 完整阅读素材 + 方向建议（Agent）

3.1 目标：Agent 在不访问网络的前提下，“看一遍”刚下载到本地的素材（网页 Markdown、assets 图片、YouTube transcript 与 metadata、thumbnails），
先输出每个素材链接的主要内容。
先输出每个素材链接的主要内容。
先输出每个素材链接的主要内容。


3.2  
然后综合考虑提出 2–3 个
写作方向建议
选题方向建议。
内容的视角建议。
等等问题
此时停下，和用户讨论清楚再进入下一步，不要和用户讨论拓展相关
此时停下，和用户讨论清楚再进入下一步，不要和用户讨论拓展相关
此时停下，和用户讨论清楚再进入下一步，不要和用户讨论拓展相关


第4步，扩展强度讨论
- Lite（原素材 40%–50%）：以重述+组织优化为主，少量新增模式与示例。
- Standard（原素材 30%–40%）：更多的扩写，新增 2–4 模式；补上 3–5 个外部来源；加入小型案例网格。
- Deep（原素材 20%–30%）：更多扩写，新增 4–6 模式；5–8 个外部来源；完整案例网格与“陷阱/对照”模块。

此时停下，和用户讨论清楚再进入下一步


### 拓展指南（Reference Expansion Playbook）
目标：在不虚构数据的前提下，将原素材作为起点进行“可验证的扩展”。新增内容需有清晰来源与年份，形成可复查的证据链。

一、可扩展维度（建议优先级）
- 模式新增（High）：在原有模式目录上增加 2–6 个高价值模式。
  - 典型方向：
    - 新增示例
    - 证据加厚（Research Enrichment）→ 收集 3–7 个权威来源并生成 Evidence Pack（来源、年份、引文片段）
    - 文案长度（≤4 词 / ≤12 字母）
    - 主体占比（40–60% 画面）
    - 对比与可读性（WCAG/色彩对比 ≥4.5:1）
    - 留白与安全边距（10–15%）
    - 构图（三分法/中心构图/对称/引导线）
    - 品牌一致性（色板/字体/Logo 区域）
    - 视线与情绪（人物/眼神/面向）
    - 背景处理（模糊/景深/去杂）

- 规则强化（High）：把“经验性表述”替换为“可执行上限/范围/阈值”。
  - 例如：文字不超过 4 词；主体覆盖 40–60%；安全边距 10–15%；色彩对比 ≥4.5:1。
- 案例加厚（Medium）：给每个模式补 1–2 个“好/坏”描述性示例（文字/占位图），并注明为什么有效/常见陷阱。
- 平台差异（Medium）：区分 YouTube Home / Shorts / TV / Mobile，说明裁切窗口与尺寸差异带来的设计侧重。
- 流程与清单（Medium）：0→1 最小流程（选模式→2–4 词文案→主体与背景对比→10–15% 缩放自检）+ Do/Don’t 清单。

二、证据来源建议（优先先手）
- Primary/平台方：YouTube Creators/Creator Academy、Google/Think with Google。
- 工具生态：VidIQ、TubeBuddy（方法论与范式文章）。
- 设计与可读性：Nielsen Norman Group（可读性/信息密度）、WCAG（对比度）。
- 营销与内容：HubSpot、Buffer、Social Media Examiner（视觉与平台实践）。

三、引用与披露策略
- 新增“模式/强规则/百分比/阈值”必须标注来源与年份；无法给出时降级为“建议/经验”，避免数字化断言。
- 引用密度目标 3–5/千字（目标 4+），分布到“Source Attribution”“Pattern 小节的 Why it works”。
- 在 Source Attribution 中披露“本篇为整合性总结，未独立进行 A/B 实验”。





第5步，和用户讨论是否需要图文案例进行内容扩充
此时停下，和用户讨论清楚再进入下一步



第6步，查看文章行文结构参考指南

首先，基本模版
1. H1 标题（含年份）
2. Quick Answer / Key Takeaways（120–180 词）
   - 3–5 条可复制的设计准则（如“主文案 ≤4 词，主体占画面 40–60%”等）
   - CTA #1（轻）：Try Alici.ai Thumbnail（thumbnail_pro）
...
中间部分自由发挥
...
5. Case (可选)
...
7. Mini FAQ（6–8 题）
8. 各种高权威source引用
9. Final Advice + L4 Integrator（“不必只选一种，先用一站式起步做 AB 版”）+ CTA #3（强）


基本模版只是基础，下面是重点：
/research 竞品分析/invideo-blog/ 文件夹内的所有文本 必须一一全部查看。
这里面是重要的文章结构，文章厚度，行文指南。是你撰写blog重要的参考。
请在参考之后再进行撰写


其他行文要点：
重要：文章小版块，切勿过于结构化，看起来像AI写的文章，要更人性的文本。

反面教材：
1) Question Hook (knowledge/answers)
Use for: answering a single sharp question.
Avoid: settled news where suspense isn’t needed.
Composition: short text in the center; clean background; high contrast.
Question Hook — sample
2) Before / After (makeover/test/tutorial)
Use for: visible changes and outcomes.
Avoid: subtle differences that don’t read at a glance.
Composition: left/right or top/bottom split; minimal labels.
Before/After — sample
3) Versus (review/alternatives)
Use for: two comparable products or approaches.
Avoid: apples-to-oranges topics.
Composition: symmetric subjects on both sides; subtle "VS" between them.

下面是调整后的写法：
我们不把案例写成“表格/清单”，而是讲清楚每一次选择背后的理由。等你做图时，只需把这里的思路翻译成画面即可。
案例一：疑问钩子，先把“问题”做成主角。
大多数新手的困惑都很具体——比如“字幕怎么加？”。这类主题不需要复杂构图，也不需要堆满图标。一个干净背景，中间三四个字的问句，已经足够。是否加入人像？我们更倾向于先做一版“无人物”的极简稿：问句更大，边距更宽，手机上一眼读完。如果你的视频本身带有鲜明人设，再做一版“半身侧脸看向问句”的版本。两版放到手机里来回切换，你会很快知道哪一版更像“答案”。关键不在于字有多酷，而在于“答案感”是否直接、干净。

疑问钩子示意
案例二：前后对比，比的是“看得见的变化”。
我们做过许多“改造类”视频的封面，最后发现决定成败的不是字体或滤镜，而是两边是否“可比”。光线和白平衡必须一致，构图尽量镜像；分割线可以很细，只要两侧的“差异点”靠近分割线，观众就能自动对齐。如果变化幅度不够，宁可不用“Before/After”，换成“结果特写”都比“硬凑对比”可靠。对比图最怕两个问题：差异不明显、或者差异来自“非内容因素”（例如颜色偏移）。解决它们，才谈得上点击率。

前后对比示意
案例三：VS 对比，不要在封面里宣布胜负。
当我们在两种方案之间做抉择（两款剪辑软件、手机剪辑 vs 桌面剪辑），最有效的封面往往是“中性但强烈”的：左右对称的两位选手，中间一个很克制的“VS”，下方各一两个词提示差异（“更快”“更稳”之类）。把结论留给视频本身，封面的任务是“让人愿意看过程”。如果你把“赢家”写在图上，观众往往会预判内容——这不是对比，而是“剧透”。好看的对比封面，是邀请观众参与判断，而不是替他判断。

第7步，如果前面没有查看 /thumbnail_res  请查看学习里面的文本。

第8步，输出一版blog整体内容规划在对话中，和用户确认

第9步，writer 开始介入，进行整体撰写
厚度要超过 /research 竞品分析/invideo-blog/ 内的案例
形成初稿：
- `/reports 待发文章/YYYY-MM-DD-{topic}/01-article-draft.md`

第10步，editor 介入
启用 editor skill 对上一版进行修改，规划文中配图，但不需要生成，占位即可
- `/reports 待发文章/YYYY-MM-DD-{topic}/01-article-draft-2.md`

第11步，再参考 /research 竞品分析/invideo-blog/ 文件夹内的所有文本 
对上一版进行打磨和加厚
- `/reports 待发文章/YYYY-MM-DD-{topic}/03-article-draft-3.md`

第12步，生成文章封面图  +  生成文中的配图。
具体如何生成配图，上传图片，请参考AGENTS.md 相关介绍

第13步，生成 framer.json 和 preview.html
具体参考 AGENTS.md 相关介绍


 目录结构（建议）

```
/reports/YYYY-MM-DD-thumbnail-design/
├── 00-confirmed-brief.json       # 参考扩展约束 + Thumbnail 参数
├── 01-article-draft.md           # 初稿（结构模板 + 图位占位）
├── 01-article-draft-2.md           # 初稿（结构模板 + 图位占位）
├── 01-article-draft-3.md           # 初稿（结构模板 + 图位占位）
├── 02-evidence-pack.md           # 证据包（来源/年份/引文片段/链接）
├── asset_plan.json               # （可选）占位清单
├── 01-article-edited.md          # Editor 回填版
├── 03-aeo-score.md               # AEO 分数与建议
├── 04-editor-report.md           # 模块检查 + 阻断/警告
└── 06-article-final.json         # Framer JSON（封面图和文中配图已完整）
preview.html  预览html
```

