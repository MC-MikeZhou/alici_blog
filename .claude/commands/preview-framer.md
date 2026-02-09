# /preview-framer - 生成 Framer 预览

使用 framer-previewer Skill 生成文章在 Framer CMS 导入后的可视化预览。

## 预置上下文

```bash
# 检查最新编辑版文章和 JSON 文件
ls -la reports/*/01-article-edited*.md 2>/dev/null | tail -3
ls -la reports/*/06-article-final.json 2>/dev/null | tail -3
```

## 预览内容

1. **本地 HTML 文件** (浏览器可直接打开)
2. **内容摘要**:
   - 标题和元数据
   - 封面图验证
   - 章节统计 (H2 数量)
   - 图片统计 (正文图片数)
   - 表格和列表统计
   - CTA 信息

## 输出位置

```
/reports/[YYYY-MM-DD]-[topic]/
└── 07-preview.html          # 主预览文件
└── 07-preview-v2.2.html     # 带版本标记 (如有)
```

## 预览特性

✅ **模拟 Framer 渲染效果**:
- H2 使用 `<h6><strong>` 样式
- 列表项包含 `data-preset-tag="p"` 属性
- 图片和表格用 `<figure>` 包裹
- 所有链接 `target="_blank"`

✅ **alici.ai 品牌样式**:
- 绿色主题 (#10B981)
- 极简排版
- 响应式设计

✅ **预览标识**:
- 顶部显示 "Preview Mode" 徽章
- 提示这是 Framer 导入后的效果

## 用途

- **发布前验证**: 在导入 Framer CMS 前检查最终效果
- **布局检查**: 验证图片位置、表格格式、列表缩进
- **样式预览**: 确保标题、段落、CTA 按钮符合预期
- **快速迭代**: 无需实际导入 Framer 即可查看效果

## 打开预览

### macOS
```bash
open /reports/[date]-[topic]/07-preview.html
```

### Linux
```bash
xdg-open /reports/[date]-[topic]/07-preview.html
```

### Windows
```bash
start /reports/[date]-[topic]/07-preview.html
```

## 验证清单

在浏览器中检查：
- [ ] 封面图是否正确显示？
- [ ] 标题样式是否醒目？
- [ ] H2 章节是否显示为粗体大号字？
- [ ] 所有图片是否在正确位置？
- [ ] 表格是否易读？
- [ ] 列表是否正确缩进？
- [ ] 链接是否可点击？
- [ ] CTA 按钮是否醒目？

## 后续行动

- ✅ 样式正确 → 导入 Framer CMS 发布
- ⚠️ 需调整 → 返回 /edit-article 或 /convert-to-framer
- ❌ 有错误 → 检查源文件，修复后重新预览

## 使用示例

### 示例 1: 预览编辑后的文章
```bash
/preview-framer /reports/2026-01-15-best-ai-video-tools/01-article-edited-v2.2.md
```

### 示例 2: 预览 JSON 文件
```bash
/preview-framer /reports/2026-01-15-best-ai-video-tools/06-article-final.json
```

### 示例 3: 使用相对路径
```bash
cd /reports/2026-01-15-best-ai-video-tools
/preview-framer 01-article-edited.md
```

## 支持的输入

| 输入类型 | 文件格式 | 说明 |
|----------|----------|------|
| Markdown | `01-article-edited.md` | 需包含 YAML frontmatter |
| Markdown | `05-article-improved.md` | 改进版文章 |
| JSON | `06-article-final.json` | Framer CMS 格式 |

## 工作流位置

```
Phase 5: Edit        → /edit-article
Phase 6: Convert     → /convert-to-framer
Phase 7: Preview     → /preview-framer (THIS COMMAND) ✨
Phase 8: Publish     → 手动导入 Framer CMS
```

---

*基于 framer-previewer Skill v1.0*
