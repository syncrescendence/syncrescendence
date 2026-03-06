#!/usr/bin/env python3
"""Inventory or check the sandbox shell against artifact-law conventions."""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import asdict, dataclass
import argparse
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
STATE_DIR = REPO_ROOT / "orchestration" / "state"
JSON_OUT = STATE_DIR / "ARTIFACT-LAW-INVENTORY.json"
MD_OUT = STATE_DIR / "ARTIFACT-LAW-INVENTORY.md"

ALLOWED_TOP_LEVEL = {
    ".claude",
    ".gemini",
    ".obsidian",
    ".gitattributes",
    ".github",
    ".gitignore",
    "orchestration",
    "AGENTS.md",
    "BOOT.md",
    "CLAUDE.md",
    "CONTINUOUS-IMPROVEMENT.md",
    "GEMINI.md",
    "INTER-OFFICE.md",
    "Makefile",
    "README.md",
    "WORK-LOOP.md",
    "communications",
    "executive",
    "knowledge",
    "memory",
    "offices",
    "operators",
    "pedigree",
    "playbooks",
    "program",
    "runtime",
    "validated-patterns",
}

TRANSITIONAL_ROOT_OPERATORS = {
    "artifact_law_inventory.py",
    "finalize_cowork_relay_job.py",
}

ALLOWED_PROMPT_PREFIXES = ("PROMPT-", "PACKET-")
ALLOWED_PROMPT_DIRS = (
    Path("communications") / "prompts",
)
ALLOWED_RESPONSE_DIRS = (
    Path("communications") / "responses",
)
PEDIGREE_COMMUNICATION_DIRS = (
    Path("pedigree") / "rehoused",
    Path("pedigree") / "originals",
)
TRANSIENT_RESPONSE_DIRS = (
    Path("orchestration") / "relay" / "cowork-v1" / "artifacts" / "outgoing",
)
ALLOWED_HANDOFF_DIRS = (
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
        status = "live"
        note = "prompt-like artifact in the successor-shell prompt lane"
    elif any(path_in_dir(path, allowed) for allowed in PEDIGREE_COMMUNICATION_DIRS):
        status = "pedigree-specimen"
        note = "prompt-like artifact preserved as pedigree rather than live communications"
    else:
        status = "misfiled"
        note = "prompt-like artifact outside approved prompt lanes"
    return Finding(str(path), status, note)


def classify_response(path: Path) -> Finding:
    if any(path_in_dir(path, allowed) for allowed in ALLOWED_RESPONSE_DIRS):
        status = "live"
        note = "response-like artifact in the successor-shell response lane"
    elif any(path_in_dir(path, allowed) for allowed in TRANSIENT_RESPONSE_DIRS):
        status = "transient-runtime"
        note = "response-like artifact in an approved relay staging lane"
    elif any(path_in_dir(path, allowed) for allowed in PEDIGREE_COMMUNICATION_DIRS):
        status = "pedigree-specimen"
        note = "response-like artifact preserved as pedigree rather than live communications"
    else:
        status = "misfiled"
        note = "response-like artifact outside approved response lanes"
    return Finding(str(path), status, note)


def classify_handoff(path: Path) -> Finding:
    if any(path_in_dir(path, allowed) for allowed in ALLOWED_HANDOFF_DIRS):
        status = "live"
        note = "handoff in the successor-shell handoff lane"
    elif any(path_in_dir(path, allowed) for allowed in PEDIGREE_COMMUNICATION_DIRS):
        status = "pedigree-specimen"
        note = "handoff preserved as pedigree rather than live communications"
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


def has_failures(report: dict[str, object]) -> bool:
    if report["unknown_top_level_entries"]:
        return True
    for key in ("prompts", "responses", "handoffs", "root_operators"):
        for finding in report[key]:
            if finding["status"] in {"misfiled", "unexpected-root"}:
                return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", choices=("both", "json", "md"), default="both")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    report = generate_inventory()
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    if args.format in {"both", "json"}:
        JSON_OUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print(f"Wrote {JSON_OUT.relative_to(REPO_ROOT)}")
    if args.format in {"both", "md"}:
        MD_OUT.write_text(render_markdown(report))
        print(f"Wrote {MD_OUT.relative_to(REPO_ROOT)}")
    if args.check and has_failures(report):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
