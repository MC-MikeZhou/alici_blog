# Growth Topic Scout v2.3 Benchmark Protocol (D1 vs D2)

目的：用一组固定种子词，对比 Seed D1（竞品锚定）与 Seed D2（多样性引擎）在 **多样性** 与 **价值** 上的变化，决定是否扩大 D2 的默认使用范围。

## 输入

- Seeds: `BENCHMARK_SEEDS_v2.3.json`
- 固定配置（建议）：
  - `scope.geo=US`, `scope.language=en`, `scope.validation_depth=standard`
  - D2 默认阈值：`cluster_threshold=0.60`, `target_avg_similarity=0.50`, `final_pairwise_max=0.60`

## 运行方式（每个 seed 跑 2 次）

1. **D1 基线**
   - 输入：`seed mode {seed}`
   - 期望输出：`final_directions` 长度=2
2. **D2 实验**
   - 输入：`seed mode v2 {seed}`（或 mission_config: `diversity.enabled=true`）
   - 期望输出：`final_directions` 长度=3，且有 `diversity_report`

## 采集指标（每次运行必须记录）

从 `00-topic-brief.json` / `03-diversity-report.json` 提取：

### Diversity
- `avg_pairwise_similarity`（D2 必填；D1 可人工估计或留空）
- `cluster_count`（D2 必填）
- `intent_type_count`（D2 必填）
- `final_pairwise_max`（最终 2/3 个方向两两最大相似度）
- `strategy_mix`（D2 必填：persona/serp_gap 至少要有 1 个方向贡献）

### Value (Top 2/3)
- `seo_score` 均值
- `aeo_score` 均值
- `combined_priority` 分布（excellent/high/good/low）
- `evidence_chain.volume`（Top1 与均值）
- `api_usage.estimated_cost`（可选）

## 成功判定（平衡型）

- D2 相对 D1：`avg_pairwise_similarity` 下降 ≥ 20%
- 且 D2 Top3 的（SEO+AEO）均分不低于 D1 Top2 均分 - 5 分

## 结果汇总模板（建议）

在 `reports/YYYY-MM-DD-growth-topic-scout-v2.3-benchmark/` 下生成：
- `00-summary.md`（整体结论 + Top seeds）
- `01-results.csv`（每行一个 seed：D1 vs D2 指标对比）

