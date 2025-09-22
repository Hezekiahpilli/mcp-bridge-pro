
# MCP Bridge Server

## Setup
```bash
uv venv
source .venv/bin/activate || source .venv/Scripts/activate
uv pip install -e .
cp .env.example .env
```

## Run (STDIO)
```bash
uv run python server.py
```

## With MCP Inspector (from repo root)
```bash
npx -y @modelcontextprotocol/inspector uv --directory ./python_server run python server.py
```
