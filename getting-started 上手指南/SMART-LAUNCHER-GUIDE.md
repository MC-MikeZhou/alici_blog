# SmartLauncher 快速入门指南

> AliciBlog v2.8 三轨制统一入口使用指南

---

## 什么是 SmartLauncher?

SmartLauncher v2.1 是 AliciBlog 的统一入口，提供三种内容创作路径:

- **Track A 全自动模式**: 最快速，URL 输入后自动完成
- **Track B 手动模式**: 精细控制，5 步确认流程
- **Track C Seed 模式**: 选题发现，从种子词生成方向

---

## 选择哪条路线?

使用以下决策树快速选择:

```
你有竞品 URL 吗?
├── 是 → 全自动模式 (Track A)
│         最快路径: URL → 1-2 问题 → 完整文章
│
└── 否 → 你有明确的标题/方向吗?
          ├── 是 → 手动模式 (Track B)
          │         精细控制: 5 步确认 + 数据验证
          │
          └── 否 → Seed 模式 (Track C)
                    选题发现: 种子词 → 2 个可执行方向
```

---

## 三轨对比

| 维度 | 全自动 (A) | 手动 (B) | Seed (C) |
|------|-----------|---------|----------|
| **输入** | URL (必需) | 标题/方向 | 种子关键词 |
| **问答** | 1-2 个问题 | 5 步流程 | 3 个问题 |
| **输出** | 1 篇文章 | 1 篇文章 | 2 个选题方向 |
| **成本** | ~$1.54 | ~$1.54 | ~$0.47 |
| **适用** | 快速批量洗稿 | 精准控制 | 选题发现 |
| **DataForSEO** | 自动 | 强制展示 | 代表性验证 |

---

## 触发词

### 全自动模式
- 粘贴竞品 URL
- "帮我写一篇..."
- "写一篇关于..."

### 手动模式
- "vs"、"对比"、"对决" + 明确主题
- "我想精确控制..."
- "手动模式"

### Seed 模式
- "seed mode"
- "种子模式"
- "选题漏斗"
- "帮我找选题"
- "topic funnel"

---

## 快速示例

### 示例 1: 全自动模式

```
你: https://competitor.com/blog/ai-video-tools

Claude:
[检测到 URL，启动 SmartLauncher]

Phase 0: 模式选择
┌─────────────────────────────────────────┐
│ [A] 全自动模式 (推荐) ← 已选择          │
│ [B] 手动模式                           │
│ [C] Seed 模式                          │
└─────────────────────────────────────────┘

问题 1/2: 目标读者是谁?
> AI 创作者和营销人员

问题 2/2: 产品植入层级?
> L5 (自然提及)

[自动执行: Scout → Writer → Editor → AEO → Framer]

输出: Preview HTML + 编辑报告
```

### 示例 2: 手动模式

```
你: 帮我写一篇 Kling vs Runway vs Sora 对比

Claude:
[检测到 "vs"，推荐手动模式]

Step 1/5: 内容类型
> Tool Showdown

Step 2/5: DataForSEO 数据确认
┌────────────────────────────────────────┐
│ 关键词: kling vs runway 2026          │
│ 搜索量: 2,400                          │
│ 难度: 32                               │
│ AI Search Heat: HIGH                   │
└────────────────────────────────────────┘
> 确认数据

Step 3/5: Writer 路由
> blog-list-writer (tool_showdown)

Step 4/5: 标题选择 (5+ 选项)
1. Kling 2.6 vs Runway Gen-4 vs Sora 2: Which AI Video Tool Wins in 2026?
2. Kling vs Runway vs Sora 2026 Comparison: Expert Showdown
3. ...
> 选择 1

Step 5/5: 配置摘要确认
> 确认开始

[执行写作流程]
```

### 示例 3: Seed 模式

```
你: 帮我找选题，种子词是 "AI video"

Claude:
[启动 Seed Mode 选题漏斗]

问题 1/3: 产品关联?
> alici.ai 的 AI 视频生成功能

问题 2/3: 目标竞品博客 (3个)?
> higgsfield.ai, invideo.io, runway.com

问题 3/3: 偏好内容类型?
> Listicle 或 Tutorial

[执行 6 Phase 漏斗]
Phase 0: Mission Config ✓
Phase 0.5: 竞品意图发现 → 8 种意图模式
Phase 1: 意图扩散 → 72 关键词
Phase 2: DataForSEO 验证 → 数据获取
Phase 2.5: Scope 裁剪 → 10 方向
Phase 3: Title Lock → 2 个锁定选题

输出:
┌─────────────────────────────────────────┐
│ D01: Best AI Video Generators in 2026  │
│ - SEO Score: 85/100                    │
│ - AEO Score: 78/100                    │
│ - Recommended: blog-list-writer        │
├─────────────────────────────────────────┤
│ D02: How to Create Viral AI Videos     │
│ - SEO Score: 72/100                    │
│ - AEO Score: 82/100                    │
│ - Recommended: blog-tutorial-writer    │
└─────────────────────────────────────────┘

你: 写 D01

Claude: [执行 blog-list-writer 流程]
```

---

## Seed Mode 6 Phase 详解

| Phase | 名称 | 输入 | 输出 |
|-------|------|------|------|
| 0 | Mission Config | Seed + 3 问题 | 00-mission-config.json |
| 0.5 | 竞品意图发现 | 3 竞品博客 | 5-8 种意图模式 |
| 1 | 意图扩散 | 意图模式 | 60-80 关键词 |
| 2 | DataForSEO 验证 | 关键词列表 | 验证数据 (含 3 个 AEO 维度) |
| 2.5 | Scope 裁剪 | 60 关键词 | 10 方向 |
| 3 | Title Lock | 10 方向 | 2 个锁定选题 |

### DataForSEO 新增 AEO 维度 (v2.8)

| 维度 | 数据源 | 含义 |
|------|--------|------|
| AI Search Heat | ai_keyword_data | AI 搜索引擎的关键词热度 |
| LLM Citation Potential | llm_mentions | 被 LLM 引用的可能性 |
| AI Answer Coverage | llm_responses | AI 答案覆盖率 |

---

## 常见问题

### Q: 全自动和手动模式产出的文章质量有差异吗?

**A**: 基本相同。两者都经过完整的 Writer → Editor → AEO 流程。差异在于:
- 全自动: 系统自动决策，80%+ 参考竞品内容
- 手动: 用户确认每一步，可以调整方向

### Q: Seed 模式的 ~$0.47 成本包含什么?

**A**: DataForSEO API 调用费用。通过"代表性验证"策略 (验证 10 个代表关键词而非 60-80 个全量)，成本从 ~$2.59 降至 ~$0.47。

### Q: 什么时候应该用 Seed 模式?

**A**: 当你有一个大方向 (如 "AI video") 但不确定具体写什么时。Seed 模式会:
1. 分析竞品已验证的内容方向
2. 发现市场需求信号
3. 输出 2 个可直接开写的选题

### Q: 可以跳过 SmartLauncher 直接使用 Writer 吗?

**A**: 可以。使用直通命令:
- `/write-tutorial` - 直接写教程
- `/write-list` - 直接写榜单
- `/write-roundup` - 直接写案例汇总

但不推荐，因为会跳过 DataForSEO 验证和选题优化。

---

## 相关文档

- [CLAUDE.md](../CLAUDE.md) - 完整项目配置
- [00-CONTENT-PHILOSOPHY.md](../docs 项目文档/00-CONTENT-PHILOSOPHY.md) - 内容策略哲学
- [08-TEAM-ONBOARDING.md](./08-TEAM-ONBOARDING.md) - 团队上手指南
- [09-TROUBLESHOOTING.md](../docs 项目文档/09-TROUBLESHOOTING.md) - 故障排除

---

*版本: v1.0 (2026-01-26)*
