#!/usr/bin/env python3
"""Bridge a returned Perplexity response artifact into the shared event/ontology pipeline."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from exocortex_event_bridge import (
    emit_event,
    load_policy,
    normalize_repo_paths,
    validate_request,
)


def validate_markdown(path: Path, label: str) -> Path:
    resolved = path.resolve()
    if not str(resolved).startswith(str(REPO_ROOT)):
        raise SystemExit(f"{label} must stay inside repo root: {path}")
    if not resolved.exists():
        raise SystemExit(f"{label} does not exist: {resolved}")
    if resolved.suffix.lower() != ".md":
        raise SystemExit(f"{label} must be a markdown file: {resolved}")
    return resolved


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dispatch", required=True)
    parser.add_argument("--response", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--citation-count", type=int, default=None)
    parser.add_argument("--project-ontology", action="store_true")
    parser.add_argument("--ontology-url", default="https://syncrescendence.com/ingest/event")
    args = parser.parse_args()

    dispatch = validate_markdown(REPO_ROOT / args.dispatch, "dispatch")
    response = validate_markdown(REPO_ROOT / args.response, "response")
    policy = load_policy()
    repo_paths = normalize_repo_paths([str(dispatch.relative_to(REPO_ROOT)), str(response.relative_to(REPO_ROOT))])
    payload = {
        "web_surface": "perplexity",
        "dispatch_packet": str(dispatch.relative_to(REPO_ROOT)),
        "response_artifact": str(response.relative_to(REPO_ROOT)),
    }
    if args.citation_count is not None:
        payload["citation_count"] = args.citation_count
    validate_request(
        surface="exocortex",
        artifact_class="repo_markdown_change",
        durable_capture="summary_and_typed_record",
        payload=payload,
        policy=policy,
    )
    event_path = emit_event(
        source="commander",
        surface="exocortex",
        artifact_class="repo_markdown_change",
        event_type="perplexity_response_landed",
        summary=args.summary,
        capture_level="summary",
        durable_capture="summary_and_typed_record",
        repo_paths=repo_paths,
        ontology_entities=["ExoEvent", "KnowledgeItem"],
        payload=payload,
    )
    print(f"Emitted event: {event_path}")
    if args.project_ontology:
        subprocess.run(
            [
                "python3",
                str(REPO_ROOT / "reconcile-ajna-events.py"),
                "--project-ontology",
                "--ontology-url",
                args.ontology_url,
            ],
            check=True,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
