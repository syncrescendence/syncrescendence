#!/usr/bin/env python3
"""Inventory the current repo shell against artifact-law conventions.

This is intentionally inventory-mode only. It reports drift but does not fail
the build or mutate the worktree.
"""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent
STATE_DIR = REPO_ROOT / "00-ORCHESTRATION" / "state"
JSON_OUT = STATE_DIR / "ARTIFACT-LAW-INVENTORY.json"
MD_OUT = STATE_DIR / "ARTIFACT-LAW-INVENTORY.md"

ALLOWED_TOP_LEVEL = {
    "-INBOX",
    ".claude",
    ".github",
    ".openclaw",
    "00-ORCHESTRATION",
    "AGENTS.md",
    "CLAUDE-EXT.md",
    "CLAUDE.md",
    "CLI-WEB-GAP",
    "GEMINI-EXT.md",
    "GEMINI.md",
    "HEARTBEAT.md",
    "IDENTITY.md",
    "Makefile",
    "OPENCLAW-EXT.md",
    "README.md",
    "SOUL.md",
    "TOOLS.md",
    "USER.md",
    "agents",
    "ascertescence",
    "canon",
    "configs",
    "corpus",
    "engine",
    "harness",
    "machine",
    "memory",
    "neocorpus",
    ".env.graphiti",
    ".gitattributes",
    ".gitignore",
}

TRANSITIONAL_ROOT_OPERATORS = {
    "artifact_law_inventory.py",
    "bootstrap-mac-mini.sh",
    "channel_surface_bridge.py",
    "cloudflare_domain_bridge.py",
    "collect-mini-constellation-status.py",
    "collect-tooling-surface-status.py",
    "constellation-mini-stage1.sh",
    "exocortex_event_bridge.py",
    "finalize_cowork_relay_job.py",
    "github_issue_bridge.py",
    "google_model_bridge.py",
    "hydrate-openclaw-channels.py",
    "install-mini-constellation-launchagent.sh",
    "manus_checkpoint_bridge.py",
    "normalize_event_ledger.py",
    "obsidian_repo_bridge.py",
    "ontology_v1.py",
    "reconcile-ajna-events.py",
    "render-configs.py",
    "sanitize-openclaw-events.py",
    "sync-openclaw.py",
    "validate-configs.py",
    "xai_model_bridge.py",
    "youtube_feed_bridge.py",
}

ALLOWED_PROMPT_PREFIXES = ("PROMPT-", "PACKET-")
ALLOWED_PROMPT_DIRS = (
    Path("engine"),
    Path("communications") / "prompts",
)
ALLOWED_RESPONSE_DIRS = (
    Path("-INBOX"),
    Path("communications") / "responses",
)
ALLOWED_HANDOFF_DIRS = (
    Path("agents") / "commander" / "outbox" / "handoffs",
    Path("communications") / "handoffs",
)

IGNORED_DIR_NAMES = {
    ".git",
    "__pycache__",
}


@dataclass
class Finding:
    path: str
    status: str
    note: str


def path_in_dir(path: Path, candidate: Path) -> bool:
    parts = path.parts
    cand = candidate.parts
    return parts[: len(cand)] == cand


def classify_prompt(path: Path) -> Finding:
    if any(path_in_dir(path, allowed) for allowed in ALLOWED_PROMPT_DIRS):
        status = "live" if path.parts[0] == "engine" else "future-lane"
        note = "prompt-like artifact in an allowed or successor lane"
    else:
        status = "misfiled"
        note = "prompt-like artifact outside approved prompt lanes"
    return Finding(str(path), status, note)


def classify_response(path: Path) -> Finding:
    if any(path_in_dir(path, allowed) for allowed in ALLOWED_RESPONSE_DIRS):
        status = "transitional" if path.parts[0] == "-INBOX" else "future-lane"
        note = "response-like artifact in transitional or successor response lane"
    else:
        status = "misfiled"
        note = "response-like artifact outside approved response lanes"
    return Finding(str(path), status, note)


def classify_handoff(path: Path) -> Finding:
    if any(path_in_dir(path, allowed) for allowed in ALLOWED_HANDOFF_DIRS):
        status = "live" if "agents" in path.parts else "future-lane"
        note = "handoff in approved live or successor lane"
    else:
        status = "misfiled"
        note = "handoff outside approved handoff lanes"
    return Finding(str(path), status, note)


def classify_root_operator(path: Path) -> Finding:
    if path.name in TRANSITIONAL_ROOT_OPERATORS:
        return Finding(
            str(path),
            "transitional-root",
            "root-level operator is allowlisted as transitional during shell redesign",
        )
    return Finding(
        str(path),
        "unexpected-root",
        "root-level operator is not in the transitional allowlist",
    )


def iter_repo_files() -> list[Path]:
    files: list[Path] = []
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(REPO_ROOT)
        if any(part in IGNORED_DIR_NAMES for part in rel.parts):
            continue
        files.append(rel)
    return files


def generate_inventory() -> dict[str, object]:
    files = iter_repo_files()

    prompts: list[Finding] = []
    responses: list[Finding] = []
    handoffs: list[Finding] = []
    root_operators: list[Finding] = []

    top_level_entries = sorted(
        path.name
        for path in REPO_ROOT.iterdir()
        if path.name not in {".DS_Store", ".git"}
    )
    unknown_top_level = [
        name
        for name in top_level_entries
        if name not in ALLOWED_TOP_LEVEL and name not in TRANSITIONAL_ROOT_OPERATORS
    ]

    for rel in files:
        name = rel.name
        if name.startswith(ALLOWED_PROMPT_PREFIXES):
            prompts.append(classify_prompt(rel))
        if name.startswith("RESPONSE-"):
            responses.append(classify_response(rel))
        if name.startswith("HANDOFF-"):
            handoffs.append(classify_handoff(rel))
        if len(rel.parts) == 1 and rel.suffix in {".py", ".sh"}:
            root_operators.append(classify_root_operator(rel))

    summary = {
        "prompt_like": len(prompts),
        "response_like": len(responses),
        "handoff_like": len(handoffs),
        "root_operators": len(root_operators),
        "unknown_top_level_entries": len(unknown_top_level),
    }

    buckets: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for category, findings in (
        ("prompts", prompts),
        ("responses", responses),
        ("handoffs", handoffs),
        ("root_operators", root_operators),
    ):
        for finding in findings:
            buckets[category][finding.status] += 1

    return {
        "summary": summary,
        "top_level_entries": top_level_entries,
        "unknown_top_level_entries": unknown_top_level,
        "prompts": [asdict(item) for item in prompts],
        "responses": [asdict(item) for item in responses],
        "handoffs": [asdict(item) for item in handoffs],
        "root_operators": [asdict(item) for item in root_operators],
        "status_buckets": {key: dict(value) for key, value in buckets.items()},
    }


def render_markdown(report: dict[str, object]) -> str:
    summary = report["summary"]
    lines = [
        "# Artifact Law Inventory",
        "",
        "Inventory-mode report for the current shell against the redesign package.",
        "",
        "## Summary",
        "",
        f"- Prompt-like artifacts: {summary['prompt_like']}",
        f"- Response-like artifacts: {summary['response_like']}",
        f"- Handoff-like artifacts: {summary['handoff_like']}",
        f"- Root-level operators: {summary['root_operators']}",
        f"- Unknown top-level entries: {summary['unknown_top_level_entries']}",
        "",
        "## Status Buckets",
        "",
    ]

    for category, buckets in report["status_buckets"].items():
        lines.append(f"### {category}")
        for status, count in sorted(buckets.items()):
            lines.append(f"- `{status}`: {count}")
        lines.append("")

    if report["unknown_top_level_entries"]:
        lines.extend(
            [
                "## Unknown Top-Level Entries",
                "",
            ]
        )
        for entry in report["unknown_top_level_entries"]:
            lines.append(f"- `{entry}`")
        lines.append("")

    def add_findings_section(title: str, findings: list[dict[str, str]]) -> None:
        lines.extend([f"## {title}", ""])
        if not findings:
            lines.append("- none")
            lines.append("")
            return
        for finding in findings:
            lines.append(
                f"- `{finding['status']}` [{finding['path']}](/Users/system/syncrescendence/{finding['path']}): {finding['note']}"
            )
        lines.append("")

    add_findings_section("Prompt Findings", report["prompts"])
    add_findings_section("Response Findings", report["responses"])
    add_findings_section("Handoff Findings", report["handoffs"])
    add_findings_section("Root Operator Findings", report["root_operators"])

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    report = generate_inventory()
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    MD_OUT.write_text(render_markdown(report))
    print(f"Wrote {JSON_OUT.relative_to(REPO_ROOT)}")
    print(f"Wrote {MD_OUT.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
