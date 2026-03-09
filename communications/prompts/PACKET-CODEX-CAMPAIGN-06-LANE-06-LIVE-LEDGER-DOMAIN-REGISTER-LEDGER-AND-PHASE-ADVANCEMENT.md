# Dispatch Packet

**Packet ID**: `PKT-20260309-codex-campaign-06-lane-06-live-ledger-domain-register-ledger-and-phase-advancement`
**Surface**: `codex_parallel_session`
**Role**: `direct_write`
**Date**: `2026-03-09`
**Objective**: add mutation history for the live-ledger domain register and advance seed families where the new proof state justifies it
**Priority**: `high`
**Target**: `the family-of-families control surface`
**Origin lane**: `communications/prompts`
**Expected response**: `communications/responses/RESPONSE-CODEX-CAMPAIGN-06-LANE-06-LIVE-LEDGER-DOMAIN-REGISTER-LEDGER-AND-PHASE-ADVANCEMENT.md`

## Required Output

1. create `orchestration/state/registry/live-ledger-domain-register-ledger.jsonl`
2. advance `office_harness_state` and `config_surface_state` only if the newly landed append-only substrate and rematerialization rules justify it
3. keep tributary widening non-breaking
4. run `git diff --check`
5. report `complete / partial / blocked`
