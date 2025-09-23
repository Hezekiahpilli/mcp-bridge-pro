
# MCP Bridge Pro

End-to-end Model Context Protocol (MCP) example consisting of:

- Python MCP Server (`python_server`): Exposes example resources, tools, and prompts.
- TypeScript MCP Client (`ts_client`): Connects to the server over STDIO and calls tools.

This repo shows a clean, minimal pattern for building and testing MCP servers and clients locally, including running with the MCP Inspector.

---

## Project Structure

- `python_server/`: Python MCP server (FastMCP) packaged with `uv`.
- `ts_client/`: Node/TypeScript client using `@modelcontextprotocol/sdk`.
- `tools/mcp.json`: Utility config for MCP tooling.

---

## Prerequisites

- Python 3.10+
- Node.js 18+
- `uv` (recommended for Python packaging and virtualenvs). Install: https://github.com/astral-sh/uv

---

## Python MCP Server

Location: `python_server/`

### Setup
```bash
uv venv
source .venv/bin/activate || source .venv/Scripts/activate
uv pip install -e .
cp .env.example .env || true
```

If you don’t have an `.env.example`, you can create `.env` as needed. The server supports the following environment variable:

- `ALLOWED_ROOT` (default: `.`): Filesystem root used by file-related tools/resources to prevent escaping into other directories.

### Run (STDIO)
```bash
uv run python server.py
```

### Run with MCP Inspector (from repo root)
```bash
npx -y @modelcontextprotocol/inspector uv --directory ./python_server run python server.py
```

### What the server provides

Resources:
- `config://about`: Describes the server and configured root
- `file://{relpath}`: Read text content for a relative file within `ALLOWED_ROOT`

Tools:
- `echo(text: str)`: Echoes text back
- `list_files(glob: str = "**/*.md")`: Lists files under `ALLOWED_ROOT` matching a glob
- `read_text(path: str)`: Reads a small UTF-8 text file relative to `ALLOWED_ROOT`
- `calc(expr: str)`: Evaluates simple arithmetic expressions (digits and +-*/(). only)

Prompts:
- `code_review(goal: str, style: str = "concise")`

---

## TypeScript MCP Client

Location: `ts_client/`

### Install
```bash
cd ts_client
npm install
```

### Configure the command used to start the server

By default the client uses environment variables to determine how to start the server over STDIO:

- `MCP_CMD` (default: `python`)
- `MCP_ARGS` (default: `C:/mcp-bridge-pro/python_server/server.py` on Windows in this example)

You can override these when running the client, for example:

```bash
# macOS/Linux example
MCP_CMD=python MCP_ARGS="python_server/server.py" npm run dev

# Windows PowerShell example
$env:MCP_CMD="python"; $env:MCP_ARGS="C:/mcp-bridge-pro/python_server/server.py"; npm run dev
```

### Run (development)
```bash
npm run dev
```

This will:
1. Spawn the Python server via the STDIO transport.
2. List available tools.
3. Call `echo` and `calc` and print their results.

### Build and run (compiled)
```bash
npm run build
npm start
```

---

## Common Workflows

### Start server and test with Inspector
```bash
# From repo root
npx -y @modelcontextprotocol/inspector uv --directory ./python_server run python server.py
```

### Run client against local server
```bash
cd ts_client
MCP_CMD=python MCP_ARGS="../python_server/server.py" npm run dev
```

On Windows PowerShell:
```powershell
cd ts_client
$env:MCP_CMD="python"; $env:MCP_ARGS="..\\python_server\\server.py"; npm run dev
```

---

## Troubleshooting

- If the client cannot spawn the server, verify `MCP_CMD` and `MCP_ARGS` point to a valid Python and script path.
- If file tools fail, confirm `ALLOWED_ROOT` is set appropriately and that paths are within that root.
- If `uv` is not found, install it and re-run the setup steps for the Python server.

---

## License

MIT