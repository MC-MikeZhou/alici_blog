# 高级功能

> 模板、照片数字人、流式交互、视频翻译等企业级功能

---

## 概览

HeyGen 高级功能超越基础视频生成，提供：

- **模板化生产** - 批量生成相似视频
- **照片数字人** - 静态照片转动态形象
- **实时流式数字人** - WebRTC 交互式对话
- **视频翻译** - 一键多语言配音

---

## 功能对比

| 功能 | 适用场景 | 技术要求 | 文档 |
|------|----------|----------|------|
| **模板生成** | 批量内容生产 | 低 | [templates.md](templates.md) |
| **照片数字人** | 品牌代言人、虚拟主播 | 中 | [photo-avatars.md](photo-avatars.md) |
| **流式数字人** | 实时客服、虚拟助手 | 高 | [streaming.md](streaming.md) |
| **视频翻译** | 多语言内容分发 | 低 | [translation.md](translation.md) |

---

## 章节导航

### [templates.md](templates.md) - 模板化生成

**核心能力**:
- 预设视频模板
- 变量替换生成
- 批量生产流程

**使用场景**:
- 房产介绍视频（批量楼盘）
- 产品推广（批量 SKU）
- 新闻播报（每日更新）

**示例**:
```json
{
  "template_id": "news_template_v1",
  "variables": {
    "title": "{{news_title}}",
    "content": "{{news_content}}"
  }
}
```

---

### [photo-avatars.md](photo-avatars.md) - 照片生成数字人

**核心能力**:
- 上传静态照片
- 生成动态数字人
- 保留人物特征

**使用场景**:
- 品牌创始人虚拟代言
- 企业内部培训讲师
- 虚拟主播/网红

**流程**:
1. 上传高清正面照
2. AI 训练生成模型（2-3 小时）
3. 获得专属 `avatar_id`
4. 正常调用视频生成 API

**要求**:
- 照片分辨率 ≥ 500x500
- 正面清晰人像
- 无遮挡、无墨镜

---

### [streaming.md](streaming.md) - 实时流式数字人

**核心能力**:
- WebRTC 实时流
- 低延迟对话（< 1 秒）
- 支持语音打断

**使用场景**:
- 智能客服（7x24 小时）
- 虚拟助手（语音交互）
- 在线教育（一对一辅导）

**技术架构**:
```
用户语音 → WebRTC → HeyGen API → TTS → 数字人动画 → WebRTC → 用户
```

**与普通视频生成的区别**:
| 维度 | 视频生成 | 流式数字人 |
|------|----------|------------|
| 延迟 | 5-10 分钟 | < 1 秒 |
| 交互 | 单向 | 双向对话 |
| 技术 | REST API | WebRTC |
| 成本 | 按视频数 | 按分钟数 |

---

### [translation.md](translation.md) - 视频翻译/配音

**核心能力**:
- 自动语音识别（ASR）
- 文本翻译
- 多语言配音
- 口型同步

**使用场景**:
- 全球市场内容分发
- 多语言培训课程
- 国际营销活动

**支持语言**:
- 英语、中文、西班牙语、法语、德语、日语、韩语等 40+ 语言

**示例**:
```json
{
  "video_id": "original_video_abc123",
  "target_languages": ["es", "fr", "de"],
  "keep_original_voice": false
}
```

**输出**:
- 西班牙语版本（口型匹配）
- 法语版本
- 德语版本

---

## 企业版功能对比

| 功能 | 免费版 | 企业版 | 定制版 |
|------|--------|--------|--------|
| 视频生成 | ✅ | ✅ | ✅ |
| 模板生成 | ❌ | ✅ | ✅ |
| 照片数字人 | ❌ | ✅ (1 个) | ✅ (无限) |
| 流式数字人 | ❌ | ❌ | ✅ |
| 视频翻译 | ❌ | ✅ | ✅ |
| API 调用频率 | 10/min | 100/min | 按需 |

---

## 使用建议

### 何时使用模板？
- 需要生成 10+ 条相似视频
- 内容结构固定，仅变量不同
- 追求生产效率

### 何时使用照片数字人？
- 需要品牌特定形象
- 公共形象库无法满足需求
- 有高质量人像照片

### 何时使用流式数字人？
- 需要实时交互
- 延迟敏感场景（客服）
- 有 WebRTC 开发能力

### 何时使用视频翻译？
- 已有英文视频素材
- 需要快速扩展多语言版本
- 预算有限（相比重新拍摄）

---

## 完整工作流示例

### 场景：多语言产品介绍视频

**Step 1: 创建照片数字人**
```bash
# 上传创始人照片
curl -X POST https://api.heygen.com/v2/photo_avatar/create \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -F "photo=@founder.jpg"
```

**Step 2: 生成英文原版**
```bash
# 使用照片数字人生成视频
curl -X POST https://api.heygen.com/v2/video/generate \
  -d '{
    "video_inputs": [{
      "character": {"type": "avatar", "avatar_id": "photo_avatar_123"},
      "voice": {"type": "text", "input_text": "Our product solves..."}
    }]
  }'
```

**Step 3: 翻译为多语言**
```bash
# 一键生成中文、西班牙语版本
curl -X POST https://api.heygen.com/v2/video/translate \
  -d '{
    "video_id": "original_video_id",
    "target_languages": ["zh", "es"]
  }'
```

**输出**:
- 英文原版（创始人形象）
- 中文配音版（口型同步）
- 西班牙语配音版

---

## 下一步

- [集成方案](../04-integration/README.md) - Remotion + HeyGen
- [实验记录](../05-experiments/README.md) - 实际应用案例

---

## 参考资源

- [HeyGen 高级功能文档](https://docs.heygen.com/reference/advanced-features)
- [Streaming Avatar SDK](https://github.com/heygen-com/StreamingAvatarSDK)
