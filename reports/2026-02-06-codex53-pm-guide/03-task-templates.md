# Codex 多 Agent 任务模板包（6 个）

> 目标：直接复制模板即可执行。  
> 建议：每个任务先填 TaskCard，再选对应模板。

## 通用 TaskCard（复制即用）

```yaml
TaskCard:
  id: ""
  objective: ""
  inputs: []
  constraints: []
  tools_allowed: []
  approval_policy: "on-request"
  done_definition: []
  output_format: "markdown"
  reviewer: ""

RunPolicy:
  execution_mode: "staged"
  sandbox_level: "strict"
  internet_access: "allowlist"
  interruption_points:
    - "after_outline"
    - "before_publish"
  escalation_rules:
    - "request approval before network expansion"
```

---

## 模板 1：Blog 生产模板（默认 5 Agent）

### 输入清单

- 主题与目标受众
- 期望关键词/叙事角度
- 允许引用域名列表
- 品牌语气与禁用表达
- 发布截止时间

### 步骤

1. 研究 Agent：整理证据矩阵（主张-证据-链接）。
2. 大纲 Agent：产出标题、H2 结构、FAQ。
3. 写作 Agent：输出首稿（含引用占位）。
4. 事实核查 Agent：核对数字、日期、链接可达性。
5. 编辑 Agent：统一语气与 CTA，输出发布稿。

### 质量门

- 所有关键结论可回链。
- 文稿结构符合约定模板。
- 含风险注记（不确定项/推断项）。

### 失败回退

- 若事实核查失败：退回写作 Agent，仅重写问题段落。
- 若口径冲突：回退到大纲 Agent 重建框架。

### 输出格式

- `final_blog.md`
- `citations.md`
- `review_log.md`

---

## 模板 2：PRD 草拟模板（主 Agent + 专家 Agent）

### 输入清单

- 商业目标与 KPI
- 用户画像与核心场景
- 现状流程与约束
- 非目标范围

### 步骤

1. 主 Agent：定义 PRD 目录与成功标准。
2. 专家 Agent（技术）：评估可行性与依赖。
3. 专家 Agent（数据）：定义埋点与指标口径。
4. 专家 Agent（合规）：检查风险和审批要求。
5. 主 Agent：汇总为统一 PRD，并标记开放问题。

### 质量门

- 每个需求有验收标准。
- 每个指标有计算口径。
- 每个风险有 owner 和缓解动作。

### 失败回退

- 若可行性不足：回退需求范围（P0/P1 重分级）。
- 若指标不可测：强制补埋点方案后再合并。

### 输出格式

- `prd_v1.md`
- `open_questions.md`
- `risk_register.md`

---

## 模板 3：竞品调研模板（并行探索 + 汇总）

### 输入清单

- 竞品名单（3-10 个）
- 调研维度（定价/功能/增长/内容策略）
- 时间窗口（例如最近 90 天）

### 步骤

1. 研究 Agent A：产品功能与定价。
2. 研究 Agent B：内容与分发策略。
3. 研究 Agent C：用户反馈与口碑信号。
4. 汇总 Agent：合并结论，输出机会点与风险点。

### 质量门

- 每个结论包含证据级别（高/中/低）。
- 区分事实与推断。
- 保留冲突观点，不强行统一。

### 失败回退

- 若证据不足：返回对应研究 Agent 补源。
- 若观点冲突过高：新增“假设验证清单”。

### 输出格式

- `competitor_matrix.md`
- `opportunity_map.md`
- `evidence_table.md`

---

## 模板 4：Bug Triage 模板（执行轨 + 评审轨）

### 输入清单

- bug 列表（严重级、影响范围、复现率）
- 当前 sprint 容量
- 发布窗口与冻结期

### 步骤

1. 执行轨 Agent：按影响/紧急度排序。
2. 评审轨 Agent：验证排序合理性与漏项。
3. 合并 Agent：形成本周修复清单与延后清单。

### 质量门

- 每个 bug 有优先级依据。
- P0/P1 有明确 owner 与截止时间。
- 延后项有业务影响说明。

### 失败回退

- 若争议大：回退到复现数据补证据。
- 若容量不够：重新切分为 hotfix 与 backlog。

### 输出格式

- `triage_board.md`
- `fix_plan.md`
- `defer_rationale.md`

---

## 模板 5：发布前检查模板（守门员优先）

### 输入清单

- 待发布内容/功能清单
- 版本说明与变更列表
- 风险等级定义

### 步骤

1. 守门员 Agent（事实）：检查版本号、日期、声明准确性。
2. 守门员 Agent（合规）：检查敏感表述和权限边界。
3. 编辑 Agent：合并修订并输出最终发布包。

### 质量门

- 0 个高风险未解决项。
- 所有外链可访问。
- 回滚步骤可执行。

### 失败回退

- 存在高风险项：直接阻断发布。
- 回滚方案缺失：退回产品/工程补齐。

### 输出格式

- `release_checklist.md`
- `go_no_go.md`
- `rollback_plan.md`

---

## 模板 6：周报复盘模板（Automation Loop）

### 输入清单

- 本周目标与实际结果
- 核心指标（流量/转化/质量/效率）
- 本周关键事件与异常

### 步骤

1. 自动收集 Agent：拉取指标与任务日志。
2. 分析 Agent：输出达成率、偏差原因、趋势变化。
3. PM Agent：形成下周行动清单与实验计划。

### 质量门

- 指标有对比基线（周环比/月环比）。
- 异常项有 root cause 假设。
- 下周行动项可执行且可验证。

### 失败回退

- 指标口径不一致：暂停结论，先统一定义。
- 数据缺失：标记置信度并限制决策范围。

### 输出格式

- `weekly_report.md`
- `kpi_snapshot.md`
- `next_week_actions.md`

---

## 附：模板执行时的默认治理策略

- 默认最小权限。
- 默认 allowlist 联网。
- 默认启用审批记录。
- 默认对外发布材料走“事实核查 gate”。

## 官方参考

- https://developers.openai.com/codex/
- https://developers.openai.com/codex/worktrees
- https://developers.openai.com/codex/commands/
- https://developers.openai.com/codex/rules
- https://developers.openai.com/codex/agents-md
- https://developers.openai.com/codex/automations
