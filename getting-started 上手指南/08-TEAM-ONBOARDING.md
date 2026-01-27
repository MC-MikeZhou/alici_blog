# 08-TEAM-ONBOARDING.md

> 新成员 10 分钟上手指南

---

## 〇、文档层次结构（新同事必读）

**⚠️ 重要**: 修改 CTA/品牌颜色/标题公式时，应修改 Level 1 配置文档，而非直接改 Skill

```
Level 0: /CLAUDE.md                              ← 入口（自动加载）
         ↓
Level 1: 核心配置文档（所有 Skills 共享依赖）
         ├── /skills/_docs/PRODUCT_CATALOG.md         ← CTA、定价
         ├── /skills/_docs/BRAND_VISUAL_GUIDE.md      ← 绿色视觉规范
         └── /skills/_docs/BLOG_WRITING_PRINCIPLES_v2.md  ← 标题公式、评测方法论
         ↓
Level 2: /blueprint/                             ← 架构与哲学
         ├── 00-CONTENT-PHILOSOPHY.md            ← 内容策略哲学（Higgsfield 洞察）
         └── 其他 blueprint 文档
         ↓
Level 3: 各 Skill SKILL.md                       ← 执行规范（引用上层文档）
         ├── /skills/core/editor/SKILL.md
         ├── /skills/writers/blog-tutorial-writer/SKILL.md
         └── /skills/writers/blog-list-writer/SKILL.md
```

### 为什么这个层次很重要？

| 如果你想修改... | 应该改哪个文件 | ❌ 不要改 |
|----------------|---------------|----------|
| CTA 链接或产品定价 | `PRODUCT_CATALOG.md` | 各 SKILL.md |
| 图片品牌颜色（绿色→其他） | `BRAND_VISUAL_GUIDE.md` | image-prompt-templates.yaml |
| 标题公式或评测框架 | `BLOG_WRITING_PRINCIPLES_v2.md` | 各 writer SKILL.md |
| 单个 Skill 的特定行为 | 对应的 SKILL.md | 上层配置文档 |

### 新同事常见错误

1. ❌ 直接在 SKILL.md 中硬编码 CTA 链接 → 导致链接不一致
2. ❌ 在 prompts/image-prompt-templates.yaml 中改颜色 → 未同步 BRAND_VISUAL_GUIDE.md
3. ❌ 不知道 BRAND_VISUAL_GUIDE.md 存在 → 图片生成风格不符合品牌

---

## 一、快速开始（10分钟）

### 第 0 步：阅读核心配置文档（1分钟）

**先了解系统依赖的核心文档**（上面的 Level 1）：
1. `PRODUCT_CATALOG.md` - 所有产品 CTA 映射
2. `BRAND_VISUAL_GUIDE.md` - 绿色视觉规范（ICSB 框架）
3. `BLOG_WRITING_PRINCIPLES_v2.md` - 标题公式和评测方法论

### 第 1 步：理解系统（2分钟）

阅读 `/CLAUDE.md` 的以下内容：
1. 核心架构图 - 了解三层结构
2. 5 条黄金规则 - 牢记使用原则
3. **文档索引** - 知道关键配置文档在哪里 ← 新增
4. 命令速查 - 知道有哪些命令

### 第 2 步：体验完整流程（5分钟）

运行一次完整工作流：
```bash
/full-workflow https://example.com/blog/ai-video-tools
```

观察输出到 `/reports/` 的文件结构：
```
/reports/2026-01-15-ai-video-tools/
├── 00-implementation.md      ← 进度追踪
├── 00-topic-scout-report.md  ← 选题分析
├── 01-article-draft.md       ← 生成的文章
├── 03-aeo-score.md           ← 质量评分
└── ...
```

### 第 3 步：独立运行单个命令（3分钟）

尝试单独运行各个命令，熟悉每个环节：

| 命令 | 作用 | 输入 |
|------|------|------|
| `/scout-topic URL` | 竞品分析 + 选题 | 竞品文章 URL |
| `/write-tutorial` | 生成教程文章 | 基于 Topic Brief |
| `/analyze-aeo FILE` | 评估质量 | 文章文件路径 |

---

## 二、团队协作规范

### CLAUDE.md 更新流程

```
发现 Claude 犯错
        ↓
立即添加到 CLAUDE.md 的「不要做的事」
        ↓
每周五团队同步，整理本周发现
        ↓
重大更新通知所有成员（飞书/Slack）
```

**更新示例**：
```markdown
## 不要做的事

- ❌ [原有内容]
- ❌ 让 Claude 生成超过 3000 词的文章（会跑偏）← 新增
```

### 并行工作

| 场景 | 推荐实例数 | 说明 |
|------|-----------|------|
| 批量内容生产 | 5-10 个 | 每个实例处理一个选题 |
| 日常工作 | 1-3 个 | 主任务 + 辅助查询 |
| 紧急内容 | 1 个 | 专注完成 |

**并行启动方式**：
- 终端: 开多个 Tab，每个运行 Claude Code
- Web: 使用 claude.ai/code 同时开多个会话
- 混合: 本地 + Web 同时进行

### 工作交接

当任务需要交接给其他同事时：

1. **交接前**：确保 `00-implementation.md` 已更新到最新状态
2. **交接内容**：告知同事项目目录路径
3. **接手后**：读取 `00-implementation.md`，从中断点继续

```bash
# 接手后的第一步
读取 /reports/2026-01-15-ai-video/00-implementation.md
然后运行对应的下一个命令
```

---

## 三、常见场景处理

### 场景 1: 生成一篇新文章

```
1. /scout-topic https://competitor.com/article
2. 确认选择的选题
3. /write-tutorial 或 /write-list
4. /edit-article [生成的文章路径]
5. /analyze-aeo [编辑后的文章路径]
6. 如果 AEO < 75: /improve-article
7. /preview-chinese [最终文章路径]
8. 人工审核 → 发布
```

### 场景 2: 批量生成内容

```
1. 先用 /scout-topic 生成 10 个选题
2. 启动 5 个 Claude 实例
3. 每个实例处理 2 个选题
4. 各自完成后汇总到同一目录
```

### 场景 3: 会话中断恢复

```
1. 进入 /reports/[日期]-[主题]/ 目录
2. 读取 00-implementation.md
3. 找到当前阶段（Phase X）
4. 运行对应的斜杠命令继续
```

### 场景 4: AEO 分数提不上去

参考 `/blueprint/09-TROUBLESHOOTING.md` 中的检查清单。

---

## 四、质量门禁

系统内置的质量控制点：

| 阶段 | 门禁条件 | 未通过处理 |
|------|----------|-----------|
| 选题 | Opportunity Score ≥ 60 | 重新选题 |
| 生成 | 字数达标 + 结构完整 | 重新生成 |
| 评分 | AEO Score ≥ 75 | 自动改进（最多 3 轮） |
| 改进 | 3 轮后仍 < 75 | 人工介入 |

---

## 五、资源索引

| 需求 | 参考文档 |
|------|----------|
| 系统总览 | `/CLAUDE.md` |
| 所有 Skills 详情 | `/blueprint/02-SKILLS.md` |
| 最佳实践 | `/blueprint/07-BEST-PRACTICES.md` |
| 故障排除 | `/blueprint/09-TROUBLESHOOTING.md` |
| AEO 评分标准 | `/skills/core/aeo-analyzer/EVALUATION_FRAMEWORK.md` |
| 内容规范 | `blog_new_sam 11.20.2025/doc/*.md` |

---

## 六、快速问答

**Q: 第一次用应该从哪个命令开始？**
A: `/full-workflow URL` - 体验完整流程

**Q: 文章生成后下一步做什么？**
A: `/edit-article` 添加图片和优化，然后 `/analyze-aeo` 评分

**Q: Claude 卡住了怎么办？**
A: `/clear` 清除上下文，简化任务重新开始

**Q: 如何知道当前进度？**
A: 查看项目目录下的 `00-implementation.md`

---

*有问题找不到答案？添加到这个 FAQ 中！*
