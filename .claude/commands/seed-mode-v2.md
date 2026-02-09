# /seed-mode-v2 - Seed Mode D2（多样性发散选题）

使用 growth-topic-scout v2.3 的 **Mode D2（Diversity Engine）**：多策略发散 → 语义聚类去重 → 多样性门禁 → DataForSEO 验证 → 输出 **3 个**可直接开写方向。

## 触发方式

- 直接输入：`seed mode v2 [你的种子词]`
- 或在 Mission Config 中设置：`diversity.enabled=true`

## 输出位置

`/reports/YYYY-MM-DD-{seed-slug}/`（关注：`03-diversity-report.json` 与 `00-topic-brief.json`）

## 快速验收（看 3 个指标）

- `avg_pairwise_similarity < 0.50`（越低越发散）
- `cluster_count >= 3` 且 `intent_type_count >= 2`
- `final_directions` 为 3 个，且两两相似度 < 0.60

