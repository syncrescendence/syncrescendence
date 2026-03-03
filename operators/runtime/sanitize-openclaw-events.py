#!/usr/bin/env python3
"""Audit and sanitize OpenClaw runtime event files for secret material."""

from __future__ import annotations

import argparse
import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent
WORKSPACE_ROOT = Path.home() / ".openclaw" / "workspace"
EVENTS_ROOT = WORKSPACE_ROOT / "events"
REPORT_PATH = REPO_ROOT / "00-ORCHESTRATION" / "state" / "OPENCLAW-EVENT-SANITIZATION.json"

SENSITIVE_KEYS = {
    "access_token",
    "api_key",
    "app_token",
    "authorization",
    "bot_token",
    "cookie",
    "cookies",
    "key_value",
    "password",
    "refresh_token",
    "secret",
    "token",
}

SENSITIVE_VALUE_PATTERNS = [
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    re.compile(r"\bBearer\s+[A-Za-z0-9._-]{16,}\b", re.IGNORECASE),
]


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def canonical_key(key: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", key.lower()).strip("_")


def redact_string(value: str) -> tuple[str, bool]:
    updated = value
    changed = False
    for pattern in SENSITIVE_VALUE_PATTERNS:
        updated, count = pattern.subn("<REDACTED>", updated)
        changed = changed or count > 0
    return updated, changed


def sanitize_value(value: Any, parent_key: str | None = None) -> tuple[Any, list[str]]:
    redacted_keys: list[str] = []

    if isinstance(value, dict):
        updated: dict[str, Any] = {}
        for key, nested in value.items():
            normalized = canonical_key(str(key))
            if normalized in SENSITIVE_KEYS:
                updated[key] = "<REDACTED>"
                redacted_keys.append(str(key))
                continue
            sanitized, nested_keys = sanitize_value(nested, parent_key=str(key))
            updated[key] = sanitized
            redacted_keys.extend(nested_keys)
        return updated, redacted_keys

    if isinstance(value, list):
        updated_list: list[Any] = []
        for item in value:
            sanitized, nested_keys = sanitize_value(item, parent_key=parent_key)
            updated_list.append(sanitized)
            redacted_keys.extend(nested_keys)
        return updated_list, redacted_keys

    if isinstance(value, str):
        sanitized, changed = redact_string(value)
        if changed and parent_key is not None:
            redacted_keys.append(parent_key)
        return sanitized, redacted_keys

    return value, redacted_keys


def event_paths() -> list[Path]:
    files: list[Path] = []
    for subdir in ("inbox", "archive", "failed"):
        root = EVENTS_ROOT / subdir
        if not root.exists():
            continue
        files.extend(sorted(root.glob("*.json")))
    return files


def sanitize_event_file(path: Path, apply: bool) -> dict[str, Any]:
    try:
        original = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {
            "path": str(path),
            "status": "invalid_json",
            "redacted_keys": [],
            "changed": False,
        }

    sanitized, redacted_keys = sanitize_value(original)
    changed = sanitized != original

    if apply and changed:
        path.write_text(json.dumps(sanitized, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return {
        "path": str(path),
        "status": "sanitized" if changed else "clean",
        "redacted_keys": sorted(set(redacted_keys)),
        "changed": changed,
    }


def write_report(results: list[dict[str, Any]], apply: bool) -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "generated_at": utc_now(),
        "mode": "apply" if apply else "check",
        "workspace_root": str(WORKSPACE_ROOT),
        "files_scanned": len(results),
        "files_changed": sum(1 for item in results if item["changed"]),
        "results": results,
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Redact secrets in place and write the report.")
    args = parser.parse_args()

    results = [sanitize_event_file(path, apply=args.apply) for path in event_paths()]
    write_report(results, apply=args.apply)

    changed = sum(1 for item in results if item["changed"])
    print(
        f"Scanned {len(results)} runtime event file(s); "
        f"{'redacted' if args.apply else 'would redact'} secrets in {changed} file(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
