#!/usr/bin/env python3
"""Normalize legacy event ledger records to the current multi-source contract."""

from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent
LEDGER_PATH = REPO_ROOT / "memory" / "AJNA-EVENT-LEDGER.jsonl"
REPORT_PATH = REPO_ROOT / "00-ORCHESTRATION" / "state" / "EVENT-LEDGER-NORMALIZATION.json"


def normalize(event: dict) -> tuple[dict, list[str]]:
    changes: list[str] = []

    event_id = str(event.get("id", ""))
    if event_id.startswith("commander-") and event.get("source") == "ajna":
        event["source"] = "commander"
        changes.append("source: ajna -> commander")

    if event.get("type") == "browser_state_check":
        if "surface" not in event:
            event["surface"] = "browser"
            changes.append("surface: browser")
        if "artifact_class" not in event:
            event["artifact_class"] = "browser_action"
            changes.append("artifact_class: browser_action")
        if "durable_capture" not in event:
            event["durable_capture"] = "summary_markdown"
            changes.append("durable_capture: summary_markdown")

    return event, changes


def main() -> int:
    rows = []
    if LEDGER_PATH.exists():
        rows = [json.loads(line) for line in LEDGER_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]

    normalized: list[dict] = []
    report: dict[str, list[str]] = {}
    for row in rows:
        updated, changes = normalize(row)
        normalized.append(updated)
        if changes:
            report[updated["id"]] = changes

    LEDGER_PATH.write_text(
        "\n".join(json.dumps(row, sort_keys=True) for row in normalized) + ("\n" if normalized else ""),
        encoding="utf-8",
    )
    REPORT_PATH.write_text(json.dumps({"normalized": report}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Normalized {len(report)} legacy event records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
