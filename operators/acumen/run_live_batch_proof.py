#!/usr/bin/env python3
"""Run a live Acumen batch and append a durable proof receipt."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
from typing import Any

try:
    from .live_batch_proof_family import (
        CONTRACT_PATH,
        EVENT_TYPE,
        FAMILY_ID,
        LEDGER_PATH,
        LEDGER_SCHEMA,
        STATUS_PATH,
        append_event,
        assert_payload_safe,
        build_status_payload,
        classify_receipt,
        ensure_surface_files,
        load_events,
        maybe_repo_rel,
        next_event_id,
        pipeline_sha,
        repo_rel,
        sha256_for_payload,
        summarize_command_result,
        utc_now,
    )
except ImportError:
    from live_batch_proof_family import (  # type: ignore
        CONTRACT_PATH,
        EVENT_TYPE,
        FAMILY_ID,
        LEDGER_PATH,
        LEDGER_SCHEMA,
        STATUS_PATH,
        append_event,
        assert_payload_safe,
        build_status_payload,
        classify_receipt,
        ensure_surface_files,
        load_events,
        maybe_repo_rel,
        next_event_id,
        pipeline_sha,
        repo_rel,
        sha256_for_payload,
        summarize_command_result,
        utc_now,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", default="runtime/acumen/registry.json")
    parser.add_argument("--binding", default="orchestration/state/ACUMEN-IDENTITY-BINDING-CC87.json")
    parser.add_argument("--queue", default="runtime/acumen/triage-decisions.jsonl")
    parser.add_argument("--training-jsonl", default="runtime/acumen/training-corpus.jsonl")
    parser.add_argument("--out", default="runtime/acumen/out")
    parser.add_argument("--pipeline-status-json", default="orchestration/state/ACUMEN-PIPELINE-STATUS.json")
    parser.add_argument("--identity-status-json", default="orchestration/state/ACUMEN-IDENTITY-STATUS.json")
    parser.add_argument("--poll-status-json", default="orchestration/state/ACUMEN-YOUTUBE-POLL-STATUS.json")
    parser.add_argument("--triage-status-json", default="runtime/acumen/triage-status.json")
    parser.add_argument("--proof-status-json", default=str(STATUS_PATH))
    parser.add_argument("--receipt-ledger", default=str(LEDGER_PATH))
    parser.add_argument("--actor", default="acumen.live_batch")
    parser.add_argument("--youtube-api-env", default="ACUMEN_YOUTUBE_API_KEY")
    parser.add_argument("--gemini-api-env", default="GEMINI_API_KEY")
    parser.add_argument("--api-base", default="https://generativelanguage.googleapis.com/v1beta/models")
    parser.add_argument("--timeout-seconds", type=float, default=45.0)
    parser.add_argument("--max-live-calls", type=int, default=12)
    parser.add_argument("--max-retries", type=int, default=2)
    parser.add_argument("--retry-backoff-seconds", type=float, default=1.5)
    parser.add_argument("--max-prompt-chars", type=int, default=18000)
    parser.add_argument("--max-output-tokens", type=int, default=220)
    parser.add_argument("--max-total-tokens", type=int, default=4096)
    parser.add_argument("--estimated-cost-per-call-usd", type=float, default=0.0)
    parser.add_argument("--max-estimated-cost-usd", type=float, default=0.0)
    parser.add_argument("--force-poll", action="store_true")
    return parser.parse_args()


def load_json_object(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    return payload if isinstance(payload, dict) else None


def run_command(command: list[str]) -> dict[str, Any]:
    proc = subprocess.run(command, capture_output=True, text=True, check=False)
    return {
        "command": command,
        "returncode": proc.returncode,
        "stdout": (proc.stdout or "").strip()[:2000],
        "stderr": (proc.stderr or "").strip()[:2000],
        "ok": proc.returncode == 0,
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    ensure_surface_files()

    registry_path = Path(args.registry).expanduser().resolve()
    binding_path = Path(args.binding).expanduser().resolve()
    queue_path = Path(args.queue).expanduser().resolve()
    training_path = Path(args.training_jsonl).expanduser().resolve()
    out_path = Path(args.out).expanduser().resolve()
    pipeline_status_path = Path(args.pipeline_status_json).expanduser().resolve()
    identity_status_path = Path(args.identity_status_json).expanduser().resolve()
    poll_status_path = Path(args.poll_status_json).expanduser().resolve()
    triage_status_path = Path(args.triage_status_json).expanduser().resolve()
    proof_status_path = Path(args.proof_status_json).expanduser().resolve()
    ledger_path = Path(args.receipt_ledger).expanduser().resolve()

    youtube_api_present = bool(os.environ.get(args.youtube_api_env, "").strip())
    gemini_api_present = bool(os.environ.get(args.gemini_api_env, "").strip())

    registry_validation: dict[str, Any] | None = None
    pipeline_run: dict[str, Any] | None = None
    pipeline_status: dict[str, Any] | None = None

    if youtube_api_present and gemini_api_present:
        registry_validation = run_command(
            [
                "python3",
                str(Path(__file__).resolve().parent / "validate_registry.py"),
                "--registry",
                str(registry_path),
                "--strict",
            ]
        )
        if registry_validation["ok"]:
            pipeline_command = [
                "python3",
                str(Path(__file__).resolve().parent / "pipeline_flow.py"),
                "--registry",
                str(registry_path),
                "--queue",
                str(queue_path),
                "--out",
                str(out_path),
                "--status-json",
                str(pipeline_status_path),
                "--identity-binding",
                str(binding_path),
                "--identity-status-json",
                str(identity_status_path),
                "--poll-status-json",
                str(poll_status_path),
                "--triage-status-json",
                str(triage_status_path),
                "--poll-mode",
                "live",
                "--training-jsonl",
                str(training_path),
                "--triage-mode",
                "gemini",
                "--triage-api-key-env",
                args.gemini_api_env,
                "--triage-api-base",
                args.api_base,
                "--triage-timeout-seconds",
                str(args.timeout_seconds),
                "--max-live-calls",
                str(args.max_live_calls),
                "--max-retries",
                str(args.max_retries),
                "--retry-backoff-seconds",
                str(args.retry_backoff_seconds),
                "--max-prompt-chars",
                str(args.max_prompt_chars),
                "--max-output-tokens",
                str(args.max_output_tokens),
                "--max-total-tokens",
                str(args.max_total_tokens),
                "--estimated-cost-per-call-usd",
                str(args.estimated_cost_per_call_usd),
                "--max-estimated-cost-usd",
                str(args.max_estimated_cost_usd),
                "--strict-identity",
            ]
            if args.force_poll:
                pipeline_command.append("--force-poll")
            pipeline_run = run_command(pipeline_command)
            pipeline_status = load_json_object(pipeline_status_path)

    classification = classify_receipt(
        youtube_api_present=youtube_api_present,
        gemini_api_present=gemini_api_present,
        registry_validation=registry_validation,
        pipeline_status=pipeline_status,
    )

    pipeline_attempted = pipeline_run is not None
    receipt_record: dict[str, Any] = {
        "entrypoint": "make acumen-live-batch",
        "outcome": classification["outcome"],
        "proof_status": classification["proof_status"],
        "failure_domain": classification["failure_domain"],
        "failure_code": classification["failure_code"],
        "failure_message": classification["failure_message"],
        "credential_state": {
            "youtube_api_env": args.youtube_api_env,
            "youtube_api_present": youtube_api_present,
            "gemini_api_env": args.gemini_api_env,
            "gemini_api_present": gemini_api_present,
            "raw_secret_capture": "forbidden",
        },
        "repo_sovereignty": {
            "intake_authority": "acumen",
            "strict_identity_required": True,
            "live_credentials_must_remain_external": True,
            "raw_secret_capture": "forbidden",
        },
        "registry_validation": summarize_command_result(registry_validation),
        "pipeline_command": summarize_command_result(pipeline_run),
        "pipeline_provenance": {
            "status_path": maybe_repo_rel(pipeline_status_path) if pipeline_attempted else None,
            "status_sha256": pipeline_sha(pipeline_status_path) if pipeline_attempted else None,
            "identity_status_path": maybe_repo_rel(identity_status_path) if pipeline_attempted else None,
            "poll_status_path": maybe_repo_rel(poll_status_path) if pipeline_attempted else None,
            "triage_status_path": maybe_repo_rel(triage_status_path) if pipeline_attempted else None,
            "snapshot": classification["pipeline_summary"],
        },
        "proof_gate": classification["proof_gate"],
    }
    assert_payload_safe(receipt_record, scope="receipt_record")

    event = {
        "schema_version": LEDGER_SCHEMA,
        "event_id": next_event_id(ledger_path),
        "event_type": EVENT_TYPE,
        "family_id": FAMILY_ID,
        "recorded_at": utc_now(),
        "actor": args.actor,
        "contract_path": repo_rel(CONTRACT_PATH),
        "proof_status_path": maybe_repo_rel(proof_status_path),
        "receipt_record_sha256": sha256_for_payload(receipt_record),
        "receipt_record": receipt_record,
    }
    append_event(event, ledger_path)

    summary = build_status_payload(load_events(ledger_path), ledger_path)
    write_json(proof_status_path, summary)

    print(maybe_repo_rel(ledger_path))
    print(event["event_id"])
    print(maybe_repo_rel(proof_status_path))

    outcome = str(classification["outcome"])
    if outcome == "proven":
        return 0
    if outcome == "blocked":
        return 2
    if outcome == "completed_not_proven":
        return 3
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
