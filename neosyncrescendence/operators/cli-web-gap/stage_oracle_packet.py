#!/usr/bin/env python3
"""Create a repo-native Oracle web dispatch packet."""

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
    parser.add_argument("--state-summary", required=True)
    parser.add_argument("--anchor", action="append", default=[])
    parser.add_argument("--output-contract", action="append", default=[])
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    slug = slugify(args.slug)
    packet_path = ENGINE_DIR / f"PACKET-ORACLE-{slug}.md"
    response_path = INBOX_DIR / f"RESPONSE-ORACLE-{slug}.md"
    if packet_path.exists() and not args.force:
        raise SystemExit(f"Packet already exists: {packet_path}")

    anchors = args.anchor or [
        "Add at least one repo or GitHub anchor with --anchor.",
    ]
    output_contract = args.output_contract or [
        "Lead with your own thesis before consensus or precedent.",
        "Ground the response in the provided anchors.",
        "Return only what is needed for downstream engineering or decision.",
    ]

    body = [
        f"# Oracle Dispatch Packet — {args.title}",
        "",
        f"- Surface: `oracle_web_surface`",
        f"- Packet type: `oracle_dispatch`",
        f"- Created: `{utc_now()}`",
        f"- Slug: `{slug}`",
        f"- Return artifact: `{repo_rel(response_path)}`",
        "",
        "## Objective",
        "",
        args.objective,
        "",
        "## Current State Summary",
        "",
        args.state_summary,
        "",
        "## Anchor Links",
        "",
    ]
    body.extend(f"- {anchor}" for anchor in anchors)
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
            "- Do not let the response remain only in web-session state.",
            "- Keep citations and concrete source references where relevant.",
            "",
            "## Bridge Command",
            "",
            "```bash",
            f"python3 CLI-WEB-GAP/scripts/oracle_response_bridge.py --dispatch {repo_rel(packet_path)} --response {repo_rel(response_path)} --summary \"<one-line landing summary>\" --project-ontology",
            "```",
            "",
        ]
    )
    packet_path.write_text("\n".join(body), encoding="utf-8")
    print(packet_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
