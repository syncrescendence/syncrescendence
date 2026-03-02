#!/usr/bin/env python3
"""Emit a Cloudflare domain cutover checkpoint into the shared event pipeline."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

from exocortex_event_bridge import emit_event, load_policy, normalize_repo_paths, validate_request


REPO_ROOT = Path(__file__).resolve().parent
ONTOLOGY_LOCAL_URL = "http://127.0.0.1:8787/ingest/event"
ONTOLOGY_DOMAIN_URL = "https://syncrescendence.com/ingest/event"
RECONCILER_PATH = REPO_ROOT / "reconcile-ajna-events.py"
STATUS_COLLECTOR_PATH = REPO_ROOT / "collect-tooling-surface-status.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Could not load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hostname", default="syncrescendence.com")
    parser.add_argument("--summary", default="Captured Cloudflare domain cutover state.")
    parser.add_argument("--project-ontology", action="store_true")
    parser.add_argument("--ontology-url", choices=["local", "domain"], default="domain")
    parser.add_argument(
        "--repo-paths",
        nargs="*",
        default=[
            "00-ORCHESTRATION/state/impl/CLOUDFLARED-ONTOLOGY-STAGE1.md",
            "00-ORCHESTRATION/state/impl/ONTOLOGY-DOMAIN-STAGE1.md",
        ],
    )
    args = parser.parse_args()

    status_module = load_module(STATUS_COLLECTOR_PATH, "collect_tooling_surface_status")
    report = status_module.collect()
    cloudflared = report.get("cloudflared", {})
    ontology = report.get("ontology", {})
    payload = {
        "hostname": args.hostname,
        "dig_resolves": bool((ontology.get("domain_dig") or {}).get("resolves")),
        "edge_health_reachable": bool((ontology.get("domain_health_edge") or {}).get("reachable")),
        "default_local_resolver_reachable": bool((ontology.get("domain_health") or {}).get("reachable")),
        "tunnel_present": bool(cloudflared.get("tunnel_present")),
        "launch_agent_state": (cloudflared.get("launch_agent") or {}).get("state"),
        "tunnel_name": cloudflared.get("tunnel_name"),
    }

    policy = load_policy()
    repo_paths = normalize_repo_paths(args.repo_paths)
    validate_request(
        surface="exocortex",
        artifact_class="cloudflare_dns_domain",
        durable_capture="pointer",
        payload=payload,
        policy=policy,
    )
    event_path = emit_event(
        source="system",
        surface="exocortex",
        artifact_class="cloudflare_dns_domain",
        event_type="domain_cutover_state",
        summary=args.summary,
        capture_level="pointer",
        durable_capture="pointer",
        repo_paths=repo_paths,
        ontology_entities=["ExoEvent"],
        payload=payload,
    )
    print(f"Emitted Cloudflare domain checkpoint: {event_path}")

    reconciler = load_module(RECONCILER_PATH, "reconcile_ajna_events")
    ontology_url = ONTOLOGY_DOMAIN_URL if args.ontology_url == "domain" else ONTOLOGY_LOCAL_URL
    return reconciler.reconcile(
        project_ontology=args.project_ontology,
        ontology_url=ontology_url,
        ontology_timeout_seconds=10.0,
    )


if __name__ == "__main__":
    raise SystemExit(main())
