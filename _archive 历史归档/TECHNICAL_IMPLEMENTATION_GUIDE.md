# AliciBlog 技术实现指南

> 面向开发者和技术决策者的深度技术文档

---

## 目录

1. [系统架构深度解析](#系统架构深度解析)
2. [当前技术栈分析](#当前技术栈分析)
3. [Phase 2 自动化脚本设计](#phase-2-自动化脚本设计)
4. [Phase 3 集成架构](#phase-3-集成架构)
5. [数据流与API设计](#数据流与api设计)
6. [部署与运维](#部署与运维)
7. [性能与成本优化](#性能与成本优化)
8. [技术债与改进方案](#技术债与改进方案)

---

## 系统架构深度解析

### 1.1 整体系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                      输入层 (Input Layer)                       │
│  ┌──────────────┬──────────────┬──────────────┐               │
│  │  Notion API  │  File System  │  Web Crawler │               │
│  │  (Links)     │  (txt files)  │  (URLs)      │               │
│  └──────────────┴──────────────┴──────────────┘               │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│              处理层 (Processing Layer)                          │
│  ┌──────────────────────────────────────────┐               │
│  │  内容类型识别与规范应用                    │               │
│  │  - News Handler                           │               │
│  │  - Tutorial Handler                       │               │
│  │  - List Handler                           │               │
│  └──────────────────────────────────────────┘               │
│  ┌──────────────────────────────────────────┐               │
│  │  AI 辅助内容生成 (Claude API)              │               │
│  │  - 中文初稿生成                          │               │
│  │  - 英文翻译与优化                        │               │
│  │  - SEO 元数据生成                        │               │
│  └──────────────────────────────────────────┘               │
│  ┌──────────────────────────────────────────┐               │
│  │  图片处理                                │               │
│  │  - FAL.ai API (图片生成)                 │               │
│  │  - Local Storage (临时存储)              │               │
│  │  - Cloud Upload (最终存储)               │               │
│  └──────────────────────────────────────────┘               │
│  ┌──────────────────────────────────────────┐               │
│  │  格式转换与验证                          │               │
│  │  - Markdown → HTML                       │               │
│  │  - JSON Schema 验证                      │               │
│  │  - SEO 标准检查                          │               │
│  └──────────────────────────────────────────┘               │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│               输出层 (Output Layer)                            │
│  ┌──────────────┬──────────────┬──────────────┐               │
│  │  JSON Array  │  HTML Preview│ Asset Files  │               │
│  │  (./output/) │  (./tmp/)    │  (./gen_*)   │               │
│  └──────────────┴──────────────┴──────────────┘               │
│                      │                                        │
│  ┌──────────────────▼──────────────────┐                     │
│  │  Framer CMS / 外部系统集成          │                     │
│  │  (Phase 3+)                        │                     │
│  └────────────────────────────────────┘                     │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 数据流向

```
素材输入
  │
  ├─→ Notion 链接抓取 (Notion API)
  ├─→ 本地文本读取 (File System)
  ├─→ 网页爬虫 (Web Scraper / Jina API)
  │
  └─→ 内容聚合与清理
      │
      ├─→ 识别内容类型
      ├─→ 应用相应规范
      │
      └─→ AI 内容生成
          │
          ├─→ 中文初稿
          │   ├─→ 规范检查
          │   ├─→ 用户审核
          │   └─→ 迭代修改
          │
          ├─→ 配图决策
          │   ├─→ 自动生成 (FAL.ai)
          │   ├─→ 本地存储
          │   └─→ 云端上传
          │
          └─→ 最终发布物生成
              ├─→ 英文翻译
              ├─→ SEO 优化
              ├─→ JSON 打包
              └─→ 质量检查

最终输出 → Framer CMS / 其他系统
```

### 1.3 关键组件职责

| 组件 | 职责 | 状态 | 优先级 |
|------|------|------|--------|
| **Notion Parser** | 解析 Notion 公开链接内容 | ✅ 已有 (AI驱动) | P1 |
| **File Manager** | 管理 input/tmp/output 目录 | ✅ 已有 | P1 |
| **Content Type Router** | 识别和路由不同内容类型 | ✅ 已有 (规范文档) | P1 |
| **AI Content Engine** | 调用 Claude API 生成内容 | ✅ 已有 (手工触发) | P1 |
| **Image Generator** | 调用 FAL.ai 生成配图 | ✅ 已有 (手工触发) | P2 |
| **Image Uploader** | 上传图片到云端 (SSH) | ⚠️ 手工命令 | P2 |
| **Format Converter** | Markdown/HTML 格式转换 | ✅ 已有 (AI驱动) | P2 |
| **JSON Validator** | JSON Schema 验证 | ❌ 无 | P3 |
| **SEO Checker** | 检查 SEO 标准 | ❌ 无 | P3 |
| **CMS Connector** | 与 Framer CMS 集成 | ❌ 无 | P4 |

---

## 当前技术栈分析

### 2.1 使用的外部服务

#### FAL.ai 图片生成 API

**端点：** `https://queue.fal.run/fal-ai/nano-banana`

**认证：**
```
Header: Authorization: Key ${API_KEY}
API_KEY: b5ea47d3-5d30-4423-b9c9-85a185752042:828167dcf4beacefd4df6b3b4d03e99f
```

**请求格式：**
```bash
curl --request POST \
  --url https://queue.fal.run/fal-ai/nano-banana \
  --header "Authorization: Key ${FAL_KEY}" \
  --header "Content-Type: application/json" \
  --data '{
     "prompt": "描述图片内容",
     "num_images": 1,
     "aspect_ratio": "16:9",
     "output_format": "png",
     "sync_mode": false
   }'
```

**响应：**
```json
{
  "request_id": "abc123...",
  "status": "pending"
}
```

**关键点：**
- ⚠️ 异步接口，需要轮询获取结果
- 支持的宽高比：见 `image_ratio.png`
- 推荐比例：16:9（横向）、2:1（更宽）
- 成本：每张约 $0.002-0.01

**改进建议（Phase 2）：**
```python
# 需要实现的轮询逻辑
def wait_for_image_generation(request_id, max_retries=30, interval=2):
    """轮询获取图片生成结果"""
    for attempt in range(max_retries):
        response = check_fal_status(request_id)
        if response['status'] == 'completed':
            return response['output']['images'][0]
        time.sleep(interval)
    raise TimeoutError(f"Image generation timeout after {max_retries * interval}s")
```

#### Notion API（实际上是网页爬虫）

**当前实现：** AI 通过浏览器访问公开链接，手工提取内容

**改进方向（Phase 2）：**
```python
# 使用官方 Notion API
from notion_client import Client

notion = Client(auth=NOTION_TOKEN)

def fetch_notion_page(page_id):
    """获取 Notion 页面内容"""
    page = notion.pages.retrieve(page_id)
    blocks = notion.blocks.children.list(page_id)
    return parse_blocks(blocks)
```

#### SSH/rsync 图片上传

**当前实现：** 手工执行 SSH 命令

**命令：**
```bash
rsync -a -r -v -p -e 'ssh -p 22' \
  --exclude='.DS_Store' \
  --progress ${项目路径}/gen_images \
  root@45.76.70.215:/var/www/static/static/image/other/
```

**服务器信息：**
- Host: `45.76.70.215`
- Port: `22`
- User: `root`
- Password: `5A_p@cjpX74H(LJM`
- 目标路径: `/var/www/static/static/image/other/`
- 访问URL: `https://ct2.alici.ai/static/image/other/gen_images/`

**安全隐患（需要改进）：**
- ❌ 密码硬编码在文档中
- ❌ root 用户权限过大
- ❌ 明文密码不安全
- ❌ 手工执行容易出错

**改进方案（Phase 2）：**
```python
import paramiko
from pathlib import Path

def upload_images_ssh(local_dir, remote_dir, ssh_config):
    """使用 SSH 密钥而非密码"""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(
        hostname=ssh_config['host'],
        port=ssh_config['port'],
        username=ssh_config['user'],
        key_filename=ssh_config['key_path']  # 使用密钥文件
    )

    sftp = ssh.open_sftp()
    for file in Path(local_dir).glob('*.png'):
        sftp.put(str(file), f"{remote_dir}/{file.name}")
    sftp.close()
```

### 2.2 文件系统结构

```
项目根目录 (blog_new_sam 11.20.2025)
│
├── doc/                          # 文档和规范
│   ├── readme.txt               # 主工作流文档
│   ├── 4_Tutorial类内容规范.md
│   ├── 5_List类内容规范.md
│   ├── 6_News类内容规范.md
│   ├── blog.json               # 输出示例
│   ├── blog.png                # 页面布局参考
│   └── image_ratio.png         # 图片比例规范
│
├── input/                        # 输入目录
│   └── *.txt                   # 用户上传的素材
│
├── tmp/                         # 临时工作目录
│   ├── chinese_preview.html    # 中文预览版
│   ├── tmp_*.json             # 中间处理文件
│   └── *.log                  # 日志文件
│
├── gen_images/                  # 生成的图片
│   ├── image_1.png
│   ├── image_2.png
│   └── ...
│
├── output/                       # 最终输出
│   └── [title]_[timestamp]_output.json
│
├── tmp_image.json              # 图片 URL 映射
│   └── { "image_1": "https://...", ... }
│
└── .gitignore                  # Git 配置
```

### 2.3 JSON 输出规范

**文件位置：** `./output/[title]_[timestamp]_output.json`

**完整字段列表：**

```json
{
  "Slug": "string (url-safe, lowercase, hyphens)",
  "title": "string (English, 60-70 chars)",
  "sub_title": "string (English, subtitle)",
  "TLNR": "string (50-100 chars summary)",

  "cover": {
    "url": "string (https link to cover image)"
  },

  "Date": "ISO 8601 format (YYYY-MM-DDTHH:mm:ss.000Z)",
  "read_time": "string (e.g., '8 min')",

  "main_category": "enum [news|tutorial|list]",
  "recommend_category": "string (comma-separated categories)",

  "article_body_content": "string (HTML format)",

  "CTA_alici_link": "string (URL, default: https://alici.ai)",
  "CTA button": "string (button text, default: 'Try It NOW')",

  "meta_title": "string (60 chars, SEO)",
  "meta_description": "string (155-160 chars, SEO)",
  "tag_for_SEO": "string (4-6 keywords, comma-separated)",

  "_metadata": {
    "generated_at": "ISO 8601 timestamp",
    "generator_version": "string",
    "source_materials": ["urls..."],
    "word_count": "number"
  }
}
```

**字段验证规则（需要实现）：**

```python
FIELD_RULES = {
    "Slug": {
        "type": "string",
        "pattern": r"^[a-z0-9\-]+$",
        "length": (20, 100),
        "required": True
    },
    "title": {
        "type": "string",
        "length": (30, 100),
        "required": True,
        "language": "english"
    },
    "TLNR": {
        "type": "string",
        "length": (50, 150),
        "required": True
    },
    "cover.url": {
        "type": "url",
        "required": True
    },
    "read_time": {
        "type": "string",
        "pattern": r"^\d+\s*min$",
        "required": True
    },
    "main_category": {
        "type": "enum",
        "values": ["news", "tutorial", "list"],
        "required": True
    },
    "article_body_content": {
        "type": "html",
        "length_min": 1200,
        "required": True
    },
    "meta_title": {
        "type": "string",
        "length": (30, 60),
        "required": True
    },
    "meta_description": {
        "type": "string",
        "length": (100, 160),
        "required": True
    },
    "tag_for_SEO": {
        "type": "string",
        "pattern": r"^([a-z\s]+,\s)*[a-z\s]+$",
        "item_count": (4, 6),
        "required": True
    }
}
```

---

## Phase 2 自动化脚本设计

### 3.1 核心自动化模块架构

```
python/
├── __init__.py
├── config.py                    # 配置管理
├── logger.py                   # 日志系统
├── models/
│   ├── __init__.py
│   ├── content.py             # 内容数据模型
│   └── blog.py                # Blog JSON 模型
├── services/
│   ├── __init__.py
│   ├── notion_parser.py       # Notion 内容解析
│   ├── file_manager.py        # 文件系统操作
│   ├── fal_client.py          # FAL.ai API 客户端
│   ├── ssh_uploader.py        # SSH 图片上传
│   ├── json_validator.py      # JSON 验证
│   └── seo_checker.py         # SEO 检查
├── pipelines/
│   ├── __init__.py
│   ├── content_pipeline.py    # 主流程
│   ├── image_pipeline.py      # 图片生成流程
│   └── validation_pipeline.py # 验证流程
├── utils/
│   ├── __init__.py
│   ├── text_utils.py
│   ├── html_utils.py
│   └── url_utils.py
└── main.py                    # CLI 入口
```

### 3.2 关键模块实现示例

#### 模块1：文件管理器

```python
# services/file_manager.py
from pathlib import Path
from typing import List
import json
from datetime import datetime

class FileManager:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.input_dir = base_dir / "input"
        self.tmp_dir = base_dir / "tmp"
        self.output_dir = base_dir / "output"
        self.gen_images_dir = base_dir / "gen_images"

        # 确保目录存在
        for d in [self.input_dir, self.tmp_dir, self.output_dir, self.gen_images_dir]:
            d.mkdir(parents=True, exist_ok=True)

    def read_input_materials(self) -> dict:
        """读取所有输入素材"""
        materials = {
            "text_files": [],
            "timestamps": []
        }

        for txt_file in self.input_dir.glob("*.txt"):
            try:
                with open(txt_file, 'r', encoding='utf-8') as f:
                    materials["text_files"].append({
                        "filename": txt_file.name,
                        "content": f.read()
                    })
                    materials["timestamps"].append(txt_file.stat().st_mtime)
            except Exception as e:
                logger.error(f"Failed to read {txt_file}: {e}")

        return materials

    def save_json_output(self, blog_data: dict, title: str) -> Path:
        """保存最终 JSON 输出"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{title}_{timestamp}_output.json"
        filepath = self.output_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(blog_data, f, ensure_ascii=False, indent=2)

        logger.info(f"Blog JSON saved to {filepath}")
        return filepath

    def clean_tmp_directory(self):
        """清空临时目录"""
        import shutil
        if self.tmp_dir.exists():
            shutil.rmtree(self.tmp_dir)
        self.tmp_dir.mkdir(parents=True, exist_ok=True)
        logger.info("Cleaned tmp directory")

    def save_image_mapping(self, mapping: dict):
        """保存图片 URL 映射"""
        filepath = self.base_dir / "tmp_image.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(mapping, f, ensure_ascii=False, indent=2)
        logger.info(f"Image mapping saved to {filepath}")
```

#### 模块2：FAL.ai 客户端

```python
# services/fal_client.py
import requests
import time
from typing import Optional, List
from dataclasses import dataclass

@dataclass
class GeneratedImage:
    url: str
    width: int
    height: int
    format: str

class FALClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://queue.fal.run"
        self.model = "fal-ai/nano-banana"
        self.headers = {
            "Authorization": f"Key {api_key}",
            "Content-Type": "application/json"
        }

    def generate_image(
        self,
        prompt: str,
        aspect_ratio: str = "16:9",
        num_images: int = 1,
        max_retries: int = 30,
        retry_interval: int = 2
    ) -> List[GeneratedImage]:
        """
        生成图片

        Args:
            prompt: 图片描述文本
            aspect_ratio: 宽高比 (e.g., "16:9", "2:1")
            num_images: 生成数量
            max_retries: 最大重试次数
            retry_interval: 重试间隔（秒）

        Returns:
            生成的图片列表
        """

        # Step 1: 提交生成请求
        payload = {
            "prompt": prompt,
            "num_images": num_images,
            "aspect_ratio": aspect_ratio,
            "output_format": "png",
            "sync_mode": False
        }

        try:
            response = requests.post(
                f"{self.base_url}/{self.model}",
                json=payload,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            request_id = response.json()["request_id"]
            logger.info(f"Image generation request submitted: {request_id}")
        except Exception as e:
            logger.error(f"Failed to submit image generation: {e}")
            raise

        # Step 2: 轮询获取结果
        for attempt in range(max_retries):
            try:
                result = self._check_status(request_id)

                if result["status"] == "completed":
                    images = []
                    for img_data in result["output"]["images"]:
                        images.append(GeneratedImage(
                            url=img_data["url"],
                            width=img_data["width"],
                            height=img_data["height"],
                            format=img_data.get("format", "png")
                        ))
                    logger.info(f"Image generation completed: {len(images)} images")
                    return images

                elif result["status"] == "failed":
                    raise Exception(f"Image generation failed: {result.get('error', 'Unknown error')}")

                # 状态为 pending，继续等待
                logger.info(f"Waiting for image generation... (attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_interval)

            except Exception as e:
                if attempt == max_retries - 1:
                    logger.error(f"Image generation timeout after {max_retries * retry_interval}s")
                    raise

        raise TimeoutError("Image generation timeout")

    def _check_status(self, request_id: str) -> dict:
        """检查生成状态"""
        response = requests.get(
            f"{self.base_url}/{self.model}/status/{request_id}",
            headers=self.headers,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
```

#### 模块3：JSON 验证器

```python
# services/json_validator.py
from typing import Dict, Tuple, List
import re

class JSONValidator:
    RULES = {
        "Slug": {
            "type": str,
            "pattern": r"^[a-z0-9\-]+$",
            "length": (20, 100),
            "required": True
        },
        "title": {
            "type": str,
            "length": (30, 100),
            "required": True,
            "not_contains": ["[", "{", "【"]  # 避免 Markdown 或中文括号
        },
        "TLNR": {
            "type": str,
            "length": (50, 150),
            "required": True
        },
        "cover": {
            "type": dict,
            "required": True,
            "fields": {
                "url": {"type": str, "pattern": r"^https?://"}
            }
        },
        "read_time": {
            "type": str,
            "pattern": r"^\d+\s*min$",
            "required": True
        },
        "main_category": {
            "type": str,
            "enum": ["news", "tutorial", "list"],
            "required": True
        },
        "article_body_content": {
            "type": str,
            "length_min": 1200,
            "required": True
        },
        "meta_title": {
            "type": str,
            "length": (30, 60),
            "required": True
        },
        "meta_description": {
            "type": str,
            "length": (100, 160),
            "required": True
        },
        "tag_for_SEO": {
            "type": str,
            "pattern": r"^([a-zA-Z0-9\s]+,\s)*[a-zA-Z0-9\s]+$",
            "required": True
        }
    }

    @classmethod
    def validate(cls, blog_data: Dict) -> Tuple[bool, List[str]]:
        """
        验证博客 JSON 数据

        Returns:
            (is_valid, error_messages)
        """
        errors = []

        for field, rules in cls.RULES.items():
            # 检查必需字段
            if rules.get("required") and field not in blog_data:
                errors.append(f"Missing required field: {field}")
                continue

            if field not in blog_data:
                continue

            value = blog_data[field]

            # 检查类型
            expected_type = rules.get("type")
            if expected_type and not isinstance(value, expected_type):
                errors.append(f"{field}: expected {expected_type.__name__}, got {type(value).__name__}")
                continue

            # 如果是字符串，检查长度和模式
            if isinstance(value, str):
                if "length" in rules:
                    min_len, max_len = rules["length"]
                    if not (min_len <= len(value) <= max_len):
                        errors.append(f"{field}: length must be {min_len}-{max_len}, got {len(value)}")

                if "length_min" in rules:
                    if len(value) < rules["length_min"]:
                        errors.append(f"{field}: minimum length is {rules['length_min']}, got {len(value)}")

                if "pattern" in rules:
                    if not re.match(rules["pattern"], value):
                        errors.append(f"{field}: does not match pattern {rules['pattern']}")

                if "enum" in rules:
                    if value not in rules["enum"]:
                        errors.append(f"{field}: must be one of {rules['enum']}, got '{value}'")

                if "not_contains" in rules:
                    for forbidden in rules["not_contains"]:
                        if forbidden in value:
                            errors.append(f"{field}: contains forbidden character '{forbidden}'")

        return len(errors) == 0, errors
```

#### 模块4：主流程管理

```python
# pipelines/content_pipeline.py
from enum import Enum
from typing import Optional, Dict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ContentType(Enum):
    NEWS = "news"
    TUTORIAL = "tutorial"
    LIST = "list"

class ContentPipeline:
    def __init__(self, file_manager, fal_client, validator):
        self.file_manager = file_manager
        self.fal_client = fal_client
        self.validator = validator

    def run(
        self,
        content_type: ContentType,
        materials: Dict,
        generate_images: bool = True,
        user_feedback: Optional[str] = None
    ) -> Dict:
        """
        执行完整的内容生成流程

        流程:
        1. 验证材料
        2. 生成中文初稿
        3. 用户审核（可选）
        4. 生成配图（可选）
        5. 生成英文版本
        6. 生成 SEO 元数据
        7. 验证最终输出
        8. 保存结果
        """

        try:
            logger.info(f"Starting {content_type.value} content generation...")

            # Step 1: 验证输入材料
            logger.info("Step 1: Validating input materials...")
            self._validate_materials(materials)

            # Step 2: 生成中文初稿
            logger.info("Step 2: Generating Chinese draft...")
            chinese_draft = self._generate_chinese_draft(
                content_type=content_type,
                materials=materials
            )

            # Step 3: 处理用户反馈（如果有）
            if user_feedback:
                logger.info("Step 3: Applying user feedback...")
                chinese_draft = self._apply_feedback(chinese_draft, user_feedback)

            # Step 4: 生成配图（如果需要）
            image_mapping = {}
            if generate_images:
                logger.info("Step 4: Generating and uploading images...")
                image_mapping = self._generate_and_upload_images(chinese_draft)

            # Step 5: 生成英文版本
            logger.info("Step 5: Translating to English...")
            english_content = self._translate_to_english(chinese_draft)

            # Step 6: 生成 SEO 元数据
            logger.info("Step 6: Generating SEO metadata...")
            seo_metadata = self._generate_seo_metadata(english_content)

            # Step 7: 组装最终 JSON
            logger.info("Step 7: Assembling final JSON...")
            final_json = self._assemble_json(
                content=english_content,
                seo_metadata=seo_metadata,
                images=image_mapping,
                content_type=content_type
            )

            # Step 8: 验证最终输出
            logger.info("Step 8: Validating final output...")
            is_valid, errors = self.validator.validate(final_json)
            if not is_valid:
                logger.error(f"Validation errors: {errors}")
                raise ValueError(f"JSON validation failed: {errors}")

            # Step 9: 保存结果
            logger.info("Step 9: Saving output...")
            output_path = self.file_manager.save_json_output(
                final_json,
                title=final_json.get("title", "untitled").replace(" ", "-").lower()
            )

            logger.info(f"✅ Content generation completed successfully!")
            logger.info(f"Output: {output_path}")

            return {
                "status": "success",
                "output_file": str(output_path),
                "json_data": final_json
            }

        except Exception as e:
            logger.error(f"❌ Content generation failed: {e}")
            raise

    def _validate_materials(self, materials: Dict):
        """验证输入材料"""
        if not materials:
            raise ValueError("No input materials provided")
        logger.info(f"Materials validated: {len(materials)} items")

    def _generate_chinese_draft(self, content_type: ContentType, materials: Dict) -> str:
        """使用 Claude API 生成中文初稿"""
        # 这里应该调用 Claude API
        # 为了简洁，这里用占位符表示
        logger.info(f"Generating {content_type.value} draft...")
        return "[中文初稿内容]"

    def _apply_feedback(self, draft: str, feedback: str) -> str:
        """应用用户反馈"""
        logger.info("Applying user feedback...")
        return draft  # 实现反馈应用逻辑

    def _generate_and_upload_images(self, content: str) -> Dict:
        """生成配图并上传"""
        logger.info("Generating images...")
        # 提取需要配图的位置
        # 调用 FAL.ai 生成图片
        # 上传到服务器
        return {}  # 返回图片 URL 映射

    def _translate_to_english(self, chinese_content: str) -> str:
        """翻译到英文"""
        logger.info("Translating to English...")
        return "[英文内容]"

    def _generate_seo_metadata(self, content: str) -> Dict:
        """生成 SEO 元数据"""
        logger.info("Generating SEO metadata...")
        return {
            "meta_title": "",
            "meta_description": "",
            "tags": []
        }

    def _assemble_json(self, content: str, seo_metadata: Dict, images: Dict, content_type: ContentType) -> Dict:
        """组装最终 JSON"""
        return {
            "Slug": "",
            "title": "",
            "article_body_content": content,
            "main_category": content_type.value,
            **seo_metadata
        }
```

### 3.3 CLI 工具设计

```python
# main.py
import click
from pathlib import Path
from services import FileManager, FALClient, JSONValidator
from pipelines import ContentPipeline, ContentType

@click.group()
def cli():
    """AliciBlog CLI - Blog content generation tool"""
    pass

@cli.command()
@click.option('--type', type=click.Choice(['news', 'tutorial', 'list']), required=True)
@click.option('--notion-links', multiple=True, help='Notion 公开链接')
@click.option('--txt-files', multiple=True, help='本地 txt 文件路径')
@click.option('--images/--no-images', default=True, help='是否生成配图')
def generate(type, notion_links, txt_files, images):
    """生成博客内容"""

    click.echo(f"🚀 Starting {type} content generation...")

    # 初始化组件
    base_dir = Path.cwd()
    file_manager = FileManager(base_dir)
    fal_client = FALClient(api_key="YOUR_API_KEY")
    validator = JSONValidator()
    pipeline = ContentPipeline(file_manager, fal_client, validator)

    # 收集材料
    materials = {}

    # 运行流程
    try:
        result = pipeline.run(
            content_type=ContentType(type),
            materials=materials,
            generate_images=images
        )
        click.secho("✅ Success!", fg="green")
        click.echo(f"Output: {result['output_file']}")
    except Exception as e:
        click.secho(f"❌ Failed: {e}", fg="red")

@cli.command()
def validate():
    """验证输出 JSON"""
    click.echo("Validating JSON files...")
    # 验证 output 目录中的所有 JSON
    pass

@cli.command()
def clean():
    """清空临时文件"""
    click.echo("Cleaning temporary files...")
    FileManager(Path.cwd()).clean_tmp_directory()
    click.secho("✅ Cleaned", fg="green")

if __name__ == '__main__':
    cli()
```

---

## Phase 3 集成架构

### 4.1 与 Framer CMS 的集成

**集成点：**
1. 从 JSON 导入内容
2. 自动创建页面
3. 自动生成 URL 路由
4. 自动发布到网站

**实现方案：**

```python
# services/framer_connector.py
import requests
from typing import Dict

class FramerCMSConnector:
    def __init__(self, api_key: str, workspace_id: str):
        self.api_key = api_key
        self.workspace_id = workspace_id
        self.base_url = "https://api.framer.com"

    def import_blog_post(self, blog_json: Dict) -> str:
        """
        导入博客文章到 Framer CMS

        Returns:
            Page URL
        """

        payload = {
            "title": blog_json["title"],
            "slug": blog_json["Slug"],
            "content": blog_json["article_body_content"],
            "metadata": {
                "cover_image": blog_json["cover"]["url"],
                "excerpt": blog_json["TLNR"],
                "category": blog_json["main_category"],
                "tags": blog_json["tag_for_SEO"].split(","),
                "seo": {
                    "title": blog_json["meta_title"],
                    "description": blog_json["meta_description"]
                },
                "read_time": blog_json["read_time"],
                "cta": {
                    "link": blog_json["CTA_alici_link"],
                    "text": blog_json["CTA button"]
                }
            }
        }

        response = requests.post(
            f"{self.base_url}/workspaces/{self.workspace_id}/pages",
            json=payload,
            headers={"Authorization": f"Bearer {self.api_key}"}
        )

        if response.status_code == 201:
            return response.json()["url"]
        else:
            raise Exception(f"Failed to import: {response.text}")

    def publish_page(self, page_id: str) -> bool:
        """发布页面"""
        response = requests.patch(
            f"{self.base_url}/pages/{page_id}/publish",
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        return response.status_code == 200
```

### 4.2 SEO 监控仪表板

**集成点：**
1. 与 Google Search Console 连接
2. 与 Google Analytics 连接
3. 实时监测排名、流量、转化

**数据模型：**

```python
@dataclass
class SEOMetrics:
    blog_id: str
    keyword: str
    rank: int
    clicks: int
    impressions: int
    ctr: float
    position: float
    updated_at: datetime

class SEOMonitor:
    def fetch_google_search_console_data(self, blog_slug: str) -> SEOMetrics:
        """从 Google Search Console 获取数据"""
        pass

    def fetch_google_analytics_data(self, blog_id: str) -> Dict:
        """从 Google Analytics 获取流量数据"""
        pass

    def calculate_performance_score(self, metrics: SEOMetrics) -> float:
        """计算性能评分"""
        pass
```

---

## 数据流与API设计

### 5.1 完整数据流

```
INPUT
  ↓
[Notion Parser] → 提取内容和元数据
  ↓
[Content Merger] → 合并多个源
  ↓
[Type Router] → 识别内容类型
  ↓
[Claude API] → 生成中文初稿
  ↓
PREVIEW (中文 HTML)
  ↓ (用户审核)
[Image Generator] → FAL.ai API
  ↓
[Image Uploader] → SSH/rsync 上传
  ↓
[Translator] → Claude API 翻译
  ↓
[SEO Generator] → 生成元数据
  ↓
[Format Converter] → 转换为 JSON
  ↓
[Validator] → 验证 JSON
  ↓
OUTPUT (JSON)
  ↓
[Framer Connector] → 导入 CMS
  ↓
Published Page
```

### 5.2 API 接口设计

#### 内部 API（用于流程管理）

```python
# API 端点设计
POST /api/v1/blog/generate
{
  "type": "news|tutorial|list",
  "materials": {
    "notion_links": ["..."],
    "txt_files": ["..."],
    "urls": ["..."]
  },
  "options": {
    "generate_images": true,
    "auto_translate": true,
    "auto_publish": false
  }
}

Response:
{
  "job_id": "uuid",
  "status": "processing",
  "progress": 0.3,
  "estimated_time": 1800
}

GET /api/v1/blog/jobs/{job_id}
Response:
{
  "job_id": "uuid",
  "status": "completed|processing|failed",
  "progress": 1.0,
  "output": {...}
}

GET /api/v1/blog/output/{blog_id}
Response:
{
  "blog_json": {...},
  "preview_url": "...",
  "status": "draft|ready|published"
}
```

#### 外部 API（与第三方服务）

```python
# FAL.ai API 包装
POST /api/v1/images/generate
{
  "prompt": "...",
  "aspect_ratio": "16:9",
  "num_images": 1
}

# Google Search Console API 包装
GET /api/v1/seo/metrics/{blog_id}
Query params: date_range, metric_type

# Framer CMS API 包装
POST /api/v1/cms/import
{
  "blog_json": {...}
}
```

---

## 部署与运维

### 6.1 本地开发环境设置

```bash
# 克隆项目
git clone <repo>
cd blog_new_sam

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # macOS/Linux

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env，填入 API 密钥

# 运行测试
pytest tests/

# 启动 CLI
python main.py --help
```

### 6.2 生产环境部署

**推荐方案：Docker + Kubernetes**

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
```

```yaml
# kubernetes.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: aliciblog-config
data:
  FLASK_ENV: production

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: aliciblog-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: aliciblog
  template:
    metadata:
      labels:
        app: aliciblog
    spec:
      containers:
      - name: aliciblog
        image: aliciblog:latest
        ports:
        - containerPort: 5000
        envFrom:
        - configMapRef:
            name: aliciblog-config
        - secretRef:
            name: aliciblog-secrets
```

### 6.3 监控与日志

```python
# 集成 ELK Stack 或 DataDog
import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
handler.setFormatter(formatter)
logger.addHandler(handler)

# 关键事件追踪
logger.info("blog_generated", extra={
    "blog_id": blog_id,
    "type": content_type,
    "word_count": word_count,
    "generation_time": elapsed_time,
    "status": "success"
})
```

---

## 性能与成本优化

### 7.1 性能优化

#### 缓存策略

```python
# 缓存已爬取的 Notion 内容（24 小时）
from functools import lru_cache
import time

NOTION_CACHE = {}
CACHE_TTL = 86400  # 24 小时

def get_notion_page_cached(url: str) -> str:
    cache_key = url
    if cache_key in NOTION_CACHE:
        cached_data, timestamp = NOTION_CACHE[cache_key]
        if time.time() - timestamp < CACHE_TTL:
            return cached_data

    # 缓存未命中或已过期，重新爬取
    content = fetch_notion_page(url)
    NOTION_CACHE[cache_key] = (content, time.time())
    return content
```

#### 并行处理

```python
# 并行生成多张配图
from concurrent.futures import ThreadPoolExecutor

def generate_images_parallel(prompts: List[str], max_workers: int = 3):
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(fal_client.generate_image, prompt)
            for prompt in prompts
        ]
        for future in futures:
            results.append(future.result())
    return results
```

### 7.2 成本优化

#### 按需付费模型

```
当前成本：
- FAL.ai 图片生成：$0.002-0.01 / 张
- 一篇文章平均 3-5 张配图：$0.01-0.05
- 月产 10 篇：$0.1-0.5 / 月

优化方案：
1. 建立图片库，减少重复生成
2. 使用更便宜的图片模型（Nano 已经很便宜）
3. 压缩图片大小，减少存储成本
```

---

## 技术债与改进方案

### 8.1 当前技术债

| 债务 | 严重程度 | 还债成本 | 优先级 |
|------|---------|---------|--------|
| 缺少自动化脚本 | 高 | 100+ 小时 | P1 |
| SSH 密码硬编码 | 高 | 4 小时 | P1 |
| 缺少 JSON 验证 | 中 | 8 小时 | P2 |
| 缺少错误处理 | 中 | 12 小时 | P2 |
| 缺少日志系统 | 中 | 6 小时 | P2 |
| 缺少单元测试 | 低 | 20 小时 | P3 |
| 缺少文档 API | 低 | 10 小时 | P3 |

### 8.2 优化路线图

```
Month 1-2: Foundation
├── ✅ 完成自动化脚本开发
├── ✅ 完成 JSON 验证
├── ✅ 修复安全问题（SSH 密钥）
└── ✅ 添加基础日志系统

Month 3: Stability
├── ✅ 单元测试覆盖率 >80%
├── ✅ 错误处理完善
├── ✅ 文档完善
└── ✅ 性能测试

Month 4+: Enhancement
├── ✅ 与 Framer CMS 集成
├── ✅ SEO 监控仪表板
├── ✅ AI 自动化内容生成
└── ✅ 多语言支持
```

---

## 总结

### 关键技术指标

| 指标 | 当前 | Phase 2 目标 | 实现难度 |
|------|------|-----------|---------|
| 自动化比例 | 0% | 40% | 中 |
| 生成速度 | 2-4h/篇 | 1.5-2.5h/篇 | 中 |
| 代码覆盖率 | 无 | >80% | 低 |
| 部署周期 | 手工 | 自动化 (CI/CD) | 中 |

### 推荐技术选型

**语言：** Python 3.11+ (成熟、库多、易部署)
**框架：** FastAPI (异步、性能好)
**数据库：** PostgreSQL (关系型、稳定)
**缓存：** Redis (高性能、分布式)
**容器化：** Docker + Kubernetes (生产级)
**监控：** Prometheus + Grafana (开源)

---

**最后更新：** 2025-01-10
**文档版本：** 1.0 (Technical Preview)
