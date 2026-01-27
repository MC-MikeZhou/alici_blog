# Claude Code Skills 项目架构文档

> 最后更新: 2026-01-20

---

## 一、项目状态总览

### 当前资产清单

| 类型 | 数量 | 说明 |
|------|------|------|
| Skills | 2 | youtube-transcript-fetcher, twitter-timeline-fetcher |
| Commands | 1 | /fetch-transcript |
| MCP 服务 | 2 | DataForSEO, FAL.ai |
| MCP 插件模板 | 14 | 官方市场预配置 |
| 输出目录 | 2 | reports/transcripts/, reports/项目文件夹/ |

### 已完成的工作

- [x] youtube-transcript-fetcher Skill 开发完成
- [x] twitter-timeline-fetcher Skill 开发完成
- [x] /fetch-transcript 命令配置
- [x] 平台兼容性分析报告
- [x] CLAUDE.md 项目配置文档
- [x] 项目架构文档

---

## 二、系统架构图

### 2.1 整体架构 (High-Level)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         用户交互层                                        │
├─────────────────────────────────────────────────────────────────────────┤
│  Claude Code CLI    │    Claude Desktop    │    Claude.ai Web           │
│  (完整工具支持)       │    (MCP 支持)         │    (纯文本/手动模式)        │
└──────────┬──────────┴─────────┬────────────┴────────────┬───────────────┘
           │                    │                         │
           ▼                    ▼                         ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         触发层 (Trigger Layer)                           │
├─────────────────────────────────────────────────────────────────────────┤
│  Slash Commands          │  触发词 (Trigger Words)      │  自然语言      │
│  /fetch-transcript       │  "抓取字幕", "竞品分析"       │  用户请求      │
└──────────┬───────────────┴─────────────┬────────────────┴───────────────┘
           │                             │
           ▼                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         Skills 执行层                                    │
├─────────────────────────────────────────────────────────────────────────┤
│  youtube-transcript-fetcher    │    twitter-timeline-fetcher            │
│  (Supadata API)                │    (Nitter 镜像)                        │
└──────────┬─────────────────────┴─────────────┬──────────────────────────┘
           │                                   │
           ▼                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         外部服务层 (External APIs)                        │
├─────────────────────────────────────────────────────────────────────────┤
│  Supadata API     │  Nitter 镜像      │  DataForSEO    │  FAL.ai        │
│  (YouTube 字幕)    │  (Twitter 数据)   │  (SEO 数据)     │  (图像生成)     │
└──────────┬────────┴─────────┬─────────┴───────┬────────┴───────┬────────┘
           │                  │                 │                │
           ▼                  ▼                 ▼                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         输出层 (Output Layer)                            │
├─────────────────────────────────────────────────────────────────────────┤
│  /reports/transcripts/     │  /reports/{project}/    │  对话内显示       │
│  YYYY-MM-DD-{video-id}.md  │  timeline-{date}.md     │  格式化内容       │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Skill 调用流程图

```
用户输入
    │
    ▼
┌───────────────────┐
│ 识别触发方式       │
│ - /command        │
│ - 触发词          │
│ - 自然语言        │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐     ┌─────────────────────┐
│ 加载 SKILL.md     │────▶│ 解析 Skill 配置      │
│ 定义文件          │     │ - 触发词            │
└───────────────────┘     │ - 允许的工具         │
                          │ - API 配置          │
                          │ - 执行步骤          │
                          └────────┬────────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    ▼                             ▼
         ┌─────────────────┐           ┌─────────────────┐
         │ 自动模式 (CLI)   │           │ 手动模式 (Web)   │
         │ 直接执行工具     │           │ 输出命令给用户   │
         └────────┬────────┘           └────────┬────────┘
                  │                             │
                  ▼                             ▼
         ┌─────────────────┐           ┌─────────────────┐
         │ 调用外部 API    │           │ 用户手动执行     │
         │ (Bash/WebFetch) │           │ 粘贴结果返回     │
         └────────┬────────┘           └────────┬────────┘
                  │                             │
                  └──────────────┬──────────────┘
                                 ▼
                    ┌─────────────────────┐
                    │ 格式化输出          │
                    │ - 显示在对话中      │
                    │ - 保存到文件        │
                    └─────────────────────┘
```

---

## 三、Skills 详细说明

### 3.1 youtube-transcript-fetcher

**版本**: v1.0

**功能**: 使用 Supadata API 抓取 YouTube 视频的 Transcript (字幕/脚本)

**触发词**:
- "抓取字幕"
- "获取脚本"
- "YouTube transcript"
- "视频字幕"

**平台支持**:
- ✅ **Claude Code CLI**: 完整自动执行
- ✅ **Claude Desktop + MCP**: 完整自动执行
- ⚠️ **Claude.ai 网页版**: 需手动执行 curl 命令

**输入**:
- YouTube URL 或视频 ID
- 可选：语言代码 (如 en, zh, es)

**输出**:
- 对话中显示格式化的字幕内容 (带时间戳)
- **仅 CLI 模式**: 自动保存到 `/reports/transcripts/YYYY-MM-DD-{video-id}.md`
- **网页版**: 需手动保存输出内容
- 文件包含 YAML frontmatter + 带时间戳版本 + 纯文本版本

**使用场景**:
1. 独立使用：快速获取视频字幕内容
2. 作为输入源：为其他 Skill 提供参考素材

**相关命令**: `/fetch-transcript`

**网页版使用流程**:
1. 输入 YouTube URL
2. Claude 生成 curl 命令
3. 用户在终端执行命令
4. 将 JSON 结果粘贴回 Claude
5. Claude 格式化并展示字幕

### 3.2 twitter-timeline-fetcher

**版本**: v1.0

**功能**: 抓取 Twitter/X 账号近 6 个月推文，生成结构化时间线和竞品简报

**触发词**:
- "Twitter 推文"
- "抓取推特"
- "timeline"
- "竞品分析"

**平台支持**:
- ✅ **Claude Code CLI**: 完整自动执行
- ✅ **Claude Desktop + MCP**: 完整自动执行
- ⚠️ **Claude.ai 网页版**: 需手动执行抓取步骤

**输入**:
- Twitter 用户名 (如 @username 或 username)

**输出**:
- 对话中显示统计分析和关键推文
- 自动保存到 `/reports/{project}/{username}-timeline-{date}.md`
- 包含推文统计、主题分类、时间线

**抓取限制**:
- 时间范围：近 6 个月
- 最多 30 页 (约 800 条推文)
- 使用 Nitter 镜像 (无需 API 密钥)

**数据源优先级**:
1. twiiit.com/{username}
2. nitter.tiekoetter.com/{username}
3. xcancel.com/{username}

---

## 四、API 调用详情

### 4.1 API 总览

| API 服务 | 用途 | 调用方式 | 密钥位置 |
|----------|------|----------|----------|
| **Supadata** | YouTube 字幕 | REST API | SKILL.md 内嵌 |
| **Nitter 镜像** | Twitter 数据 | WebFetch | 无需密钥 |
| **DataForSEO** | SEO 关键词 | MCP Server | .mcp.json |
| **FAL.ai** | 图像生成 | 环境变量 | .mcp.json |

### 4.2 YouTube 字幕 API (Supadata)

**端点**: `https://api.supadata.ai/v1/youtube/transcript`

**请求方式**: GET

**Headers**:
```
x-api-key: sd_xxx...
```

**参数**:
| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `videoId` | 否 | YouTube 视频 ID | `dQw4w9WgXcQ` |
| `url` | 否 | 完整 YouTube URL | `https://www.youtube.com/watch?v=xxx` |
| `lang` | 否 | 语言代码 | `en`, `zh`, `es` |
| `text` | 否 | 是否返回纯文本 | `true` |

**响应格式**:
```json
{
  "content": [
    {
      "text": "字幕文本",
      "offset": 8150,
      "duration": 1200
    }
  ],
  "lang": "en",
  "availableLangs": ["en", "zh", "es"]
}
```

**调用流程**:
```
输入: YouTube URL / Video ID
    │
    ▼
┌─────────────────────────────────────────────────────┐
│ GET https://api.supadata.ai/v1/youtube/transcript   │
│ Headers: x-api-key: sd_xxx...                       │
│ Params: videoId=xxx / url=xxx / lang=en / text=true │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│ 响应格式:                                            │
│ {                                                   │
│   "content": [                                      │
│     {"text": "...", "offset": 8150, "duration": 1200}│
│   ],                                                │
│   "lang": "en",                                     │
│   "availableLangs": ["en", "zh", "es"]              │
│ }                                                   │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
输出: /reports/transcripts/YYYY-MM-DD-{video-id}.md
```

### 4.3 Twitter 数据抓取 (Nitter)

**数据源**: Nitter 公共镜像站

**请求方式**: WebFetch (HTML 抓取)

**优先级列表**:
1. `twiiit.com/{username}`
2. `nitter.tiekoetter.com/{username}`
3. `xcancel.com/{username}`

**抓取策略**:
| 参数 | 配置 |
|------|------|
| 时间范围 | 近 6 个月 |
| 最大页数 | 30 页 |
| 最大推文数 | 800 条 |
| 停止条件 | 日期超出 OR 达到限制 |

**抓取流程**:
```
输入: Twitter 用户名
    │
    ▼
┌─────────────────────────────────────────────────────┐
│ 数据源 (按优先级):                                    │
│ 1. twiiit.com/{username}                            │
│ 2. nitter.tiekoetter.com/{username}                 │
│ 3. xcancel.com/{username}                           │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│ 停止条件:                                            │
│ - 推文日期 > 6 个月前                                │
│ - 已抓取 30 页                                       │
│ - 已抓取 800 条推文                                  │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
输出: {username}-timeline-{YYYY-MM-DD}.md
```

**数据提取**:
- 推文内容
- 发布时间
- 互动数据 (点赞、转发、回复)
- 媒体链接

---

## 五、MCP 公共组件

### 5.1 MCP 配置位置

```
/Users/H/
├── Documents/AliciBlog/.mcp.json          # 项目级 MCP 配置 (活跃)
└── .claude/plugins/marketplaces/
    └── claude-plugins-official/
        └── external_plugins/              # 官方插件模板
            ├── github/.mcp.json
            ├── slack/.mcp.json
            ├── supabase/.mcp.json
            └── ... (14 个插件)
```

### 5.2 活跃 MCP 服务

| 服务 | 类型 | 启用模块 | 用途 |
|------|------|----------|------|
| **DataForSEO** | npx MCP | SERP, KEYWORDS_DATA | SEO 关键词分析 |
| **FAL.ai** | 环境变量 | - | 图像生成 |

### 5.3 MCP 架构图

```
┌─────────────────────────────────────────────────────────────┐
│                     MCP 架构                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Claude Code CLI / Desktop                                  │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              MCP 协议层                              │   │
│  │  (Model Context Protocol)                           │   │
│  └──────────────────────┬──────────────────────────────┘   │
│                         │                                   │
│         ┌───────────────┼───────────────┐                  │
│         ▼               ▼               ▼                  │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐           │
│  │ DataForSEO │  │  GitHub    │  │  Slack     │           │
│  │ MCP Server │  │ MCP Server │  │ MCP Server │           │
│  │ (活跃)      │  │ (模板)     │  │ (模板)     │           │
│  └─────┬──────┘  └────────────┘  └────────────┘           │
│        │                                                    │
│        ▼                                                    │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ DataForSEO API                                      │   │
│  │ - SERP 搜索结果                                      │   │
│  │ - Keywords 关键词数据                                │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 5.4 官方 MCP 插件模板

可用但未启用的插件 (位于 `.claude/plugins/marketplaces/claude-plugins-official/external_plugins/`):

| 插件 | 功能 | 配置文件 |
|------|------|----------|
| GitHub | 代码仓库管理 | github/.mcp.json |
| Slack | 消息协作 | slack/.mcp.json |
| Supabase | 数据库操作 | supabase/.mcp.json |
| Linear | 项目管理 | linear/.mcp.json |
| Notion | 知识库 | notion/.mcp.json |
| Google Drive | 文件存储 | google-drive/.mcp.json |
| ... | ... | ... |

---

## 六、目录结构规范

### 6.1 完整目录结构

```
/Users/H/
├── CLAUDE.md                              # 项目主配置 (入口文档)
├── reports/                               # 输出目录
│   ├── transcripts/                       # YouTube 字幕
│   │   └── YYYY-MM-DD-{video-id}.md
│   ├── {project-name}/                    # 项目报告
│   │   └── *.md
│   ├── youtube-skill-platform-analysis.md # 分析报告
│   └── project-architecture.md            # 本架构文档
│
└── .claude/                               # Claude Code 配置根目录
    ├── commands/                          # Slash 命令定义
    │   └── fetch-transcript.md
    ├── skills/                            # Skills 定义
    │   ├── _shared/                       # 共享 Skills
    │   │   └── youtube-transcript-fetcher/
    │   │       ├── SKILL.md
    │   │       └── dist/                  # 发布版本
    │   └── twitter-timeline-fetcher/      # 项目级 Skill
    │       ├── SKILL.md
    │       ├── README.md
    │       └── DEVELOPMENT.md
    ├── plugins/                           # MCP 插件
    │   └── marketplaces/
    │       └── claude-plugins-official/
    │           └── external_plugins/      # 14 个官方插件模板
    └── plans/                             # 计划模式文件
```

### 6.2 命名规范

| 类型 | 命名格式 | 示例 |
|------|----------|------|
| **Skill 目录** | kebab-case | `youtube-transcript-fetcher/` |
| **输出文件** | `YYYY-MM-DD-{标识}.md` | `2026-01-19-dQw4w9WgXcQ.md` |
| **命令文件** | kebab-case.md | `fetch-transcript.md` |
| **项目报告** | `{项目名}/报告名.md` | `AliciBlog/timeline-2026-01-20.md` |

### 6.3 输出文件结构规范

#### YouTube 字幕文件格式

```markdown
---
video_id: dQw4w9WgXcQ
title: 视频标题
url: https://www.youtube.com/watch?v=xxx
language: en
fetched_at: 2026-01-20T10:00:00Z
---

# 视频标题

## 带时间戳版本

[00:00:08] 字幕内容...
[00:00:12] 字幕内容...

## 纯文本版本

字幕内容...
字幕内容...
```

#### Twitter 时间线文件格式

```markdown
---
username: example
fetched_at: 2026-01-20
date_range: 2025-07-20 to 2026-01-20
total_tweets: 456
---

# @example Twitter 时间线

## 统计概览

- 推文数: 456
- 时间范围: 6 个月
- 平均频率: 76 条/月

## 主题分类

### 主题 A (123 条)
- 推文示例...

### 主题 B (89 条)
- 推文示例...

## 完整时间线

### 2026-01-20

**推文内容**
- 互动: 123 likes, 45 retweets
- [原文链接](...)
```

---

## 七、平台兼容性矩阵

| 平台 | 工具能力 | Skill 支持 | MCP 支持 | 自动文件保存 |
|------|----------|-----------|----------|-------------|
| **Claude Code CLI** | ✅ 完整 | ✅ 自动执行 | ✅ 支持 | ✅ 自动 |
| **Claude Desktop + MCP** | ✅ 完整 | ✅ 自动执行 | ✅ 支持 | ✅ 自动 |
| **Claude.ai 网页版** | ❌ 无工具 | ⚠️ 手动模式 | ❌ 不支持 | ❌ 手动保存 |

### 重要说明

⚠️ **关于 Claude.ai 网页版**:

Claude.ai 网页版 (包括 Projects 功能) **无法执行工具或命令**。

当在网页版使用需要 API 调用的 Skills 时:
1. Claude 会生成需要执行的命令 (如 curl)
2. **你需要手动复制命令到终端执行**
3. 将执行结果粘贴回 Claude
4. Claude 会格式化和展示结果

这不是 Bug，而是 Claude.ai 网页版的架构限制。如需自动执行，请使用 Claude Code CLI。

---

## 八、扩展指南

### 8.1 添加新 Skill

1. **创建 Skill 目录**:
   ```bash
   mkdir -p .claude/skills/new-skill-name
   ```

2. **创建 SKILL.md**:
   - 定义触发词
   - 配置允许的工具
   - 编写执行步骤
   - 指定 API 配置

3. **测试**:
   - CLI 模式: 直接使用触发词测试
   - 网页版: 验证手动执行流程

4. **文档更新**:
   - 更新 CLAUDE.md
   - 更新本架构文档

### 8.2 添加新 MCP 服务

1. **配置文件**:
   - 项目级: `/Documents/{project}/.mcp.json`
   - 全局: `~/.claude/plugins/...`

2. **配置格式**:
   ```json
   {
     "mcpServers": {
       "service-name": {
         "command": "npx",
         "args": ["-y", "package-name"],
         "env": {
           "API_KEY": "xxx"
         }
       }
     }
   }
   ```

3. **验证**:
   - 重启 Claude Code CLI
   - 检查 MCP 服务是否加载成功

---

## 九、关键文件清单

| 文件路径 | 用途 | 修改频率 |
|----------|------|----------|
| `/Users/H/CLAUDE.md` | 项目入口文档 | 高 |
| `/Users/H/reports/project-architecture.md` | 本架构文档 | 中 |
| `/Users/H/.claude/skills/_shared/youtube-transcript-fetcher/SKILL.md` | YouTube Skill 定义 | 低 |
| `/Users/H/.claude/skills/twitter-timeline-fetcher/SKILL.md` | Twitter Skill 定义 | 低 |
| `/Users/H/.claude/commands/fetch-transcript.md` | Slash 命令定义 | 低 |
| `/Users/H/Documents/AliciBlog/.mcp.json` | MCP 配置 | 中 |

---

## 十、常见问题 (FAQ)

### Q1: 为什么网页版不能自动执行？

**A**: Claude.ai 网页版是纯文本界面，无法执行系统命令或调用外部 API。这是平台架构的固有限制，不是 Bug。

### Q2: 如何在不同平台间切换？

**A**: Skills 自动适配平台：
- CLI/Desktop: 自动执行模式
- 网页版: 自动切换到手动指导模式

### Q3: MCP 服务和 Skills 有什么区别？

**A**:
- **MCP 服务**: 持久化服务，提供底层工具能力 (如 API 调用)
- **Skills**: 高层次工作流，组合多个工具完成复杂任务

### Q4: 输出文件保存在哪里？

**A**:
- YouTube 字幕: `/reports/transcripts/`
- Twitter 时间线: `/reports/{project-name}/`
- 分析报告: `/reports/`

### Q5: 如何添加新的 API 密钥？

**A**:
- **Skill 内嵌**: 直接在 SKILL.md 中配置
- **MCP 服务**: 在 .mcp.json 的 `env` 字段配置
- **环境变量**: 在系统环境变量中设置

---

## 十一、维护记录

| 日期 | 版本 | 修改内容 | 修改人 |
|------|------|----------|--------|
| 2026-01-20 | v1.0 | 初始架构文档创建 | System |

---

**文档状态**: 🟢 活跃维护

**联系方式**: 参见 CLAUDE.md

**相关文档**:
- [CLAUDE.md](/Users/H/CLAUDE.md) - 项目配置入口
- [youtube-skill-platform-analysis.md](/Users/H/reports/youtube-skill-platform-analysis.md) - 平台兼容性分析
