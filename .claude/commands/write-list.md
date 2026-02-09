# /write-list - 生成 List 榜单文章

使用 blog-list-writer Skill 生成 2,000-3,000 词排名榜单文章。

## 预置上下文

```bash
# 检查 Topic Brief 是否存在
ls -la reports/*/00-topic-brief.json 2>/dev/null | tail -3

# 当前日期
echo "发布日期: $(date +%Y-%m-%d)"
```

## 输入要求

- Topic Brief JSON（来自 /scout-topic，content_type="list"）
- 或直接提供榜单主题

## 文章结构

```
[开篇直答+Top3 60词] → [引言 300词] → [背景 300词] →
[列表项 10-15个 各150-200词] → [对比表格] →
[如何选择 400词] → [结论 200词] → [FAQ 3-5问]
```

## 列表项模板

```markdown
## [N]. [工具名称]

**Core Feature**: [一句话核心价值]
**Best For**: [目标用户/场景]
**Key Advantages**:
• [优势1]
• [优势2]
• [优势3]
**Considerations**: [诚实的局限性]
**Pricing**: [定价信息]
**Rating**: ⭐⭐⭐⭐⭐ (X/10)
```

## 输出位置

```
/reports/[YYYY-MM-DD]-[topic]/
├── 01-article-draft.md
└── 00-implementation.md
```

## 质量目标

- 字数: 2,000-3,000 词
- AEO 目标分数: ≥ 75 分
- 外链数量: 5-8 个（每个工具链接官网）
- alici.ai 定位: 诚实客观，基于真实优势排名

## 使用示例

```
/write-list 生成 "15 Best AI Video Generators 2025" 文章
```

---

*基于 blog-list-writer Skill*
