---
name: bc-sync-engine
version: "2.1"
description: >
  Basecamp 4 Pull + Push 同步引擎。读取和写入 Basecamp 内容，将 Agent 产出推到 BC 供人类在浏览器阅读。
  合并自 basecamp-link-ops (Pull) + bc-project-launcher (Push 部分) + bc_push.sh。
  触发词: basecamp url, bc链接, 读取basecamp, bc push, bc comment, bc todo, bc 同步.
allowed-tools: Bash, Read, Write, AskUserQuestion
env-required: [BC_ACCESS_TOKEN, BC_USER_AGENT]
env-optional: [BC_REFRESH_TOKEN, BC_CLIENT_ID, BC_CLIENT_SECRET, BC_ACCOUNT, BC_BUCKET]
---

# BC Sync Engine v2.1

> Pull + Push — Agent 与人类之间的 Basecamp 桥梁

## 为什么

Agent 产出（MD 文件、文件夹、CLI 输出）和人类阅读方式（浏览器、中文翻译插件）之间有一道鸿沟。BC Sync Engine 用 Basecamp 作为桥梁：Agent 推到 BC，人类在浏览器阅读。

## 前置条件

1. `BC_ACCESS_TOKEN` + `BC_USER_AGENT` — 必需
2. `BC_REFRESH_TOKEN` + `BC_CLIENT_ID` + `BC_CLIENT_SECRET` — 推荐（自动刷新）
3. `BC_ACCOUNT` + `BC_BUCKET` — 推荐（省去每次传参）
4. 以上均从 `.env.basecamp` 自动加载

### OAuth 设置

```bash
cd scripts/
python3 oauth_easy.py --env-file "../.env.basecamp"
```

## Pull（读取）

### bc_read_link.py

从 Basecamp App URL 拉取内容到本地。

```bash
python3 scripts/bc_read_link.py "https://3.basecamp.com/3135399/buckets/46059256/todolists/9571811788" \
  --out /tmp/bc-output
```

支持资源类型: documents, vaults, todolists, messages, uploads

输出结构:
```
/tmp/bc-output/
├── 01-raw/          # 原始 API 响应
├── 02-normalized/   # context.json（结构化数据）
└── 03-digest/       # context.md（人类可读摘要）
```

## Startup（启动项）

### bc_startup.py（推荐默认入口）

新博文项目建议从启动项进入：先 Pull 建立本地快照，再按模式执行写回。

```bash
python3 scripts/bc_startup.py \
  --list-url "https://3.basecamp.com/<account>/buckets/<bucket>/todolists/<id>" \
  --mode bidirectional
```

模式:
- `readonly`: 只 Pull，不写回
- `bidirectional`: Pull + 写回（评论 + 3 个模板 todo）

幂等规则（默认）:
- marker: `[BC-STARTUP-V2|YYYY-MM-DD|LIST_ID]`
- 若评论已包含同 marker: 跳过评论写入
- 若同名模板 todo 已存在: 跳过该 todo 创建

输出:
- `startup-report.json`（created/skipped/errors/degraded）

## Push（写入）

### bc_write.py — 6 个命令

所有命令从 `.env.basecamp` 读取 `BC_ACCOUNT`/`BC_BUCKET`，也可通过 `--account`/`--bucket` 覆盖。

#### 1. create-comment（P0 — 最常用）

在任何 recording 上贴评论。支持 **todolist + todo + document** 三种 recording 类型。用于版本标记、进度更新、反向链接。

```bash
# 文本评论
python3 scripts/bc_write.py create-comment <recording_id> "[BC-V2.0] bc-sync-engine shipped"

# MD 文件转 HTML 评论
python3 scripts/bc_write.py create-comment <recording_id> ./plan.md

# HTML 文件
python3 scripts/bc_write.py create-comment <recording_id> ./report.html
```

#### 2. create-todo（P0）

在 todolist 中创建 todo，可选附带 MD/HTML notes。

```bash
# 简单 todo
python3 scripts/bc_write.py create-todo <list_id> "实施 bc-sync-engine v2.0"

# 带 notes 的 todo
python3 scripts/bc_write.py create-todo <list_id> "v2.0 实施记录" --notes-file ./implementation.md
```

#### 3. create-sublist（P1）

在 todolist 中创建子分组。

```bash
python3 scripts/bc_write.py create-sublist <list_id> "Phase 1: 核心基础设施"
```

#### 4. create-doc（P1）

推 MD 文件为 BC Document（浏览器可读 + 翻译插件友好）。

```bash
python3 scripts/bc_write.py create-doc <vault_id> "BC Sync Engine 设计文档" ./design.md
```

#### 5. create-folder（P1）

在 Docs & Files vault 中创建文件夹。可嵌套（folder ID 也可作为 parent）。

```bash
python3 scripts/bc_write.py create-folder <vault_id> "v2.1"
```

> **提示**: `create-doc` 天然支持在文件夹中创建文档 — 把 folder ID 当作 vault_id 传入即可。

#### 6. update-todo（P1）

标记 todo 完成/未完成。

```bash
python3 scripts/bc_write.py update-todo <todo_id> --complete
python3 scripts/bc_write.py update-todo <todo_id> --uncomplete
```

### 输出格式

所有命令成功后输出 JSON:
```json
{"ok": true, "id": 12345, "app_url": "https://3.basecamp.com/...", "type": "comment"}
```

失败时 stderr 输出:
```json
{"ok": false, "status": 422, "action": "create-comment", "body": "..."}
```

## 内容输入规则

`content` 参数支持 4 种输入:
| 输入 | 处理 |
|------|------|
| 纯文本字符串 | 包裹在 `<p>` 标签 |
| `.md` 文件路径 | 自动转 HTML（headers/lists/code/bold/italic） |
| `.html` 文件路径 | 直接使用 |
| `-` | 从 stdin 读取 |

## URL-to-API Mapping

App URL: `https://3.basecamp.com/<account>/buckets/<bucket>/<resource>/<id>`
API URL: `https://3.basecampapi.com/<account>/buckets/<bucket>/<resource>/<id>.json`

## 安全规则

1. 不在输出中暴露 `BC_ACCESS_TOKEN` 或 `Client Secret`
2. 写操作前确认目标（除非用户已明确意图）
3. 写操作返回 created object id + app_url
4. `.env.basecamp` 权限设为 600

## 工作流约定 (v2.1)

### 版本化项目管理模式

每个版本迭代（如 v2.1）在 BC 中对应一个子列表 + 文档文件夹:

```
Todo List (主列表)
├── 🔄 v2.0 方向         ← 子列表 (已完成的版本)
├── ✅ v2.0 实施记录      ← 子列表 (归档)
├── 🔄 v2.1 需求与进展    ← 子列表 (当前版本)
│   ├── Todo: 需求 A
│   ├── Todo: 需求 B
│   └── ...
└── ...

Docs & Files vault
├── v2.0/                  ← 文件夹
│   └── SKILL v2.0 定义
├── v2.1/                  ← 文件夹
│   └── SKILL v2.1 定义
└── ...
```

### 评论分流策略

| 信息类型 | 评论位置 | 示例 |
|---------|---------|------|
| 版本进展更新 | 版本子列表 | "v2.1 create-folder 测试通过" |
| 单个需求进展 | 对应的 Todo | "API 端点验证成功" |
| 重大问题/决策 | 主列表 | "方向变更: 取消 diff 引擎" |
| 版本总结 | 主列表 | "v2.1 shipped — 6 个命令" |

### 反向链接约定

创建 Doc 后，必须在关联的 Todo/子列表发一条评论包含链接:

```markdown
📄 文档已推送: [SKILL v2.1 定义](https://3.basecamp.com/3135399/buckets/.../documents/XXXXX)
```

### 版本号约定

- 功能迭代以 **0.1** 为单位（v2.0 → v2.1 → v2.2）
- 修复/微调以 **0.0.1** 为单位（v2.1 → v2.1.1）
- 每个版本在 BC 子列表标题中标注版本号

## 明确不做的事

- Clarity Score / Shape 对话 / 项目类型检测（v1.0 教训）
- 自动轮询 / 定时同步
- Diff 引擎 / 增量同步（v2.2+）
- @mention 通知（v2.2+）
