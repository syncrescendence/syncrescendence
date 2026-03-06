#!/usr/bin/env python3
"""Emit connector manifest/control-plane status checkpoints into event and ontology pipelines."""

from __future__ import annotations

import argparse
import importlib.util
import json
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


def summarize_manifest(manifest: dict) -> dict:
    return {
        "manifest_version": manifest.get("version"),
        "manifest_status": manifest.get("status"),
        "connector_count": manifest.get("counts", {}).get("connector_count"),
        "connector_source_count": manifest.get("counts", {}).get("source_count"),
        "external_target_count": manifest.get("counts", {}).get("external_target_count"),
        "unknown_sources_not_in_registry": manifest.get("gaps", {}).get("unknown_sources_not_in_registry", []),
        "unknown_internal_targets_not_in_registry": manifest.get("gaps", {}).get(
            "unknown_internal_targets_not_in_registry", []
        ),
    }


def summarize_status(status: dict) -> dict:
    return {
        "status_version": status.get("version"),
        "status_state": status.get("status"),
        "control_plane_readiness": status.get("readiness", {}).get("control_plane_readiness"),
        "surface_profile_coverage_pct": status.get("readiness", {}).get("surface_profile_coverage_pct"),
        "teleology_coverage_pct": status.get("readiness", {}).get("teleology_coverage_pct"),
        "connector_count": status.get("counts", {}).get("connector_count"),
        "high_fanout_count": status.get("counts", {}).get("high_fanout_count"),
        "profile_missing_count": status.get("counts", {}).get("profile_missing_count"),
        "cross_boundary_heavy_count": status.get("counts", {}).get("cross_boundary_heavy_count"),
        "unresolved_source_count": status.get("counts", {}).get("unresolved_source_count"),
        "unresolved_internal_target_count": status.get("counts", {}).get("unresolved_internal_target_count"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        default="orchestration/state/EXOCORTEX-CONNECTOR-MANIFEST-CC91.json",
    )
    parser.add_argument(
        "--control-status",
        default="orchestration/state/EXOCORTEX-CONTROL-PLANE-STATUS-CC91.json",
    )
    parser.add_argument(
        "--repo-paths",
        nargs="*",
        default=[
            "orchestration/state/EXOCORTEX-CONNECTOR-MANIFEST-CC91.json",
            "orchestration/state/EXOCORTEX-CONTROL-PLANE-STATUS-CC91.json",
            "orchestration/state/impl/EXOCORTEX-CONTROL-PLANE-STATUS-CC91.md",
        ],
    )
    parser.add_argument(
        "--summary",
        default="Exocortex connector manifest and control-plane status synchronized.",
    )
    parser.add_argument("--project-ontology", action="store_true")
    parser.add_argument("--ontology-url", choices=["local", "domain"], default="domain")
    args = parser.parse_args()

    exocortex = load_module(SCRIPT_DIR / "exocortex_event_bridge.py", "exocortex_event_bridge")
    manifest_path = (REPO_ROOT / args.manifest).resolve()
    status_path = (REPO_ROOT / args.control_status).resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    status = None
    if status_path.exists():
        status = json.loads(status_path.read_text(encoding="utf-8"))

    manifest_payload = summarize_manifest(manifest)
    policy = exocortex.load_policy()
    repo_paths = exocortex.normalize_repo_paths(args.repo_paths)
    exocortex.validate_request(
        surface="exocortex",
        artifact_class="exocortex_connector_manifest",
        durable_capture="summary_and_typed_record",
        payload=manifest_payload,
        policy=policy,
    )
    event_path = exocortex.emit_event(
        source="system",
        surface="exocortex",
        artifact_class="exocortex_connector_manifest",
        event_type="exocortex_connector_manifest_snapshot",
        summary=args.summary,
        capture_level="summary",
        durable_capture="summary_and_typed_record",
        repo_paths=repo_paths,
        ontology_entities=["ExoEvent", "ConfigSnapshot"],
        payload=manifest_payload,
    )
    print(f"Emitted connector checkpoint: {event_path}")

    if isinstance(status, dict):
        status_payload = summarize_status(status)
        exocortex.validate_request(
            surface="exocortex",
            artifact_class="exocortex_control_plane_status",
            durable_capture="summary_and_typed_record",
            payload=status_payload,
            policy=policy,
        )
        status_event = exocortex.emit_event(
            source="system",
            surface="exocortex",
            artifact_class="exocortex_control_plane_status",
            event_type="exocortex_control_plane_status_snapshot",
            summary="Exocortex control-plane status synchronized.",
            capture_level="summary",
            durable_capture="summary_and_typed_record",
            repo_paths=repo_paths,
            ontology_entities=["ExoEvent", "ConfigSnapshot"],
            payload=status_payload,
        )
        print(f"Emitted control-plane checkpoint: {status_event}")

    reconciler = load_module(RECONCILER_PATH, "reconcile_ajna_events")
    ontology_url = ONTOLOGY_DOMAIN_URL if args.ontology_url == "domain" else ONTOLOGY_LOCAL_URL
    return reconciler.reconcile(
        project_ontology=args.project_ontology,
        ontology_url=ontology_url,
        ontology_timeout_seconds=10.0,
    )


if __name__ == "__main__":
    raise SystemExit(main())
