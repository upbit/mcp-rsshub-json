import os
from rsshub import *


TITLE = "RSSHUB MCP Service"
VERSION = "1.0.0"

USER_INSTANCES = [
    inst.strip()
    for inst in os.getenv("USER_INSTANCES", "").split(";")
    if inst.strip() != ""
]
if len(USER_INSTANCES) > 0:
    RSSHUB_INSTANCES = USER_INSTANCES
print("RSSHUB_INSTANCES> ", json.dumps(RSSHUB_INSTANCES, indent=2))

# MCP endpoint
http_app = mcp.http_app(path=os.getenv("MCP_ENDPOINT", "/rsshub"))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(http_app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
