#!/usr/bin/env python3
"""Bridge a returned Perplexity response artifact into the sandbox event ledger."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[2]
OPS_DIR = REPO_ROOT / "operators"
if str(OPS_DIR) not in sys.path:
    sys.path.insert(0, str(OPS_DIR))

from sandbox_event_bridge import emit_event, repo_rel, validate_markdown


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dispatch", required=True)
    parser.add_argument("--response", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--citation-count", type=int, default=None)
    args = parser.parse_args()

    dispatch = validate_markdown(REPO_ROOT / args.dispatch, "dispatch")
    response = validate_markdown(REPO_ROOT / args.response, "response")
    payload = {
        "web_surface": "perplexity",
        "dispatch_packet": repo_rel(dispatch),
        "response_artifact": repo_rel(response),
    }
    if args.citation_count is not None:
        payload["citation_count"] = args.citation_count
    event_path = emit_event(
        source="sandbox",
        surface="exocortex",
        artifact_class="repo_markdown_change",
        event_type="perplexity_response_landed",
        summary=args.summary,
        repo_paths=[repo_rel(dispatch), repo_rel(response)],
        payload=payload,
    )
    print(f"Emitted event: {event_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
