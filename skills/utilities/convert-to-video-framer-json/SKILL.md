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

> 在既有 `framer.json` 基础上，按用户需求插入视频（最多 5 个：正文前 1 个 + 正文内最多 4 个），生成“输入名 + `-video.json`”。

> 非破坏性（Non-Destructive）保证：本 Skill 绝不会修改或覆盖任何已有输出（如 `06-article-final.json`）。只会新增一个以输入文件名为基础、追加 `-video` 后缀的 JSON 文件。

## 前置条件
- 必读：`skills/utilities/convert-to-video-framer-json/blog_scheme_example.json`
- 参考：`skills/utilities/convert-to-video-framer-json/FIELD_SCHEMA.md`
- 参考：`skills/utilities/convert-to-video-framer-json/CONVERSION_RULES.md`
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
   - 不注入任何 `<iframe>` / `<video>` 标记，不改写正文 HTML
   - 仅基于“插入点”把正文拆散为多段：第一段写入 `article_body_content`；后续段依次写入 `article_body_content_2`、`article_body_content_3` ...
   - 依序写入视频链接字段：`video_link_1`、`video_link_2`、...
   - 其余字段保持与输入 JSON 一致，不做改动

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

包含字段（STRICT）：
- `article_body_content`（正文第一段）
- `article_body_content_2..N`（正文后续段）
- `video_link_1..N`（对应每个插入点的视频链接，已上传 CDN 或云端链接）

禁止输出（STRICT）：
- 不输出 `video_embeds`、`article_body_content_parts`、`article_body_content_html_injected` 等任何额外字段
- 不输出任何 `<iframe>` / `<video>` HTML 片段到正文

## 注意事项

- 本 Skill 不产生任何 HTML 组件（不插入 `<iframe>` 或 `<video>`），仅输出结构化的多段正文与视频链接字段，便于下游按 `blog_scheme_example.json` 的注释完成落版。
- 如检测到代理尝试添加 `video_embeds` 数组或 HTML 注入，视为不符合规范，应回退并改用本 Skill 输出的 `*-video.json`。

### 例规（必须先看 example）

- 在运行本 Skill 之前，必须打开并通读：
  - `skills/utilities/convert-to-video-framer-json/blog_scheme_example.json`
- 任何情况下，输出字段集应等于：`源 JSON 字段 ∪ example.json 字段`（同名字段以 example 的字段名为准、值来自源 JSON）。
- 如加载 example 失败或检测到关键字段缺失，应“阻断并提示”，不得输出不完整的 `*-video.json`。

### 字段保留与校验（IMPORTANT）

- 保留源 JSON 的所有字段（逐字复制，除正文拆分外不改动原值）
- 按 `blog_scheme_example.json` 对“字段清单”做校验：
  - 仅使用“源 JSON 中的同名/同义字段值”来满足 example 的字段（大小写或分隔差异允许）
  - 严禁使用 example 的示例默认值或任意填充值
  - 若 example 中的字段在源 JSON 中不存在（无法映射），应“阻断并提示”，不得输出不完整的 `*-video.json`
- `Slug/slug`、`Date/date` 等大小写或分隔差异：按 example 字段名输出，但取值只能来源于源 JSON 的等价字段（大小写不一致也会匹配）

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
