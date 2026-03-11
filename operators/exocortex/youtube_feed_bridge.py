#!/usr/bin/env python3
"""Emit a YouTube feed/media checkpoint into the shared event and ontology pipeline."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

from exocortex_event_bridge import emit_event, load_policy, normalize_repo_paths, validate_request


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
ONTOLOGY_LOCAL_URL = "http://127.0.0.1:8787/ingest/event"
ONTOLOGY_DOMAIN_URL = "https://syncrescendence.com/ingest/event"
RECONCILER_PATH = REPO_ROOT / "operators" / "runtime" / "reconcile-ajna-events.py"
ACUMEN_TRIAGE_PATH = REPO_ROOT / "operators" / "acumen" / "build_triage_packet.py"


def load_reconciler():
    spec = importlib.util.spec_from_file_location("reconcile_ajna_events", RECONCILER_PATH)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Could not load reconciler from {RECONCILER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_acumen_triage():
    spec = importlib.util.spec_from_file_location("acumen_build_triage_packet", ACUMEN_TRIAGE_PATH)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Could not load Acumen triage helper from {ACUMEN_TRIAGE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--resource-kind", required=True, choices=["video", "channel", "playlist", "search", "commentary"])
    parser.add_argument("--resource-id", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--event-type", default="youtube_feed_checkpoint")
    parser.add_argument("--capture-level", default="summary", choices=["pointer", "summary", "full"])
    parser.add_argument("--durable-capture", default="summary_and_typed_record", choices=["pointer", "typed_record", "summary_and_typed_record"])
    parser.add_argument("--title", default=None)
    parser.add_argument("--channel-id", default=None)
    parser.add_argument("--channel-title", default=None)
    parser.add_argument("--published-at", default=None)
    parser.add_argument("--source-url", default=None)
    parser.add_argument("--repo-paths", nargs="*", default=[])
    parser.add_argument("--ontology-entities", nargs="*", default=["ExoEvent", "KnowledgeItem"])
    parser.add_argument("--payload", default="{}")
    parser.add_argument("--project-ontology", action="store_true")
    parser.add_argument("--ontology-url", choices=["local", "domain"], default="domain")
    parser.add_argument(
        "--acumen-registry",
        default=None,
        help="Optional Acumen registry path. When set, materialize an Acumen-owned handoff under the runtime lane.",
    )
    parser.add_argument(
        "--acumen-runtime-root",
        default="runtime/acumen",
        help="Runtime root for Acumen handoff artifacts when --acumen-registry is provided.",
    )
    args = parser.parse_args()

    policy = load_policy()
    extra_payload = json.loads(args.payload)
    if not isinstance(extra_payload, dict):
        raise SystemExit("Payload must decode to a JSON object.")
    payload = {
        "resource_kind": args.resource_kind,
        "resource_id": args.resource_id,
        **extra_payload,
    }
    optional_fields = {
        "title": args.title,
        "channel_id": args.channel_id,
        "channel_title": args.channel_title,
        "published_at": args.published_at,
        "source_url": args.source_url,
    }
    payload.update({key: value for key, value in optional_fields.items() if value})
    repo_paths = normalize_repo_paths(args.repo_paths)
    validate_request(
        surface="exocortex",
        artifact_class="youtube_feed_metadata",
        durable_capture=args.durable_capture,
        payload=payload,
        policy=policy,
    )
    event_path = emit_event(
        source="commander",
        surface="exocortex",
        artifact_class="youtube_feed_metadata",
        event_type=args.event_type,
        summary=args.summary,
        capture_level=args.capture_level,
        durable_capture=args.durable_capture,
        repo_paths=repo_paths,
        ontology_entities=args.ontology_entities,
        payload=payload,
    )
    print(f"Emitted YouTube checkpoint: {event_path}")

    if args.acumen_registry:
        acumen_triage = load_acumen_triage()
        acumen_runtime_root = Path(args.acumen_runtime_root)
        if not acumen_runtime_root.is_absolute():
            acumen_runtime_root = REPO_ROOT / acumen_runtime_root
        handoff = acumen_triage.materialize_youtube_bridge_handoff(
            registry_path=args.acumen_registry,
            output_root=acumen_runtime_root,
            bridge_payload=payload,
            summary=args.summary,
        )
        print(f"Acumen handoff: {json.dumps(handoff, sort_keys=True)}")

    ontology_url = ONTOLOGY_DOMAIN_URL if args.ontology_url == "domain" else ONTOLOGY_LOCAL_URL
    reconciler = load_reconciler()
    return reconciler.reconcile(
        project_ontology=args.project_ontology,
        ontology_url=ontology_url,
        ontology_timeout_seconds=10.0,
    )


if __name__ == "__main__":
    raise SystemExit(main())
