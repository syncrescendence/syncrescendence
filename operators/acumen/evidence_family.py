#!/usr/bin/env python3
"""Shared helpers for the Acumen evidence family."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]

TRIAGE_LEDGER_PATH = REPO_ROOT / "orchestration" / "state" / "registry" / "acumen-triage-decision-ledger.jsonl"
TRAINING_LEDGER_PATH = REPO_ROOT / "orchestration" / "state" / "registry" / "acumen-training-corpus-ledger.jsonl"
TRIAGE_RUNTIME_PATH = REPO_ROOT / "runtime" / "acumen" / "triage-decisions.jsonl"
TRAINING_RUNTIME_PATH = REPO_ROOT / "runtime" / "acumen" / "training-corpus.jsonl"
CONTRACT_PATH = REPO_ROOT / "orchestration" / "state" / "impl" / "ACUMEN-TRIAGE-EVIDENCE-CONTRACT-v1.md"

TRIAGE_FAMILY_ID = "acumen_triage_decision"
TRAINING_FAMILY_ID = "acumen_model_call_training_corpus"
TRIAGE_LEDGER_SCHEMA = "acumen-triage-decision-ledger-event/v1"
TRAINING_LEDGER_SCHEMA = "acumen-training-corpus-ledger-event/v1"

FORBIDDEN_KEYS = {
    "api_key",
    "apikey",
    "authorization",
    "authorization_header",
    "raw_prompt",
    "prompt_text",
    "prompt_body",
    "system_prompt",
    "raw_response",
    "response_text",
    "response_body",
}
FORBIDDEN_SUBSTRINGS = (
    "Bearer ",
    "AIza",
    "x-goog-api-key",
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def canonical_json_bytes(payload: Any) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def sha256_for_payload(payload: Any) -> str:
    digest = hashlib.sha256()
    digest.update(canonical_json_bytes(payload))
    return f"sha256:{digest.hexdigest()}"


def sha256_for_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return f"sha256:{digest.hexdigest()}"


def repo_rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def repo_path_string(raw_value: str | None) -> str | None:
    if raw_value is None:
        return None
    path = Path(raw_value).expanduser()
    if path.is_absolute():
        try:
            return repo_rel(path.resolve())
        except ValueError:
            return str(path)
    return str(path)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        payload = json.loads(line)
        if not isinstance(payload, dict):
            raise ValueError(f"{repo_rel(path)}:{line_number} must be a JSON object")
        rows.append(payload)
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(row, sort_keys=True, ensure_ascii=True) for row in rows]
    path.write_text("\n".join(lines).rstrip() + ("\n" if lines else "\n"), encoding="utf-8")


def append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True, ensure_ascii=True))
        handle.write("\n")


def ensure_surface_files() -> None:
    for path in (TRIAGE_LEDGER_PATH, TRAINING_LEDGER_PATH, TRIAGE_RUNTIME_PATH, TRAINING_RUNTIME_PATH):
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_text("\n", encoding="utf-8")


def _recursive_forbidden_scan(payload: Any, *, scope: str) -> list[str]:
    findings: list[str] = []
    if isinstance(payload, dict):
        for key, value in payload.items():
            key_text = str(key)
            if key_text.lower() in FORBIDDEN_KEYS:
                findings.append(f"{scope}.{key_text} uses a forbidden field")
            findings.extend(_recursive_forbidden_scan(value, scope=f"{scope}.{key_text}"))
    elif isinstance(payload, list):
        for index, item in enumerate(payload):
            findings.extend(_recursive_forbidden_scan(item, scope=f"{scope}[{index}]"))
    elif isinstance(payload, str):
        for needle in FORBIDDEN_SUBSTRINGS:
            if needle in payload:
                findings.append(f"{scope} contains forbidden substring {needle!r}")
    return findings


def scan_forbidden_content(payload: Any, *, scope: str) -> list[str]:
    return _recursive_forbidden_scan(payload, scope=scope)


def materialize_runtime_rows(
    triage_events: list[dict[str, Any]],
    training_events: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    triage_rows: list[dict[str, Any]] = []
    for event in triage_events:
        if event.get("event_type") != "decision_recorded":
            continue
        record = dict(event.get("decision_record", {}))
        if not record:
            continue
        record.setdefault("triage_event_id", event.get("event_id"))
        record.setdefault("recorded_at", event.get("recorded_at"))
        triage_rows.append(record)

    training_rows: list[dict[str, Any]] = []
    for event in training_events:
        if event.get("event_type") not in {"model_call_recorded", "model_call_failed"}:
            continue
        record = dict(event.get("training_record", {}))
        if not record:
            continue
        record.setdefault("call_event_id", event.get("event_id"))
        record.setdefault("recorded_at", event.get("recorded_at"))
        training_rows.append(record)

    triage_rows.sort(key=lambda item: (str(item.get("recorded_at", "")), str(item.get("triage_event_id", ""))))
    training_rows.sort(key=lambda item: (str(item.get("recorded_at", "")), str(item.get("call_event_id", ""))))
    return triage_rows, training_rows
