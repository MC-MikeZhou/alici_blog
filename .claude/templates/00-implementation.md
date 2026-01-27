# Implementation Progress

> 工作流进度追踪 - 支持会话恢复

---

## 基本信息

| 字段 | 值 |
|------|-----|
| **创建时间** | [YYYY-MM-DD HH:MM] |
| **选题** | [Topic Title] |
| **输入源** | [URL / Notion / Text] |
| **文章类型** | [tutorial / list / news] |
| **目标 AEO** | ≥ 75 |

---

## 阶段进度

### Phase 1: 选题发现
- [ ] 竞品分析完成
- [ ] Top 10 选题生成
- [ ] 用户选择确认
- [ ] Topic Brief 输出

**状态**: `pending` | `in_progress` | `completed` | `skipped`

**输出文件**:
- `00-topic-scout-report.md`
- `00-topic-brief.json`

---

### Phase 2: 内容生成
- [ ] 文章类型确定
- [ ] 初稿生成
- [ ] 字数验证 (Tutorial: 1800-2500 / List: 2000-3000)
- [ ] 结构验证

**状态**: `pending` | `in_progress` | `completed`

**输出文件**:
- `01-article-draft.md`

---

### Phase 3: 中文预览 (可选)
- [ ] 预览生成
- [ ] 团队审核

**状态**: `pending` | `in_progress` | `completed` | `skipped`

**输出文件**:
- `02-chinese-preview.md`

---

### Phase 4: 质量保障
- [ ] AEO 评分完成
- [ ] 评分 ≥ 75？

**状态**: `pending` | `in_progress` | `completed`

**当前评分**: [XX] / 100

**输出文件**:
- `03-aeo-score.md`

---

### Phase 5: 自动改进 (如需)
- [ ] 改进轮次 1
- [ ] 改进轮次 2
- [ ] 改进轮次 3
- [ ] 最终评分 ≥ 75？

**状态**: `pending` | `in_progress` | `completed` | `manual_review`

**改进历史**:
| 轮次 | 改进前 | 改进后 | 主要改动 |
|------|--------|--------|----------|
| 1 | - | - | - |
| 2 | - | - | - |
| 3 | - | - | - |

**输出文件**:
- `04-article-improved.md`
- `04-changelog.md`

---

### Phase 6: 最终输出
- [ ] 最终文章生成
- [ ] 人工审核确认
- [ ] Framer JSON 输出 (如需)

**状态**: `pending` | `in_progress` | `completed`

**输出文件**:
- `05-article-final.md`
- `05-framer-cms.json` (可选)

---

## 会话记录

| 时间 | 会话 ID | 中断点 | 备注 |
|------|---------|--------|------|
| [YYYY-MM-DD HH:MM] | [session-1] | Phase X | 初始会话 |

---

## 决策记录

### Decision 1: [标题]
- **日期**: [YYYY-MM-DD]
- **背景**: [为什么需要决策]
- **选项**: [考虑的选项]
- **决定**: [最终选择]
- **原因**: [选择原因]

---

## 问题追踪

| ID | 问题 | 状态 | 解决方案 |
|----|------|------|----------|
| 1 | - | open/resolved | - |

---

## 下次继续

**当前阶段**: [Phase X]
**下一步**: [具体动作]
**阻塞项**: [如有]

---

*此文件由 Claude 自动维护，支持会话中断后恢复。*
