# AliciBlog

> AI 内容工厂 - 70%+ 自动化博客生产

AliciBlog 是一个基于 Claude Code 的 AI 驱动内容生产系统，专为 [alici.ai](https://alici.ai) 设计。

---

## 快速开始

### 1. 环境准备

```bash
# 安装 Claude Code CLI
npm install -g @anthropic-ai/claude-code

# 克隆项目
git clone <repo-url>
cd AliciBlog
```

### 2. 配置 API 密钥

```bash
# 复制示例配置
cp .env.example .env
cp .mcp.json.example .mcp.json

# 编辑配置文件，填入你的 API 密钥
```

### 3. 开始使用

```bash
claude
```

输入自然语言描述或使用命令：
```
帮我写一篇关于 AI 视频生成的教程
```

---

## 项目结构

```
AliciBlog/
├── CLAUDE.md              # Claude Code 主配置（必读）
├── ONBOARDING.md          # 新成员入门指南
├── CONTRIBUTING.md        # 贡献指南
├── .env.example           # 环境变量模板
├── .mcp.json.example      # MCP 配置模板
├── blueprint/             # 架构文档 (17 个)
│   ├── 01-ARCHITECTURE.md # 三层架构设计
│   ├── 02-SKILLS.md       # Skills 清单
│   └── ...
├── .claude/
│   └── skills/_shared/    # 共享 Skills (20 个)
├── reports/               # 输出目录
├── insights/              # Insight Pack 存储
└── case-packs/            # Case Pack 存储
```

---

## 核心功能

### Skills 系统

| 类别 | Skills |
|------|--------|
| **路由** | smart-launcher v2.1 (三轨制入口) |
| **选题** | growth-topic-scout v2.2 (含 Seed Mode 🆕) |
| **写作** | blog-tutorial-writer, blog-list-writer, case-roundup-writer |
| **编辑** | editor, auto-improver |
| **分析** | aeo-analyzer, competitive-validator |
| **输出** | markdown-to-framer, framer-previewer |

### 常用命令

| 命令 | 用途 |
|------|------|
| `/smart-root` | 交互式内容创作（推荐入口） |
| `/write-tutorial` | 写教程文章 |
| `/analyze-aeo FILE` | AEO 质量评分 |
| `/fetch-transcript URL` | 获取 YouTube 字幕 |
| `seed mode [关键词]` | 选题漏斗（从种子词发现 2 个可执行选题）🆕 |

---

## 文档

| 文档 | 说明 |
|------|------|
| [CLAUDE.md](./CLAUDE.md) | 主配置文件，系统架构 |
| [ONBOARDING.md](./ONBOARDING.md) | 新成员 10 分钟入门 |
| [CONTRIBUTING.md](./CONTRIBUTING.md) | 如何贡献代码 |
| [blueprint/](./blueprint/) | 详细架构文档 |

---

## 配置要求

### 必需 API

| API | 用途 | 获取地址 |
|-----|------|----------|
| DataForSEO | 关键词/SERP 数据 | https://dataforseo.com/ |
| FAL.ai | 图片生成 | https://fal.ai/ |
| Supadata | YouTube 字幕 | https://supadata.io/ |

### 配置文件

- `.env` - 环境变量（从 `.env.example` 复制）
- `.mcp.json` - MCP 服务器配置（从 `.mcp.json.example` 复制）

---

## 工作流

```
用户输入 → SmartLauncher v2.1 (三轨制)
             ├── [A] 全自动模式 → URL → Writer → Editor → AEO → 输出
             ├── [B] 手动模式 → DataForSEO → Writer 选择 → 执行
             └── [C] Seed 模式 🆕 → 选题漏斗 → 2 个方向 → Writer → 执行

执行阶段 (三条路线共享):
Writer → Editor Gate → AEO 评分 (≥75 分通过) → Framer → Preview
                         ↓
                    <75 分自动改进
```

---

## 协作指南

1. **新成员**: 阅读 [ONBOARDING.md](./ONBOARDING.md)
2. **贡献代码**: 阅读 [CONTRIBUTING.md](./CONTRIBUTING.md)
3. **了解架构**: 阅读 [CLAUDE.md](./CLAUDE.md)

---

## 版本

- 当前版本: v2.8
- Skills 数量: 20+ (含 Seed Mode)
- Capabilities 数量: 2

---

## 许可证

私有项目 - 仅限团队内部使用

---

*最后更新: 2026-01-25*
