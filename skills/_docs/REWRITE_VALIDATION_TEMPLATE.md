# Rewrite Validation Template v1.0

> 洗稿模式验证检查清单，基于 InVideo 原则系统化集成
> **版本**: 1.0
> **创建日期**: 2026-01-26
> **适用范围**: 洗稿模式 (rewrite_mode) + Tool Showdown 文章

---

## 概述

本模板用于验证洗稿模式产出的文章是否符合 InVideo 原则标准。所有验证项分为两个级别：

| 级别 | 符号 | 含义 | 后果 |
|------|------|------|------|
| **BLOCKING** | ⛔ | 必须通过 | 阻止输出，必须修复 |
| **WARNING** | ⚠️ | 强烈建议 | 输出警告，建议修复 |

---

## 六大核心原则验证

### 原则 1: Key Takeaways 前置 ⛔ BLOCKING

**规则**: Key Takeaways 必须在 H1 后 500 字符内出现

**检查方法**:
```python
def check_key_takeaways_position(draft):
    h1_pos = find_h1_position(draft)
    kt_pos = find_pattern_position(draft, "## Key Takeaways")

    if kt_pos is None:
        return {"status": "BLOCKING", "message": "缺少 Key Takeaways 章节"}

    if kt_pos - h1_pos > 500:
        return {"status": "BLOCKING", "message": f"Key Takeaways 距离 H1 {kt_pos - h1_pos} 字符，超过 500 限制"}

    return {"status": "PASS"}
```

**验证清单**:
- [ ] 文章包含 `## Key Takeaways` 章节
- [ ] Key Takeaways 在标题后 500 字符内
- [ ] Key Takeaways 包含 3-7 个要点
- [ ] 每个要点包含工具名称 + 一句话优势

---

### 原则 2: Reframe 开篇 (P4) ⛔ BLOCKING

**规则**: Tool Showdown 文章必须使用 Pattern 4 (Reframe) 开篇模式

**Reframe 模式结构**:
```
常规认知 → 现实揭露 → 问题重定义 → 新视角承诺
```

**检查方法**:
```python
def check_reframe_opening(draft):
    opening = extract_first_300_words(draft)

    # 检查弱开篇
    weak_patterns = [
        "In this article",
        "Welcome to",
        "Let's explore",
        "Today we",
        "This guide will"
    ]
    for pattern in weak_patterns:
        if pattern.lower() in opening.lower():
            return {"status": "BLOCKING", "message": f"检测到弱开篇: {pattern}"}

    # 检查 Reframe 特征
    reframe_indicators = [
        "real question",
        "demos",
        "actually",
        "reveals the truth",
        "what they don't show"
    ]
    if not any(ind.lower() in opening.lower() for ind in reframe_indicators):
        return {"status": "BLOCKING", "message": "未检测到 Reframe 模式特征"}

    return {"status": "PASS"}
```

**验证清单**:
- [ ] 开篇不包含弱模式 (In this article, Welcome to...)
- [ ] 开篇包含 Reframe 特征 (real question, reveals...)
- [ ] 开篇重新定义读者的问题
- [ ] 开篇承诺回答重定义后的问题

---

### 原则 3: Source Attribution ⛔ BLOCKING

**规则**: 洗稿文章必须包含专门的 Source Attribution 章节

**必须章节结构**:
```markdown
## About This Comparison

**Testing Source**: [Source Name]
**Test Date**: [Date]
**Methodology**: [Brief description]

**Disclosure**: This analysis is based on [Source]'s testing methodology.
alici.ai did not independently verify all results.

[Link to Original Source](URL)
```

**检查方法**:
```python
def check_source_attribution(draft):
    # 检查章节存在
    if "## About This Comparison" not in draft and "## Source Attribution" not in draft:
        return {"status": "BLOCKING", "message": "缺少 Source Attribution 章节"}

    # 检查披露声明
    if "did not independently verify" not in draft:
        return {"status": "BLOCKING", "message": "缺少披露声明"}

    # 检查来源链接
    source_section = extract_source_attribution_section(draft)
    if not contains_url(source_section):
        return {"status": "WARNING", "message": "Source Attribution 缺少原始来源链接"}

    return {"status": "PASS"}
```

**验证清单**:
- [ ] 包含 `## About This Comparison` 章节
- [ ] 声明测试来源 (Testing Source)
- [ ] 声明测试日期 (Test Date)
- [ ] 包含披露声明 (Disclosure)
- [ ] 包含原始来源链接

---

### 原则 4: 无虚假声明 ⛔ BLOCKING

**规则**: 所有数据、评分、排名必须有来源引用

**禁止模式**:
| 禁止 | 正确 |
|------|------|
| "Sora 2: 4.5/5" | "Rated 4.5/5 on G2 (500+ reviews)" |
| "Kling ranks #2" | "According to [Source], Kling ranks #2" |
| "We tested..." | "According to [Source] testing..." |
| "Our analysis found..." | "[Source] found that..." |

**检查方法**:
```python
def check_claim_accuracy(draft):
    errors = []

    # 1. 检查无来源评分
    rating_pattern = r'(\d+\.?\d*)/5'
    for match in re.finditer(rating_pattern, draft):
        context = get_surrounding_text(draft, match.start(), 100)
        if not has_source_attribution(context):
            errors.append({
                "type": "BLOCKING",
                "message": f"无来源评分: {match.group()}"
            })

    # 2. 检查无来源排名
    ranking_pattern = r'ranks?\s*#?\d+'
    for match in re.finditer(ranking_pattern, draft, re.IGNORECASE):
        context = get_surrounding_text(draft, match.start(), 100)
        if not has_source_attribution(context):
            errors.append({
                "type": "BLOCKING",
                "message": f"无来源排名: {match.group()}"
            })

    # 3. 检查第一人称测试声明
    first_person_patterns = ["We tested", "Our analysis", "Our research", "We found"]
    for pattern in first_person_patterns:
        if pattern in draft:
            errors.append({
                "type": "WARNING",
                "message": f"第一人称测试声明: {pattern}"
            })

    return errors
```

**验证清单**:
- [ ] 所有 X/5 评分有来源 (G2, Capterra, etc.)
- [ ] 所有排名声明有来源
- [ ] 无 "We tested" 虚假声明
- [ ] 无 "Our analysis" 虚假声明
- [ ] 所有数据有年份标注

---

### 原则 5: L4 整合者定位 ⚠️ WARNING

**规则**: alici.ai 在竞品对决中定位为整合者，而非竞品

**必须包含**:
- "don't have to pick just one" 或等效表述
- "one platform" 或 "single platform"
- 整合者/聚合器定位

**禁止包含**:
- "alici.ai is the best"
- "better than [competitor]"
- "beats [competitor]"
- "#1 tool"

**检查方法**:
```python
def check_l4_positioning(draft):
    warnings = []

    # 检查整合者定位
    integrator_patterns = [
        "don't have to pick",
        "don't have to choose",
        "one platform",
        "single platform",
        "all in one"
    ]
    has_integrator = any(p.lower() in draft.lower() for p in integrator_patterns)

    if not has_integrator:
        warnings.append({
            "type": "WARNING",
            "message": "缺少 L4 整合者定位表述"
        })

    # 检查禁止表述
    forbidden_patterns = [
        "alici.ai is the best",
        "better than",
        "beats",
        "#1 tool",
        "superior"
    ]
    for pattern in forbidden_patterns:
        if pattern.lower() in draft.lower():
            warnings.append({
                "type": "WARNING",
                "message": f"检测到禁止表述: {pattern}"
            })

    return warnings
```

**验证清单**:
- [ ] 包含整合者定位表述
- [ ] 不包含 "best tool" 自称
- [ ] 不包含 "better than" 贬低竞品
- [ ] alici.ai 定位为平台，非单一工具

---

### 原则 6: 引用密度 ⚠️ WARNING

**规则**: Tool Showdown 文章引用密度 ≥ 5/千字

**检查方法**:
```python
def check_citation_density(draft):
    word_count = count_words(draft)

    # 计算引用数量 (链接 + 来源标注)
    citation_patterns = [
        r'According to \[',
        r'\[Source\]',
        r'https?://',
        r'\(\d{4}\)',  # 年份引用
        r'G2|Capterra|Trustpilot'  # 评测平台
    ]

    citation_count = 0
    for pattern in citation_patterns:
        citation_count += len(re.findall(pattern, draft))

    density = citation_count / (word_count / 1000)

    if density < 5:
        return {
            "status": "WARNING",
            "message": f"引用密度 {density:.1f}/千字，低于目标 5/千字"
        }

    return {"status": "PASS", "density": density}
```

**验证清单**:
- [ ] 引用密度 ≥ 5/千字
- [ ] L1-L3 权威来源占比 ≥ 50%
- [ ] 所有外部数据有年份
- [ ] 包含至少 3 个不同来源

---

## 验证报告模板

```markdown
# 洗稿验证报告

**文章标题**: [标题]
**验证日期**: [日期]
**验证版本**: InVideo Principles v1.0

## 验证结果汇总

| 原则 | 状态 | 详情 |
|------|------|------|
| 1. Key Takeaways 前置 | ⛔/✅ | [详情] |
| 2. Reframe 开篇 | ⛔/✅ | [详情] |
| 3. Source Attribution | ⛔/✅ | [详情] |
| 4. 无虚假声明 | ⛔/✅ | [详情] |
| 5. L4 整合者定位 | ⚠️/✅ | [详情] |
| 6. 引用密度 | ⚠️/✅ | [X]/千字 |

## BLOCKING 问题 (必须修复)

1. [问题描述]
   - 位置: [行号/章节]
   - 修复建议: [建议]

## WARNING 问题 (建议修复)

1. [问题描述]
   - 位置: [行号/章节]
   - 修复建议: [建议]

## 总体评估

- **BLOCKING 数量**: [N]
- **WARNING 数量**: [N]
- **验证结果**: PASS / NEEDS_FIX / MANUAL_REVIEW

## 下一步

- [ ] 修复所有 BLOCKING 问题
- [ ] 评估 WARNING 问题
- [ ] 重新验证
```

---

## 自动验证流程

```python
def validate_rewrite_article(draft, source_features):
    """
    完整的洗稿验证流程
    """
    report = {
        "blocking": [],
        "warning": [],
        "passed": []
    }

    # 1. Key Takeaways 位置
    result = check_key_takeaways_position(draft)
    categorize_result(report, "Key Takeaways 前置", result)

    # 2. Reframe 开篇
    result = check_reframe_opening(draft)
    categorize_result(report, "Reframe 开篇", result)

    # 3. Source Attribution
    result = check_source_attribution(draft)
    categorize_result(report, "Source Attribution", result)

    # 4. 声明准确性
    errors = check_claim_accuracy(draft)
    for error in errors:
        if error["type"] == "BLOCKING":
            report["blocking"].append(error)
        else:
            report["warning"].append(error)

    # 5. L4 定位
    warnings = check_l4_positioning(draft)
    report["warning"].extend(warnings)

    # 6. 引用密度
    result = check_citation_density(draft)
    categorize_result(report, "引用密度", result)

    # 生成验证结果
    if report["blocking"]:
        report["status"] = "NEEDS_FIX"
    elif len(report["warning"]) > 3:
        report["status"] = "MANUAL_REVIEW"
    else:
        report["status"] = "PASS"

    return report
```

---

## 版本历史

### v1.0 (2026-01-26)
- 初始版本
- 六大原则验证清单
- 自动验证函数模板
- 验证报告模板

---

*InVideo 原则验证模板 - 确保洗稿模式输出符合质量标准*
