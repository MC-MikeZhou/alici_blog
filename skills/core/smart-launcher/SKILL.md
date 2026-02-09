---
name: smart-launcher
version: "2.3"
type: skill
provides: unified-entry-orchestration
dependencies:
  - mcp: dataforseo
  - skill: competitive-validator
  - skill: growth-topic-scout (v2.2+)
  - skill: art-scout (v1.1+)
  - capability: output-path-builder
description: >
  SmartLauncher v2.3 - 四轨制架构。
  Step 1.5: 素材使用意图 (洗稿/参考) - 用户明确选择使用方式
  Phase 0: 模式选择（全自动 vs 手动 vs Seed vs 深度研究）- 根据意图推荐
  洗稿模式: 80%+ 保留原内容，禁止新增，品牌换 Alici AI
  参考模式: 作为起点，可以深挖扩展、补充新内容
  深度研究: art-scout 5 Agent 并行 → CEO 综合 → 8 Direction 输出
allowed-tools: Read, Write, WebFetch, WebSearch, AskUserQuestion, Bash
mcp-servers: dataforseo
metadata:
  author: H
  updated: 2026-02-07
  supersedes: [smart-launcher v2.2, smart-router v2.0, smart-root v2.2]
---

# SmartLauncher v2.3 - 四轨制架构

## Purpose

SmartLauncher v2.3 是 AliciBlog 的统一入口层，采用**四轨制架构**，提供全自动/手动/Seed/深度研究四种执行模式，并在用户输入 URL 后首先明确素材使用意图（洗稿/参考），再推荐适合的执行模式。

### 为什么升级到 v2.3？

| v2.2 问题 | v2.3 解决方案 |
|-----------|---------------|
| 缺少深度选题研究能力 | 新增 Route D: art-scout 5 Agent 并行深度研究 |
| 三轨制只覆盖已有方向 | 深度研究模式可从零发现全新选题方向 |
| 单人选题视角局限 | 5 专家角色并行探索，CEO 综合去重排名 |

### 用户定义的两种模式

| 模式 | 定义 | 行为 |
|------|------|------|
| **洗稿** | 几乎 100% 使用原内容，品牌换成 Alici AI | 禁止新增内容，结构保持 |
| **参考** | 作为起点，需要深挖扩展 | 可以扩展、补充、改写 |

### 核心理念

```
v2.2: 意图前置 → 选择路线 → 按路线执行 (三轨制)
     URL → 素材使用意图 (洗稿/参考) → 模式推荐 (A/B/C) → 执行

v2.3: 意图前置 → 选择路线 → 按路线执行 (四轨制) ⭐
     URL → 素材使用意图 (洗稿/参考) → 模式推荐 (A/B/C/D) → 执行
         ↑
   关键新增: Route D 深度研究 (art-scout 5 Agent 并行)
```

---

## Trigger Words

```yaml
triggers:
  # 写作意图 (进入模式选择)
  - "帮我写"
  - "写一篇"
  - "创建内容"
  - "帮我创建"
  - "生成文章"
  - "write about"
  - "create content"
  # Tool Showdown triggers
  - "vs"
  - "对比"
  - "对决"
  - "comparison"
  - "showdown"
  # 内容类型
  - "教程"
  - "tutorial"
  - "how-to"
  - "榜单"
  - "list"
  - "best"
  - "top"
  - "案例"
  - "roundup"
  - "汇总"
  # Seed Mode triggers (v2.1 NEW)
  - "seed mode"
  - "种子模式"
  - "topic funnel"
  - "选题漏斗"
  - "direction expansion"
  - "方向扩展"
  - "find topics for"
  - "帮我找选题"
  - "expand from seed"
  - "从种子词扩展"
```

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   SmartLauncher v2.2 - 意图前置架构                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  用户输入                                                                    │
│      ↓                                                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ Step 1: 直通命令检测                                                  │    │
│  │ - 以 "/" 开头? → 直接执行命令 (不经问卷)                               │    │
│  │ - 否 → 进入意图分析                                                   │    │
│  └──────────────────────┬──────────────────────────────────────────────┘    │
│                         ↓                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ Step 2: 非写作意图检测                                                │    │
│  │ - 分析/选题 → scout-topic                                            │    │
│  │ - 评分/AEO → analyze-aeo                                             │    │
│  │ - 改进 → improve-article                                             │    │
│  │ - 字幕 / YouTube URL (单独输入) → fetch-transcript                   │    │
│  │ - 导出 → convert-to-framer                                           │    │
│  │ - 预览 → preview-chinese                                             │    │
│  │ - Seed模式触发词 → 直接进入 Seed Mode                                 │    │
│  │ - 否 → 进入写作流程                                                   │    │
│  └──────────────────────┬──────────────────────────────────────────────┘    │
│                         ↓                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ Step 1.5: 素材使用意图 (v2.2 NEW) ⭐                                   │    │
│  │                                                                     │    │
│  │   触发条件: 用户输入包含 URL (YouTube/竞品文章)                        │    │
│  │                                                                     │    │
│  │   Q: 你想如何使用这个素材？                                           │    │
│  │   ┌─────────────────────────────────────────────────────────────┐   │    │
│  │   │ [A] 洗稿 (Recommended)                                       │   │    │
│  │   │     80%+ 保留原内容，品牌换成 Alici AI，禁止新增              │   │    │
│  │   ├─────────────────────────────────────────────────────────────┤   │    │
│  │   │ [B] 参考                                                     │   │    │
│  │   │     作为起点，可以深挖扩展、补充新内容                         │   │    │
│  │   └─────────────────────────────────────────────────────────────┘   │    │
│  └──────────────────────┬──────────────────────────────────────────────┘    │
│                         │                                                   │
│         ┌───────────────┴───────────────┐                                   │
│         ↓                               ↓                                   │
│  ┌────────────────┐            ┌────────────────┐                           │
│  │ 🔄 洗稿模式     │            │ 📚 参考模式     │                           │
│  │                │            │                │                           │
│  │ - 禁止新增内容 │            │ - 可扩展内容   │                           │
│  │ - 保持原结构   │            │ - 调用选题扩展 │                           │
│  │ - 品牌替换     │            │ - DataForSEO   │                           │
│  │ - 严格验证     │            │ - 可重组结构   │                           │
│  └───────┬────────┘            └───────┬────────┘                           │
│          │                             │                                    │
│          └─────────────┬───────────────┘                                    │
│                        ↓                                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ Phase 0: 模式选择 (v2.3 Updated)                                      │    │
│  │ (根据 intent 自动推荐模式)                                            │    │
│  │                                                                     │    │
│  │   洗稿意图 → 推荐 [A] 全自动模式 (无需扩展调研，快速执行)              │    │
│  │   参考意图 → 推荐 [B] 手动模式 或 [C] Seed模式 (需确认扩展方向)        │    │
│  │   深度研究 → [D] Agent Team 多角色并行                                │    │
│  │                                                                     │    │
│  │   ┌─────────────────────────────────────────────────────────────┐   │    │
│  │   │ [A] 全自动模式                                               │   │    │
│  │   │     输入 URL → 简单问题 → 一口气到 Preview HTML               │   │    │
│  │   ├─────────────────────────────────────────────────────────────┤   │    │
│  │   │ [B] 手动模式                                                 │   │    │
│  │   │     提供标题/方向 → DataForSEO 确认 → 选择 Writer            │   │    │
│  │   ├─────────────────────────────────────────────────────────────┤   │    │
│  │   │ [C] Seed 模式                                                │   │    │
│  │   │     种子词 → 选题漏斗（D1=2 / D2=3）→ 可执行方向               │   │    │
│  │   ├─────────────────────────────────────────────────────────────┤   │    │
│  │   │ [D] 深度研究 (Agent Team) 🆕                                  │   │    │
│  │   │     5 专家并行 → 8 方向 → DataForSEO 验证 → Direction         │   │    │
│  │   └─────────────────────────────────────────────────────────────┘   │    │
│  └──────────────────────┬──────────────────────────────────────────────┘    │
│                         │                                                   │
│         ┌───────────┬───┼───────────┬───────────┐                           │
│         ↓           ↓   ↓           ↓           │                           │
│  ┌──────────┐ ┌──────────┐ ┌──────────────┐ ┌──────────────┐               │
│  │🤖 全自动 │ │✋ 手动    │ │🌱 Seed模式   │ │🔬 深度研究   │               │
│  │Full-Auto │ │Manual    │ │选题漏斗       │ │Agent Team    │               │
│  │          │ │          │ │              │ │              │               │
│  │AUTO_ROUTE│ │MANUAL_   │ │growth-topic- │ │art-scout     │               │
│  │.md       │ │ROUTE.md  │ │scout v2.4    │ │v1.1          │               │
│  └────┬─────┘ └────┬─────┘ └──────┬───────┘ └──────┬───────┘               │
│       │            │              │                │                       │
│       └────────────┴──────────────┴────────────────┘                       │
│                        ↓                                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ 执行阶段 (共享)                                                       │    │
│  │ Writer → **Editor Gate** → AEO ⟷ Improver → 竞品验证 → Framer        │    │
│  │          ↑       │                                                  │    │
│  │          └───────┘ (Feedback Loop if BLOCKING)                      │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Step 1.5: 素材使用意图 (v2.2 NEW) ⭐

### 触发条件

当用户输入包含 URL (YouTube 视频 / 竞品文章) 时，在进入模式选择前，首先询问素材使用意图。

### 意图问卷

```json
{
  "questions": [
    {
      "question": "你想如何使用这个素材？",
      "header": "Intent",
      "multiSelect": false,
      "options": [
        {
          "label": "洗稿 (Recommended)",
          "description": "80%+ 保留原内容，品牌换成 Alici AI，禁止新增"
        },
        {
          "label": "参考",
          "description": "作为起点，可以深挖扩展、补充新内容"
        }
      ]
    }
  ]
}
```

### 意图定义

| 意图 | 定义 | 适用场景 |
|------|------|----------|
| **洗稿** | 几乎 100% 使用原内容，品牌换成 Alici AI | 竞品内容质量高，直接借鉴 |
| **参考** | 作为起点，需要深挖扩展 | 竞品内容有启发，但需要扩展 |

### 意图 → 约束配置

**洗稿意图 (intent = "洗稿")**:
- `preserve_structure: true` - 保持原结构
- `no_new_tools: true` - 禁止新增工具
- `no_new_scenarios: true` - 禁止新增场景
- `brand_swap: "Alici AI"` - 品牌替换目标
- `word_count_ratio: [0.8, 1.2]` - 字数约束
- `strict_validation: true` - 严格验证

**参考意图 (intent = "参考")**:
- `preserve_structure: false` - 可重组结构
- `allow_new_tools: true` - 允许新增工具
- `allow_expansion: true` - 允许扩展内容
- `research_required: true` - 需要额外调研
- `call_growth_topic_scout: true` - 调用选题扩展
- `call_dataforseo: true` - 验证关键词数据

### 意图 → 模式推荐映射

| 素材使用意图 | 推荐模式 | 原因 |
|-------------|---------|------|
| 洗稿 | **全自动** (Recommended) | 无需扩展调研，快速执行 |
| 参考 | **手动** 或 **Seed** | 需要确认扩展方向，可能需要选题发现 |

### 跳过条件

以下情况跳过意图问卷，直接进入模式选择：
- 用户未提供 URL（仅提供标题/方向）
- 用户使用 Seed Mode 触发词
- 用户使用直通命令 (/)

---

## Phase 0: 模式选择 (v2.2 Updated)

### 0.1 模式问卷

基于 Step 1.5 的意图，动态调整推荐：

```json
{
  "questions": [
    {
      "question": "你想用哪种模式创建内容？",
      "header": "Mode",
      "multiSelect": false,
      "options": [
        {
          "label": "全自动模式",
          "description": "输入 URL → 回答 1-2 个问题 → 一口气到 Preview HTML",
          "recommended_when": "intent == '洗稿'"
        },
        {
          "label": "手动模式",
          "description": "提供标题/方向 → 确认 DataForSEO 数据 → 选择 Writer → 逐步确认",
          "recommended_when": "intent == '参考'"
        },
        {
          "label": "Seed 模式 (选题漏斗)",
          "description": "种子词 + 竞品锚点 → 意图模式发现 → 2 个可执行方向",
          "recommended_when": "intent == '参考' && need_topic_discovery"
        },
        {
          "label": "深度研究 (Agent Team)",
          "description": "5 专家并行探索 → 8 个方向 → DataForSEO 验证 → Decision Brief",
          "recommended_when": "need_comprehensive_research || important_topic"
        }
      ]
    }
  ]
}
```

### 0.2 模式特点对比

| 特点 | 全自动模式 | 手动模式 | Seed 模式 | 深度研究 🆕 |
|------|-----------|----------|-----------|-------------|
| 适合场景 | 有竞品 URL + **洗稿意图** | 已有方向 + **参考意图** | 只有种子词 | 重要选题，需全景视角 |
| 用户输入 | 1 个 URL + 1-2 问题 | 标题 + 素材 + 多步确认 | 种子词 + 3 问题 | 种子词 + 3 问题 |
| DataForSEO | 自动验证 | 展示确认 | 验证代表词 | Phase 3 集中验证 |
| Writer 选择 | 自动决策 | 用户选择 | 基于方向推荐 | 基于 Direction 推荐 |
| 标题选择 | 自动最佳 | 5+ 选项 | Title Lock | Title Lock |
| 输出 | 1 篇文章 | 1 篇文章 | 2-3 方向 | 5-8 方向 + Brief |
| 执行过程 | 完全无干预 | 每步确认 | 漏斗透明 | Agent 并行透明 |
| 成本 | ~$1.54 | ~$1.54 | ~$0.47 | ~$0.17 |
| **推荐意图** | **洗稿** | **参考** | **参考 + 需选题** | **全景研究** |

### 0.3 路线分流

根据用户选择，分流到对应路线：

| 选择 | 分流目标 | 详细规范 |
|------|----------|----------|
| 全自动模式 | → AUTO_ROUTE.md | 简化问卷 + 自动决策 |
| 手动模式 | → MANUAL_ROUTE.md | 5 步流程 + 强制确认 |
| Seed 模式 | → growth-topic-scout v2.4 Mode D1/D2 | 选题漏斗（D1=2 / D2=3）+ Title Lock |
| 深度研究 🆕 | → art-scout v1.1 | 5 Agent 并行 → CEO 综合 → 8 Direction |

### 0.4 Seed 模式自动触发

当检测到以下触发词时，自动进入 Seed 模式（跳过模式选择问卷）：

```yaml
auto_trigger_seed_mode:
  - "seed mode"
  - "seed mode v2"
  - "种子模式"
  - "topic funnel"
  - "选题漏斗"
  - "diversity seed"
  - "发散选题"
  - "多样性选题"
  - "cosine"
  - "余弦相似度"
  - "find topics for [X]"
  - "帮我找 [X] 相关选题"
  - "expand from seed"
  - "从种子词扩展"
```

---

## 全自动路线概要

> 详细规范见 `AUTO_ROUTE.md`

```
全自动路线流程 (v2.2 Updated):
┌─────────────────────────────────────────────────────────────────┐
│ Step 1: 输入                                                     │
│ └── URL (竞品文章 / YouTube 视频)                                │
│                      ↓                                          │
│ Step 1.5: 素材使用意图 (v2.2 NEW) ⭐                             │
│ ├── Q: 你想如何使用这个素材？                                    │
│ ├── [A] 洗稿 → rewrite_mode 约束                                │
│ └── [B] 参考 → reference_mode 约束                              │
│                      ↓                                          │
│ Step 2: 快速问卷 (1-2 个问题)                                    │
│ ├── 目标: 帮人选择 / 教人做事 / 展示发现                         │
│ └── (可选) 产品聚焦                                              │
│                      ↓                                          │
│ Step 3: 内容分析 + 工具数量检测                                  │
│ ├── fetch-transcript (如果是 YouTube)                            │
│ ├── 提取工具列表 + 测试场景                                      │
│ ├── 统计对比工具数量                                             │
│ └── 判断: 洗稿模式 (≤3) vs 可扩展模式 (>4)                      │
│                      ↓                                          │
│ Step 3.5: 文章类型确认 (条件触发)                                │
│ ├── 触发条件: 工具数量 2-4 / 混合意图 / 置信度 <80%              │
│ ├── 用户选择: Tool Showdown / Listicle / Tutorial                │
│ └── 未触发则自动决策                                             │
│                      ↓                                          │
│ Step 4: 自动执行 (无需干预)                                      │
│ ├── 根据 intent 应用约束配置 (v2.2 NEW)                         │
│ ├── growth-topic-scout (自动选题)                                │
│ ├── 自动选择 Writer (含意图约束)                                 │
│ ├── Writer 执行                                                  │
│ ├── 意图验证 (v2.2 NEW): 检查新工具/场景 (洗稿) 或扩展内容 (参考)│
│ ├── Editor Gate                                                  │
│ ├── AEO Analyzer                                                 │
│ ├── Auto-Improver (如需要)                                       │
│ ├── Framer JSON                                                  │
│ └── Preview HTML                                                 │
│                      ↓                                          │
│ Step 5: 呈现结果                                                 │
│ └── 直接展示 Preview HTML + 报告摘要                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 手动路线概要

> 详细规范见 `MANUAL_ROUTE.md`

```
手动路线流程:
┌─────────────────────────────────────────────────────────────────┐
│ Step 1: 收集用户意图                                             │
│ ├── 想要的标题 (或标题方向)                                      │
│ ├── 想要的方向/角度                                              │
│ └── 相关素材 (URL / 参考文章 / 关键词)                           │
│                      ↓                                          │
│ Step 2: DataForSEO 数据验证 (强制)                               │
│ ├── 搜索量查询                                                   │
│ ├── 竞品分析                                                     │
│ └── 用户确认数据 (可调整关键词)                                  │
│                      ↓                                          │
│ Step 3: 识别写作方向 (路由决策)                                   │
│ ├── Tool Showdown → blog-list-writer (showdown mode)            │
│ ├── Listicle → blog-list-writer                                 │
│ ├── Tutorial → blog-tutorial-writer                              │
│ └── Case Study → case-roundup-writer                             │
│                      ↓                                          │
│ Step 4: 标题确认                                                 │
│ ├── 基于 growth-topic-scout 生成 5+ 标题选项                     │
│ └── 用户选择或自定义                                             │
│                      ↓                                          │
│ Step 5: 确认执行                                                 │
│ ├── 显示完整配置摘要                                             │
│ └── 用户确认后进入执行阶段                                       │
│                      ↓                                          │
│ [执行阶段] Writer → Editor Gate → AEO → Framer → Preview         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Seed 模式概要 (v2.1 NEW)

> 详细规范见 `growth-topic-scout/SKILL.md` Mode D1/D2

```
Seed 模式流程:
┌─────────────────────────────────────────────────────────────────┐
│ Phase 0: Mission Config                                          │
│ ├── 输入种子词 (如 "ai video tools 2026")                        │
│ ├── 3 个简单问题 (受众/目标/竞品)                                │
│ └── 输出: 00-mission-config.json                                 │
│                      ↓                                          │
│ Phase 0.5: 竞品意图模式发现                                      │
│ ├── 抓取 5 个竞品博客 (默认；各 10-20 篇)                        │
│ ├── 提取标题、内容类型、目标关键词                               │
│ └── 归纳 5-8 种意图模式                                          │
│                      ↓                                          │
│ Phase 1: 意图模式扩散                                            │
│ ├── 每个模式扩散 8-10 个关键词                                   │
│ └── 输出: 60-80 个待验证关键词                                   │
│                      ↓                                          │
│ Phase 2: DataForSEO 数据验证                                     │
│ ├── 批量验证关键词                                               │
│ ├── 三级筛选 (高/中/长尾)                                        │
│ └── 方向级聚合                                                   │
│                      ↓                                          │
│ Phase 2.5: Scope 裁剪 (60 → 10 方向)                            │
│ ├── Gate 1: 需求验证 (volume ≥ 100)                             │
│ ├── Gate 2: 业务对齐 (产品映射)                                  │
│ └── Gate 3: 聚类去重                                             │
│                      ↓                                          │
│ Phase 3: Title Lock                                              │
│ ├── 主关键词命中                                                 │
│ ├── 意图匹配                                                     │
│ ├── SERP 范式对齐                                                │
│ └── 年份验证                                                     │
│                      ↓                                          │
│ 输出: 2 个可执行方向                                             │
│ ├── 00-mission-config.json                                       │
│ ├── 00-directions-report.md                                      │
│ └── 00-topic-brief.json (v2.2 格式)                              │
│                      ↓                                          │
│ [可选] 选择方向后进入执行阶段                                    │
│ Writer → Editor Gate → AEO → Framer → Preview                    │
└─────────────────────────────────────────────────────────────────┘
```

### Seed 模式输出

Seed 模式完成后输出：

| 文件 | 说明 |
|------|------|
| `00-mission-config.json` | Mission Architecture 配置 |
| `00-directions-report.md` | 人类可读报告 (10 个初始方向 → 2 个最终方向) |
| `00-topic-brief.json` | v2.2 格式，含 evidence chains 和 Title Lock |

### Seed 模式与写作执行

用户可选择：
1. **立即执行** - 选择 1 个方向，进入执行阶段
2. **全部执行** - 依次执行 2 个方向 (批量模式)
3. **仅保存** - 保存方向，稍后执行

---

## 深度研究模式概要 (v2.3 NEW)

> 详细规范见 `art-scout/SKILL.md` v1.1

```
深度研究模式流程:
┌─────────────────────────────────────────────────────────────────┐
│ art-scout Phase 0: Mission Briefing                              │
│ ├── 3 个问题 (种子词/受众/产品)                                   │
│ └── 输出: mission-config                                         │
│                      ↓                                          │
│ art-scout Phase 1: 5 SubAgent 并行探索                            │
│ ├── keyword_scout (关键词猎手)                                    │
│ ├── content_strategist (内容策略师)                                │
│ ├── market_analyst (市场分析师)                                    │
│ ├── tech_specialist (技术专家)                                     │
│ └── user_persona (用户画像师)                                      │
│     → 各自 WebSearch 产出 5-8 个方向                               │
│                      ↓                                          │
│ art-scout Phase 2: CEO 综合                                       │
│ ├── 去重 + 排名 + 多样性分析                                      │
│ └── 输出: 8-10 个候选方向                                         │
│                      ↓                                          │
│ art-scout Phase 3: DataForSEO 集中验证                             │
│ ├── 搜索量 + 竞品分析 + AEO 维度                                  │
│ └── Title Lock                                                   │
│                      ↓                                          │
│ art-scout Phase 4: 输出                                           │
│ ├── 5-8 个 Direction + Decision Brief                             │
│ └── 输出到 /research 竞品分析/team-research/                      │
│                      ↓                                          │
│ 用户选择 1-2 个 Direction                                         │
│ → 回到 SmartLauncher 共享执行阶段                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 深度研究 vs 其他模式对比

| 模式 | 研究深度 | 方向数量 | 耗时 | DataForSEO 成本 | 适用场景 |
|------|---------|---------|------|----------------|---------|
| 全自动 | 无 (洗稿) | 1 | ~5 min | ~$0 | URL 洗稿、快速产出 |
| 手动 | 单点验证 | 1 | ~10 min | ~$0.10 | 已有方向，需数据确认 |
| Seed | 单人漏斗 | 2-3 | ~15 min | ~$0.47 | 需要选题发现 |
| **深度研究** | **5 专家并行** | **5-8** | **~20 min** | **~$0.17** | **重要选题、需要全景视角** |

### 独立触发

art-scout 仍可通过独立触发词直接调用 (不经 SmartLauncher):
- "团队研究", "多角色选题", "全景扫描", "agent team", "team scout"

独立调用时输出到 `/research 竞品分析/team-research/YYYY-MM-DD-{seed-slug}/`，不自动进入 Writer 流程。

---

## 执行阶段 (四条路线共享)

### 执行流程

```
═══════════════════════════════════════════════════
▶ 进入全自动执行模式，无需进一步干预
═══════════════════════════════════════════════════

Step 1: 素材准备
├── YouTube URL? → fetch-transcript → transcript saved
└── 无 URL? → 跳过

Step 2: 内容生成 (根据路由结果选择 Writer)
├── Tool Showdown → blog-list-writer (mode: tool_showdown)
├── Listicle → blog-list-writer (mode: standard)
├── Tutorial → blog-tutorial-writer
└── Case Study → case-roundup-writer

Step 3: Editor Gate (强制)
├── 输入: 01-article-draft.md
├── 执行: Editor v2.9.2 (9 Modules + 4 强制规则)
├── 输出: 01-article-edited.md
└── 判断:
    ├── ✅ PASS → Step 4
    ├── ⚠️ WARNING → Auto-fix → Step 4
    └── ⛔ BLOCKING (无法自动修复) → Step 3.5 (Writer Feedback Loop)

Step 3.5: Writer Feedback Loop (条件触发)
├── 触发条件: Editor BLOCKING 且无法自动修复
├── 反馈内容: 04-editor-report.md 中的 BLOCKING 问题
├── Writer 重写: 针对性修复 BLOCKING 问题
├── 返回: Step 3 (Editor Gate)
└── 最大循环: 2 次，超过则 MANUAL_REVIEW

Step 4: 质量评估
└── aeo-analyzer → 评分

Step 5: 自动改进 (如需要)
├── 分数 >= 目标? → 通过
└── 分数 < 目标? → auto-improver → 重新评估 (最多 3 轮)

Step 6: 竞品验证
└── competitive-validator → Top 5 竞品对比

Step 7: 输出生成
├── markdown-to-framer → Framer JSON
├── framer-previewer → HTML Preview
└── 首次呈现给用户的是 01-article-edited.md (已通过 Editor)
```

### AEO 目标分数

| 写作方向 | AEO 目标 |
|----------|----------|
| Case Study (新功能速报) | >= 70 |
| Tutorial (快速教程) | >= 75 |
| Listicle (榜单) | >= 75 |
| Tool Showdown (对决) | >= 75 |
| Ultimate Guide (终极指南) | >= 80 |

---

## Writer 路由表

| 写作方向 | Writer | Mode | 输出字数 | 检测信号 |
|----------|--------|------|----------|----------|
| Tool Showdown | blog-showdown-writer | - | 2,500-3,500 | vs, 对比, 对决, comparison |
| Listicle | blog-list-writer | standard | 2,500-3,500 | best, top N, 榜单, 数字开头 |
| Tutorial | blog-tutorial-writer | - | 1,800-2,500 | how to, 如何, 教程, guide |
| Case Study | case-roundup-writer | - | 300-600 | 案例, case, roundup, 汇总 |

---

## 非写作意图 (直接执行)

以下意图不经过问卷，直接路由到对应工具：

| 意图 | 关键词 | 路由目标 |
|------|--------|----------|
| 分析/选题 | 分析, 竞品, 选题 | → scout-topic |
| 质量评分 | 评分, AEO, 质量 | → analyze-aeo |
| 文章改进 | 改进, 优化, improve | → improve-article |
| 字幕获取 | 字幕, transcript, **YouTube URL 单独输入** | → fetch-transcript |
| 导出 JSON | 导出, framer, json | → convert-to-framer |
| 中文预览 | 预览, 中文, 审核 | → preview-chinese |

---

## YouTube URL 检测

当用户输入**仅包含** YouTube URL（无其他文字或仅有简单请求）时，自动路由到 `fetch-transcript`：

```python
def is_youtube_url_only(input_text):
    """
    检测用户输入是否为单独的 YouTube URL
    """
    import re

    cleaned = input_text.strip()

    youtube_patterns = [
        r'^https?://(www\.)?youtube\.com/watch\?v=[a-zA-Z0-9_-]{11}(\S*)?$',
        r'^https?://youtu\.be/[a-zA-Z0-9_-]{11}(\S*)?$',
        r'^https?://(www\.)?youtube\.com/embed/[a-zA-Z0-9_-]{11}(\S*)?$'
    ]

    simple_prefixes = ['', '抓取', '获取', '字幕', '帮我', '请', 'fetch', 'get', 'transcript', 'please']

    for pattern in youtube_patterns:
        for prefix in simple_prefixes:
            test_input = cleaned.lower().replace(prefix, '').strip()
            if re.match(pattern, test_input, re.IGNORECASE):
                return True

    return False
```

---

## Configuration

### Default Settings

```yaml
defaults:
  recommended_mode: "full_auto"
  language: "en"
  images: "video_embed_plus_ai"
  aeo_target:
    roundup: 70
    tutorial: 75
    list: 75
    showdown: 75
    ultimate_guide: 80
  max_improvement_rounds: 3
  max_editor_feedback_loops: 2
```

### DataForSEO Settings

```yaml
dataforseo:
  location_code: 2840  # US
  language_code: "en"
  batch_size: 10
  fallback: "websearch"
```

---

## Output

### Confirmed Brief 格式 (v2.0)

```json
{
  "confirmed_at": "2026-01-23T12:00:00Z",
  "schema_version": "4.0",
  "mode": "full_auto | manual",
  "goal": "帮人选择工具",
  "writer": "blog-list-writer",
  "writer_mode": "tool_showdown",
  "topic": {
    "keyword": "Sora vs Runway vs Kling",
    "search_volume": 4800,
    "data_source": "dataforseo"
  },
  "title": {
    "selected": "Sora vs Runway vs Kling: Which AI Video Model Wins in 2026?",
    "type": "showdown"
  },
  "verified_tools": [...],
  "execution_config": {
    "auto_mode": true,
    "aeo_target": 75,
    "max_improvement_rounds": 3
  }
}
```

### 输出文件路径

```
/reports/YYYY-MM-DD-{topic-slug}/
├── 00-implementation.md
├── 00-confirmed-brief.json
├── 01-article-draft.md
├── 01-article-edited.md
├── 03-aeo-score.md
├── 04-editor-report.md
├── 06-article-final.json
├── 07-preview.html
└── 08-competitive-validation.md
```

---

## Error Handling

| 错误类型 | 处理方式 |
|----------|----------|
| DataForSEO 配额用尽 | 切换到 WebSearch 估算 |
| 用户选择 "Other" | 接受自定义输入，继续流程 |
| Writer 执行失败 | 报告错误，提供手动命令 |
| AEO 3 轮后仍 < 目标 | 标记 MANUAL_REVIEW，输出当前最佳版本 |
| Editor BLOCKING 2 轮后未解决 | 标记 MANUAL_REVIEW，停止自动流程 |

---

## Changelog

### v2.3 (2026-02-07)

**四轨制架构: 新增 Route D 深度研究**

1. **Phase 0 新增 [D] 深度研究**:
   - 调用 art-scout v1.1 (5 Agent 并行探索)
   - 输出 5-8 个 Direction + Decision Brief
   - 用户选择 1-2 个 Direction 后进入共享执行阶段

2. **四轨制对比表**:
   - 全自动 / 手动 / Seed / 深度研究
   - 研究深度递增，方向数量递增

3. **art-scout 独立触发保留**:
   - 触发词: 团队研究, 多角色选题, 全景扫描, agent team
   - 独立调用时输出到 /research 竞品分析/team-research/

4. **版本号更新**:
   - smart-launcher v2.2 → v2.3
   - 新增 art-scout v1.1 依赖

---

### v2.2 (2026-01-26)

**意图前置架构: 素材使用意图问卷**

1. **Step 1.5 素材使用意图 (NEW)**:
   - 触发条件: 用户输入包含 URL (YouTube/竞品文章)
   - 两种意图: 洗稿 (80%+ 保留) / 参考 (可扩展)
   - 在模式选择前明确用户意图

2. **意图 → 约束配置**:
   - 洗稿模式: `preserve_structure`, `no_new_tools`, `no_new_scenarios`, `brand_swap`, `strict_validation`
   - 参考模式: `allow_expansion`, `research_required`, `call_growth_topic_scout`, `call_dataforseo`

3. **意图 → 模式推荐映射**:
   - 洗稿意图 → 推荐全自动模式 (无需扩展调研，快速执行)
   - 参考意图 → 推荐手动模式 或 Seed模式 (需确认扩展方向)

4. **架构图更新**:
   - 新增 Step 1.5 素材使用意图分支
   - 洗稿/参考模式约束对比
   - Phase 0 显示意图 → 模式推荐

5. **文件更新**:
   - `AUTO_ROUTE.md`: 新增 intent 参数 + 洗稿/参考模式配置
   - `MANUAL_ROUTE.md`: 新增参考模式扩展调研流程

**预期效果**:
- 用户明确选择素材使用方式
- 洗稿模式: 严格约束，禁止新增
- 参考模式: 允许扩展，调用选题发现
- 模式推荐: 基于意图自动推荐最佳模式

---

### v2.1.1 (2026-01-26)

**洗稿模式优化: 工具数量检测 + 文章类型确认**

1. **工具数量检测** (AUTO_ROUTE.md Step 3.3):
   - 新增 `count_compared_tools()` 函数
   - 新增 `extract_tool_list()` 函数
   - 新增 `extract_test_scenarios()` 函数
   - 根据工具数量决定 Tool Showdown vs Listicle

2. **文章类型确认** (AUTO_ROUTE.md Step 3.5 NEW):
   - 边界情况 (工具数量 2-4) 时触发确认问卷
   - 混合意图 (对比 + 教程) 时触发确认
   - 置信度 < 80% 时触发确认

3. **洗稿约束强化** (AUTO_ROUTE.md Step 3.6 NEW):
   - `no_new_tools: true` - 禁止添加原素材未提及的工具
   - `no_new_scenarios: true` - 禁止添加原素材未覆盖的场景
   - `word_count_ratio: [0.8, 1.2]` - 字数约束
   - 新增 `validate_rewrite_output()` 验证函数

4. **COMBOS.md 更新**:
   - 新增路由决策矩阵 (工具数量 → 模式)
   - 新增洗稿约束表 (约束项 + 违反后果)
   - 更新 `route_auto()` 函数

5. **架构图更新** (SKILL.md):
   - Step 3 增加工具数量检测
   - Step 3.5 新增文章类型确认
   - Step 4 增加洗稿验证

**预期效果**:
- Runway vs Kling (2 工具) → Tool Showdown 洗稿模式
- Top 8 AI Video (8 工具) → Listicle 可扩展模式
- 边界情况 (4 工具) → 用户确认

---

### v2.1 (2026-01-25)

**Seed Mode 集成: 选题漏斗系统**

1. **三轨制架构**:
   - 全自动模式 (preserved)
   - 手动模式 (preserved)
   - Seed 模式 (NEW) - 选题漏斗系统

2. **Seed 模式特性**:
   - Phase 0: Mission Config + 竞品锚点 (3 个问题)
   - Phase 0.5: 竞品意图模式发现 (5-8 种模式)
   - Phase 1: 意图模式扩散 (60-80 关键词)
   - Phase 2: DataForSEO 验证 + 三级筛选
   - Phase 2.5: Scope 裁剪 (60 → 10 方向)
   - Phase 3: Title Lock (验证后可用标题)

3. **新增触发词**:
   - seed mode, 种子模式, topic funnel, 选题漏斗
   - find topics for [X], 帮我找 [X] 相关选题

4. **成本优化**:
   - Seed 模式 ~$0.47 (standard) vs 传统模式 ~$1.54
   - 只验证方向代表词，不是全部关键词

5. **依赖升级**:
   - growth-topic-scout v2.3+ (Mode D1/D2: Seed Mode)

**预期效果**:
- 从种子词到可执行方向: 1 seed → 2 directions
- 方向淘汰率: 60 → 10 → 2 (精准筛选)
- 标题可用性: 建议 → 验证后直接使用

### v2.0.1 (2026-01-23)

**测试通过: 双轨制流程验证**

1. **手动路线测试** (7/7 PASS):
   - Phase 0 模式选择问卷正确显示
   - Step 2 DataForSEO 数据强制展示并确认
   - Step 3 "vs" 自动识别为 Tool Showdown
   - Step 4 展示 5+ 标题选项
   - Step 5 配置摘要完整
   - 正确路由到 blog-list-writer (tool_showdown)

2. **全自动路线测试** (7/7 PASS):
   - 只问 1-2 个问题 (目标)
   - 自动调用 growth-topic-scout
   - 自动选择正确的 Writer
   - 洗稿模式: 80%+ 内容参考竞品
   - 一口气执行到 Preview HTML
   - 呈现 Preview + 报告摘要

3. **测试覆盖率**: 14/14 验证点全部通过

### v2.0 (2026-01-23)

**架构重设计: 双轨制入口**

1. **Phase 0 模式选择** (新增):
   - 入口处明确选择全自动 vs 手动模式
   - 用户清楚知道自己在哪条路线上

2. **全自动路线** (AUTO_ROUTE.md):
   - URL + 1-2 个问题 → 一键到 Preview HTML
   - 自动调用 growth-topic-scout
   - 自动选择 Writer
   - 完全无需干预

3. **手动路线** (MANUAL_ROUTE.md):
   - 5 步流程 + 每步确认
   - 强制 DataForSEO 数据展示和确认
   - 用户选择 Writer 和标题
   - 配置摘要确认后执行

4. **强制 growth-topic-scout**:
   - 两条路线都必须调用
   - 不再被绕过

5. **强制 DataForSEO 确认 (手动路线)**:
   - 展示搜索量、趋势、CPC
   - 用户必须确认或调整关键词

6. **明确 Writer 路由**:
   - Tool Showdown → blog-list-writer (tool_showdown)
   - Listicle → blog-list-writer (standard)
   - Tutorial → blog-tutorial-writer
   - Case Study → case-roundup-writer

**预期收益**:
- 用户模式感知: 不清楚 → 100% 清晰
- growth-topic-scout 调用率: 可变 → 100%
- DataForSEO 确认率 (手动): 0% → 100%
- Writer 路由正确率: 可变 → 100%

### v1.2 (2026-01-22)

- Editor Gate 强制
- Writer Feedback Loop
- 详见旧版本历史

---

*SmartLauncher v2.3 - 意图前置架构 × 洗稿/参考模式 × 四轨制执行 (全自动/手动/Seed/深度研究)*
