	# 更新日志

> AI 内容工厂蓝图的版本历史

---

## [2.8.0] - 2026-01-25 - SmartLauncher v2.1 三轨制架构

### 新增功能

- **SmartLauncher v2.1**: 三轨制统一入口
  - **Track A 全自动模式**: URL → 1-2 问题 → 洗稿 80%+
  - **Track B 手动模式**: 5 步确认 + DataForSEO 强制展示
  - **Track C Seed 模式**: 选题漏斗 - 6 Phase 架构
- **Growth-Topic-Scout v2.2**: Seed Mode 选题漏斗
  - 6 Phase: Mission Config → 竞品意图 → 扩散 → 验证 → 裁剪 → Title Lock
  - Direction 对象输出 (locked_title + evidence_chain)
  - 成本优化: ~$2.59 → ~$0.47 (standard)
- **DataForSEO 升级**: 3 个 AEO/LLM 数据维度
  - AI Search Heat (ai_keyword_data)
  - LLM Citation Potential (llm_mentions)
  - AI Answer Coverage (llm_responses)
- **新增 Schema 文件**
  - MISSION_CONFIG_SCHEMA.json
  - DIRECTION_SCHEMA.json

---

## [2.75] - 2026-01-23 - SmartLauncher v2.0 测试通过

### 验证结果

- 双轨制流程测试: 14/14 验证点全部 PASS
- 手动路线 7/7 + 全自动路线 7/7

---

## [2.74] - 2026-01-23 - SmartLauncher v2.0 双轨制架构

### 新增功能

- **全自动路线**: 洗稿模式 + 素材自动抓取
- **手动路线**: 5 步确认 + DataForSEO 强制展示
- **新增文件**: AUTO_ROUTE.md, MANUAL_ROUTE.md
- **COMBOS.md 简化**: 9 种组合 → 4 种核心方向

---

## [2.73.2] - 2026-01-22 - SmartLauncher v1.2 架构统一

### 新增功能

- **Editor Gate 强制**: 所有 Writer 必须经过 Editor
- **Writer Feedback Loop**: BLOCKING 时自动反馈重写
- **case-roundup-writer v1.5**: 加入 Editor 流程
- **editor v2.9.2**: Module 10 Writer Feedback 机制

---

## [2.73.1] - 2026-01-22 - Editor v2.9.1 强制规则升级

### 新增功能

- Key Takeaways 强制前置 (⛔ BLOCKING)
- Data Hook 开篇强制 (⚠️ → 自动修复)
- 标题年份验证升级为 ⛔ BLOCKING
- Module 9 新增: CTA Enforcement

---

## [2.73] - 2026-01-22 - Editor v2.9 Invideo 竞品 Review

### 新增功能

- 24 种 AEO 开篇模式 + 选择矩阵
- 37 种标题公式验证
- L1-L20 产品植入层级检测
- 5 层引用权威金字塔评分
- 4 个新 YAML 配置文件

---

## [2.72] - 2026-01-22 - YouTube URL 路由修复

### 修复

- YouTube URL 单独输入自动路由到 fetch-transcript
- 支持: watch URL、短链接、嵌入链接

---

## [2.71] - 2026-01-22 - Markdown-to-Framer v1.3 修复

### 修复

- 图片格式修复 (无 figure, alt 在 src 前)
- 特殊字符处理 (em dash/smart quotes)
- cover 字段简化

---

## [2.7.0] - 2026-01-21

### 新增

- **Tool Showdown + Version Verification 系统**
  - **smart-root v2.2**: Phase 0 版本验证，检测 "vs/对比/对决" 意图时自动 WebSearch 验证工具版本
  - **blog-list-writer v2.2**: 新增 `tool_showdown` 内容类型，10 固定 Headings 高对比度结构
  - **TOOL_SHOWDOWN_TEMPLATE.md**: 工具对决文章结构规范模板
  - 核心解决：版本滞后问题 + 高对比度结构一致性

### 更新

- **CLAUDE.md**: 架构图更新至 v2.7，新增版本验证层说明
- **调用链**: 新增版本验证 → Writer 传递 verified_tools JSON

---

## [2.6.0] - 2026-01-20

### 新增

- **Visual Asset System (数据契约系统)**
  - **writer v1.3**: 输出 asset_plan.json + prompt_pack.md
  - **editor v2.6**: Asset Pack Mode (批量图片生成) + asset_manifest.json
  - 核心突破：Writer ↔ Editor 标准化数据契约

- **质量保障升级**
  - **competitive-validator v1.0**: Top 5 竞品对比 + 快速 AEO 评分 + PASS/FAIL 判定
  - **trending-monitor v1.0**: QDF 信号检测 + 热点优先级 + 内容日历建议
  - **output-path-builder capability v1.0**: 统一路径生成 + 冲突检测

- **SmartRoot 交互式选题确认**
  - **smart-root v2.0 → v2.1**: 4 步交互问卷 + DataForSEO 集成 + 竞品验证层集成
  - **smart-router v2.0**: 写作意图自动路由到 smart-root

- **Insight-Driven Blog Writer**
  - **case-roundup-writer v1.3**: Material Gate + 多维度拓展 + Prompts to Try + 标题确认

### 更新

- **growth-topic-scout v1.2**: trending-monitor 集成 + Trend Relevance 评分
- **aeo-analyzer v2.4**: Module 5 Content Freshness Signals (20 bonus points)
- **CLAUDE.md**: 架构图更新至 v2.5，新增选题确认层

---

## [2.3.0] - 2026-01-20

### 新增

- **智能路由 + 批量处理**
  - **smart-router v1.0**: 自然语言意图识别 + URL 类型检测 + 路径分发
  - **batch-processor v1.0**: 队列管理 + 进度追踪 + 错误恢复 + 汇总报告
  - `/batch-workflow` 命令创建

### 更新

- **01-ARCHITECTURE.md**: 更新至 v2.3，新增路由层和批量处理设计
- **CLAUDE.md**: 架构图更新至 v2.3

---

## [2.2.0] - 2026-01-18

### 新增

- **版本继承机制** - 保护 E-E-A-T 投资
  - **blog-tutorial-writer v2.2**: 版本继承，检测并保留 improved 版本的 E-E-A-T 内容
  - **editor v2.4**: Module 7 版本对比检查，BLOCKING 如果关键内容丢失
  - **auto-improver v2.1**: E-E-A-T 保护标记系统
  - **blueprint/10-VERSION-INHERITANCE.md**: 版本继承规则完整文档
  - 核心原则：改进不可丢失 (Improvements Never Lost)

- **Higgsfield 内容策略洞察**
  - **growth-topic-scout v1.2**: 3 类型标题建议 (Listicle/How-to/Insights) + CTR 预测
  - **blog-list-writer v2.0**: 强制年份 + 数字标题 + 5 维度评测方法论
  - **blog-tutorial-writer v2.1**: How-to 标题公式 + 7 要素 Prompt 结构章节
  - **blueprint/00-CONTENT-PHILOSOPHY.md**: 内容策略哲学文档

### 更新

- **START_HERE.md**: 简化为入口导航，指向最新文档结构（2026-01-18）
- **CLAUDE.md**: 完整更新版本继承规则章节

---

## [2.1.0] - 2026-01-17

### 新增

- **E-E-A-T 内容深度检查**
  - **editor v2.3**: Module 6 强制执行（案例研究、测试方法论、作者信息）
  - **aeo-analyzer v2.3**: M3 重组为结构信号(12分) + 内容深度(13分)
  - 修复 Editor 模块跳过问题

---

## [2.0.0] - 2026-01-16

### 新增

- **Writer v2.0 重大升级**
  - **blog-tutorial-writer v2.0**: AIDA 开篇框架 + Citable Block 系统
  - 强化 E-E-A-T 信号（7 个外部引用 + 完整作者信息）
  - 验证通过：首次 AEO 评分 73 → 82 (+9 分)
  - Changelog: `.claude/skills/blog/blog-tutorial-writer/CHANGELOG.md`

### 项目成果

- ✅ **Sora 2 Prompt Guide** 项目完成
  - 报告位置: `/Users/H/reports/2026-01-17-sora-prompt-guide/`
  - 验证 blog-tutorial-writer v2.0 方法论有效性
  - 首次 AEO 评分达到 82 分（无需 auto-improver 迭代）

---

## [1.2.0] - 2025-01-12

### 新增

- **06-COLLABORATION.md** - 协作模式文档
  - 从人驱动到 Agent 驱动的范式转变
  - Git 在新范式中的角色
  - Boris 一人多 Agent 模式的启示
  - 回应 Sam 关于 Git 协作的讨论

---

## [1.1.0] - 2025-01-11

### 新增

- **00-PHILOSOPHY.md** - 产品哲学文档
  - 三种 AI 协作模式对比（对话式 / Agent 平台 / Claude Code）
  - Claude Code 三个关键突破
  - "文件胜过应用"产品哲学
  - 新操作系统视角

---

## [1.0.0] - 2025-01-11

### 新增

- **蓝图文档体系**
  - README.md - 索引与总览
  - 01-ARCHITECTURE.md - 三层架构设计
  - 02-SKILLS.md - Skills 清单（17 个 Skills）
  - 03-AGENTS.md - Agents 清单（3 个 Agents）
  - 04-SOP.md - SOP 总览
  - 05-IMPLEMENTATION.md - 实施计划

- **目录结构**
  - `.claude/skills/_shared/` - 共用 Skills 目录
  - `.claude/skills/blog/` - Blog 专用 Skills 目录
  - `.claude/skills/hitclone/` - HitClone 专用 Skills 目录
  - `.claude/skills/video-super-agent/` - VSA 专用 Skills 目录
  - `.claude/agents/` - Agents 目录
  - `sop/blog-production/` - Blog SOP 目录
  - `sop/hitclone-production/` - HitClone SOP 目录
  - `sop/vsa-production/` - VSA SOP 目录
  - `runbooks/` - 运维手册目录

- **Skills 迁移**
  - aeo-analyzer 从 `skills/aeo-analyzer/` 迁移到 `skills/_shared/aeo-analyzer/`

### 确认

- 通知渠道：Slack
- 人工节点：选题确认 + 发布审核（共 2 个）
- Framer 发布：短期半自动，长期 API 对接

---

## 版本说明

### 版本号规则

- **主版本号**: 架构重大变更
- **次版本号**: 新增 Skills/Agents/SOP
- **修订号**: 文档修正、小幅调整

### 状态说明

- ✅ 已完成
- 🚧 进行中
- 📋 计划中

---

## 路线图

### Q1 2025

- [ ] Phase 1: 基础设施（2 周）
- [ ] Phase 2: Blog 生产线（3 周）

### Q2 2025

- [ ] Phase 3: 上游雷达（2 周）
- [ ] Phase 4: 监测闭环（2 周）
- [ ] Phase 5: 扩展到 HitClone 和 VSA（4 周）

---

## 贡献者

- Hans - 架构设计、文档编写

---

## 反馈

如有问题或建议，请通过以下渠道反馈：

- Slack: #ai-factory
- 直接编辑本文档并提交
