# AI 内容工厂蓝图

> 从"手工坊"到"自动化工厂"的架构升级规划

---

## 文档索引

| 文档 | 说明 | 状态 |
|------|------|------|
| [README.md](./README.md) | 本文件 - 蓝图总览与索引 | 当前 |
| [00-PHILOSOPHY.md](./00-PHILOSOPHY.md) | 工具哲学 - 为什么是 Claude Code + Skills | ✅ |
| [00-CONTENT-PHILOSOPHY.md](./00-CONTENT-PHILOSOPHY.md) | 内容策略哲学 - 博客创作的底层原则 | ✅ 🆕 |
| [01-ARCHITECTURE.md](./01-ARCHITECTURE.md) | 整体架构设计 | ✅ |
| [02-SKILLS.md](./02-SKILLS.md) | Skills 清单与定义 | ✅ |
| [03-AGENTS.md](./03-AGENTS.md) | Agents 清单与定义 | ✅ |
| [04-SOP.md](./04-SOP.md) | SOP 标准操作规程总览 | ✅ |
| [05-IMPLEMENTATION.md](./05-IMPLEMENTATION.md) | 实施计划与优先级 | ✅ |
| [06-COLLABORATION.md](./06-COLLABORATION.md) | 协作模式 - 从人驱动到 Agent 驱动 | ✅ |
| [CHANGELOG.md](./CHANGELOG.md) | 更新日志 | ✅ |

---

## 核心目标

将三条内容生产线（Blog、HitClone、Video Super Agent）从"人驱动"升级为"Agent 驱动"，通过 Skills 组合实现 **70%+ 自动化率**。

---

## 三条生产线

| 生产线 | 产品 | 上游来源 | 输出 |
|--------|------|----------|------|
| **Blog** | SEO/AEO 优化文章 | Twitter/竞品/Deep Research | Framer CMS |
| **HitClone** | YouTube 视频克隆页 | YouTube 热门视频 | alici.ai/youtube-hitclone |
| **Video Super Agent** | AI 短视频 Use Case | 病毒视频/社会热点 | alici.ai/video-super-agent |

---

## 设计原则

```
原则 1：Skill 优先于 Agent
        Skill = 可复用的知识包，被调用时激活，无状态
        Agent = 持续运行的小人，有状态，仅在需要"巡检"或"多步决策"时使用

原则 2：人工节点最小化
        只在战略决策点（选题确认、最终发布）保留人工
        其他环节自动流转，异常时上报

原则 3：共用优先于专用
        先设计三条线共用的基础 Skills
        再设计各产线特化的 Skills
```

---

## 快速导航

### 我想了解...

- **为什么选择这条路？** → [00-PHILOSOPHY.md](./00-PHILOSOPHY.md) (工具哲学)
- **为什么这样创作内容？** → [00-CONTENT-PHILOSOPHY.md](./00-CONTENT-PHILOSOPHY.md) (内容策略哲学) 🆕
- **整体架构是什么样的？** → [01-ARCHITECTURE.md](./01-ARCHITECTURE.md)
- **有哪些 Skills？** → [02-SKILLS.md](./02-SKILLS.md)
- **有哪些 Agents？** → [03-AGENTS.md](./03-AGENTS.md)
- **生产流程怎么走？** → [04-SOP.md](./04-SOP.md)
- **实施计划和优先级？** → [05-IMPLEMENTATION.md](./05-IMPLEMENTATION.md)
- **团队如何协作？** → [06-COLLABORATION.md](./06-COLLABORATION.md)
- **最近更新了什么？** → [CHANGELOG.md](./CHANGELOG.md)

---

## 目录结构

```
/AliciBlog/
├── blueprint/                    # 蓝图文档（本目录）
│   ├── README.md                 # 索引与总览
│   ├── 00-PHILOSOPHY.md          # 产品哲学
│   ├── 01-ARCHITECTURE.md        # 架构设计
│   ├── 02-SKILLS.md              # Skills 清单
│   ├── 03-AGENTS.md              # Agents 清单
│   ├── 04-SOP.md                 # SOP 总览
│   ├── 05-IMPLEMENTATION.md      # 实施计划
│   ├── 06-COLLABORATION.md       # 协作模式
│   └── CHANGELOG.md              # 更新日志
│
├── .claude/
│   ├── skills/                   # Skills 实现
│   │   ├── _shared/              # 共用 Skills
│   │   ├── blog/                 # Blog 专用
│   │   ├── hitclone/             # HitClone 专用
│   │   └── video-super-agent/    # VSA 专用
│   └── agents/                   # Agents 定义
│
├── sop/                          # SOP 标准操作规程
│   ├── blog-production/
│   ├── hitclone-production/
│   └── vsa-production/
│
└── runbooks/                     # 运维手册
```

---

## 联系与反馈

- **负责人**: Hans
- **协作渠道**: Slack
- **更新频率**: 按需更新

---

**版本**: v1.3.0
**创建日期**: 2025-01-11
**最后更新**: 2026-01-18
