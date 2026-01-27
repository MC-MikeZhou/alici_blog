# 版本继承规范 (Version Inheritance Specification)

> **核心原则**: 改进不可丢失 (Improvements Never Lost)

**版本**: v1.0
**创建日期**: 2026-01-18
**适用范围**: AliciBlog Skills 系统全流程

---

## 问题诊断

### 案例：Sora 2 Prompt Guide 版本演进断裂

```
v1.0 draft (4,800 词)
    ↓ Editor v2.3 + auto-improver（3h45m 工作量）
v1.1 improved (5,500 词)  ← 包含完整 E-E-A-T 投资
    ↓ blog-tutorial-writer v2.1 重写（从 topic brief 开始，忽略 v1.1）
v2.0 (4,100 词)  ← 丢失全部 E-E-A-T 内容
```

**根因**: blog-tutorial-writer v2.1 没有"版本继承"机制，重写时从 topic brief 开始，完全忽略了 v1.1 的改进成果。

**损失清单**:
| 内容 | v1.1 文件位置 | 状态 |
|------|--------------|------|
| Hans Chen 作者信息 | 第 9-13 行 YAML | ❌ 丢失 |
| Case Study 1: 产品视频 | 第 161-203 行 | ❌ 丢失 |
| Case Study 2: Prompt 长度测试 | 第 319-343 行 | ❌ 丢失 |
| 测试方法论 (n=200) | 第 36-37 行 | ❌ 丢失 |
| Sources 外部引用 (4个) | 第 616-619 行 | ❌ 丢失 |
| Disclosure 利益披露 | 第 442-443 行 | ❌ 丢失 |
| FAQ (5个问题) | 第 563-584 行 | ❌ 丢失 |

**编辑投资损失**: 约 3 小时 45 分钟工作量 + 1,400 词 E-E-A-T 内容

---

## 版本链定义

### 标准版本流程

```
draft → improved → v2 → v2.5 → ...
         ↑           ↑
      E-E-A-T    结构优化
       投资       （必须继承 improved）
```

### 版本类型定义

| 版本类型 | 文件名格式 | 产生者 | 特征 |
|----------|-----------|--------|------|
| **Draft** | `01-article-draft.md` | writer skill | 初稿，未优化 |
| **Edited** | `01-article-edited.md` | editor skill | 图片 + 开篇 + 格式优化 |
| **Improved** | `01-article-improved-v{N}.md` | auto-improver | E-E-A-T 投资版本 ⭐ |
| **Rewritten** | `01-article-v{N}.md` | writer skill (重写) | 结构升级版本 |
| **Merged** | `01-article-v{N}.5.md` | 手动合并 | 框架 + E-E-A-T 合并版 |

**关键版本**: `01-article-improved-v*.md` - **必须被后续所有重写继承**

---

## 强制规则

### 规则 1: 重写必须基于最新 improved 版本

**触发条件**: 当存在 `01-article-improved-*.md` 文件时

**强制要求**:
- ✅ writer skill **必须**检测 improved 文件
- ✅ writer skill **必须**继承 E-E-A-T 章节
- ⛔ 禁止仅从 topic brief 重写

**违规后果**:
- editor v2.4 Module 7 将 BLOCKING
- 字数减少 >20% 触发告警
- 人工审核标记

### 规则 2: E-E-A-T 内容标记为 PROTECTED

**保护标记格式**:
```markdown
<!-- E-E-A-T_PROTECTED_CONTENT_START -->

[所有 E-E-A-T 内容]

<!-- E-E-A-T_PROTECTED_CONTENT_END -->
```

**谁添加标记**: auto-improver v2.1 (Path B 输出时)

**谁检测标记**:
- blog-tutorial-writer v2.2
- editor v2.4 Module 7

**保护内容列表**:
| 内容类型 | 必须保留 |
|---------|---------|
| Author Information | ✅ |
| Case Studies | ✅ |
| Testing Methodology (n=X) | ✅ |
| External Sources | ✅ |
| Disclosure Statements | ✅ |
| FAQ Section | ✅ (questions minimum) |
| Citable Blocks | ✅ |

### 规则 3: 字数减少 >20% 需人工审批

**检测点**: editor v2.4 Module 7

**阈值**:
- 字数减少 ≤ 20%: WARNING（标记但允许）
- 字数减少 > 20%: BLOCKING（停止输出，人工审核）

**例外情况**:
- 用户显式要求缩短文章
- 删除冗余内容有明确理由

### 规则 4: Editor 必须执行版本对比检查

**检查内容** (editor v2.4 Module 7):
- [ ] 检测是否存在 `01-article-improved-*.md`
- [ ] 提取前版本指标（字数、作者、案例数、来源数等）
- [ ] 对比当前版本指标
- [ ] 验证保护内容是否完整
- [ ] BLOCKING 如果关键内容丢失

**输出**:
- Module 7 status: PASS / WARNING / BLOCKING
- 对比表格（prev vs current）
- 问题清单

---

## 文件命名规范

### 标准命名格式

| 版本类型 | 文件名 | 说明 |
|----------|--------|------|
| 初稿 | `01-article-draft.md` | Writer 直接输出 |
| 编辑版 | `01-article-edited.md` | Editor 输出 |
| 改进版 | `01-article-improved-v1.md` | auto-improver 首次输出 |
| 改进版迭代 | `01-article-improved-v2.md` | auto-improver 第二轮输出 |
| 重写版 | `01-article-v2.md` | Writer 重写（必须继承 improved） |
| 手动合并版 | `01-article-v2.5.md` | 手动合并框架 + E-E-A-T |

### 版本号规则

**整数版本** (v1, v2, v3):
- 结构性重写
- 来自 writer skill
- **必须继承最新 improved 版本**

**小数版本** (v1.5, v2.5):
- 手动合并版本
- 通常合并框架 + E-E-A-T
- 临时解决方案（理想情况下不应需要）

**improved 版本** (improved-v1, improved-v2):
- auto-improver 输出
- 基于评分报告的迭代改进
- **后续重写的基准版本**

---

## Skills 系统集成

### blog-tutorial-writer v2.2

**新增参数**:
```markdown
## Input (Updated v2.2)

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| topic_brief | JSON | Yes | 主题 Brief |
| previous_version | File path | Optional | 前版本路径（自动检测 improved-*） |
```

**版本继承逻辑**:
```python
# Pseudocode
if exists("01-article-improved-*.md"):
    previous = read_most_recent("01-article-improved-*.md")
    protected_content = extract_eeai_content(previous)

    # 强制保留
    new_article.author = previous.author  # EXACT match
    new_article.case_studies = previous.case_studies  # ALL
    new_article.testing_data = previous.testing_data  # ALL "n=X"
    new_article.sources = previous.sources + new_sources  # MERGE
    new_article.disclosure = previous.disclosure  # EXACT
    new_article.faq = previous.faq  # QUESTIONS minimum

    # 可更新
    new_article.title = apply_v2_1_formula()  # How-to format
    new_article.opening = apply_AIDA_framework()
    new_article.structure = apply_7_element_framework()
else:
    # 正常流程（无前版本）
    new_article = generate_from_brief(topic_brief)
```

**验证检查点**:
```python
# Before output
if previous_version_exists:
    assert new_article.word_count >= previous.word_count * 0.8
    assert new_article.author.name == previous.author.name
    assert len(new_article.case_studies) >= len(previous.case_studies)
    assert count("n=", new_article) >= count("n=", previous)
    assert len(new_article.sources) >= len(previous.sources)
```

### editor v2.4 - Module 7

**执行时机**: 所有文章编辑后

**检测逻辑**:
```python
# Phase 0: Version Detection
previous_files = glob("01-article-improved-*.md")
if previous_files:
    run_module_7(current_article, previous_version)
else:
    skip_module_7("no previous version")
```

**验证项**:
| 检查项 | 阈值 | 失败等级 |
|--------|------|---------|
| Word Count | -20% max | BLOCKING |
| Author Name | Exact match | BLOCKING |
| Case Study Count | >= previous | WARNING |
| Testing Refs (n=X) | All retained | WARNING |
| External Sources | >= previous | WARNING |
| FAQ Count | >= previous | WARNING |

**输出状态**:
- ✅ PASS: 所有检查通过
- ⚠️ WARNING: 部分内容减少但在容忍范围
- ⛔ BLOCKING: 关键内容丢失，禁止输出

### auto-improver v2.1 - E-E-A-T Protection

**Path B 输出时添加保护标记**:

```markdown
<!-- E-E-A-T_PROTECTED_CONTENT_START -->

## About the Author
[Author 信息复述 frontmatter]

## Real-World Case Studies
[Path B 添加的所有案例]

## Testing Methodology
[测试方法和数据]

## Sources
[外部来源列表]

## Disclosure
[利益披露声明]

<!-- E-E-A-T_PROTECTED_CONTENT_END -->
```

**位置**: 文章末尾（Conclusion/FAQ 之后）

**检测**: writer v2.2 和 editor v2.4 自动检测并保留标记内容

---

## 实施示例

### 示例 1: 正常版本继承流程

```
Step 1: Writer v2.1 生成初稿
输出: 01-article-draft.md (4,800 词)

Step 2: Editor v2.3 优化
输出: 01-article-edited.md (4,850 词)

Step 3: AEO Analyzer 评分
输出: 03-aeo-score.md (73/100)

Step 4: Auto-improver Path A (AEO 结构优化)
输出: 01-article-improved-v1.md (5,100 词, 79/100)

Step 5: Auto-improver Path B (E-E-A-T 内容优化)
输入: 01-article-improved-v1.md + editor report
输出: 01-article-improved-v2.md (5,500 词, 85/100)
       + E-E-A-T 保护标记 ⭐

Step 6: Writer v2.2 重写（Higgsfield 洞察集成）
检测: 01-article-improved-v2.md exists
继承: Author + 2 Case Studies + Testing + Sources + Disclosure
更新: Title (How-to formula) + 7-element framework
输出: 01-article-v3.md (5,400 词)

Step 7: Editor v2.4 验证
Module 7: 对比 v3 vs improved-v2
状态: PASS ✅
  - Word count: 5,400 (prev 5,500, -1.8%) ✅
  - Author: Hans Chen (match) ✅
  - Case studies: 2 (prev 2) ✅
  - Testing: n=200 retained ✅
  - Sources: 5 (prev 4, +1) ✅
输出: 01-article-edited-v3.md

结果: ✅ 版本继承成功，E-E-A-T 内容完整保留
```

### 示例 2: BLOCKING 场景

```
Step 1-5: (同上)
输出: 01-article-improved-v2.md (5,500 词, 85/100)

Step 6: Writer v2.2 重写（错误：忽略 improved 版本）
错误: 仅从 topic brief 生成，未检测 improved-v2
输出: 01-article-v3.md (4,100 词)
  - Author: "alici.ai Content Team" ❌
  - Case studies: 0 ❌
  - Testing: 0 ❌
  - Sources: 0 ❌

Step 7: Editor v2.4 Module 7 检测
Module 7: 对比 v3 vs improved-v2
状态: BLOCKING ⛔
  Issues:
  1. Word count: 4,100 (prev 5,500, -25.5%) ⛔ BLOCKING
  2. Author: Team (prev Hans Chen) ⛔ BLOCKING
  3. Case studies: 0 (prev 2) ⚠️ WARNING
  4. Testing: 0 refs (prev "n=200") ⚠️ WARNING
  5. Sources: 0 (prev 4) ⚠️ WARNING

Editor 动作: ⛔ 停止输出 01-article-edited-v3.md
           生成 04-editor-report.md with BLOCKING status
           标记 MANUAL_REVIEW required

人工介入: 手动合并 v3 (框架) + improved-v2 (E-E-A-T)
输出: 01-article-v3.5.md (5,500 词, 100/100)

教训: Writer v2.2 版本继承机制必须强制执行
```

---

## 验证清单

### 对于 Writer (v2.2)

**执行前检查**:
- [ ] 检测是否存在 `01-article-improved-*.md`
- [ ] 如存在，读取并提取 E-E-A-T 内容
- [ ] 如存在，提取保护标记内容

**输出前验证**:
- [ ] Author YAML 与前版本完全一致
- [ ] 所有案例研究已包含
- [ ] 所有 "n=X" 测试引用已保留
- [ ] 外部来源数量 >= 前版本
- [ ] Disclosure 声明已保留
- [ ] FAQ 问题数量 >= 前版本
- [ ] 字数减少 ≤ 20%

### 对于 Editor (v2.4 Module 7)

**执行检查**:
- [ ] 检测 previous_version
- [ ] 提取前版本指标
- [ ] 提取当前版本指标
- [ ] 运行所有 7 项对比检查
- [ ] 生成对比表格
- [ ] 确定状态 (PASS/WARNING/BLOCKING)

**BLOCKING 条件**:
- [ ] 字数减少 > 20%
- [ ] Author 名称变更
- (任一条件满足即 BLOCKING)

**输出决策**:
- [ ] PASS → 正常输出 edited 文件
- [ ] WARNING → 输出 + flag warnings
- [ ] BLOCKING → 仅输出 report，禁止 edited 文件

### 对于 Auto-improver (v2.1 Path B)

**输出要求**:
- [ ] 识别所有添加的 E-E-A-T 内容
- [ ] 创建 "About the Author" 章节（复述 frontmatter）
- [ ] 将所有 E-E-A-T 内容移至文章末尾
- [ ] 添加 `<!-- E-E-A-T_PROTECTED_CONTENT_START/END -->` 标记
- [ ] 确保标记内容完整且格式正确

---

## 故障排除

### 问题 1: Writer 未检测到 improved 版本

**症状**: 重写文章丢失 E-E-A-T 内容

**诊断**:
```bash
# 检查是否存在 improved 文件
ls /path/to/report/01-article-improved-*.md

# 检查 writer 日志
grep "previous_version" writer.log
```

**解决**:
1. 确认 improved 文件存在于同一目录
2. 确认 writer v2.2 版本继承逻辑已启用
3. 手动传递 `previous_version` 参数

### 问题 2: Editor Module 7 误报 BLOCKING

**症状**: Editor 标记 BLOCKING 但内容实际完整

**诊断**:
```bash
# 检查指标对比
grep "Module 7" 04-editor-report.md
```

**解决**:
1. 检查阈值设置是否合理（-20% word count）
2. 检查 Author 名称是否完全一致（大小写、标点）
3. 如误报，调整阈值或手动批准

### 问题 3: 保护标记格式错误

**症状**: Writer/editor 无法识别保护标记

**诊断**:
```bash
# 检查标记格式
grep "E-E-A-T_PROTECTED" 01-article-improved-*.md
```

**解决**:
1. 确认标记使用正确格式：
   - `<!-- E-E-A-T_PROTECTED_CONTENT_START -->`
   - `<!-- E-E-A-T_PROTECTED_CONTENT_END -->`
2. 确认标记成对出现
3. 确认标记之间有实际内容

### 问题 4: 版本链断裂

**症状**: 无法确定哪个版本是最新

**诊断**:
```bash
# 列出所有版本文件及时间戳
ls -lt /path/to/report/01-article-*.md
```

**解决**:
1. 使用文件修改时间确定最新版本
2. 读取 `00-implementation.md` 查看版本历史
3. 必要时手动标记最新版本

---

## 最佳实践

### 1. 始终从最新 improved 版本开始

**推荐**:
```
检查 improved 文件 → 从 improved 重写 → 保留 E-E-A-T
```

**避免**:
```
从 topic brief 重写 → 忽略 improved → 丢失 E-E-A-T ❌
```

### 2. 重写前运行 editor Module 7 预检

在 writer 输出后、发布前：
```bash
# 运行 editor 预检
/edit-article 01-article-v3.md

# 检查 Module 7 status
grep "Module 7" 04-editor-report.md
```

### 3. 保护标记放置于文章末尾

**Good**:
```markdown
## Conclusion
...

## FAQ
...

---

<!-- E-E-A-T_PROTECTED_CONTENT_START -->
[所有 E-E-A-T 内容]
<!-- E-E-A-T_PROTECTED_CONTENT_END -->
```

**Bad**:
```markdown
<!-- E-E-A-T_PROTECTED_CONTENT_START -->
[E-E-A-T 内容穿插在文章各处]
<!-- E-E-A-T_PROTECTED_CONTENT_END -->
```

### 4. 定期审计版本链完整性

每周或每月检查：
```bash
# 检查是否有孤立的 draft 文件（未改进）
find . -name "01-article-draft.md" -newer "01-article-improved-*.md"

# 检查是否有 v2+ 文件但无 improved 基准
find . -name "01-article-v[2-9].md" ! -path "*/01-article-improved-*.md"
```

---

## 成功指标

### 技术指标

| 指标 | 目标 | 测量方法 |
|------|------|---------|
| **版本继承率** | 100% | (重写时检测到 improved) / (存在 improved 的重写) |
| **E-E-A-T 保留率** | 100% | (保留的 E-E-A-T 元素) / (前版本 E-E-A-T 元素) |
| **BLOCKING 误报率** | < 5% | (误报 BLOCKING) / (总 BLOCKING) |
| **字数损失率** | < 10% | avg((prev - curr) / prev) for all rewrites |

### 业务指标

| 指标 | 目标 | 影响 |
|------|------|------|
| **编辑返工时间** | -80% | 减少手动合并需求 |
| **AEO 评分稳定性** | ±5 分 | 重写不降低评分 |
| **E-E-A-T 投资 ROI** | 持久 | 投资的内容不会丢失 |

---

## 未来改进

### v1.1 规划

1. **自动版本链可视化**
   - 生成版本演进图
   - 显示每个版本的关键指标
   - 高亮断裂点

2. **版本 diff 工具**
   - 自动对比任意两个版本
   - 高亮 E-E-A-T 内容变化
   - 生成变更摘要

3. **智能合并建议**
   - 检测 improved + rewrite 需要合并
   - 自动建议合并策略
   - 生成合并后预览

### v2.0 规划

1. **版本继承 CI/CD**
   - pre-commit hook 检查版本继承
   - 自动运行 Module 7 验证
   - BLOCKING 时禁止 commit

2. **E-E-A-T 内容库**
   - 集中管理所有 case studies
   - 可跨文章复用案例
   - 版本化案例管理

---

**Document Version**: v1.0
**Last Updated**: 2026-01-18
**Author**: AliciBlog Skills Team
**Related Documents**:
- `/blueprint/02-SKILLS.md` - Skills 系统概览
- `/blueprint/07-BEST-PRACTICES.md` - 最佳实践
- `/skills/writers/blog-tutorial-writer/SKILL.md` - Writer v2.2 规范
- `/skills/core/editor/SKILL.md` - Editor v2.4 规范
- `/skills/core/auto-improver/SKILL.md` - Auto-improver v2.1 规范
