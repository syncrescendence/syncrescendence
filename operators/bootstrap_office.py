#!/usr/bin/env python3
"""Instantiate a lawful office inside the successor shell."""

from __future__ import annotations

import argparse
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
OFFICES_ROOT = REPO_ROOT / "offices"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def office_readme(name: str) -> str:
    title = name.replace("-", " ").title()
    return (
        f"# {title} Office\n\n"
        f"Local office for {title}.\n\n"
        "Use this office for local intake, working memory, scratch work, outgoing staging, and platform-local notes.\n"
    )


def lane_readme(title: str, body: str) -> str:
    return f"# {title}\n\n{body}\n"


def bootstrap(name: str) -> Path:
    slug = name.strip().lower()
    title = slug.replace("-", " ").title()
    office = OFFICES_ROOT / slug
    write(office / "README.md", office_readme(slug))
    write(office / "inbox" / "README.md", lane_readme(f"{title} Inbox", "Local intake and pending working items."))
    write(office / "inbox" / "pending" / "README.md", lane_readme(f"{title} Inbox Pending", "New local work awaiting triage or claim."))
    write(office / "inbox" / "active" / "README.md", lane_readme(f"{title} Inbox Active", "Current office-local work in progress."))
    write(office / "inbox" / "done" / "README.md", lane_readme(f"{title} Inbox Done", "Completed local items retained until promoted or compacted."))
    write(office / "inbox" / "failed" / "README.md", lane_readme(f"{title} Inbox Failed", "Items that failed locally and need retry or escalation."))
    write(office / "inbox" / "blocked" / "README.md", lane_readme(f"{title} Inbox Blocked", "Items waiting on another office, human action, or dependency."))
    write(office / "memory" / "README.md", lane_readme(f"{title} Memory", "Office-local working memory."))
    write(office / "memory" / "journal" / "README.md", lane_readme(f"{title} Memory Journal", "Session-local logs and resumability notes."))
    write(office / "memory" / "cache" / "README.md", lane_readme(f"{title} Memory Cache", "Low-durability office-local reference material."))
    write(office / "memory" / "sync" / "README.md", lane_readme(f"{title} Memory Sync", "Cross-office or cross-machine sync notes that have not yet been promoted."))
    write(office / "scratchpad" / "README.md", lane_readme(f"{title} Scratchpad", "Ephemeral local shaping space."))
    write(office / "outbox" / "README.md", lane_readme(f"{title} Outbox", "Local outgoing staging only."))
    write(office / "outbox" / "dispatches" / "README.md", lane_readme(f"{title} Outbox Dispatches", "Office-local staging for outgoing work before federal promotion."))
    write(office / "outbox" / "receipts" / "README.md", lane_readme(f"{title} Outbox Receipts", "Local receipts before they are promoted into federal communications or runtime evidence."))
    write(office / "outbox" / "results" / "README.md", lane_readme(f"{title} Outbox Results", "Result artifacts awaiting promotion, compaction, or archival classification."))
    write(office / "platform" / "README.md", lane_readme(f"{title} Platform", "Harness- or platform-local notes."))
    return office


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="office name, e.g. researcher or planner")
    args = parser.parse_args()
    print(bootstrap(args.name))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
