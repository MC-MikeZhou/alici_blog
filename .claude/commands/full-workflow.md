# /full-workflow - 完整内容生产流程

一键执行从竞品分析到发布就绪的完整工作流。

## 预置上下文

```bash
# 当前日期
echo "工作流启动: $(date +%Y-%m-%d %H:%M)"

# 检查 MCP 状态
echo "DataForSEO MCP:"
cat /Users/H/Documents/AliciBlog/.mcp.json 2>/dev/null | grep -A2 "dataforseo"

# 检查 Skills 状态
echo "已加载 Skills:"
ls /Users/H/Documents/AliciBlog/skills/*/SKILL.md /Users/H/Documents/AliciBlog/skills/*/*/SKILL.md 2>/dev/null | wc -l
```

## 工作流步骤

```
┌─────────────────────────────────────────────────────────────┐
│ Phase 1: 选题发现                                            │
│ /scout-topic → Top 10 选题 → 用户选择                        │
├─────────────────────────────────────────────────────────────┤
│ Phase 2: 内容生成                                            │
│ /write-tutorial 或 /write-list → 文章初稿                   │
├─────────────────────────────────────────────────────────────┤
│ Phase 3: 中文预览 (可选)                                     │
│ /preview-chinese → 团队快速审核                              │
├─────────────────────────────────────────────────────────────┤
│ Phase 4: 质量保障                                            │
│ /analyze-aeo → 评分                                          │
│ └─ < 75分 → /improve-article (max 3轮)                       │
│ └─ ≥ 75分 → 继续下一阶段                                     │
├─────────────────────────────────────────────────────────────┤
│ Phase 5: 内容编辑                                            │
│ /edit-article → 图片生成 + 开篇优化 + AEO 增强              │
├─────────────────────────────────────────────────────────────┤
│ Phase 6: 导出 JSON                                           │
│ /convert-to-framer → Framer CMS JSON                        │
│ └─ 自动校验 + 自动修复                                       │
│ └─ 双路径输出 → 发布就绪 ✅                                   │
├─────────────────────────────────────────────────────────────┤
│ Phase 7: 视频集成 (可选)                                     │
│ 询问是否需要插入视频 → 若是：                               │
│ /convert-to-video-framer-json 06-article-final.json         │
│ └─ 解析 /video_resources/video_links.txt → 选择插入位置      │
│ └─ 输出 *-video.json (非破坏性，仅新增)                      │
└─────────────────────────────────────────────────────────────┘
```

## 输出目录结构

```
/reports/[YYYY-MM-DD]-[topic-slug]/
├── 00-implementation.md      # 进度追踪 (支持会话恢复)
├── 00-topic-scout-report.md  # 选题分析报告
├── 00-topic-brief.json       # Topic Brief JSON
├── 01-article-draft.md       # 文章初稿
├── 01-article-edited.md      # 编辑版 (图片+开篇优化)
├── 02-chinese-preview.md     # 中文预览
├── 03-aeo-score.md           # AEO 评分报告
├── 04-editor-report.md       # 编辑报告
├── 05-article-improved.md    # 改进版文章 (如需)
└── 06-article-final.json     # Framer CMS JSON (最终输出)
    06-article-final-video.json  # (可选) 含视频版本，输入名 + -video.json

/blog_new_sam 11.20.2025/output/
└── [slug].json               # 交付给同事的 JSON 副本
```

## 质量门禁

| 阶段 | 门禁 | 未通过处理 |
|------|------|-----------|
| 选题 | Opportunity Score ≥ 60 | 重新选题 |
| 生成 | 字数达标 + 结构完整 | 补充内容 |
| 评分 | AEO ≥ 75 | 自动改进 (max 3轮) |
| 改进 | 3轮后仍 < 75 | MANUAL_REVIEW |
| 导出 | JSON 校验通过 | 自动修复 |

## 人工节点

1. **选题确认** - 从 Top 10 中选择
2. **最终审核** - 发布前确认

## 使用示例

```
/full-workflow https://competitor.com/blog/ai-video-guide
```

## 会话恢复

如果会话中断，Claude 会读取 `00-implementation.md` 继续执行。

---

*整合 AliciBlog 2.0 全部 Skills*
