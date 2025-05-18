# Build with docker build -t ghcr.io/upbit/mcp-rsshub:latest -t ghcr.io/upbit/mcp-rsshub:{VERSION} .
FROM python:3.12-alpine

RUN pip install uv

COPY rsshub /app
WORKDIR /app

RUN uv pip install --system -r /app/requirements.txt

CMD [ "python", "rsshub_server.py" ]