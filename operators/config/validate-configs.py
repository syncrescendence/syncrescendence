#!/usr/bin/env python3
"""Validate config source files and manifest coherence."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ABSOLUTE_PATH_RE = re.compile(r"`((?:~|/)[^`\n]+)`")
REPO_PATH_RE = re.compile(r"`([A-Za-z0-9][A-Za-z0-9._/-]*/[A-Za-z0-9._/-]+)`")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_source_paths(repo_root: Path, source: Path) -> list[str]:
    errors: list[str] = []
    text = source.read_text(encoding="utf-8")

    for raw in ABSOLUTE_PATH_RE.findall(text):
        if raw.startswith("/") and raw.count("/") < 2:
            continue
        if raw.startswith("~/.") and not raw.startswith("~/.openclaw/"):
            continue
        expanded = Path(raw).expanduser()
        if raw.startswith("/Users/home/"):
            continue
        if not expanded.exists():
            errors.append(f"{source.name}: missing absolute path {raw}")

    for raw in REPO_PATH_RE.findall(text):
        if raw.startswith(("http://", "https://")):
            continue
        candidate = repo_root / raw
        if candidate.exists():
            continue
        errors.append(f"{source.name}: missing repo path {raw}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="AGENTS.md")
    parser.add_argument("--harness-dir", default="harness")
    parser.add_argument("--machine-dir", default="machine")
    args = parser.parse_args()

    repo_root = Path(args.source).resolve().parent
    harness_dir = repo_root / args.harness_dir
    machine_dir = repo_root / args.machine_dir
    errors: list[str] = []

    source = repo_root / Path(args.source).name
    if not source.exists():
        errors.append(f"Missing source file: {source}")

    targets_path = harness_dir / "targets.json"
    harnesses: dict[str, dict] = {}
    if not targets_path.exists():
        errors.append(f"Missing target manifest: {targets_path}")
        targets = []
    else:
        targets = load_json(targets_path)

    for manifest_path in sorted(harness_dir.glob("*.json")):
        if manifest_path.name == "targets.json":
            continue
        data = load_json(manifest_path)
        name = data.get("name") or manifest_path.stem
        if name in harnesses:
            errors.append(f"Duplicate harness manifest: {name}")
        harnesses[name] = data
        for relative in data.get("extension_sources", []):
            if not (repo_root / relative).exists():
                errors.append(f"{manifest_path.name}: missing extension source {relative}")

    seen_agents: set[str] = set()
    for target in targets:
        agent = target.get("agent")
        harness = target.get("harness")
        if not agent or not harness:
            errors.append(f"Invalid target entry: {target}")
            continue
        if agent in seen_agents:
            errors.append(f"Duplicate target agent: {agent}")
        seen_agents.add(agent)
        if harness not in harnesses:
            errors.append(f"Target {agent} references unknown harness {harness}")
        for section in target.get("source_sections", []):
            if f"## {section}" not in source.read_text(encoding="utf-8"):
                errors.append(f"Target {agent} missing source section {section!r}")
        for relative in target.get("extra_sources", []):
            if not (repo_root / relative).exists():
                errors.append(f"Target {agent} missing extra source {relative}")

    hostnames: set[str] = set()
    for manifest_path in sorted(machine_dir.glob("*.json")):
        data = load_json(manifest_path)
        for hostname in data.get("hostnames", []):
            lowered = hostname.lower()
            if lowered in hostnames:
                errors.append(f"Duplicate machine hostname: {hostname}")
            hostnames.add(lowered)

    sources_to_check = [source]
    for data in harnesses.values():
        for relative in data.get("extension_sources", []):
            sources_to_check.append(repo_root / relative)
    for target in targets:
        for relative in target.get("extra_sources", []):
            sources_to_check.append(repo_root / relative)

    for candidate in sources_to_check:
        if candidate.exists():
            errors.extend(validate_source_paths(repo_root, candidate))

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(
        "Validation passed: source, harness manifests, machine manifests, and referenced paths are coherent."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
