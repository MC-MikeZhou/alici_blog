# YouTube Transcript Skill 无法在 Claude.ai 网页版使用 - 根因分析报告

## 问题描述

用户将 `youtube-transcript-fetcher` Skill 安装到 Claude.ai 网页版（Projects 的 Custom Instructions），但无法实际调用 Supadata API 获取 YouTube 字幕。

---

## 根本原因：Claude.ai 网页版没有工具执行能力

### 核心发现

| 环境 | 工具能力 | API 调用能力 |
|------|----------|--------------|
| **Claude Code CLI** | 有 Bash, WebFetch, Read, Write 等工具 | ✅ 可以执行 curl 或 WebFetch |
| **Claude.ai 网页版** | **无任何工具** | ❌ 只能输出文本，无法执行命令 |

### 技术分析

**Claude.ai 网页版的架构限制：**

1. **纯文本生成模型** - Claude.ai 网页版是一个文本生成界面，没有任何"工具"或"函数调用"能力
2. **无法执行代码** - 即使在 Custom Instructions 中写了 `curl` 命令，Claude 只能将其作为文本输出，无法实际执行
3. **无网络访问** - Claude.ai 网页版无法主动发起 HTTP 请求到外部 API

**当前 Skill 文件的问题（第 64-78 行）：**

```markdown
#### Step 2: 调用 API

使用以下 curl 命令格式（注意：你需要告诉用户执行此命令，或者使用可用的工具）：

curl -X GET "https://api.supadata.ai/v1/youtube/transcript?videoId=VIDEO_ID" \
  -H "x-api-key: sd_fe238b5804c459d03740695389a2eb25"
```

这里说"使用可用的工具"，但 **Claude.ai 网页版根本没有工具可用**。

### 对比：Claude Code CLI 为什么能工作

```
用户请求 → Claude Code CLI → Bash 工具 → 执行 curl → API 返回数据 → 格式化输出
                  ↑
              有工具系统
```

### Claude.ai 网页版为什么不能工作

```
用户请求 → Claude.ai 网页版 → [无工具] → 只能输出 curl 命令文本
                  ↑
              没有工具系统
```

---

## 可行的解决方案

### 方案 1：用户手动执行（当前唯一可行方案）

**流程：**
1. 用户提供 YouTube URL
2. Claude 输出格式化的 `curl` 命令
3. **用户自己在终端执行** curl 命令
4. 用户将 API 返回结果粘贴回 Claude
5. Claude 格式化并展示字幕

**优点：** 不需要任何额外配置
**缺点：** 用户体验差，需要用户手动操作

### 方案 2：等待 Claude.ai 支持 MCP（未来可能）

Anthropic 正在开发 Model Context Protocol (MCP)，未来可能让 Claude.ai 网页版也能连接外部工具服务器。

**现状：** MCP 目前只在 Claude Code CLI 和 Claude Desktop 中可用

### 方案 3：使用 Claude Desktop + MCP

如果用户安装了 Claude Desktop 应用并配置了 MCP 服务器，可以实现自动 API 调用。

**限制：** 需要用户安装桌面应用并配置 MCP

### 方案 4：创建 Web App 中间层

创建一个简单的 Web 应用作为中间层：
1. 用户访问 Web App，输入 YouTube URL
2. Web App 调用 Supadata API
3. 返回格式化的字幕
4. 用户将结果粘贴到 Claude

**缺点：** 需要额外开发和部署

---

## 结论

### 为什么 Skill 在 Claude.ai 网页版不能工作

**根本原因：Claude.ai 网页版是纯文本生成界面，没有工具执行能力，无法发起 HTTP 请求。**

这不是 Skill 文件的问题，不是 API Key 的问题，不是 frontmatter 格式的问题 —— 这是 **Claude.ai 网页版的架构限制**。

### 适用平台对比

| 平台 | 能否使用此 Skill |
|------|------------------|
| Claude Code CLI | ✅ 完全支持 |
| Claude Desktop + MCP | ✅ 可以支持（需配置）|
| Claude.ai 网页版 (Projects) | ❌ **无法自动执行 API 调用** |
| Claude.ai 普通对话 | ❌ 无法自动执行 API 调用 |

### 建议

1. **继续在 Claude Code CLI 中使用此 Skill** - 功能完整
2. **更新网页版文档** - 明确说明这是"辅助指令"而非"自动执行工具"
3. **重新定位网页版 Skill** - 改为"帮助用户生成 curl 命令，用户自行执行"的模式

---

## 下一步行动

1. 更新 Skill 文件，在开头添加平台兼容性说明
2. 更新 CLAUDE.md，明确标注各 Skill 的平台支持情况
3. 考虑创建两个版本的使用指南：
   - Claude Code CLI 版本（自动执行）
   - Claude.ai 网页版（手动执行）

---

**报告生成时间：** 2026-01-20
**分析对象：** youtube-transcript-fetcher Skill v1.0
**结论：** 架构限制，非 Bug，需更新文档说明
