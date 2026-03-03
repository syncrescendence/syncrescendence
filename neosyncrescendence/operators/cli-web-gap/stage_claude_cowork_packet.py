#!/usr/bin/env python3
"""Create a repo-native Claude Cowork collaboration packet."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
from pathlib import Path
import re


REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE_DIR = REPO_ROOT / "engine"
INBOX_DIR = REPO_ROOT / "-INBOX" / "commander" / "00-INBOX0"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def repo_rel(path: Path) -> str:
    return str(path.resolve().relative_to(REPO_ROOT))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--objective", required=True)
    parser.add_argument("--work-scope", required=True)
    parser.add_argument("--anchor", action="append", default=[])
    parser.add_argument("--deliverable", action="append", default=[])
    parser.add_argument("--output-contract", action="append", default=[])
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    slug = slugify(args.slug)
    packet_path = ENGINE_DIR / f"PACKET-CLAUDE-COWORK-{slug}.md"
    response_path = INBOX_DIR / f"RESPONSE-CLAUDE-COWORK-{slug}.md"
    if packet_path.exists() and not args.force:
        raise SystemExit(f"Packet already exists: {packet_path}")

    anchors = args.anchor or [
        "Add at least one repo, issue, or external anchor with --anchor.",
    ]
    deliverables = args.deliverable or [
        "Return the narrowest artifact or recommendation set that directly advances the work scope.",
    ]
    output_contract = args.output_contract or [
        "Treat Claude Cowork as a collaborative execution surface, not a constitutional authority.",
        "Ground the result in the declared work scope and anchors.",
        "Keep the return artifact bounded, implementation-oriented, and suitable for repo landing.",
    ]

    body = [
        f"# Claude Cowork Collaboration Packet — {args.title}",
        "",
        "- Surface: `claude_cowork_surface`",
        "- Packet type: `claude_cowork_dispatch`",
        f"- Created: `{utc_now()}`",
        f"- Slug: `{slug}`",
        f"- Return artifact: `{repo_rel(response_path)}`",
        "",
        "## Objective",
        "",
        args.objective,
        "",
        "## Work Scope",
        "",
        args.work_scope,
        "",
        "## Anchors",
        "",
    ]
    body.extend(f"- {anchor}" for anchor in anchors)
    body.extend(
        [
            "",
            "## Requested Deliverables",
            "",
        ]
    )
    body.extend(f"- {item}" for item in deliverables)
    body.extend(
        [
            "",
            "## Required Output Contract",
            "",
        ]
    )
    body.extend(f"- {line}" for line in output_contract)
    body.extend(
        [
            "",
            "## Return Instructions",
            "",
            f"- Save or relay the response back into `{repo_rel(response_path)}`",
            "- Do not let the output remain only inside cowork session state.",
            "- Prefer implementation-grade content over conversational recap.",
            "",
            "## Bridge Command",
            "",
            "```bash",
            f"python3 CLI-WEB-GAP/scripts/claude_cowork_response_bridge.py --dispatch {repo_rel(packet_path)} --response {repo_rel(response_path)} --summary \"<one-line landing summary>\" --project-ontology",
            "```",
            "",
        ]
    )
    packet_path.write_text("\n".join(body), encoding="utf-8")
    print(packet_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
