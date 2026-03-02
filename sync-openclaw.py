#!/usr/bin/env python3
"""Sync live OpenClaw runtime state back into the repo and deploy generated configs safely."""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import UTC, datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent
STATE_DIR = REPO_ROOT / "00-ORCHESTRATION" / "state"
MEMORY_DIR = REPO_ROOT / "memory"
CONFIG_MANIFEST = REPO_ROOT / "configs" / "manifest.json"
OPENCLAW_CONFIG = Path.home() / ".openclaw" / "openclaw.json"
OPENCLAW_WORKSPACE = Path.home() / ".openclaw" / "workspace"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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
        "channels": {
            name: {"enabled": data.get("enabled")}
            for name, data in channels.items()
        },
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
        lines.append(f"- `{name}` enabled: `{data.get('enabled')}`")
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


def synthesize_memory(runtime: dict) -> Path:
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    path = MEMORY_DIR / "AJNA-RUNTIME-SYNTHESIS.md"
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
    for name, data in runtime["channels"].items():
        lines.append(f"- Channel `{name}` enabled: `{data.get('enabled')}`")
    lines.extend(
        [
            "",
            "## Operational Reading",
            "",
            "- Ajna is browser-capable and repo-grounded.",
            "- Runtime remains conservative: browser is available, shell mutation remains denied in OpenClaw.",
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
        print(f"Wrote runtime snapshots to {json_path} and {md_path}")

    if args.synthesize_memory and runtime is not None:
        memory_path = synthesize_memory(runtime)
        print(f"Wrote memory synthesis to {memory_path}")

    if not ran:
        parser.error("Specify at least one action: --deploy, --snapshot, or --synthesize-memory")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
