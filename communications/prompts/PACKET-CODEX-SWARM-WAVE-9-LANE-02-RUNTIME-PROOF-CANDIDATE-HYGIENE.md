# Dispatch Packet

**Packet ID**: `PKT-20260309-codex-swarm-wave-9-lane-02-runtime-proof-candidate-hygiene`  
**Surface**: `codex_parallel_session`  
**Role**: `direct_write`  
**Date**: `2026-03-09`  
**Objective**: prepare one current repo-valid synthetic runtime-proof candidate and verify the expected response and ledger evidence surfaces without depending on Hazel execution  
**Priority**: `high`  
**Target**: `proof-candidate hygiene before any new Hazel-triggered attempt`  
**Origin lane**: `communications/prompts`  
**Expected response**: `communications/responses/RESPONSE-CODEX-SWARM-WAVE-9-LANE-02-RUNTIME-PROOF-CANDIDATE-HYGIENE.md`

## Decision Envelope

- **Trigger**: Wave 8 showed that older smoke files were not trustworthy proof candidates because they referenced dead paths and stale packet targets
- **Selected approach**: prepare one clean synthetic candidate against current repo-valid paths and document the exact expected evidence surfaces before runtime is retried
- **Alternatives considered**:
  - reusing historical smoke artifacts — rejected because their path assumptions are already known to be stale
  - bundling this silently into the runtime-proof lane — rejected because separating proof-candidate hygiene from Hazel recovery makes the next runtime attempt easier to judge
- **Assumptions**:
  - the operator-path finalizer and current communications surfaces expose enough structure to define one valid synthetic proof candidate
- **Inherited constraints**:
  - do not claim runtime success in this lane
  - do not delete the wrapper in this lane
  - keep changes bounded to proof-candidate artifacts and documentation

## Assigned Live Files

- [operators/cli-web-gap/finalize_cowork_relay_job.py](/Users/system/syncrescendence/operators/cli-web-gap/finalize_cowork_relay_job.py)
- [orchestration/relay/cowork-v1/artifacts/outgoing](/Users/system/syncrescendence/orchestration/relay/cowork-v1/artifacts/outgoing)
- [orchestration/relay/cowork-v1/jobs/inbox](/Users/system/syncrescendence/orchestration/relay/cowork-v1/jobs/inbox)
- [communications/responses](/Users/system/syncrescendence/communications/responses)
- [HAZEL-LIVE-CALLER-CUTOVER-RECEIPT-v1.md](/Users/system/syncrescendence/orchestration/state/HAZEL-LIVE-CALLER-CUTOVER-RECEIPT-v1.md)
- [WRAPPER-RETIREMENT-RESULT-v1.md](/Users/system/syncrescendence/orchestration/state/WRAPPER-RETIREMENT-RESULT-v1.md)

## Anchors

- [WAVE-8-RUNTIME-PROOF-AND-CONDITIONAL-WRAPPER-RETIREMENT-SYNTHESIS-v1.md](/Users/system/syncrescendence/orchestration/state/impl/WAVE-8-RUNTIME-PROOF-AND-CONDITIONAL-WRAPPER-RETIREMENT-SYNTHESIS-v1.md)
- [PACKET-CODEX-SWARM-WAVE-8-LANE-01-RUNTIME-PROOF-AND-CONDITIONAL-RETIREMENT.md](/Users/system/syncrescendence/communications/prompts/PACKET-CODEX-SWARM-WAVE-8-LANE-01-RUNTIME-PROOF-AND-CONDITIONAL-RETIREMENT.md)

## Required Output

1. identify one current repo-valid synthetic job plus `.status.json` proof candidate for the outgoing cowork flow
2. verify that all referenced packet, response, and ledger targets exist or can be safely staged under current shell law
3. write one repo-native artifact documenting the exact candidate shape and expected evidence surfaces
4. write a short response artifact summarizing whether the proof candidate is now clean and ready
5. run `git diff --check`
6. report `complete / partial / blocked`
