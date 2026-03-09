# Dispatch Packet

**Packet ID**: `PKT-20260309-codex-campaign-04-lane-04-commander-office-harness-specimen-direct-write`
**Surface**: `codex_parallel_session`
**Role**: `direct_write`
**Date**: `2026-03-09`
**Objective**: create the first lawful office-harness metadata specimen for commander
**Priority**: `high`
**Target**: `offices/commander/platform/contracts/OFFICE-HARNESS-METADATA.v1.yaml`
**Origin lane**: `communications/prompts`
**Expected response**: `communications/responses/RESPONSE-CODEX-CAMPAIGN-04-LANE-04-COMMANDER-OFFICE-HARNESS-SPECIMEN-DIRECT-WRITE.md`

## Required Output

1. create `offices/commander/platform/contracts/OFFICE-HARNESS-METADATA.v1.yaml`
2. make `commander` the first typed office specimen using the contract shape implied by Campaign 03
3. keep office identity, harness identity, promotion rights, required local paths, and authority fields explicit
4. do not include secrets, tokens, or speculative runtime claims
5. run `git diff --check`
6. report `complete / partial / blocked`
