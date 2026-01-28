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
2. 解析 `video_links.txt`（位于输入 JSON 同目录）：
   - 分隔符：换行 / 空格 / 英文逗号（`,`)；支持混排
   - 自动提取链接末尾的时间参数（`?t=75s`、`start=75`、`#t=1:15` 等）
   - 同行描述中的时间提示（`start: 1:23`、`at 90s`）也会识别
3. 可选上传本地视频（位于输入 JSON 同目录）：
   - 将同目录下的本地视频（`.mp4/.webm/.mov/.mkv` 等）通过 rsync 上传到 CDN：
     - 示例：`rsync -a -r -v -p -e 'ssh -p 22' --exclude='.DS_Store' --progress <完整前置路径>/<name>.mp4 root@45.76.70.215:/var/www/static/static/image/other/`（密码：`5A_p@cjpX74H(LJM`）
     - 得到的 CDN 链接形如：`https://ct2.alici.ai/static/image/other/<name>.mp4`
   - 或手动粘贴任意云端视频链接
4. 列出可用视频与段落预览并选择插入位置：
   - 视频列表包含：`<输入 JSON 同目录>/video_links.txt` 中的链接 + 同目录本地视频 + 手动粘贴
   - 段落预览：按 H2 拆分为“段1..段N”，展示每段开头摘要
   - 必须经用户确认具体“使用哪个视频、插在第几段之前”；未确认不得默认插到正文顶部、也不得直接生成 JSON
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

## Resource Location（重要变更）

- 资源定位，与输入 Framer JSON 同目录”。
- 将 `video_links.txt` 和待上传的本地视频文件放在与 `06-article-final.json` 相同的目录。
- 可选参数：`--resources-dir` 指向输入 JSON 同目录（如未显式提供，交互流程会默认以输入 JSON 所在目录为资源目录）。

## Non-Destructive Guarantee

- 绝不修改或覆盖原始 `framer.json`
- 仅在同目录新增 `*-video.json`
- 若用户显式指定 `--output` 为原文件名，将拒绝执行

## Related

- Skill: `skills/utilities/convert-to-video-framer-json/SKILL.md`
- Scripts:
  - `scripts/convert_to_video_json/interactive_convert.py`
