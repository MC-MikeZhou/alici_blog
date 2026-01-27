---
name: convert-to-video-framer-json
version: "0.9"
type: skill
provides: framer-video-json-generation
allowed-tools: Read, Write, AskUserQuestion, Bash
description: >
  After standard Framer JSON is generated, interactively collect cloud video links
  (and upload local videos to CDN), confirm insertion points, and produce a
  video-enhanced JSON: 06-article-final-video.json.
triggers:
  - "/convert-to-video-framer-json"
  - "video framer json"
  - "嵌入视频 json"
  - "framer 视频"
metadata:
  author: AliciBlog Team
  updated: 2026-01-27
---

# Convert-to-Video Framer JSON Skill (v0.9)

> 在既有 `framer.json` 基础上，按用户需求插入视频（最多 5 个：正文前 1 个 + 正文内最多 4 个），生成 `06-article-final-video.json`。

> 非破坏性（Non-Destructive）保证：本 Skill 绝不会修改或覆盖任何已有输出（如 `06-article-final.json`）。只会新增一个以输入文件名为基础、追加 `-video` 后缀的 JSON 文件。

## 前置条件

- 已完成标准导出：`/convert-to-framer`（即已存在 `framer.json`，常见名如 `06-article-final.json`）
- 项目根目录存在 `/video_resources/` 目录：
  - `video_links.txt`（可能包含云端视频链接，原始文本，不保证可自动解析）
  - 本地视频文件（如 `.mp4`, `.webm`, `.mov` 等）

## 执行流程（交互式）

1) 确认是否需要插入视频（若否 → 结束）。
2) 采集视频资源：
   - 从 `video_resources/video_links.txt` 解析云端链接（分隔符：换行/空格/英文逗号），列出给用户确认
   - 支持手动追加/删减链接
   - 若存在本地视频，使用与图片一致的方式（rsync）上传到 CDN，获得可访问的云端链接
3) 选择插入位置：
   - 支持 1 个“正文之前”插入点（默认启用）
   - 支持正文内最多 4 个插入点（“在第 N 个 H2 前”或“在匹配到的文本前”）
   - 输出插入计划供用户二次确认
4) 生成 `*-video.json`（基于输入文件名追加 `-video`）：
   - 在原 `article_body_content` 基础上插入 `<div class="video-embed">…</div>` 块（YouTube 使用 `youtube-nocookie` 的 `<iframe>`；直链视频使用 `<video controls>`）
   - 同时输出 `article_body_content_parts`（数组）与 `video_embeds` 元数据，便于后续系统处理
   - 若需严格对齐 `blog_scheme_example.json`，在确认该 schema 后将本输出映射为对应多字段结构（例如将正文拆分为 `article_body_content_01/02/...` 等）

> 说明：若最终 CMS 需要严格遵循 `blog_scheme_example.json`，请在提供该 schema 后将本 Skill 的输出字段名与结构做一致化映射（当前版本同时提供合并后的字符串与分片结构，保证兼容）。

## 使用方法

```bash
# 交互式：从标准 JSON 生成视频版 JSON
python scripts/convert_to_video_json/interactive_convert.py \
  --input /reports/2026-01-26-sample/06-article-final.json

# 可选参数
# --resources-dir ./video_resources     # 默认使用仓库根的 /video_resources
# --output /reports/.../06-article-final-video.json  # 自定义输出路径
# --max-inline 4                        # 正文内最多4个
```

CDN 上传（本地视频）示例：
```bash
python scripts/convert_to_video_json/upload_videos.py --dir ./video_resources

# 环境变量（可选）
export CDN_SERVER_IP=45.76.70.215
export CDN_SERVER_USER=root
export CDN_VIDEO_REMOTE_PATH=/var/www/static/static/video/other/gen_videos/
export CDN_VIDEO_URL_PREFIX=https://ct2.alici.ai/static/video/other/gen_videos/
```

## 输出文件

位于原 JSON 同目录，命名规则：在输入 JSON 文件名基础上追加 `-video` 后缀。

示例：
- `06-article-final.json` → `06-article-final-video.json`
- `06-article-final-v2.3.json` → `06-article-final-v2.3-video.json`

包含字段：
- `article_body_content`（合并后的含视频块的 HTML）
- `article_body_content_parts`（数组：HTML 片段与视频块分段）
- `video_embeds`（数组：每个视频的 url、类型、插入位置说明）

## 插入块格式

- YouTube（无追踪域）：
```html
<div class="video-embed">
  <iframe src="https://www.youtube-nocookie.com/embed/{VIDEO_ID}?start={START_IN_SECONDS}"
          title="Video Walkthrough" frameborder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
          allowfullscreen></iframe>
</div>
```

- 直链视频（MP4/WebM）：
```html
<div class="video-embed">
  <video controls src="{CDN_VIDEO_URL}" playsinline></video>
  <!-- 可选 poster="{IMAGE_URL}" -->
  <!-- 可选 data-start="{START_IN_SECONDS}" -->
  
</div>
```

> 建议在预览模板或站点 CSS 中补充 `.video-embed { width:100%; aspect-ratio:16/9; }` 以保证显示效果。

## 与主流程的衔接（挂载点）

```
Track A/B/C → convert-to-framer (06-article-final.json)
           → [询问：是否需要插入视频?]
             ├─ 否 → 结束
             └─ 是 → convert-to-video-framer-json → 06-article-final-video.json
```

## 失败与回滚

- 任何一步失败或用户取消时，不修改原 `framer.json`；新文件不会生成
- 如需重试，重新运行本 Skill 并覆盖输出

## 非破坏性（Non-Destructive）保证

- 不修改：不修改/覆盖原始的 `framer.json` 或任何既有报告/产物
- 不重命名：不对现有文件进行移动/重命名操作
- 仅新增：只在同目录新增 `*-video.json`（输入名 + `-video` 后缀）
- 安全写入：如用户显式指定 `--output` 与输入文件相同，直接拒绝并提示（避免误覆盖）
