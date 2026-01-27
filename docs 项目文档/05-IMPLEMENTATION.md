# 05 - 实施计划

> 实施优先级、关键指标与风险评估

---

## 实施阶段

```
Phase 1 (2周)     Phase 2 (3周)     Phase 3 (2周)     Phase 4 (2周)     Phase 5 (4周)
基础设施    →    Blog 生产线   →    上游雷达    →    监测闭环    →    扩展其他线
```

---

## Phase 1：基础设施（2 周）

**目标**: 建立 Skills 框架，封装现有能力

| 任务 | 优先级 | 产出 | 状态 |
|------|--------|------|------|
| 设计 Skills 目录结构 | P0 | skills/ 目录 | ✅ 完成 |
| 迁移 AEO Analyzer 到 _shared/ | P0 | 统一的共用 Skills 入口 | ✅ 完成 |
| 创建 SOP 目录结构 | P1 | sop/ 目录 | ✅ 完成 |
| 封装 image-generator Skill | P1 | 图片生成能力标准化 | 待开始 |
| 创建 content-formatter Skill | P1 | JSON 输出标准化 | 待开始 |

---

## Phase 2：Blog 生产线（3 周）

**目标**: 让 Blog 生产线实现 50% 自动化

| 任务 | 优先级 | 产出 |
|------|--------|------|
| 创建 blog-tutorial-writer Skill | P0 | Tutorial 自动生成 |
| 创建 blog-list-writer Skill | P0 | List 自动生成 |
| 创建 blog-news-writer Skill | P0 | News 自动生成 |
| 创建 chinese-previewer Skill | P1 | 中文预览自动生成 |
| 编写 Blog 生产线 SOP | P1 | 完整流程文档 |
| 创建 qa-agent | P1 | 批量质量检查 |

---

## Phase 3：上游雷达（2 周）

**目标**: 实现内容发现自动化

| 任务 | 优先级 | 产出 |
|------|--------|------|
| 创建 seo-keyword-researcher Skill | P0 | 关键词研究能力 |
| 创建 scout-agent | P1 | 自动内容侦察 |
| 定义数据源清单 | P1 | SOURCES.md |
| 创建筛选规则 | P1 | Filter Skill |

---

## Phase 4：监测闭环（2 周）

**目标**: 实现数据反馈自动化

| 任务 | 优先级 | 产出 |
|------|--------|------|
| 创建 analytics-reporter Skill | P0 | 数据分析能力 |
| 创建 monitor-agent | P1 | 自动数据监测 |
| 创建反馈规则 | P1 | Feedback Skill |

---

## Phase 5：扩展到其他生产线（4 周）

**目标**: 复制模式到 HitClone 和 VSA

| 任务 | 优先级 | 产出 |
|------|--------|------|
| 创建 HitClone Skills | P1 | youtube-analyzer, page-generator |
| 创建 VSA Skills | P2 | viral-analyzer, use-case-writer |
| 编写各生产线 SOP | P1 | 完整流程文档 |

---

## 关键成功指标

### 效率指标

| 指标 | 当前 | Phase 2 目标 | Phase 5 目标 |
|------|------|-------------|-------------|
| 单篇生产时间 | 2-4 小时 | 1-1.5 小时 | 30 分钟 |
| 人工介入次数 | 7+ 次/篇 | 2 次/篇 | 2 次/篇 |
| 自动化比例 | 0% | 50% | 70% |
| 月产量 | 5 篇 | 15 篇 | 30 篇 |

### 质量指标

| 指标 | 目标 |
|------|------|
| AEO 评分 | > 75 分 |
| 发布成功率 | > 95% |
| 人工审核通过率 | > 90% |

### 运营指标

| 指标 | 目标 |
|------|------|
| Skill 复用率 | > 60%（共用 Skills 被多条线调用） |
| Agent 稳定性 | > 99%（无异常中断） |
| 上报响应时间 | < 4 小时 |

---

## 风险评估

| 风险 | 等级 | 缓解措施 |
|------|------|----------|
| Skills 定义不清导致输出不稳定 | 高 | 每个 Skill 必须有明确的输入/输出 Schema |
| Agent 运行成本过高 | 中 | 设置 token 预算上限，优先使用 Skill |
| 人工节点成为瓶颈 | 中 | 批量处理，设置 SLA |
| Framer API 集成复杂 | 中 | 短期保持半自动，长期推进 API 对接 |

---

## 已确认事项

1. **通知渠道** ✅
   - 使用 Slack 作为主要协作渠道

2. **上游数据源优先级**
   - 暂无强偏好，按需决定
   - 建议：先聚焦生产环节自动化，上游侦察后续迭代

3. **Framer 发布方式**
   - 短期保持半自动（手动 CMS）
   - 长期规划 API 对接

---

## 立即可做（本周）

- [x] 创建目录结构（skills/, sop/, agents/）
- [x] 迁移 aeo-analyzer 到 _shared/
- [x] 创建蓝图文档
- [ ] 封装 image-generator（high-level 定义）
- [ ] 封装 content-formatter（high-level 定义）

---

**上一篇**: [04-SOP.md](./04-SOP.md) - SOP 标准操作规程总览
