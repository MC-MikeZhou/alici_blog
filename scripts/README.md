# AliciBlog Scripts 

统一的图片生成与上传脚本，供 Skills System 调用。

## 脚本清单

| 脚本 | 用途 |
|------|------|
| `fal_image_generator.py` | FAL.ai nano-banana 图片生成 |
| `cdn_uploader.py` | CDN 上传（rsync） |
| `requirements.txt` | 依赖声明（当前无外部依赖） |

---

## 环境配置

### 1. API Key 设置

```bash
export FAL_API_KEY='your-fal-api-key'
```

添加到 `~/.zshrc` 或 `~/.bashrc` 以持久化：

```bash
echo 'export FAL_API_KEY="your-key-here"' >> ~/.zshrc
source ~/.zshrc
```

### 2. SSH 访问配置（用于 CDN 上传）

```bash
# 确保 SSH key 已添加
ssh-add ~/.ssh/id_rsa

# 测试连接
ssh root@45.76.70.215

# 首次连接需要确认 host key
```

---

## fal_image_generator.py 使用说明

### 基本用法

```bash
# 生成单张 hero 图片
python scripts/fal_image_generator.py \
  --prompt "Magazine cover style editorial photography for AI video tools article..." \
  --role hero \
  --output-dir ./gen_images \
  --filename ai-video-hero.png

# 生成 concept 图片（自动使用 1200x800 尺寸）
python scripts/fal_image_generator.py \
  --prompt "Educational infographic explaining video generation workflow..." \
  --role concept

# 测试配置
python scripts/fal_image_generator.py --test
```

### 批量生成

创建 `prompts.json`:

```json
[
  {
    "prompt": "Magazine cover style editorial photography...",
    "role": "hero",
    "filename": "ai-video-hero.png"
  },
  {
    "prompt": "Educational infographic diagram...",
    "role": "concept",
    "filename": "ai-video-concept.png"
  },
  {
    "prompt": "Side-by-side comparison infographic...",
    "role": "comparison",
    "filename": "ai-video-comparison.png"
  }
]
```

执行批量生成：

```bash
python scripts/fal_image_generator.py --batch prompts.json
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--prompt` | ICS 框架 Prompt | 必填 |
| `--role` | 图片角色 (hero\|concept\|comparison\|cta) | hero |
| `--output-dir` | 输出目录 | ./gen_images |
| `--filename` | 自定义文件名 | 自动生成 |
| `--batch` | 批量模式 JSON 文件路径 | - |
| `--test` | 测试模式（检查配置） | - |

### 图片角色与尺寸

| Role | 尺寸 | 用途 |
|------|------|------|
| `hero` | 1920x1080 | 封面图 |
| `concept` | 1200x800 | 概念图 |
| `comparison` | 1200x800 | 对比图 |
| `cta` | 600x400 | 行动号召卡片 |

---

## cdn_uploader.py 使用说明

### 基本用法

```bash
# 上传 ./gen_images/ 目录下所有图片
python scripts/cdn_uploader.py --dir ./gen_images

# 预览上传（不实际上传）
python scripts/cdn_uploader.py --dir ./gen_images --dry-run

# 仅验证 SSH 访问
python scripts/cdn_uploader.py --verify-only
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--dir` | 图片目录 | ./gen_images |
| `--dry-run` | 预览模式 | - |
| `--verify-only` | 仅验证 SSH | - |

---

## 完整工作流示例

### 单篇文章图片生成

```bash
# Step 1: 创建 prompts.json (Editor Skill 会自动生成)
cat > prompts.json <<EOF
[
  {
    "prompt": "Magazine cover style editorial photography for tech article about AI video generation. Content: Multiple floating holographic screens showing video editing timelines, Abstract neural network patterns glowing in background, Central focus on stylized AI processor chip with video frame overlay, Subtle film reel and play button elements integrated into composition. Style: Cinematic lighting with dramatic rim light, shallow depth of field, modern minimalist composition, rich color palette with electric blue and purple accent, 8K resolution, professional editorial aesthetic.",
    "role": "hero",
    "filename": "ai-video-tools-hero.png"
  },
  {
    "prompt": "Educational infographic diagram explaining video generation workflow. Content: Section 1: Input (video prompt) - showing text input with icon, Section 2: AI Processing - showing neural network with loading indicator, Section 3: Output (generated video) - showing video player with play button, Visual flow arrows showing relationships between sections, Key statistics embedded: 30 sec generation time. Style: Clean McKinsey presentation aesthetic, soft gradient background (blue to purple), numbered steps, professional sans-serif typography, maximum legibility at thumbnail size, minimalist geometric icons.",
    "role": "concept",
    "filename": "ai-video-tools-concept.png"
  }
]
EOF

# Step 2: 生成图片
python scripts/fal_image_generator.py --batch prompts.json

# Step 3: 上传到 CDN
python scripts/cdn_uploader.py --dir ./gen_images

# Step 4: 输出结果
# ./gen_images/ai-video-tools-hero.png
# ./gen_images/ai-video-tools-concept.png
# prompts_results.json (包含 CDN URLs)
```

### 从 Editor Skill 调用

Editor Skill 会自动：
1. 分析文章，选择 3-5 个战略位置
2. 生成 ICS Prompt并保存为 JSON
3. 调用 `fal_image_generator.py --batch`
4. 自动上传图片（如果配置了 SSH）
5. 更新 Markdown 文件中的图片 URL

---

## 故障排查

### fal_image_generator.py

| 问题 | 解决方案 |
|------|----------|
| `FAL_API_KEY not set` | 运行 `export FAL_API_KEY='your-key'` |
| `HTTP Error 401` | API Key 错误或过期 |
| `Polling timeout` | 图片生成时间过长（>5分钟），重试或检查 FAL.ai 状态 |
| `Download failed` | 临时图片 URL 过期，重新生成 |

### cdn_uploader.py

| 问题 | 解决方案 |
|------|----------|
| `SSH connection failed` | 确保 SSH key 已添加：`ssh-add ~/.ssh/id_rsa` |
| `rsync command not found` | 安装 rsync：`brew install rsync` |
| `Permission denied` | 检查 SSH 权限：`ssh root@45.76.70.215` |

---

## 技术细节

### FAL.ai API 端点

| 端点 | 用途 |
|------|------|
| `https://queue.fal.run/fal-ai/nano-banana` | 提交请求 |
| `{endpoint}/requests/{id}/status` | 轮询结果 |

### CDN 配置

| 配置项 | 值 |
|--------|-----|
| 服务器 | root@45.76.70.215 |
| 远程路径 | /var/www/static/static/image/other/gen_images/ |
| CDN 前缀 | https://ct2.alici.ai/static/image/other/gen_images/ |

---

## 开发计划

### v1.0 (当前)
- [x] nano-banana 图片生成
- [x] 异步队列轮询
- [x] 批量生成
- [x] CDN 上传

### v1.1 (未来)
- [ ] 图片压缩优化（< 500KB）
- [ ] 并行批量生成
- [ ] Retry 机制增强
- [ ] 进度条显示

---

**Created**: 2026-01-15
**Version**: 1.0
**Maintained by**: AliciBlog Team
