---
name: framer-previewer
version: "1.1"
description: >
  Generate visual HTML preview of Framer CMS rendering before publishing.
  Accepts both Markdown and JSON inputs, simulates Framer styling.
  Triggers on: preview framer, 预览 framer, preview before publish, 发布预览.
allowed-tools: Read, Write
---

# Framer Previewer Skill v1.0

> **可视化预览** - 在导入 Framer CMS 前查看最终渲染效果

## 触发条件

- 用户调用 `/preview-framer`
- 关键词："preview framer", "预览 framer", "preview before publish", "发布预览"

## 输入要求

**接受两种输入**：
1. **Markdown 文件** (`01-article-edited.md`) - 包含 YAML frontmatter
2. **JSON 文件** (`06-article-final.json`) - Framer CMS 格式

**推荐时机**: 在 `/convert-to-framer` 之后，发布前

## 执行流程

### Phase 1: 解析输入

```
1. 检测输入文件类型:
   - .md → 按 Markdown 处理
   - .json → 按 Framer JSON 处理

2. 如果是 Markdown:
   ├── 读取文件内容
   ├── 分离 YAML frontmatter 和 Markdown body
   ├── 提取字段: title, featured_image, category, tags 等
   └── 应用 CONVERSION_RULES 转换为 Framer HTML

3. 如果是 JSON:
   ├── 读取 JSON 数组
   ├── 提取第一个对象（文章）
   ├── 直接使用 article_body_content
   └── 提取元数据: title, cover.url, read_time 等

4. 定位图片资源:
   ├── 检查图片是否使用 CDN URL (优先)
   ├── 如果是本地路径, 转换为绝对路径
   └── 验证图片可访问性
```

### Phase 2: 生成预览 HTML

```
1. 加载 TEMPLATE.html
2. 替换模板变量:
   - {{TITLE}} → 文章标题
   - {{SUB_TITLE}} → 副标题 (如有)
   - {{READ_TIME}} → 阅读时间
   - {{DATE}} → 发布日期
   - {{COVER_URL}} → 封面图 URL
   - {{ARTICLE_BODY}} → Framer HTML 正文
   - {{CTA_LINK}} → CTA 链接
   - {{CTA_BUTTON}} → CTA 按钮文案

3. 注入 Framer-like CSS:
   - 模拟 alici.ai 博客样式
   - 绿色中心主题
   - 响应式布局

4. 添加预览标识:
   - 顶部显示 "Preview Mode" 徽章
   - 提示："这是 Framer CMS 导入后的预览效果"
```

### Phase 3: 输出预览文件

```
1. 确定输出路径:
   /reports/[date]-[topic]/07-preview.html

2. 写入 HTML 文件

3. 输出预览摘要:
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   🎨 Framer 预览已生成
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   预览文件: /reports/.../07-preview.html

   📊 内容摘要:
   - 标题: [Title]
   - 封面: ✅ [filename] ([width]×[height])
   - 正文图片: N 张
   - 章节: N 个 H2
   - 表格: N 个
   - 列表: N 个
   - CTA: "[CTA button]" → [CTA_link]

   📝 请在浏览器中打开以查看完整效果

   macOS: open /reports/.../07-preview.html
   Linux: xdg-open /reports/.../07-preview.html
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Phase 4: (可选) 自动打开浏览器

如果用户同意，自动执行：
```bash
open /reports/.../07-preview.html  # macOS
```

## 预览 HTML 特性

### 模拟 Framer 渲染效果

✅ **HTML 结构**：
- H2 使用 `<h6><strong>` (与 Framer 一致)
- 列表项包含 `data-preset-tag="p"` 属性
- 图片和表格用 `<figure>` 包裹
- 所有链接 `target="_blank"`

✅ **样式系统**：
- 字体: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto
- 行高: 1.7
- 最大宽度: 680px (居中)
- 绿色主题: #10B981 (alici.ai 品牌色)

✅ **响应式设计**：
- 移动端友好
- 图片自适应宽度
- 表格横向滚动

### 预览标识

```html
<div class="preview-header">
  <span class="badge">Preview Mode</span>
  <p class="hint">这是 Framer CMS 导入后的预览效果</p>
</div>
```

## 图片处理策略

| 图片来源 | 处理方式 | 优先级 |
|----------|----------|--------|
| **CDN URL** | 直接使用 `https://ct2.alici.ai/...` | ✅ 最高 |
| **本地绝对路径** | 转换为 `file:///Users/H/...` | ⚠️ 备选 |
| **本地相对路径** | 转换为绝对路径 | ⚠️ 备选 |

**CDN URL 识别**：
```
https://ct2.alici.ai/static/image/other/gen_images/
https://v3b.fal.media/files/...
```

## 内容统计

预览摘要中自动统计：

| 统计项 | 计算方法 |
|--------|----------|
| **章节数** | H2 标题数量 (`<h6><strong>` 标签) |
| **图片数** | `<figure><img>` 标签数量 (不含封面) |
| **表格数** | `<figure><table>` 标签数量 |
| **列表数** | `<ul>` 和 `<ol>` 标签数量 |
| **字数** | article_body 纯文本字数 |

## 错误处理

| 错误场景 | 处理方式 |
|----------|----------|
| 输入文件不存在 | ERROR: "文件未找到: [path]" |
| Markdown 缺少 frontmatter | ERROR: "Markdown 文件缺少 YAML frontmatter" |
| JSON 格式错误 | ERROR: "JSON 格式无效" |
| 缺少必需字段 (title) | ERROR: "缺少必需字段: title" |
| 封面图 URL 无效 | ⚠️ WARNING: "封面图 URL 可能无效，请检查" |

## 输出文件命名

| 输入文件 | 输出文件 |
|----------|----------|
| `01-article-edited.md` | `07-preview.html` |
| `01-article-edited-v2.2.md` | `07-preview-v2.2.html` |
| `06-article-final.json` | `07-preview.html` |

**版本保留规则**：自动检测输入文件的版本后缀 (如 `-v2.2`)，应用到输出文件名

## 验证检查清单

预览生成后，提示用户在浏览器中验证：

```
🔍 预览验证清单:
├─ 封面图: 是否正确显示？
├─ 标题样式: H2 是否显示为粗体大号字？
├─ 图片位置: 所有图片是否在正确位置？
├─ 表格格式: 表格是否易读？
├─ 列表缩进: 列表项是否正确缩进？
├─ 链接功能: 点击链接是否跳转？
└─ CTA 按钮: 按钮是否醒目？
```

## 与其他 Skills 的集成

### 推荐工作流

```
Phase 5: Edit        → /edit-article
Phase 6: Convert     → /convert-to-framer
Phase 7: Preview     → /preview-framer (THIS SKILL) ✨
Phase 8: Publish     → 手动导入 Framer CMS
```

### 输入来源

| Skill | 输出 | 作为本 Skill 输入 |
|-------|------|-------------------|
| editor | `01-article-edited.md` | ✅ 推荐 |
| markdown-to-framer | `06-article-final.json` | ✅ 推荐 |
| auto-improver | `05-article-improved.md` | ✅ 可用 |

## 相关文件

- `TEMPLATE.html` - HTML 模板文件
- `../markdown-to-framer/CONVERSION_RULES.md` - Framer HTML 转换规则
- `../BRAND_VISUAL_GUIDE.md` - alici.ai 品牌视觉规范

## 使用示例

### 示例 1: 预览编辑后的文章

```bash
/preview-framer /reports/2026-01-15-best-ai-video-tools/01-article-edited-v2.2.md
```

### 示例 2: 预览 JSON 文件

```bash
/preview-framer /reports/2026-01-15-best-ai-video-tools/06-article-final.json
```

### 示例 3: 从相对路径

```bash
cd /reports/2026-01-15-best-ai-video-tools
/preview-framer 01-article-edited.md
```

## 技术说明

### Markdown 转换复用

本 Skill 复用 `markdown-to-framer` 的转换规则：
- H2 → `<h6><strong>`
- H3 → `<p><strong>`
- 列表项 → `data-preset-tag="p"`
- 表格/图片 → `<figure>` 包裹

### CSS 样式源

CSS 参考以下来源设计：
1. Framer 实际渲染样式
2. alici.ai 博客风格
3. BRAND_VISUAL_GUIDE.md 规范

### 性能考虑

- 单文件输出 (~200-500KB)
- CDN 图片加载 (已优化)
- 无外部依赖
- 浏览器本地渲染 (无服务器要求)
