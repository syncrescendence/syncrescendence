#!/usr/bin/env python3
"""Rematerialize Acumen runtime evidence from repo-native append-only ledgers."""

from __future__ import annotations

import argparse
from pathlib import Path

try:
    from .evidence_family import (
        TRAINING_LEDGER_PATH,
        TRAINING_RUNTIME_PATH,
        TRIAGE_LEDGER_PATH,
        TRIAGE_RUNTIME_PATH,
        ensure_surface_files,
        load_jsonl,
        materialize_runtime_rows,
        write_jsonl,
    )
except ImportError:
    from evidence_family import (
        TRAINING_LEDGER_PATH,
        TRAINING_RUNTIME_PATH,
        TRIAGE_LEDGER_PATH,
        TRIAGE_RUNTIME_PATH,
        ensure_surface_files,
        load_jsonl,
        materialize_runtime_rows,
        write_jsonl,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--triage-ledger", default=str(TRIAGE_LEDGER_PATH))
    parser.add_argument("--training-ledger", default=str(TRAINING_LEDGER_PATH))
    parser.add_argument("--triage-runtime", default=str(TRIAGE_RUNTIME_PATH))
    parser.add_argument("--training-runtime", default=str(TRAINING_RUNTIME_PATH))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ensure_surface_files()
    triage_events = load_jsonl(Path(args.triage_ledger).expanduser().resolve())
    training_events = load_jsonl(Path(args.training_ledger).expanduser().resolve())
    triage_rows, training_rows = materialize_runtime_rows(triage_events, training_events)
    write_jsonl(Path(args.triage_runtime).expanduser().resolve(), triage_rows)
    write_jsonl(Path(args.training_runtime).expanduser().resolve(), training_rows)
    print(Path(args.triage_runtime).expanduser().resolve())
    print(Path(args.training_runtime).expanduser().resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
