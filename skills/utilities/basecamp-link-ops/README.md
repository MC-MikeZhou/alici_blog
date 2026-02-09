# Basecamp Link Ops

> Basecamp 4 API 集成 Skill - 在 Claude Code 中直接读写 Basecamp 内容

---

## 📖 快速导航

| 文档 | 说明 | 适合人群 |
|------|------|---------|
| **[快速开始](./QUICKSTART.md)** | 5 分钟配置指南 | 🚀 想快速开始的用户 |
| **[完整安装指南](./INSTALLATION_GUIDE.md)** | 详细步骤、故障排除、最佳实践 | 📚 需要深入了解的用户 |
| **[Skill 定义](./SKILL.md)** | API 映射、工作流、安全规则 | 🛠️ 开发者和维护者 |

---

## ⚡ 功能特性

### 已支持 ✅

- ✅ **读取** Messages / Comments / Documents / Vaults / Todolists / Todos
- ✅ **创建** Comments / Todos
- ✅ **OAuth 2.0 认证**（自动化脚本，无需手动复制粘贴）
- ✅ **URL 自动解析**（支持 Basecamp App URLs）
- ✅ **递归读取**（Vaults 子文件夹、文档层级）

### 计划支持 🚧

- 🚧 更新 Todos 状态
- 🚧 创建和更新 Documents
- 🚧 上传附件
- 🚧 搜索功能

---

## 🎯 使用场景

### 1. 自动化内容分析
```
请帮我分析这个 Basecamp 文档中的项目进度：
https://3.basecamp.com/3135399/buckets/42744895/documents/9491234567
```

### 2. 批量创建待办事项
```
请在这个待办列表中添加以下任务：
https://3.basecamp.com/3135399/buckets/42744895/todolists/9491234567

任务列表：
1. 完成 AEO 分析
2. 更新 B4 文章
3. 生成封面图
```

### 3. 智能回复讨论
```
请在这个 message 下评论，总结一下 toolkit.video 的 AEO 价值：
https://3.basecamp.com/3135399/buckets/42744895/messages/9491566573
```

### 4. 提取文档结构
```
请列出这个 Vault 下所有文档的标题：
https://3.basecamp.com/3135399/buckets/42744895/vaults/9491234567
```

---

## 🔧 安装

### 前置要求
- Python 3.7+
- Basecamp 4 账户
- Basecamp 项目访问权限

### 快速安装（5 分钟）

1. **获取凭据**
   - 访问 https://launchpad.37signals.com/integrations
   - 创建新集成，获取 Client ID 和 Client Secret

2. **运行认证**
   ```bash
   cd <PROJECT_ROOT>/skills/utilities/basecamp-link-ops

   python3 scripts/oauth_easy.py \
     --client-id "你的_CLIENT_ID" \
     --client-secret "你的_CLIENT_SECRET" \
     --env-file ".env.basecamp"
   ```

3. **验证**
   ```bash
   source .env.basecamp
   curl -sS \
     -H "Authorization: Bearer $BC_ACCESS_TOKEN" \
     -H "User-Agent: $BC_USER_AGENT" \
     "https://launchpad.37signals.com/authorization.json"
   ```

**详细步骤请查看**: [完整安装指南](./INSTALLATION_GUIDE.md)

---

## 📚 API 参考

### URL 映射

Basecamp App URL → API URL 转换规则：

| App URL | API URL |
|---------|---------|
| `https://3.basecamp.com/ACCOUNT/buckets/BUCKET/messages/ID` | `https://3.basecampapi.com/ACCOUNT/buckets/BUCKET/messages/ID.json` |
| `https://3.basecamp.com/ACCOUNT/buckets/BUCKET/documents/ID` | `https://3.basecampapi.com/ACCOUNT/buckets/BUCKET/documents/ID.json` |
| `https://3.basecamp.com/ACCOUNT/buckets/BUCKET/todolists/ID` | `https://3.basecampapi.com/ACCOUNT/buckets/BUCKET/todolists/ID.json` |
| `https://3.basecamp.com/ACCOUNT/buckets/BUCKET/vaults/ID` | `https://3.basecampapi.com/ACCOUNT/buckets/BUCKET/vaults/ID.json` |

### 支持的操作

| 资源类型 | GET (读取) | POST (创建) | PATCH (更新) | DELETE (删除) |
|---------|-----------|------------|-------------|--------------|
| Messages | ✅ | ❌ | ❌ | ❌ |
| Comments | ✅ | ✅ | ❌ | ❌ |
| Documents | ✅ | ❌ | ❌ | ❌ |
| Vaults | ✅ | ❌ | ❌ | ❌ |
| Todolists | ✅ | ❌ | ❌ | ❌ |
| Todos | ✅ | ✅ | 🚧 | ❌ |

---

## 🔒 安全

### 环境变量
```bash
BC_ACCESS_TOKEN      # OAuth Access Token (2 周有效期)
BC_USER_AGENT        # User Agent (格式: AppName (email@example.com))
BC_CLIENT_ID         # OAuth Client ID
BC_CLIENT_SECRET     # OAuth Client Secret
```

### 最佳实践
1. ✅ 不要提交 `.env.basecamp` 到 Git
2. ✅ 使用 `chmod 600 .env.basecamp` 限制权限
3. ✅ 定期轮换 Client Secret（3-6 个月）
4. ✅ 仅在需要时加载环境变量

---

## 🐛 故障排除

### 常见错误

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| `BC_ACCESS_TOKEN 未设置` | 环境变量未加载 | `source .env.basecamp` |
| `401 Unauthorized` | Token 过期或无效 | 重新运行 OAuth 认证 |
| `403 Forbidden` | 没有权限 | 检查 Basecamp 账户权限 |
| `404 Not Found` | 资源不存在 | 检查 URL 格式和 ID |

**详细故障排除**: [完整安装指南 - 故障排除章节](./INSTALLATION_GUIDE.md#故障排除)

---

## 📦 文件结构

```
basecamp-link-ops/
├── README.md                    # 📖 本文件（主入口）
├── QUICKSTART.md                # 🚀 5 分钟快速开始
├── INSTALLATION_GUIDE.md        # 📚 完整安装指南
├── SKILL.md                     # 🛠️ Skill 定义和 API 规范
├── scripts/
│   └── oauth_easy.py            # OAuth 认证脚本
└── .env.basecamp               # 🔒 环境变量配置（不提交到 Git）
```

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

**改进建议**：
- 添加更多资源类型支持（Schedules, Campfire, etc.）
- 实现批量操作 API
- 添加缓存机制
- 支持 Webhook 集成

---

## 📄 许可

本项目遵循 MIT 许可证。

---

## 🔗 相关链接

- [Basecamp 4 API 文档](https://github.com/basecamp/bc3-api)
- [37signals OAuth 指南](https://github.com/basecamp/api/blob/master/sections/authentication.md)
- [AliciBlog 项目](https://alici.ai)

---

**版本**: v1.0
**最后更新**: 2026-02-08
**维护者**: AliciBlog Team

---

💡 **提示**: 如果这是你第一次使用，建议从 [快速开始](./QUICKSTART.md) 开始！
