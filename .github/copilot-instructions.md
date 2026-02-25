# Copilot Instructions

## Project Overview

`gb-mcp-notify` is a minimal [MCP](https://modelcontextprotocol.io/) server that exposes a single `notify` tool backed by the system's `notify-send` binary. It is intended for CLI/tmux workflows where an AI agent should ping the user on completion or when interaction is required.

## Architecture

- **`src/gb_mcp_notify/__init__.py`** — all server logic lives here: the `FastMCP` instance, `_send()` helper, `notify` tool, and `main()` entry point that calls `mcp.run(transport="stdio")`.
- **`server.py`** — thin backward-compatibility shim that imports and calls `main()`. Existing MCP configs pointing at this file still work, but prefer the package entry point.
- **`pyproject.toml`** — declares `gb-mcp-notify = "gb_mcp_notify:main"` as the console script.

When adding new MCP tools, add them in `src/gb_mcp_notify/__init__.py` using the `@mcp.tool()` decorator.

## Build & Run

This project uses [uv](https://docs.astral.sh/uv/) exclusively:

```bash
# Install dependencies
uv sync

# Run without installing
uv run gb-mcp-notify

# Install as a system tool (adds gb-mcp-notify to PATH)
uv tool install .

# Upgrade after code changes
uv tool upgrade gb-mcp-notify
```

## Key Conventions

- **`notify-send` is a hard runtime dependency** — `_send()` raises `RuntimeError` if it isn't in `PATH`. Tests or environments without it must mock `shutil.which` and `subprocess.run`.
- **Urgency values are validated** against `{"low", "normal", "critical"}` — `ValueError` for invalid urgency, `RuntimeError` for `notify-send` failures.
- **`src/gb_mcp_notify/__init__.py` is intentionally flat** — keep new tools in the same file unless it grows significantly.
- Python `>=3.14` is required (see `.python-version` and `pyproject.toml`).

## MCP Client Configuration

After `uv tool install .`, point clients at the installed binary:

```json
{ "command": "gb-mcp-notify", "args": [] }
```

Without installing, use `uv run`:

```json
{ "command": "uv", "args": ["run", "--directory", "/path/to/gb-mcp-notify", "gb-mcp-notify"] }
```

Client-specific config paths: Claude Code (`~/.claude/settings.json`), opencode (`~/.config/opencode/config.json`), VS Code Copilot (`settings.json` → `github.copilot.chat.mcp.servers`).
