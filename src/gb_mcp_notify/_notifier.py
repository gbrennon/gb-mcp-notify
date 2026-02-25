import subprocess
import shutil


def send(summary: str, body: str = "", urgency: str = "normal") -> str:
    if not shutil.which("notify-send"):
        raise RuntimeError("notify-send not found in PATH")

    valid = {"low", "normal", "critical"}
    if urgency not in valid:
        raise ValueError(f"urgency must be one of {valid}")

    cmd = ["notify-send", "--urgency", urgency, summary]
    if body:
        cmd.append(body)

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"notify-send failed: {result.stderr.strip()}")

    return "notification sent"
