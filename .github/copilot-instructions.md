# Copilot Instructions

## Project Overview

`gb-mcp-notify` is a minimal [MCP](https://modelcontextprotocol.io/) server that exposes a single `notify` tool backed by the system's `notify-send` binary. It is intended for CLI/tmux workflows where an AI agent should ping the user on completion or when interaction is required.

## Architecture

```
src/gb_mcp_notify/
├── __init__.py     # Package initializer — re-exports main()
├── server.py       # FastMCP instance, @mcp.tool() notify, main()
└── _notifier.py    # send() helper — subprocess/notify-send concern
server.py           # Backward-compat shim → calls main()
```

- **`_notifier.py`** owns the subprocess interaction with `notify-send`. No MCP dependency.
- **`server.py`** owns the MCP layer: tool registration and `mcp.run()`. Imports `send` from `_notifier`.
- **`__init__.py`** only re-exports `main` for the console script entry point.
- **`server.py` (root)** is a thin shim kept for existing MCP configs that point at it directly.

When adding new MCP tools, add them in `src/gb_mcp_notify/server.py`. Add new system-level helpers in `src/gb_mcp_notify/_notifier.py` or a new `_<concern>.py` module.

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

- **`notify-send` is a hard runtime dependency** — `send()` in `_notifier.py` raises `RuntimeError` if it isn't in `PATH`. Tests must mock `shutil.which` and `subprocess.run`.
- **Urgency values are validated** against `{"low", "normal", "critical"}` — `ValueError` for invalid urgency, `RuntimeError` for `notify-send` failures.
- **Private helpers are prefixed with `_`** (e.g., `_notifier.py`) — they are internal to the package.
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

Client-specific config paths: Claude Code (`~/.claude/settings.json`), opencode (`~/.config/opencode/config.json`), Copilot CLI (`~/.copilot/mcp.json`), VS Code Copilot (`settings.json` → `github.copilot.chat.mcp.servers`).
