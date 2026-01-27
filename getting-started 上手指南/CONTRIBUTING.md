# 贡献指南

> 如何为 AliciBlog 项目做贡献

---

## 概述

AliciBlog 是一个 AI 驱动的内容工厂项目，欢迎团队成员贡献代码、文档和改进建议。

---

## 贡献类型

### 1. Skills 开发

创建新的 Skill 或改进现有 Skill。

**位置**: `skills/` 目录下对应分组

**Skill 文件结构**:
```
my-skill/
├── SKILL.md          # 主定义文件（必须）
├── README.md         # 使用说明
└── CHANGELOG.md      # 变更日志
```

**SKILL.md 必需字段**:
```yaml
---
name: my-skill
version: "1.0"
description: Skill 描述
allowed-tools:
  - WebFetch
  - Read
  - Write
---
```

### 2. 文档更新

改进或修正文档。

**关键文档位置**:
- `/CLAUDE.md` - 主配置文件
- `/blueprint/` - 架构文档
- `/skills/_docs/` - 共享文档
- `/skills/` - 所有 Skills

### 3. Bug 修复

修复已知问题。

---

## 提交规范

### Commit 消息格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type**:
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `skill`: Skill 相关更改
- `refactor`: 重构
- `test`: 测试相关

**示例**:
```
feat(skill): add competitive-validator v1.0

- Add Top 5 competitor search
- Add quick AEO scoring
- Add PASS/FAIL judgment

Closes #123
```

### 分支命名

```
<type>/<description>

# 示例
feat/add-competitive-validator
fix/aeo-score-calculation
docs/update-onboarding
```

---

## 开发流程

### 1. 创建分支

```bash
git checkout -b feat/my-feature
```

### 2. 开发与测试

- 遵循现有代码风格
- 测试 Skill 功能
- 确保 AEO 评分通过

### 3. 提交更改

```bash
git add .
git commit -m "feat(skill): add my-feature"
```

### 4. 创建 Pull Request

- 填写 PR 模板
- 指定 Reviewer
- 等待审核

---

## Skill 开发指南

### 版本号规范

使用语义化版本：`MAJOR.MINOR.PATCH`

- **MAJOR**: 不兼容的 API 变更
- **MINOR**: 新增功能（向后兼容）
- **PATCH**: Bug 修复

### 必须包含

- [ ] YAML frontmatter 包含 `name`, `version`, `description`
- [ ] 明确的触发词
- [ ] 输入/输出说明
- [ ] 错误处理
- [ ] 使用示例

### 质量要求

- AEO 分数 ≥ 75（内容类 Skill）
- 文档完整
- 遵循现有命名约定

---

## 代码审查清单

### 通用

- [ ] 代码遵循项目规范
- [ ] 无敏感信息（API 密钥、IP 等）
- [ ] 文档已更新

### Skills

- [ ] 版本号已更新
- [ ] CHANGELOG 已更新
- [ ] 测试通过

---

## 敏感信息处理

**禁止提交**:
- API 密钥
- 密码
- 服务器 IP 地址
- 个人邮箱

**使用占位符**:
```
<YOUR_API_KEY>
<YOUR_SERVER_IP>
<YOUR_EMAIL>
```

---

## 获取帮助

- 查看 `/blueprint/09-TROUBLESHOOTING.md`
- 在 Slack #dev-help 频道提问
- 联系项目维护者

---

*最后更新: 2026-01-21*
