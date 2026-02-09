# Seed Mode D2（Diversity Engine）三用例对比验证报告
**Date**: 2026-02-03  
**Scope**: 3 use cases × (D1 baseline vs D2 diversity selection)  
**Data constraint**: 本环境网络受限，本报告使用仓库内已落盘的验证产物，离线重构 D2 的“聚类/去重/门禁/选 3”流程。

---

## 方法说明（重要）

- **D1 baseline**：优先使用已存在的 Seed D1 `final_directions`；若缺失，则用候选池按 (SEO+AEO)/2 取 Top2 作为“D1 proxy”。
- **D2 reconstruction**：对同一候选池应用 **TF-IDF 余弦相似度（词面 proxy）** 做 greedy clustering + diversity gate + 最终 3 方向组合约束。
- **相似度口径**：D1 的 `d1_final_sim` 是最终 2 个标题的 TF-IDF cosine；D2 的 `avg_pairwise_similarity` 来自 final 3 的平均两两相似度。
- **注意**：这不是“真正线上 D2 执行”（LLM 语义 embedding / WebSearch）；因此结果用于评估 *机制可行性* 与 *门禁可操作性*，不等同于最终线上效果。

---

## 结果总览（PASS/FAIL）

| Use Case | D1 平均分 | D2 平均分 | D1 相似度 | D2 平均相似度 | D2 Clusters | D2 Intents | 多样性门禁 | 价值门禁 |
|---|---:|---:|---:|---:|---:|---:|---|---|
| UC1 | 55.50 | 59.33 | 0.1868 | 0.0441 | 3 | 2 | PASS | PASS |
| UC2 | 89.75 | 88.67 | 0.4111 | 0.2818 | 3 | 2 | PASS | PASS |
| UC3 | 35.00 | 32.50 | 0.2061 | 0.2187 | 3 | 2 | PASS | PASS |

---

## UC1: UGC 广告，用 AI 怎么做？

- Seed（用于候选池）: `ugc creator (proxy for ai ugc ads)`  
- 数据来源目录: `/Users/H/Documents/AliciBlog/reports 待发文章/2026-02-03-ugc-creator-guide-2026`

### D1 Baseline（2 个方向）

1. **How to Become a UGC Creator in 2026: A Beginner Video Workflow (Step-by-Step)**  
   - keyword: `what is a ugc creator`  
   - intent: `how-to`  
   - SEO/AEO: 67 / 75  
   - volume: 3720
2. **UGC Creator Portfolio in 2026: Templates, Examples, and What Brands Want**  
   - keyword: `ugc portfolio examples`  
   - intent: `workflow`  
   - SEO/AEO: 25 / 55  
   - volume: 1140

### D2 Reconstructed（3 个方向 + 多样性门禁）

- Diversity metrics: avg_sim=0.0441, max_sim=0.0804, clusters=3, intents=2  
- Gate: **PASS**

1. **Become a UGC creator (beginner path)**  
   - keyword: `what is a ugc creator`  
   - intent: `use-case`  
   - strategy: `seed_xpollination`  
   - cluster: `C01`  
   - SEO/AEO: 67 / 75  
   - volume: 3720
2. **Rates / pricing / usage rights**  
   - keyword: `ugc usage rights`  
   - intent: `use-case`  
   - strategy: `seed_xpollination`  
   - cluster: `C02`  
   - SEO/AEO: 20 / 95  
   - volume: 80
3. **Editing workflow (short-form)**  
   - keyword: `how to edit ugc videos`  
   - intent: `how-to`  
   - strategy: `seed_xpollination`  
   - cluster: `C04`  
   - SEO/AEO: 4 / 95  
   - volume: 20

### 备注 / 风险

- UC1 uses an existing Seed D1 run ('ugc creator') as a proxy for the UGC ads use case.

---

## UC2: 10个最佳 AI Video Generator 是什么？

- Seed（用于候选池）: `best ai video generator (proxy via ai video tools 2026 dataset)`  
- 数据来源目录: `/Users/H/Documents/AliciBlog/reports 待发文章/2026-01-24-ai-video-tools-2026`

### D1 Baseline（2 个方向）

> 注：D1 baseline is reconstructed as top-2 by (SEO+AEO)/2 from existing validated keyword matrix outputs.

1. **sora 2 vs runway gen-4**  
   - keyword: `sora 2 vs runway gen-4`  
   - intent: `comparison`  
   - SEO/AEO: 92 / 88  
   - volume: 12200
2. **sora 2 vs kling 2.6 vs veo 3**  
   - keyword: `sora 2 vs kling 2.6 vs veo 3`  
   - intent: `comparison`  
   - SEO/AEO: 89 / 90  
   - volume: 7500

### D2 Reconstructed（3 个方向 + 多样性门禁）

- Diversity metrics: avg_sim=0.2818, max_sim=0.4929, clusters=3, intents=2  
- Gate: **PASS**

1. **sora 2 vs runway gen-4**  
   - keyword: `sora 2 vs runway gen-4`  
   - intent: `comparison`  
   - strategy: `serp_gap`  
   - cluster: `C01`  
   - SEO/AEO: 92 / 88  
   - volume: 12200
2. **sora 2 vs kling 2.6 vs veo 3**  
   - keyword: `sora 2 vs kling 2.6 vs veo 3`  
   - intent: `comparison`  
   - strategy: `serp_gap`  
   - cluster: `C02`  
   - SEO/AEO: 89 / 90  
   - volume: 7500
3. **best ai video tools 2026**  
   - keyword: `best ai video tools 2026`  
   - intent: `list`  
   - strategy: `seed_xpollination`  
   - cluster: `C03`  
   - SEO/AEO: 88 / 85  
   - volume: 14500

### 备注 / 风险

- UC2 uses the existing ai-video-tools-2026 keyword matrix (validated) as the candidate pool.

---

## UC3: 我想做一个 AI Influencer 的账号，我该怎么准备？用什么工具起步？有没有什么教程能让我快速赚到钱？

- Seed（用于候选池）: `ai influencer tools (proxy via batch-ai-influencer dataset)`  
- 数据来源目录: `/Users/H/Documents/AliciBlog/reports/2026-01-27-batch-ai-influencer`

### D1 Baseline（2 个方向）

> 注：D1 baseline is reconstructed from a small validated keyword set (4 keywords).

1. **how to create AI influencer at scale**  
   - keyword: `how to create AI influencer at scale`  
   - intent: `how-to`  
   - SEO/AEO: 45 / 30  
   - volume: 0
2. **batch AI influencer tutorial 2026**  
   - keyword: `batch AI influencer tutorial 2026`  
   - intent: `use-case`  
   - SEO/AEO: 45 / 20  
   - volume: 0

### D2 Reconstructed（3 个方向 + 多样性门禁）

- Diversity metrics: avg_sim=0.2187, max_sim=0.2667, clusters=3, intents=2  
- Gate: **PASS**

1. **how to create AI influencer at scale**  
   - keyword: `how to create AI influencer at scale`  
   - intent: `how-to`  
   - strategy: `seed_xpollination`  
   - cluster: `C01`  
   - SEO/AEO: 45 / 30  
   - volume: 0
2. **batch AI influencer tutorial 2026**  
   - keyword: `batch AI influencer tutorial 2026`  
   - intent: `use-case`  
   - strategy: `seed_xpollination`  
   - cluster: `C02`  
   - SEO/AEO: 45 / 20  
   - volume: 0
3. **AI digital human content creation**  
   - keyword: `AI digital human content creation`  
   - intent: `use-case`  
   - strategy: `seed_xpollination`  
   - cluster: `C03`  
   - SEO/AEO: 45 / 10  
   - volume: 0

### 备注 / 风险

- UC3 dataset is niche/emerging (monthly_search_volume=0 for all validated keywords in saved artifacts).
- Treat value comparisons as direction-quality proxy (SERP features) rather than demand validation.

---

## 总结结论（当前数据条件下）

- 这份报告验证了：在**无需新增外部依赖**的情况下，D2 的“聚类去重 + 多样性门禁 + 组合约束”可以被工程化执行，并能输出可审计的指标。
- 但由于本次相似度使用的是 **TF-IDF 词面 cosine**（不是 embedding 语义 cosine），以及部分用例候选池/需求数据不足（例如 UC3 volume=0），结论更适合作为“机制可行性”验证。
- 下一步建议：在可联网环境中用真实的 Seed D1/D2 执行产物（含 `03-diversity-report.json` 与 DataForSEO）重跑同样的三用例，替换本报告中的 offline proxy。
