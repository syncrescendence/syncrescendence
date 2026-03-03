#!/usr/bin/env python3
"""Create a sandbox-native NotebookLM synthesis packet."""

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
    parser.add_argument("--source", action="append", default=[])
    parser.add_argument("--question", action="append", default=[])
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    PROMPTS_DIR.mkdir(parents=True, exist_ok=True)
    RESPONSES_DIR.mkdir(parents=True, exist_ok=True)

    slug = slugify(args.slug)
    packet_path = PROMPTS_DIR / f"PACKET-NOTEBOOKLM-{slug}.md"
    response_path = RESPONSES_DIR / f"RESPONSE-NOTEBOOKLM-{slug}.md"
    if packet_path.exists() and not args.force:
        raise SystemExit(f"Packet already exists: {packet_path}")

    sources = args.source or ["Add at least one source with --source."]
    questions = args.question or ["What are the highest-signal synthesized takeaways?"]

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
    ]
    body.extend(f"- {source}" for source in sources)
    body.extend(["", "## Focus Questions", ""])
    body.extend(f"- {question}" for question in questions)
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
            f"python3 operators/cli-web-gap/notebooklm_response_bridge.py --dispatch {repo_rel(packet_path)} --response {repo_rel(response_path)} --summary \"<one-line landing summary>\"",
            "```",
            "",
        ]
    )
    packet_path.write_text("\n".join(body), encoding="utf-8")
    print(packet_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
