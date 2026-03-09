# Dispatch Packet

**Packet ID**: `PKT-20260309-codex-campaign-01-lane-01-continuous-edge-consolidation`  
**Surface**: `codex_parallel_session`  
**Role**: `continuous_loop`  
**Date**: `2026-03-09`  
**Objective**: own the post-wrapper edge until stale blocker guidance, stale runtime debris, and immediate Hazel/cowork edge instability are closed or explicitly handed off  
**Priority**: `highest`  
**Target**: `the tightly coupled post-wrapper runtime frontier`  
**Origin lane**: `communications/prompts`  
**Expected response**: `communications/responses/RESPONSE-CODEX-CAMPAIGN-01-LANE-01-CONTINUOUS-EDGE-CONSOLIDATION.md`

## Decision Envelope

- **Trigger**: the wrapper blocker is resolved, so edge-local work should now be closed by one agent rather than re-sliced into many micro packets
- **Selected approach**: keep one agent in a loop over edge-local cleanup, stale artifact retirement, active guidance correction, and stability checks until the edge is quiet enough to stop active babysitting
- **Inherited constraints**:
  - do not reopen broad tributary or doctrine work here
  - keep this lane on tightly coupled runtime, validators, active edge guidance, and stale edge debt only
  - record concrete closures and remaining edge-local debt in the same response artifact over time

## Required Output

1. clean or retire stale post-wrapper edge artifacts and guidance that still present the wrapper as active
2. verify Hazel/cowork stability after the repair and runtime proof
3. codify any reusable edge-repair lessons that should survive as validated pattern or playbook updates
4. keep one continuously updated response artifact rather than many tiny closures
5. run `git diff --check`
6. report `active / complete / blocked`
