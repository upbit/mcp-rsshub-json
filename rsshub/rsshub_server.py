import os
from rsshub import *

USER_INSTANCES = [
    inst.strip()
    for inst in os.getenv("USER_INSTANCES", "").split(";")
    if inst.strip() != ""
]
if len(USER_INSTANCES) > 0:
    RSSHUB_INSTANCES = USER_INSTANCES

if __name__ == "__main__":
    mode = os.getenv("MCP_MODE", "sse")  # stdio, streamable-http, sse
    port = int(os.getenv("PORT", 8000))
    endpoint = os.getenv("MCP_ENDPOINT", "/rsshub")
    print(
        f"Start mcp-rsshub(mode={mode}, port={port}, path={endpoint}) instances={json.dumps(RSSHUB_INSTANCES, indent=2)}"
    )
    mcp.run(transport=mode, host="0.0.0.0", port=port, path=endpoint)
