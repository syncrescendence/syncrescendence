#!/usr/bin/env python3
"""Append sanitized Acumen evidence events and rebuild runtime surfaces."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

try:
    from .evidence_family import (
        CONTRACT_PATH,
        TRAINING_FAMILY_ID,
        TRAINING_LEDGER_PATH,
        TRAINING_LEDGER_SCHEMA,
        TRAINING_RUNTIME_PATH,
        TRIAGE_FAMILY_ID,
        TRIAGE_LEDGER_PATH,
        TRIAGE_LEDGER_SCHEMA,
        TRIAGE_RUNTIME_PATH,
        append_jsonl,
        ensure_surface_files,
        load_jsonl,
        materialize_runtime_rows,
        repo_path_string,
        repo_rel,
        scan_forbidden_content,
        sha256_for_file,
        sha256_for_payload,
        utc_now,
        write_jsonl,
    )
except ImportError:
    from evidence_family import (
        CONTRACT_PATH,
        TRAINING_FAMILY_ID,
        TRAINING_LEDGER_PATH,
        TRAINING_LEDGER_SCHEMA,
        TRAINING_RUNTIME_PATH,
        TRIAGE_FAMILY_ID,
        TRIAGE_LEDGER_PATH,
        TRIAGE_LEDGER_SCHEMA,
        TRIAGE_RUNTIME_PATH,
        append_jsonl,
        ensure_surface_files,
        load_jsonl,
        materialize_runtime_rows,
        repo_path_string,
        repo_rel,
        scan_forbidden_content,
        sha256_for_file,
        sha256_for_payload,
        utc_now,
        write_jsonl,
    )

EVENT_COUNTER_RE = re.compile(r"^[a-z]{3}-\d{8}-(\d{4})$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    decision = subparsers.add_parser("decision")
    decision.add_argument("--input-json", required=True)
    decision.add_argument("--actor", required=True)
    decision.add_argument("--no-rematerialize", action="store_true")

    model_call = subparsers.add_parser("model-call")
    model_call.add_argument("--input-json", required=True)
    model_call.add_argument("--actor", required=True)
    model_call.add_argument("--no-rematerialize", action="store_true")
    return parser.parse_args()


def load_json_object(path: str) -> dict[str, Any]:
    payload = json.loads(Path(path).expanduser().read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit("input payload must be a JSON object")
    return payload


def next_event_id(prefix: str, ledger_path: Path) -> str:
    today = utc_now()[:10].replace("-", "")
    highest = 0
    for row in load_jsonl(ledger_path):
        event_id = str(row.get("event_id", ""))
        if not event_id.startswith(f"{prefix}-{today}-"):
            continue
        match = EVENT_COUNTER_RE.match(event_id)
        if match:
            highest = max(highest, int(match.group(1)))
    return f"{prefix}-{today}-{highest + 1:04d}"


def compute_packet_sha(payload: dict[str, Any]) -> tuple[str | None, str | None]:
    raw_path = payload.get("packet_path")
    packet_path = repo_path_string(str(raw_path)) if raw_path else None
    packet_sha = payload.get("packet_sha256")
    if packet_sha:
        return packet_path, str(packet_sha)
    if not raw_path:
        return packet_path, None
    file_path = Path(str(raw_path)).expanduser()
    if not file_path.is_absolute():
        file_path = (Path.cwd() / file_path).resolve()
    if not file_path.exists():
        raise SystemExit(f"packet_path does not exist: {file_path}")
    return packet_path, sha256_for_file(file_path)


def build_decision_event(payload: dict[str, Any], actor: str) -> dict[str, Any]:
    event_id = next_event_id("atd", TRIAGE_LEDGER_PATH)
    recorded_at = utc_now()
    decision_record = {
        "triage_event_id": event_id,
        "recorded_at": recorded_at,
        "channel_name": payload["channel_name"],
        "channel_id": payload["channel_id"],
        "title": payload["title"],
        "decision": payload["decision"],
        "priority_band": payload["priority_band"],
        "rationale": payload["rationale"],
    }
    for key in (
        "abstract",
        "suggested_consumption",
        "domain_tags",
        "video_id",
        "model_call_event_id",
        "target_depth",
        "target_polish",
    ):
        if key in payload:
            decision_record[key] = payload[key]

    packet_path, packet_sha = compute_packet_sha(payload)
    return {
        "schema_version": TRIAGE_LEDGER_SCHEMA,
        "event_id": event_id,
        "event_type": "decision_recorded",
        "family_id": TRIAGE_FAMILY_ID,
        "recorded_at": recorded_at,
        "actor": actor,
        "runtime_path": repo_rel(TRIAGE_RUNTIME_PATH),
        "contract_path": repo_rel(CONTRACT_PATH),
        "policy": {
            "prompt_capture": "metadata_only",
            "raw_prompt_capture": "forbidden",
            "raw_response_capture": "forbidden",
            "secret_capture": "forbidden",
        },
        "packet_provenance": {
            "packet_path": packet_path,
            "packet_sha256": packet_sha,
            "input_summary": payload.get("input_summary"),
        },
        "decision_sha256": sha256_for_payload(decision_record),
        "decision_record": decision_record,
    }


def build_model_call_event(payload: dict[str, Any], actor: str) -> dict[str, Any]:
    event_id = next_event_id("atc", TRAINING_LEDGER_PATH)
    recorded_at = utc_now()
    packet_path, packet_sha = compute_packet_sha(payload)
    prompt_sha = payload.get("prompt_sha256") or packet_sha
    outcome = payload["outcome"]
    status = str(outcome.get("status", "")).strip()
    event_type = "model_call_recorded" if status == "success" else "model_call_failed"
    training_record = {
        "call_event_id": event_id,
        "recorded_at": recorded_at,
        "provider": payload["provider"],
        "model": payload["model"],
        "operation": payload["operation"],
        "request_context": payload["request_context"],
        "packet_provenance": {
            "packet_path": packet_path,
            "packet_sha256": packet_sha,
        },
        "prompt_capture": {
            "policy": "metadata_only",
            "prompt_sha256": prompt_sha,
            "input_summary": payload.get("input_summary"),
        },
        "response_capture": payload["response_capture"],
        "usage": payload.get("usage", {}),
        "cost": payload.get("cost", {}),
        "outcome": outcome,
    }
    if "decision_event_id" in payload:
        training_record["decision_event_id"] = payload["decision_event_id"]

    return {
        "schema_version": TRAINING_LEDGER_SCHEMA,
        "event_id": event_id,
        "event_type": event_type,
        "family_id": TRAINING_FAMILY_ID,
        "recorded_at": recorded_at,
        "actor": actor,
        "runtime_path": repo_rel(TRAINING_RUNTIME_PATH),
        "contract_path": repo_rel(CONTRACT_PATH),
        "policy": {
            "prompt_capture": "metadata_only",
            "raw_prompt_capture": "forbidden",
            "raw_response_capture": "forbidden",
            "secret_capture": "forbidden",
        },
        "training_record_sha256": sha256_for_payload(training_record),
        "training_record": training_record,
    }


def rematerialize_runtime() -> None:
    triage_rows, training_rows = materialize_runtime_rows(load_jsonl(TRIAGE_LEDGER_PATH), load_jsonl(TRAINING_LEDGER_PATH))
    write_jsonl(TRIAGE_RUNTIME_PATH, triage_rows)
    write_jsonl(TRAINING_RUNTIME_PATH, training_rows)


def main() -> int:
    args = parse_args()
    ensure_surface_files()
    payload = load_json_object(args.input_json)
    findings = scan_forbidden_content(payload, scope="payload")
    if findings:
        raise SystemExit("\n".join(findings))

    if args.command == "decision":
        event = build_decision_event(payload, args.actor)
        append_jsonl(TRIAGE_LEDGER_PATH, event)
        ledger_path = TRIAGE_LEDGER_PATH
    else:
        event = build_model_call_event(payload, args.actor)
        append_jsonl(TRAINING_LEDGER_PATH, event)
        ledger_path = TRAINING_LEDGER_PATH

    if not args.no_rematerialize:
        rematerialize_runtime()
    print(repo_rel(ledger_path))
    print(event["event_id"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
