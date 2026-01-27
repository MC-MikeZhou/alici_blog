# /analyze-aeo - AEO 内容评分

使用 aeo-analyzer Skill 评估文章的 AI 答案引擎友好度。

## 预置上下文

```bash
# 检查最新文章
ls -la /Users/H/Documents/AliciBlog/reports/*/01-article-draft.md 2>/dev/null | tail -3

# AEO 评分框架位置
echo "评分框架: skills/core/aeo-analyzer/EVALUATION_FRAMEWORK.md"
```

## 评分模块 (100 分制)

| 模块 | 权重 | 评估内容 |
|------|------|---------|
| **M1: 内容结构** | 30% | 标题对齐、开篇直答、FAQ、列表/表格 |
| **M2: 技术可索引** | 25% | Schema、JS渲染、语义HTML |
| **M3: E-E-A-T 信号** | 25% | 作者信息、来源引用、数据统计 |
| **M4: 可见性设计** | 20% | URL语义、Meta描述、查询覆盖 |

## 评分解读

```
90-100: Excellent (高度优化)
75-89:  Good (可发布) ← 目标门槛
60-74:  Fair (需改进)
<60:    Poor (不可发布)
```

## 输出位置

```
/reports/[YYYY-MM-DD]-[topic]/
└── 03-aeo-score.md
```

## 后续行动

- Score ≥ 75: 通过，可进入发布流程
- Score < 75: 触发 /improve-article 自动改进
- Score < 60: 标记 MANUAL_REVIEW

## 使用示例

```
/analyze-aeo 评估 reports/2025-01-15-viral-ai-videos/01-article-draft.md
```

---

*基于 aeo-analyzer Skill*
