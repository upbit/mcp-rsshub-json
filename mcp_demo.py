import asyncio
from fastmcp import Client

# Start docker with: docker run -i --rm -p 8000:8000 ghcr.io/upbit/mcp-rsshub:latest


async def main():
    url = "rsshub://zaobao/realtime/world"
    async with Client("http://127.0.0.1:8000/rsshub") as client:
        result = await client.call_tool("get_feed", {"url": url})
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
