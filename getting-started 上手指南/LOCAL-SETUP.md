# AliciBlog 本地环境配置

> 15 分钟完成配置 | v2.7 | 2026-01-22

---

## 前置要求

- macOS / Linux
- Node.js 18+
- Claude Code CLI 已安装

---

## 1. 安装 Claude Code CLI

```bash
# 安装 Claude Code
npm install -g @anthropic-ai/claude-code

# 验证安装
claude --version
```

---

## 2. 克隆项目

```bash
# 进入项目目录
cd /Users/H/Documents/AliciBlog

# 验证目录结构
ls -la
# 应该看到: CLAUDE.md, .claude/, reports/, blueprint/
```

---

## 3. API 密钥配置

AliciBlog 使用以下外部服务：

| 服务 | 用途 | 配置位置 |
|------|------|---------|
| **DataForSEO** | 关键词研究 + SERP 数据 | `.mcp.json` |
| **FAL.ai** | 图片生成 (nano-banana-pro) | `.mcp.json` |

### 3.1 获取 API 密钥

**DataForSEO**:
1. 注册 https://dataforseo.com/
2. 获取 Username 和 Password
3. 启用模块: SERP, KEYWORDS_DATA

**FAL.ai**:
1. 注册 https://fal.ai/
2. 创建 API Key
3. 选择模型: nano-banana-pro

### 3.2 配置 .mcp.json

项目已包含 `.mcp.json` 配置文件，结构如下：

```json
{
  "mcpServers": {
    "dataforseo": {
      "command": "npx",
      "args": ["-y", "dataforseo-mcp-server"],
      "env": {
        "DATAFORSEO_USERNAME": "your-username",
        "DATAFORSEO_PASSWORD": "your-password",
        "ENABLED_MODULES": "SERP,KEYWORDS_DATA"
      }
    },
    "fal": {
      "command": "echo",
      "args": ["FAL.ai config - API key stored for image generation"],
      "env": {
        "FAL_API_KEY": "your-api-key"
      }
    }
  }
}
```

**当前配置**:
- DataForSEO 和 FAL.ai 密钥已配置
- 新同事可直接使用现有密钥
- 如需更新密钥，请联系 Hans

---

## 4. 验证配置

启动 Claude Code 并测试各组件：

```bash
cd /Users/H/Documents/AliciBlog
claude
```

### 4.1 测试 DataForSEO

```bash
帮我分析关键词 "AI video generator"
```

预期结果：返回搜索量、竞争度等数据。

### 4.2 测试 Skills 系统

```bash
/fetch-transcript https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

预期结果：返回视频字幕内容。

### 4.3 测试完整工作流

```bash
帮我写一篇简短的测试文章
```

预期结果：smart-root 启动 4 步问卷。

---

## 5. 目录说明

```
/Users/H/Documents/AliciBlog/
├── CLAUDE.md                 # 主配置文件
├── HANDOFF-GUIDE.md          # 交接指南
├── LOCAL-SETUP.md            # 本文件
├── START_HERE.md             # 快速开始
├── ONBOARDING.md             # 详细入门
│
├── .claude/                  # Claude Code 配置
│   ├── skills/               # Skills 定义
│   │   ├── _shared/          # 共享 Skills
│   │   └── blog/             # Blog 专用 Skills
│   └── commands/             # 斜杠命令
│
├── .mcp.json                 # MCP 服务器配置 (API 密钥)
│
├── blueprint/                # 架构文档
│   ├── CHANGELOG.md          # 版本历史
│   ├── 01-ARCHITECTURE.md    # 架构设计
│   ├── 02-SKILLS.md          # Skills 清单
│   └── ...
│
├── reports/                  # 项目输出
│   └── YYYY-MM-DD-{topic}/   # 每个文章的输出目录
│
├── docs/                     # 项目文档
│   └── PROJECT-LOG-2026-01.md # 项目管理日志
│
└── competitive-research/     # 竞品分析输出
    └── invideo-blog/         # invideo 竞品分析 (6 份报告)
```

---

## 6. 常见问题

### Q: Claude Code 无法识别项目

**A**: 确保从项目目录启动：

```bash
cd /Users/H/Documents/AliciBlog && claude
```

### Q: DataForSEO 返回错误

**A**: 检查 `.mcp.json` 中的凭据是否正确。

### Q: 图片生成失败

**A**:
1. 检查 FAL.ai API Key 是否有效
2. 检查网络连接
3. 查看 `scripts/fal_image_generator.py` 日志

### Q: 输出目录不正确

**A**: 所有输出必须在 `/reports/` 目录下，格式为 `YYYY-MM-DD-{topic-slug}`。

---

## 7. 图片生成配置

图片通过 FAL.ai nano-banana-pro 模型生成：

```
生成脚本: /scripts/fal_image_generator.py
上传目标: rsync 到服务器
CDN 地址: https://ct2.alici.ai/static/image/other/gen_images/
```

**API Key 读取优先级**:
1. 环境变量 `FAL_API_KEY`
2. `.mcp.json` 配置文件

---

## 8. 下一步

配置完成后：

1. 阅读 `HANDOFF-GUIDE.md` 了解项目概况
2. 阅读 `CLAUDE.md` 了解完整架构
3. 尝试创建第一篇文章

---

## 联系方式

- 配置问题: 联系 Hans
- Slack: #content-help
