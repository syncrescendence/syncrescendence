#!/usr/bin/env python3
"""Sync a reference tree from an archived shell into the live successor shell."""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
RECEIPTS_DIR = REPO_ROOT / "pedigree" / "rehousing-receipts"


def count_tree(root: Path) -> tuple[int, int]:
    files = 0
    dirs = 0
    for path in root.rglob("*"):
        if path.is_dir():
            dirs += 1
        elif path.is_file():
            files += 1
    return files, dirs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--dest-rel", required=True)
    parser.add_argument("--label", required=True)
    parser.add_argument("--reason", required=True)
    parser.add_argument("--replace", action="store_true")
    args = parser.parse_args()

    source_root = Path(args.source_root).expanduser().resolve()
    if not source_root.exists() or not source_root.is_dir():
        raise SystemExit(f"source tree not found: {source_root}")

    dest_root = (REPO_ROOT / args.dest_rel).resolve()
    if REPO_ROOT not in dest_root.parents and dest_root != REPO_ROOT:
        raise SystemExit(f"destination must stay inside repo: {dest_root}")

    if dest_root.exists():
        if not args.replace:
            raise SystemExit(f"destination already exists: {dest_root} (use --replace)")
        shutil.rmtree(dest_root)

    dest_root.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source_root, dest_root)

    files, dirs = count_tree(dest_root)
    RECEIPTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    receipt_path = RECEIPTS_DIR / f"{args.label}-{timestamp}.json"
    receipt = {
        "label": args.label,
        "reason": args.reason,
        "source_root": str(source_root),
        "dest_root": str(dest_root),
        "files": files,
        "dirs": dirs,
        "timestamp": timestamp,
        "mode": "reference-tree-sync",
    }
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
    print(dest_root)
    print(receipt_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
