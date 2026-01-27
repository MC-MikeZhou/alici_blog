# Plan - Scale Demo (10 篇批量重构实验)

> 版本: v0.1
> 日期: 2026-01-24

## 目标

找出 10 篇可直接批量重构的高价值内容，并完成评分与挑战评估。

---

## Step 1. 搜索与整理 (Search & Map)

### 1.1 候选池来源
- 使用 `competitive-research/invideo-blog/data/invideo-article-samples.json`
- 优先类型：Listicle / Comparison / Showdown / How-to / Statistics / Guide / Trends / Alternatives

### 1.2 快速筛选规则
- 结构清晰（有固定模板）
- 可映射到现有 Alici Writer 类型（tutorial / list / showdown / roundup）
- 非高度依赖可视化图表的文章优先

### 1.3 Skill 映射（临时）
为每篇候选指定“服务线 Demo”Skill 名称，用于区分旧体系：
- demo-listicle
- demo-comparison
- demo-showdown
- demo-howto
- demo-statistics

---

## Step 2. 评分与决策 (Score & Decide)

### 2.1 评分维度
- 意图强度 (1-5)
- 转化价值 (1-5)
- 结构可复制性 (1-5)
- 数据依赖复杂度 (1-5，反向)
- 资产复杂度 (1-5，反向)

### 2.2 决策规则
- 总分 ≥ 12 → 进入批量重构候选
- 8-11 → 备用候选
- < 8 → 淘汰

---

## Step 3. 提交报告 (Report)

报告包含：
- Top 10 候选列表 + Skill 映射
- 评分表
- 主要挑战
  - 是否强依赖图表/视频
  - 是否高度依赖最新数据
  - 是否需要深度案例或特殊素材

---

## 最终交付物

- `Scale Mode/Demo-Candidates.md`
- `Scale Mode/Demo-Scorecard.md`
- `Scale Mode/Demo-Report.md`
