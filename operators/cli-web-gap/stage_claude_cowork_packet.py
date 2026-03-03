#!/usr/bin/env python3
"""Create a sandbox-native Claude Cowork collaboration packet."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
from pathlib import Path
import re


REPO_ROOT = Path(__file__).resolve().parents[2]
PROMPTS_DIR = REPO_ROOT / "communications" / "prompts"
RESPONSES_DIR = REPO_ROOT / "communications" / "responses"


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
    parser.add_argument("--anchor", action="append", default=[])
    parser.add_argument("--deliverable", action="append", default=[])
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    PROMPTS_DIR.mkdir(parents=True, exist_ok=True)
    RESPONSES_DIR.mkdir(parents=True, exist_ok=True)

    slug = slugify(args.slug)
    packet_path = PROMPTS_DIR / f"PACKET-CLAUDE-COWORK-{slug}.md"
    response_path = RESPONSES_DIR / f"RESPONSE-CLAUDE-COWORK-{slug}.md"
    if packet_path.exists() and not args.force:
        raise SystemExit(f"Packet already exists: {packet_path}")

    anchors = args.anchor or ["Add at least one anchor with --anchor."]
    deliverables = args.deliverable or ["Return one concrete deliverable."]

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
        "## Anchors",
        "",
    ]
    body.extend(f"- {anchor}" for anchor in anchors)
    body.extend(["", "## Requested Deliverables", ""])
    body.extend(f"- {deliverable}" for deliverables in deliverables)
    body.extend(
        [
            "",
            "## Return Instructions",
            "",
            f"- Save or relay the response back into `{repo_rel(response_path)}`",
            "",
            "## Bridge Command",
            "",
            "```bash",
            f"python3 operators/cli-web-gap/claude_cowork_response_bridge.py --dispatch {repo_rel(packet_path)} --response {repo_rel(response_path)} --summary \"<one-line landing summary>\"",
            "```",
            "",
        ]
    )
    packet_path.write_text("\n".join(body), encoding="utf-8")
    print(packet_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
