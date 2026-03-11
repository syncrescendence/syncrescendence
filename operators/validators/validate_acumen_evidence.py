#!/usr/bin/env python3
"""Report-first validator for the Acumen triage evidence family."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from operators.acumen.evidence_family import (
    CONTRACT_PATH,
    TRAINING_FAMILY_ID,
    TRAINING_LEDGER_PATH,
    TRAINING_LEDGER_SCHEMA,
    TRAINING_RUNTIME_PATH,
    TRIAGE_FAMILY_ID,
    TRIAGE_LEDGER_PATH,
    TRIAGE_LEDGER_SCHEMA,
    TRIAGE_RUNTIME_PATH,
    canonical_json_bytes,
    ensure_surface_files,
    load_jsonl,
    materialize_runtime_rows,
    repo_rel,
    scan_forbidden_content,
    sha256_for_payload,
)

STATE_DIR = REPO_ROOT / "orchestration" / "state"
DEFAULT_MD_REPORT = STATE_DIR / "ACUMEN-TRIAGE-EVIDENCE-REPORT.md"
DEFAULT_JSON_REPORT = STATE_DIR / "ACUMEN-TRIAGE-EVIDENCE-REPORT.json"

TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
TRIAGE_EVENT_ID_RE = re.compile(r"^atd-\d{8}-\d{4}$")
TRAINING_EVENT_ID_RE = re.compile(r"^atc-\d{8}-\d{4}$")
ALLOWED_DECISIONS = {"Skip", "Headline", "Compress", "Promote", "Flag-for-Primary"}
ALLOWED_PRIORITY_BANDS = {"Tier 1", "Tier 2", "Tier 3"}


@dataclass(frozen=True)
class Finding:
    level: str
    scope: str
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--triage-ledger", default=str(TRIAGE_LEDGER_PATH))
    parser.add_argument("--training-ledger", default=str(TRAINING_LEDGER_PATH))
    parser.add_argument("--triage-runtime", default=str(TRIAGE_RUNTIME_PATH))
    parser.add_argument("--training-runtime", default=str(TRAINING_RUNTIME_PATH))
    parser.add_argument("--output-md", default=str(DEFAULT_MD_REPORT))
    parser.add_argument("--output-json", default=str(DEFAULT_JSON_REPORT))
    return parser.parse_args()


def add_finding(findings: list[Finding], scope: str, message: str, *, level: str = "error") -> None:
    findings.append(Finding(level=level, scope=scope, message=message))


def add_forbidden_findings(findings: list[Finding], payload: Any, scope: str) -> None:
    for message in scan_forbidden_content(payload, scope=scope):
        add_finding(findings, scope, message)


def require_string(mapping: dict[str, Any], key: str, findings: list[Finding], scope: str) -> str | None:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        add_finding(findings, f"{scope}.{key}", "must be a non-empty string")
        return None
    return value.strip()


def require_mapping(mapping: dict[str, Any], key: str, findings: list[Finding], scope: str) -> dict[str, Any] | None:
    value = mapping.get(key)
    if not isinstance(value, dict):
        add_finding(findings, f"{scope}.{key}", "must be a JSON object")
        return None
    return value


def require_digest(value: str | None, findings: list[Finding], scope: str) -> None:
    if value is None or not SHA256_RE.fullmatch(value):
        add_finding(findings, scope, "must be a sha256 digest")


def validate_policy(policy: dict[str, Any], findings: list[Finding], scope: str) -> None:
    expected = {
        "prompt_capture": "metadata_only",
        "raw_prompt_capture": "forbidden",
        "raw_response_capture": "forbidden",
        "secret_capture": "forbidden",
    }
    for key, value in expected.items():
        if policy.get(key) != value:
            add_finding(findings, f"{scope}.{key}", f"must equal {value!r}")


def validate_packet_provenance(packet: dict[str, Any], findings: list[Finding], scope: str) -> None:
    packet_path = packet.get("packet_path")
    if packet_path is not None and (not isinstance(packet_path, str) or not packet_path.strip()):
        add_finding(findings, f"{scope}.packet_path", "must be a non-empty string when present")
    packet_sha = packet.get("packet_sha256")
    if packet_sha is not None:
        require_digest(str(packet_sha), findings, f"{scope}.packet_sha256")


def validate_decision_event(event: dict[str, Any], findings: list[Finding], line_number: int) -> None:
    scope = f"triage_ledger:{line_number}"
    schema_version = require_string(event, "schema_version", findings, scope)
    event_id = require_string(event, "event_id", findings, scope)
    event_type = require_string(event, "event_type", findings, scope)
    family_id = require_string(event, "family_id", findings, scope)
    recorded_at = require_string(event, "recorded_at", findings, scope)
    runtime_path = require_string(event, "runtime_path", findings, scope)
    contract_path = require_string(event, "contract_path", findings, scope)
    digest = require_string(event, "decision_sha256", findings, scope)
    policy = require_mapping(event, "policy", findings, scope)
    packet = require_mapping(event, "packet_provenance", findings, scope)
    record = require_mapping(event, "decision_record", findings, scope)
    require_string(event, "actor", findings, scope)

    if schema_version and schema_version != TRIAGE_LEDGER_SCHEMA:
        add_finding(findings, f"{scope}.schema_version", f"must equal {TRIAGE_LEDGER_SCHEMA!r}")
    if event_id and not TRIAGE_EVENT_ID_RE.fullmatch(event_id):
        add_finding(findings, f"{scope}.event_id", "must match atd-YYYYMMDD-NNNN")
    if event_type and event_type != "decision_recorded":
        add_finding(findings, f"{scope}.event_type", "must equal 'decision_recorded'")
    if family_id and family_id != TRIAGE_FAMILY_ID:
        add_finding(findings, f"{scope}.family_id", f"must equal {TRIAGE_FAMILY_ID!r}")
    if recorded_at and not TIMESTAMP_RE.fullmatch(recorded_at):
        add_finding(findings, f"{scope}.recorded_at", "must be ISO-8601 UTC")
    if runtime_path and runtime_path != repo_rel(TRIAGE_RUNTIME_PATH):
        add_finding(findings, f"{scope}.runtime_path", f"must equal {repo_rel(TRIAGE_RUNTIME_PATH)!r}")
    if contract_path and contract_path != repo_rel(CONTRACT_PATH):
        add_finding(findings, f"{scope}.contract_path", f"must equal {repo_rel(CONTRACT_PATH)!r}")
    if digest:
        require_digest(digest, findings, f"{scope}.decision_sha256")
    if policy is not None:
        validate_policy(policy, findings, f"{scope}.policy")
    if packet is not None:
        validate_packet_provenance(packet, findings, f"{scope}.packet_provenance")
    if record is not None:
        for key in ("triage_event_id", "recorded_at", "channel_name", "channel_id", "title", "decision", "priority_band", "rationale"):
            require_string(record, key, findings, f"{scope}.decision_record")
        if record.get("decision") not in ALLOWED_DECISIONS:
            add_finding(findings, f"{scope}.decision_record.decision", "must be a supported triage decision")
        if record.get("priority_band") not in ALLOWED_PRIORITY_BANDS:
            add_finding(findings, f"{scope}.decision_record.priority_band", "must be Tier 1, Tier 2, or Tier 3")
        add_forbidden_findings(findings, record, f"{scope}.decision_record")
        if digest and sha256_for_payload(record) != digest:
            add_finding(findings, f"{scope}.decision_sha256", "does not match decision_record bytes")


def validate_training_event(event: dict[str, Any], findings: list[Finding], line_number: int) -> None:
    scope = f"training_ledger:{line_number}"
    schema_version = require_string(event, "schema_version", findings, scope)
    event_id = require_string(event, "event_id", findings, scope)
    event_type = require_string(event, "event_type", findings, scope)
    family_id = require_string(event, "family_id", findings, scope)
    recorded_at = require_string(event, "recorded_at", findings, scope)
    runtime_path = require_string(event, "runtime_path", findings, scope)
    contract_path = require_string(event, "contract_path", findings, scope)
    digest = require_string(event, "training_record_sha256", findings, scope)
    policy = require_mapping(event, "policy", findings, scope)
    record = require_mapping(event, "training_record", findings, scope)
    require_string(event, "actor", findings, scope)

    if schema_version and schema_version != TRAINING_LEDGER_SCHEMA:
        add_finding(findings, f"{scope}.schema_version", f"must equal {TRAINING_LEDGER_SCHEMA!r}")
    if event_id and not TRAINING_EVENT_ID_RE.fullmatch(event_id):
        add_finding(findings, f"{scope}.event_id", "must match atc-YYYYMMDD-NNNN")
    if event_type and event_type not in {"model_call_recorded", "model_call_failed"}:
        add_finding(findings, f"{scope}.event_type", "must be a supported model call event type")
    if family_id and family_id != TRAINING_FAMILY_ID:
        add_finding(findings, f"{scope}.family_id", f"must equal {TRAINING_FAMILY_ID!r}")
    if recorded_at and not TIMESTAMP_RE.fullmatch(recorded_at):
        add_finding(findings, f"{scope}.recorded_at", "must be ISO-8601 UTC")
    if runtime_path and runtime_path != repo_rel(TRAINING_RUNTIME_PATH):
        add_finding(findings, f"{scope}.runtime_path", f"must equal {repo_rel(TRAINING_RUNTIME_PATH)!r}")
    if contract_path and contract_path != repo_rel(CONTRACT_PATH):
        add_finding(findings, f"{scope}.contract_path", f"must equal {repo_rel(CONTRACT_PATH)!r}")
    if digest:
        require_digest(digest, findings, f"{scope}.training_record_sha256")
    if policy is not None:
        validate_policy(policy, findings, f"{scope}.policy")
    if record is not None:
        for key in ("call_event_id", "recorded_at", "provider", "model", "operation"):
            require_string(record, key, findings, f"{scope}.training_record")
        require_mapping(record, "request_context", findings, f"{scope}.training_record")
        packet = require_mapping(record, "packet_provenance", findings, f"{scope}.training_record")
        prompt_capture = require_mapping(record, "prompt_capture", findings, f"{scope}.training_record")
        response_capture = require_mapping(record, "response_capture", findings, f"{scope}.training_record")
        outcome = require_mapping(record, "outcome", findings, f"{scope}.training_record")
        if packet is not None:
            validate_packet_provenance(packet, findings, f"{scope}.training_record.packet_provenance")
        if prompt_capture is not None:
            if prompt_capture.get("policy") != "metadata_only":
                add_finding(findings, f"{scope}.training_record.prompt_capture.policy", "must equal 'metadata_only'")
            prompt_sha = prompt_capture.get("prompt_sha256")
            if prompt_sha is not None:
                require_digest(str(prompt_sha), findings, f"{scope}.training_record.prompt_capture.prompt_sha256")
        if response_capture is not None and "schema_valid" in response_capture and not isinstance(response_capture.get("schema_valid"), bool):
            add_finding(findings, f"{scope}.training_record.response_capture.schema_valid", "must be a boolean")
        if outcome is not None:
            status = require_string(outcome, "status", findings, f"{scope}.training_record.outcome")
            if status is not None and status not in {"success", "failure"}:
                add_finding(findings, f"{scope}.training_record.outcome.status", "must be 'success' or 'failure'")
        for bucket in ("usage", "cost"):
            value = record.get(bucket, {})
            if not isinstance(value, dict):
                add_finding(findings, f"{scope}.training_record.{bucket}", "must be an object")
            elif any(not isinstance(item, (int, float, str, bool, type(None))) for item in value.values()):
                add_finding(findings, f"{scope}.training_record.{bucket}", "must contain scalar values only")
        add_forbidden_findings(findings, record, f"{scope}.training_record")
        if digest and sha256_for_payload(record) != digest:
            add_finding(findings, f"{scope}.training_record_sha256", "does not match training_record bytes")


def load_runtime_rows(path: Path, findings: list[Finding], scope: str) -> list[dict[str, Any]]:
    if not path.exists():
        add_finding(findings, scope, f"missing file: {repo_rel(path)}")
        return []
    try:
        return load_jsonl(path)
    except ValueError as exc:
        add_finding(findings, scope, str(exc))
        return []


def write_report(report_json: Path, report_md: Path, report: dict[str, Any]) -> None:
    report_json.parent.mkdir(parents=True, exist_ok=True)
    report_json.write_bytes(canonical_json_bytes(report) + b"\n")
    lines = [
        "# Acumen Triage Evidence Report",
        "",
        f"- status: {report['status']}",
        f"- triage ledger events: {report['summary']['triage_event_count']}",
        f"- training ledger events: {report['summary']['training_event_count']}",
        f"- triage runtime rows: {report['summary']['triage_runtime_row_count']}",
        f"- training runtime rows: {report['summary']['training_runtime_row_count']}",
        f"- findings: {report['summary']['finding_count']}",
        "",
        "## Findings",
        "",
    ]
    if not report["findings"]:
        lines.append("- none")
    else:
        for finding in report["findings"]:
            lines.append(f"- [{finding['level']}] {finding['scope']}: {finding['message']}")
    report_md.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    ensure_surface_files()

    findings: list[Finding] = []
    if not CONTRACT_PATH.exists():
        add_finding(findings, "contract", f"missing contract: {repo_rel(CONTRACT_PATH)}")

    triage_events = load_runtime_rows(Path(args.triage_ledger).expanduser().resolve(), findings, "triage_ledger")
    training_events = load_runtime_rows(Path(args.training_ledger).expanduser().resolve(), findings, "training_ledger")
    triage_runtime = load_runtime_rows(Path(args.triage_runtime).expanduser().resolve(), findings, "triage_runtime")
    training_runtime = load_runtime_rows(Path(args.training_runtime).expanduser().resolve(), findings, "training_runtime")

    for index, event in enumerate(triage_events, start=1):
        validate_decision_event(event, findings, index)
    for index, event in enumerate(training_events, start=1):
        validate_training_event(event, findings, index)

    expected_triage, expected_training = materialize_runtime_rows(triage_events, training_events)
    if triage_runtime != expected_triage:
        add_finding(findings, "triage_runtime", "runtime triage surface is not the deterministic materialization of the triage ledger")
    if training_runtime != expected_training:
        add_finding(
            findings,
            "training_runtime",
            "runtime training corpus surface is not the deterministic materialization of the training ledger",
        )

    report = {
        "status": "PASS" if not findings else "FAIL",
        "summary": {
            "triage_event_count": len(triage_events),
            "training_event_count": len(training_events),
            "triage_runtime_row_count": len(triage_runtime),
            "training_runtime_row_count": len(training_runtime),
            "finding_count": len(findings),
            "contract_path": repo_rel(CONTRACT_PATH),
        },
        "findings": [asdict(item) for item in findings],
    }
    write_report(Path(args.output_json).expanduser().resolve(), Path(args.output_md).expanduser().resolve(), report)
    print(Path(args.output_json).expanduser().resolve())
    print(Path(args.output_md).expanduser().resolve())
    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
