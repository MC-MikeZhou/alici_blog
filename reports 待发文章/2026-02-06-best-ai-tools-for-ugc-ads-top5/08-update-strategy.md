# 双周更新迭代策略（基于站外 SERP 证据包）

> 适用文章：`/Users/H/Documents/AliciBlog/reports 待发文章/2026-02-06-best-ai-tools-for-ugc-ads-top5/01-article.md`  
> 生成日期：2026-02-07  
> 注意：本文件是“旁路策略文件”，不写入文章正文，避免触发 `listicle_validator` 的 `ARTICLE_EXTRA_H2`。

## 1) 证据来源（站外竞品 + SERP 特征）

本轮证据包输出目录（US + EN）：
- `/Users/H/Documents/AliciBlog/reports/2026-02-07-ugc-ai-tools-serp-harvest/`

关键文件：
- `/Users/H/Documents/AliciBlog/reports/2026-02-07-ugc-ai-tools-serp-harvest/01-query-universe.json`：每个 query 的 search volume / CPC / competition（DataForSEO）。
- `/Users/H/Documents/AliciBlog/reports/2026-02-07-ugc-ai-tools-serp-harvest/02-serp-snapshots.jsonl`：SERP features（AIO/PAA/视频/论坛等）+ top organic（含 rank）。
- `/Users/H/Documents/AliciBlog/reports/2026-02-07-ugc-ai-tools-serp-harvest/03-candidate-urls.jsonl`：去重后的站外候选 URL（每条可追溯到 source_query + rank）。
- `/Users/H/Documents/AliciBlog/reports/2026-02-07-ugc-ai-tools-serp-harvest/04-competitor-url-pack.md`：给编辑直接可用的“站外链接包”（按 query、按 domain 分组）。
- `/Users/H/Documents/AliciBlog/reports/2026-02-07-ugc-ai-tools-serp-harvest/05-update-strategy.md`：证据驱动的通用更新策略（L1/L2/L3 分级）。

## 2) 双周例行流程（固定动作清单）

每两周做一次（建议固定在周二或周三）：
1. 复跑站外 harvest（同一份 mission config）：
   - 命令：`python3 /Users/H/Documents/AliciBlog/scripts/ugc_ai_tools_serp_harvest.py --out-dir /Users/H/Documents/AliciBlog/reports/2026-02-07-ugc-ai-tools-serp-harvest`
2. 对比上次与本次输出，记录 delta：
   - Query metrics：volume/CPC/competition 是否出现明显变化。
   - SERP features：AIO/PAA 是否出现/消失，视频模块是否更强。
   - Top20（强对标）新增/流失的竞品 URL。
3. 按 L1/L2/L3 分级选择本篇文章的更新力度（见第 4 节）。

## 3) 触发式规则（什么情况下必须升级更新力度）

- 主词衰减（连续两轮双周）：若文章主词或核心次词的 `search_volume` 下降 >= 30%，进入“重选主词/改标题公式”评审。
- Intent 漂移：如果 SERP Top10 从“榜单/对比”漂移到“定义/How-to”为主，下一版应从 listicle 结构切换到 guide 结构（可能需要新稿或改为 mega profile）。
- AIO/PAA 集中：若 AIO 出现，并且 PAA 问题聚焦到某一个子意图（例如“UGC video ads 的合规/成本/真实感”），优先：
  - 在本篇 FAQ 用 PAA 问法替换问题（不新增 H2），或
  - 拆分一篇新文章承接该子意图。

## 4) 更新分级（避免每次都大改）

- L1 轻改（30 分钟）
  - 更新工具 pricing/官方链接，修正过期描述。
  - 更新 freshness 声明（Verified as of 日期）。
  - 更新对比表中最易过时列（价格、输出限制、语言、模板等）。

- L2 结构增强（2–3 小时）
  - 重写首屏 Quick Answer（更短、更强、更可被抽取）。
  - 用本轮 SERP 的 PAA 问法替换 FAQ（不新增 H2）。
  - 强化 quick comparison 表格：列名更一致，可直接被 AIO 摘取。

- L3 重构（1 天）
  - 更换 primary keyword / 重写标题与 meta。
  - 调整工具池（新增/移除/重新排序），必要时扩到 Top7/Top10（这一步会影响 validator 与篇幅，需要重新门禁）。
  - 完整复跑：listicle validator + AEO 评分（并留档）。

## 5) 门禁与兼容性（必须遵守）

- 不在文章正文新增额外 H2（避免 `listicle_validator` 失败）。
- 本篇更新完成后，至少复查：
  - `/Users/H/Documents/AliciBlog/reports 待发文章/2026-02-06-best-ai-tools-for-ugc-ads-top5/04-listicle-validator-report.json`
  - `/Users/H/Documents/AliciBlog/reports 待发文章/2026-02-06-best-ai-tools-for-ugc-ads-top5/03-aeo-score.md`

