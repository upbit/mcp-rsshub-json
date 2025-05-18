import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client
from fastmcp import Client

# Start docker with: docker run -i --rm -p 8000:8000 ghcr.io/upbit/mcp-rsshub:latest


async def sse_demo():
    url = "rsshub://zaobao/realtime/world"
    async with sse_client(url="http://127.0.0.1:8000/rsshub") as streams:
        # Create the client session with the streams
        async with ClientSession(*streams) as session:
            # Initialize the session
            await session.initialize()

            # List available tools
            response = await session.list_tools()
            print("Available tools:", [tool.name for tool in response.tools])

            # Call the get_feeds
            result = await session.call_tool("get_feed", {"url": url})
            print(result.content)


async def streamable_http_demo():
    url = "rsshub://zaobao/realtime/world"
    async with Client("http://127.0.0.1:8000/rsshub") as client:
        result = await client.call_tool("get_feed", {"url": url})
        print(result)


if __name__ == "__main__":
    asyncio.run(sse_demo())
    # asyncio.run(streamable_http_demo())  # with --env MCP_MODE="streamable-http"
