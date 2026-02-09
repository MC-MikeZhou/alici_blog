# Basecamp Link Ops Skill 安装指南

> 从零开始配置 Basecamp API 集成，实现自动读写 Basecamp 内容

**版本**: v1.0
**更新日期**: 2026-02-08
**预计安装时间**: 10-15 分钟

---

## 📋 目录

1. [前置要求](#前置要求)
2. [步骤 1：创建 Basecamp 集成应用](#步骤-1创建-basecamp-集成应用)
3. [步骤 2：配置 OAuth 认证](#步骤-2配置-oauth-认证)
4. [步骤 3：验证安装](#步骤-3验证安装)
5. [步骤 4：测试功能](#步骤-4测试功能)
6. [常见问题](#常见问题)
7. [故障排除](#故障排除)

---

## 前置要求

### 系统要求
- ✅ macOS / Linux / Windows WSL
- ✅ Python 3.7+
- ✅ curl 命令行工具
- ✅ 网络访问（需要访问 Basecamp 和 37signals）

### 权限要求
- ✅ Basecamp 账户（需要有权限创建集成应用）
- ✅ Basecamp 项目访问权限（Owner 或 Admin）

### 检查 Python 版本
```bash
python3 --version
# 应该显示 Python 3.7 或更高版本
```

---

## 步骤 1：创建 Basecamp 集成应用

### 1.1 访问 37signals Launchpad

在浏览器中打开：
```
https://launchpad.37signals.com/integrations
```

### 1.2 登录你的 37signals 账户

使用你的 Basecamp 账户登录。

### 1.3 创建新集成

1. 点击页面右上角的 **"Register one now"** 或 **"New Integration"** 按钮
2. 填写集成信息：

| 字段 | 填写内容 | 示例 |
|------|---------|------|
| **Name of your application** | AliciBlog Agent | AliciBlog Agent |
| **Company name** | 你的公司名 | Alici |
| **Your website** | 你的网站 URL | https://alici.ai |
| **Products** | 选择 **Basecamp 4** | ✅ Basecamp 4 |
| **Redirect URI** | `http://localhost:8888/callback` | http://localhost:8888/callback |

> ⚠️ **重要**：Redirect URI 必须是 `http://localhost:8888/callback`，这是 OAuth 脚本的默认回调地址。

3. 点击 **"Register this app"** 保存

### 1.4 获取凭据

创建成功后，你会看到：
- ✅ **Client ID**：一串 40 字符的字符串（例如：`0eae9101caaef88da2eb7a9a8928ed17ee50ff80`）
- ✅ **Client Secret**：一串 40 字符的字符串（例如：`56900272b4befcd39989899af997ac6b8d8ee49a`）

> 🔒 **安全提示**：请妥善保管这两个凭据，不要分享给他人或提交到公开代码库。

---

## 步骤 2：配置 OAuth 认证

### 2.1 准备 OAuth 脚本

确认脚本存在：
```bash
cd <PROJECT_ROOT>/skills/utilities/basecamp-link-ops
ls scripts/oauth_easy.py
```

应该显示：
```
scripts/oauth_easy.py
```

### 2.2 运行 OAuth 认证脚本

使用以下命令运行认证脚本（替换成你自己的凭据）：

```bash
cd <PROJECT_ROOT>/skills/utilities/basecamp-link-ops

python3 scripts/oauth_easy.py \
  --client-id "你的_CLIENT_ID" \
  --client-secret "你的_CLIENT_SECRET" \
  --env-file ".env.basecamp"
```

**示例**（使用实际凭据）：
```bash
python3 scripts/oauth_easy.py \
  --client-id "0eae9101caaef88da2eb7a9a8928ed17ee50ff80" \
  --client-secret "56900272b4befcd39989899af997ac6b8d8ee49a" \
  --env-file ".env.basecamp"
```

### 2.3 完成浏览器授权

脚本运行后会：

1. **自动打开浏览器**，显示 Basecamp 授权页面
2. 页面显示：
   ```
   AliciBlog Agent would like to:
   - Access your account information
   - Read and write to your Basecamp projects
   ```
3. **点击绿色按钮**："Yes, I'll allow access"
4. 浏览器会跳转到 `http://localhost:8888/callback?code=...`
5. **脚本自动捕获授权码**并完成认证
6. 看到成功消息：
   ```
   ✅ OAuth 认证成功！
   ✅ Access Token 已保存到 .env.basecamp
   ```

### 2.4 验证配置文件

检查生成的配置文件：
```bash
cat .env.basecamp
```

应该看到类似内容：
```bash
export BC_ACCESS_TOKEN="BAhbB0kiAbB7ImNsaWVudF9pZCI6IjBl..."
export BC_USER_AGENT="AliciAgent2025 (hans@morechinese.cc)"
export BC_CLIENT_ID="0eae9101caaef88da2eb7a9a8928ed17ee50ff80"
export BC_CLIENT_SECRET="56900272b4befcd39989899af997ac6b8d8ee49a"
```

> ✅ **配置完成**！现在可以使用 Basecamp API 了。

---

## 步骤 3：验证安装

### 3.1 加载环境变量

```bash
source <PROJECT_ROOT>/skills/utilities/basecamp-link-ops/.env.basecamp
```

### 3.2 测试 API 连接

运行以下命令测试 API 是否正常工作：

```bash
curl -sS \
  -H "Authorization: Bearer $BC_ACCESS_TOKEN" \
  -H "User-Agent: $BC_USER_AGENT" \
  "https://launchpad.37signals.com/authorization.json"
```

**成功响应示例**：
```json
{
  "expires_at": "2026-02-22T12:51:02Z",
  "identity": {
    "id": 27271865,
    "first_name": "Hans",
    "last_name": "Zhang",
    "email_address": "hans@morechinese.cc"
  },
  "accounts": [
    {
      "product": "bc4",
      "id": 3135399,
      "name": "Alici Growth",
      "href": "https://3.basecampapi.com/3135399"
    }
  ]
}
```

> ✅ 如果看到你的账户信息和项目列表，说明安装成功！

---

## 步骤 4：测试功能

### 4.1 读取 Basecamp Message

测试读取一个 Message 的内容：

```bash
# 示例 URL: https://3.basecamp.com/3135399/buckets/42744895/messages/9491566573
# 转换为 API URL: https://3.basecampapi.com/3135399/buckets/42744895/messages/9491566573.json

curl -sS \
  -H "Authorization: Bearer $BC_ACCESS_TOKEN" \
  -H "User-Agent: $BC_USER_AGENT" \
  "https://3.basecampapi.com/3135399/buckets/42744895/messages/9491566573.json"
```

### 4.2 在 Claude Code 中使用

现在你可以在 Claude Code 中使用 Basecamp Skill 了：

**示例 1：读取文档**
```
请帮我读取这个 Basecamp 文档：
https://3.basecamp.com/3135399/buckets/42744895/documents/9491234567
```

**示例 2：创建评论**
```
请在这个 message 下评论：
https://3.basecamp.com/3135399/buckets/42744895/messages/9491566573

评论内容：
项目进展顺利，已完成 Phase 1，准备进入 Phase 2。
```

**示例 3：创建待办事项**
```
请在这个待办列表中添加任务：
https://3.basecamp.com/3135399/buckets/42744895/todolists/9491234567

任务：完成 AEO 分析报告
```

---

## 常见问题

### Q1: 浏览器没有自动打开怎么办？

**A**: 手动复制脚本输出的 URL 到浏览器中：
```
Please visit this URL to authorize:
https://launchpad.37signals.com/authorization/new?...
```

### Q2: 授权后浏览器显示 "无法访问此网站"？

**A**: 这是正常的！脚本已经捕获了授权码。如果看到 URL 中包含 `?code=...`，说明授权成功。

### Q3: Access Token 过期了怎么办？

**A**: Access Token 有效期为 2 周。过期后重新运行 OAuth 脚本：
```bash
python3 scripts/oauth_easy.py \
  --client-id "你的_CLIENT_ID" \
  --client-secret "你的_CLIENT_SECRET" \
  --env-file ".env.basecamp"
```

### Q4: 如何在新的 Terminal 会话中使用？

**A**: 每次打开新 Terminal 时需要重新加载环境变量：
```bash
source <PROJECT_ROOT>/skills/utilities/basecamp-link-ops/.env.basecamp
```

或者将以下内容添加到 `~/.zshrc` 或 `~/.bashrc`：
```bash
# Basecamp API 环境变量
if [ -f "<PROJECT_ROOT>/skills/utilities/basecamp-link-ops/.env.basecamp" ]; then
  source "<PROJECT_ROOT>/skills/utilities/basecamp-link-ops/.env.basecamp"
fi
```

### Q5: 如何更新 User Agent？

**A**: 编辑 `.env.basecamp` 文件，修改 `BC_USER_AGENT` 行：
```bash
export BC_USER_AGENT="YourAppName (your@email.com)"
```

---

## 故障排除

### 错误 1: `BC_ACCESS_TOKEN 未设置`

**原因**：环境变量没有加载

**解决方案**：
```bash
source <PROJECT_ROOT>/skills/utilities/basecamp-link-ops/.env.basecamp
echo $BC_ACCESS_TOKEN  # 验证是否加载
```

### 错误 2: `401 Unauthorized`

**原因**：Access Token 过期或无效

**解决方案**：重新运行 OAuth 认证
```bash
cd <PROJECT_ROOT>/skills/utilities/basecamp-link-ops
python3 scripts/oauth_easy.py --client-id "..." --client-secret "..." --env-file ".env.basecamp"
```

### 错误 3: `403 Forbidden`

**原因**：没有权限访问该资源

**解决方案**：
1. 确认你的 Basecamp 账户有权限访问该项目
2. 确认 URL 中的 account ID 和 bucket ID 正确

### 错误 4: `404 Not Found`

**原因**：资源 ID 不存在或 URL 格式错误

**解决方案**：
1. 检查 URL 格式是否正确
2. 确认资源 ID 是否有效
3. 参考 URL 转换规则：
   ```
   App URL:  https://3.basecamp.com/ACCOUNT/buckets/BUCKET/messages/ID
   API URL:  https://3.basecampapi.com/ACCOUNT/buckets/BUCKET/messages/ID.json
   ```

### 错误 5: Python 模块缺失

**错误信息**：`ModuleNotFoundError: No module named 'requests'`

**解决方案**：安装依赖
```bash
pip3 install requests
```

---

## 安全最佳实践

### 🔒 保护你的凭据

1. **不要提交凭据到 Git**
   ```bash
   # 确认 .env.basecamp 在 .gitignore 中
   echo ".env.basecamp" >> .gitignore
   ```

2. **限制文件权限**
   ```bash
   chmod 600 .env.basecamp
   ```

3. **定期轮换凭据**
   - 每 3-6 个月更新 Client Secret
   - 在 https://launchpad.37signals.com/integrations 中重新生成

4. **使用环境变量**
   - 生产环境使用环境变量而非文件
   - 不要在代码中硬编码凭据

---

## 进阶配置

### 自动加载环境变量（可选）

将以下内容添加到 `~/.zshrc`（或 `~/.bashrc`）：

```bash
# Basecamp API Auto-load
BASECAMP_ENV="<PROJECT_ROOT>/skills/utilities/basecamp-link-ops/.env.basecamp"
if [ -f "$BASECAMP_ENV" ]; then
  source "$BASECAMP_ENV"
  echo "✅ Basecamp API 环境已加载"
fi
```

保存后重新加载配置：
```bash
source ~/.zshrc
```

### 多账户配置（可选）

如果需要管理多个 Basecamp 账户：

1. 创建多个配置文件：
   ```bash
   .env.basecamp.account1
   .env.basecamp.account2
   ```

2. 使用时指定配置文件：
   ```bash
   source .env.basecamp.account1  # 切换到账户 1
   source .env.basecamp.account2  # 切换到账户 2
   ```

---

## 支持的 Basecamp 资源类型

目前 Skill 支持以下资源类型：

| 资源类型 | 读取 | 写入 | 说明 |
|---------|------|------|------|
| **Messages** | ✅ | ❌ | 读取 Message Board 帖子 |
| **Comments** | ✅ | ✅ | 读取和创建评论 |
| **Documents** | ✅ | ❌ | 读取文档内容 |
| **Vaults** | ✅ | ❌ | 读取文件库（含子文件夹） |
| **Todolists** | ✅ | ❌ | 读取待办列表 |
| **Todos** | ✅ | ✅ | 读取和创建待办事项 |

---

## 下一步

✅ 安装完成后，你可以：

1. **在 Claude Code 中测试**
   - 发送任意 Basecamp URL 给 Claude
   - 请求读取、分析或创建内容

2. **查看 API 文档**
   - Basecamp 4 API: https://github.com/basecamp/bc3-api

3. **扩展功能**
   - 修改 `scripts/oauth_easy.py` 自定义认证流程
   - 添加新的资源类型支持

---

## 致谢

- Basecamp API: https://basecamp.com/
- 37signals: https://37signals.com/

---

**版本历史**:
- v1.0 (2026-02-08): 初始版本，支持基础读写功能

**维护者**: AliciBlog Team
**反馈**: 如有问题请在 Basecamp 项目中提出或联系团队
