# Scale Mode Demo 项目说明文档

> 版本: v1.0
> 日期: 2026-01-24
> 面向对象: AliciBlog 内部团队（含未参与前期讨论的成员）

## 1. 项目全貌（背景 / 目的 / 思路）

### 背景
AliciBlog 已形成稳定的内容生产链路（smart‑launcher → Writer → Editor → AEO → 竞品验证 → Framer），但随着功能迭代，存在规则分散、版本不一致、批量执行难追踪等问题。同时，InVideo 已沉淀 300‑500 篇高质量内容，具备可系统借鉴的结构与策略。

### 目的
启动一个小规模 Demo，验证“批量重构”是否可行，特别是验证以下能力：
- 能否从竞品内容中快速建立候选池
- 能否用 DataForSEO 做硬验证，筛掉无价值选题
- 能否形成可重复的评分与筛选流程，产出 Top 候选清单

### 大致思路
不从零写、不依赖单一模板，而是先做“高质量对标 + 意图匹配 + 数据验证”，再进入规模化改写：
1) 从 InVideo 内容样本中抽取高价值类型
2) 用结构化字段建立候选池（标题/目录/前文/关键词）
3) 用 DataForSEO 验证需求与 SERP 机会
4) 评分排序 → 输出 Top 候选 + 重构挑战

---

## 2. 受众定位（内部团队）

这份文档面向 AliciBlog 内部团队，包含对项目全流程的简要解释，适合：
- 未参与前期讨论的同事快速了解背景与进展
- 需要复用流程的执行同事
- 需要评估“是否进入下一阶段”的决策同事

文档默认不要求具备全部上下文，关键概念均做了明确说明。

---

## 3. 执行过程（阶段与完成动作）

### 阶段 1：方法论与计划建立
- 明确批量重构的核心原则与筛选流程
- 输出 Demo 级临时 Skill 与计划文档
- 文件：
  - `Methodology-Notes.md`
  - `Plan-Scale-Demo.md`
  - `Skill-Scale-Demo.md`

### 阶段 2：InVideo Blog 批量抓取
- 抓取 ≥50 篇 InVideo Blog 内容
- 结构化字段：标题、前 600 字、目录、内容类型、意图、关键词种子
- 输出：
  - `invideo-blog-harvest.jsonl`
  - `invideo-blog-harvest.csv`

### 阶段 3：DataForSEO 验证
- 对 50 个关键词做 Search Volume / CPC / Competition 验证
- 对 Top 10 关键词做 SERP 特征检测
- 输出：
  - `invideo-blog-validated.jsonl`
  - `invideo-blog-validation-summary.md`

### 阶段 4：评分与候选筛选
- 评分模型：SV + CPC + SERP 特征 + 结构可复制性 + 刷新机会 − 竞争惩罚
- 输出 Top10 候选
- 输出：
  - `Demo-Validation-and-Candidates.md`
  - `Demo-Scorecard.csv`

### 阶段 5：逐条重构挑战与策略
- 为 Top10 候选逐条评估重构挑战
- 给出具体结构化重构策略建议
- 输出：
  - `Demo-Top10-Refactor-Plan.md`

---

## 4. 现状与结论（报告内容与结论）

### 现状
当前 Demo 已完成“候选池建立 → 数据验证 → 评分筛选 → Top10 重构建议”的闭环，尚未进入实际批量重构执行阶段。

### 主要产物
- 抓取数据集：`invideo-blog-harvest.jsonl` / `invideo-blog-harvest.csv`
- 验证数据集：`invideo-blog-validated.jsonl`
- 候选筛选与评分：`Demo-Validation-and-Candidates.md`, `Demo-Scorecard.csv`
- Top10 重构策略：`Demo-Top10-Refactor-Plan.md`

### 结论
- “批量重构”流程可行：从竞品 → 候选池 → DataForSEO 验证 → Top 候选筛选已经跑通。
- DataForSEO 是有效硬门槛：能过滤无需求/低机会选题。
- Top10 已具备进入下一阶段（实际重构执行）的条件。

---

## 下一步建议（可选）

1) 选定 5‑7 篇 Top10 作为试点执行
2) 走完整 Writer → Editor → AEO → 竞品验证
3) 输出成本与质量对比（AEO 分数、修复成本）

