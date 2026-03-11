# Dispatch Packet

**Packet ID**: `PKT-20260310-codex-campaign-09-lane-03-triage-decision-ledger-and-training-corpus`  
**Surface**: `codex_parallel_session`  
**Role**: `direct_write`  
**Date**: `2026-03-10`  
**Objective**: create durable decision evidence for Acumen triage and model-call logging  
**Priority**: `high`  
**Target**: `Acumen append-only decision evidence`  
**Origin lane**: `communications/prompts`  
**Expected response**: `communications/responses/RESPONSE-CODEX-CAMPAIGN-09-LANE-03-TRIAGE-DECISION-LEDGER-AND-TRAINING-CORPUS.md`

## Required Output

1. create append-only triage-decision and training-corpus surfaces if now justified
2. keep those surfaces derivative of the Acumen runtime path and repo law
3. ensure model-call evidence captures cost/failure metadata without leaking secrets or raw prompt internals beyond what policy permits
4. add validators or report surfaces as needed
5. run `git diff --check`
6. report `complete / partial / blocked`
