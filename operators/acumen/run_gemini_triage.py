#!/usr/bin/env python3
"""Run Gemini triage for a single Acumen packet and emit a strict decision record."""

from __future__ import annotations

import argparse

from gemini_triage_adapter import DEFAULT_API_BASE, DEFAULT_MODEL, GeminiTriageError, invoke_gemini_packet
from triage_contract import append_jsonl, build_decision_record, load_json, write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", required=True, help="Path to an Acumen triage packet JSON artifact.")
    parser.add_argument("--output", required=True, help="Path for the strict decision JSON artifact.")
    parser.add_argument("--append-jsonl", help="Optional queue path for appending the decision record.")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--api-base", default=DEFAULT_API_BASE)
    parser.add_argument("--api-key-env", default="GEMINI_API_KEY")
    parser.add_argument("--timeout-seconds", type=float, default=45.0)
    parser.add_argument("--max-attempts", type=int, default=3)
    parser.add_argument("--retry-backoff-seconds", type=float, default=1.5)
    parser.add_argument("--max-prompt-chars", type=int, default=18000)
    parser.add_argument("--max-output-tokens", type=int, default=220)
    parser.add_argument("--max-total-tokens", type=int, default=4096)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    packet = load_json(args.packet)
    try:
        result = invoke_gemini_packet(
            packet,
            model=args.model,
            api_base=args.api_base,
            api_key_env=args.api_key_env,
            timeout_seconds=args.timeout_seconds,
            max_attempts=args.max_attempts,
            retry_backoff_seconds=args.retry_backoff_seconds,
            max_prompt_chars=args.max_prompt_chars,
            max_output_tokens=args.max_output_tokens,
            max_total_tokens=args.max_total_tokens,
        )
    except GeminiTriageError as exc:
        raise SystemExit(str(exc))

    record = build_decision_record(
        packet,
        result["decision"],
        model=args.model,
        attempts_used=result["attempts_used"],
        prompt_chars=result["prompt_chars"],
        usage_metadata=result["usage_metadata"],
        budget_guardrails=result["budget_guardrails"],
        source_mode="gemini",
    )
    output_path = write_json(args.output, record)
    print(output_path)
    if args.append_jsonl:
        queue_path = append_jsonl(args.append_jsonl, record)
        print(queue_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
