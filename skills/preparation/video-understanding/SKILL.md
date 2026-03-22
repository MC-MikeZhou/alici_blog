---
name: video-understanding
version: "1.0"
type: skill
provides: video-multimodal-analysis
dependencies:
  - tool: Bash (ffmpeg)
  - tool: Read (multimodal)
  - script: scripts/video_frame_extractor.py
description: >
  Video Understanding v1.0 - 视频多模态理解。
  输入视频文件路径 → FFmpeg 抽帧 → Claude 多模态视觉理解 → 输出结构化分析报告。
  用于 Route E Phase 2 素材深化，与 Lucy 的 Gemini pipeline 互补。
allowed-tools: Bash, Read, Write
metadata:
  author: H
  created: 2026-03-22
  route: "E (Formula-Driven)"
  complementary: "Lucy's video-understanding-pipeline-SKILL.md (Gemini API)"
---

# Video Understanding v1.0

## Purpose

通过 FFmpeg 抽帧 + Claude 多模态理解，快速分析视频内容并生成：
- 角色/场景/风格的结构化描述
- 技术质量评估
- 第一人称叙事转化 (用于 Lucy persona 写作)
- 文章嵌入位置建议

**与 Lucy 的 Gemini pipeline 的关系**: 互补。
- Lucy pipeline: Gemini API 深度分析 (6 维度，需 API key)
- 本 Skill: Claude 多模态快速理解 + 第一人称叙事转化 (无额外 API)

---

## Trigger Words

```yaml
triggers:
  - "video understanding"
  - "视频理解"
  - "分析视频"
  - "analyze video"
  - "video analysis"
  - "抽帧分析"
```

---

## Input

| 参数 | 必需 | 说明 |
|------|------|------|
| `video_path` | ✅ | 视频文件绝对路径 |
| `context` | 推荐 | 文章主题/背景 (帮助理解视频在文章中的用途) |
| `persona` | 可选 | 叙事视角，默认 `lucy` |

---

## Execution Steps

### Step 1: 视频信息提取

```bash
# 获取视频基本信息
ffprobe -v quiet -print_format json -show_format -show_streams "{video_path}"
```

提取: 时长、分辨率、帧率、文件大小。

### Step 2: 关键帧抽取

```bash
# 调用已有脚本抽取 6-8 帧
python3 scripts/video_frame_extractor.py "{video_path}" --frames 8 --output /tmp/frames/
```

抽帧策略:
- 第 1 帧: 开场 (0.5s)
- 中间帧: 均匀分布
- 最后 1 帧: 结尾 (-0.5s)
- 动作峰值帧: 如有明显动作变化

### Step 3: 多模态视觉分析

对每个关键帧使用 Read 工具读取图片，分析:

| 维度 | 分析内容 |
|------|---------|
| **角色** | 外观描述、发色、服装、表情、身份锚点 |
| **场景** | 地点、灯光、布景、氛围 |
| **动作** | 舞蹈风格、动作类型、动态感 |
| **技术** | 画质、帧间一致性、瑕疵检测 |
| **叙事** | 视频传达的故事/情绪 |

### Step 4: 第一人称叙事转化

将视觉分析转化为第一人称体验叙事:

```
输入: 角色穿黄色 punk 装在停车场跳街舞，表情自信
输出: "I threw on my yellow punk outfit and hit the parking garage. The industrial
       lighting made every move look cinematic. Three takes to get the attitude right."
```

规则:
- 使用 "I" 视角 (Lucy persona)
- 量化体验 (几次尝试、多长时间)
- 包含失败/迭代过程
- 描述技术选择的原因

### Step 5: 输出分析报告

写入 `video-analysis.json` 和 `video-analysis.md`。

---

## Output Structure

**文件 1**: `video-analysis.json`

```json
{
  "metadata": {
    "video_path": "/path/to/video.mp4",
    "duration": 10.1,
    "resolution": "720x1280",
    "fps": 30,
    "file_size_mb": 12.5,
    "frames_extracted": 8,
    "analyzed_at": "2026-03-22T10:00:00Z"
  },
  "character": {
    "description": "Young woman with gradient blue-pink hair",
    "identity_anchor": "蓝粉渐变发色",
    "outfit": "Yellow punk jacket, black boots",
    "expression": "Confident, playful",
    "consistency_across_frames": true
  },
  "scene": {
    "location": "Underground parking garage",
    "lighting": "Industrial fluorescent, dramatic shadows",
    "mood": "Urban, edgy, cinematic",
    "props": []
  },
  "dance_style": "Street hip-hop with freestyle elements",
  "technical_quality": {
    "score": "⭐⭐⭐⭐⭐",
    "resolution_grade": "HD vertical",
    "frame_consistency": "high",
    "issues": [],
    "estimated_model": "Kling 3 / equivalent",
    "notes": "Smooth motion, no visible artifacts"
  },
  "first_person_narrative": "I threw on my yellow punk outfit and hit the parking garage. The industrial lighting made every move look cinematic. Three takes to get the attitude right — the first two felt too stiff, but the third nailed that confident swagger I was going for.",
  "article_embed_suggestion": {
    "position": "Opening experience paragraph",
    "rationale": "Best proof of AI dance influencer viability",
    "caption_suggestion": "Lucy's parking garage hip-hop — Kling 3 + custom prompt"
  },
  "key_observations": [
    "Identity anchor (hair color) consistent across all frames",
    "Dance style matches prompt intent",
    "Vertical format optimized for social media"
  ]
}
```

**文件 2**: `video-analysis.md` (人类可读报告)

```markdown
# Video Analysis: [filename]

## Quick Stats
- Duration: 10.1s | Resolution: 720x1280 | Quality: ⭐⭐⭐⭐⭐

## Character
蓝粉渐变发色 + Yellow punk jacket. Confident expression throughout.

## Scene
Underground parking garage. Industrial fluorescent lighting creates dramatic shadows.

## Dance Style
Street hip-hop with freestyle elements.

## First-Person Narrative (Lucy)
> I threw on my yellow punk outfit and hit the parking garage...

## Article Embed Suggestion
**Position**: Opening experience paragraph
**Rationale**: Best proof of AI dance influencer viability
```

---

## Error Handling

| 场景 | 处理 |
|------|------|
| 视频文件不存在 | 报错并退出，提示检查路径 |
| FFmpeg 未安装 | 提示 `brew install ffmpeg` |
| video_frame_extractor.py 失败 | 回退到直接 ffmpeg 命令: `ffmpeg -i {path} -vf "select=eq(n\,0)+..." -vsync vfr` |
| 帧太暗/模糊无法分析 | 在报告中标记 `low_visibility` 并跳过该帧 |
| 非视频文件 | 检查 mime type，如果是图片则直接分析单帧 |

---

## Usage in Route E Pipeline

```
Route E Phase 2: 素材深化 (可选)
  ├── [video-understanding] ← THIS SKILL (如有视频素材)
  └── Basecamp 内容拉取 (如有 BC 链接)
```

分析结果的数据流向：
- `first_person_narrative` → Writer: 嵌入第一人称体验段
- `article_embed_suggestion` → Editor: 视频嵌入位置
- `technical_quality` → Writer: 技术评价段落
- `character` + `scene` → Writer: 视觉描述素材

---

## Changelog

### v1.0 (2026-03-22)
- 初始版本: FFmpeg 抽帧 + 多模态分析 + 第一人称叙事 + JSON/MD 双输出
