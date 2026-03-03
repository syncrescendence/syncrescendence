#!/usr/bin/env python3
"""Compatibility wrapper for Hazel until local rules are repointed."""

from __future__ import annotations

from pathlib import Path
import runpy
import sys


TARGET = Path(__file__).resolve().parent / "CLI-WEB-GAP" / "scripts" / "finalize_cowork_relay_job.py"
sys.argv[0] = str(TARGET)
runpy.run_path(str(TARGET), run_name="__main__")
