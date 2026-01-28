# /upload-cdn - 上传图片到 CDN

上传本地图片到 Alici CDN 服务器，返回可用的 CDN URL。

## 使用方法

```
/upload-cdn <图片路径>
```

**示例**:
```
/upload-cdn /reports/2026-01-21-topic/assets/hero.jpg
/upload-cdn assets/cover-image.png
```

## 服务器配置

| 配置项 | 值 |
|--------|-----|
| 服务器 | 45.76.70.215 |
| 端口 | 22 |
| 用户 | root |
| 密码 | 5A_p@cjpX74H(LJM |
| 目标路径 | /var/www/static/static/image/other/gen_images/ |
| CDN 域名 | https://ct2.alici.ai/static/image/other/gen_images/ |

## 执行步骤

### Step 1: 验证文件存在

```bash
ls -la <图片路径>
```

### Step 2: 上传到 CDN

```bash
sshpass -p '5A_p@cjpX74H(LJM' rsync -avz -e 'ssh -p 22 -o StrictHostKeyChecking=no' <图片路径> root@45.76.70.215:/var/www/static/static/image/other/gen_images/
```

### Step 3: 验证上传成功

```bash
curl -I https://ct2.alici.ai/static/image/other/gen_images/<文件名> | head -5
```

### Step 4: 返回 CDN URL

```
✅ 上传成功
文件: <文件名>
CDN URL: https://ct2.alici.ai/static/image/other/gen_images/<文件名>
```

## 输出格式

成功时:
```
✅ 上传成功
文件: hero-motion-control-workflow.jpg
大小: 132 KB
CDN URL: https://ct2.alici.ai/static/image/other/gen_images/hero-motion-control-workflow.jpg
```

失败时:
```
❌ 上传失败
原因: 文件不存在 / 网络错误 / 认证失败
```

## 支持的格式

- 图片: `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`, `.svg`
- 其他: 任何文件都可以上传

## 注意事项

1. 文件名会保持原样，建议使用英文小写和连字符
2. 如果 CDN 上已存在同名文件，会被覆盖
3. 上传后需要几秒钟 CDN 缓存生效

---

*用于 AliciBlog 图片资源上传*
