#!/usr/bin/env python3
"""Render CC94 feed recon/migration artifacts from capture or migrate JSON."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def write_md(path: Path, title: str, rows: list[dict], caveats: list[str]) -> None:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    lines = [
        f"# {title}",
        "",
        f"- Capture date/time: {timestamp}",
        f"- Total count captured: {len(rows)}",
        "- Capture method: direct OpenClaw relay/CDP extraction from Ajna Vivaldi session",
        "- Caveats:",
    ]
    lines.extend([f"  - {caveat}" for caveat in caveats] or ["  - none"])
    lines.extend(["", "## Entries", ""])
    for row in rows:
        label = row.get("handle") or row.get("channel_handle") or row.get("channel_name") or row.get("display_name") or row.get("profile_url") or row.get("channel_url") or "unknown"
        lines.append(f"- {label}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--outdir", required=True)
    args = parser.parse_args()

    data = load_json(Path(args.input))
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    x_fields = [
        "source_account",
        "platform",
        "display_name",
        "handle",
        "profile_url",
        "bio",
        "notes",
    ]
    y_fields = [
        "source_account",
        "platform",
        "channel_name",
        "channel_handle",
        "channel_url",
        "notes",
    ]

    account1_rows: list[dict] = []
    account2_x_rows = data.get("xDest", {}).get("items", [])
    account3_x_rows = data.get("xSource", {}).get("items", [])
    account2_y_rows = data.get("yDest", {}).get("items", [])
    account3_y_rows = data.get("ySource", {}).get("items", [])
    x_missing_rows = data.get("xMissing", [])
    y_missing_rows = data.get("yMissing", [])

    write_csv(outdir / "account1-x-following.csv", account1_rows, x_fields)
    write_md(
        outdir / "account1-x-following.md",
        "Account 1 X Following",
        account1_rows,
        ["Account 1 X identity is not surfaced in the current Vivaldi/X session; capture remains unresolved."],
    )

    write_csv(outdir / "account2-x-following-pre.csv", account2_x_rows, x_fields)
    write_md(
        outdir / "account2-x-following-pre.md",
        "Account 2 X Following (Pre-Mutation)",
        account2_x_rows,
        ["Account 2 inferred as @truongphillipt_ based on sparse destination graph and live X account switcher state."],
    )

    write_csv(outdir / "account2-youtube-subscriptions-pre.csv", account2_y_rows, y_fields)
    write_md(
        outdir / "account2-youtube-subscriptions-pre.md",
        "Account 2 YouTube Subscriptions (Pre-Mutation)",
        account2_y_rows,
        ["Account 2 bound to icloud.truongphillipthanh@gmail.com from visible YouTube account switcher state."],
    )

    write_csv(outdir / "account3-x-following-source.csv", account3_x_rows, x_fields)
    write_md(
        outdir / "account3-x-following-source.md",
        "Account 3 X Following (Source Graph)",
        account3_x_rows,
        [
            "Account 3 inferred as @truongphillipth from live X profile metrics (201 Following) and source-vs-destination graph shape.",
            "DOM capture under-materialized relative to the visible profile metric, so this X source list should be treated as partial until a stronger extraction path is used.",
        ],
    )

    write_csv(outdir / "account3-youtube-subscriptions-source.csv", account3_y_rows, y_fields)
    write_md(
        outdir / "account3-youtube-subscriptions-source.md",
        "Account 3 YouTube Subscriptions (Source Graph)",
        account3_y_rows,
        ["Account 3 bound to truongphillipthanh@gmail.com from visible YouTube account switcher state."],
    )

    write_csv(outdir / "account2-x-missing-from-account3.csv", x_missing_rows, x_fields)
    write_csv(outdir / "account2-youtube-missing-from-account3.csv", y_missing_rows, y_fields)


if __name__ == "__main__":
    main()
