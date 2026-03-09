# Dispatch Packet

**Packet ID**: `PKT-20260309-codex-campaign-02-lane-06-edge-wake-reproof-sidecar`  
**Surface**: `codex_parallel_session`  
**Role**: `direct_write`  
**Date**: `2026-03-09`  
**Objective**: obtain one fresh automatic Hazel wake receipt on a new outgoing `.status.json` without reordering the macro campaign  
**Priority**: `medium`  
**Target**: `bounded edge observation closure`  
**Origin lane**: `communications/prompts`  
**Expected response**: `communications/responses/RESPONSE-CODEX-CAMPAIGN-02-LANE-06-EDGE-WAKE-REPROOF-SIDECAR.md`

## Required Output

1. attempt one bounded fresh automatic wake reproving
2. if it lands, record the receipt
3. if it does not, record the exact remaining observation gap
4. keep this lane sidecar only and do not reopen macro ordering around it
5. run `git diff --check`
6. report `complete / partial / blocked`
