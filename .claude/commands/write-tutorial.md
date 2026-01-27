# /write-tutorial - 生成 Tutorial 文章

使用 blog-tutorial-writer Skill 生成 1,800-2,500 词教程文章。

## 预置上下文

```bash
# 检查 Topic Brief 是否存在
ls -la /Users/H/Documents/AliciBlog/reports/*/00-topic-brief.json 2>/dev/null | tail -3

# 当前日期
echo "发布日期: $(date +%Y-%m-%d)"
```

## 输入要求

- Topic Brief JSON（来自 /scout-topic）
- 或直接提供主题描述

## 文章结构

```
[开篇直答 50词] → [引言 200词] → [背景 250词] →
[Step 1-7 各300-400词] → [常见错误 3-5项] →
[Pro Tips 3-5项] → [结论 150词] → [FAQ 3-5问]
```

## 输出格式

包含完整 E-E-A-T 字段：
- date / last_updated
- author (name, role, bio)
- featured_image (url, alt)
- 3-5 个外部来源引用
- 5-7 个图片占位符
- 尾部署名

## 输出位置

```
/reports/[YYYY-MM-DD]-[topic]/
├── 01-article-draft.md
└── 00-implementation.md  # 进度追踪
```

## 质量目标

- 字数: 1,800-2,500 词
- AEO 目标分数: ≥ 75 分
- 外链数量: 3-5 个

## 使用示例

```
/write-tutorial 基于最新的 Topic Brief 生成文章
```

---

*基于 blog-tutorial-writer Skill*
