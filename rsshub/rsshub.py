from typing import Any, Dict, List, Optional
import httpx
from mcp.server.fastmcp import FastMCP
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import random
import json

# Initialize MCP server
mcp = FastMCP("rsshub")

# 添加 RSSHub 实例列表
RSSHUB_INSTANCES = [
    "https://rsshub.app",
    "https://rsshub.rssforever.com",
    "https://rsshub.feeded.xyz",
    "https://hub.slarker.me",
    "https://rsshub.liumingye.cn",
    "https://rsshub-instance.zeabur.app",
    "https://rss.fatpandac.com",
    "https://rsshub.pseudoyu.com",
    "https://rsshub.friesport.ac.cn",
    "https://rsshub.atgw.io",
    "https://rsshub.rss.tips",
    "https://rsshub.mubibai.com",
    "https://rsshub.ktachibana.party",
    "https://rsshub.woodland.cafe",
    "https://rsshub.aierliz.xyz",
    "http://localhost:1200"
]

def convert_rsshub_url(url: str) -> str:
    """将 rsshub:// 格式的链接或标准 RSSHub URL 转换为所有可能的实例 URL"""
    if url.startswith('rsshub://'):
        path = url[9:]
        return [f"{instance}/{path}" for instance in RSSHUB_INSTANCES]
    
    # 处理标准 RSSHub URL
    for instance in RSSHUB_INSTANCES:
        if url.startswith(instance):
            # 提取路径部分
            path = url[len(instance):].lstrip('/')
            # 为所有实例生成对应的 URL
            return [f"{inst}/{path}" for inst in RSSHUB_INSTANCES]
    
    return [url]  # 非 RSSHub 格式的 URL 直接返回单个 URL 的列表

@mcp.tool()
async def rsshub_get_feed(url: str) -> Dict[str, Any]:
    """获取RSSHub的RSS源"""
    
    # 确保参数是字符串类型
    if isinstance(url, (dict, str)):
        try:
            # 如果是JSON字符串，尝试解析
            if isinstance(url, str):
                # 尝试解析JSON字符串
                try:
                    parsed = json.loads(url)
                    if isinstance(parsed, dict) and 'url' in parsed:
                        url = parsed['url']
                except json.JSONDecodeError:
                    # 如果不是有效的JSON，直接使用原始字符串
                    pass
        except Exception as e:
            print(f"URL处理错误: {str(e)}")
            # 如果解析失败，保持原始URL不变
            pass
    
    if not isinstance(url, str):
        raise ValueError(f"URL必须是字符串类型，当前类型: {type(url)}")
    
    # 如果URL是bilibili这样的路径格式，自动添加rsshub://前缀
    if not url.startswith(('http://', 'https://', 'rsshub://')):
        url = f"rsshub://{url}"
    
    # 转换 rsshub:// 格式的链接，获取所有可能的URL
    urls = convert_rsshub_url(url)
    
    # 模拟真实浏览器的 User-Agent 列表
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0"
    ]
    
    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept": "application/rss+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }

    last_error = None
    
    # 遍历所有可能的URL，直到成功获取数据
    for current_url in urls:
        try:
            async with httpx.AsyncClient(
                timeout=30.0,
                follow_redirects=True,
                verify=False
            ) as client:
                response = await client.get(current_url, headers=headers)
                response.raise_for_status()
                
                # 使用 feedparser 解析 RSS
                feed = feedparser.parse(response.text)
                
                if not feed.entries and not hasattr(feed, 'feed'):
                    raise Exception("无法解析RSS源")

                # 获取 feed 元数据
                feed_info = {
                    "title": feed.feed.get('title'),
                    "link": feed.feed.get('link'),
                    "description": feed.feed.get('description'),
                    "items": []
                }

                # 处理每个条目
                for entry in feed.entries:
                    # 清理 HTML 内容
                    description = entry.get('description', '')
                    if description:
                        soup = BeautifulSoup(description, 'html.parser')
                        description = soup.get_text(separator=' ', strip=True)

                    # 处理发布日期
                    pub_date = None
                    if 'published_parsed' in entry:
                        try:
                            dt = datetime(*entry.published_parsed[:6])
                            pub_date = dt.astimezone(pytz.UTC).isoformat()
                        except Exception as e:
                            print(f"Date parse error: {str(e)}")
                            pub_date = entry.get('published', '')

                    # 构建条目字典
                    feed_item = {
                        "title": entry.get('title'),
                        "description": description,
                        "link": entry.get('link'),
                        "guid": entry.get('id', entry.get('guid', entry.get('link'))),
                        "pubDate": pub_date,
                        "author": entry.get('author'),
                        "category": [tag.term for tag in entry.get('tags', [])] if 'tags' in entry else None
                    }
                    feed_info["items"].append(feed_item)

                return feed_info

        except Exception as e:
            last_error = e
            print(f"尝试访问 {current_url} 失败: {str(e)}")
            continue  # 尝试下一个URL
    
    # 如果所有URL都失败，抛出最后一个错误
    raise Exception(f"所有RSSHub实例均无法访问: {str(last_error)}")

if __name__ == "__main__":
    mcp.run(transport='stdio')
