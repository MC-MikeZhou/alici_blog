# Human Review Checklist - Changelog

## [1.1.1] - 2026-02-03

### 文档改进

- **Module 4 依赖说明增强**: 明确指出需要读取 `/skills/_docs/BLOG_CONTENT_REGISTRY.md`
  - 新增"依赖文件"小节，说明 Registry 中各表格的用途
  - 代码示例更新：显式展示 Registry 文件读取步骤
  - 强调只链接 Status=Published 的文章
- **维护规则新增**: 在 SKILL.md 底部新增"Changelog 强制更新"规则
  - 每次修改 Skill 必须同步更新 CHANGELOG.md
  - 遵循 SemVer 版本号规范

### 触发背景

BLOG_CONTENT_REGISTRY.md 同步更新后（v1.2.0），发现 Module 4 内链检查没有明确引用该文件路径，导致执行时可能遗漏读取 Registry。

---

## [1.1.0] - 2026-02-01

### 核心理念升级 ⭐

**v1.0 的问题**: 只检查"技术指标"（CTR、内链、竞品），没有从**目标读者视角**审视。

**v1.1 的核心**:
1. 先识别目标读者是谁
2. 站在读者视角问：他们能看懂吗？他们会怎么搜索？他们的问题是什么？
3. 然后检查：文章是否用读者的语言在回答读者的问题？

### 新增模块

#### Module 9: Reader Persona Check (目标读者识别) ⭐

**核心问题**: 这篇文章的目标读者是谁？

**Reader Persona 卡片**:
| 维度 | 问题 |
|------|------|
| **Who** | 他们是谁？ |
| **Pain** | 他们的痛点？ |
| **Search** | 他们会怎么搜索？ |
| **Language** | 他们用什么词汇？ |
| **Goal** | 他们想得到什么？ |

**检查项**:
- 标题匹配读者的搜索习惯吗？
- 术语是读者能理解的吗？
- 开篇直接回应痛点吗？
- 内容帮读者达成目标吗？

**自动修复**: ⚠️ 部分（术语替换）

#### Module 10: Internal Language Leak Check (内部语言泄露检测) ⛔ BLOCKING

**核心问题**: 有没有"写给编辑/写给AI"而不是"写给读者"的内容？

**检测类型**:
| 类型 | 示例 | 严重级别 |
|------|------|---------|
| 编辑注释 | "Based on v3", "改掉AI痕迹" | ⛔ BLOCKING |
| 内部术语 | "AEO", "Data Hook", "洗稿" | ⛔ BLOCKING |
| AI设计暴露 | "(easy for AI to cite)" | ⛔ BLOCKING |
| H2写作指导 | "(putting the problem into human terms)" | ⚠️ WARNING |

**自动修复**: ✅ 是（删除/替换）

### 新增配置文件

| 文件 | 用途 |
|------|------|
| `prompts/READER_PERSONA_TEMPLATE.yaml` | Reader Persona 卡片模板 + 审视清单 |
| `prompts/INTERNAL_LANGUAGE_PATTERNS.yaml` | 内部语言检测规则 + 自动修复策略 |

### 触发背景

基于 **YouTube CTR Guide** 文章审核发现的问题：

| 问题 | 原文 | 分析 |
|------|------|------|
| 编辑注释开篇 | "Based on v3, this version changed several AI-like writing methods..." | 读者不关心这是第几版，不关心有没有AI痕迹 |
| 内部术语标题 | "AEO quick answers" | 读者不知道AEO是什么 |
| 写作框架暴露 | "Opening data hook (Data Hook)" | "Data Hook"是写作框架术语 |
| H2写作指导 | "(putting the problem into human terms)" | 这是作者的写作目标，不是读者需要的信息 |
| 结尾编辑注释 | "This article is written as a 'reference expansion'..." | "reference expansion"是内部洗稿术语 |

### 教训总结

> **Human Review 不仅要检查技术指标，更要从目标读者视角审视——读者不需要知道"这是v3版本"、"AEO优化"、"洗稿模式"这些内部术语。**

---

## [1.0.0] - 2026-01-31

### 初始版本

- 8 个 Check Module
- 6 个可自动修复 + 2 个需要 Writer Feedback
- 最多 2 轮 Feedback Loop

| # | Module | 编辑问题 |
|---|--------|----------|
| 1 | Title CTR Check | 标题能让人点吗？ |
| 2 | Title-Reader Alignment | 读者会这样搜吗？ |
| 3 | Competitor Mention Scan | 在帮竞品打广告吗？ |
| 4 | Internal Link Audit | 有没有留住读者？ |
| 5 | H2 AEO Citable Check | AI 能引用章节吗？ |
| 6 | Promise-Delivery Check | 说到做到了吗？ |
| 7 | TL;DR Value Statement | 读者知道能得到什么吗？ |
| 8 | Brand Voice Check | 这是 alici.ai 的声音吗？ |
