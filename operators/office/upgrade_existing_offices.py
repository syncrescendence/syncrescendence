#!/usr/bin/env python3
"""Refine existing offices with richer lawful substructure."""

from __future__ import annotations

import argparse
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
OFFICES_ROOT = REPO_ROOT / "offices"


def write_if_missing(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def lane(title: str, body: str) -> str:
    return f"# {title}\n\n{body}\n"


def refine_office(office: Path) -> None:
    title = office.name.replace("-", " ").title()

    write_if_missing(
        office / "inbox" / "pending" / "README.md",
        lane(f"{title} Inbox Pending", "New local work awaiting triage or claim."),
    )
    write_if_missing(
        office / "inbox" / "active" / "README.md",
        lane(f"{title} Inbox Active", "Current office-local work in progress."),
    )
    write_if_missing(
        office / "inbox" / "done" / "README.md",
        lane(f"{title} Inbox Done", "Completed local items retained until promoted or compacted."),
    )
    write_if_missing(
        office / "inbox" / "failed" / "README.md",
        lane(f"{title} Inbox Failed", "Items that failed locally and need retry or escalation."),
    )
    write_if_missing(
        office / "inbox" / "blocked" / "README.md",
        lane(f"{title} Inbox Blocked", "Items waiting on another office, human action, or dependency."),
    )

    write_if_missing(
        office / "outbox" / "dispatches" / "README.md",
        lane(f"{title} Outbox Dispatches", "Office-local staging for outgoing work before federal promotion."),
    )
    write_if_missing(
        office / "outbox" / "receipts" / "README.md",
        lane(f"{title} Outbox Receipts", "Local receipts before they are promoted into federal communications or runtime evidence."),
    )
    write_if_missing(
        office / "outbox" / "results" / "README.md",
        lane(f"{title} Outbox Results", "Result artifacts awaiting promotion, compaction, or archival classification."),
    )

    write_if_missing(
        office / "memory" / "journal" / "README.md",
        lane(f"{title} Memory Journal", "Session-local logs and resumability notes."),
    )
    write_if_missing(
        office / "memory" / "cache" / "README.md",
        lane(f"{title} Memory Cache", "Low-durability office-local reference material."),
    )
    write_if_missing(
        office / "memory" / "sync" / "README.md",
        lane(f"{title} Memory Sync", "Cross-office or cross-machine sync notes that have not yet been promoted."),
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--office", action="append", help="specific office slug(s) to refine")
    args = parser.parse_args()

    if args.office:
        offices = [OFFICES_ROOT / slug.strip().lower() for slug in args.office]
    else:
        offices = sorted(path for path in OFFICES_ROOT.iterdir() if path.is_dir() and not path.name.startswith("."))

    for office in offices:
        if not office.is_dir():
            raise SystemExit(f"office not found: {office}")
        refine_office(office)
        print(office)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
