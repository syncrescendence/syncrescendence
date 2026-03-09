# Dispatch Packet

**Packet ID**: `PKT-20260309-codex-campaign-04-lane-06-ratification-pointer-rollout-direct-write`
**Surface**: `codex_parallel_session`
**Role**: `direct_write`
**Date**: `2026-03-09`
**Objective**: write the non-breaking ratification-pointer rollout law
**Priority**: `high`
**Target**: `orchestration/state/impl/RATIFICATION-POINTER-ROLLOUT-v1.md`
**Origin lane**: `communications/prompts`
**Expected response**: `communications/responses/RESPONSE-CODEX-CAMPAIGN-04-LANE-06-RATIFICATION-POINTER-ROLLOUT-DIRECT-WRITE.md`

## Required Output

1. create `orchestration/state/impl/RATIFICATION-POINTER-ROLLOUT-v1.md`
2. define the schema-law first, validator compatibility second, header-change last rollout order
3. define temporary compatibility treatment for legacy authority-bearing rows versus informative-only rows
4. keep the live tributary proof non-breaking
5. run `git diff --check`
6. report `complete / partial / blocked`
