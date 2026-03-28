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
├── CLAUDE.md                    # Claude Code 主配置（必读）
├── CHANGELOG.md                 # 完整版本历史
├── .env.example                 # 环境变量模板
├── .mcp.json.example            # MCP 配置模板
├── skills/                      # Skills 系统
│   ├── _docs/                   # 共享配置文档 (PRODUCT_CATALOG, BRAND_VISUAL_GUIDE 等)
│   ├── core/                    # 核心 Skills (smart-launcher, editor, aeo-analyzer 等)
│   ├── writers/                 # 写作 Skills (tutorial, list, showdown, roundup)
│   │   └── _shared/            # 共享组件 (CTA_CARD, IMAGE_PLACEHOLDER)
│   ├── utilities/               # 工具 Skills (framer, cover-generator, image-sourcer 等)
│   └── monitors/                # 监控 Skills (competitive-validator, trending-monitor)
├── docs 项目文档/                # 架构文档 (17 个)
│   ├── 00-CONTENT-PHILOSOPHY.md # 内容策略哲学
│   ├── 02-SKILLS.md             # Skills 详细定义
│   └── ...
├── getting-started 上手指南/     # 新成员入门
│   └── 08-TEAM-ONBOARDING.md   # 10 分钟上手指南
├── reports 待发文章/             # 文章输出目录
├── scripts/                     # 辅助脚本 (fal_image_generator.py 等)
└── _archive 历史归档/            # 已归档的历史文档
```

---

## 核心功能

### Skills 系统 (21 个)

| 类别 | Skills |
|------|--------|
| **路由** | smart-launcher v2.3 (四轨制入口: 全自动/手动/Seed/深度研究) |
| **选题** | growth-topic-scout v2.4 (含 Seed D1/D2 多样性引擎), art-scout v1.1 (5 Agent 并行深度研究) |
| **写作** | blog-tutorial-writer v3.1, blog-list-writer v3.1, blog-showdown-writer v1.0, case-roundup-writer v1.5 |
| **编辑** | editor v2.9.2, auto-improver v2.2 |
| **分析** | aeo-analyzer v2.4, competitive-validator v1.1 |
| **输出** | markdown-to-framer v1.3, framer-previewer v1.1, chinese-previewer v1.1 |
| **工具** | youtube-transcript-fetcher v1.1, blog-cover-generator v1.0, image-sourcer v1.0, batch-processor v1.1, basecamp-link-ops v1.0 |
| **监控** | trending-monitor v1.1 |

### 常用命令

| 命令 | 用途 |
|------|------|
| `/full-workflow URL` | 完整流程（推荐入口） |
| `/batch-workflow URLs` | 批量处理多个 URL |
| `/scout-topic URL` | 选题发现 |
| `/write-tutorial` | 写教程文章 (1,800-3,500 词) |
| `/write-list` | 写榜单文章 (4,500-10,000 词) |
| `/write-roundup` | 案例汇总小博文 (300-600 词) |
| `/edit-article FILE` | 图片 + 优化 |
| `/analyze-aeo FILE` | AEO 质量评分 |
| `/improve-article FILE` | 自动改进 |
| `/preview-chinese FILE` | 中文预览 |
| `/convert-to-framer FILE` | 输出 CMS JSON |
| `/fetch-transcript URL` | 获取 YouTube 字幕 |
| `/generate-cover FILE` | 生成封面图 (6 种背景类型) |
| `seed mode [关键词]` | 选题漏斗 D1（竞品锚定：从种子词发现 2 个可执行方向） |
| `seed mode v2 [关键词]` | 选题漏斗 D2（多样性引擎：从种子词发现 3 个可执行方向） |

---

## 工作流

```
用户输入 → SmartLauncher v2.3 (四轨制)
             ├── [A] 全自动模式 → URL → Writer → Editor → AEO → 输出
             ├── [B] 手动模式 → DataForSEO → Writer 选择 → 执行
             ├── [C] Seed 模式 → 选题漏斗（D1=2 / D2=3）→ Writer → 执行
             └── [D] 深度研究 → art-scout (5 Agent) → Direction → Writer → 执行

执行阶段 (四条路线共享):
Writer → Editor Gate → AEO 评分 (≥75 分通过) → 竞品验证 → Framer → Preview
                         ↓
                    <75 分自动改进
```

---

## 文档

| 文档 | 说明 |
|------|------|
| [CLAUDE.md](./CLAUDE.md) | 主配置文件，系统架构 |
| [CHANGELOG.md](./CHANGELOG.md) | 完整版本历史 |
| [docs 项目文档/](./docs%20项目文档/) | 详细架构文档 |
| [getting-started 上手指南/08-TEAM-ONBOARDING.md](./getting-started%20上手指南/08-TEAM-ONBOARDING.md) | 新成员 10 分钟入门 |

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

## 协作指南

1. **新成员**: 阅读 [08-TEAM-ONBOARDING.md](./getting-started%20上手指南/08-TEAM-ONBOARDING.md)
2. **了解架构**: 阅读 [CLAUDE.md](./CLAUDE.md)
3. **版本历史**: 阅读 [CHANGELOG.md](./CHANGELOG.md)

---

## 版本

- 当前版本: v3.0
- Skills 数量: 21
- Capabilities 数量: 2

---

## 许可证

私有项目 - 仅限团队内部使用

---

*最后更新: 2026-02-08*
