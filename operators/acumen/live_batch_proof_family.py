#!/usr/bin/env python3
"""Shared helpers for the Acumen live-batch proof receipt family."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

try:
    from .evidence_family import (
        append_jsonl,
        load_jsonl,
        repo_path_string,
        repo_rel,
        scan_forbidden_content,
        sha256_for_file,
        sha256_for_payload,
        utc_now,
    )
except ImportError:
    from evidence_family import (  # type: ignore
        append_jsonl,
        load_jsonl,
        repo_path_string,
        repo_rel,
        scan_forbidden_content,
        sha256_for_file,
        sha256_for_payload,
        utc_now,
    )


REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = REPO_ROOT / "orchestration" / "state" / "impl" / "ACUMEN-LIVE-BATCH-PROOF-RECEIPT-CONTRACT-v1.md"
LEDGER_PATH = REPO_ROOT / "orchestration" / "state" / "registry" / "acumen-live-batch-proof-ledger.jsonl"
STATUS_PATH = REPO_ROOT / "orchestration" / "state" / "ACUMEN-LIVE-BATCH-PROOF-STATUS.json"
REPORT_JSON_PATH = REPO_ROOT / "orchestration" / "state" / "ACUMEN-LIVE-BATCH-PROOF-REPORT.json"
REPORT_MD_PATH = REPO_ROOT / "orchestration" / "state" / "ACUMEN-LIVE-BATCH-PROOF-REPORT.md"

FAMILY_ID = "acumen_live_batch_proof"
LEDGER_SCHEMA = "acumen-live-batch-proof-ledger-event/v1"
EVENT_TYPE = "live_batch_attempt_receipted"
EVENT_ID_PREFIX = "alp"
EVENT_ID_RE = re.compile(r"^alp-\d{8}-(\d{4})$")
ALLOWED_OUTCOMES = {"blocked", "completed_not_proven", "failed", "proven"}


def ensure_surface_files() -> None:
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not LEDGER_PATH.exists():
        LEDGER_PATH.write_text("\n", encoding="utf-8")


def load_events(path: Path = LEDGER_PATH) -> list[dict[str, Any]]:
    ensure_surface_files()
    return load_jsonl(path)


def next_event_id(path: Path = LEDGER_PATH) -> str:
    today = utc_now()[:10].replace("-", "")
    highest = 0
    for row in load_events(path):
        event_id = str(row.get("event_id", ""))
        if not event_id.startswith(f"{EVENT_ID_PREFIX}-{today}-"):
            continue
        match = EVENT_ID_RE.fullmatch(event_id)
        if match:
            highest = max(highest, int(match.group(1)))
    return f"{EVENT_ID_PREFIX}-{today}-{highest + 1:04d}"


def maybe_repo_rel(path: Path | None) -> str | None:
    if path is None:
        return None
    try:
        return repo_rel(path.resolve())
    except ValueError:
        return str(path.resolve())


def maybe_repo_path_string(raw_value: str | None) -> str | None:
    return repo_path_string(raw_value) if raw_value is not None else None


def summarize_command_result(payload: dict[str, Any] | None) -> dict[str, Any] | None:
    if not isinstance(payload, dict):
        return None
    command = payload.get("command")
    summary = {
        "ok": bool(payload.get("ok")),
        "returncode": payload.get("returncode"),
        "stdout": str(payload.get("stdout") or "")[:500],
        "stderr": str(payload.get("stderr") or "")[:500],
    }
    if isinstance(command, list):
        summary["command"] = [str(item) for item in command]
    return summary


def summarize_pipeline_status(payload: dict[str, Any] | None) -> dict[str, Any] | None:
    if not isinstance(payload, dict):
        return None

    poll_snapshot = payload.get("poll_status_snapshot")
    if not isinstance(poll_snapshot, dict):
        poll_snapshot = {}

    triage_snapshot = payload.get("triage_status_snapshot")
    if not isinstance(triage_snapshot, dict):
        triage_snapshot = {}

    external_dependencies = payload.get("external_dependencies")
    if not isinstance(external_dependencies, dict):
        external_dependencies = {}

    youtube_dependency = external_dependencies.get("youtube_feed")
    if not isinstance(youtube_dependency, dict):
        youtube_dependency = {}

    gemini_dependency = external_dependencies.get("gemini_api")
    if not isinstance(gemini_dependency, dict):
        gemini_dependency = {}

    triage_external_dependencies = triage_snapshot.get("external_dependencies")
    if not isinstance(triage_external_dependencies, dict):
        triage_external_dependencies = {}

    triage_gemini_dependency = triage_external_dependencies.get("gemini_api")
    if not isinstance(triage_gemini_dependency, dict):
        triage_gemini_dependency = {}

    return {
        "captured_at": payload.get("captured_at"),
        "execution_profile": payload.get("execution_profile"),
        "ok": bool(payload.get("ok")),
        "failure_domain": payload.get("failure_domain"),
        "failure_code": payload.get("failure_code"),
        "failure_message": payload.get("failure_message"),
        "poll_success": bool(payload.get("poll_success")),
        "triage_success": bool(payload.get("triage_success")),
        "evidence_validation_success": bool(payload.get("evidence_validation_success")),
        "dawn_brief_success": bool(payload.get("dawn_brief_success")),
        "poll_mode": poll_snapshot.get("mode") or youtube_dependency.get("mode"),
        "triage_mode": triage_snapshot.get("mode") or gemini_dependency.get("mode"),
        "poll_new_uploads": poll_snapshot.get("new_uploads"),
        "poll_failures": poll_snapshot.get("failures"),
        "triage_processed": triage_snapshot.get("processed"),
        "triage_queued": triage_snapshot.get("queued"),
        "triage_failures": triage_snapshot.get("failures"),
        "gemini_calls_used": triage_gemini_dependency.get("calls_used"),
        "gemini_model": triage_gemini_dependency.get("model"),
        "queue_jsonl": maybe_repo_path_string(str(payload.get("queue_jsonl"))) if payload.get("queue_jsonl") else None,
        "training_jsonl": maybe_repo_path_string(str(payload.get("training_jsonl"))) if payload.get("training_jsonl") else None,
        "dawn_brief_path": maybe_repo_path_string(str(payload.get("dawn_brief_path"))) if payload.get("dawn_brief_path") else None,
        "poll_status_json": maybe_repo_path_string(str(payload.get("poll_status_json")))
        if payload.get("poll_status_json")
        else None,
        "triage_status_json": maybe_repo_path_string(str(payload.get("triage_status_json")))
        if payload.get("triage_status_json")
        else None,
        "identity_status_json": maybe_repo_path_string(str(payload.get("identity_status_json")))
        if payload.get("identity_status_json")
        else None,
        "identity_probe": summarize_command_result(payload.get("identity_probe")),
        "poll_status": summarize_command_result(payload.get("poll_status")),
        "triage_status": summarize_command_result(payload.get("triage_status")),
        "evidence_validation_status": summarize_command_result(payload.get("evidence_validation_status")),
        "dawn_brief_status": summarize_command_result(payload.get("dawn_brief_status")),
    }


def _to_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, str) and value.strip().isdigit():
        return int(value.strip())
    return None


def build_proof_gate(pipeline_summary: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(pipeline_summary, dict):
        return {
            "meets_live_poll_requirement": False,
            "meets_live_triage_requirement": False,
            "meets_live_batch_proof": False,
            "reason_code": "missing_pipeline_status",
            "reason_message": "pipeline status was not captured",
        }

    gemini_calls_used = _to_int(pipeline_summary.get("gemini_calls_used")) or 0
    poll_mode = str(pipeline_summary.get("poll_mode") or "")
    triage_mode = str(pipeline_summary.get("triage_mode") or "")
    pipeline_ok = bool(pipeline_summary.get("ok"))

    meets_live_poll_requirement = poll_mode == "live" and bool(pipeline_summary.get("poll_success"))
    meets_live_triage_requirement = triage_mode == "gemini" and bool(pipeline_summary.get("triage_success")) and gemini_calls_used >= 1
    meets_live_batch_proof = pipeline_ok and meets_live_poll_requirement and meets_live_triage_requirement

    if meets_live_batch_proof:
        reason_code = "live_batch_proven"
        reason_message = "live poll and live Gemini triage both succeeded"
    elif not pipeline_ok:
        reason_code = str(pipeline_summary.get("failure_code") or "pipeline_not_ok")
        reason_message = str(pipeline_summary.get("failure_message") or "pipeline did not complete successfully")
    elif not meets_live_poll_requirement:
        reason_code = "live_poll_requirement_unmet"
        reason_message = "pipeline completed without a successful live poll"
    elif gemini_calls_used == 0:
        reason_code = "no_live_gemini_calls"
        reason_message = "pipeline completed but did not execute any live Gemini triage calls"
    else:
        reason_code = "live_triage_requirement_unmet"
        reason_message = "pipeline completed without satisfying the live Gemini triage proof gate"

    return {
        "meets_live_poll_requirement": meets_live_poll_requirement,
        "meets_live_triage_requirement": meets_live_triage_requirement,
        "meets_live_batch_proof": meets_live_batch_proof,
        "poll_mode": poll_mode or None,
        "triage_mode": triage_mode or None,
        "gemini_calls_used": gemini_calls_used,
        "reason_code": reason_code,
        "reason_message": reason_message,
    }


def classify_receipt(
    *,
    youtube_api_present: bool,
    gemini_api_present: bool,
    registry_validation: dict[str, Any] | None,
    pipeline_status: dict[str, Any] | None,
) -> dict[str, Any]:
    if not youtube_api_present or not gemini_api_present:
        missing = []
        if not youtube_api_present:
            missing.append("ACUMEN_YOUTUBE_API_KEY")
        if not gemini_api_present:
            missing.append("GEMINI_API_KEY")
        message = "missing required environment credentials: " + ", ".join(missing)
        return {
            "outcome": "blocked",
            "proof_status": "blocked_missing_credentials",
            "failure_domain": "credential",
            "failure_code": "missing_credentials",
            "failure_message": message,
            "proof_gate": build_proof_gate(None),
            "pipeline_summary": None,
        }

    registry_summary = summarize_command_result(registry_validation)
    if not registry_summary or not registry_summary.get("ok"):
        message = str((registry_summary or {}).get("stderr") or (registry_summary or {}).get("stdout") or "registry validation failed")
        return {
            "outcome": "failed",
            "proof_status": "failed_registry_validation",
            "failure_domain": "repo_contract",
            "failure_code": "registry_validation_failed",
            "failure_message": message,
            "proof_gate": build_proof_gate(None),
            "pipeline_summary": None,
        }

    pipeline_summary = summarize_pipeline_status(pipeline_status)
    proof_gate = build_proof_gate(pipeline_summary)
    if not isinstance(pipeline_status, dict):
        return {
            "outcome": "failed",
            "proof_status": "failed_pipeline_contract",
            "failure_domain": "repo_contract",
            "failure_code": "missing_pipeline_status",
            "failure_message": "pipeline status file was not produced",
            "proof_gate": proof_gate,
            "pipeline_summary": pipeline_summary,
        }

    if bool(pipeline_status.get("ok")) and bool(proof_gate.get("meets_live_batch_proof")):
        return {
            "outcome": "proven",
            "proof_status": "live_batch_proven",
            "failure_domain": None,
            "failure_code": None,
            "failure_message": None,
            "proof_gate": proof_gate,
            "pipeline_summary": pipeline_summary,
        }

    failure_domain = str(pipeline_status.get("failure_domain") or "")
    failure_code = str(pipeline_status.get("failure_code") or "")
    failure_message = str(pipeline_status.get("failure_message") or "")

    if failure_domain == "identity":
        return {
            "outcome": "blocked",
            "proof_status": "blocked_identity",
            "failure_domain": "identity",
            "failure_code": failure_code or "identity_mismatch",
            "failure_message": failure_message or "strict identity gate failed",
            "proof_gate": proof_gate,
            "pipeline_summary": pipeline_summary,
        }

    if bool(pipeline_status.get("ok")):
        if str(proof_gate.get("reason_code")) == "no_live_gemini_calls":
            proof_status = "completed_no_live_gemini_calls"
        else:
            proof_status = "completed_without_live_batch_proof"
        return {
            "outcome": "completed_not_proven",
            "proof_status": proof_status,
            "failure_domain": "proof_gap",
            "failure_code": str(proof_gate.get("reason_code") or "proof_gap"),
            "failure_message": str(proof_gate.get("reason_message") or "live-batch proof gate not satisfied"),
            "proof_gate": proof_gate,
            "pipeline_summary": pipeline_summary,
        }

    if failure_domain == "evidence_contract":
        proof_status = "failed_evidence_contract"
    elif failure_domain == "external_service":
        proof_status = "failed_external_service"
    else:
        proof_status = "failed_live_batch_attempt"

    return {
        "outcome": "failed",
        "proof_status": proof_status,
        "failure_domain": failure_domain or "external_service",
        "failure_code": failure_code or "live_batch_failed",
        "failure_message": failure_message or "live batch attempt failed",
        "proof_gate": proof_gate,
        "pipeline_summary": pipeline_summary,
    }


def build_status_payload(events: list[dict[str, Any]], ledger_path: Path = LEDGER_PATH) -> dict[str, Any]:
    counts_by_outcome: dict[str, int] = {}
    counts_by_proof_status: dict[str, int] = {}
    counts_by_failure_domain: dict[str, int] = {}

    latest_event: dict[str, Any] | None = events[-1] if events else None
    def record_for(event: dict[str, Any]) -> dict[str, Any]:
        record = event.get("receipt_record", {})
        return record if isinstance(record, dict) else {}

    last_proven_event: dict[str, Any] | None = next(
        (event for event in reversed(events) if record_for(event).get("outcome") == "proven"),
        None,
    )

    for event in events:
        record = record_for(event)
        outcome = str(record.get("outcome") or "")
        proof_status = str(record.get("proof_status") or "")
        failure_domain = str(record.get("failure_domain") or "")
        if outcome:
            counts_by_outcome[outcome] = counts_by_outcome.get(outcome, 0) + 1
        if proof_status:
            counts_by_proof_status[proof_status] = counts_by_proof_status.get(proof_status, 0) + 1
        if failure_domain:
            counts_by_failure_domain[failure_domain] = counts_by_failure_domain.get(failure_domain, 0) + 1

    latest_record = latest_event.get("receipt_record", {}) if isinstance(latest_event, dict) else {}
    if not isinstance(latest_record, dict):
        latest_record = {}
    latest_pipeline = latest_record.get("pipeline_provenance", {})
    if not isinstance(latest_pipeline, dict):
        latest_pipeline = {}

    last_proven_record = last_proven_event.get("receipt_record", {}) if isinstance(last_proven_event, dict) else {}
    if not isinstance(last_proven_record, dict):
        last_proven_record = {}

    return {
        "generated_at": utc_now(),
        "family_id": FAMILY_ID,
        "contract_path": repo_rel(CONTRACT_PATH),
        "ledger_path": maybe_repo_rel(ledger_path),
        "receipt_events": len(events),
        "live_proof_present": any(record_for(event).get("outcome") == "proven" for event in events),
        "counts_by_outcome": counts_by_outcome,
        "counts_by_proof_status": counts_by_proof_status,
        "counts_by_failure_domain": counts_by_failure_domain,
        "latest_receipt_event_id": latest_event.get("event_id") if isinstance(latest_event, dict) else None,
        "latest_recorded_at": latest_event.get("recorded_at") if isinstance(latest_event, dict) else None,
        "latest_outcome": latest_record.get("outcome"),
        "latest_proof_status": latest_record.get("proof_status"),
        "latest_failure_domain": latest_record.get("failure_domain"),
        "latest_failure_code": latest_record.get("failure_code"),
        "latest_failure_message": latest_record.get("failure_message"),
        "latest_pipeline_status_path": latest_pipeline.get("status_path"),
        "latest_pipeline_status_sha256": latest_pipeline.get("status_sha256"),
        "latest_proof_gate": latest_record.get("proof_gate"),
        "last_proven_receipt_event_id": last_proven_event.get("event_id") if isinstance(last_proven_event, dict) else None,
        "last_proven_at": last_proven_event.get("recorded_at") if isinstance(last_proven_event, dict) else None,
        "last_proven_pipeline_status_path": last_proven_record.get("pipeline_provenance", {}).get("status_path")
        if isinstance(last_proven_record.get("pipeline_provenance"), dict)
        else None,
        "repo_sovereignty": {
            "intake_authority": "acumen",
            "strict_identity_required": True,
            "raw_secret_capture": "forbidden",
            "live_credentials_must_remain_external": True,
        },
    }


def assert_payload_safe(payload: dict[str, Any], *, scope: str) -> None:
    findings = scan_forbidden_content(payload, scope=scope)
    if findings:
        raise SystemExit("\n".join(findings))


def append_event(payload: dict[str, Any], ledger_path: Path = LEDGER_PATH) -> None:
    ensure_surface_files()
    append_jsonl(ledger_path, payload)


def pipeline_sha(path: Path | None) -> str | None:
    if path is None or not path.exists():
        return None
    return sha256_for_file(path)
