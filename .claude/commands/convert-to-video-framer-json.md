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
5. 生成输出（非破坏，STRICT 不注入 HTML）：
   - 正文拆分：`article_body_content`（第一段）、`article_body_content_2..N`（后续段）
   - 视频链接：`video_link_1..N`（按插入顺序；若选择“正文前”，`video_link_1` 表示 Before Body）
   - 输出文件名：在输入 JSON 文件名基础上追加 `-video` 后缀，例如：
     - `06-article-final.json` → `06-article-final-video.json`
     - `06-article-final-v2.3.json` → `06-article-final-v2.3-video.json`

6. 字段校验（STRICT）：
   - 输出字段 = 源 JSON 字段 ∪ example.json 字段（仅用于字段清单校验）
   - example 中的每个字段，必须从源 JSON 获取对应值（大小写/分隔差异允许映射）
   - 禁止用 example 的默认值或任意填充值；如缺字段则阻断并提示

## Non-Destructive Guarantee

- 绝不修改或覆盖原始 `framer.json`
- 仅在同目录新增 `*-video.json`
- 若用户显式指定 `--output` 为原文件名，将拒绝执行

## Related

- Skill: `skills/utilities/convert-to-video-framer-json/SKILL.md`
- Scripts:
  - `scripts/convert_to_video_json/interactive_convert.py`
  - `scripts/convert_to_video_json/upload_videos.py`
