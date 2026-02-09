# /preview-chinese - 生成中文预览

使用 chinese-previewer Skill 生成文章的中文摘要预览。

## 预置上下文

```bash
# 检查最新文章
ls -la reports/*/01-article-draft.md 2>/dev/null | tail -3
ls -la reports/*/04-article-improved.md 2>/dev/null | tail -3
```

## 预览内容

1. **内容概要** (3-5 句核心观点)
2. **主要章节要点** (提炼 H2 关键点)
3. **AEO 亮点检查表**:
   - 开篇直答: ✅/⚠️/❌
   - FAQ 章节: ✅/⚠️/❌
   - 可引用块: ✅/⚠️/❌
   - 列表/表格: ✅/⚠️/❌
4. **关键引用块** (中英对照)
5. **审核要点检查表**

## 输出位置

```
/reports/[YYYY-MM-DD]-[topic]/
└── 02-chinese-preview.md
```

## 用途

- 非英文团队成员快速了解文章方向
- 早期发现选题/内容问题
- 加速审核反馈周期

## 后续行动

- ✅ 通过 → 继续 /analyze-aeo
- ⚠️ 需修改 → 返回 Writer 调整
- ❌ 重选 → 返回 /scout-topic

## 使用示例

```
/preview-chinese 生成 01-article-draft.md 的中文预览
```

---

*基于 chinese-previewer Skill*
