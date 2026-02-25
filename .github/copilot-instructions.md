# Copilot Instructions

## Project Overview

`gb-mcp-notify` is a minimal [MCP](https://modelcontextprotocol.io/) server that exposes a single `notify` tool backed by the system's `notify-send` binary. It is intended for CLI/tmux workflows where an AI agent should ping the user on completion or when interaction is required.

## Architecture

The project has a split structure:

- **`server.py`** — the runnable MCP server. This is the file to point MCP clients at. It uses `FastMCP` from the `mcp` SDK, registers the `notify` tool, and runs with `transport="stdio"`.
- **`src/gb_mcp_notify/__init__.py`** — the installable Python package entry point (currently a stub `main()`). The `pyproject.toml` `[project.scripts]` entry points here, not to `server.py`.

When extending functionality, add new MCP tools in `server.py` using the `@mcp.tool()` decorator pattern. The `_send()` helper is internal and not exposed as a tool.

## Build & Run

This project uses [uv](https://docs.astral.sh/uv/) exclusively (no pip/poetry):

```bash
# Install dependencies
uv sync

# Run the MCP server directly (stdio transport)
python server.py

# Or via installed script
uv run gb-mcp-notify
```

## Key Conventions

- **`notify-send` is a hard runtime dependency** — `_send()` raises `RuntimeError` if it isn't in `PATH`. Tests or environments without it must mock `shutil.which` and `subprocess.run`.
- **Urgency values are validated** against the set `{"low", "normal", "critical"}` — use `ValueError` for invalid values, `RuntimeError` for `notify-send` failures.
- **`server.py` is intentionally flat** — no sub-modules. Keep new tools in the same file unless the file grows significantly.
- Python `>=3.14` is required (see `.python-version` and `pyproject.toml`).

## MCP Client Configuration

Point MCP clients at `server.py` with `python3` as the command and `stdio` transport:

```json
{
  "command": "python3",
  "args": ["/path/to/gb-mcp-notify/server.py"]
}
```

Client-specific config paths: Claude Code (`~/.claude/settings.json`), opencode (`~/.config/opencode/config.json`), VS Code Copilot (`settings.json` → `github.copilot.chat.mcp.servers`).
