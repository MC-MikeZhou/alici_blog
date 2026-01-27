# 03 - Agents 清单

> Agent 定义原则与清单

---

## Agent vs Skill 的区分原则

```
Skill = 可复用的知识包，被调用时激活，无状态
Agent = 持续运行的小人，有状态，仅在需要"巡检"或"多步决策"时使用

原则：能用 Skill 解决的，不用 Agent
```

### 什么时候用 Agent？

Agent 只用于需要以下能力的场景：

| 能力 | 说明 | 示例 |
|------|------|------|
| **持续监控** | 需要定期检查外部状态变化 | 监控 Twitter 热点 |
| **多步决策** | 需要根据中间结果调整后续行动 | 根据筛选结果决定下一步 |
| **状态维护** | 需要记住之前的操作结果 | 记录已处理的内容 |

### 决策矩阵

| 任务 | 形态 | 理由 |
|------|------|------|
| 抓取 Twitter/Reddit 热门 | **Agent** | 需要持续监控变化 |
| 筛选符合标准的内容 | Skill | 规则明确，无状态 |
| 生成文章内容 | Skill | 调用规范，无状态 |
| AEO 评估 | Skill | 一次性评估，无状态 |
| 图片生成 | Skill | 调用 API，无状态 |
| 发布到 Framer | Skill | 流程固定，可脚本化 |
| 监测 SEO 排名变化 | **Agent** | 需要持续监控 |
| 生成数据报告 | Skill | 分析逻辑固定 |

---

## Agents 清单

| Agent | 职责 | 运行方式 | 调用的 Skills |
|-------|------|----------|---------------|
| **scout-agent** | 上游内容侦察 | 定时触发 | seo-keyword-researcher |
| **monitor-agent** | 发布后数据监测 | 定时触发 | analytics-reporter |
| **qa-agent** | 批量质量检查 | 按需触发 | aeo-analyzer, content-formatter |

---

## scout-agent

### 定位

自动侦察上游内容源，发现值得生产的内容线索。

### 职责

1. 定时扫描配置的数据源
2. 按筛选规则过滤内容
3. 生成候选内容清单
4. 推送到 Slack 等待人工确认

### 数据源（待定义）

- Twitter：关注的 AI 领域 KOL
- 竞品博客：HeyGen、Runway 等
- Reddit：相关 subreddit
- ProductHunt：新产品发布

### 运行配置

| 配置项 | 值 |
|--------|---|
| 触发频率 | 每日 / 每周 |
| 输出位置 | Slack #content-queue |
| 状态存储 | 本地 JSON 文件 |

---

## monitor-agent

### 定位

监测已发布内容的效果数据，发现问题和机会。

### 职责

1. 定时收集已发布内容的数据
2. 对比历史数据，识别异常
3. 生成每日/每周报告
4. 异常情况即时上报

### 监测指标

- **SEO**: Google 排名变化、展示量、点击率
- **流量**: PV、UV、停留时间、跳出率
- **转化**: CTA 点击率、注册转化

### 运行配置

| 配置项 | 值 |
|--------|---|
| 触发频率 | 每日 |
| 报告输出 | Slack #daily-digest |
| 异常阈值 | 待定义 |

---

## qa-agent

### 定位

批量检查内容质量，确保符合规范。

### 职责

1. 批量运行 AEO 评分
2. 检查格式是否符合 Schema
3. 识别常见问题
4. 生成质量报告

### 运行配置

| 配置项 | 值 |
|--------|---|
| 触发方式 | 按需 / 发布前 |
| 质量阈值 | AEO >= 75 分 |
| 报告输出 | Slack #content-review |

---

## Agents 目录结构

```
.claude/agents/
├── scout-agent/
│   ├── AGENT.md          # Agent 定义
│   ├── CONFIG.json       # 运行配置
│   └── SOURCES.md        # 数据源清单
│
├── monitor-agent/
│   ├── AGENT.md
│   ├── CONFIG.json
│   └── METRICS.md        # 监测指标定义
│
└── qa-agent/
    ├── AGENT.md
    └── CHECKLIST.md      # 质检清单
```

---

## Agents 统计

| Agent | 状态 | 优先级 |
|-------|------|--------|
| scout-agent | 待建 | Phase 3 |
| monitor-agent | 待建 | Phase 4 |
| qa-agent | 待建 | Phase 2 |

---

**上一篇**: [02-SKILLS.md](./02-SKILLS.md) - Skills 清单与定义
**下一篇**: [04-SOP.md](./04-SOP.md) - SOP 标准操作规程总览
