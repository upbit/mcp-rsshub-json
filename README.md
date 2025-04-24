# RSSHUB MCP 工具

RSSHUB MCP 是一个用于获取和解析 RSS 源的 Python 工具，它支持多种 RSSHub 实例，并提供了自动故障转移功能。

## 功能特点

- 支持多种 RSSHub 实例自动切换
- 自动处理 `rsshub://` 格式的链接
- 智能解析 RSS 源内容
- 支持多种用户代理随机切换
- 自动清理 HTML 内容
- 支持 JSON 格式的输入
- 自动时区转换

## 支持的 RSSHub 实例

工具内置了多个 RSSHub 实例，包括：
- rsshub.app
- rsshub.rssforever.com
- rsshub.feeded.xyz
- hub.slarker.me
- 等多个公共实例

## 使用方法

### 基本用法

```python
from rsshub import rsshub_get_feed

# 使用 rsshub:// 格式
result = await rsshub_get_feed("rsshub://bilibili/user/video/123456")

# 使用标准 URL 格式
result = await rsshub_get_feed("https://rsshub.app/bilibili/user/video/123456")

# 使用简写格式
result = await rsshub_get_feed("bilibili/user/video/123456")
```

### 返回数据格式

工具返回的数据包含以下字段：

```json
{
    "title": "RSS源标题",
    "link": "RSS源链接",
    "description": "RSS源描述",
    "items": [
        {
            "title": "文章标题",
            "description": "文章描述",
            "link": "文章链接",
            "guid": "文章唯一标识",
            "pubDate": "发布时间",
            "author": "作者",
            "category": ["分类标签1", "分类标签2"]
        }
    ]
}
```

## 环境要求

- Python 3.8+
- 依赖包：
  - httpx
  - feedparser
  - beautifulsoup4
  - pytz

## 安装方法

### 方法一：使用 pip

1. 克隆仓库
2. 安装依赖：
```bash
pip install -r requirements.txt
```

### 方法二：使用 uv（推荐）

uv 是一个极快的 Python 包管理器，安装过程如下：

1. 安装 uv（如果尚未安装）：
```bash
pip install uv
```

2. 创建并初始化项目（如果是新项目）：
```bash
uv init rsshub
cd rsshub
```

3. 创建虚拟环境：
```bash
uv venv
```

4. 激活虚拟环境：
```bash
.venv\Scripts\activate  # Windows
# 或
source .venv/bin/activate  # Linux/macOS
```

5. 安装依赖：
```bash
uv pip install -r requirements.txt
```

## 注意事项

- 工具会自动尝试多个 RSSHub 实例，直到成功获取数据
- 所有实例都失败时才会抛出异常
- 支持自动清理 HTML 标签，提取纯文本内容
- 时间会自动转换为 UTC 时区

## 许可证

MIT License 