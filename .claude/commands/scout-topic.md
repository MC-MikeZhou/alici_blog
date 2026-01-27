# /scout-topic - 竞品分析与选题发现

使用 growth-topic-scout Skill 分析竞品内容，发现 Top 10 选题机会。

## 预置上下文

```bash
# 当前日期
echo "今日日期: $(date +%Y-%m-%d)"

# 检查 DataForSEO MCP 状态
echo "MCP 配置状态:"
cat /Users/H/Documents/AliciBlog/.mcp.json 2>/dev/null | head -5
```

## 执行步骤

1. **获取输入**: 用户提供竞品 URL（1-3 个）
2. **内容抓取**: 使用 WebFetch 获取竞品内容
3. **主题提取**: 分析 H1/H2/H3 层级，提取关键实体
4. **Query 生成**: 生成 20-60 个候选搜索词
5. **市场验证**: 使用 WebSearch/DataForSEO 验证搜索量
6. **机会评分**: 4 维度评分（需求 30% + AEO 25% + 竞争 25% + 业务 20%）
7. **输出报告**: Top 10 选题 + Topic Brief JSON

## 输出位置

```
/reports/[YYYY-MM-DD]-[topic-slug]/
├── 00-topic-scout-report.md    # 人可读报告
└── 00-topic-brief.json         # 机器可读 JSON
```

## 质量门禁

- 每个选题必须有 Opportunity Score ≥ 60
- 必须验证搜索量数据来源
- 必须包含 product_mapping

## 使用示例

```
/scout-topic https://competitor.com/blog/article-1
```

---

*基于 growth-topic-scout Skill v1.1*
