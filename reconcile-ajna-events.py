#!/usr/bin/env python3
"""Ingest Ajna event files from the OpenClaw workspace into repo state."""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import UTC, datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent
WORKSPACE_ROOT = Path.home() / ".openclaw" / "workspace"
EVENTS_ROOT = WORKSPACE_ROOT / "events"
INBOX_DIR = EVENTS_ROOT / "inbox"
ARCHIVE_DIR = EVENTS_ROOT / "archive"
FAILED_DIR = EVENTS_ROOT / "failed"

LEDGER_PATH = REPO_ROOT / "memory" / "AJNA-EVENT-LEDGER.jsonl"
SUMMARY_PATH = REPO_ROOT / "memory" / "AJNA-EVENT-SUMMARY.md"
STATE_PATH = REPO_ROOT / "00-ORCHESTRATION" / "state" / "AJNA-EVENT-RECONCILIATION.json"

REQUIRED_FIELDS = {"id", "emitted_at", "source", "type", "summary", "capture_level", "payload"}
VALID_CAPTURE_LEVELS = {"pointer", "summary", "full"}


def ensure_dirs() -> None:
    for path in (INBOX_DIR, ARCHIVE_DIR, FAILED_DIR, LEDGER_PATH.parent, SUMMARY_PATH.parent, STATE_PATH.parent):
        path.mkdir(parents=True, exist_ok=True)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_existing_ids() -> set[str]:
    if not LEDGER_PATH.exists():
        return set()
    seen: set[str] = set()
    for line in LEDGER_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            seen.add(json.loads(line)["id"])
        except Exception:
            continue
    return seen


def validate_event(event: dict, path: Path) -> list[str]:
    errors: list[str] = []
    missing = REQUIRED_FIELDS - event.keys()
    if missing:
        errors.append(f"{path.name}: missing fields {sorted(missing)}")
    if event.get("source") != "ajna":
        errors.append(f"{path.name}: source must be 'ajna'")
    if event.get("capture_level") not in VALID_CAPTURE_LEVELS:
        errors.append(f"{path.name}: invalid capture_level {event.get('capture_level')!r}")
    if not isinstance(event.get("payload"), dict):
        errors.append(f"{path.name}: payload must be an object")
    if not isinstance(event.get("summary"), str):
        errors.append(f"{path.name}: summary must be a string")
    return errors


def write_summary(events: list[dict]) -> None:
    lines = [
        "# Ajna Event Summary",
        "",
        f"**Updated**: {utc_now()}",
        "",
        "## Recent Events",
        "",
    ]
    if not events:
        lines.append("- No Ajna events reconciled yet.")
    else:
        for event in events[-10:][::-1]:
            lines.extend(
                [
                    f"### {event['id']}",
                    f"- Emitted: `{event['emitted_at']}`",
                    f"- Type: `{event['type']}`",
                    f"- Capture level: `{event['capture_level']}`",
                    f"- Summary: {event['summary']}",
                    "",
                ]
            )
    SUMMARY_PATH.write_text("\n".join(lines), encoding="utf-8")


def load_recent_events() -> list[dict]:
    if not LEDGER_PATH.exists():
        return []
    events: list[dict] = []
    for line in LEDGER_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except Exception:
            continue
    return events


def write_state(processed: list[str], failed: list[str], skipped: list[str]) -> None:
    state = {
        "last_run_at": utc_now(),
        "processed_count": len(processed),
        "processed_ids": processed,
        "failed_count": len(failed),
        "failed_files": failed,
        "skipped_duplicates": skipped,
    }
    STATE_PATH.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def archive_file(path: Path, destination_dir: Path) -> None:
    destination = destination_dir / path.name
    if destination.exists():
        destination = destination_dir / f"{path.stem}-{int(datetime.now().timestamp())}{path.suffix}"
    shutil.move(str(path), str(destination))


def reconcile() -> int:
    ensure_dirs()
    existing_ids = load_existing_ids()
    processed: list[str] = []
    failed: list[str] = []
    skipped: list[str] = []

    for path in sorted(INBOX_DIR.glob("*.json")):
        try:
            event = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            failed.append(path.name)
            archive_file(path, FAILED_DIR)
            continue

        errors = validate_event(event, path)
        if errors:
            failed.append(path.name)
            archive_file(path, FAILED_DIR)
            continue

        if event["id"] in existing_ids:
            skipped.append(event["id"])
            archive_file(path, ARCHIVE_DIR)
            continue

        normalized = {
            "id": event["id"],
            "emitted_at": event["emitted_at"],
            "source": event["source"],
            "type": event["type"],
            "capture_level": event["capture_level"],
            "summary": event["summary"],
            "repo_paths": event.get("repo_paths", []),
            "ontology_entities": event.get("ontology_entities", []),
            "payload": event["payload"],
            "reconciled_at": utc_now(),
        }
        with LEDGER_PATH.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(normalized, sort_keys=True) + "\n")
        processed.append(event["id"])
        existing_ids.add(event["id"])
        archive_file(path, ARCHIVE_DIR)

    write_state(processed, failed, skipped)
    write_summary(load_recent_events())

    print(f"Processed: {len(processed)}")
    print(f"Failed: {len(failed)}")
    print(f"Skipped duplicates: {len(skipped)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ensure-dirs", action="store_true")
    args = parser.parse_args()
    ensure_dirs()
    if args.ensure_dirs:
        print(f"Ensured event directories under {EVENTS_ROOT}")
        return 0
    return reconcile()


if __name__ == "__main__":
    raise SystemExit(main())
