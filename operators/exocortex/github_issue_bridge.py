#!/usr/bin/env python3
"""Emit a GitHub issue or PR checkpoint into the shared event pipeline."""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
from pathlib import Path

from exocortex_event_bridge import emit_event, load_policy, normalize_repo_paths, validate_request


REPO_ROOT = Path(__file__).resolve().parent
ONTOLOGY_LOCAL_URL = "http://127.0.0.1:8787/ingest/event"
ONTOLOGY_DOMAIN_URL = "https://syncrescendence.com/ingest/event"
RECONCILER_PATH = REPO_ROOT / "reconcile-ajna-events.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Could not load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def gh_json(command: list[str]) -> dict:
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise SystemExit((result.stderr or result.stdout).strip() or "gh command failed")
    return json.loads(result.stdout)


def issue_or_pr(repo: str, number: int) -> tuple[str, dict]:
    issue_cmd = [
        "gh",
        "issue",
        "view",
        str(number),
        "--repo",
        repo,
        "--json",
        "number,title,state,url,labels",
    ]
    issue = subprocess.run(issue_cmd, capture_output=True, text=True, check=False)
    if issue.returncode == 0:
        return "issue", json.loads(issue.stdout)

    pr_cmd = [
        "gh",
        "pr",
        "view",
        str(number),
        "--repo",
        repo,
        "--json",
        "number,title,state,url,labels",
    ]
    pr = subprocess.run(pr_cmd, capture_output=True, text=True, check=False)
    if pr.returncode == 0:
        return "pull_request", json.loads(pr.stdout)
    raise SystemExit((issue.stderr or pr.stderr or issue.stdout or pr.stdout).strip() or "No issue or PR found")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--number", type=int, required=True)
    parser.add_argument("--summary")
    parser.add_argument("--event-type", default="github_issue_state")
    parser.add_argument("--project-ontology", action="store_true")
    parser.add_argument("--ontology-url", choices=["local", "domain"], default="domain")
    parser.add_argument("--repo-paths", nargs="*", default=[])
    args = parser.parse_args()

    kind, item = issue_or_pr(args.repo, args.number)
    payload = {
        "repo": args.repo,
        "kind": kind,
        "number": item["number"],
        "title": item["title"],
        "state": item["state"],
        "url": item["url"],
        "labels": [label["name"] for label in item.get("labels", [])],
    }
    summary = args.summary or f"Captured GitHub {kind} #{item['number']} state: {item['title']} ({item['state']})."

    policy = load_policy()
    repo_paths = normalize_repo_paths(args.repo_paths)
    validate_request(
        surface="github",
        artifact_class="github_issue_pr",
        durable_capture="pointer",
        payload=payload,
        policy=policy,
    )
    event_path = emit_event(
        source="system",
        surface="github",
        artifact_class="github_issue_pr",
        event_type=args.event_type,
        summary=summary,
        capture_level="pointer",
        durable_capture="pointer",
        repo_paths=repo_paths,
        ontology_entities=["ExoEvent"],
        payload=payload,
    )
    print(f"Emitted GitHub checkpoint: {event_path}")

    reconciler = load_module(RECONCILER_PATH, "reconcile_ajna_events")
    ontology_url = ONTOLOGY_DOMAIN_URL if args.ontology_url == "domain" else ONTOLOGY_LOCAL_URL
    return reconciler.reconcile(
        project_ontology=args.project_ontology,
        ontology_url=ontology_url,
        ontology_timeout_seconds=10.0,
    )


if __name__ == "__main__":
    raise SystemExit(main())
