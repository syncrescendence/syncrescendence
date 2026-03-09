# Dispatch Packet

**Packet ID**: `PKT-20260309-codex-campaign-06-lane-01-office-harness-ledger-and-rematerialization`
**Surface**: `codex_parallel_session`
**Role**: `direct_write`
**Date**: `2026-03-09`
**Objective**: create append-only mutation history and deterministic rematerialization for office-harness state
**Priority**: `highest`
**Target**: `office-harness state as a true repo-native proof family`
**Origin lane**: `communications/prompts`
**Expected response**: `communications/responses/RESPONSE-CODEX-CAMPAIGN-06-LANE-01-OFFICE-HARNESS-LEDGER-AND-REMATERIALIZATION.md`

## Required Output

1. create `orchestration/state/registry/office-harness-binding-ledger.jsonl`
2. define the minimal rebinding event shape and rematerialization rule from the ledger into `office-harness-bindings.effective.json`
3. keep the effective registry subordinate and replaceable
4. run `git diff --check`
5. report `complete / partial / blocked`
