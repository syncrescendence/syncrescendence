#!/usr/bin/env python3
"""Minimal sandbox-native event bridge for neosyncrescendence."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = REPO_ROOT / "00-ORCHESTRATION" / "state"
LEDGER_PATH = STATE_DIR / "SANDBOX-EVENT-LEDGER.jsonl"


def ensure_state_dir() -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)


def validate_markdown(path: Path, label: str) -> Path:
    resolved = path.resolve()
    if not str(resolved).startswith(str(REPO_ROOT)):
        raise SystemExit(f"{label} must stay inside sandbox root: {path}")
    if not resolved.exists():
        raise SystemExit(f"{label} does not exist: {resolved}")
    if resolved.suffix.lower() != ".md":
        raise SystemExit(f"{label} must be a markdown file: {resolved}")
    return resolved


def repo_rel(path: Path) -> str:
    return str(path.resolve().relative_to(REPO_ROOT))


def emit_event(
    *,
    source: str,
    surface: str,
    artifact_class: str,
    event_type: str,
    summary: str,
    repo_paths: list[str],
    payload: dict,
) -> Path:
    ensure_state_dir()
    event = {
        "id": f"{surface}-{event_type}-{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}",
        "emitted_at": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source": source,
        "surface": surface,
        "artifact_class": artifact_class,
        "type": event_type,
        "summary": summary,
        "repo_paths": repo_paths,
        "payload": payload,
    }
    with LEDGER_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True) + "\n")
    return LEDGER_PATH
