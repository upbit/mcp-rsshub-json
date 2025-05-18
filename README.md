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

### Docker 部署

#### docker compose

参考 [docker-compose.yaml](https://github.com/upbit/mcp-rsshub-json/blob/main/docker-compose.yaml)

#### docker 命令

`docker run -i --rm -p 8000:8000 ghcr.io/upbit/mcp-rsshub:latest`

国内镜像源：

`docker run -i --rm -p 8000:8000 ghcr.nju.edu.cn/upbit/mcp-rsshub:latest`

如果你有多个 mcp servers，可以调整 -p {本地端口}:8000。其他环境变量参数：

|环境变量|说明|参考配置|
|-------|----|-------|
|PORT|服务的监听端口|默认 `8000`；一般改docker映射端口即可|
|MCP_ENDPOINT|MCP的路径|默认 `rsshub`；对应配置中的 `http://127.0.0.1:8000/rsshub` 最后部分|
|USER_INSTANCES|覆盖默认的rsshub源|仅在指定自己的源时需要，分号分隔。如 "http://localhost:1234;http://localhost:2234"|

#### mcpServers 配置

```
{
  "mcpServers": {
    "filesystem": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-p",
        "8000:8000",
        "ghcr.io/upbit/mcp-rsshub"
      ]
    }
  }
}
```

## 基本用法

### mcp获取演示

```py
from fastmcp import Client

async def main():
    # 要获取的 rsshub URL
    url = "rsshub://zaobao/realtime/world"

    async with Client("http://127.0.0.1:8000/rsshub") as client:
        result = await client.call_tool("get_feed", {"url": url})
        print(result)
```

详见 [mcp_demo.py](https://github.com/upbit/mcp-rsshub-json/blob/main/mcp_demo.py)

### LLM调用演示 (qwen_agent)

1. 加载模型 http://localhost:8080/v1 : `llama-server --alias "qwen3-32b:q4_k_m" -m Qwen3-32B-Q4_K_M.gguf -ngl 99`
2. 启动 MCP server http://localhost:8000/rsshub : `docker compose up -d`
3. 安装 qwen_agent : `uv pip install "qwen-agent[rag,code_interpreter,gui,mcp]"`

```py
from qwen_agent.agents import Assistant
from qwen_agent.utils.output_beautify import typewriter_print

llm_cfg = {
    "model": "qwen3-32b:q4_k_m", # load model with llama.cpp
    "model_server": "http://localhost:8080/v1",  # base_url, also known as api_base
    "api_key": "EMPTY",
    "generate_cfg": {
        "temperature": 0.6,
        "top_p": 0.6,
        "top_k": 20,
        "presence_penalty": 1.5,
    },
}

tools = [
    {
        "mcpServers": {
            "mcp-rsshub": {
                "url": "http://localhost:8000/rsshub",
                "timeout": 60,
            },
        }
    }
]

system_prompts = """你是个新闻抓取的帮助AI。在收到用户的指令后，你应该：
- 优先分析给定的内容是否 rsshub 工具可以处理的内容
- 获取内容后，将信息汇总并组织成一个连贯的总结
"""

bot = Assistant(llm=llm_cfg, system_message=system_prompts, function_list=tools)

messages = [{"role": "user", "content": "使用 rsshub 工具获取 rsshub://zaobao/realtime/world 的最新内容"}]

response_plain_text = ""
for response in bot.run(messages=messages):
    response_plain_text = typewriter_print(response, response_plain_text)
```

### 支持的 URL 格式

```python
from rsshub import get_feed

# 使用 rsshub:// 格式
result = await get_feed("rsshub://bilibili/user/video/123456")

# 使用标准 URL 格式
result = await get_feed("https://rsshub.app/bilibili/user/video/123456")

# 使用简写格式
result = await get_feed("bilibili/user/video/123456")
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

## Docker

推荐使用 docker 镜像来启动 mcp server

`docker compose up -d`

启动后配置mcp服务如下：

```json
{
    "mcpServers": {
        "rsshub": {
            "url": "http://localhost:8000/rsshub",
            "timeout": 60,
        },
    }
}
```

## 注意事项

- 工具会自动尝试多个 RSSHub 实例，直到成功获取数据
- 所有实例都失败时才会抛出异常
- 支持自动清理 HTML 标签，提取纯文本内容
- 时间会自动转换为 UTC 时区

## 许可证

MIT License 
