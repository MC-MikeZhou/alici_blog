# AliciBlog 新成员入门指南

> 10 分钟快速上手 AliciBlog AI 内容工厂

---

## 一、环境准备

### 1.1 安装 Claude Code CLI

```bash
# macOS/Linux
npm install -g @anthropic-ai/claude-code

# 验证安装
claude --version
```

### 1.2 配置 API 密钥

1. 复制示例配置文件：
   ```bash
   cp .env.example .env
   cp .mcp.json.example .mcp.json
   ```

2. 编辑 `.env` 文件，填入你的 API 密钥：
   - **DataForSEO**: 用于关键词和 SERP 数据
   - **FAL.ai**: 用于图片生成
   - **Supadata**: 用于 YouTube 字幕抓取

3. 编辑 `.mcp.json` 文件，替换占位符为实际密钥

### 1.3 验证配置

```bash
cd /path/to/AliciBlog
claude
```

输入测试命令验证各组件：
```
# 测试 DataForSEO
帮我分析关键词 "AI video generator"

# 测试 Skills 系统
/fetch-transcript https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

---

## 二、核心概念

### 2.1 系统架构

AliciBlog 是一个 AI 驱动的内容工厂，采用分层架构：

```
输入层 → 路由层 → 选题确认层 → 处理层 → 输出层
```

### 2.2 关键组件

| 组件 | 说明 |
|------|------|
| **Skills** | 可复用的功能模块，如 `blog-tutorial-writer` |
| **Capabilities** | 底层能力，如 `youtube-transcript` |
| **MCP Servers** | 外部 API 集成，如 DataForSEO |

### 2.3 核心工作流

1. **SmartRoot 问卷** → 确认内容类型、选题、标题
2. **Writer** → 生成初稿
3. **Editor** → 添加图片、优化格式
4. **AEO Analyzer** → 质量评分（目标 ≥75 分）
5. **Improver** → 自动改进（如需要）
6. **Framer** → 输出 CMS JSON

---

## 三、关键文档

### 必读文档

| 文档 | 位置 | 内容 |
|------|------|------|
| **CLAUDE.md** | `/CLAUDE.md` | 主配置文件，系统架构概览 |
| **设计理念** | `/blueprint/02-PHILOSOPHY.md` | 内容策略哲学 |
| **Skills 清单** | `/blueprint/02-SKILLS.md` | 所有 Skills 定义 |

### 参考文档

| 文档 | 位置 | 内容 |
|------|------|------|
| 架构设计 | `/blueprint/01-ARCHITECTURE.md` | 三层架构详解 |
| 故障排除 | `/blueprint/09-TROUBLESHOOTING.md` | 常见问题解决 |
| 最佳实践 | `/blueprint/07-BEST-PRACTICES.md` | 专家经验总结 |

---

## 四、常用命令

### 4.1 内容创作

| 命令 | 用途 |
|------|------|
| `/smart-root` | 启动交互式内容创作（推荐入口） |
| `/write-tutorial` | 写教程文章 (1,800-2,500 词) |
| `/write-list` | 写榜单文章 (2,500-3,500 词) |
| `/write-roundup` | 写案例汇总 (300-600 词) |

### 4.2 分析工具

| 命令 | 用途 |
|------|------|
| `/analyze-aeo FILE` | AEO 质量评分 |
| `/scout-topic URL` | 竞品选题分析 |
| `/fetch-transcript URL` | 获取 YouTube 字幕 |

### 4.3 输出工具

| 命令 | 用途 |
|------|------|
| `/convert-to-framer FILE` | 转换为 Framer CMS JSON |
| `/preview-framer FILE` | 本地预览 |

---

## 五、5 条黄金规则

1. **Plan 模式优先** - 复杂任务使用 shift+tab×2 进入计划模式
2. **30% 上下文警戒** - 超过 30% 就 `/compact`
3. **验证闭环** - 文章必须通过 `aeo-analyzer` (≥75 分)
4. **外部记忆** - 进度写入 `00-implementation.md`
5. **一会话一主题** - 不混合任务

---

## 六、输出目录

所有输出保存在 `/reports/` 目录：

```
/reports/YYYY-MM-DD-{topic}/
├── 00-implementation.md      # 进度追踪
├── 01-article-draft.md       # 初稿
├── 01-article-edited.md      # 编辑版
├── 03-aeo-score.md           # 评分报告
└── 06-article-final.json     # Framer CMS JSON
```

---

## 七、获取帮助

- **故障排除**: 查看 `/blueprint/09-TROUBLESHOOTING.md`
- **Slack**: 在 #content-help 频道提问
- **文档更新**: 发现问题请更新文档并提交 PR

---

## 八、下一步

1. 阅读 `CLAUDE.md` 了解完整架构
2. 尝试 `/smart-root` 创建一篇测试文章
3. 阅读 `/blueprint/02-PHILOSOPHY.md` 了解内容策略

---

*最后更新: 2026-01-21*
