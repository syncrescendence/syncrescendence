#!/usr/bin/env python3
"""Emit Slack or Discord runtime channel state into the shared event pipeline."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent
RECONCILER_PATH = REPO_ROOT / "reconcile-ajna-events.py"
STATUS_COLLECTOR_PATH = REPO_ROOT / "collect-tooling-surface-status.py"
ONTOLOGY_LOCAL_URL = "http://127.0.0.1:8787/ingest/event"
ONTOLOGY_DOMAIN_URL = "https://syncrescendence.com/ingest/event"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Could not load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--channel", choices=["slack", "discord"], required=True)
    parser.add_argument("--summary")
    parser.add_argument("--project-ontology", action="store_true")
    parser.add_argument("--ontology-url", choices=["local", "domain"], default="domain")
    parser.add_argument("--repo-paths", nargs="*", default=["00-ORCHESTRATION/state/LOCAL-SURFACE-STATUS.md"])
    args = parser.parse_args()

    exocortex = load_module(REPO_ROOT / "exocortex_event_bridge.py", "exocortex_event_bridge")
    collector = load_module(STATUS_COLLECTOR_PATH, "collect_tooling_surface_status")
    report = collector.collect()
    channel_status = ((report.get("openclaw_channels") or {}).get("channels") or {}).get(args.channel, {})
    account = (((report.get("openclaw_channels") or {}).get("channel_accounts") or {}).get(args.channel) or [{}])[0]
    probe = channel_status.get("probe") or {}

    payload = {
        "channel": args.channel,
        "running": channel_status.get("running"),
        "probe_ok": probe.get("ok"),
        "last_inbound_at": account.get("lastInboundAt"),
        "last_outbound_at": account.get("lastOutboundAt"),
    }
    if args.channel == "slack":
        team = probe.get("team") or {}
        bot = probe.get("bot") or {}
        payload["workspace"] = {"id": team.get("id"), "name": team.get("name")}
        payload["bot"] = {"id": bot.get("id"), "name": bot.get("name")}
    else:
        bot = probe.get("bot") or {}
        app = probe.get("application") or {}
        payload["bot"] = {"id": bot.get("id"), "username": bot.get("username")}
        payload["application"] = {
            "id": app.get("id"),
            "intents": app.get("intents"),
        }

    policy = exocortex.load_policy()
    repo_paths = exocortex.normalize_repo_paths(args.repo_paths)
    exocortex.validate_request(
        surface="runtime",
        artifact_class="slack_discord_comms",
        durable_capture="summary_and_typed_record",
        payload=payload,
        policy=policy,
    )
    event_path = exocortex.emit_event(
        source="system",
        surface="runtime",
        artifact_class="slack_discord_comms",
        event_type=f"{args.channel}_channel_state",
        summary=args.summary or f"Captured {args.channel} channel runtime state.",
        capture_level="summary",
        durable_capture="summary_and_typed_record",
        repo_paths=repo_paths,
        ontology_entities=["ExoEvent"],
        payload=payload,
    )
    print(f"Emitted channel checkpoint: {event_path}")

    reconciler = load_module(RECONCILER_PATH, "reconcile_ajna_events")
    ontology_url = ONTOLOGY_DOMAIN_URL if args.ontology_url == "domain" else ONTOLOGY_LOCAL_URL
    return reconciler.reconcile(
        project_ontology=args.project_ontology,
        ontology_url=ontology_url,
        ontology_timeout_seconds=10.0,
    )


if __name__ == "__main__":
    raise SystemExit(main())
