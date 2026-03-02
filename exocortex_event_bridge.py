#!/usr/bin/env python3
"""Emit boundary-compliant exocortex events into the current Ajna landing zone."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent
WORKSPACE_EVENTS_INBOX = Path.home() / ".openclaw" / "workspace" / "events" / "inbox"
CAPTURE_POLICY_PATH = REPO_ROOT / "00-ORCHESTRATION" / "state" / "EXOCORTEX-CAPTURE-POLICY.json"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def compact_timestamp() -> str:
    return datetime.now(UTC).strftime("%Y%m%d-%H%M%S")


def slugify(value: str) -> str:
    return "-".join(
        piece for piece in "".join(ch.lower() if ch.isalnum() else " " for ch in value).split() if piece
    )


def load_policy() -> dict:
    return json.loads(CAPTURE_POLICY_PATH.read_text(encoding="utf-8"))


def payload_keys(value) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, nested in value.items():
            keys.add(str(key))
            keys.update(payload_keys(nested))
    elif isinstance(value, list):
        for nested in value:
            keys.update(payload_keys(nested))
    return keys


def normalize_repo_paths(values: list[str]) -> list[str]:
    normalized: list[str] = []
    for value in values:
        path = (REPO_ROOT / value).resolve()
        if not str(path).startswith(str(REPO_ROOT)):
            raise SystemExit(f"Repo path must stay inside repo root: {value}")
        if "/.obsidian/" in str(path):
            raise SystemExit(f"Repo path must not target .obsidian local state: {value}")
        normalized.append(str(path))
    return normalized


def validate_request(
    *,
    surface: str,
    artifact_class: str,
    durable_capture: str,
    payload: dict,
    policy: dict,
) -> None:
    surfaces = set(policy.get("surfaces", []))
    if surface not in surfaces:
        raise SystemExit(f"Invalid surface {surface!r}; expected one of {sorted(surfaces)}")
    classes = policy.get("artifact_classes", {})
    artifact_policy = classes.get(artifact_class)
    if artifact_policy is None:
        raise SystemExit(f"Invalid artifact_class {artifact_class!r}")
    modes = set(policy.get("durable_capture_modes", []))
    if durable_capture not in modes:
        raise SystemExit(f"Invalid durable_capture {durable_capture!r}; expected one of {sorted(modes)}")
    allowed = set(artifact_policy.get("allowed_durable_capture", []))
    if durable_capture not in allowed:
        raise SystemExit(
            f"durable_capture {durable_capture!r} is not allowed for artifact_class {artifact_class!r}"
        )
    forbidden = set(artifact_policy.get("forbidden_payload_keys", []))
    seen = payload_keys(payload)
    blocked = sorted(forbidden & seen)
    if blocked:
        raise SystemExit(f"Payload contains forbidden keys for {artifact_class}: {blocked}")


def emit_event(
    *,
    source: str,
    surface: str,
    artifact_class: str,
    event_type: str,
    summary: str,
    capture_level: str,
    durable_capture: str,
    repo_paths: list[str],
    ontology_entities: list[str],
    payload: dict,
) -> Path:
    WORKSPACE_EVENTS_INBOX.mkdir(parents=True, exist_ok=True)
    event_id = f"{source}-{compact_timestamp()}-{slugify(event_type)}"
    event_path = WORKSPACE_EVENTS_INBOX / f"{event_id}.json"
    event = {
        "id": event_id,
        "emitted_at": utc_now(),
        "source": source,
        "surface": surface,
        "artifact_class": artifact_class,
        "type": event_type,
        "summary": summary,
        "capture_level": capture_level,
        "durable_capture": durable_capture,
        "repo_paths": repo_paths,
        "ontology_entities": ontology_entities,
        "payload": payload,
    }
    event_path.write_text(json.dumps(event, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return event_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="ajna", help="Current landing zone accepts ajna events by default")
    parser.add_argument("--surface", required=True)
    parser.add_argument("--artifact-class", required=True)
    parser.add_argument("--event-type", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--capture-level", default="summary", choices=["pointer", "summary", "full"])
    parser.add_argument("--durable-capture", required=True)
    parser.add_argument("--repo-paths", nargs="*", default=[])
    parser.add_argument("--ontology-entities", nargs="*", default=[])
    parser.add_argument("--payload", default="{}")
    args = parser.parse_args()

    if args.source != "ajna":
        raise SystemExit("The current reconciliation pipeline only accepts source='ajna'.")

    policy = load_policy()
    payload = json.loads(args.payload)
    if not isinstance(payload, dict):
        raise SystemExit("Payload must decode to a JSON object.")
    repo_paths = normalize_repo_paths(args.repo_paths)
    validate_request(
        surface=args.surface,
        artifact_class=args.artifact_class,
        durable_capture=args.durable_capture,
        payload=payload,
        policy=policy,
    )
    event_path = emit_event(
        source=args.source,
        surface=args.surface,
        artifact_class=args.artifact_class,
        event_type=args.event_type,
        summary=args.summary,
        capture_level=args.capture_level,
        durable_capture=args.durable_capture,
        repo_paths=repo_paths,
        ontology_entities=args.ontology_entities,
        payload=payload,
    )
    print(f"Emitted event: {event_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
