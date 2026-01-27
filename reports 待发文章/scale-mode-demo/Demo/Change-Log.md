# Change Log - Scale Mode Demo

> 启用日期: 2026-01-24

- [Status] 接收初始研究背景与策略思路。
- [Action] 解析了基于 invideo-blog 的批量重构逻辑，包括候选池建立、结构复用及优先级评估初步设想。
- [Config] 激活日志记录模式，后续所有指令执行与系统状态变更将同步更新至 Change Log。
- [Action] 新建 Demo 目录并迁移临时 Skill/Plan 文件至 `Scale Mode/Demo/`。
- [Action] 新建方法论整理文档 `Methodology-Notes.md`。
- [Action] 新增 InVideo Blog 批量抓取方案与数据结构：`Harvest-Plan.md` + `Schema-Invideo-Harvest.json`。
- [Action] 新增抓取脚本 `harvest_invideo_blog.py`（支持小规模与扩展抓取）。
- [Action] 完成小规模试跑（10 篇）并扩展到 60 篇，输出 JSONL/CSV/LOG。
- [Artifact] `invideo-blog-harvest.jsonl`, `invideo-blog-harvest.csv`, `invideo-blog-harvest.log`。
- [Action] 尝试运行 DataForSEO 验证脚本 `validate_growth_topics.py`，接口返回 HTTP 402（Payment Required），未能获取关键词数据。
- [Artifact] `invideo-blog-validation-summary.md`, `invideo-blog-validation.log`。
- [Action] DataForSEO 验证已成功执行（50 关键词 + 10 SERP）。
- [Artifact] `invideo-blog-validated.jsonl`, `invideo-blog-validation-summary.md`, `invideo-blog-validation.log`.
- [Action] 生成合并报告与评分表：`Demo-Validation-and-Candidates.md` + `Demo-Scorecard.csv`。
- [Action] 生成 Top10 逐条重构挑战与策略文档：`Demo-Top10-Refactor-Plan.md`。
