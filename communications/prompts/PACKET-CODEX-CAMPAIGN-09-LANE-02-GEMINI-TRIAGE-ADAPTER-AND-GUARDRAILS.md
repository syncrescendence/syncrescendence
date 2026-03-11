# Dispatch Packet

**Packet ID**: `PKT-20260310-codex-campaign-09-lane-02-gemini-triage-adapter-and-guardrails`  
**Surface**: `codex_parallel_session`  
**Role**: `direct_write`  
**Date**: `2026-03-10`  
**Objective**: implement real Gemini triage invocation for Acumen with strict contracts and cost guardrails  
**Priority**: `extra_high`  
**Target**: `real triage execution`  
**Origin lane**: `communications/prompts`  
**Expected response**: `communications/responses/RESPONSE-CODEX-CAMPAIGN-09-LANE-02-GEMINI-TRIAGE-ADAPTER-AND-GUARDRAILS.md`

## Required Output

1. implement a Gemini Flash or Pro triage adapter that consumes Acumen triage packets and returns strict JSON decisions
2. keep API-key handling external to repo
3. add budget, retry, and malformed-response guardrails
4. preserve a clean separation between deterministic packet construction and model invocation
5. run `git diff --check`
6. report `complete / partial / blocked`
