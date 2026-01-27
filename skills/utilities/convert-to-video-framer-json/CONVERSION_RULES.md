# Markdown → Framer HTML 转换规则

> Framer CMS 使用特定的 HTML 格式，与标准 Markdown 转 HTML 有差异。

## 核心差异

| 元素 | 标准 HTML | Framer HTML |
|------|-----------|-------------|
| H2 标题 | `<h2>` | `<h6><strong>...</strong></h6>` |
| H3 标题 | `<h3>` | `<p><strong>...</strong></p>` |
| 列表项 | `<li>` | `<li data-preset-tag="p"><p>...</p></li>` |
| 表格 | `<table>` | `<figure><table>...</table></figure>` |
| 图片 | `<img src="..." alt="...">` | `<img alt="..." src="...">` (无 figure，alt 在前) |

---

## 转换规则详表

### 1. 标题处理

**H1 标题**：完全移除（title 是单独的 JSON 字段）

```markdown
# 10 Best AI Video Generators
```
→ 不输出（已在 `title` 字段）

**H2 标题**：转为 `<h6><strong>...</strong></h6>`

```markdown
## Why AI Video Generators Matter
```
→
```html
<h6><strong>Why AI Video Generators Matter</strong></h6>
```

**H3 标题**：转为加粗段落

```markdown
### Key Features
```
→
```html
<p><strong>Key Features</strong></p>
```

**H4-H6 标题**：转为加粗段落（与 H3 相同）

---

### 2. 段落处理

普通段落用 `<p>` 包裹：

```markdown
This is a regular paragraph with some text.
```
→
```html
<p>This is a regular paragraph with some text.</p>
```

**空行**：不输出（用于分隔段落）

---

### 3. 内联格式

| Markdown | HTML |
|----------|------|
| `**bold**` | `<strong>bold</strong>` |
| `*italic*` | `<em>italic</em>` |
| `***bold italic***` | `<strong><em>bold italic</em></strong>` |
| `` `code` `` | `<code>code</code>` |

---

### 4. 链接处理

**所有链接必须添加 `target="_blank"`**

```markdown
[alici.ai](https://alici.ai)
```
→
```html
<a href="https://alici.ai" target="_blank">alici.ai</a>
```

**带格式的链接**：

```markdown
**[Try alici.ai](https://alici.ai)**
```
→
```html
<strong><a href="https://alici.ai" target="_blank">Try alici.ai</a></strong>
```

---

### 5. 列表处理

**无序列表**：

```markdown
- Item one
- Item two
- Item three
```
→
```html
<ul>
<li data-preset-tag="p"><p>Item one</p></li>
<li data-preset-tag="p"><p>Item two</p></li>
<li data-preset-tag="p"><p>Item three</p></li>
</ul>
```

**带格式的列表项**：

```markdown
- **Bold item**: with description
- *Italic item*: with description
```
→
```html
<ul>
<li data-preset-tag="p"><p><strong>Bold item</strong>: with description</p></li>
<li data-preset-tag="p"><p><em>Italic item</em>: with description</p></li>
</ul>
```

**有序列表**：

```markdown
1. First step
2. Second step
3. Third step
```
→
```html
<ol>
<li data-preset-tag="p"><p>First step</p></li>
<li data-preset-tag="p"><p>Second step</p></li>
<li data-preset-tag="p"><p>Third step</p></li>
</ol>
```

**关键点**：每个 `<li>` 必须有 `data-preset-tag="p"` 属性，内容用 `<p>` 包裹

---

### 6. 图片处理

```markdown
![Alt text](https://example.com/image.png)
```
→
```html
<img alt="Alt text" src="https://example.com/image.png">
```

**⚠️ 重要规则**：
- 图片标签**不用** `<figure>` 包裹（与表格不同）
- `alt` 属性**必须**在 `src` 属性前面
- 这是 Framer CMS 的特定要求，与标准 HTML 不同

**正确** ✅：
```html
<img alt="AI video generator interface" src="https://example.com/image.png">
```

**错误** ❌：
```html
<figure><img src="https://example.com/image.png" alt="AI video generator interface"></figure>
<img src="https://example.com/image.png" alt="AI video generator interface">
```

---

### 7. 表格处理

```markdown
| Tool | Price | Rating |
|------|-------|--------|
| Veo 3 | $20/mo | ★★★★★ |
| Kling | $5/mo | ★★★★★ |
```
→
```html
<figure>
<table>
<tbody>
<tr>
<th><p>Tool</p></th>
<th><p>Price</p></th>
<th><p>Rating</p></th>
</tr>
<tr>
<td><p>Veo 3</p></td>
<td><p>$20/mo</p></td>
<td><p>★★★★★</p></td>
</tr>
<tr>
<td><p>Kling</p></td>
<td><p>$5/mo</p></td>
<td><p>★★★★★</p></td>
</tr>
</tbody>
</table>
</figure>
```

**关键点**：
- 整个表格用 `<figure>` 包裹
- 表头用 `<th>` 而非 `<td>`
- 每个单元格内容用 `<p>` 包裹

---

### 8. 引用块处理

```markdown
> This is a blockquote with important information.
```
→
```html
<blockquote><p>This is a blockquote with important information.</p></blockquote>
```

**多行引用**：

```markdown
> First line of quote.
> Second line of quote.
```
→
```html
<blockquote>
<p>First line of quote.</p>
<p>Second line of quote.</p>
</blockquote>
```

---

### 9. 水平分割线

```markdown
---
```
→
```html
<hr>
```

或直接不输出（Framer 中很少使用 hr）

---

### 10. 代码块处理

````markdown
```python
def hello():
    print("Hello")
```
````
→
```html
<pre><code>def hello():
    print("Hello")</code></pre>
```

**注意**：Framer 对代码块支持有限，建议在博客中避免大段代码

---

### 11. 特殊字符处理

在生成 HTML 内容时，替换以下特殊字符以确保 Framer CMS 兼容性：

| 字符 | Unicode | 替换为 | 原因 |
|------|---------|--------|------|
| `—` (em dash) | U+2014 | ` - ` (空格+连字符+空格) | Framer JSON 解析问题 |
| `–` (en dash) | U+2013 | `-` (连字符) | 兼容性 |
| `'` `'` (智能单引号) | U+2018 U+2019 | `'` (直引号) | 兼容性 |
| `"` `"` (智能双引号) | U+201C U+201D | `"` (直双引号) | JSON 解析 |
| `…` (省略号) | U+2026 | `...` (三个点) | 兼容性 |

**示例**：
```
输入: "This—is a test" with "smart quotes"
输出: "This - is a test" with "smart quotes"
```

**注意**：此处理应在生成最终 HTML 内容后、写入 JSON 前执行。

---

## 特殊处理规则

### CTA 链接识别

如果段落包含 alici.ai 链接，保持原样但确保有 `target="_blank"`：

```markdown
**Ready to start?** [Try alici.ai free](https://app.alici.ai/)
```
→
```html
<p><strong>Ready to start?</strong> <a href="https://app.alici.ai/" target="_blank">Try alici.ai free</a></p>
```

### 连续段落

多个段落之间不需要额外分隔，每个都是独立的 `<p>`：

```markdown
First paragraph here.

Second paragraph here.
```
→
```html
<p>First paragraph here.</p><p>Second paragraph here.</p>
```

### HTML 实体

保留必要的 HTML 实体：
- `&` → `&amp;` (如果不是已有实体)
- `<` → `&lt;` (在代码块外)
- `>` → `&gt;` (在代码块外)

---

## 完整转换示例

**输入 Markdown**：

```markdown
## Why AI Video Generators Matter

The market has exploded. Here's what you need to know:

- **Cost reduction**: 90% cheaper than traditional production
- **Speed**: Generate in seconds vs. hours

| Tool | Best For |
|------|----------|
| Veo 3 | Quality |
| Kling | Value |

> AI video is the future of content creation.

**Ready to try?** [Start with alici.ai](https://app.alici.ai/)
```

**输出 Framer HTML**：

```html
<h6><strong>Why AI Video Generators Matter</strong></h6><p>The market has exploded. Here's what you need to know:</p><ul><li data-preset-tag="p"><p><strong>Cost reduction</strong>: 90% cheaper than traditional production</p></li><li data-preset-tag="p"><p><strong>Speed</strong>: Generate in seconds vs. hours</p></li></ul><figure><table><tbody><tr><th><p>Tool</p></th><th><p>Best For</p></th></tr><tr><td><p>Veo 3</p></td><td><p>Quality</p></td></tr><tr><td><p>Kling</p></td><td><p>Value</p></td></tr></tbody></table></figure><blockquote><p>AI video is the future of content creation.</p></blockquote><p><strong>Ready to try?</strong> <a href="https://app.alici.ai/" target="_blank">Start with alici.ai</a></p>
```

---

## 常见错误避免

| 错误 | 正确 |
|------|------|
| `<h2>Title</h2>` | `<h6><strong>Title</strong></h6>` |
| `<li>Item</li>` | `<li data-preset-tag="p"><p>Item</p></li>` |
| `<a href="...">` | `<a href="..." target="_blank">` |
| `<table>...</table>` | `<figure><table>...</table></figure>` |
| `<figure><img src="..." alt="..."></figure>` | `<img alt="..." src="...">` |
| `<img src="..." alt="...">` | `<img alt="..." src="...">` |
| 使用 em dash `—` | 使用空格+连字符 ` - ` |
| 使用 smart quotes `"..."` | 使用直引号 `"..."` |
