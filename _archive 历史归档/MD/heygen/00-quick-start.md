# HeyGen 快速入门

> 10 分钟完成环境配置 + 生成第一个数字人视频

---

## 前置要求

- HeyGen 账号（[注册地址](https://app.heygen.com/)）
- API Key（企业版功能）
- curl 或支持 HTTP 的编程语言

---

## Step 1: 获取 API Key

### 1.1 登录 HeyGen Dashboard
访问 [HeyGen](https://app.heygen.com/) 并登录账号。

### 1.2 获取 API Key
1. 进入 **Settings** > **API Keys**
2. 点击 **Generate New Key**
3. 复制生成的 API Key（格式如 `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`）

### 1.3 配置环境变量

**macOS/Linux**
```bash
export HEYGEN_API_KEY="your_api_key_here"
```

**Windows (PowerShell)**
```powershell
$env:HEYGEN_API_KEY="your_api_key_here"
```

**验证配置**
```bash
echo $HEYGEN_API_KEY  # 应输出你的 API Key
```

---

## Step 2: 生成第一个视频

### 2.1 基础视频生成请求

**curl 示例**
```bash
curl -X POST https://api.heygen.com/v2/video/generate \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "video_inputs": [
      {
        "character": {
          "type": "avatar",
          "avatar_id": "Angela-inblackskirt-20220820",
          "avatar_style": "normal"
        },
        "voice": {
          "type": "text",
          "input_text": "Hello! This is my first HeyGen video.",
          "voice_id": "1bd001e7e50f421d891986aad5158bc8"
        }
      }
    ],
    "dimension": {
      "width": 1920,
      "height": 1080
    },
    "aspect_ratio": "16:9"
  }'
```

### 2.2 理解请求参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `avatar_id` | 数字人形象 ID | `Angela-inblackskirt-20220820` |
| `input_text` | 语音文本内容 | 任意文本 |
| `voice_id` | 语音 ID（语言+音色） | `1bd001e7...`（英文女声） |
| `dimension` | 视频分辨率 | 1920x1080 |
| `aspect_ratio` | 画面比例 | `16:9` / `9:16` / `1:1` |

### 2.3 响应示例

**成功响应**
```json
{
  "code": 100,
  "data": {
    "video_id": "abc123def456"
  },
  "message": "Success"
}
```

**保存 `video_id`** - 用于后续查询视频状态。

---

## Step 3: 轮询视频状态

### 3.1 查询生成进度

```bash
curl -X GET "https://api.heygen.com/v1/video_status.get?video_id=abc123def456" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

### 3.2 状态类型

| 状态 | 说明 | 操作 |
|------|------|------|
| `pending` | 排队中 | 继续轮询 |
| `processing` | 生成中 | 继续轮询 |
| `completed` | 完成 | 获取视频 URL |
| `failed` | 失败 | 查看 `error` 字段 |

### 3.3 完成响应示例

```json
{
  "code": 100,
  "data": {
    "video_id": "abc123def456",
    "status": "completed",
    "video_url": "https://resource.heygen.ai/videos/abc123def456.mp4",
    "thumbnail_url": "https://resource.heygen.ai/thumbnails/abc123def456.jpg",
    "duration": 5.2
  }
}
```

### 3.4 下载视频

```bash
wget https://resource.heygen.ai/videos/abc123def456.mp4
```

---

## Step 4: 完整自动化脚本

### Bash 脚本示例

```bash
#!/bin/bash

# 1. 生成视频
VIDEO_ID=$(curl -s -X POST https://api.heygen.com/v2/video/generate \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "video_inputs": [
      {
        "character": {
          "type": "avatar",
          "avatar_id": "Angela-inblackskirt-20220820"
        },
        "voice": {
          "type": "text",
          "input_text": "This is an automated test video.",
          "voice_id": "1bd001e7e50f421d891986aad5158bc8"
        }
      }
    ]
  }' | jq -r '.data.video_id')

echo "Video ID: $VIDEO_ID"

# 2. 轮询状态
while true; do
  STATUS=$(curl -s -X GET "https://api.heygen.com/v1/video_status.get?video_id=$VIDEO_ID" \
    -H "X-Api-Key: $HEYGEN_API_KEY" | jq -r '.data.status')

  echo "Status: $STATUS"

  if [ "$STATUS" = "completed" ]; then
    VIDEO_URL=$(curl -s -X GET "https://api.heygen.com/v1/video_status.get?video_id=$VIDEO_ID" \
      -H "X-Api-Key: $HEYGEN_API_KEY" | jq -r '.data.video_url')
    echo "Video URL: $VIDEO_URL"
    wget -O output.mp4 "$VIDEO_URL"
    break
  elif [ "$STATUS" = "failed" ]; then
    echo "Video generation failed!"
    break
  fi

  sleep 10
done
```

---

## 常见问题

### Q1: API Key 无效
**错误**: `401 Unauthorized`

**解决**:
1. 检查 API Key 是否正确复制
2. 确认账号已升级到企业版
3. 验证 Header 格式: `X-Api-Key: xxx`

### Q2: 视频生成时间
**平均时长**: 5-10 分钟（取决于视频长度和队列）

**加速**:
- 使用简短文本测试
- 避免高峰期生成

### Q3: 形象/语音 ID 从哪获取？
查看:
- [01-core-api/avatars.md](01-core-api/avatars.md) - 形象 ID 列表
- [01-core-api/voices.md](01-core-api/voices.md) - 语音 ID 列表
- 或使用 `/v2/avatars.list` API 动态查询

---

## 下一步

- [核心 API 参考](01-core-api/README.md) - 完整 API 功能
- [自定义配置](02-customization/README.md) - 背景、字幕、分辨率
- [Remotion 集成](04-integration/remotion-heygen.md) - 与 Remotion 结合使用

---

## 相关资源

- [HeyGen API 文档](https://docs.heygen.com/reference/overview)
- [API 速查表](99-cheatsheet.md)
