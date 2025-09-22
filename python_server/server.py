
from __future__ import annotations
import logging
import os
from pathlib import Path
from typing import Iterable

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP, Context

load_dotenv()
# Log to stderr (safe for STDIO servers)
logging.basicConfig(level=logging.INFO)

ALLOWED_ROOT = Path(os.environ.get("ALLOWED_ROOT", ".")).resolve()
mcp = FastMCP("bridge-server")

def _inside_root(p: Path) -> bool:
    try:
        p.resolve().relative_to(ALLOWED_ROOT)
        return True
    except Exception:
        return False

# Resources
@mcp.resource("config://about")
def about() -> str:
    return (
        "MCP Bridge Server — tools: list_files, read_text, calc, echo; "
        f"root: {ALLOWED_ROOT}"
    )

@mcp.resource("file://{relpath}")
def read_file(relpath: str) -> str:
    target = (ALLOWED_ROOT / relpath).resolve()
    if not _inside_root(target):
        raise ValueError("Path escapes allowed root")
    if not target.exists() or not target.is_file():
        raise FileNotFoundError(relpath)
    return target.read_text(encoding="utf-8")

# Tools
@mcp.tool()
def echo(text: str) -> str:
    """Echo text back (smoke test)."""
    return text

@mcp.tool()
def list_files(glob: str = "**/*.md") -> str:
    """List files (relative to ALLOWED_ROOT) matching glob."""
    base = ALLOWED_ROOT
    matches: Iterable[Path] = base.glob(glob)
    lines = [str(p.relative_to(base)) for p in matches if p.is_file()]
    return "\n".join(lines) if lines else "No matches"

@mcp.tool()
def read_text(path: str) -> str:
    """Read small UTF-8 text file (relative)."""
    target = (ALLOWED_ROOT / path).resolve()
    if not _inside_root(target):
        raise ValueError("Path escapes allowed root")
    if target.stat().st_size > 256_000:
        raise ValueError("File too large")
    return target.read_text(encoding="utf-8")

@mcp.tool()
def calc(expr: str) -> str:
    """Evaluate simple arithmetic safely (digits + +-*/().)."""
    allowed = set("0123456789+-*/(). ")
    if not set(expr) <= allowed:
        raise ValueError("Only arithmetic is allowed")
    result = eval(expr, {"__builtins__": {}}, {})
    return str(result)

# Prompts
@mcp.prompt()
def code_review(goal: str, style: str = "concise") -> str:
    return (
        f"Review the code for: {goal}. Focus on correctness, security, and tests. "
        f"Keep it {style}."
    )

if __name__ == "__main__":
    # Run over STDIO (don't print to stdout elsewhere)
    mcp.run(transport="stdio")
