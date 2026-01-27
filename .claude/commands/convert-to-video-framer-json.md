# Convert to Video Framer JSON (v0.9)

> 在既有 Framer JSON 基础上，按用户需求插入视频（最多 5 个：正文前 1 个 + 正文内最多 4 个），生成输入名 + `-video.json`，不改动原文件。

## Usage

```
/convert-to-video-framer-json /reports/[date]-[topic]/06-article-final.json
```

或在完整工作流末尾由系统询问后自动调用：

```
Phase 6: /convert-to-framer → 06-article-final.json
Phase 7: (可选) /convert-to-video-framer-json 06-article-final.json
```

## What This Command Does

1. 读取既有 Framer JSON（数组格式，首个元素为文章）
2. 解析 `/video_resources/video_links.txt`：
   - 分隔符：换行 / 空格 / 英文逗号（`,`)；支持混排
   - 自动提取链接末尾的时间参数（`?t=75s`、`start=75`、`#t=1:15` 等）
   - 同行描述中的时间提示（`start: 1:23`、`at 90s`）也会识别
3. 可选上传本地视频：
   - `/video_resources` 下的本地视频（`.mp4/.webm/.mov/.mkv`）通过 rsync 上传到 CDN
   - 复制打印出的 CDN 链接并粘贴回 CLI
4. 选择插入位置：
   - 默认支持 1 个“正文之前”视频
   - 正文内最多 4 个“在第 N 个 H2 前”插入点（H2 为 `<h6><strong>`）
   - 输出插入计划供用户确认
5. 生成输出（非破坏）：
   - 合并正文：`article_body_content`（注入 `<div class="video-embed">…</div>`）
   - 分段数组：`article_body_content_parts`（html / video 块）
   - 元数据：`video_embeds`（url/type/position/start）
   - 输出文件名：在输入 JSON 文件名基础上追加 `-video` 后缀，例如：
     - `06-article-final.json` → `06-article-final-video.json`
     - `06-article-final-v2.3.json` → `06-article-final-v2.3-video.json`

## Non-Destructive Guarantee

- 绝不修改或覆盖原始 `framer.json`
- 仅在同目录新增 `*-video.json`
- 若用户显式指定 `--output` 为原文件名，将拒绝执行

## Related

- Skill: `skills/utilities/convert-to-video-framer-json/SKILL.md`
- Scripts:
  - `scripts/convert_to_video_json/interactive_convert.py`
  - `scripts/convert_to_video_json/upload_videos.py`

