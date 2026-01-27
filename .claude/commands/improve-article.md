# /improve-article - 自动改进文章

使用 auto-improver Skill 基于 AEO 评分报告自动改进文章。

## 预置上下文

```bash
# 检查最新 AEO 报告
ls -la /Users/H/Documents/AliciBlog/reports/*/03-aeo-score.md 2>/dev/null | tail -3

# 检查最新文章
ls -la /Users/H/Documents/AliciBlog/reports/*/01-article-draft.md 2>/dev/null | tail -3
```

## 改进策略

**优先级矩阵**: Priority = Point Value × Ease ÷ Risk

| 优先级 | 项目 | 修复方式 | 预期提分 |
|--------|------|---------|---------|
| CRITICAL | 开篇直答、FAQ、列表/表格 | 40-60词直答、3-5个FAQ | +4分/项 |
| HIGH | 段落长度、可引用块、数据 | 拆分段落、添加统计 | +3-4分/项 |
| MEDIUM | 发布日期、品牌一致性 | 添加元数据 | +3-4分/项 |
| LOW | Schema、作者信息 | 标记人工审核 | - |

## 迭代规则

- 最多 3 轮迭代
- 每轮修复 3-5 个高优先级项目
- 迭代后自动重新评分
- 3 轮后仍 < 75 分 → MANUAL_REVIEW

## 输出位置

```
/reports/[YYYY-MM-DD]-[topic]/
├── 04-article-improved.md    # 改进版文章
├── 04-changelog.md           # 改进记录
└── 00-implementation.md      # 更新进度
```

## 使用示例

```
/improve-article 基于 03-aeo-score.md 改进 01-article-draft.md
```

---

*基于 auto-improver Skill*
