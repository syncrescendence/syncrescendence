#!/usr/bin/env python3
"""Sync live OpenClaw runtime state back into the repo and deploy generated configs safely."""

from __future__ import annotations

import argparse
import json
import subprocess
import shutil
from datetime import UTC, datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent
STATE_DIR = REPO_ROOT / "00-ORCHESTRATION" / "state"
MEMORY_DIR = REPO_ROOT / "memory"
CONFIG_MANIFEST = REPO_ROOT / "configs" / "manifest.json"
OPENCLAW_CONFIG = Path.home() / ".openclaw" / "openclaw.json"
OPENCLAW_WORKSPACE = Path.home() / ".openclaw" / "workspace"
KEYCHAIN_SERVICE = "syncrescendence"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def keychain_item_metadata(account: str) -> dict:
    command = [
        "security",
        "find-generic-password",
        "-s",
        KEYCHAIN_SERVICE,
        "-a",
        account,
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        return {"present": False}

    created_at = None
    modified_at = None
    for line in result.stdout.splitlines():
        if '"cdat"' in line and "202" in line:
            created_at = line.split('"')[-2].replace("\\000", "")
        if '"mdat"' in line and "202" in line:
            modified_at = line.split('"')[-2].replace("\\000", "")
    return {
        "present": True,
        "created_at": created_at,
        "modified_at": modified_at,
    }


def channel_runtime_summary(name: str, data: dict) -> dict:
    summary = {
        "enabled": bool(data.get("enabled")),
    }
    for key in ("mode", "groupPolicy", "dmPolicy", "streaming", "nativeStreaming", "webhookPath"):
        if key in data:
            summary[key] = data.get(key)

    if name == "slack":
        summary["bot_token_configured"] = bool(data.get("botToken"))
        summary["app_token_configured"] = bool(data.get("appToken"))
        summary["bot_token_keychain"] = keychain_item_metadata("slack-bot-token")
        summary["app_token_keychain"] = keychain_item_metadata("slack-app-token")
    elif name == "discord":
        summary["bot_token_configured"] = bool(data.get("token"))
        summary["bot_token_keychain"] = keychain_item_metadata("discord-bot-token")
    return summary


def get_target(agent: str) -> dict:
    manifest = read_json(CONFIG_MANIFEST)
    for target in manifest["targets"]:
        if target["agent"] == agent:
            return target
    raise SystemExit(f"Agent {agent!r} not found in configs/manifest.json")


def deploy_agent(agent: str, backup: bool) -> Path:
    target = get_target(agent)
    workspace_path = target.get("openclaw_workspace")
    if not workspace_path:
        raise SystemExit(f"Agent {agent!r} has no configured OpenClaw workspace path")

    source = REPO_ROOT / "configs" / target["generated"]
    destination = Path(workspace_path).expanduser()
    destination.parent.mkdir(parents=True, exist_ok=True)

    if backup and destination.exists():
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_path = destination.with_suffix(destination.suffix + f".bak.{stamp}")
        shutil.copyfile(destination, backup_path)

    shutil.copyfile(source, destination)
    return destination


def collect_runtime(agent: str) -> dict:
    openclaw = read_json(OPENCLAW_CONFIG) if OPENCLAW_CONFIG.exists() else {}
    workspace_agents = (OPENCLAW_WORKSPACE / "AGENTS.md").read_text(encoding="utf-8") if (OPENCLAW_WORKSPACE / "AGENTS.md").exists() else ""
    workspace_memory = (OPENCLAW_WORKSPACE / "MEMORY.md").read_text(encoding="utf-8") if (OPENCLAW_WORKSPACE / "MEMORY.md").exists() else ""
    skills_dir = Path.home() / ".openclaw" / "skills"
    installed_skills = sorted(path.name for path in skills_dir.iterdir() if path.is_dir()) if skills_dir.exists() else []

    channels = openclaw.get("channels", {})
    defaults = openclaw.get("agents", {}).get("defaults", {})
    gateway = openclaw.get("gateway", {})

    return {
        "captured_at": utc_now(),
        "agent": agent,
        "model_primary": defaults.get("model", {}).get("primary"),
        "workspace_path": defaults.get("workspace"),
        "tools_deny": openclaw.get("tools", {}).get("deny", []),
        "browser_enabled": "browser" not in openclaw.get("tools", {}).get("deny", []),
        "skills_installed": installed_skills,
        "gateway": {
            "port": gateway.get("port"),
            "bind": gateway.get("bind"),
            "mode": gateway.get("mode"),
        },
        "channels": {name: channel_runtime_summary(name, data) for name, data in channels.items()},
        "workspace_agents_excerpt": workspace_agents[:4000],
        "workspace_memory_excerpt": workspace_memory[:4000],
    }


def write_runtime_snapshot(runtime: dict) -> tuple[Path, Path]:
    json_path = STATE_DIR / "OPENCLAW-RUNTIME-SNAPSHOT.json"
    md_path = STATE_DIR / "OPENCLAW-RUNTIME-SNAPSHOT.md"
    STATE_DIR.mkdir(parents=True, exist_ok=True)

    json_path.write_text(json.dumps(runtime, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# OpenClaw Runtime Snapshot",
        "",
        f"- Captured: `{runtime['captured_at']}`",
        f"- Agent focus: `{runtime['agent']}`",
        f"- Primary model: `{runtime.get('model_primary')}`",
        f"- Workspace path: `{runtime.get('workspace_path')}`",
        f"- Browser enabled: `{runtime.get('browser_enabled')}`",
        f"- Tools denied: `{', '.join(runtime.get('tools_deny', []))}`",
        f"- Installed skills: `{', '.join(runtime.get('skills_installed', [])) or 'none'}`",
        f"- Gateway: `bind={runtime['gateway'].get('bind')}` `port={runtime['gateway'].get('port')}` `mode={runtime['gateway'].get('mode')}`",
        "",
        "## Channels",
        "",
    ]
    for name, data in runtime["channels"].items():
        details = [f"enabled={data.get('enabled')}"]
        for key in ("mode", "groupPolicy", "dmPolicy", "streaming"):
            if key in data:
                details.append(f"{key}={data.get(key)}")
        if name == "slack":
            details.append(f"botTokenConfigured={data.get('bot_token_configured')}")
            details.append(f"appTokenConfigured={data.get('app_token_configured')}")
            details.append(f"botTokenKeychain={data.get('bot_token_keychain', {}).get('present')}")
            details.append(f"appTokenKeychain={data.get('app_token_keychain', {}).get('present')}")
        if name == "discord":
            details.append(f"botTokenConfigured={data.get('bot_token_configured')}")
            details.append(f"botTokenKeychain={data.get('bot_token_keychain', {}).get('present')}")
        lines.append(f"- `{name}` " + " ".join(f"`{item}`" for item in details))
    lines.extend(
        [
            "",
            "## Workspace Excerpts",
            "",
            "### AGENTS.md",
            "```md",
            runtime["workspace_agents_excerpt"].rstrip(),
            "```",
            "",
            "### MEMORY.md",
            "```md",
            runtime["workspace_memory_excerpt"].rstrip(),
            "```",
            "",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, md_path


def write_tool_stack_live_state(runtime: dict) -> Path:
    path = STATE_DIR / "TOOL-STACK-LIVE-STATE.md"
    slack = runtime["channels"].get("slack", {})
    discord = runtime["channels"].get("discord", {})
    lines = [
        "# Tool Stack Live State",
        "",
        f"**Date**: {runtime['captured_at'][:10]}  ",
        "**Purpose**: factual live runtime snapshot for repo↔harness reconciliation  ",
        "**Status**: ACTIVE reference for current tool-stack truth",
        "",
        "---",
        "",
        "## Live Runtime Facts",
        "",
        "- `syncrescendence.com` is secured",
        f"- OpenClaw gateway is live on the MacBook Air at `127.0.0.1:{runtime['gateway'].get('port')}`",
        f"- Ajna's current primary model in live OpenClaw config is `{runtime.get('model_primary')}`",
        f"- OpenClaw workspace path is `{runtime.get('workspace_path')}`",
        f"- Browser is {'not denied' if runtime.get('browser_enabled') else 'disabled'} in OpenClaw",
        f"- Ajna has `{', '.join(runtime.get('skills_installed', [])) or 'no extra'}` skill(s) installed",
        f"- Slack channel is currently {'enabled' if slack.get('enabled') else 'disabled'}",
        f"- Discord channel is currently {'enabled' if discord.get('enabled') else 'disabled'}",
        f"- Slack socket mode tokens are configured in runtime: bot=`{slack.get('bot_token_configured')}` app=`{slack.get('app_token_configured')}`",
        f"- Slack keychain entries are present: bot=`{slack.get('bot_token_keychain', {}).get('present')}` app=`{slack.get('app_token_keychain', {}).get('present')}`",
        f"- Discord bot token is configured in runtime: `{discord.get('bot_token_configured')}`",
        f"- Discord keychain entry is present: `{discord.get('bot_token_keychain', {}).get('present')}`",
        "- `exec`, `process`, and `apply_patch` remain denied in OpenClaw",
        "- Rendered + validated config scaffold now exists locally:",
        "  - `harness/*.json`",
        "  - `machine/*.json`",
        "  - `render-configs.py`",
        "  - `validate-configs.py`",
        "  - `configs/manifest.json`",
        "- OpenClaw repo↔runtime tooling now exists locally:",
        "  - `make deploy-ajna`",
        "  - `make sync-openclaw`",
        "  - `sync-openclaw.py`",
        "  - `00-ORCHESTRATION/state/OPENCLAW-RUNTIME-SNAPSHOT.md`",
        "  - `memory/AJNA-RUNTIME-SYNTHESIS.md`",
        "- Ajna event reconciliation now exists locally:",
        "  - `make reconcile-ajna-events`",
        "  - `reconcile-ajna-events.py`",
        "  - `memory/AJNA-EVENT-LEDGER.jsonl`",
        "  - `memory/AJNA-EVENT-SUMMARY.md`",
        "  - `00-ORCHESTRATION/state/AJNA-EVENT-RECONCILIATION.json`",
        "- Ajna's OpenClaw workspace instruction surface has been compacted below the 20k bootstrap ceiling",
        "",
        "## Current Truth Split",
        "",
        "- Repo constitutional/orientation docs have been partially reconciled, but historical artifacts still narrate Ajna as Kimi-primary",
        "- Live OpenClaw runtime has already moved Ajna onto Claude Sonnet",
        "- Config scaffold is implemented in-repo and Ajna workspace deployment is now repo-driven",
        "- Memory remains split across repo memory, OpenClaw workspace memory, and session logs, but there is now a first synthesis loop back into repo memory",
        "- Ajna can now emit durable event files into a landing zone that Commander reconciles into repo state",
        "",
        "## Immediate Blockers",
        "",
        "1. The current sync loop is snapshot-first and still needs richer normalization rules",
        "2. Memory synthesis is still first-pass and not yet canon-promotion aware",
        "3. Historical documents still preserve pre-rewire Ajna/Kimi assumptions",
        "4. Public ontology cutover still depends on DNS / edge for `syncrescendence.com`",
        "5. OpenClaw stores active channel credentials in local runtime config; repo truth remains pointer-only and repo-safe",
        "",
        "## Authority",
        "",
        "- Strategic architecture: `engine/CC65-TOOL-STACK-FINAL.md`",
        "- Current narrowing brief: `engine/CC72b-IMPLEMENTATION-BRIEF.md`",
        "- This file is the factual runtime snapshot, not the long-term architecture",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def synthesize_memory(runtime: dict) -> Path:
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    path = MEMORY_DIR / "AJNA-RUNTIME-SYNTHESIS.md"
    slack = runtime["channels"].get("slack", {})
    discord = runtime["channels"].get("discord", {})
    lines = [
        "# Ajna Runtime Synthesis",
        "",
        f"**Captured**: {runtime['captured_at']}",
        "",
        "## Stable Facts",
        "",
        f"- Ajna primary model: `{runtime.get('model_primary')}`",
        f"- OpenClaw workspace: `{runtime.get('workspace_path')}`",
        f"- Browser enabled: `{runtime.get('browser_enabled')}`",
        f"- Installed skills: `{', '.join(runtime.get('skills_installed', [])) or 'none'}`",
        "",
        "## Current Constraints",
        "",
        f"- Denied tools: `{', '.join(runtime.get('tools_deny', []))}`",
    ]
    lines.extend(
        [
            f"- Channel `slack` enabled: `{slack.get('enabled')}`",
            f"- Channel `discord` enabled: `{discord.get('enabled')}`",
            f"- Slack runtime token presence: bot=`{slack.get('bot_token_configured')}` app=`{slack.get('app_token_configured')}`",
            f"- Slack keychain presence: bot=`{slack.get('bot_token_keychain', {}).get('present')}` app=`{slack.get('app_token_keychain', {}).get('present')}`",
            f"- Discord runtime token presence: bot=`{discord.get('bot_token_configured')}`",
            f"- Discord keychain presence: bot=`{discord.get('bot_token_keychain', {}).get('present')}`",
        ]
    )
    lines.extend(
        [
            "",
            "## Operational Reading",
            "",
            "- Ajna is browser-capable and repo-grounded.",
            "- Runtime remains conservative: browser is available, shell mutation remains denied in OpenClaw.",
            "- Slack and Discord are now live in runtime, but their durable description must remain pointer-only and repo-safe.",
            "- Durable decisions should be promoted from workspace memory into repo artifacts rather than living only in runtime files.",
            "",
            "## Next Actions",
            "",
            "- Use `make deploy-ajna` after repo-side OpenClaw instruction updates.",
            "- Run `make sync-openclaw` after meaningful runtime changes or browser/OAuth milestones.",
            "- Keep ontology/exocortex design separate until the boundary contract is settled.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", default="ajna")
    parser.add_argument("--snapshot", action="store_true")
    parser.add_argument("--deploy", action="store_true")
    parser.add_argument("--synthesize-memory", action="store_true")
    parser.add_argument("--no-backup", action="store_true")
    args = parser.parse_args()

    ran = False
    if args.deploy:
        destination = deploy_agent(args.agent, backup=not args.no_backup)
        print(f"Deployed generated config to {destination}")
        ran = True

    runtime = None
    if args.snapshot or args.synthesize_memory:
        runtime = collect_runtime(args.agent)
        ran = True

    if args.snapshot and runtime is not None:
        json_path, md_path = write_runtime_snapshot(runtime)
        live_state_path = write_tool_stack_live_state(runtime)
        print(f"Wrote runtime snapshots to {json_path} and {md_path}")
        print(f"Wrote live-state snapshot to {live_state_path}")

    if args.synthesize_memory and runtime is not None:
        memory_path = synthesize_memory(runtime)
        print(f"Wrote memory synthesis to {memory_path}")

    if not ran:
        parser.error("Specify at least one action: --deploy, --snapshot, or --synthesize-memory")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
