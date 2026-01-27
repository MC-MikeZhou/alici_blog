---
name: batch-processor
type: skill
provides: batch-workflow-execution
dependencies:
  - smart-router
description: 批量处理器 - 支持多 URL 批量生产
metadata:
  version: 1.1
  author: H
  updated: 2026-01-20
---

# Batch Processor Skill v1.0

## Purpose

支持一次输入多个 URL，批量执行内容生产流程。提供队列管理、进度追踪、错误恢复和汇总报告功能。

## Trigger Words

```yaml
triggers:
  - "批量"
  - "多个"
  - "这些 URL"
  - "batch"
  - "bulk"
  - "/batch-workflow"
```

## Input Formats

### Format 1: 自然语言 + 多 URL

```
批量分析这些竞品:
https://competitor1.com/blog
https://competitor2.com/blog
https://competitor3.com/blog
```

### Format 2: 命令 + 参数

```bash
/batch-workflow https://url1.com https://url2.com https://url3.com
```

### Format 3: 从文件读取

```bash
/batch-workflow --file /path/to/urls.txt
```

`urls.txt` 格式（每行一个 URL）：
```
https://competitor1.com/blog
https://competitor2.com/blog
https://competitor3.com/blog
```

## Processing Flow

```
输入: [URL1, URL2, URL3, ...]
    ↓
┌─────────────────────────────────────────────────────┐
│ Step 1: 创建批量任务                                 │
│ - 生成 batch-{date}-{id} 目录                       │
│ - 创建 00-batch-manifest.json                       │
│ - 记录所有 URL 和初始状态                            │
└──────────────────┬──────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────┐
│ Step 2: 用户确认                                     │
│ - 显示 URL 列表和预估工作量                          │
│ - 选择执行模式 (依次/并行)                           │
│ - 选择工作流类型 (full-workflow/scout-only/etc)      │
└──────────────────┬──────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────┐
│ Step 3: 队列执行                                     │
│ - 依次模式: URL1 → URL2 → URL3 (推荐)               │
│ - 并行模式: 同时 2-3 个 (需谨慎)                     │
│ - 实时更新 manifest 状态                             │
└──────────────────┬──────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────┐
│ Step 4: 错误处理                                     │
│ - 单个失败不影响队列                                 │
│ - 记录失败原因到 manifest                            │
│ - 提供重试选项                                       │
└──────────────────┬──────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────┐
│ Step 5: 汇总报告                                     │
│ - 生成 00-batch-summary.md                          │
│ - 成功/失败统计                                      │
│ - 输出文件列表                                       │
│ - 下一步建议                                         │
└─────────────────────────────────────────────────────┘
```

## Output Directory Structure

```
/reports/batch-YYYY-MM-DD-{id}/
├── 00-batch-manifest.json      # 批量任务清单 (核心追踪文件)
├── 00-batch-summary.md         # 汇总报告 (完成后生成)
├── YYYY-MM-DD-{topic-1}/       # URL1 输出目录
│   ├── 00-implementation.md
│   ├── 00-topic-scout-report.md
│   ├── 00-topic-brief.json
│   ├── 01-article-draft.md
│   └── ...
├── YYYY-MM-DD-{topic-2}/       # URL2 输出目录
│   └── ...
└── YYYY-MM-DD-{topic-3}/       # URL3 输出目录
    └── ...
```

## Manifest File Format

`00-batch-manifest.json`:

```json
{
  "batch_id": "batch-2026-01-20-001",
  "created_at": "2026-01-20T10:30:00Z",
  "workflow": "full-workflow",
  "execution_mode": "sequential",
  "total_urls": 3,
  "status": "in_progress",
  "tasks": [
    {
      "id": 1,
      "url": "https://competitor1.com/blog",
      "status": "completed",
      "started_at": "2026-01-20T10:30:05Z",
      "completed_at": "2026-01-20T10:45:30Z",
      "output_dir": "2026-01-20-ai-video-tools",
      "aeo_score": 82,
      "error": null
    },
    {
      "id": 2,
      "url": "https://competitor2.com/blog",
      "status": "in_progress",
      "started_at": "2026-01-20T10:45:35Z",
      "completed_at": null,
      "output_dir": "2026-01-20-ai-art-generators",
      "aeo_score": null,
      "error": null
    },
    {
      "id": 3,
      "url": "https://competitor3.com/blog",
      "status": "pending",
      "started_at": null,
      "completed_at": null,
      "output_dir": null,
      "aeo_score": null,
      "error": null
    }
  ],
  "summary": {
    "completed": 1,
    "in_progress": 1,
    "pending": 1,
    "failed": 0
  }
}
```

## Execution Steps

### Step 1: Create Batch Task

```bash
# 生成批量任务目录
DATE=$(date +%Y-%m-%d)
BATCH_ID="batch-${DATE}-$(printf '%03d' $(($(ls /reports/batch-${DATE}-* 2>/dev/null | wc -l) + 1)))"
mkdir -p "/reports/${BATCH_ID}"
```

初始化 manifest:
```json
{
  "batch_id": "batch-2026-01-20-001",
  "created_at": "2026-01-20T10:30:00Z",
  "workflow": "full-workflow",
  "execution_mode": "sequential",
  "total_urls": N,
  "status": "created",
  "tasks": [/* URL tasks */]
}
```

### Step 2: User Confirmation

显示确认信息：

```markdown
## Batch Processor - 批量任务确认

**任务 ID**: batch-2026-01-20-001
**URL 数量**: 3
**预估工作流**: full-workflow (选题 → 写作 → 编辑 → 评分)

### URL 列表
1. https://competitor1.com/blog
2. https://competitor2.com/blog
3. https://competitor3.com/blog

### 执行选项
请选择:
1. **依次执行** (推荐) - 更稳定，便于追踪
2. **并行执行** (2个同时) - 更快，但可能有 API 限流

### 工作流选项
请选择:
1. **完整流程** - scout → writer → editor → analyzer
2. **仅选题分析** - 只运行 scout-topic
3. **仅字幕获取** - 只运行 fetch-transcript (YouTube URL)
```

### Step 3: Queue Execution

**依次执行模式** (推荐):

```python
for task in manifest.tasks:
    # 更新状态
    task.status = "in_progress"
    task.started_at = now()
    save_manifest()

    # 执行工作流
    try:
        output_dir = execute_workflow(task.url, manifest.workflow)
        task.status = "completed"
        task.output_dir = output_dir
        task.completed_at = now()
    except Exception as e:
        task.status = "failed"
        task.error = str(e)

    save_manifest()
```

**并行执行模式** (谨慎使用):

```python
# 最多同时 2-3 个任务，避免 API 限流
MAX_CONCURRENT = 2
```

### Step 4: Error Handling

单个任务失败时：
1. 记录错误信息到 manifest
2. 继续处理下一个任务
3. 最后汇总失败任务

```json
{
  "id": 2,
  "url": "https://competitor2.com/blog",
  "status": "failed",
  "error": "DataForSEO API rate limit exceeded",
  "retry_count": 0
}
```

### Step 5: Summary Report

生成 `00-batch-summary.md`:

```markdown
# Batch Summary Report

**Batch ID**: batch-2026-01-20-001
**执行时间**: 2026-01-20 10:30 - 12:45
**总耗时**: 2小时15分钟

## 执行统计

| 状态 | 数量 | 百分比 |
|------|------|--------|
| 成功 | 8 | 80% |
| 失败 | 1 | 10% |
| 跳过 | 1 | 10% |
| **总计** | **10** | **100%** |

## 成功任务

| # | URL | 选题 | AEO 分数 | 输出目录 |
|---|-----|------|----------|----------|
| 1 | competitor1.com | AI Video Tools | 82 | /2026-01-20-ai-video-tools/ |
| 2 | competitor2.com | AI Art Generators | 78 | /2026-01-20-ai-art-generators/ |
| ... | ... | ... | ... | ... |

## 失败任务

| # | URL | 错误原因 | 建议操作 |
|---|-----|----------|----------|
| 5 | competitor5.com | API rate limit | 等待后重试 |

## 输出文件汇总

```
/reports/batch-2026-01-20-001/
├── 2026-01-20-ai-video-tools/01-article-edited.md ✅
├── 2026-01-20-ai-art-generators/01-article-edited.md ✅
├── ... (共 8 篇文章)
```

## 下一步建议

1. 检查失败任务，考虑重试: `/batch-retry batch-2026-01-20-001`
2. 批量导出 Framer JSON: `/batch-export batch-2026-01-20-001`
3. 查看任一文章详情: `cat /reports/batch-2026-01-20-001/2026-01-20-ai-video-tools/03-aeo-score.md`

---
*Generated by Batch Processor v1.0*
```

## Session Recovery

如果会话中断，可以通过读取 manifest 恢复：

```bash
# 检查未完成的批量任务
ls /reports/batch-*/00-batch-manifest.json | while read f; do
  status=$(jq -r '.status' "$f")
  if [ "$status" != "completed" ]; then
    echo "未完成: $f"
  fi
done
```

恢复命令：
```
/batch-resume batch-2026-01-20-001
```

恢复逻辑：
1. 读取 manifest
2. 跳过已完成的任务
3. 从第一个 pending/failed 任务继续

## Workflow Types

| 工作流 | 命令 | 适用场景 |
|--------|------|----------|
| `full-workflow` | 完整流程 | 竞品 URL，需要完整文章 |
| `scout-only` | 仅选题 | 批量收集选题不写文章 |
| `transcript-only` | 仅字幕 | YouTube URL 批量获取字幕 |
| `analyze-only` | 仅评分 | 批量评估现有文章 |

## Configuration Options

```json
{
  "execution_mode": "sequential",  // sequential | parallel
  "max_concurrent": 2,             // 并行模式最大并发数
  "continue_on_error": true,       // 单个失败是否继续
  "auto_retry": false,             // 失败是否自动重试
  "max_retry": 3,                  // 最大重试次数
  "notify_on_complete": true       // 完成后是否通知
}
```

## Integration with Smart Router

当 smart-router 检测到多个 URL 时，自动调用 batch-processor：

```
smart-router 检测到 3 个 URL
    ↓
路由到 batch-processor
    ↓
batch-processor 创建任务并执行
```

## Error Codes

| 错误码 | 描述 | 处理建议 |
|--------|------|----------|
| `E001` | URL 无法访问 | 检查 URL 有效性 |
| `E002` | API 限流 | 等待后重试 |
| `E003` | 选题分析失败 | 检查 DataForSEO 配置 |
| `E004` | 写作生成失败 | 检查 Topic Brief |
| `E005` | AEO 评分超时 | 重新运行 analyze-aeo |

## Usage Examples

### Example 1: 批量竞品分析

```
批量分析这些竞品博客:
https://higgsfield.ai/blog
https://runway.ai/blog
https://pika.art/blog
```

### Example 2: 批量获取 YouTube 字幕

```
/batch-workflow --workflow transcript-only \
  https://youtube.com/watch?v=xxx \
  https://youtube.com/watch?v=yyy \
  https://youtube.com/watch?v=zzz
```

### Example 3: 从文件批量执行

```bash
# 创建 URL 列表文件
cat > /tmp/urls.txt << EOF
https://competitor1.com/blog
https://competitor2.com/blog
https://competitor3.com/blog
EOF

# 执行批量任务
/batch-workflow --file /tmp/urls.txt
```

### Example 4: 恢复中断的批量任务

```
/batch-resume batch-2026-01-20-001
```

## Notes

- 默认使用依次执行模式，更稳定
- 并行模式建议最多 2 个同时执行，避免 API 限流
- manifest 文件是任务恢复的关键，请勿删除
- 建议在开始批量任务前确认 MCP 配置正常
- 批量任务可能消耗较多上下文，注意 30% 警戒线

---

*Batch Processor v1.0 - 规模化内容生产*
