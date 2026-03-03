#!/usr/bin/env python3
"""Create a repo-native NotebookLM synthesis packet."""

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
    parser.add_argument("--source-set", required=True)
    parser.add_argument("--focus-question", action="append", default=[])
    parser.add_argument("--source-anchor", action="append", default=[])
    parser.add_argument("--output-contract", action="append", default=[])
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    slug = slugify(args.slug)
    packet_path = ENGINE_DIR / f"PACKET-NOTEBOOKLM-{slug}.md"
    response_path = INBOX_DIR / f"RESPONSE-NOTEBOOKLM-{slug}.md"
    if packet_path.exists() and not args.force:
        raise SystemExit(f"Packet already exists: {packet_path}")

    focus_questions = args.focus_question or [
        "What are the strongest convergences, tensions, and open questions inside the source set?",
        "Which claims appear most actionable for downstream engineering or planning?",
    ]
    source_anchors = args.source_anchor or [
        "Add at least one repo or external source-set anchor with --source-anchor.",
    ]
    output_contract = args.output_contract or [
        "Treat NotebookLM as source-bounded synthesis, not canonical authority.",
        "Ground the response in the provided source set and distinguish direct source-backed points from synthesis.",
        "Return only the material needed for downstream repo landing, reconciliation, or implementation.",
    ]

    body = [
        f"# NotebookLM Synthesis Packet — {args.title}",
        "",
        "- Surface: `notebooklm_surface`",
        "- Packet type: `notebooklm_synthesis`",
        f"- Created: `{utc_now()}`",
        f"- Slug: `{slug}`",
        f"- Return artifact: `{repo_rel(response_path)}`",
        "",
        "## Objective",
        "",
        args.objective,
        "",
        "## Source Set",
        "",
        args.source_set,
        "",
        "## Source Anchors",
        "",
    ]
    body.extend(f"- {anchor}" for anchor in source_anchors)
    body.extend(
        [
            "",
            "## Focus Questions",
            "",
        ]
    )
    body.extend(f"- {question}" for question in focus_questions)
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
            "- Do not let the result remain only inside NotebookLM web state.",
            "- Keep the returned artifact concise, source-bounded, and citation-aware where possible.",
            "",
            "## Bridge Command",
            "",
            "```bash",
            f"python3 CLI-WEB-GAP/scripts/notebooklm_response_bridge.py --dispatch {repo_rel(packet_path)} --response {repo_rel(response_path)} --summary \"<one-line landing summary>\" --project-ontology",
            "```",
            "",
        ]
    )
    packet_path.write_text("\n".join(body), encoding="utf-8")
    print(packet_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
