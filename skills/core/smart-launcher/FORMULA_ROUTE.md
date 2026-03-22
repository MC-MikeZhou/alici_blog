# SmartLauncher Route E: Formula-Driven Pipeline

> v1.0 — Formula 驱动写作流程，从 Alici Formulas 生态出发

---

## Overview

Route E 是 SmartLauncher v2.4 新增的第五条路线，核心差异：

| 维度 | Route A-D | Route E |
|------|----------|---------|
| **驱动源** | URL / 关键词 / 种子词 | Alici Formulas 生态 |
| **竞品研究** | source-parser 单源 | 并行 Sub-agent 多源 |
| **数据验证** | 估算搜索量 | DataForSEO 真实数据 |
| **视频理解** | 无 / YouTube 字幕 | FFmpeg 抽帧 + 多模态分析 |
| **叙事视角** | 团队署名 | Lucy 第一人称体验线 |
| **过程管理** | 00-implementation.md | + Basecamp 推送 |

---

## Trigger Words

```yaml
formula_route_triggers:
  - "formula driven"
  - "formula 驱动"
  - "从 formula 出发"
  - "AI influencer"
  - "用 formulas 写"
  - "formula pipeline"
  - "工具页 + 写文章"     # e.g., "/ai-dance-generator 写一篇教程"
```

---

## Pipeline Phases

### Phase 0: Formula 生态扫描

**并行执行** 3 个任务:

```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ formula-         │  │ link-            │  │ DataForSEO       │
│ integrator v1.0  │  │ architect v1.0   │  │ 验证             │
│                  │  │                  │  │ (复用 growth-    │
│ → templates      │  │ → 内链地图       │  │  topic-scout)    │
│ → creators       │  │ → 防蚕食策略     │  │ → 搜索量         │
│ → prompts        │  │ → template 链接  │  │ → 竞争度         │
│ → sub-niches     │  │                  │  │ → SERP 特征      │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         └──────────────┬─────┘────────────────────┘
                        ↓
              Phase 0 Summary 呈现给用户确认
```

**输出**:
- `formula-integration-pack.json`
- `link-architecture.json`
- DataForSEO 验证数据

**用户确认点**: 展示 Formula 生态扫描结果 + 建议写作方向，用户确认后进入 Phase 1。

---

### Phase 1: 竞品并行研究 (Sub-agents)

**3 个 Agent 并行执行**:

```yaml
agents:
  agent_1:
    name: "同赛道竞品搜索"
    task: >
      WebSearch 搜索同主题竞品文章 (英文 + 中文)
      提取: 标题、结构、关键词、独特价值点
    output: competitor-articles.json

  agent_2:
    name: "写作标杆分析"
    task: >
      分析 InVideo/Buffer/HubSpot 等标杆博客的写作风格
      提取: 开篇模式、段落结构、CTA 策略、数据使用方式
    output: benchmark-analysis.json

  agent_3:
    name: "市场数据搜索"
    task: >
      搜索平台算法更新、行业报告、用户行为数据
      提取: 趋势数据、算法变化、市场规模、用户偏好
    output: market-data.json
```

**合并输出**: `competitive-research-pack.json`

---

### Phase 2: 素材深化 (可选)

根据可用素材类型，选择性执行:

| 素材类型 | 执行 Skill | 输出 |
|---------|-----------|------|
| 视频文件 (.mp4/.mov) | `video-understanding v1.0` | `video-analysis.json` |
| Basecamp 链接 | `bc-sync-engine` Pull | Basecamp 内容 |
| YouTube URL | `youtube-transcript-fetcher` | 字幕文件 |
| 无额外素材 | 跳过 Phase 2 | — |

---

### Phase 3: 写作

**Writer 路由** (基于 Phase 0 的方向判断):

| 内容类型 | Writer | 特殊配置 |
|---------|--------|---------|
| 教程 (how-to) | blog-tutorial-writer | + Lucy persona |
| 榜单 (best/top) | blog-list-writer | + Lucy persona |
| 对决 (vs) | blog-showdown-writer | + Lucy persona |
| Playbook (策略) | blog-tutorial-writer (Tier 3) | + Lucy persona |

**写作时注入的额外数据**:

```yaml
writer_context:
  # Phase 0 数据
  formula_pack: "formula-integration-pack.json"
  link_architecture: "link-architecture.json"

  # Phase 1 数据
  competitive_research: "competitive-research-pack.json"

  # Phase 2 数据 (如有)
  video_analysis: "video-analysis.json"

  # Persona 配置
  author_persona: "lucy"   # → 引用 LUCY_PERSONA.md
```

**Writer 必须执行的额外步骤**:
1. 在 Phase 0 建议的位置嵌入 template 链接
2. 在 Phase 0 建议的位置嵌入 creator 案例
3. 遵循 link-architecture 的出链规划
4. 遵循 cannibalization_check 的内容边界
5. 使用 video_analysis 的第一人称叙事 (如有)

---

### Phase 4: 质量 + 输出

标准质量流程 + Formula 特有验证:

```
Writer 输出
    ↓
Editor Gate (标准)
    ↓
AEO Analyzer (目标 ≥85)
    ↓
Formula 专项验证 🆕:
  ├── 内链完整性: 对照 link-architecture 检查所有 outbound_links 是否插入
  ├── Formula 引用: 对照 formula-pack 检查 high-relevance items 是否引用
  ├── 蚕食边界: 确认未重复已有文章的核心内容
  └── Lucy persona 一致性: 检查第一人称叙事风格
    ↓
Framer JSON (含 CDN 图片)
    ↓
Preview HTML
    ↓
(可选) Basecamp 推送:
  ├── 研究文档 (Phase 0-1 输出)
  ├── 交付物 (文章 + JSON)
  └── 复盘 Brief
```

---

## Directory Structure

```
/reports 待发文章/YYYY-MM-DD-{topic-slug}/
├── 00-implementation.md           # 进度追踪
├── 00-formula-integration-pack.json  # Phase 0: Formula 生态
├── 00-link-architecture.json      # Phase 0: 内链规划
├── 00-competitive-research.json   # Phase 1: 竞品研究
├── 00-video-analysis.json         # Phase 2: 视频分析 (如有)
├── 00-video-analysis.md           # Phase 2: 视频报告 (如有)
├── 01-article-draft.md            # Phase 3: 初稿
├── 01-article-edited.md           # Phase 4: 编辑版
├── 03-aeo-score.md                # Phase 4: AEO 评分
├── 07-article-final.json          # Phase 4: Framer JSON
└── 08-preview.html                # Phase 4: 预览
```

---

## Quick Example

```
用户: "从 /ai-dance-generator 出发，写一篇 AI cat dance 教程"

Phase 0:
  → formula-integrator 扫描 /ai-dance-generator → 找到 9 个 cat dance templates
  → link-architect 扫描 blog → 发现 "best-ai-dance-video-generators" 可互链
  → DataForSEO: "AI cat dance" 1,600/mo, low competition

Phase 1:
  → Agent 1: 找到 3 篇竞品 cat dance 教程
  → Agent 2: Buffer 风格分析 → 数据驱动 + 步骤截图
  → Agent 3: TikTok cat dance 趋势数据

Phase 2:
  → video-understanding: 分析 Lucy 的 cat dance 视频 → 第一人称叙事

Phase 3:
  → blog-tutorial-writer + Lucy persona + Formula 案例 + 竞品精华

Phase 4:
  → AEO 89 ✅ → 内链 4/4 ✅ → Formula 引用 5/5 ✅ → Framer JSON → Preview
```

---

## Changelog

### v1.0 (2026-03-22)
- 初始版本: 4 Phase pipeline + 3 新 Skill 集成 + Lucy persona + 并行竞品研究
