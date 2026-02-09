# /batch-workflow - 批量内容生产流程

批量处理多个 URL，支持依次或并行执行完整工作流。

## 预置上下文

```bash
# 当前日期
echo "批量工作流启动: $(date +%Y-%m-%d %H:%M)"

# 检查 MCP 状态
echo "DataForSEO MCP:"
cat .mcp.json 2>/dev/null | grep -A2 "dataforseo"

# 检查已有批量任务
echo "已有批量任务:"
ls -d reports/batch-* 2>/dev/null | wc -l
```

## 使用方法

### 方式 1: 直接传入 URL

```bash
/batch-workflow URL1 URL2 URL3
```

### 方式 2: 从文件读取

```bash
/batch-workflow --file /path/to/urls.txt
```

### 方式 3: 指定工作流类型

```bash
# 仅选题分析
/batch-workflow --workflow scout-only URL1 URL2 URL3

# 仅获取字幕 (YouTube URL)
/batch-workflow --workflow transcript-only URL1 URL2 URL3
```

## 工作流步骤

```
┌─────────────────────────────────────────────────────────────────┐
│ Phase 1: 创建批量任务                                            │
│ - 生成 batch-{date}-{id} 目录                                   │
│ - 创建 00-batch-manifest.json                                   │
│ - 显示 URL 列表供用户确认                                        │
├─────────────────────────────────────────────────────────────────┤
│ Phase 2: 用户确认                                                │
│ - 确认 URL 列表                                                  │
│ - 选择执行模式 (依次/并行)                                       │
│ - 选择工作流类型 (full/scout/transcript)                         │
├─────────────────────────────────────────────────────────────────┤
│ Phase 3: 队列执行                                                │
│ - 依次执行各 URL 的工作流                                        │
│ - 实时更新 manifest 状态                                         │
│ - 单个失败不影响队列                                             │
├─────────────────────────────────────────────────────────────────┤
│ Phase 4: 汇总报告                                                │
│ - 生成 00-batch-summary.md                                      │
│ - 成功/失败统计                                                  │
│ - 输出文件列表                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## 输出目录结构

```
/reports/batch-YYYY-MM-DD-{id}/
├── 00-batch-manifest.json      # 批量任务清单
├── 00-batch-summary.md         # 汇总报告
├── YYYY-MM-DD-{topic-1}/       # URL1 输出
│   ├── 00-implementation.md
│   ├── 00-topic-scout-report.md
│   ├── 00-topic-brief.json
│   ├── 01-article-draft.md
│   └── ...
├── YYYY-MM-DD-{topic-2}/       # URL2 输出
│   └── ...
└── YYYY-MM-DD-{topic-3}/       # URL3 输出
    └── ...
```

## 可用工作流类型

| 类型 | 参数 | 说明 |
|------|------|------|
| 完整流程 | `full-workflow` (默认) | scout → writer → editor → analyzer |
| 仅选题 | `scout-only` | 只运行选题分析，不写文章 |
| 仅字幕 | `transcript-only` | YouTube URL 批量获取字幕 |
| 仅评分 | `analyze-only` | 批量评估现有文章 |

## 执行模式

| 模式 | 参数 | 说明 |
|------|------|------|
| 依次执行 | `--sequential` (默认) | URL1 → URL2 → URL3，更稳定 |
| 并行执行 | `--parallel` | 同时处理 2 个 URL，更快但需注意限流 |

## 使用示例

```bash
# 批量分析 3 个竞品博客
/batch-workflow https://higgsfield.ai/blog https://runway.ai/blog https://pika.art/blog

# 批量获取 YouTube 字幕
/batch-workflow --workflow transcript-only \
  https://youtube.com/watch?v=xxx \
  https://youtube.com/watch?v=yyy

# 从文件读取 URL 列表
/batch-workflow --file /tmp/competitor-urls.txt

# 并行执行 (谨慎使用)
/batch-workflow --parallel URL1 URL2 URL3
```

## 会话恢复

如果会话中断，可以恢复未完成的批量任务：

```bash
# 列出未完成的批量任务
ls /reports/batch-*/00-batch-manifest.json

# 恢复特定批量任务
/batch-resume batch-2026-01-20-001
```

## 质量门禁

继承 `/full-workflow` 的所有质量门禁：

| 阶段 | 门禁 | 未通过处理 |
|------|------|-----------|
| 选题 | Opportunity Score ≥ 60 | 跳过该 URL，记录原因 |
| 生成 | 字数达标 + 结构完整 | 补充内容 |
| 评分 | AEO ≥ 75 | 自动改进 (max 3轮) |
| 改进 | 3轮后仍 < 75 | 标记需人工审核 |

## 错误处理

单个 URL 失败不会终止整个批量任务：

```json
{
  "id": 2,
  "url": "https://competitor2.com/blog",
  "status": "failed",
  "error": "DataForSEO API rate limit exceeded"
}
```

失败任务会被记录，可以稍后重试：

```bash
/batch-retry batch-2026-01-20-001
```

## 注意事项

- 默认使用依次执行模式，避免 API 限流
- 批量任务可能消耗较多上下文，注意 30% 警戒线
- 建议单次批量不超过 10 个 URL
- manifest.json 是任务恢复的关键，请勿删除

---

*整合 AliciBlog 2.3 批量处理能力*
