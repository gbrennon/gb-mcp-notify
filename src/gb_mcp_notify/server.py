from mcp.server.fastmcp import FastMCP

from gb_mcp_notify._notifier import send

mcp = FastMCP("notify")


@mcp.tool()
def notify(
    summary: str,
    body: str = "",
    urgency: str = "normal",
) -> str:
    """
    Send a desktop notification via notify-send.

    Call this tool whenever you need the user to come back and interact,
    or when a long-running task completes.

    Args:
        summary: Short title shown in the notification (required).
        body:    Optional longer description.
        urgency: One of 'low', 'normal', 'critical'. Use 'critical' when
                 blocking input is required immediately.
    """
    return send(summary, body, urgency)


def main() -> None:
    mcp.run(transport="stdio")
