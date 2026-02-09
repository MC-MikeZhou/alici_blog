# Basecamp Skill 快速开始 🚀

> 5 分钟快速配置指南

---

## 第一步：获取凭据（3 分钟）

1. 访问 https://launchpad.37signals.com/integrations
2. 点击 **"New Integration"**
3. 填写信息：
   - Name: `AliciBlog Agent`
   - Company: `你的公司名`
   - Website: `https://alici.ai`
   - Products: 勾选 **Basecamp 4**
   - Redirect URI: `http://localhost:8888/callback` ⚠️ 必须准确
4. 保存后获取：
   - ✅ **Client ID** (40 字符)
   - ✅ **Client Secret** (40 字符)

---

## 第二步：运行认证（2 分钟）

```bash
cd <PROJECT_ROOT>/skills/utilities/basecamp-link-ops

python3 scripts/oauth_easy.py \
  --client-id "你的_CLIENT_ID" \
  --client-secret "你的_CLIENT_SECRET" \
  --env-file ".env.basecamp"
```

浏览器自动打开 → 点击 **"Yes, I'll allow access"** → 完成！

---

## 第三步：验证（30 秒）

```bash
source .env.basecamp

curl -sS \
  -H "Authorization: Bearer $BC_ACCESS_TOKEN" \
  -H "User-Agent: $BC_USER_AGENT" \
  "https://launchpad.37signals.com/authorization.json"
```

看到你的账户信息 = ✅ 成功！

---

## 开始使用

在 Claude Code 中：

```
请在这个 Basecamp message 下评论：
https://3.basecamp.com/3135399/buckets/42744895/messages/9491566573

评论内容：
测试评论功能
```

---

## 常见问题

**Q: 环境变量没生效？**
```bash
source <PROJECT_ROOT>/skills/utilities/basecamp-link-ops/.env.basecamp
```

**Q: Token 过期了？**
```bash
# 重新运行第二步的命令即可
```

**Q: 需要详细文档？**
查看 [完整安装指南](./INSTALLATION_GUIDE.md)

---

✅ 配置完成！开始使用 Basecamp Skill 吧！
