# InVideo Blog 批量抓取方案 (Demo 起点)

> 版本: v0.1
> 日期: 2026-01-24
> 目的: 为后续 Growth Topic 评选提供可直接使用的候选数据集

## 1. 输出目标

- 主输出: JSONL（每行一篇，适合批量处理与增量更新）
- 附输出: CSV（便于人工快速筛选）

## 2. 字段设计（面向 Growth Topic 评选）

必备字段：
- source: 固定 `invideo_blog`
- url
- title
- publish_date
- toc: 目录数组（若无目录，用 H2 替代）
- intro: 前 600 字（可调）
- content_type_guess: listicle / how_to / comparison / statistics / guide / trends / alternatives / other
- intent_guess: awareness / interest / consideration / decision
- keyword_seed: 5-10 个关键词候选（来自 title/toc/intro）
- needs_refresh: 是否需要更新年份/版本（true/false）
- notes: 抓取异常或结构说明

## 3. 抓取范围与策略

- 范围: `invideo.io/blog` 下文章页
- 过滤: 排除纯视频页/无正文页/重复 URL
- 目录: 优先提取 TOC；无 TOC 则提取 H2 作为目录
- 前文: 截取正文前 600 字
- 类型识别: 用标题公式 + 目录结构作初判

## 4. 为什么这样设计

- Growth Topic 评选需要关键词候选 + 语境 + 类型/意图
- JSONL 便于后续追加 DataForSEO 验证字段
- CSV 便于人工快速删选

## 5. 后续验证衔接

- DataForSEO: search volume / CPC / competition
- 竞品强度: SERP 前 10 结构与类型
- 优先级评分: intent + volume + fit + freshness
