# 自定义配置

> 背景、分辨率、字幕等视频外观配置选项

---

## 概览

HeyGen 提供灵活的视频外观定制能力，无需视频编辑软件即可实现：

- **背景** - 纯色、图片、视频、透明
- **分辨率** - 1080p、720p、自定义尺寸
- **画面比例** - 横屏、竖屏、方形
- **字幕** - 自动字幕 + 样式定制

---

## 配置位置

所有自定义选项在 `/v2/video/generate` 请求的**顶层**配置：

```json
{
  "video_inputs": [ ... ],          // 数字人 + 语音
  "dimension": { ... },              // 分辨率
  "aspect_ratio": "16:9",            // 画面比例
  "background": { ... },             // 背景
  "caption": true,                   // 字幕
  "test": false                      // 测试模式
}
```

---

## 章节导航

### [backgrounds.md](backgrounds.md) - 背景配置
- **纯色背景** - `#HEX` 颜色码
- **图片背景** - 上传图片 URL
- **视频背景** - 动态背景视频
- **透明背景** - 用于 Remotion 集成

**示例**:
```json
{
  "background": {
    "type": "color",
    "value": "#E8F5E9"
  }
}
```

---

### [dimensions.md](dimensions.md) - 分辨率与比例
- **预设分辨率** - 1080p、720p
- **自定义尺寸** - 任意宽高
- **画面比例** - 16:9、9:16、1:1

**示例**:
```json
{
  "dimension": {
    "width": 1920,
    "height": 1080
  },
  "aspect_ratio": "16:9"
}
```

---

### [captions.md](captions.md) - 字幕配置
- **自动字幕** - 基于语音生成
- **字幕样式** - 字体、颜色、位置
- **多语言支持** - 自动翻译字幕

**示例**:
```json
{
  "caption": {
    "enabled": true,
    "position": "bottom",
    "font_size": 24,
    "font_color": "#FFFFFF"
  }
}
```

---

## 常用配置组合

### YouTube 横屏视频
```json
{
  "dimension": {"width": 1920, "height": 1080},
  "aspect_ratio": "16:9",
  "background": {"type": "color", "value": "#FFFFFF"},
  "caption": true
}
```

### TikTok/Shorts 竖屏
```json
{
  "dimension": {"width": 1080, "height": 1920},
  "aspect_ratio": "9:16",
  "background": {"type": "image", "url": "https://example.com/bg.jpg"},
  "caption": true
}
```

### Instagram 方形
```json
{
  "dimension": {"width": 1080, "height": 1080},
  "aspect_ratio": "1:1",
  "background": {"type": "color", "value": "#000000"},
  "caption": false
}
```

### Remotion 集成（透明背景）
```json
{
  "dimension": {"width": 1920, "height": 1080},
  "aspect_ratio": "16:9",
  "background": {"type": "transparent"}
}
```

---

## 测试模式

### 快速预览（test 模式）

生成低分辨率预览视频，缩短等待时间：

```json
{
  "test": true
}
```

**特点**:
- ✅ 分辨率降为 480p
- ✅ 生成速度快（1-2 分钟）
- ✅ 不消耗配额
- ❌ 带水印

**使用场景**:
- 测试形象/语音组合
- 验证文本内容
- 调试 API 参数

---

## 完整请求示例

```bash
curl -X POST https://api.heygen.com/v2/video/generate \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "video_inputs": [{
      "character": {
        "type": "avatar",
        "avatar_id": "Angela-inblackskirt-20220820"
      },
      "voice": {
        "type": "text",
        "input_text": "This is a customized video with green background.",
        "voice_id": "1bd001e7e50f421d891986aad5158bc8"
      }
    }],
    "dimension": {
      "width": 1920,
      "height": 1080
    },
    "aspect_ratio": "16:9",
    "background": {
      "type": "color",
      "value": "#00FF00"
    },
    "caption": {
      "enabled": true,
      "position": "bottom",
      "font_size": 28,
      "font_color": "#FFFFFF",
      "background_color": "#000000"
    },
    "test": false
  }'
```

---

## 最佳实践

### 1. 背景选择
- **纯色背景** - 适合品牌色、抠图后期
- **透明背景** - 用于 Remotion/Premiere 合成
- **图片背景** - 产品展示、场景化内容
- **视频背景** - 高级定制（需额外配额）

### 2. 分辨率建议
| 平台 | 推荐分辨率 | 画面比例 |
|------|------------|----------|
| YouTube | 1920x1080 | 16:9 |
| TikTok/Shorts | 1080x1920 | 9:16 |
| Instagram Feed | 1080x1080 | 1:1 |
| LinkedIn | 1280x720 | 16:9 |

### 3. 字幕策略
- **教程类** - 启用字幕，提升可访问性
- **营销类** - 可选，避免遮挡产品
- **多语言** - 结合翻译功能扩展受众

---

## 下一步

- [背景配置详解](backgrounds.md)
- [分辨率配置详解](dimensions.md)
- [字幕配置详解](captions.md)
- [高级功能](../03-advanced/README.md)

---

## 参考资源

- [HeyGen 视频定制文档](https://docs.heygen.com/reference/video-customization)
- [API 速查表](../99-cheatsheet.md)
