# Codex 5.3 + Codex App 多 Agent PM Playbook（从零起步）

> 版本时间锚点：2026-02-06（美国时间）  
> 受众：AI 产品经理（含非工程背景）  
> 目标：把“模型能力提升”转化为“可复用的任务编排能力”

## 为什么是现在（截至 2026-02-06 的官方信息）

- GPT-5.3-Codex 是面向执行型工作的统一模型，官方表述为整合了 GPT-5.2-Codex 的编码能力与 GPT-5.2 的推理/知识能力，并且响应速度更快（官方描述约 25%）。
- Codex App 在 2026-02-02 发布后，产品形态从“单次问答”升级为“可持续运行的任务工作台”，支持并行任务、可中断干预、review、审批与自动化。
- 对 PM 的核心变化不是“写代码更强”，而是“任务可拆分、可治理、可度量”。这使 blog/文档/PRD/缺陷治理等知识工作都能进入标准化流水线。

## 证据底座（主张-证据-链接）

| 主张 | 官方证据 | 链接 |
|---|---|---|
| GPT-5.3-Codex 为统一模型，强调 coding + reasoning 合并与更快响应 | OpenAI 发布文案：整合 GPT-5.2-Codex 与 GPT-5.2，并提到更快 | https://openai.com/index/introducing-gpt-5-3-codex/ |
| Codex App 支持并行任务与中途干预 | 发布文案写明可并行运行多个任务，且任务中可发送后续消息调整方向 | https://openai.com/index/introducing-the-codex-app/ |
| Codex cloud task 支持共享与可继续执行 | Cloud Tasks 文档说明可分享任务链接、跨设备继续任务 | https://developers.openai.com/codex/cloud |
| Worktree 是隔离并行执行核心机制 | Worktrees 文档描述每个任务在独立 worktree 中执行，避免冲突 | https://developers.openai.com/codex/worktrees |
| 审批与命令规则可配置 | Commands / Rules 文档介绍审批策略与命令 allow/block 规则 | https://developers.openai.com/codex/commands/ ; https://developers.openai.com/codex/rules |
| AGENTS.md 用于项目级行为约束 | AGENTS.md 文档说明就近生效、可定义构建/测试/代码规范/PR 要求 | https://developers.openai.com/codex/agents-md |
| Internet Access 可按 off/allowlist/on 管理 | Internet Access 文档给出 `off` / `restricted` / `full` 模式 | https://developers.openai.com/codex/cloud/environments/internet-access |
| 安全边界默认“受限 + 可审计” | Security 文档说明云端默认无网络、需授权升级；任务受策略控制 | https://developers.openai.com/codex/security |
| Automations 支持定时触发 + 审批控制 | Automations 文档提供 schedule、approval mode、notifications | https://developers.openai.com/codex/automations |
| Prompting 推荐把任务拆成结构化目标与步骤 | Prompting 文档强调清晰任务定义、约束、分阶段指令 | https://developers.openai.com/codex/prompting |

## 单模型能力 vs 多 Agent 编排

### 单模型能力（Model Capability）

- 一次会话内完成推理、写作、代码、总结。
- 适合低耦合、短链路任务（如单篇文档初稿、一次 SQL 分析）。
- PM 价值：启动快，沟通成本低。

### 多 Agent 编排（Orchestration Capability）

- 将任务拆成多个可并行或串行的子任务，并分配不同角色（研究/生成/审核/发布）。
- 通过 worktree 隔离、审批策略、规则、回放记录提升稳定性。
- PM 价值：可复用、可治理、可规模化。

### 推荐默认：文档/Blog 任务也走“轻量多 Agent”

- 即使不是编码任务，也建议至少采用“写作 Agent + 守门员 Agent（事实核查/合规）”双 Agent。
- 原因：文档任务最容易在事实准确性、口径一致性、品牌语气上出错，多一道 gate 的 ROI 很高。

## 内容产品接口（TaskCard / RunPolicy）

```yaml
TaskCard:
  id: string
  objective: string
  inputs: string[]
  constraints: string[]
  tools_allowed: string[]
  approval_policy: string
  done_definition: string[]
  output_format: string
  reviewer: string
```

```yaml
RunPolicy:
  execution_mode: one_shot | staged | multi_agent
  sandbox_level: strict | balanced | permissive
  internet_access: off | allowlist | on
  interruption_points: string[]
  escalation_rules: string[]
```

## 6 大任务模式（含 blog/文档制作）

### 模式 A：并行探索 + 汇总（Parallel Discover + Synthesize）

- 适用：竞品调研、市场扫描、用户声音归纳。
- 结构：3-5 个研究 Agent 并行抓取 -> 1 个汇总 Agent 归并结论。
- 输出：证据矩阵、冲突观点列表、优先级建议。

### 模式 B：串行内容流水线（Research -> Outline -> Draft -> Fact-check -> Edit）

- 适用：Blog、白皮书、FAQ、产品文档。
- 结构：研究 Agent -> 大纲 Agent -> 写作 Agent -> 事实核查 Agent -> 编辑 Agent。
- 输出：可发布稿 + 引用清单 + 风险注记。

### 模式 C：主 Agent + 专家 Agent（Lead + Specialists）

- 适用：复杂 PRD、跨技术方案、系统设计文档。
- 结构：主 Agent 持有目标与节奏，专家 Agent 分别负责技术、合规、商业。
- 输出：统一方案稿 + 争议点处理记录。

### 模式 D：守门员 Agent（Gatekeeper）

- 适用：高风险内容（法律、金融、医疗、政策）或对外发布材料。
- 结构：生成流程后置 gate，未通过则退回修改。
- 输出：通过/驳回结论、问题清单、修订建议。

### 模式 E：双轨执行（执行轨 + 评审轨）

- 适用：代码+文档混合任务（发布说明、变更公告、SDK 文档）。
- 结构：执行轨产出结果，评审轨独立 review（不共享同一上下文偏见）。
- 输出：主产物 + review 结论 + 风险等级。

### 模式 F：持续运营（Automation Loop）

- 适用：周报、缺陷 triage、舆情追踪、内容复盘。
- 结构：定时触发 -> 自动收集 -> 人工审批 -> 发布归档。
- 输出：固定格式报告，保留周期趋势数据。

## 12 条 Best Practices（动作化检查项）

> 固定格式：触发条件 -> 执行动作 -> 反模式 -> 验收标准

1. **任务超过 30 分钟或跨 2 个以上子目标**  
触发：需求复杂或会中途变更。  
执行：强制拆分 TaskCard（每卡一个可验证结果）。  
反模式：一个超长 prompt 试图“一次做完”。  
验收：每个 TaskCard 都有 `done_definition`。

2. **涉及外部资料检索**  
触发：需要“最新”信息或官方引用。  
执行：设置 `internet_access=allowlist`，优先官方域名。  
反模式：默认 full internet，来源不可追溯。  
验收：输出中每个关键结论至少 1 个可访问链接。

3. **并行多任务**  
触发：两条以上任务可独立执行。  
执行：每条任务使用独立 worktree。  
反模式：多个 Agent 共用同一工作目录互相污染。  
验收：任务执行日志中可区分独立上下文和变更。

4. **需要执行命令**  
触发：任务包含脚本/CLI/构建步骤。  
执行：先设 Rules（allowlist/blocklist）再执行。  
反模式：先跑命令后补治理。  
验收：敏感命令需要审批，规则可复用。

5. **团队协作频繁复用同类流程**  
触发：同任务每周重复 >=2 次。  
执行：写 AGENTS.md 明确约束（测试、风格、输出结构、禁用动作）。  
反模式：靠口头约定或聊天记忆。  
验收：新成员可仅凭 AGENTS.md 跑通任务。

6. **任务需要稳定语气和结构**  
触发：面向客户/公开发布。  
执行：建立“分层提示词”：目标层、约束层、格式层、质检层。  
反模式：仅写主题，不写格式和质检要求。  
验收：首稿结构达标率 >=80%。

7. **内容存在事实风险**  
触发：统计、政策、版本号、日期。  
执行：增加守门员 Agent 做“日期+来源”核验。  
反模式：让同一 Agent 自审。  
验收：所有数字/日期可回链。

8. **任务中途需求变化**  
触发：新增方向或优先级调整。  
执行：利用中途消息机制改向，保留原任务分支记录。  
反模式：直接覆盖原始目标导致追溯困难。  
验收：变更原因、时间点、影响范围可审计。

9. **需要跨设备/跨人交接**  
触发：任务被转交或异步协作。  
执行：使用 cloud tasks 链接 + 标准输出模板。  
反模式：仅口头同步。  
验收：接手者 10 分钟内可继续执行。

10. **定期重复任务**  
触发：日报/周报/巡检。  
执行：配置 Automations（schedule + approval + notifications）。  
反模式：手工重复触发，格式漂移。  
验收：连续 4 周格式一致，人工仅做审批。

11. **高风险权限申请**  
触发：需要扩展网络、文件写入范围、执行高危命令。  
执行：先声明目的与最小权限，再审批。  
反模式：一开始给最大权限。  
验收：权限申请记录可解释且可回收。

12. **上线前最终检查**  
触发：内容/功能即将发布。  
执行：双清单 gate（事实完整性 + 品牌一致性）。  
反模式：只看“写得像不像”。  
验收：通过 gate 才能发布，失败有回退动作。

## 风险与治理（审批、沙箱、访问范围、合规）

### 1) 审批策略

- 低风险任务：`on-request`，保效率。
- 高风险任务：`on-failure` 或更严格策略，先阻断再申请。
- 原则：默认最小权限，按任务升级。

### 2) 沙箱与访问范围

- 沙箱建议三档：
  - `strict`：默认档，适合文档和分析。
  - `balanced`：需要受控联网/命令执行。
  - `permissive`：仅用于受信任环境与明确审计。
- 网络建议优先 allowlist 域名，避免全网抓取带来版权与准确性风险。

### 3) 合规边界

- 不抓取 paywalled / 登录后专有内容。
- 不绕过访问控制或平台限制。
- 对敏感话题（政策、医疗、金融）强制“来源 + 日期 + 守门员复核”。

### 4) 质量治理指标（推荐最小集）

- 准确性：关键结论可回链率（目标 >=95%）
- 返工率：一次通过率（目标 >=70%）
- 周期：从需求到可发布的中位耗时
- 稳定性：模板遵循率（目标 >=90%）
- 风险：审批拦截率与误拦截率

## 30 天 Adoption 计划（从 0 到 1）

### Week 1：单 Agent 标准化

- 建立 TaskCard / RunPolicy 模板。
- 选 2 个低风险任务试点（如周报、FAQ）。
- 输出：首版 AGENTS.md 约束清单。
- 验收：两类任务都能稳定复现。

### Week 2：双 Agent 分工

- 引入守门员 Agent（事实核查或合规）。
- 将 blog/文档流程升级为 5 步流水线。
- 输出：可发布内容模板 + 引用规范。
- 验收：关键事实可追溯率 >=90%。

### Week 3：多 Agent 流水线 + 审批策略

- 并行研究 + 串行写作组合。
- 上线 rules 和 approval 分层策略。
- 输出：任务模式库（A-F）在团队内试运行。
- 验收：平均交付周期较 Week 1 缩短 20%。

### Week 4：指标化运营与复盘

- 配置 Automations 跑固定任务（周报、triage）。
- 做一次端到端复盘：效率、质量、风险。
- 输出：团队版 playbook v1.0。
- 验收：形成可持续迭代的 KPI 仪表盘。

## Test Cases / Scenarios（验收测试）

1. **事实可追溯测试**：随机抽 10 条结论，检查是否有官方链接。  
2. **可执行性测试**：按 Blog 模板跑完整流程，验证输入输出闭环。  
3. **稳定性测试**：中途改需求，验证可中断、可续跑、可回退。  
4. **治理测试**：模拟“需联网抓资料”，验证审批与 allowlist 生效。  
5. **PM 可读性测试**：非工程 PM 10 分钟内能复述 3 种模式与选型标准。

## 官方来源清单

- https://openai.com/index/introducing-gpt-5-3-codex/
- https://openai.com/index/introducing-the-codex-app/
- https://developers.openai.com/codex/
- https://developers.openai.com/codex/ide
- https://developers.openai.com/codex/cloud
- https://developers.openai.com/codex/worktrees
- https://developers.openai.com/codex/commands/
- https://developers.openai.com/codex/prompting
- https://developers.openai.com/codex/agents-md
- https://developers.openai.com/codex/automations
- https://developers.openai.com/codex/rules
- https://developers.openai.com/codex/security
- https://developers.openai.com/codex/cloud/environments/internet-access
