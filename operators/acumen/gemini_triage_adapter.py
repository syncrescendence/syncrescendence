#!/usr/bin/env python3
"""Gemini invocation helpers for Acumen triage packets."""

from __future__ import annotations

import hashlib
import json
import os
import time
from typing import Any
import urllib.error
import urllib.request

from triage_contract import DECISION_JSON_SCHEMA, SYSTEM_INSTRUCTION, render_user_prompt, validate_decision, validate_packet


DEFAULT_MODEL = "gemini-2.5-flash"
DEFAULT_API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"
DEFAULT_USER_AGENT = "syncrescendence-acumen-triage/1.0"
RETRYABLE_STATUS_CODES = {408, 429, 500, 502, 503, 504}


class GeminiTriageError(RuntimeError):
    """Raised when the Gemini triage adapter cannot return a valid decision."""


def resolve_api_key(env_name: str) -> str:
    value = os.environ.get(env_name, "").strip()
    if not value:
        raise GeminiTriageError(f"Missing Gemini API key in environment variable {env_name}.")
    return value


def retryable(message: str) -> GeminiTriageError:
    return GeminiTriageError(f"Retryable {message}")


def build_request_payload(packet: dict[str, Any], *, max_output_tokens: int) -> tuple[dict[str, Any], int]:
    user_prompt = render_user_prompt(packet)
    prompt_chars = len(SYSTEM_INSTRUCTION) + len(user_prompt)
    payload = {
        "systemInstruction": {"parts": [{"text": SYSTEM_INSTRUCTION}]},
        "contents": [
            {
                "role": "user",
                "parts": [{"text": user_prompt}],
            }
        ],
        "generationConfig": {
            "temperature": 0,
            "candidateCount": 1,
            "maxOutputTokens": max_output_tokens,
            "responseMimeType": "application/json",
            "responseJsonSchema": DECISION_JSON_SCHEMA,
        },
    }
    return payload, prompt_chars


def request_json(
    *,
    url: str,
    api_key: str,
    payload: dict[str, Any],
    timeout_seconds: float,
) -> tuple[dict[str, Any], str]:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "User-Agent": DEFAULT_USER_AGENT,
            "x-goog-api-key": api_key,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            raw_body = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        raw_body = exc.read().decode("utf-8", errors="replace")
        try:
            error_payload = json.loads(raw_body)
        except Exception:
            error_payload = {"raw": raw_body}
        detail = json.dumps(error_payload, sort_keys=True)
        if exc.code in RETRYABLE_STATUS_CODES:
            raise retryable(f"Gemini HTTP {exc.code}: {detail}") from exc
        raise GeminiTriageError(f"Gemini HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise retryable(f"Gemini transport failure: {exc.reason}") from exc

    try:
        parsed = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise retryable(f"Gemini returned non-JSON HTTP body: {exc}") from exc
    if not isinstance(parsed, dict):
        raise retryable("Gemini HTTP body must decode to an object.")
    return parsed, hashlib.sha256(raw_body.encode("utf-8")).hexdigest()


def extract_candidate_text(response: dict[str, Any]) -> str:
    candidates = response.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        raise retryable("Gemini response missing candidates.")
    first = candidates[0]
    if not isinstance(first, dict):
        raise retryable("Gemini candidate payload is malformed.")
    content = first.get("content")
    if not isinstance(content, dict):
        raise retryable("Gemini candidate missing content object.")
    parts = content.get("parts")
    if not isinstance(parts, list) or not parts:
        raise retryable("Gemini candidate missing content parts.")

    text_parts: list[str] = []
    for part in parts:
        if not isinstance(part, dict):
            continue
        text = part.get("text")
        if isinstance(text, str):
            text_parts.append(text)
    text = "".join(text_parts).strip()
    if not text:
        raise retryable("Gemini candidate text was empty.")
    return text


def extract_usage_metadata(response: dict[str, Any]) -> dict[str, Any]:
    usage = response.get("usageMetadata")
    if not isinstance(usage, dict):
        raise retryable("Gemini response missing usageMetadata.")
    return usage


def to_int(value: Any) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def validate_budget(
    *,
    prompt_chars: int,
    max_prompt_chars: int,
    usage_metadata: dict[str, Any],
    max_total_tokens: int,
) -> None:
    if prompt_chars > max_prompt_chars:
        raise GeminiTriageError(
            f"Prompt budget exceeded before invocation: {prompt_chars} chars > {max_prompt_chars} chars."
        )
    total_tokens = to_int(usage_metadata.get("totalTokenCount"))
    if total_tokens is None:
        raise retryable("Gemini response missing usageMetadata.totalTokenCount.")
    if total_tokens > max_total_tokens:
        raise GeminiTriageError(
            f"Token budget exceeded: totalTokenCount={total_tokens} > max_total_tokens={max_total_tokens}."
        )


def invoke_gemini_packet(
    packet: dict[str, Any],
    *,
    model: str = DEFAULT_MODEL,
    api_base: str = DEFAULT_API_BASE,
    api_key_env: str = "GEMINI_API_KEY",
    timeout_seconds: float = 45.0,
    max_attempts: int = 3,
    retry_backoff_seconds: float = 1.5,
    max_prompt_chars: int = 18000,
    max_output_tokens: int = 220,
    max_total_tokens: int = 4096,
) -> dict[str, Any]:
    packet_errors = validate_packet(packet)
    if packet_errors:
        raise GeminiTriageError("\n".join(packet_errors))
    if max_attempts < 1:
        raise GeminiTriageError("max_attempts must be >= 1.")
    if max_output_tokens < 1:
        raise GeminiTriageError("max_output_tokens must be >= 1.")

    api_key = resolve_api_key(api_key_env)
    request_payload, prompt_chars = build_request_payload(packet, max_output_tokens=max_output_tokens)
    if prompt_chars > max_prompt_chars:
        raise GeminiTriageError(
            f"Prompt budget exceeded before invocation: {prompt_chars} chars > {max_prompt_chars} chars."
        )
    url = f"{api_base.rstrip('/')}/{model}:generateContent"

    last_error: GeminiTriageError | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            response, response_sha256 = request_json(
                url=url,
                api_key=api_key,
                payload=request_payload,
                timeout_seconds=timeout_seconds,
            )
            usage_metadata = extract_usage_metadata(response)
            validate_budget(
                prompt_chars=prompt_chars,
                max_prompt_chars=max_prompt_chars,
                usage_metadata=usage_metadata,
                max_total_tokens=max_total_tokens,
            )
            try:
                decision = json.loads(extract_candidate_text(response))
            except json.JSONDecodeError as exc:
                raise retryable(f"Gemini returned malformed JSON decision: {exc}") from exc
            errors = validate_decision(packet, decision)
            if errors:
                raise retryable("Gemini decision failed contract validation: " + " | ".join(errors))
            return {
                "decision": decision,
                "attempts_used": attempt,
                "prompt_chars": prompt_chars,
                "usage_metadata": usage_metadata,
                "response_sha256": response_sha256,
                "budget_guardrails": {
                    "max_attempts": max_attempts,
                    "attempts_used": attempt,
                    "max_prompt_chars": max_prompt_chars,
                    "max_output_tokens": max_output_tokens,
                    "max_total_tokens": max_total_tokens,
                    "prompt_chars": prompt_chars,
                },
            }
        except GeminiTriageError as exc:
            last_error = exc
            should_retry = str(exc).startswith("Retryable ")
            if not should_retry or attempt == max_attempts:
                break
            time.sleep(retry_backoff_seconds * attempt)

    if last_error is None:
        raise GeminiTriageError("Gemini triage failed without an explicit error.")
    raise GeminiTriageError(f"Gemini triage failed after {max_attempts} attempt(s): {last_error}")
