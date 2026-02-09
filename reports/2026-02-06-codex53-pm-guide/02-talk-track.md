# 15-20 分钟内部分享讲稿：Codex 5.3 + Codex App 多 Agent 实战

> 面向：AI 产品经理  
> 时间锚点：2026-02-06  
> 目标：让团队明白“为什么现在要上多 Agent”，以及“明天就能怎么用”。

## 0. 开场（30 秒）

今天只回答三个问题：
1. GPT-5.3-Codex 的产品意义是什么？
2. Codex App 的多 Agent 体系怎么用？
3. 我们如何在 30 天把它变成可复用流程？

---

## 背景（3 分钟）

### Slide 1：从“模型能力”到“任务能力”

- 过去：我们关注“单次回答质量”。
- 现在：我们关注“任务从输入到发布是否稳定可控”。
- 关键变化：Codex 不只是回答器，而是可执行、可中断、可审计的任务系统。

### Slide 2：为什么是现在

- GPT-5.3-Codex：统一 coding + reasoning 能力，速度更快。
- Codex App：并行任务、云端执行、可中途干预、可审批。
- 对 PM 的直接收益：更快上线试验、更低返工、更可追责。

### Slide 3：一句话定义

**多 Agent 不是“多开几个聊天窗口”，而是把任务拆成有角色、有边界、有验收的流水线。**

---

## 模式（8 分钟）

### Slide 4：能力地图（1 分钟）

- 模型能力：写、推理、总结。
- 运行能力：并行、隔离、自动化。
- 治理能力：审批、规则、沙箱、审计。

### Slide 5：6 种任务模式（3 分钟）

- A 并行探索 + 汇总：竞品研究。
- B 串行内容流水线：Blog/文档。
- C 主 Agent + 专家 Agent：复杂 PRD。
- D 守门员 Agent：事实与合规 gate。
- E 双轨执行：执行轨 + 评审轨。
- F 持续运营：Automations 周期任务。

### Slide 6：Blog/文档默认流水线（2 分钟）

- 研究 Agent -> 大纲 Agent -> 写作 Agent -> 事实核查 Agent -> 编辑 Agent。
- Done 定义：
  - 有来源；
  - 结构符合模板；
  - 有发布前 gate 记录。

### Slide 7：12 条 best practices（2 分钟）

重点口播 4 条高收益：
- 默认 TaskCard 化（避免超长 prompt）。
- 默认 worktree 隔离并行任务。
- 默认 allowlist 联网而不是全网开放。
- 默认加入守门员 Agent 做事实核查。

---

## 案例（6 分钟）

### Slide 8：案例设定（1 分钟）

目标：48 小时内产出《Codex 5.3 产品解读》对外 blog。  
限制：仅引用 OpenAI 官方来源；需中英摘要；需审校记录。

### Slide 9：执行拆解（2 分钟）

- Agent 1（研究）：收集官方证据矩阵。
- Agent 2（结构）：输出提纲和 FAQ。
- Agent 3（写作）：生成长文初稿。
- Agent 4（守门）：核对日期/数字/来源链接。
- Agent 5（编辑）：统一品牌语气和 CTA。

### Slide 10：产出与指标（2 分钟）

- 产出：主稿 + 引用表 + 审校日志。
- 指标：
  - 可追溯率 >=95%
  - 一次通过率 >=70%
  - 从需求到可发布 <=2 天

### Slide 11：复盘（1 分钟）

- 成功因子：任务拆分清晰、守门员后置、审批策略前置。
- 失败模式：不设规则、无 done 定义、把“改方向”混在原任务里。

---

## Q&A（3 分钟）

### 常见问题口径

1. **是不是以后所有文档都只用 5.3-Codex？**  
不是“只用一个模型”，而是“默认用 5.3-Codex 跑主流程；必要时加专用润色模型”。

2. **多 Agent 会不会太重？**  
从双 Agent 起步（写作 + 守门员），先稳定质量，再扩并行。

3. **怎么避免安全风险？**  
最小权限、allowlist 联网、规则先行、审批可审计。

---

## 结束页（30 秒）

下周就能执行的最小动作：
- 选 1 个 Blog 流程上双 Agent；
- 使用 TaskCard + RunPolicy；
- 加入事实核查 gate；
- 用统一模板复盘。

## 官方参考链接（讲稿附录）

- https://openai.com/index/introducing-gpt-5-3-codex/
- https://openai.com/index/introducing-the-codex-app/
- https://developers.openai.com/codex/
- https://developers.openai.com/codex/cloud
- https://developers.openai.com/codex/worktrees
- https://developers.openai.com/codex/agents-md
- https://developers.openai.com/codex/commands/
- https://developers.openai.com/codex/rules
- https://developers.openai.com/codex/automations
