#!/usr/bin/env python3
"""Validate the Acumen live-batch proof receipt family and current status surface."""

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

from operators.acumen.live_batch_proof_family import (
    CONTRACT_PATH,
    EVENT_ID_RE,
    EVENT_TYPE,
    FAMILY_ID,
    LEDGER_PATH,
    LEDGER_SCHEMA,
    REPORT_JSON_PATH,
    REPORT_MD_PATH,
    STATUS_PATH,
    ALLOWED_OUTCOMES,
    build_status_payload,
    load_events,
    repo_rel,
    scan_forbidden_content,
    sha256_for_payload,
    utc_now,
)


TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


@dataclass(frozen=True)
class Finding:
    level: str
    scope: str
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", default=str(LEDGER_PATH))
    parser.add_argument("--status-json", default=str(STATUS_PATH))
    parser.add_argument("--output-json", default=str(REPORT_JSON_PATH))
    parser.add_argument("--output-md", default=str(REPORT_MD_PATH))
    return parser.parse_args()


def add_finding(findings: list[Finding], scope: str, message: str, *, level: str = "error") -> None:
    findings.append(Finding(level=level, scope=scope, message=message))


def load_json_object(path: Path, findings: list[Finding], scope: str) -> dict[str, Any] | None:
    if not path.exists():
        add_finding(findings, scope, f"missing file: {path}")
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        add_finding(findings, scope, f"invalid JSON: {exc}")
        return None
    if not isinstance(payload, dict):
        add_finding(findings, scope, "must be a JSON object")
        return None
    return payload


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


def require_bool(mapping: dict[str, Any], key: str, findings: list[Finding], scope: str) -> bool | None:
    value = mapping.get(key)
    if not isinstance(value, bool):
        add_finding(findings, f"{scope}.{key}", "must be a boolean")
        return None
    return value


def add_forbidden_findings(findings: list[Finding], payload: Any, scope: str) -> None:
    for message in scan_forbidden_content(payload, scope=scope):
        add_finding(findings, scope, message)


def validate_command_summary(payload: dict[str, Any] | None, findings: list[Finding], scope: str) -> None:
    if payload is None:
        return
    if not isinstance(payload, dict):
        add_finding(findings, scope, "must be a JSON object when present")
        return
    if "ok" in payload and not isinstance(payload.get("ok"), bool):
        add_finding(findings, f"{scope}.ok", "must be a boolean")
    if "returncode" in payload and payload.get("returncode") is not None and not isinstance(payload.get("returncode"), int):
        add_finding(findings, f"{scope}.returncode", "must be an integer or null")
    if "command" in payload:
        command = payload.get("command")
        if not isinstance(command, list) or not all(isinstance(item, str) for item in command):
            add_finding(findings, f"{scope}.command", "must be a list of strings")
    for key in ("stdout", "stderr"):
        if key in payload and not isinstance(payload.get(key), str):
            add_finding(findings, f"{scope}.{key}", "must be a string")


def validate_receipt_record(record: dict[str, Any], findings: list[Finding], scope: str) -> None:
    outcome = require_string(record, "outcome", findings, scope)
    proof_status = require_string(record, "proof_status", findings, scope)
    if outcome and outcome not in ALLOWED_OUTCOMES:
        add_finding(findings, f"{scope}.outcome", f"must be one of {sorted(ALLOWED_OUTCOMES)}")
    if outcome and proof_status:
        if outcome == "blocked" and not proof_status.startswith("blocked_"):
            add_finding(findings, f"{scope}.proof_status", "blocked outcomes must use a blocked_* proof_status")
        if outcome == "failed" and not proof_status.startswith("failed_"):
            add_finding(findings, f"{scope}.proof_status", "failed outcomes must use a failed_* proof_status")
        if outcome == "completed_not_proven" and not proof_status.startswith("completed_"):
            add_finding(findings, f"{scope}.proof_status", "completed_not_proven outcomes must use a completed_* proof_status")
        if outcome == "proven" and proof_status != "live_batch_proven":
            add_finding(findings, f"{scope}.proof_status", "proven outcomes must use proof_status=live_batch_proven")

    for key in ("failure_domain", "failure_code", "failure_message"):
        if key in record and record.get(key) is not None and not isinstance(record.get(key), str):
            add_finding(findings, f"{scope}.{key}", "must be a string or null")

    credential_state = require_mapping(record, "credential_state", findings, scope)
    if credential_state is not None:
        require_string(credential_state, "youtube_api_env", findings, f"{scope}.credential_state")
        require_bool(credential_state, "youtube_api_present", findings, f"{scope}.credential_state")
        require_string(credential_state, "gemini_api_env", findings, f"{scope}.credential_state")
        require_bool(credential_state, "gemini_api_present", findings, f"{scope}.credential_state")
        raw_secret_capture = require_string(credential_state, "raw_secret_capture", findings, f"{scope}.credential_state")
        if raw_secret_capture and raw_secret_capture != "forbidden":
            add_finding(findings, f"{scope}.credential_state.raw_secret_capture", "must equal 'forbidden'")

    repo_sovereignty = require_mapping(record, "repo_sovereignty", findings, scope)
    if repo_sovereignty is not None:
        intake_authority = require_string(repo_sovereignty, "intake_authority", findings, f"{scope}.repo_sovereignty")
        strict_identity_required = require_bool(repo_sovereignty, "strict_identity_required", findings, f"{scope}.repo_sovereignty")
        live_credentials_external = require_bool(
            repo_sovereignty,
            "live_credentials_must_remain_external",
            findings,
            f"{scope}.repo_sovereignty",
        )
        raw_secret_capture = require_string(repo_sovereignty, "raw_secret_capture", findings, f"{scope}.repo_sovereignty")
        if intake_authority and intake_authority != "acumen":
            add_finding(findings, f"{scope}.repo_sovereignty.intake_authority", "must equal 'acumen'")
        if strict_identity_required is not None and not strict_identity_required:
            add_finding(findings, f"{scope}.repo_sovereignty.strict_identity_required", "must be true")
        if live_credentials_external is not None and not live_credentials_external:
            add_finding(findings, f"{scope}.repo_sovereignty.live_credentials_must_remain_external", "must be true")
        if raw_secret_capture and raw_secret_capture != "forbidden":
            add_finding(findings, f"{scope}.repo_sovereignty.raw_secret_capture", "must equal 'forbidden'")

    validate_command_summary(record.get("registry_validation"), findings, f"{scope}.registry_validation")
    validate_command_summary(record.get("pipeline_command"), findings, f"{scope}.pipeline_command")

    pipeline_provenance = require_mapping(record, "pipeline_provenance", findings, scope)
    if pipeline_provenance is not None:
        for key in ("status_path", "status_sha256", "identity_status_path", "poll_status_path", "triage_status_path"):
            value = pipeline_provenance.get(key)
            if value is not None and not isinstance(value, str):
                add_finding(findings, f"{scope}.pipeline_provenance.{key}", "must be a string or null")
        status_sha256 = pipeline_provenance.get("status_sha256")
        if status_sha256 is not None and (not isinstance(status_sha256, str) or not SHA256_RE.fullmatch(status_sha256)):
            add_finding(findings, f"{scope}.pipeline_provenance.status_sha256", "must be a sha256 digest when present")
        snapshot = pipeline_provenance.get("snapshot")
        if snapshot is not None and not isinstance(snapshot, dict):
            add_finding(findings, f"{scope}.pipeline_provenance.snapshot", "must be a JSON object or null")

    proof_gate = require_mapping(record, "proof_gate", findings, scope)
    if proof_gate is not None:
        meets_live_batch_proof = require_bool(proof_gate, "meets_live_batch_proof", findings, f"{scope}.proof_gate")
        require_bool(proof_gate, "meets_live_poll_requirement", findings, f"{scope}.proof_gate")
        require_bool(proof_gate, "meets_live_triage_requirement", findings, f"{scope}.proof_gate")
        reason_code = require_string(proof_gate, "reason_code", findings, f"{scope}.proof_gate")
        require_string(proof_gate, "reason_message", findings, f"{scope}.proof_gate")
        gemini_calls_used = proof_gate.get("gemini_calls_used")
        if gemini_calls_used is not None and not isinstance(gemini_calls_used, int):
            add_finding(findings, f"{scope}.proof_gate.gemini_calls_used", "must be an integer when present")
        if outcome == "proven" and meets_live_batch_proof is not True:
            add_finding(findings, f"{scope}.proof_gate.meets_live_batch_proof", "proven outcomes must satisfy the live-batch proof gate")
        if outcome == "completed_not_proven" and meets_live_batch_proof is not False:
            add_finding(findings, f"{scope}.proof_gate.meets_live_batch_proof", "completed_not_proven outcomes must not satisfy the live-batch proof gate")
        if outcome == "completed_not_proven" and reason_code is not None and reason_code == "live_batch_proven":
            add_finding(findings, f"{scope}.proof_gate.reason_code", "completed_not_proven outcomes cannot use reason_code=live_batch_proven")

    add_forbidden_findings(findings, record, scope)


def normalize_status_payload(payload: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in payload.items() if key != "generated_at"}


def render_markdown_report(report: dict[str, Any]) -> str:
    lines = [
        "# Acumen Live Batch Proof Report",
        "",
        f"- Ledger: `{report['ledger_path']}`",
        f"- Status JSON: `{report['status_json']}`",
        f"- Checked at: `{report['checked_at']}`",
        f"- OK: `{str(report['ok']).lower()}`",
        f"- Receipt events: `{report['summary']['receipt_events']}`",
        f"- Live proof present: `{str(report['summary']['live_proof_present']).lower()}`",
        f"- Latest receipt: `{report['summary']['latest_receipt_event_id'] or 'none'}`",
        f"- Latest outcome: `{report['summary']['latest_outcome'] or 'none'}`",
        f"- Findings: `{len(report['findings'])}`",
        "",
        "## Findings",
        "",
    ]
    if report["findings"]:
        for finding in report["findings"]:
            lines.append(f"- [{finding['level']}] `{finding['scope']}` {finding['message']}")
    else:
        lines.append("- no findings")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    ledger_path = Path(args.ledger).expanduser().resolve()
    status_path = Path(args.status_json).expanduser().resolve()
    output_json = Path(args.output_json).expanduser().resolve()
    output_md = Path(args.output_md).expanduser().resolve()

    findings: list[Finding] = []
    events = load_events(ledger_path)
    if not events:
        add_finding(findings, "ledger", "ledger must contain at least one receipt event")

    for index, event in enumerate(events):
        scope = f"ledger[{index}]"
        if not isinstance(event, dict):
            add_finding(findings, scope, "must be a JSON object")
            continue
        schema_version = require_string(event, "schema_version", findings, scope)
        event_id = require_string(event, "event_id", findings, scope)
        event_type = require_string(event, "event_type", findings, scope)
        family_id = require_string(event, "family_id", findings, scope)
        recorded_at = require_string(event, "recorded_at", findings, scope)
        actor = require_string(event, "actor", findings, scope)
        contract_path = require_string(event, "contract_path", findings, scope)
        proof_status_path = require_string(event, "proof_status_path", findings, scope)
        receipt_record_sha256 = require_string(event, "receipt_record_sha256", findings, scope)
        receipt_record = require_mapping(event, "receipt_record", findings, scope)

        if schema_version and schema_version != LEDGER_SCHEMA:
            add_finding(findings, f"{scope}.schema_version", f"must equal {LEDGER_SCHEMA!r}")
        if event_id and not EVENT_ID_RE.fullmatch(event_id):
            add_finding(findings, f"{scope}.event_id", "must match alp-YYYYMMDD-NNNN")
        if event_type and event_type != EVENT_TYPE:
            add_finding(findings, f"{scope}.event_type", f"must equal {EVENT_TYPE!r}")
        if family_id and family_id != FAMILY_ID:
            add_finding(findings, f"{scope}.family_id", f"must equal {FAMILY_ID!r}")
        if recorded_at and not TIMESTAMP_RE.fullmatch(recorded_at):
            add_finding(findings, f"{scope}.recorded_at", "must be ISO-8601 UTC")
        if actor is None:
            pass
        if contract_path and contract_path != repo_rel(CONTRACT_PATH):
            add_finding(findings, f"{scope}.contract_path", f"must equal {repo_rel(CONTRACT_PATH)!r}")
        if proof_status_path and proof_status_path != repo_rel(status_path):
            add_finding(findings, f"{scope}.proof_status_path", f"must equal {repo_rel(status_path)!r}")
        if receipt_record_sha256 and not SHA256_RE.fullmatch(receipt_record_sha256):
            add_finding(findings, f"{scope}.receipt_record_sha256", "must be a sha256 digest")
        if receipt_record is not None:
            validate_receipt_record(receipt_record, findings, f"{scope}.receipt_record")
            if receipt_record_sha256 and sha256_for_payload(receipt_record) != receipt_record_sha256:
                add_finding(findings, f"{scope}.receipt_record_sha256", "does not match receipt_record bytes")
        add_forbidden_findings(findings, event, scope)

    expected_status = build_status_payload(events, ledger_path)
    status_payload = load_json_object(status_path, findings, "status")
    if status_payload is not None:
        actual = normalize_status_payload(status_payload)
        expected = normalize_status_payload(expected_status)
        if actual != expected:
            add_finding(findings, "status", "current status JSON does not match the summary rebuilt from the ledger")

    report = {
        "ledger_path": repo_rel(ledger_path) if ledger_path.exists() else str(ledger_path),
        "status_json": repo_rel(status_path) if status_path.exists() else str(status_path),
        "checked_at": utc_now(),
        "ok": not any(finding.level == "error" for finding in findings),
        "summary": {
            "receipt_events": expected_status.get("receipt_events"),
            "live_proof_present": expected_status.get("live_proof_present"),
            "latest_receipt_event_id": expected_status.get("latest_receipt_event_id"),
            "latest_outcome": expected_status.get("latest_outcome"),
            "latest_proof_status": expected_status.get("latest_proof_status"),
            "last_proven_receipt_event_id": expected_status.get("last_proven_receipt_event_id"),
        },
        "findings": [asdict(finding) for finding in findings],
    }
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_md.write_text(render_markdown_report(report), encoding="utf-8")
    print(output_json)
    print(output_md)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
