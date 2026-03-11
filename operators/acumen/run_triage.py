#!/usr/bin/env python3
"""Run Acumen triage with strict contracts and repo-local evidence outputs."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any

from build_triage_packet import build_triage_packet, resolve_channel
from gemini_triage_adapter import DEFAULT_API_BASE, DEFAULT_MODEL, GeminiTriageError, invoke_gemini_packet
from triage_contract import (
    TARGET_DEPTH_VALUES,
    TARGET_POLISH_VALUES,
    build_decision_record,
    render_prompt_preview,
    utc_now,
    validate_decision,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", required=True)
    parser.add_argument("--poll-jsonl", required=True)
    parser.add_argument("--queue-jsonl", required=True)
    parser.add_argument("--training-jsonl", required=True)
    parser.add_argument("--status-json", default="runtime/acumen/triage-status.json")
    parser.add_argument("--artifact-dir", default="runtime/acumen/out/triage")
    parser.add_argument("--mode", choices=("auto", "heuristic", "gemini"), default="auto")
    parser.add_argument("--model", default=os.environ.get("ACUMEN_GEMINI_MODEL", DEFAULT_MODEL))
    parser.add_argument("--api-base", default=os.environ.get("ACUMEN_GEMINI_API_BASE", DEFAULT_API_BASE))
    parser.add_argument("--api-key-env", default="GEMINI_API_KEY")
    parser.add_argument("--timeout-seconds", type=float, default=45.0)
    parser.add_argument("--max-live-calls", type=int, default=5)
    parser.add_argument("--max-retries", type=int, default=2)
    parser.add_argument("--retry-backoff-seconds", type=float, default=1.5)
    parser.add_argument("--max-prompt-chars", type=int, default=18000)
    parser.add_argument("--max-output-tokens", type=int, default=220)
    parser.add_argument("--max-total-tokens", type=int, default=4096)
    parser.add_argument("--estimated-cost-per-call-usd", type=float, default=0.0)
    parser.add_argument("--max-estimated-cost-usd", type=float, default=0.0)
    return parser.parse_args()


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        payload = json.loads(line)
        if isinstance(payload, dict):
            rows.append(payload)
    return rows


def append_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def summarize_text(video: dict[str, Any], limit: int = 160) -> str:
    base = " ".join(
        str(video.get(key, "")).strip()
        for key in ("title", "description", "initial_transcript")
        if str(video.get(key, "")).strip()
    )
    if len(base) <= limit:
        return base
    return base[: limit - 1].rstrip() + "..."


def next_promoted_shape(default_depth: str, default_polish: str) -> tuple[str, str]:
    if default_depth in TARGET_DEPTH_VALUES:
        depth_index = TARGET_DEPTH_VALUES.index(default_depth)
        if depth_index < len(TARGET_DEPTH_VALUES) - 1:
            return TARGET_DEPTH_VALUES[depth_index + 1], default_polish
    if default_polish in TARGET_POLISH_VALUES:
        polish_index = TARGET_POLISH_VALUES.index(default_polish)
        if polish_index < len(TARGET_POLISH_VALUES) - 1:
            return default_depth, TARGET_POLISH_VALUES[polish_index + 1]
    return "Transcript", "editorial"


def heuristic_decision(channel: dict[str, Any], video: dict[str, Any]) -> dict[str, Any]:
    text = " ".join(str(video.get(key, "")).lower() for key in ("title", "description", "initial_transcript"))
    priority_band = str(channel.get("priority_band", "Tier 3"))
    default_depth = str(channel.get("default_compression", "Precis"))
    default_polish = str(channel.get("default_polish", "charitable"))

    if any(term in text for term in ("live debate", "live demo", "hearing", "cross-examination")):
        return {
            "decision": "Flag-for-Primary",
            "target_depth": "Transcript",
            "target_polish": "clean_verbatim",
            "rationale": "Live or adversarial dynamics create signal that compression will likely erase.",
            "primary_flag_reason": "Original viewing is required because interaction dynamics carry the signal.",
        }

    if any(term in text for term in ("architecture", "tpu", "alphafold", "gemini", "breakthrough", "roadmap", "release")):
        promoted_depth, promoted_polish = next_promoted_shape(default_depth, default_polish)
        if priority_band in {"Tier 1", "Tier 2"} and (
            promoted_depth != default_depth or promoted_polish != default_polish
        ):
            return {
                "decision": "Promote",
                "target_depth": promoted_depth,
                "target_polish": promoted_polish,
                "rationale": "Architecture or platform-shift language suggests non-routine signal worth escalation.",
                "primary_flag_reason": None,
            }
        return {
            "decision": "Compress",
            "target_depth": default_depth,
            "target_polish": default_polish,
            "rationale": "Architecture or platform-shift language is useful but remains compressible at the channel default.",
            "primary_flag_reason": None,
        }

    if any(term in text for term in ("walkthrough", "tutorial", "implementation", "tokenizer", "backpropagation")):
        return {
            "decision": "Compress",
            "target_depth": default_depth,
            "target_polish": default_polish,
            "rationale": "Implementation-oriented material is useful but remains compressible at the channel default.",
            "primary_flag_reason": None,
        }

    if priority_band == "Tier 1":
        return {
            "decision": "Headline",
            "target_depth": "Headline",
            "target_polish": "clean_verbatim",
            "rationale": "Tier 1 channel activity is worth logging even when novelty is not yet proven.",
            "primary_flag_reason": None,
        }

    return {
        "decision": "Skip",
        "target_depth": "None",
        "target_polish": "clean_verbatim",
        "rationale": "No strong novelty markers were detected in the available metadata.",
        "primary_flag_reason": None,
    }


def packet_sha256(packet: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(packet, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()


def queue_existing_ids(queue_rows: list[dict[str, Any]]) -> set[str]:
    existing: set[str] = set()
    for row in queue_rows:
        video_id = str(row.get("video_id", "")).strip()
        if video_id:
            existing.add(video_id)
    return existing


def main() -> int:
    args = parse_args()
    registry_path = Path(args.registry).expanduser().resolve()
    poll_path = Path(args.poll_jsonl).expanduser().resolve()
    queue_path = Path(args.queue_jsonl).expanduser().resolve()
    training_path = Path(args.training_jsonl).expanduser().resolve()
    status_path = Path(args.status_json).expanduser().resolve()
    artifact_dir = Path(args.artifact_dir).expanduser().resolve()

    registry = load_json(registry_path, {})
    poll_rows = load_jsonl(poll_path)
    existing_ids = queue_existing_ids(load_jsonl(queue_path))

    artifact_dir.mkdir(parents=True, exist_ok=True)
    packet_dir = artifact_dir / "packets"
    prompt_dir = artifact_dir / "prompts"
    packet_dir.mkdir(parents=True, exist_ok=True)
    prompt_dir.mkdir(parents=True, exist_ok=True)

    queue_rows: list[dict[str, Any]] = []
    training_rows: list[dict[str, Any]] = []
    failures = 0
    skipped_existing = 0
    gemini_calls = 0
    estimated_cost = 0.0
    gemini_available = bool(os.environ.get(args.api_key_env, "").strip())

    for video in poll_rows:
        video_id = str(video.get("video_id", "")).strip()
        channel_id = str(video.get("channel_id", "")).strip()
        if video_id and video_id in existing_ids:
            skipped_existing += 1
            continue

        try:
            channel = resolve_channel(registry, channel_id)
            packet = build_triage_packet(registry, channel_id, video)
        except SystemExit as exc:
            failures += 1
            training_rows.append(
                {
                    "captured_at": utc_now(),
                    "video_id": video_id,
                    "channel_id": channel_id,
                    "mode": args.mode,
                    "status": "invalid_input",
                    "error": str(exc),
                }
            )
            continue

        packet_name = video_id or packet["packet_id"]
        packet_path = write_json(packet_dir / f"{packet_name}.json", packet)
        prompt_preview = render_prompt_preview(packet)
        prompt_path = prompt_dir / f"{packet_name}.md"
        prompt_path.write_text(prompt_preview, encoding="utf-8")
        packet_digest = packet_sha256(packet)

        active_mode = args.mode
        if active_mode == "auto":
            active_mode = "gemini" if gemini_available else "heuristic"

        live_allowed = (
            active_mode == "gemini"
            and gemini_calls < args.max_live_calls
            and (
                args.max_estimated_cost_usd <= 0
                or estimated_cost + args.estimated_cost_per_call_usd <= args.max_estimated_cost_usd
            )
        )

        if active_mode == "gemini" and not live_allowed:
            if args.mode == "gemini":
                failures += 1
                training_rows.append(
                    {
                        "captured_at": utc_now(),
                        "packet_id": packet["packet_id"],
                        "video_id": video_id,
                        "channel_id": channel_id,
                        "model": args.model,
                        "mode": "gemini",
                        "status": "skipped_budget_guardrail",
                        "packet_path": str(packet_path),
                        "prompt_path": str(prompt_path),
                        "packet_sha256": packet_digest,
                        "estimated_cost_usd": round(estimated_cost, 6),
                    }
                )
                continue
            active_mode = "heuristic"

        if active_mode == "gemini":
            try:
                result = invoke_gemini_packet(
                    packet,
                    model=args.model,
                    api_base=args.api_base,
                    api_key_env=args.api_key_env,
                    timeout_seconds=args.timeout_seconds,
                    max_attempts=args.max_retries + 1,
                    retry_backoff_seconds=args.retry_backoff_seconds,
                    max_prompt_chars=args.max_prompt_chars,
                    max_output_tokens=args.max_output_tokens,
                    max_total_tokens=args.max_total_tokens,
                )
                budget_guardrails = dict(result["budget_guardrails"])
                budget_guardrails["max_live_calls"] = args.max_live_calls
                budget_guardrails["estimated_cost_per_call_usd"] = args.estimated_cost_per_call_usd
                budget_guardrails["max_estimated_cost_usd"] = args.max_estimated_cost_usd
                record = build_decision_record(
                    packet,
                    result["decision"],
                    model=args.model,
                    attempts_used=result["attempts_used"],
                    prompt_chars=result["prompt_chars"],
                    usage_metadata=result["usage_metadata"],
                    budget_guardrails=budget_guardrails,
                    source_mode="gemini",
                    abstract=summarize_text(video),
                )
                gemini_calls += 1
                estimated_cost += args.estimated_cost_per_call_usd
                queue_rows.append(record)
                if video_id:
                    existing_ids.add(video_id)
                training_rows.append(
                    {
                        "captured_at": utc_now(),
                        "packet_id": packet["packet_id"],
                        "video_id": video_id,
                        "channel_id": channel_id,
                        "model": args.model,
                        "mode": "gemini",
                        "status": "ok",
                        "attempts": result["attempts_used"],
                        "packet_path": str(packet_path),
                        "prompt_path": str(prompt_path),
                        "packet_sha256": packet_digest,
                        "response_sha256": result["response_sha256"],
                        "usage_metadata": result["usage_metadata"],
                        "budget_guardrails": budget_guardrails,
                        "decision": record["decision"],
                        "target_depth": record["target_depth"],
                        "target_polish": record["target_polish"],
                        "estimated_cost_usd": args.estimated_cost_per_call_usd,
                    }
                )
                continue
            except GeminiTriageError as exc:
                failures += 1
                training_rows.append(
                    {
                        "captured_at": utc_now(),
                        "packet_id": packet["packet_id"],
                        "video_id": video_id,
                        "channel_id": channel_id,
                        "model": args.model,
                        "mode": "gemini",
                        "status": "failed",
                        "error": str(exc),
                        "attempts": args.max_retries + 1,
                        "packet_path": str(packet_path),
                        "prompt_path": str(prompt_path),
                        "packet_sha256": packet_digest,
                    }
                )
                continue

        payload = heuristic_decision(channel, video)
        errors = validate_decision(packet, payload)
        if errors:
            failures += 1
            training_rows.append(
                {
                    "captured_at": utc_now(),
                    "packet_id": packet["packet_id"],
                    "video_id": video_id,
                    "channel_id": channel_id,
                    "model": "heuristic",
                    "mode": "heuristic",
                    "status": "failed",
                    "error": " | ".join(errors),
                    "packet_path": str(packet_path),
                    "prompt_path": str(prompt_path),
                    "packet_sha256": packet_digest,
                }
            )
            continue

        record = build_decision_record(
            packet,
            payload,
            model="heuristic",
            attempts_used=0,
            prompt_chars=len(prompt_preview),
            usage_metadata={},
            budget_guardrails={
                "mode": "heuristic",
                "max_live_calls": args.max_live_calls,
                "estimated_cost_per_call_usd": args.estimated_cost_per_call_usd,
                "max_estimated_cost_usd": args.max_estimated_cost_usd,
            },
            source_mode="heuristic",
            abstract=summarize_text(video),
        )
        queue_rows.append(record)
        if video_id:
            existing_ids.add(video_id)
        training_rows.append(
            {
                "captured_at": utc_now(),
                "packet_id": packet["packet_id"],
                "video_id": video_id,
                "channel_id": channel_id,
                "model": "heuristic",
                "mode": "heuristic",
                "status": "ok",
                "attempts": 0,
                "packet_path": str(packet_path),
                "prompt_path": str(prompt_path),
                "packet_sha256": packet_digest,
                "decision": record["decision"],
                "target_depth": record["target_depth"],
                "target_polish": record["target_polish"],
            }
        )

    append_jsonl(queue_path, queue_rows)
    append_jsonl(training_path, training_rows)

    status = {
        "captured_at": utc_now(),
        "registry": str(registry_path),
        "poll_jsonl": str(poll_path),
        "queue_jsonl": str(queue_path),
        "training_jsonl": str(training_path),
        "artifact_dir": str(artifact_dir),
        "mode": args.mode,
        "processed": len(poll_rows),
        "queued": len(queue_rows),
        "training_records": len(training_rows),
        "failures": failures,
        "skipped_existing": skipped_existing,
        "ok": failures == 0,
        "external_dependencies": {
            "gemini_api": {
                "required": args.mode == "gemini" or (args.mode == "auto" and gemini_available),
                "available": gemini_available,
                "api_key_env": args.api_key_env,
                "api_base": args.api_base,
                "model": args.model,
                "calls_used": gemini_calls,
                "max_live_calls": args.max_live_calls,
                "estimated_cost_usd": round(estimated_cost, 6),
                "estimated_cost_per_call_usd": args.estimated_cost_per_call_usd,
                "max_estimated_cost_usd": args.max_estimated_cost_usd,
                "timeout_seconds": args.timeout_seconds,
                "max_attempts_per_call": args.max_retries + 1,
                "max_prompt_chars": args.max_prompt_chars,
                "max_output_tokens": args.max_output_tokens,
                "max_total_tokens": args.max_total_tokens,
            }
        },
    }
    status_path.parent.mkdir(parents=True, exist_ok=True)
    status_path.write_text(json.dumps(status, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(queue_path)
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
