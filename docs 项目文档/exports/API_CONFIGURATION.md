# API Configuration Guide

> AliciBlog 系统 API 配置与环境变量管理指南

---

## 概述

AliciBlog 使用以下外部服务：
- **DataForSEO** - SERP 数据和关键词分析（growth-topic-scout）
- **FAL.ai** - AI 图片生成（editor）

所有 API 密钥通过 `.mcp.json` 文件管理（MCP Server 配置）。

---

## 快速配置

### 第 1 步：复制配置模板

```bash
cd /Users/H/Documents/AliciBlog
cp .mcp.json.example .mcp.json
```

### 第 2 步：填入 API 密钥

编辑 `.mcp.json`，替换占位符：

```json
{
  "mcpServers": {
    "dataforseo": {
      "env": {
        "DATAFORSEO_USERNAME": "YOUR_USERNAME",  ← 替换为你的用户名
        "DATAFORSEO_PASSWORD": "YOUR_PASSWORD"   ← 替换为你的密码
      }
    },
    "fal": {
      "env": {
        "FAL_API_KEY": "YOUR_API_KEY"  ← 替换为你的 API Key
      }
    }
  }
}
```

### 第 3 步：验证配置

运行任意使用 API 的命令测试：

```bash
/scout-topic https://competitor.com/article  # 测试 DataForSEO
/edit-article /path/to/article.md            # 测试 FAL.ai
```

---

## API 密钥获取指南

### DataForSEO

**用途**: SERP 数据、关键词搜索量、竞品分析

**获取步骤**:
1. 访问 [DataForSEO](https://dataforseo.com/)
2. 注册账号并登录
3. 进入 Dashboard → API Access
4. 复制 Username 和 Password
5. 选择付费计划（按需付费，约 $0.001-0.005/请求）

**需要的模块**:
- `SERP` - 搜索结果页数据
- `KEYWORDS_DATA` - 关键词搜索量和竞争度

**成本估算**:
- 选题分析（1 次）: ~$0.02-0.05
- 关键词查询（1 次）: ~$0.01
- 月度预估（50 篇文章）: ~$2-5

### FAL.ai

**用途**: AI 图片生成（Nano Banana Pro 模型）

**获取步骤**:
1. 访问 [FAL.ai](https://fal.ai/)
2. 注册账号并登录
3. 进入 Dashboard → API Keys
4. 创建新 API Key（复制完整 key，格式: `xxx:yyy`）
5. 充值账户（按图片数量计费）

**模型**: `nano-banana-pro`
- 速度: 快（~5-10 秒/图）
- 质量: 高（8K 分辨率）
- 成本: $0.15/图

**成本估算**:
- 单篇文章（3-5 张图）: $0.45-0.75
- 月度预估（50 篇文章）: ~$25-40

---

## 环境变量优先级

系统按以下优先级读取 API 密钥：

```
1. 环境变量（Terminal export）         ← 最高优先级
2. .mcp.json 配置文件                   ← 推荐方式
3. 系统默认值（无）                     ← 无默认值，必须配置
```

### 方式 1: MCP 配置文件（推荐）

**优点**:
- ✅ 持久化存储，会话压缩后自动加载
- ✅ 无需手动 export，Claude Code 自动读取
- ✅ 多环境管理（dev/prod 配置分离）

**配置位置**: `/Users/H/Documents/AliciBlog/.mcp.json`

### 方式 2: 环境变量（不推荐）

**缺点**:
- ❌ 仅在当前终端会话有效
- ❌ 每次重启终端需要重新 export
- ❌ 不适合团队协作

**使用场景**: 临时覆盖配置测试

```bash
export FAL_API_KEY="test-key-xxx"
export DATAFORSEO_USERNAME="test-user"
export DATAFORSEO_PASSWORD="test-pass"
```

---

## 安全注意事项

### ⚠️ 永远不要提交 .mcp.json 到 Git

`.mcp.json` 包含敏感的 API 密钥，绝对不能提交到版本控制系统。

**检查清单**:
- ✅ `.mcp.json` 已添加到 `.gitignore`
- ✅ 使用 `.mcp.json.example` 作为模板（不含真实密钥）
- ✅ 团队成员各自维护自己的 `.mcp.json`

**验证是否泄露**:
```bash
# 检查 .gitignore 是否包含 .mcp.json
grep ".mcp.json" .gitignore

# 检查 git 状态（.mcp.json 不应出现）
git status
```

### 密钥轮换

建议定期更换 API 密钥（每 3-6 个月）：

1. 生成新的 API Key
2. 更新 `.mcp.json`
3. 测试验证
4. 废弃旧密钥

### 团队协作

**不要在飞书/Slack 中分享真实密钥**，使用以下方式：

1. **公司账号共享** - 通过密码管理器（1Password/LastPass）
2. **个人账号** - 各自注册并自行管理
3. **测试环境** - 使用独立的测试密钥

---

## 故障排除

### 问题 1: "API key not found"

**原因**: `.mcp.json` 不存在或格式错误

**解决**:
```bash
# 检查文件是否存在
ls -la .mcp.json

# 检查 JSON 格式是否正确
cat .mcp.json | jq .
```

### 问题 2: "Invalid API key"

**原因**: 密钥错误或已过期

**解决**:
1. 访问 API 提供商控制台
2. 验证密钥是否有效
3. 检查账户余额是否充足
4. 重新生成密钥并更新 `.mcp.json`

### 问题 3: "Module SERP not enabled"

**原因**: DataForSEO 模块未启用

**解决**:
检查 `.mcp.json` 中的 `ENABLED_MODULES`:
```json
"env": {
  "ENABLED_MODULES": "SERP,KEYWORDS_DATA"  ← 必须包含所需模块
}
```

### 问题 4: 图片生成失败（FAL.ai）

**可能原因**:
1. API Key 格式错误（应为 `xxx:yyy` 格式）
2. 账户余额不足
3. 网络连接问题

**解决**:
```bash
# 测试 API 连通性
curl -H "Authorization: Key YOUR_API_KEY" https://fal.ai/api/health

# 检查余额（登录 fal.ai Dashboard）
```

---

## 配置文件参考

### .mcp.json 完整示例

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
        "FAL_API_KEY": "your-api-key:your-secret"
      }
    }
  }
}
```

### 字段说明

| 字段 | 说明 | 必需 |
|------|------|------|
| `mcpServers` | MCP 服务器配置根节点 | ✅ |
| `dataforseo.command` | 启动命令（npx） | ✅ |
| `dataforseo.args` | 命令参数 | ✅ |
| `dataforseo.env.DATAFORSEO_USERNAME` | DataForSEO 用户名 | ✅ |
| `dataforseo.env.DATAFORSEO_PASSWORD` | DataForSEO 密码 | ✅ |
| `dataforseo.env.ENABLED_MODULES` | 启用的模块（逗号分隔） | ✅ |
| `fal.env.FAL_API_KEY` | FAL.ai API 密钥 | ✅ |

---

## 相关文档

- **产品目录**: `/skills/_docs/PRODUCT_CATALOG.md`
- **Skills 文档**: `/blueprint/02-SKILLS.md`
- **故障排除**: `/blueprint/09-TROUBLESHOOTING.md`
- **系统总览**: `/CLAUDE.md`

---

*遇到配置问题？添加到本文档的故障排除章节！*
