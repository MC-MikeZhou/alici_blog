# 方法论与判断 - 批量重构选题→验证

> 日期: 2026-01-24
> 来源: 用户输入整理（基于 invideo-blog 研究）

## 核心原则

- 不从零写、不过度依赖模板
- 先做“高质量对标 + 意图匹配 + 数据验证”

## 1. 建立候选池

- 直接从 `invideo-article-samples.json` 拉出高价值类型：
  - listicle / comparison / showdown / how_to / statistics / guide / trends / alternatives / vertical_industry
- 优先挑“结构成熟且有明确意图”的类型：
  - Listicle、Comparison、How-to、Statistics
- 将文章按漏斗阶段映射（认知/兴趣/考虑/决策）形成矩阵，确保覆盖

## 2. 选题不是复制标题，而是复制结构 + 替换需求

- 使用 invideo 标题公式，但替换为 Alici 的产品场景与用户痛点
- 优先选择更“新”+更“具体”的角度：
  - 2026 年、平台变化、工具版本变化、行业变化

## 3. 做“选题优先级评分”

- 以可重复筛选系统为目标
- 先验证再改写，避免盲目规模化
