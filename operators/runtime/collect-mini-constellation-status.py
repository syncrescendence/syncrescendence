#!/usr/bin/env python3
"""Capture the current Mac mini constellation revival state into repo-safe artifacts."""

from __future__ import annotations

import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent
STATE_DIR = REPO_ROOT / "00-ORCHESTRATION" / "state"
REMOTE = "mini"
REMOTE_REPO = "/Users/home/syncrescendence"
REMOTE_WORKSPACE = "/Users/home/.openclaw/workspace/AGENTS.md"
REMOTE_GIT = "/opt/homebrew/bin/git"
LAUNCH_AGENT_LABEL = "com.syncrescendence.constellation-stage1"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def run_remote(command: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["ssh", "-o", "BatchMode=yes", REMOTE, command],
        capture_output=True,
        text=True,
        check=False,
    )


def remote_text(command: str) -> str:
    result = run_remote(command)
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def main() -> int:
    STATE_DIR.mkdir(parents=True, exist_ok=True)

    hostname = remote_text("hostname")
    tmux_path = remote_text("PATH=/opt/homebrew/bin:$PATH; command -v tmux")
    openclaw_path = remote_text("PATH=/opt/homebrew/bin:$PATH; command -v openclaw")
    codex_path = remote_text("PATH=/opt/homebrew/bin:$PATH; command -v codex")
    gemini_path = remote_text("PATH=/opt/homebrew/bin:$PATH; command -v gemini")
    repo_present = run_remote(f"test -d {REMOTE_REPO!s}").returncode == 0
    workspace_present = run_remote(f"test -f {REMOTE_WORKSPACE!s}").returncode == 0
    workspace_bytes = remote_text(f"wc -c < {REMOTE_WORKSPACE}")
    windows_text = remote_text("PATH=/opt/homebrew/bin:$PATH; tmux has-session -t constellation 2>/dev/null && tmux list-windows -t constellation || true")
    windows = [line.strip() for line in windows_text.splitlines() if line.strip()]
    launch_agent_probe = run_remote(
        f"launchctl print gui/$(id -u)/{LAUNCH_AGENT_LABEL}"
    )
    launch_agent_present = launch_agent_probe.returncode == 0
    launch_agent_running = "state = running" in (launch_agent_probe.stdout or "")

    git_probe = run_remote(
        f"PATH=/opt/homebrew/bin:$PATH; {REMOTE_GIT} -C {REMOTE_REPO} status --short --branch"
    )
    git_native_ready = git_probe.returncode == 0
    git_probe_error = (git_probe.stderr or git_probe.stdout).strip() if not git_native_ready else ""
    xcode_license_blocked = "xcode license" in git_probe_error.lower()

    payload = {
        "captured_at": utc_now(),
        "remote_alias": REMOTE,
        "hostname": hostname,
        "repo_path": REMOTE_REPO,
        "repo_present": repo_present,
        "psyche_workspace_path": REMOTE_WORKSPACE,
        "psyche_workspace_present": workspace_present,
        "psyche_workspace_bytes": int(workspace_bytes) if workspace_bytes.isdigit() else None,
        "binaries": {
            "tmux": tmux_path or None,
            "openclaw": openclaw_path or None,
            "codex": codex_path or None,
            "gemini": gemini_path or None,
        },
        "constellation_session_present": bool(windows),
        "constellation_windows": windows,
        "launch_agent": {
            "label": LAUNCH_AGENT_LABEL,
            "present": launch_agent_present,
            "running": launch_agent_running,
        },
        "git_native_ready": git_native_ready,
        "xcode_license_blocked": xcode_license_blocked,
        "git_probe_error": git_probe_error or None,
    }

    json_path = STATE_DIR / "MINI-CONSTELLATION-STATUS.json"
    md_path = STATE_DIR / "MINI-CONSTELLATION-STATUS.md"
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Mini Constellation Status",
        "",
        f"- Captured: `{payload['captured_at']}`",
        f"- Remote alias: `{payload['remote_alias']}`",
        f"- Hostname: `{payload['hostname']}`",
        f"- Repo present: `{payload['repo_present']}` at `{payload['repo_path']}`",
        f"- Psyche workspace present: `{payload['psyche_workspace_present']}` at `{payload['psyche_workspace_path']}`",
        f"- Psyche workspace bytes: `{payload['psyche_workspace_bytes']}`",
        f"- tmux path: `{payload['binaries']['tmux']}`",
        f"- OpenClaw path: `{payload['binaries']['openclaw']}`",
        f"- Codex path: `{payload['binaries']['codex']}`",
        f"- Gemini path: `{payload['binaries']['gemini']}`",
        f"- Constellation session present: `{payload['constellation_session_present']}`",
        f"- LaunchAgent present: `{payload['launch_agent']['present']}`",
        f"- LaunchAgent running: `{payload['launch_agent']['running']}`",
        f"- Git-native ready: `{payload['git_native_ready']}`",
        f"- Xcode license blocked: `{payload['xcode_license_blocked']}`",
        "",
        "## tmux Windows",
        "",
    ]
    if windows:
        lines.extend(f"- `{line}`" for line in windows)
    else:
        lines.append("- `none`")
    if payload["git_probe_error"]:
        lines.extend(
            [
                "",
                "## Git Probe Error",
                "",
                "```text",
                payload["git_probe_error"],
                "```",
            ]
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
