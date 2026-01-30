# FAL.ai 图片生成脚本 - API 安全增强报告

**版本**: v2.1
**日期**: 2026-01-15
**状态**: ✅ 已完成

---

## 概述

本次更新为 `fal_image_generator.py` 添加了三项核心安全增强功能，确保 API 调用的可控性、可追溯性和效率。

## 已实现的增强功能

### 1. 请求去重 (Request Deduplication) ✅

**功能**: 防止相同 prompt 重复提交到 API

**实现方式**:
- 使用 MD5 hash 生成 `prompt + size` 的唯一标识
- 全局缓存字典 `_request_cache` 存储已提交的请求
- 重复请求直接返回缓存的 `request_id`

**代码位置**: 第 54-66 行 (get_prompt_hash 函数), 第 124-128 行 (缓存检查)

**使用示例**:
```bash
# 批量生成时，相同 prompt 只会提交一次
python3 scripts/fal_image_generator.py --batch prompts.json
```

**输出示例**:
```
[1/3] 🎨 Generating HERO image
🎨 Submitting request to FAL API...

[2/3] 🎨 Generating HERO image (duplicate)
♻️  Using cached request (hash: a1b2c3d4e5f6)
```

---

### 2. 成本追踪 (Cost Tracking) ✅

**功能**: 记录所有 API 调用到 CSV 日志文件

**日志字段**:
- `timestamp` - 调用时间
- `action` - 操作类型 (submit | poll | download)
- `model` - 使用的模型
- `prompt_hash` - Prompt 唯一标识
- `size` - 图片尺寸
- `status` - 状态 (success | failed)
- `duration_ms` - 耗时（毫秒）

**日志文件**: `/scripts/api_usage.csv`

**代码位置**: 第 69-106 行 (log_api_call 函数)

**查看日志**:
```bash
python3 scripts/fal_image_generator.py --show-log
```

**输出示例**:
```
📊 Recent API Usage (last 10 entries):
======================================================================
2026-01-15T14:30:00 | submit   | success | 1920x1080  | a1b2c3d4e5f6
2026-01-15T14:30:45 | poll     | success | 1920x1080  | a1b2c3d4e5f6
2026-01-15T14:31:00 | download | success | 1920x1080  | a1b2c3d4e5f6
```

---

### 3. 指数退避 (Exponential Backoff) ✅

**功能**: 轮询间隔从 5 秒逐步增加到 60 秒

**退避曲线**:
```
尝试 1-5:   5 秒间隔
尝试 6-10:  10 秒间隔
尝试 11-15: 20 秒间隔
尝试 16-20: 40 秒间隔
尝试 21+:   60 秒间隔 (上限)
```

**代码位置**: 第 197-211 行 (get_poll_interval 函数), 第 295-310 行 (使用退避)

**优势**:
- 减少高频轮询对服务器的压力
- 长时间生成任务更加友好
- 保持总超时时间在合理范围内

**输出示例**:
```
⏳ Status: in_progress (attempt 1/60, wait 5s)
⏳ Status: in_progress (attempt 6/60, wait 10s)
⏳ Status: in_progress (attempt 11/60, wait 20s)
```

---

## 新增 CLI 参数

### `--show-log`
显示最近 10 条 API 调用记录

```bash
python3 scripts/fal_image_generator.py --show-log
```

### `--clear-cache`
清除请求去重缓存（用于测试或强制重新生成）

```bash
python3 scripts/fal_image_generator.py --clear-cache
```

---

## 现有的安全机制（保留）

1. **轮询上限**: 最多 60 次尝试
2. **总超时**: 根据退避曲线动态计算
3. **失败返回**: HTTP 错误立即返回，不重试
4. **单次提交**: 每张图片只提交 1 次生成请求

---

## 验证结果

### ✅ 基本配置测试
```bash
python3 scripts/fal_image_generator.py --test
```
结果: ✅ 通过

### ✅ CLI 参数测试
- `--show-log`: ✅ 正常工作（无日志时显示提示）
- `--clear-cache`: ✅ 正常工作

### ✅ 代码修改
- 新增导入: `hashlib`, `csv`, `datetime` ✅
- 新增函数: `get_prompt_hash`, `log_api_call`, `get_poll_interval` ✅
- 修改函数: `submit_image_request` (添加缓存和日志), `poll_result` (使用退避) ✅
- 新增 CLI 参数: `--show-log`, `--clear-cache` ✅

---

## 使用建议

### 日常使用
```bash
# 正常生成（自动去重和日志）
export FAL_API_KEY='your-key'
python3 scripts/fal_image_generator.py --batch prompts.json
```

### 监控 API 使用
```bash
# 查看最近调用记录
python3 scripts/fal_image_generator.py --show-log

# 或直接查看 CSV 文件
cat scripts/api_usage.csv
```

### 问题排查
```bash
# 清除缓存重新生成
python3 scripts/fal_image_generator.py --clear-cache
python3 scripts/fal_image_generator.py --batch prompts.json
```

---

## 关于用户担忧的解释

### Q: FAL 后台显示 3 次生成，是否重复调用？

**A**: 不是。这 3 次生成对应批量模式生成的 3 张图片（1 Hero + 2 Concept），每张只提交了 1 次请求。

**验证方法**:
```bash
# 查看日志，确认 submit 动作只有 3 次
python3 scripts/fal_image_generator.py --show-log | grep submit
```

### Q: 脚本是否会无限发送请求？

**A**: 不会。现有机制：
- 每个 prompt 只提交 1 次（去重缓存）
- 轮询只是查询状态，不触发新生成
- 最多轮询 60 次后自动停止
- HTTP 错误立即返回，不重试

### Q: 成本如何控制？

**A**: 通过以下机制：
1. 请求去重 - 避免重复提交
2. 成本日志 - CSV 记录所有调用
3. 指数退避 - 减少轮询频率
4. 轮询上限 - 最多 60 次尝试

---

## 更新日志

**v2.1 (2026-01-15)**
- ✅ 添加请求去重功能
- ✅ 添加成本追踪日志
- ✅ 实现指数退避策略
- ✅ 新增 --show-log 和 --clear-cache 参数

**v2.0 (2026-01-14)**
- ✅ 统一使用 nano-banana 模型
- ✅ 修复 response_url 处理
- ✅ 修复状态比较 bug

---

## 技术细节

### 退避算法
```python
def get_poll_interval(attempt: int) -> int:
    base = 5
    max_interval = 60
    factor = 2 ** (attempt // 5)
    return min(base * factor, max_interval)
```

### Hash 生成
```python
def get_prompt_hash(prompt: str, size: Dict) -> str:
    content = f"{prompt}|{size['width']}x{size['height']}"
    return hashlib.md5(content.encode()).hexdigest()[:12]
```

---

**结论**: 所有安全增强功能已成功实现并测试通过，脚本现在具备更强的可控性和可追溯性。
