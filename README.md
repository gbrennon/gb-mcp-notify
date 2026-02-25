# gb-mcp-notify

Minimal MCP server that exposes a `notify` tool backed by `notify-send`.
Designed for CLI/tmux workflows where you want the agent to ping you when
it needs interaction or finishes a long task.

## Requirements

- `notify-send` in PATH (ships with `libnotify-bin` on Debian/Ubuntu)
- Python ≥ 3.14
- [uv](https://docs.astral.sh/uv/)

## Install

```bash
# Install as a persistent uv tool (adds gb-mcp-notify to PATH)
uv tool install .

# Or run directly from the project directory without installing
uv run gb-mcp-notify
```

## MCP client configuration

Point your MCP client at the installed binary or use `uv run`:

### Using the installed tool

```json
{
  "command": "gb-mcp-notify",
  "args": []
}
```

### Using uv run (no install required)

```json
{
  "command": "uv",
  "args": ["run", "--directory", "/path/to/gb-mcp-notify", "gb-mcp-notify"]
}
```

### Using server.py directly (legacy)

```json
{
  "command": "python3",
  "args": ["/path/to/gb-mcp-notify/server.py"]
}
```

---

### Claude Code (`~/.claude/settings.json` or project `.claude/settings.json`)

```json
{
  "mcpServers": {
    "notify": {
      "command": "gb-mcp-notify",
      "args": []
    }
  }
}
```

### opencode (`~/.config/opencode/config.json`)

```json
{
  "mcp": {
    "notify": {
      "command": "gb-mcp-notify",
      "args": []
    }
  }
}
```

### GitHub Copilot CLI (`~/.copilot/mcp.json`)

```json
{
  "mcpServers": {
    "notify": {
      "command": "gb-mcp-notify",
      "args": []
    }
  }
}
```

To make the agent use it proactively, add to `~/.copilot/copilot-instructions.md`:

```
When you need user input or are about to ask a question, always call the
notify tool first with urgency="critical" so the user knows to look at
the terminal.
```

### GitHub Copilot — VS Code (`settings.json`)

```json
"github.copilot.chat.mcp.servers": {
  "notify": {
    "command": "gb-mcp-notify",
    "args": []
  }
}
```

---

## Usage

The agent calls the `notify` tool autonomously. For clients other than Copilot CLI,
add an instruction to your system prompt / global rules:

```
When you need user input or are about to ask a question, always call the
notify tool first with urgency="critical" so the user knows to look at
the terminal.
```

## Tool schema

| param     | type   | default    | description                                   |
|-----------|--------|------------|-----------------------------------------------|
| `summary` | string | (required) | Notification title                            |
| `body`    | string | `""`       | Optional detail text                          |
| `urgency` | string | `"normal"` | `low` / `normal` / `critical`                |

Use `critical` when the agent is blocked waiting for your input.
