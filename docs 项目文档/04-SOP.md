# 04 - SOP 标准操作规程

> 各生产线的标准操作规程总览

---

## SOP 目录结构

```
sop/
├── _overview.md                  # SOP 总览（待创建）
│
├── blog-production/              # Blog 生产线 SOP
│   ├── 01-content-discovery.md   # 内容发现流程
│   ├── 02-content-filtering.md   # 内容筛选标准
│   ├── 03-content-creation.md    # 内容生产流程
│   ├── 04-quality-assurance.md   # 质量保证流程
│   ├── 05-publishing.md          # 发布流程
│   └── 06-monitoring.md          # 监测反馈流程
│
├── hitclone-production/          # HitClone 生产线 SOP
│   └── ...
│
└── vsa-production/               # VSA 生产线 SOP
    └── ...
```

---

## Blog 生产线 SOP

### 流程概览

```
内容发现 → 内容筛选 → [人工确认] → 内容生产 → 质量检查 → [人工审核] → 发布 → 监测
```

### SOP 清单

| SOP | 说明 | 负责角色 | 状态 |
|-----|------|----------|------|
| 01-content-discovery | 如何发现值得写的内容 | Scout Agent / 人工 | 待编写 |
| 02-content-filtering | 内容筛选的标准和规则 | Filter Skill | 待编写 |
| 03-content-creation | 内容生产的完整流程 | Writer Skills | 待编写 |
| 04-quality-assurance | 质量检查的标准和流程 | QA Skill | 待编写 |
| 05-publishing | 发布到 Framer 的流程 | Publisher Skill | 待编写 |
| 06-monitoring | 发布后的监测和反馈 | Monitor Agent | 待编写 |

### 现有规范文档

Blog 生产线已有以下规范文档可作为 SOP 基础：

| 文档 | 位置 | 用途 |
|------|------|------|
| 4_Tutorial类内容规范.md | blog_new_sam/doc/ | Tutorial 文章标准 |
| 5_List类内容规范.md | blog_new_sam/doc/ | List 文章标准 |
| 6_News类内容规范.md | blog_new_sam/doc/ | News 文章标准 |
| readme.txt | blog_new_sam/ | 7 步工作流说明 |
| blog.json | blog_new_sam/doc/ | JSON 输出示例 |

---

## HitClone 生产线 SOP

### 流程概览

```
视频发现 → 视频分析 → [人工确认] → 页面生成 → 质量检查 → [人工审核] → 发布 → 监测
```

### SOP 清单

| SOP | 说明 | 状态 |
|-----|------|------|
| 01-video-discovery | 如何发现热门 YouTube 视频 | 待编写 |
| 02-video-analysis | 视频分析的标准流程 | 待编写 |
| 03-page-generation | 克隆页面生成流程 | 待编写 |
| 04-quality-assurance | 质量检查标准 | 待编写 |
| 05-publishing | 发布流程 | 待编写 |

---

## VSA 生产线 SOP

### 流程概览

```
热点发现 → 概念提炼 → [人工确认] → Use Case 生成 → 质量检查 → [人工审核] → 发布 → 监测
```

### SOP 清单

| SOP | 说明 | 状态 |
|-----|------|------|
| 01-trend-discovery | 如何发现病毒视频/热点 | 待编写 |
| 02-concept-extraction | 如何提炼 AI 可实现的概念 | 待编写 |
| 03-usecase-creation | Use Case 页面生成流程 | 待编写 |
| 04-quality-assurance | 质量检查标准 | 待编写 |
| 05-publishing | 发布流程 | 待编写 |

---

## 运维手册 (Runbooks)

```
runbooks/
├── incident-response.md      # 异常处理手册
├── skill-update.md           # Skill 更新流程
└── agent-maintenance.md      # Agent 维护流程
```

### Runbooks 清单

| Runbook | 说明 | 状态 |
|---------|------|------|
| incident-response | 异常情况的处理流程 | 待编写 |
| skill-update | 如何更新和迭代 Skill | 待编写 |
| agent-maintenance | Agent 的日常维护 | 待编写 |

---

## SOP 编写原则

### 格式要求

每份 SOP 应包含：

1. **目的**: 这个流程要解决什么问题
2. **适用范围**: 什么情况下使用
3. **角色**: 谁负责执行
4. **流程步骤**: 具体的操作步骤
5. **检查清单**: 完成标准
6. **异常处理**: 出问题怎么办

### 编写优先级

| 优先级 | SOP | 理由 |
|--------|-----|------|
| P0 | Blog 03-content-creation | 核心生产流程 |
| P0 | Blog 04-quality-assurance | 质量保证 |
| P1 | Blog 05-publishing | 发布流程 |
| P1 | Blog 01-content-discovery | 上游流程 |
| P2 | HitClone 全流程 | 第二条线 |
| P2 | VSA 全流程 | 第三条线 |

---

**上一篇**: [03-AGENTS.md](./03-AGENTS.md) - Agents 清单与定义
**下一篇**: [05-IMPLEMENTATION.md](./05-IMPLEMENTATION.md) - 实施计划与优先级
