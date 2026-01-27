# HeyGen API 速查表

> 常用 API Endpoints、curl 命令与错误码快速参考

---

## 认证

**Header 格式**
```bash
-H "X-Api-Key: YOUR_API_KEY"
-H "Content-Type: application/json"
```

**环境变量**
```bash
export HEYGEN_API_KEY="your_key_here"
```

---

## 核心 Endpoints

### 视频生成

**POST /v2/video/generate**
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
        "input_text": "Hello world",
        "voice_id": "1bd001e7e50f421d891986aad5158bc8"
      }
    }]
  }'
```

### 查询视频状态

**GET /v1/video_status.get**
```bash
curl -X GET "https://api.heygen.com/v1/video_status.get?video_id=VIDEO_ID" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

### 获取形象列表

**GET /v2/avatars.list**
```bash
curl -X GET https://api.heygen.com/v2/avatars.list \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

### 获取语音列表

**GET /v2/voices.list**
```bash
curl -X GET https://api.heygen.com/v2/voices.list \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

---

## 常用视频配置

### 横屏 1080p
```json
{
  "dimension": {"width": 1920, "height": 1080},
  "aspect_ratio": "16:9"
}
```

### 竖屏（短视频）
```json
{
  "dimension": {"width": 1080, "height": 1920},
  "aspect_ratio": "9:16"
}
```

### 方形（社交媒体）
```json
{
  "dimension": {"width": 1080, "height": 1080},
  "aspect_ratio": "1:1"
}
```

---

## 常用形象 ID

| 形象 | ID | 风格 |
|------|-----|------|
| Angela (黑裙) | `Angela-inblackskirt-20220820` | 职业女性 |
| Josh (休闲) | `josh_lite3_20230714` | 休闲男性 |
| Monica (正装) | `Monica-incasualsuit-20220818` | 商务女性 |

**获取完整列表**: `/v2/avatars.list` API

---

## 常用语音 ID

| 语言 | 音色 | ID |
|------|------|-----|
| 英文 | 女声 (美音) | `1bd001e7e50f421d891986aad5158bc8` |
| 英文 | 男声 (美音) | `2d5b0e6cf36f4a3eae5810c04ba805cf` |
| 中文 | 女声 (普通话) | `b6a18b8576a54e0e9f6a5a1b0c3d7e8f` |

**获取完整列表**: `/v2/voices.list` API

---

## 背景配置

### 纯色背景
```json
{
  "background": {
    "type": "color",
    "value": "#00FF00"
  }
}
```

### 图片背景
```json
{
  "background": {
    "type": "image",
    "url": "https://example.com/background.jpg"
  }
}
```

### 透明背景（用于 Remotion 集成）
```json
{
  "background": {
    "type": "transparent"
  }
}
```

---

## 语音控制

### 基础 TTS
```json
{
  "voice": {
    "type": "text",
    "input_text": "Hello world",
    "voice_id": "1bd001e7e50f421d891986aad5158bc8"
  }
}
```

### 语速控制
```json
{
  "voice": {
    "type": "text",
    "input_text": "Faster speech",
    "voice_id": "1bd001e7e50f421d891986aad5158bc8",
    "speed": 1.2
  }
}
```

### SSML 停顿
```json
{
  "voice": {
    "type": "text",
    "input_text": "Hello <break time='1s'/> world",
    "voice_id": "1bd001e7e50f421d891986aad5158bc8"
  }
}
```

---

## 字幕配置

### 启用自动字幕
```json
{
  "caption": true
}
```

### 自定义字幕样式
```json
{
  "caption": {
    "enabled": true,
    "position": "bottom",
    "font_size": 24,
    "font_color": "#FFFFFF",
    "background_color": "#000000"
  }
}
```

---

## 状态码

### 视频状态
| 状态 | 说明 | 操作 |
|------|------|------|
| `pending` | 排队中 | 继续轮询 |
| `processing` | 生成中 | 继续轮询 |
| `completed` | 完成 | 获取 URL |
| `failed` | 失败 | 查看错误信息 |

### HTTP 状态码
| 状态码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | API Key 无效 |
| 429 | 请求频率超限 |
| 500 | 服务器错误 |

---

## 错误码

| code | 说明 | 解决方法 |
|------|------|----------|
| 100 | 成功 | - |
| 400 | 参数错误 | 检查 JSON 格式 |
| 401 | 未授权 | 检查 API Key |
| 403 | 配额不足 | 升级套餐 |
| 404 | 资源不存在 | 检查 ID 正确性 |
| 500 | 服务器错误 | 稍后重试 |

---

## 完整生成示例

```bash
#!/bin/bash

# 生成带自定义背景和字幕的视频
curl -X POST https://api.heygen.com/v2/video/generate \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "video_inputs": [{
      "character": {
        "type": "avatar",
        "avatar_id": "Angela-inblackskirt-20220820",
        "avatar_style": "normal"
      },
      "voice": {
        "type": "text",
        "input_text": "Welcome to HeyGen! <break time=\"1s\"/> Let me show you how easy it is to create AI videos.",
        "voice_id": "1bd001e7e50f421d891986aad5158bc8",
        "speed": 1.0
      },
      "background": {
        "type": "color",
        "value": "#E8F5E9"
      }
    }],
    "dimension": {
      "width": 1920,
      "height": 1080
    },
    "aspect_ratio": "16:9",
    "caption": true,
    "test": false
  }'
```

---

## 轮询脚本模板

```bash
#!/bin/bash

VIDEO_ID="$1"  # 传入 video_id

while true; do
  RESPONSE=$(curl -s -X GET "https://api.heygen.com/v1/video_status.get?video_id=$VIDEO_ID" \
    -H "X-Api-Key: $HEYGEN_API_KEY")

  STATUS=$(echo $RESPONSE | jq -r '.data.status')

  case $STATUS in
    "completed")
      echo "✅ Video completed!"
      echo $RESPONSE | jq -r '.data.video_url'
      break
      ;;
    "failed")
      echo "❌ Video generation failed!"
      echo $RESPONSE | jq -r '.data.error'
      break
      ;;
    *)
      echo "⏳ Status: $STATUS"
      sleep 10
      ;;
  esac
done
```

**使用方法**
```bash
./poll-video.sh abc123def456
```

---

## 参考链接

- [HeyGen API 文档](https://docs.heygen.com/reference/overview)
- [快速入门指南](00-quick-start.md)
- [核心 API 参考](01-core-api/README.md)
- [Remotion 集成](04-integration/remotion-heygen.md)
