# DataForSEO AEO/LLM 维度测试报告

> **测试日期**: 2026-01-26
> **测试种子词**: "ai video tools"
> **API 账户**: hans.h@hey.com

---

## 测试结果摘要

| API 维度 | 端点 | 状态 | 成本 |
|---------|------|------|------|
| Keywords Data | `/v3/keywords_data/google_ads/search_volume/live` | **PASS** | $0.075 |
| Google Trends | `/v3/keywords_data/google_trends/explore/live` | **PASS** | $0.009 |
| LLM Responses (ChatGPT) | `/v3/ai_optimization/chat_gpt/llm_responses/live` | **PASS** | $0.072 |
| LLM Mentions | `/v3/ai_optimization/llm_mentions/*/live` | **BLOCKED** | 需要订阅 |

---

## 维度 1: Keywords Data (传统 SEO)

### 测试结果

```json
{
  "keyword": "ai video tools",
  "search_volume": 1600,
  "cpc": 6.38,
  "competition": "LOW",
  "competition_index": 27,
  "trend": "rising (Dec 2025: 2400)"
}
```

### 月度趋势

| 月份 | 搜索量 |
|------|--------|
| Dec 2025 | 2,400 |
| Nov 2025 | 1,600 |
| Oct 2025 | 1,300 |
| Jul 2025 | 5,400 (峰值) |

**结论**: API 正常工作，返回完整的搜索量、CPC 和月度趋势数据。

---

## 维度 2: Google Trends (搜索趋势对比)

### 测试关键词

- ai video generator
- sora ai
- runway ml
- kling ai

### 趋势数据 (过去 12 个月)

| 周期 | ai video generator | sora ai | runway ml | kling ai |
|------|-------------------|---------|-----------|----------|
| Jan 2025 | 9 | 2 | 1 | 4 |
| Feb 2025 | 10 | 2 | 1 | 3 |
| Recent | Rising | Stable | Declining | Rising |

**结论**: API 正常工作，返回多关键词趋势对比数据。

---

## 维度 3: LLM Responses (AI 回答内容)

### 测试提示词

```
What are the best AI video generators in 2026?
```

### API 响应

**状态**: SUCCESS
**模型**: gpt-4o-2024-08-06
**Token 使用**: Input 16,850 / Output 469
**成本**: $0.072

### LLM 提及的工具

| 排名 | 工具 | 评价 |
|------|------|------|
| 1 | DeeVid AI | Best All-in-One Workflow |
| 2 | Google Veo 3.1 | Best for Cinematic Quality |
| 3 | OpenAI Sora 2 | Best for Story-Driven Realism |
| 4 | Kling AI 2.0 | Best for Realism & Character Consistency |

### 引用来源

- indiehackers.com - "5 Best AI Video Generators for 2026"
- aifuelhub.com - "Best AI Video Generators 2026"

### 关键洞察

1. **alici.ai 未被提及** - 需要 AEO 优化
2. **Sora 2 排名第 3** - 强调"story-driven realism"
3. **Kling 2.0 强调**"character consistency"
4. **DeeVid AI 是新竞争者** - 需要关注

**结论**: API 正常工作，返回完整的 LLM 回答内容、工具提及和引用来源。

---

## 维度 4: LLM Mentions (AI 提及分析)

### 测试端点

- `/v3/ai_optimization/llm_mentions/aggregated_metrics/live`
- `/v3/ai_optimization/llm_mentions/search/live`

### 结果

```json
{
  "status_code": 40204,
  "status_message": "Access denied. Visit Plans and Subscriptions to activate your subscription and get access to this API."
}
```

**结论**: LLM Mentions API 需要单独订阅 ($100/月)。当前账户未激活此服务。

---

## 成本汇总

| API 调用 | 成本 |
|----------|------|
| Keywords Data (3 关键词) | $0.075 |
| Google Trends (4 关键词) | $0.009 |
| LLM Responses (1 查询) | $0.072 |
| **合计** | **$0.156** |

---

## 结论与建议

### 可用 API (3/4)

1. **Keywords Data** - 完全可用，支持 Seed Mode Phase 2
2. **Google Trends** - 完全可用，支持趋势分析
3. **LLM Responses** - 完全可用，支持 AI 回答内容分析

### 不可用 API (1/4)

4. **LLM Mentions** - 需要 $100/月订阅

### Seed Mode 影响

| Phase | 原计划 API | 当前状态 | 替代方案 |
|-------|-----------|---------|---------|
| Phase 2 | Keywords Data | **可用** | - |
| Phase 2 | Google Trends | **可用** | - |
| Mode C | LLM Responses | **可用** | - |
| Mode C | LLM Mentions | **不可用** | 使用 LLM Responses 分析竞品提及 |

### 建议

1. **保留当前 3 个 API** - 已足够支持 Seed Mode 核心功能
2. **LLM Mentions 替代方案** - 通过 LLM Responses 查询竞品相关问题，分析回答中的提及情况
3. **成本优化** - 当前 Seed Mode 预估成本 ~$0.47 仍然有效

---

## 修复 Supadata API (YouTube 字幕)

**问题**: Supadata API 返回 401 Unauthorized

**当前替代方案**: 使用 `youtube-transcript-api` Python 库 (免费)

**建议修复步骤**:
1. 检查 Supadata API Key 是否过期
2. 验证 API 端点是否需要更新
3. 在 .mcp.json 中添加 Supadata 配置

---

*报告生成时间: 2026-01-26 00:10:00*
