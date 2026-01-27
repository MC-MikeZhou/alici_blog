# 功能更新：convert-to-video-framer-json（视频集成）

日期：2026-01-27
负责人：AliciBlog 团队

## 摘要

在现有 Framer JSON 基础上新增“视频集成”可选环节（严格、非破坏）。工具以交互方式收集云端视频链接，确认插入位置，将正文拆分为多段，并输出符合 `blog_scheme_example.json` 与 `FIELD_SCHEMA.md` 的新文件：输入名追加 `-video.json`。

该功能不会修改或覆盖原 JSON，只会新增一个“输入名 + `-video.json`”的文件。

## 背景/动机

- 满足可选的视频嵌入需求，不改 HTML，不注入组件。
- 与 Framer CMS 的字段/结构保持一致，遵循 example/schema。
- 作为显式的后处理步骤，按需执行，保证安全可控。

## 关键行为（STRICT）

- 输入：必须是 Framer JSON（数组，单对象），且 `article_body_content` 为有效 Framer HTML。
- 输出：与输入同目录，文件名在原名基础上追加 `-video`（如：`06-article-final-video.json`）。
- 禁止：不注入 `<iframe>`/`<video>`，不输出 `video_embeds` 数组。
- 字段：保留源 JSON 的全部字段和值（逐字复制），值只能来自源 JSON。
- 校验：`blog_scheme_example.json`/`FIELD_SCHEMA.md` 仅用于“字段名/结构校验”。若 example 中的字段在源 JSON 中不存在（且不是视频阶段新增字段），则直接中止，绝不使用示例默认值或空值补齐。
- 仅允许新增的“视频阶段字段”：
  - `video_link_1..5`
  - `article_body_content_2..5`
- 未使用的槽位允许使用空字符串占位，以匹配 example 的布局。

## 段落与插入位映射

- 段落字段：
  - 段1 → `article_body_content`
  - 段2 → `article_body_content_2`
  - 段3 → `article_body_content_3`
  - 依此类推（最多至 `_5`）

- 视频插入字段（按“段间”定义）：
  - `video_link_1` → 在“正文顶部”（`article_body_content` 之前）
  - `video_link_2` → 段1 与 段2 之间
  - `video_link_3` → 段2 与 段3 之间
  - `video_link_4` → 段3 与 段4 之间
  - `video_link_5` → 段4 与 段5 之间

示例：若要“在第三段之前”插入视频，应填写 `video_link_3`。

## 使用方法

1) 准备输入（Framer JSON）：如 `reports/.../06-article-final.json`
2) 准备视频链接：
   - 将云端链接写入 `/video_resources/video_links.txt`（分隔符：换行/空格/英文逗号/中文逗号）。
   - 如有本地视频，请先“手动”用与图片一致的方式（rsync）上传到 CDN，然后粘贴生成的 CDN 链接。
3) 运行转换：

```bash
python scripts/convert_to_video_json/interactive_convert.py \
  --input reports/.../06-article-final.json
```

4) 工具将：
   - 展示“视频链接列表（列表 A）”与“文章段落预览（列表 B，按 H2 拆分并显示段首摘要）”。
   - 询问每个视频的插入位置：“0=正文顶部”或“插入到第 K 段之前（K=1..N）”。
   - 生成写入前确认单（明确 `video_link_N` 映射）。
   - 输出 `*-video.json`（数组，单对象）。

## 手动上传（视频）

- 将 `/video_resources/` 下本地视频用 rsync 上传至 CDN（与图片一致，仅目录不同）：

```bash
rsync -avz --progress ./video_resources/ \
  root@<YOUR_SERVER_IP>:/var/www/static/static/video/other/gen_videos/
```

- 公网 URL 示例：
  - `https://ct2.alici.ai/static/video/other/gen_videos/<file>`
- 将生成的 CDN 链接写入 `video_links.txt` 或在交互中直接粘贴。

## 工具与文档

- Skill（必读）：`skills/utilities/convert-to-video-framer-json/SKILL.md`
- Example（必读）：`skills/utilities/convert-to-video-framer-json/blog_scheme_example.json`
- Schema：`skills/utilities/convert-to-video-framer-json/FIELD_SCHEMA.md`（已补充缺失字段，严格值来源规则）
- 转换规则（Framer HTML）：`skills/utilities/convert-to-video-framer-json/CONVERSION_RULES.md`
- 交互脚本：`scripts/convert_to_video_json/interactive_convert.py`

代理路由（非写作意图）：
- `CLAUDE.md` 与 `AGENTS.md` 已加入命令：`/convert-to-video-framer-json <path/to/06-article-final.json>`
- 附带成功/失败反馈模板，以及“视频列表+段落预览”的交互提示。

## 行为变更

- 移除上传脚本依赖：交互工具不再调用任何上传脚本；视频上传改为手动。
- 文档中关于 `scripts/convert_to_video_json/upload_videos.py` 的引用统一改为手动 rsync 说明。
- 交互行为修正：按“分段顺序”分配 `video_link_N`（非输入顺序）；`video_link_1` 专用于“正文顶部”。
- 输出稳态：确保存在 `article_body_content_2..5` 与 `video_link_1..5`（未用则为空字符串）。

## 已知约束

- 输入正文必须是 Framer HTML；若疑似 Markdown，请先进行“convert-to-framer”。
- 最多 5 个视频槽位（顶部 1 个 + 正文内最多 4 个），与 example 对齐。
- 若 example 中字段在源 JSON 缺失（且不是视频阶段新增字段），将直接中止并列出缺失字段。

## 示例会话（简版）

```
🎬 Convert-to-Video Framer JSON (interactive)
Article: How to Make Your Product Go Viral…

🔗 待插入视频：
  1) https://ct2.alici.ai/static/video/other/gen_videos/clip-01.mp4
  2) https://www.youtube.com/watch?v=XxYyZzAaBbC (start=75s)

🧩 文章段落（按 H2 拆分）：
  段1: The competition for attention in 2026 is fierce. Pro...
  段2: 2. The Power of Presets: Your Shortcut to Visual Ident...
  段3: 3. From Concept to Video: How the Process Works — Crea...

选择：video #1 → 0（正文顶部）
选择：video #2 → 3（第三段之前）

📋 确认计划：
  - https://ct2.../clip-01.mp4 @ 正文顶部 → video_link_1
  - https://www.youtube.com/watch?v=... @ 第三段之前 → video_link_3

✅ 生成成功：reports/.../06-article-final-video.json
```

## 回滚/安全

- 非破坏性：原 JSON 不改动。
- 需要重试时，删除已生成的 `*-video.json` 重新运行即可。

## 团队检查清单

- [ ] 使用前阅读：SKILL.md、FIELD_SCHEMA.md、blog_scheme_example.json
- [ ] 确认输入为 Framer JSON（数组 + `article_body_content` 为 HTML）
- [ ] 准备 CDN 链接（先手动上传），写入 `video_links.txt` 或在交互中粘贴
- [ ] 在确认单中核对：视频 ↔ `video_link_N` ↔ 段间关系
- [ ] 对照 example 校验最终 `*-video.json` 字段齐全且值来自源 JSON
