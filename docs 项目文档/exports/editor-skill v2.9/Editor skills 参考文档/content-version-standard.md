# 版本管理标准

> **版本**: v1.0
> **基于**: Editor Skill v2.9 Module 7 (Version Inheritance Check)
> **最后更新**: 2026-01-23
> **文档用途**: 防止内容迭代时丢失 E-E-A-T 投资

---

## 核心原则

> **改进不可丢失 (Improvements Never Lost)**

当重写或更新文章时，之前版本中积累的 E-E-A-T 内容（案例研究、测试数据、作者信息、引用来源等）必须被保留。这些内容代表了真实的编辑投资，一旦丢失将无法恢复。

---

## 版本命名规范

### 文件命名约定

| 版本类型 | 文件名 | 说明 |
|----------|--------|------|
| 初稿 | `01-article-draft.md` | Writer 直接输出 |
| 编辑版 | `01-article-edited.md` | Editor 处理后输出 |
| 改进版 | `01-article-improved-v1.md` | Auto-improver 输出 ⭐ **后续基准** |
| 重写版 | `01-article-v2.md` | Writer 重写（必须继承 improved） |
| 二次改进 | `01-article-improved-v2.md` | 第二轮 Auto-improver |

### 版本号规则

```
v[主版本].[次版本]

主版本 (Major): 结构性重写
次版本 (Minor): 内容改进/优化
```

**示例**:
- `v1.0` → 初始发布版本
- `v1.1` → 第一次改进（增加案例/引用）
- `v2.0` → 结构性重写（新框架/新方法论）
- `v2.1` → v2.0 基础上的改进

---

## 版本继承检查规则

### 触发条件

Editor Module 7 在以下情况下自动激活：

1. 目录中存在 `01-article-improved-*.md` 文件
2. 文章包含 `<!-- E-E-A-T_PROTECTED_CONTENT_START -->` 标记

### 受保护内容清单

| 内容类型 | 检测模式 | 处理方式 |
|----------|----------|----------|
| **Author Information** | YAML `author.name` ≠ "alici.ai Content Team" | ✅ 完全保留 |
| **Case Studies** | 章节含 "Case Study", "Real-World Example" | ✅ 完全保留 |
| **Testing Data** | 任何 "n=X" 引用、测试方法论 | ✅ 保留上下文 |
| **External Sources** | "Sources" 章节中的链接或行内引用 | ✅ 保留 + 计数 |
| **Disclosure** | "alici.ai is our product" 等声明 | ✅ 完全保留 |
| **FAQ Section** | H2 "FAQ" 或 "Frequently Asked Questions" | ✅ 至少保留问题 |
| **Citable Blocks** | `<!-- CITABLE_BLOCK -->` 标记 | ✅ 保留所有块 |

### 验证检查

输出前自动验证：

| 检查项 | 阈值 | 失败后果 |
|--------|------|----------|
| **Word Count** | 当前 vs 前版本 -20% max | ⛔ BLOCKING |
| **Author Name** | 完全匹配 | ⛔ BLOCKING |
| **Case Studies** | 数量 ≥ 前版本 | ⚠️ WARNING |
| **Testing Data (n=X)** | 全部保留 | ⚠️ WARNING |
| **External Sources** | 链接数 ≥ 前版本 | ⚠️ WARNING |
| **FAQ Count** | 问题数 ≥ 前版本 | ⚠️ WARNING |
| **Citable Blocks** | 块数 ≥ 前版本 | ⚠️ WARNING |

---

## BLOCKING vs WARNING 处理流程

### ⛔ BLOCKING 情况

**触发条件**:
- 作者从命名个人改为团队
- 字数下降超过 20%

**处理流程**:
1. Editor **停止输出** `01-article-edited.md`
2. 仅生成 `04-editor-report.md` 并标记 BLOCKING
3. 报告中详细说明丢失内容
4. 需要人工审核和决策

**报告示例**:
```markdown
## Module 7: Version Inheritance Check

**Validation Result**: ⛔ BLOCKING

### BLOCKING Issues

1. **Author Changed**
   - Previous: Hans Chen (CEO, tested 10,000+ prompts)
   - Current: alici.ai Content Team
   - Action Required: Restore original author information

2. **Word Count Drop**
   - Previous: 5,500 words
   - Current: 4,100 words (-25.5%)
   - Action Required: Review for content loss
```

### ⚠️ WARNING 情况

**触发条件**:
- 案例研究数量减少
- 测试数据引用减少
- 外部来源减少
- FAQ 问题减少
- Citable Block 减少

**处理流程**:
1. Editor **正常输出** `01-article-edited.md`
2. 在 `04-editor-report.md` 中标记 WARNING
3. 列出具体减少的内容
4. 建议检查是否为有意删除

---

## CHANGELOG.md 模板

每个文章目录应包含 `CHANGELOG.md` 记录版本演化：

```markdown
# Changelog: [Article Title]

## [v2.1] - 2026-01-22

### Changed
- Updated pricing data for Kling 2.6 (verified as of 2026-01-22)
- Improved Motion Control section with new test results

### Added
- New case study: Dance video generation (n=50)
- FAQ Q6-Q8 based on user feedback

### Fixed
- Corrected Runway Gen-3 generation time (was 90s, now 120s)

## [v2.0] - 2026-01-20

### Changed
- Complete restructure using How-to formula
- Integrated 7-element prompt framework

### Preserved from v1.1
- Author: Hans Chen
- 2 original case studies
- Testing methodology (n=200)
- 4 external sources
- Disclosure statement

## [v1.1] - 2026-01-18

### Added
- Case Study 1: Product Video Comparison
- Case Study 2: Prompt Length Testing
- Author bio with credentials
- 4 external source citations

## [v1.0] - 2026-01-15

### Initial Release
- First draft from topic brief
- Basic structure and content
```

---

## E-E-A-T 保护标记

Auto-improver 输出时自动添加的保护标记：

```markdown
<!-- E-E-A-T_PROTECTED_CONTENT_START -->

## About the Author

**Hans Chen** is the CEO of alici.ai and has tested over 10,000 AI video prompts
across Kling, Runway, Sora, and Veo. His research on Motion Control optimization
has been featured in TechCrunch.

## Real-World Case Studies

### Case Study 1: Product Video Comparison
[详细案例内容...]

### Case Study 2: Prompt Length Testing
[详细案例内容...]

## Testing Methodology

All comparisons were conducted using identical prompts across models.
Sample size: n=200 videos. Test period: January 10-15, 2026.

## Sources

1. [OpenAI Sora Documentation](https://openai.com/sora)
2. [Kling 2.6 Release Notes](https://kling.ai/releases/2.6)
3. [Runway Gen-3 Turbo Overview](https://runwayml.com/gen3)
4. [Wyzowl Video Marketing Statistics 2026](https://wyzowl.com/stats)

## Disclosure

alici.ai is a product of our company. While we believe it offers competitive
features, we've included both strengths and limitations in our evaluation.
Pricing and features are accurate as of January 2026.

<!-- E-E-A-T_PROTECTED_CONTENT_END -->
```

**规则**:
- 这些标记之间的内容在后续版本中**必须保留**
- Writer/Editor 看到此标记时自动进入继承模式

---

## 版本链示例

### 正常演化路径

```
v1.0 draft (4,800 词)
    ↓ Editor + AEO Analyzer + Auto-improver
v1.1 improved (5,500 词)  ← E-E-A-T 投资点 ⭐
    │
    │ [包含:]
    │ - 命名作者: Hans Chen
    │ - 2 个案例研究
    │ - 测试数据: n=200
    │ - 4 个外部来源
    │ - 利益披露
    │
    ↓ Writer v2.x 重写 (检测到 improved, 继承 E-E-A-T)
v2.0 (5,400 词)  ← 框架更新 + E-E-A-T 完整保留 ✅
    ↓ Editor Module 7 验证
v2.0 edited ← PASS (所有内容保留) ✅
```

### 问题场景（已通过 Module 7 阻止）

```
v1.1 improved (5,500 词)
    │
    │ [包含 E-E-A-T 内容...]
    │
    ↓ Writer 从 topic brief 重写（忽略 improved）
v2.0 草稿 (4,100 词)  ← 问题版本 ❌
    │
    │ [丢失:]
    │ - 作者改为团队
    │ - 0 个案例研究
    │ - 0 个测试数据
    │ - 0 个外部来源
    │
    ↓ Editor Module 7 检测
⛔ BLOCKING - 禁止输出，需人工合并
```

---

## 可更新内容

以下内容可以在保留受保护内容的前提下更新：

| 可更新项 | 说明 |
|----------|------|
| ✅ 标题格式 | 使用最新公式（如 How-to 2026） |
| ✅ 开篇框架 | 应用 AIDA 或新的 AEO 模式 |
| ✅ 章节组织 | 重构 H2/H3 层级 |
| ✅ Prompt 框架 | 添加/更新方法论 |
| ✅ 示例代码 | 更新为更清晰的演示 |
| ✅ 时效性数据 | 更新价格、功能、版本号 |
| ❌ 作者信息 | 禁止从命名作者改为团队 |
| ❌ 原创案例 | 禁止删除，只能新增 |
| ❌ 测试数据 | 禁止删除，只能新增 |

---

## 报告输出格式

`04-editor-report.md` 中的 Module 7 章节：

```markdown
## Module 7: Version Inheritance Check

**Previous Version Detected**: `01-article-improved-v1.md`

**Validation Result**: ✅ PASS / ⚠️ WARNING / ⛔ BLOCKING

### Content Comparison

| Metric | Previous | Current | Change | Status |
|--------|----------|---------|--------|--------|
| Word Count | 5,500 | 5,300 | -3.6% | ✅ PASS |
| Author Name | Hans Chen | Hans Chen | No change | ✅ PASS |
| Case Studies | 2 | 2 | No change | ✅ PASS |
| Testing Data (n=X) | 3 refs | 3 refs | No change | ✅ PASS |
| External Sources | 4 | 5 | +1 | ✅ PASS |
| FAQ Questions | 5 | 5 | No change | ✅ PASS |
| Citable Blocks | 5 | 6 | +1 | ✅ PASS |

### Issues Found

**BLOCKING Issues**: None

**WARNING Issues**: None

### Recommendations

- Consider adding more recent statistics for 2026
- FAQ section could be expanded based on user queries

---
```

---

## 最佳实践

### 对于 Writer

1. **重写前检查**: 始终查看目录中是否存在 `improved` 版本
2. **继承优先**: 如果存在 improved 版本，从它开始而非 topic brief
3. **保留标记**: 不要删除 `E-E-A-T_PROTECTED_CONTENT` 标记之间的内容
4. **新增而非替换**: 添加新案例/来源，不要删除旧的

### 对于 Editor

1. **依赖 Module 7**: 让自动检查发现问题
2. **BLOCKING 即停止**: 看到 BLOCKING 不要尝试继续
3. **记录变化**: 确保 CHANGELOG.md 更新

### 对于团队

1. **版本即资产**: improved 版本是宝贵资产，不是可丢弃的草稿
2. **合并而非覆盖**: 新想法应合并到现有内容，而非完全替换
3. **回溯检查**: 发布前检查是否有 improved 版本被忽略

---

## 相关文档

- [Editor v2.9 能力总览](./editor-v2.9-capabilities.md)
- [E-E-A-T 强化指南](./eeat-optimization-guide.md)
- [内部链接指南](./internal-linking-guide.md)
- 完整 CLAUDE.md: `/Users/H/Documents/AliciBlog/CLAUDE.md` (版本继承规则章节)

---

*文档维护: Editor Skill v2.9.3 | 最后同步: 2026-01-23*
