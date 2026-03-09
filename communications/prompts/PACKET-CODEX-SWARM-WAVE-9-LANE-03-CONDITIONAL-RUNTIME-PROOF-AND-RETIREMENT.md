# Dispatch Packet

**Packet ID**: `PKT-20260309-codex-swarm-wave-9-lane-03-conditional-runtime-proof-and-retirement`  
**Surface**: `codex_parallel_session`  
**Role**: `direct_write`  
**Date**: `2026-03-09`  
**Objective**: after deployment recovery and proof-candidate hygiene land, attempt one bounded post-recovery runtime proof and retire the wrapper only if success evidence is obtained  
**Priority**: `highest`  
**Target**: `conditional closure of the wrapper-retirement gate`  
**Origin lane**: `communications/prompts`  
**Expected response**: `communications/responses/RESPONSE-CODEX-SWARM-WAVE-9-LANE-03-CONDITIONAL-RUNTIME-PROOF-AND-RETIREMENT.md`

## Decision Envelope

- **Trigger**: Wave 8 proved that monolithic runtime proof was blocked by Hazel deployment state, not by repo ambiguity
- **Selected approach**: wait for Lane `01` and Lane `02`, then attempt one bounded runtime proof only if the live deployment/polling surface and proof candidate are both healthy
- **Alternatives considered**:
  - retrying runtime proof blindly — rejected because Wave 8 already narrowed the blocker further
  - deleting the wrapper based only on storage-level cutover — rejected because runtime success is still the deletion gate
- **Assumptions**:
  - if Hazel deployment and polling are restored, one bounded runtime-proof attempt is enough to judge whether retirement can proceed
- **Inherited constraints**:
  - read Lane `01` and Lane `02` outputs before attempting runtime proof
  - if either lane remains blocked on the critical path, leave repo retirement surfaces untouched
  - only after successful runtime proof may this lane apply the prepared retirement patch and regenerate affected reports

## Assigned Live Files

- [finalize_cowork_relay_job.py](/Users/system/syncrescendence/finalize_cowork_relay_job.py)
- [operators/cli-web-gap/finalize_cowork_relay_job.py](/Users/system/syncrescendence/operators/cli-web-gap/finalize_cowork_relay_job.py)
- [validate_constitution.py](/Users/system/syncrescendence/operators/validators/validate_constitution.py)
- [artifact_law_inventory.py](/Users/system/syncrescendence/operators/validators/artifact_law_inventory.py)
- [CONSTITUTION-VALIDATION-REPORT.json](/Users/system/syncrescendence/orchestration/state/CONSTITUTION-VALIDATION-REPORT.json)
- [CONSTITUTION-VALIDATION-REPORT.md](/Users/system/syncrescendence/orchestration/state/CONSTITUTION-VALIDATION-REPORT.md)
- [WRAPPER-RETIREMENT-RESULT-v1.md](/Users/system/syncrescendence/orchestration/state/WRAPPER-RETIREMENT-RESULT-v1.md)

## Anchors

- [WAVE-8-RUNTIME-PROOF-AND-CONDITIONAL-WRAPPER-RETIREMENT-SYNTHESIS-v1.md](/Users/system/syncrescendence/orchestration/state/impl/WAVE-8-RUNTIME-PROOF-AND-CONDITIONAL-WRAPPER-RETIREMENT-SYNTHESIS-v1.md)
- [ROOT-WRAPPER-RETIREMENT-PATCHSET-v1.md](/Users/system/syncrescendence/orchestration/state/ROOT-WRAPPER-RETIREMENT-PATCHSET-v1.md)
- [PACKET-CODEX-SWARM-WAVE-9-LANE-01-HAZEL-DEPLOYMENT-AND-POLLING-RECOVERY.md](/Users/system/syncrescendence/communications/prompts/PACKET-CODEX-SWARM-WAVE-9-LANE-01-HAZEL-DEPLOYMENT-AND-POLLING-RECOVERY.md)
- [PACKET-CODEX-SWARM-WAVE-9-LANE-02-RUNTIME-PROOF-CANDIDATE-HYGIENE.md](/Users/system/syncrescendence/communications/prompts/PACKET-CODEX-SWARM-WAVE-9-LANE-02-RUNTIME-PROOF-CANDIDATE-HYGIENE.md)

## Required Output

1. read the landed outputs from Lane `01` and Lane `02`
2. if the outgoing-folder deployment/polling surface is healthy and the proof candidate is clean, attempt one bounded runtime proof
3. only if that proof succeeds, apply the prepared wrapper-retirement patch:
   - delete [finalize_cowork_relay_job.py](/Users/system/syncrescendence/finalize_cowork_relay_job.py)
   - remove the transitional entry in [validate_constitution.py](/Users/system/syncrescendence/operators/validators/validate_constitution.py)
   - remove the transitional root-operator entry in [artifact_law_inventory.py](/Users/system/syncrescendence/operators/validators/artifact_law_inventory.py)
   - regenerate constitution and artifact-law outputs as applicable
4. if proof is absent, leave those repo edits unapplied and report the exact remaining blocker
5. write a short response artifact summarizing whether the wrapper remains blocked or has been retired
6. run `git diff --check`
7. report `complete / partial / blocked`
