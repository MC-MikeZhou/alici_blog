---
name: smart-segmenter
version: "1.0"
type: skill
provides: video-scene-segmentation
dependencies:
  - tool: Bash (ffmpeg, python3)
  - script: scripts/segment.py
  - optional: GEMINI_API_KEY (for --deep mode)
  - optional: yt-dlp (for YouTube cutting)
description: >
  Smart Segmenter v1.0 - 视频场景分段 + YouTube 精确裁剪。
  输入视频文件 → PySceneDetect 转场检测 + 静音检测 + (可选) Gemini 语义分析
  → 输出 segments.json 场景边界。附带 YouTube 精确裁剪标准流程。
allowed-tools: Bash, Read, Write
metadata:
  author: Lucy (MVP) + H (integration)
  created: 2026-04-03
  origin: /Who is Lucy/smart-segmenter-skill/ (PRD v2.0)
  complementary: skills/preparation/video-understanding/SKILL.md
triggers:
  - "segment video"
  - "视频分段"
  - "scene detection"
  - "场景检测"
  - "smart segmenter"
  - "cut youtube"
  - "剪切 YouTube"
  - "YouTube 精确剪切"
  - "youtube clip"
  - "裁剪视频"
---

# Smart Segmenter v1.0

## Purpose

两大能力：

1. **场景分段** — 自动识别视频中的场景边界，输出带时间码 + 情感标签 + 叙事角色的 segments.json
2. **YouTube 精确裁剪** — 从长视频中定位并精确剪出目标片段的标准化流程

**与 video-understanding 的关系**：互补，不重叠。
- **smart-segmenter** 回答 "*where* — 场景边界在哪？"
- **video-understanding** 回答 "*what* — 视频里有什么？"
- 组合使用：先 segmenter 分段定位 → 再 understanding 分析选中片段内容

---

## Capability A: Scene Segmentation

### Input

| 参数 | 必需 | 说明 |
|------|------|------|
| `video_path` | Yes | 视频文件绝对路径 |
| `--fast` | 默认 | PySceneDetect + 静音检测（本地，$0） |
| `--deep` | 可选 | + Gemini 语义分析（需 GEMINI_API_KEY） |

### Execution

```bash
# Fast mode: 视觉转场 + 静音检测（推荐起步）
python3 scripts/segment.py --input <video.mp4> --output segments.json --fast

# Deep mode: + Gemini 语义理解（情感/叙事标签更丰富）
export GEMINI_API_KEY="..."
python3 scripts/segment.py --input <video.mp4> --output segments.json --deep
```

### Output: segments.json

```json
{
  "version": "1.0",
  "source": {
    "file": "video.mp4",
    "duration_s": 76.0,
    "fps": 30.0,
    "resolution": "1080x1920"
  },
  "segments": [
    {
      "id": "seg_01",
      "start": { "time_s": 0.0, "frame": 0 },
      "end": { "time_s": 14.8, "frame": 444 },
      "duration_s": 14.8,
      "label": "Opening Scene",
      "description": "...",
      "emotion": "shock",
      "narrative_role": "hook",
      "confidence": 0.92
    }
  ]
}
```

`--fast` 模式输出基础边界 + label；`--deep` 模式额外填充 emotion、narrative_role、dialogue summary 等语义字段。

---

## Capability B: YouTube 精确裁剪流程

从长 YouTube 视频中精确剪出目标片段的标准化 7 步流程。

### B1: 下载源视频

```bash
yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]" \
  --cookies-from-browser chrome \
  -o "source.mp4" \
  "<YOUTUBE_URL>"
```

### B2: 全局扫描定位

```bash
python3 scripts/segment.py --input source.mp4 --output segments.json --fast
```

查看输出的 segments.json，每个 segment 有 label 和时间范围。

### B3: 审查定位目标

读取 segments.json，根据 label/description/时间范围确认目标片段。

如果 `--fast` 的 label 不够精确（如多个 segment 描述模糊）：

### B4: (可选) Deep 语义标签

```bash
python3 scripts/segment.py --input source.mp4 --output segments_deep.json --deep
```

Gemini 会给出更详细的内容描述和情感标签，帮助精确定位。

### B5: 计算精确时间戳

从 segments.json 中获取目标 segment 的 `start.time_s` 和 `end.time_s`，计算 duration：

```
start = segment.start.time_s
duration = segment.end.time_s - segment.start.time_s
```

如果目标跨越多个 segment，取首个的 start 和末尾的 end。

### B6: FFmpeg 精确剪切

```bash
ffmpeg -ss <start> -t <duration> -i source.mp4 -c copy output_clip.mp4
```

注意：`-c copy` 无损但可能在非关键帧处有几帧不准。如需帧级精确：

```bash
ffmpeg -ss <start> -t <duration> -i source.mp4 \
  -c:v libx264 -crf 18 -c:a aac output_clip.mp4
```

### B7: 抽帧验证

```bash
ffmpeg -i output_clip.mp4 -vf "select=eq(n\,0)" -frames:v 1 /tmp/verify_first.png
ffmpeg -i output_clip.mp4 -sseof -0.5 -frames:v 1 /tmp/verify_last.png
```

用 Read 工具查看首帧和末帧，确认裁剪准确。

---

## Error Handling

| 场景 | 处理 |
|------|------|
| ffmpeg 未安装 | 提示 `brew install ffmpeg` |
| scenedetect 未安装 | 自动回退到 ffmpeg scene score 解析 |
| GEMINI_API_KEY 缺失 | `--deep` 模式警告并跳过语义分析，仅输出视觉+音频边界 |
| yt-dlp 未安装 | 提示 `brew install yt-dlp`（仅影响 YouTube 裁剪流程） |
| 视频文件不存在 | 报错退出 |
| 视频太短 (<2s) | 输出单 segment，标注 warning |

---

## Prerequisites

```bash
# 核心依赖
pip install scenedetect[opencv] google-genai

# YouTube 裁剪（可选）
brew install yt-dlp

# 系统工具（通常已有）
brew install ffmpeg
```

---

## Usage in Pipeline

```
写作流程中的视频处理:
  ├── smart-segmenter --fast  → 定位场景边界 / 裁剪目标片段
  ├── smart-segmenter --deep  → 语义标签（情感/叙事角色）
  └── video-understanding     → 内容理解 + 第一人称叙事转化
```

---

## Changelog

### v1.0 (2026-04-03)
- 从 Lucy 工作区 (`/Who is Lucy/smart-segmenter-skill/`) 迁入正式 skills
- 重写 SKILL.md，标准化触发词和执行流程
- 新增 Capability B: YouTube 精确裁剪标准化流程（7 步）
- segment.py 脚本原样保留（MVP: fast + deep 双模式）
