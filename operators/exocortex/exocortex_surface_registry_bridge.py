#!/usr/bin/env python3
"""Emit the canonical exocortex surface registry into event and ontology pipelines."""

from __future__ import annotations

import argparse
import importlib.util
import json
from collections import Counter
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
RECONCILER_PATH = REPO_ROOT / "operators" / "runtime" / "reconcile-ajna-events.py"
ONTOLOGY_LOCAL_URL = "http://127.0.0.1:8787/ingest/event"
ONTOLOGY_DOMAIN_URL = "https://syncrescendence.com/ingest/event"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Could not load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_payload(registry: dict) -> dict:
    surfaces = registry.get("surfaces", [])
    if not isinstance(surfaces, list):
        raise SystemExit("Registry file must contain a list at key 'surfaces'.")
    auth_deps = registry.get("auth_dependencies", [])
    if not isinstance(auth_deps, list):
        raise SystemExit("Registry file key 'auth_dependencies' must be a list.")

    class_counts: Counter[str] = Counter()
    access_counts: Counter[str] = Counter()
    statuses: Counter[str] = Counter()
    for item in surfaces:
        if not isinstance(item, dict):
            continue
        class_counts[str(item.get("class", "unknown"))] += 1
        access_counts[str(item.get("access_model", "unknown"))] += 1
        statuses[str(item.get("status", "unknown"))] += 1

    return {
        "registry_version": registry.get("version"),
        "canonical_identity": registry.get("canonical_identity"),
        "canonical_workspace_domain": registry.get("canonical_workspace_domain"),
        "canonical_github_repo": registry.get("canonical_github_repo"),
        "surface_count": len(surfaces),
        "auth_dependency_count": len(auth_deps),
        "class_counts": dict(sorted(class_counts.items())),
        "access_model_counts": dict(sorted(access_counts.items())),
        "status_counts": dict(sorted(statuses.items())),
        "auth_dependencies": auth_deps,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--registry",
        default="orchestration/state/EXOCORTEX-SURFACE-REGISTRY-CC90.json",
    )
    parser.add_argument(
        "--repo-paths",
        nargs="*",
        default=[
            "orchestration/state/EXOCORTEX-SURFACE-REGISTRY-CC90.json",
            "orchestration/state/impl/EXOCORTEX-SURFACE-REGISTRY-CC90.md",
        ],
    )
    parser.add_argument(
        "--summary",
        default="Canonical exocortex registry synchronized with 37 surfaces and auth dependency edges.",
    )
    parser.add_argument("--project-ontology", action="store_true")
    parser.add_argument("--ontology-url", choices=["local", "domain"], default="domain")
    args = parser.parse_args()

    exocortex = load_module(SCRIPT_DIR / "exocortex_event_bridge.py", "exocortex_event_bridge")
    registry_path = (REPO_ROOT / args.registry).resolve()
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    payload = build_payload(registry)

    policy = exocortex.load_policy()
    repo_paths = exocortex.normalize_repo_paths(args.repo_paths)
    exocortex.validate_request(
        surface="exocortex",
        artifact_class="exocortex_surface_registry",
        durable_capture="summary_and_typed_record",
        payload=payload,
        policy=policy,
    )
    event_path = exocortex.emit_event(
        source="system",
        surface="exocortex",
        artifact_class="exocortex_surface_registry",
        event_type="exocortex_surface_registry_snapshot",
        summary=args.summary,
        capture_level="summary",
        durable_capture="summary_and_typed_record",
        repo_paths=repo_paths,
        ontology_entities=["ExoEvent", "ConfigSnapshot"],
        payload=payload,
    )
    print(f"Emitted exocortex registry checkpoint: {event_path}")

    reconciler = load_module(RECONCILER_PATH, "reconcile_ajna_events")
    ontology_url = ONTOLOGY_DOMAIN_URL if args.ontology_url == "domain" else ONTOLOGY_LOCAL_URL
    return reconciler.reconcile(
        project_ontology=args.project_ontology,
        ontology_url=ontology_url,
        ontology_timeout_seconds=10.0,
    )


if __name__ == "__main__":
    raise SystemExit(main())
