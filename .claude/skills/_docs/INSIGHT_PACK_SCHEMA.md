# Insight Pack Schema v1.0

> 用于 blog-tutorial-writer v2.5+ 的结构化竞品分析数据输入

## 版本

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-02-05 | 初始版本 |

## 完整 Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Insight Pack",
  "type": "object",
  "required": ["thesis", "why_now", "key_takeaways"],
  "properties": {
    "thesis": {
      "type": "string",
      "description": "核心论点 (1 句话)",
      "maxLength": 200
    },
    "why_now": {
      "type": "string",
      "description": "为什么现在写这个选题",
      "maxLength": 300
    },
    "key_takeaways": {
      "type": "array",
      "description": "3-5 个关键要点",
      "items": {"type": "string"},
      "minItems": 3,
      "maxItems": 5
    },
    "market_data": {
      "type": "object",
      "description": "市场数据 (触发 Market Context 章节)",
      "properties": {
        "market_size": {"type": "string"},
        "cagr": {"type": "string"},
        "key_metrics": {
          "type": "object",
          "additionalProperties": {"type": "string"}
        }
      }
    },
    "monetization_paths": {
      "type": "array",
      "description": "变现路径 (触发 Monetization Framework 章节)",
      "items": {
        "type": "object",
        "properties": {
          "path": {"type": "string"},
          "income_range": {"type": "string"}
        }
      }
    },
    "competitive_sources": {
      "type": "array",
      "description": "数据来源引用 (用于 E-E-A-T)",
      "items": {
        "type": "object",
        "properties": {
          "source": {"type": "string"},
          "data_used": {"type": "string"}
        }
      }
    },
    "content_gaps": {
      "type": "array",
      "description": "竞品内容空白点 (差异化方向)",
      "items": {"type": "string"}
    }
  }
}
```

## 使用示例

### 完整示例：AI Influencer + UGC Ads 变现选题

```json
{
  "insight_pack": {
    "thesis": "AI Influencer + UGC Ads 是 2026 年内容创作者最赚钱的组合",
    "why_now": "市场爆发期（$6.06B） + 技术成熟（SoulID） + 成本优势（-70%）",
    "key_takeaways": [
      "SoulID 技术保持虚拟网红角色一致性",
      "170+ 语言全球化能力，无需真人出镜",
      "UGC 广告 CTR 提升 4 倍，成本降低 70%",
      "日更 20 条内容的规模化生产能力",
      "5 种变现模式：代言/服务/产品/直播/授权"
    ],
    "market_data": {
      "market_size": "$6.06B (2024)",
      "cagr": "40.8% (2025-2030)",
      "key_metrics": {
        "ctr_improvement": "4x vs 传统广告",
        "cost_reduction": "70% vs 传统拍摄",
        "conversion_lift": "29% 转化率提升"
      }
    },
    "monetization_paths": [
      {"path": "品牌代言", "income_range": "$500-$50,000/条"},
      {"path": "UGC 广告服务", "income_range": "$100-$500/视频"},
      {"path": "数字产品", "income_range": "被动收入"},
      {"path": "直播带货", "income_range": "佣金分成"},
      {"path": "IP 授权", "income_range": "年度授权费"}
    ],
    "competitive_sources": [
      {"source": "Higgsfield", "data_used": "SoulID 技术、UGC Factory"},
      {"source": "HeyGen", "data_used": "Avatar IV、170+ 语言"},
      {"source": "Invideo", "data_used": "4x CTR、29% 转化率"}
    ],
    "content_gaps": [
      "中文市场策略（抖音/小红书/快手）",
      "具体变现金额案例",
      "从 0 到 1 的启动路径"
    ]
  }
}
```

### 最小化示例（仅必需字段）

```json
{
  "insight_pack": {
    "thesis": "AI 工具 X 可以提升内容创作效率 10 倍",
    "why_now": "技术成熟 + 成本可接受 + 市场需求爆发",
    "key_takeaways": [
      "核心功能 A 解决痛点 1",
      "核心功能 B 解决痛点 2",
      "实测数据：效率提升 10 倍"
    ]
  }
}
```

## 字段说明

### 必需字段

| 字段 | 类型 | 说明 | 最佳实践 |
|------|------|------|----------|
| `thesis` | string | 核心论点（1 句话） | 清晰陈述主题价值主张 |
| `why_now` | string | 时机解释 | 市场趋势 + 技术成熟度 + 成本优势 |
| `key_takeaways` | array | 3-5 个要点 | 提取最核心的价值点 |

### 可选字段

| 字段 | 类型 | 触发效果 | 何时使用 |
|------|------|----------|----------|
| `market_data` | object | 生成 Market Context 章节 | 有市场规模/增长率数据时 |
| `monetization_paths` | array | 生成 Monetization Framework 章节 | 变现导向选题 |
| `competitive_sources` | array | 增强 E-E-A-T 信号 | 有竞品分析数据时 |
| `content_gaps` | array | 指导差异化方向 | 需要与竞品区分时 |

## 与 Topic Brief 的关系

Insight Pack 是 Topic Brief 的补充输入：

```
growth-topic-scout 输出 Topic Brief
         +
用户提供 Insight Pack (可选)
         ↓
blog-tutorial-writer v2.5
```

## 向后兼容性

未提供 Insight Pack 时，blog-tutorial-writer 使用默认行为（v2.4 及之前版本逻辑）。
