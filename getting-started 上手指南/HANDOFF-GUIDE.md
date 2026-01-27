# AliciBlog 交接指南

> 5 分钟快速上手 | v2.8 | 2026-01-26

---

## 项目是什么？

AliciBlog 是 alici.ai 的 **AI 内容工厂**，目标是实现博客生产 **70%+ 自动化**。

**核心能力**:
- 自然语言驱动：说"帮我写一篇关于 X 的文章"即可启动
- 交互式选题：4 步问卷确认后全自动执行
- 质量保障：AEO 评分 ≥75 分才能通过
- 竞品验证：自动对比 Top 5 竞品

---

## 快速开始

### 1. 环境配置 (15 分钟)

```bash
# 进入项目目录
cd /Users/H/Documents/AliciBlog

# 启动 Claude Code
claude
```

详细配置步骤见 `LOCAL-SETUP.md`。

### 2. 第一次使用

```bash
# 最简单的方式 - 自然语言
帮我写一篇关于 AI 视频生成工具的教程

# 或使用直接命令
/write-tutorial
```

### 3. 理解输出

所有输出保存在 `/reports/YYYY-MM-DD-{topic}/` 目录：

```
/reports/2026-01-22-ai-video-tools/
├── 00-implementation.md      # 进度追踪
├── 01-article-draft.md       # 初稿
├── 01-article-edited.md      # 编辑版（含图片）
├── 03-aeo-score.md           # 质量评分
└── 06-article-final.json     # Framer CMS JSON
```

---

## 核心工作流 (v2.8 三轨制)

```
用户描述需求
       ↓
smart-launcher v2.1 三轨制入口
  ┌─────────────────────────────────────┐
  │ [A] 全自动模式 (推荐)               │
  │     URL → 1-2 问题 → 一键到 Preview │
  ├─────────────────────────────────────┤
  │ [B] 手动模式                        │
  │     5 步确认 + DataForSEO 验证      │
  ├─────────────────────────────────────┤
  │ [C] Seed 模式 (选题漏斗)            │
  │     种子词 → 竞品锚定 → 2 个选题    │
  └─────────────────────────────────────┘
       ↓
═══════════════════════════════
▶ 执行阶段 (三条路线共享)
═══════════════════════════════
Writer → Editor Gate → AEO → Framer → Preview
```

---

## 常用命令速查

| 命令 | 用途 |
|------|------|
| `帮我写...` | 启动交互式创作 (推荐) |
| `/write-tutorial` | 教程文章 (1,800-2,500 词) |
| `/write-list` | 榜单文章 (2,500-3,500 词) |
| `/write-roundup` | 案例汇总 (300-600 词) |
| `/analyze-aeo FILE` | AEO 质量评分 |
| `/fetch-transcript URL` | 获取 YouTube 字幕 |

---

## 关键文档

| 优先级 | 文档 | 说明 |
|--------|------|------|
| 1 | `CLAUDE.md` | 主配置，架构和规则 |
| 2 | `LOCAL-SETUP.md` | 环境配置 |
| 3 | `blueprint/02-SKILLS.md` | 所有 Skills 定义 |
| 4 | `docs/PROJECT-LOG-2026-01.md` | 项目管理日志 |

---

## 近期重大更新 (2026-01-21/22)

### 1. 竞品分析 v5.0 完成

**输出**: `/competitive-research/invideo-blog/`
- 6 份分析报告（50 篇标杆文章）
- 37 种标题公式
- 24 种开篇模式
- 20 层产品植入体系

### 2. 三轨制架构 (v2.8 NEW)

- `smart-launcher v2.1`: 统一入口，三种模式选择
- **全自动模式**: URL → 洗稿 80%+ → 一键完成
- **手动模式**: 5 步确认 + DataForSEO 数据展示
- **Seed 模式**: 种子词 → 选题漏斗 → 2 个可执行方向

### 3. Tool Showdown + 竞品验证

- `blog-list-writer v2.4`: 工具对决 10 固定 Headings
- `competitive-validator v1.1`: Top 5 竞品对比 (PASS ≥30%)

---

## 5 条黄金规则

1. **Plan 模式优先** - 复杂任务使用 shift+tab×2
2. **30% 上下文警戒** - 超过就 `/compact`
3. **验证闭环** - 文章必须过 aeo-analyzer (≥75 分)
4. **外部记忆** - 进度写入 `00-implementation.md`
5. **一会话一主题** - 不混合任务

---

## 遇到问题？

1. 查看 `blueprint/09-TROUBLESHOOTING.md`
2. 检查 `docs/PROJECT-LOG-2026-01.md` 了解近期变更
3. Slack: #content-help

---

## 下一步

1. 完成 `LOCAL-SETUP.md` 环境配置
2. 阅读 `CLAUDE.md` 了解完整架构
3. 尝试创建第一篇测试文章
