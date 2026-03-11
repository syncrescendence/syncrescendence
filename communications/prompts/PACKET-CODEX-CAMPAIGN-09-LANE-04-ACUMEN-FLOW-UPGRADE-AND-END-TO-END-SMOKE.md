# Dispatch Packet

**Packet ID**: `PKT-20260310-codex-campaign-09-lane-04-acumen-flow-upgrade-and-end-to-end-smoke`  
**Surface**: `codex_parallel_session`  
**Role**: `direct_write`  
**Date**: `2026-03-10`  
**Objective**: upgrade the Acumen flow from sample compile to real operational sequence  
**Priority**: `high`  
**Target**: `poll -> triage -> queue -> Dawn Brief flow`  
**Origin lane**: `communications/prompts`  
**Expected response**: `communications/responses/RESPONSE-CODEX-CAMPAIGN-09-LANE-04-ACUMEN-FLOW-UPGRADE-AND-END-TO-END-SMOKE.md`

## Required Output

1. upgrade the Acumen flow so it can orchestrate the newly landed ingestion and triage surfaces
2. preserve strict identity checks and explicit failure/status reporting
3. produce one end-to-end smoke path using fixtures or runtime-safe sample data if live polling is unavailable
4. keep the flow deterministic where possible and explicit about what remains external
5. run `git diff --check`
6. report `complete / partial / blocked`
