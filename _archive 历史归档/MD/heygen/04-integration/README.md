# 集成方案

> HeyGen 与其他工具/平台的集成模式 - 重点：Remotion + HeyGen

---

## 概览

HeyGen 的真正价值在于与其他工具结合，形成完整的视频生产流水线：

- **Remotion + HeyGen** ⭐ - 数字人 + 动态背景/图表
- **Webhook 回调** - 自动化工作流触发
- **批量生产模式** - CI/CD 集成

---

## 集成模式对比

| 集成方式 | 技术栈 | 适用场景 | 文档 |
|----------|--------|----------|------|
| **Remotion + HeyGen** | React + API | 技术教程、数据可视化 | [remotion-heygen.md](remotion-heygen.md) |
| **Webhook 回调** | HTTP Endpoint | 自动化流程、通知系统 | [webhooks.md](webhooks.md) |
| **批量生产** | CI/CD + Scripts | 规模化内容生产 | [workflow-patterns.md](workflow-patterns.md) |

---

## 章节导航

### [remotion-heygen.md](remotion-heygen.md) ⭐ - Remotion + HeyGen 组合

**核心能力**:
- HeyGen 生成数字人（透明背景）
- Remotion 构建动态背景/图表
- 两者叠加合成最终视频

**典型场景**:
1. **技术教程** - 数字人讲解 + 代码动画
2. **数据报告** - 数字人解读 + 图表变化
3. **产品演示** - 数字人介绍 + 产品动画

**工作流**:
```
1. HeyGen API 生成数字人视频 (transparent WebM)
2. 保存 video_id，异步等待完成
3. Remotion 构建背景动画/图表
4. 轮询 HeyGen 状态 → completed
5. 下载视频到本地
6. Remotion 用 OffthreadVideo 集成数字人
7. 渲染最终视频
```

**代码示例**:
```tsx
// Remotion Composition
import { OffthreadVideo } from "remotion";

export const VideoWithAvatar = () => (
  <AbsoluteFill>
    {/* 背景层：动态图表 */}
    <AnimatedChart data={chartData} />

    {/* 前景层：HeyGen 数字人 */}
    <OffthreadVideo
      src="/heygen-avatar.webm"
      transparent
    />
  </AbsoluteFill>
);
```

---

### [webhooks.md](webhooks.md) - Webhook 事件处理

**核心能力**:
- 视频生成完成自动通知
- 无需轮询，减少 API 调用
- 集成到现有工作流

**事件类型**:
- `video.completed` - 视频生成完成
- `video.failed` - 视频生成失败
- `avatar.ready` - 照片数字人训练完成

**配置示例**:
```json
{
  "webhook_url": "https://yourdomain.com/heygen-webhook",
  "events": ["video.completed", "video.failed"]
}
```

**接收处理**:
```javascript
// Express.js 示例
app.post('/heygen-webhook', (req, res) => {
  const { event, data } = req.body;

  if (event === 'video.completed') {
    const { video_id, video_url } = data;
    // 下载视频、推送通知等
  }

  res.status(200).send('OK');
});
```

---

### [workflow-patterns.md](workflow-patterns.md) - 自动化工作流模式

**场景 1: 每日新闻播报**
```
1. 定时任务获取新闻内容 (Cron)
2. 调用 HeyGen API 生成视频
3. Webhook 回调下载视频
4. 自动上传到 YouTube/社交媒体
```

**场景 2: 批量产品介绍**
```
1. 读取产品数据库 (CSV/API)
2. 遍历每个 SKU
3. 并发调用 HeyGen API (限流)
4. 收集所有视频 URL
5. 生成索引页面
```

**场景 3: Remotion + HeyGen 自动化**
```
1. HeyGen 生成数字人（透明背景）
2. Webhook 触发 Remotion 渲染
3. Remotion 下载数字人视频
4. Remotion 合成最终视频
5. 输出到指定目录
```

**技术栈**:
- **任务调度**: GitHub Actions / Cron / Airflow
- **并发控制**: p-limit / Bull Queue
- **错误重试**: exponential backoff
- **监控告警**: Sentry / Datadog

---

## Remotion + HeyGen 深度指南

### 为什么结合使用？

| 工具 | 擅长 | 不擅长 |
|------|------|--------|
| **HeyGen** | 数字人形象、语音合成 | 动画、图表、时序控制 |
| **Remotion** | 动画、图表、代码驱动 | 真人形象、语音生成 |

**组合效果**: 1 + 1 > 2

---

### 技术要点

#### 1. 透明背景配置

HeyGen 生成透明背景 WebM：
```json
{
  "background": {
    "type": "transparent"
  }
}
```

#### 2. 尺寸匹配

确保 HeyGen 和 Remotion 使用相同分辨率：
```tsx
// Remotion config
export const MyComp = () => (
  <Composition
    width={1920}
    height={1080}  // 与 HeyGen dimension 匹配
    fps={30}
  />
);
```

#### 3. 视频下载与集成

```bash
# 下载 HeyGen 视频
wget https://resource.heygen.ai/videos/abc123.webm -O public/avatar.webm
```

```tsx
// Remotion 中使用
<OffthreadVideo src={staticFile("avatar.webm")} transparent />
```

#### 4. 时序同步

```tsx
// 根据视频时长动态调整
const avatarDuration = 10; // 秒
const totalDuration = avatarDuration * fps;

<Sequence from={0} durationInFrames={totalDuration}>
  <OffthreadVideo src={avatarUrl} transparent />
</Sequence>
```

---

## 完整示例项目

### 场景：技术教程视频

**需求**:
- 数字人讲解 React Hooks
- 背景显示代码动画
- 图表展示性能对比

**实现**:

**1. HeyGen 生成数字人**
```bash
curl -X POST https://api.heygen.com/v2/video/generate \
  -d '{
    "video_inputs": [{
      "character": {"avatar_id": "Josh"},
      "voice": {
        "input_text": "Let me explain React Hooks...",
        "voice_id": "en_male_1"
      }
    }],
    "background": {"type": "transparent"}
  }'
```

**2. Remotion 构建背景**
```tsx
export const TutorialVideo = () => (
  <AbsoluteFill>
    {/* 背景：代码编辑器动画 */}
    <CodeEditor code={reactHooksCode} />

    {/* 图表：性能对比 */}
    <PerformanceChart data={benchmarkData} />

    {/* 数字人：HeyGen 生成 */}
    <OffthreadVideo
      src={staticFile("heygen-avatar.webm")}
      transparent
      style={{ position: "absolute", right: 0, bottom: 0 }}
    />
  </AbsoluteFill>
);
```

**3. 渲染最终视频**
```bash
npx remotion render src/index.ts TutorialVideo output.mp4
```

---

## 最佳实践

### 1. 异步生成策略
- HeyGen 视频生成需 5-10 分钟
- 先触发 HeyGen API，继续开发 Remotion
- 使用 Webhook 或轮询获取结果

### 2. 缓存机制
- 缓存已生成的数字人视频
- 避免重复调用 HeyGen API
- 版本化管理（`avatar_v1.webm`, `avatar_v2.webm`）

### 3. 本地开发流程
```bash
# 1. 生成数字人（一次性）
npm run generate-avatar

# 2. 开发 Remotion（实时预览）
npm run remotion-dev

# 3. 最终渲染
npm run render-final
```

---

## 下一步

- [Remotion + HeyGen 详细教程](remotion-heygen.md)
- [Webhook 配置指南](webhooks.md)
- [自动化工作流示例](workflow-patterns.md)
- [实验记录](../05-experiments/README.md)

---

## 参考资源

- [HeyGen API 文档](https://docs.heygen.com/reference/overview)
- [Remotion 官方文档](https://www.remotion.dev/docs)
- [HeyGen Skills - Remotion 集成](https://github.com/heygen-com/skills/blob/main/remotion-integration.md)
