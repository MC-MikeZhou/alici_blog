# 核心 API 参考

> HeyGen API 基础功能 - 认证、形象、语音、视频生成

---

## 概览

HeyGen API 采用 **RESTful** 架构，所有请求需通过 API Key 认证。核心流程分为三步：

1. **配置数字人** - 选择形象 (Avatar)
2. **配置语音** - 设置文本/音频 + 语音 ID
3. **生成视频** - 提交请求，轮询状态，获取结果

---

## 认证

### API Key 配置

所有请求需在 Header 中包含：

```bash
X-Api-Key: YOUR_API_KEY
Content-Type: application/json
```

### 获取 API Key

1. 登录 [HeyGen Dashboard](https://app.heygen.com/)
2. 进入 **Settings** > **API Keys**
3. 点击 **Generate New Key**
4. 复制 API Key（仅显示一次）

### 环境变量设置

```bash
# macOS/Linux
export HEYGEN_API_KEY="your_key_here"

# Windows PowerShell
$env:HEYGEN_API_KEY="your_key_here"
```

---

## Base URL

所有 API 请求的基础地址：

```
https://api.heygen.com
```

**版本**:
- `/v1/*` - 旧版 API（状态查询）
- `/v2/*` - 新版 API（视频生成、资源列表）

---

## 核心 API 列表

| Endpoint | 方法 | 功能 | 文档 |
|----------|------|------|------|
| `/v2/video/generate` | POST | 生成视频 | [video-generation.md](video-generation.md) |
| `/v1/video_status.get` | GET | 查询状态 | [video-generation.md](video-generation.md) |
| `/v2/avatars.list` | GET | 获取形象列表 | [avatars.md](avatars.md) |
| `/v2/voices.list` | GET | 获取语音列表 | [voices.md](voices.md) |

---

## 错误处理

### 响应结构

**成功响应**
```json
{
  "code": 100,
  "data": { ... },
  "message": "Success"
}
```

**错误响应**
```json
{
  "code": 400,
  "message": "Invalid avatar_id",
  "details": "Avatar 'xxx' not found"
}
```

### 常见错误码

| code | HTTP | 说明 | 解决方法 |
|------|------|------|----------|
| 100 | 200 | 成功 | - |
| 400 | 400 | 参数错误 | 检查 JSON 格式与必填字段 |
| 401 | 401 | 认证失败 | 检查 API Key 有效性 |
| 403 | 403 | 配额不足 | 升级套餐或联系支持 |
| 404 | 404 | 资源不存在 | 检查 ID 正确性 |
| 429 | 429 | 请求频率超限 | 降低请求频率 |
| 500 | 500 | 服务器错误 | 稍后重试或联系支持 |

---

## 请求限制

### 频率限制

| 套餐 | 请求频率 | 并发视频 |
|------|----------|----------|
| 免费版 | 10 req/min | 1 |
| 企业版 | 100 req/min | 5 |
| 定制版 | 按需调整 | 按需调整 |

**超限响应**:
```json
{
  "code": 429,
  "message": "Rate limit exceeded",
  "retry_after": 60
}
```

### 视频长度限制

| 套餐 | 单视频时长 | 月总时长 |
|------|------------|----------|
| 免费版 | 1 分钟 | 10 分钟 |
| 企业版 | 5 分钟 | 500 分钟 |

---

## 典型请求流程

### 1. 生成视频

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

**响应**:
```json
{
  "code": 100,
  "data": {
    "video_id": "abc123"
  }
}
```

### 2. 轮询状态

```bash
curl -X GET "https://api.heygen.com/v1/video_status.get?video_id=abc123" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

**响应（完成）**:
```json
{
  "code": 100,
  "data": {
    "video_id": "abc123",
    "status": "completed",
    "video_url": "https://resource.heygen.ai/videos/abc123.mp4",
    "duration": 3.5
  }
}
```

### 3. 下载视频

```bash
wget https://resource.heygen.ai/videos/abc123.mp4
```

---

## 章节导航

### [avatars.md](avatars.md) - 形象配置
- 公共形象库
- 自定义数字人
- 即时形象（Photo Avatar）
- 形象样式选项

### [voices.md](voices.md) - 语音配置
- TTS 语音库
- 多语言支持
- 语速/音调控制
- SSML 停顿标记
- 自定义音频上传

### [video-generation.md](video-generation.md) - 视频生成
- `/v2/video/generate` 完整参数
- 状态轮询策略
- 批量生成模式
- Webhook 回调

---

## 下一步

- [快速入门](../00-quick-start.md) - 快速上手
- [自定义配置](../02-customization/README.md) - 背景、字幕、分辨率
- [API 速查表](../99-cheatsheet.md) - 常用命令

---

## 参考资源

- [HeyGen 官方文档](https://docs.heygen.com/reference/overview)
- [API 状态页](https://status.heygen.com/)
