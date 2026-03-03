#!/usr/bin/env python3
"""Emit a Manus checkpoint into the event pipeline and optionally project it."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

from exocortex_event_bridge import emit_event, load_policy, normalize_repo_paths, validate_request


REPO_ROOT = Path(__file__).resolve().parent
ONTOLOGY_LOCAL_URL = "http://127.0.0.1:8787/ingest/event"
ONTOLOGY_DOMAIN_URL = "https://syncrescendence.com/ingest/event"
RECONCILER_PATH = REPO_ROOT / "reconcile-ajna-events.py"


def load_reconciler():
    spec = importlib.util.spec_from_file_location("reconcile_ajna_events", RECONCILER_PATH)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Could not load reconciler from {RECONCILER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workflow", required=True)
    parser.add_argument("--status", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--event-type", default="manus_queue_state")
    parser.add_argument("--capture-level", default="summary", choices=["pointer", "summary", "full"])
    parser.add_argument("--repo-paths", nargs="*", default=[])
    parser.add_argument("--ontology-entities", nargs="*", default=[])
    parser.add_argument("--payload", default="{}")
    parser.add_argument("--project-ontology", action="store_true")
    parser.add_argument("--ontology-url", choices=["local", "domain"], default="domain")
    args = parser.parse_args()

    policy = load_policy()
    payload = json.loads(args.payload)
    if not isinstance(payload, dict):
        raise SystemExit("Payload must decode to a JSON object.")
    payload = {
        "workflow": args.workflow,
        "status": args.status,
        **payload,
    }
    repo_paths = normalize_repo_paths(args.repo_paths)
    validate_request(
        surface="exocortex",
        artifact_class="manus_workflow",
        durable_capture="summary_and_typed_record",
        payload=payload,
        policy=policy,
    )
    event_path = emit_event(
        source="manus",
        surface="exocortex",
        artifact_class="manus_workflow",
        event_type=args.event_type,
        summary=args.summary,
        capture_level=args.capture_level,
        durable_capture="summary_and_typed_record",
        repo_paths=repo_paths,
        ontology_entities=args.ontology_entities,
        payload=payload,
    )
    print(f"Emitted Manus checkpoint: {event_path}")

    ontology_url = ONTOLOGY_DOMAIN_URL if args.ontology_url == "domain" else ONTOLOGY_LOCAL_URL
    reconciler = load_reconciler()
    return reconciler.reconcile(
        project_ontology=args.project_ontology,
        ontology_url=ontology_url,
        ontology_timeout_seconds=10.0,
    )


if __name__ == "__main__":
    raise SystemExit(main())
