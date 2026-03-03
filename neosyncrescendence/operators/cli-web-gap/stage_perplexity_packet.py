#!/usr/bin/env python3
"""Create a repo-native Perplexity verification packet."""

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
    parser.add_argument("--claim", required=True)
    parser.add_argument("--why", required=True)
    parser.add_argument("--acceptable-source", action="append", default=[])
    parser.add_argument("--verification-question", action="append", default=[])
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    slug = slugify(args.slug)
    packet_path = ENGINE_DIR / f"PACKET-PERPLEXITY-{slug}.md"
    response_path = INBOX_DIR / f"RESPONSE-PERPLEXITY-{slug}.md"
    if packet_path.exists() and not args.force:
        raise SystemExit(f"Packet already exists: {packet_path}")

    acceptable_sources = args.acceptable_source or [
        "Primary sources and official documentation first.",
        "Direct citations required for factual claims.",
    ]
    verification_questions = args.verification_question or [
        "Is the claim factually correct as stated?",
        "What primary-source-backed caveats or corrections matter most?",
    ]

    body = [
        f"# Perplexity Verification Packet — {args.title}",
        "",
        f"- Surface: `perplexity_web_surface`",
        f"- Packet type: `perplexity_verification`",
        f"- Created: `{utc_now()}`",
        f"- Slug: `{slug}`",
        f"- Return artifact: `{repo_rel(response_path)}`",
        "",
        "## Claim Or Question To Verify",
        "",
        args.claim,
        "",
        "## Why This Verification Matters",
        "",
        args.why,
        "",
        "## Verification Questions",
        "",
    ]
    body.extend(f"- {question}" for question in verification_questions)
    body.extend(
        [
            "",
            "## Acceptable Source Classes",
            "",
        ]
    )
    body.extend(f"- {source}" for source in acceptable_sources)
    body.extend(
        [
            "",
            "## Citation Contract",
            "",
            "- Cite the strongest sources directly.",
            "- Distinguish verified fact from inference.",
            "- Prefer precise dates, identifiers, and official pages.",
            "",
            "## Return Instructions",
            "",
            f"- Save or relay the response back into `{repo_rel(response_path)}`",
            "- Keep citations intact in the returned artifact.",
            "- Return disproofs, caveats, and confidence limits explicitly.",
            "",
            "## Bridge Command",
            "",
            "```bash",
            f"python3 CLI-WEB-GAP/scripts/perplexity_response_bridge.py --dispatch {repo_rel(packet_path)} --response {repo_rel(response_path)} --summary \"<one-line landing summary>\" --project-ontology",
            "```",
            "",
        ]
    )
    packet_path.write_text("\n".join(body), encoding="utf-8")
    print(packet_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
