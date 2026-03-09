# Dispatch Packet

**Packet ID**: `PKT-20260308-codex-swarm-wave-8-lane-01-runtime-proof-and-conditional-retirement`  
**Surface**: `codex_parallel_session`  
**Role**: `direct_write`  
**Date**: `2026-03-08`  
**Objective**: obtain one successful post-cutover Hazel-triggered finalization and, if that proof lands, apply the prepared wrapper-retirement patch and refresh the affected reports  
**Priority**: `highest`  
**Target**: `the last live gate to wrapper retirement`  
**Origin lane**: `communications/prompts`  
**Expected response**: `communications/responses/RESPONSE-CODEX-SWARM-WAVE-8-LANE-01-RUNTIME-PROOF-AND-CONDITIONAL-RETIREMENT.md`

## Decision Envelope

- **Trigger**: Wave 7 proved Hazel storage cutover and prepared the exact repo-side retirement patch
- **Selected approach**: try to obtain one real post-cutover Hazel-triggered success and only then apply the prepared repo-side retirement patch
- **Alternatives considered**:
  - deleting the wrapper immediately after storage cutover — rejected because runtime proof is still missing
  - waiting indefinitely for organic runtime proof — rejected because the shell now has enough evidence to attempt a bounded verification wave
- **Assumptions**:
  - the watched Hazel surface or triggering condition can be identified from the live Hazel artifacts
- **Inherited constraints**:
  - if runtime proof is not obtained, do not delete the wrapper
  - if the trigger mechanism cannot be exercised safely, leave repo state untouched and report the exact blocker
  - keep any non-proof naming work out of scope

## Assigned Live Files

- [16777231-58660320.hazelrules](/Users/system/Library/Application%20Support/Hazel/16777231-58660320.hazelrules)
- [16777231-58660320.hazellocalrulesdb](/Users/system/Library/Application%20Support/Hazel/16777231-58660320.hazellocalrulesdb)
- [16777231-58660320.hazeldb](/Users/system/Library/Application%20Support/Hazel/16777231-58660320.hazeldb)
- [com.noodlesoft.Hazel.plist](/Users/system/Library/Preferences/com.noodlesoft.Hazel.plist)
- [finalize_cowork_relay_job.py](/Users/system/syncrescendence/finalize_cowork_relay_job.py)
- [validate_constitution.py](/Users/system/syncrescendence/operators/validators/validate_constitution.py)
- [artifact_law_inventory.py](/Users/system/syncrescendence/operators/validators/artifact_law_inventory.py)
- [CONSTITUTION-VALIDATION-REPORT.json](/Users/system/syncrescendence/orchestration/state/CONSTITUTION-VALIDATION-REPORT.json)
- [CONSTITUTION-VALIDATION-REPORT.md](/Users/system/syncrescendence/orchestration/state/CONSTITUTION-VALIDATION-REPORT.md)
- [WRAPPER-RETIREMENT-RESULT-v1.md](/Users/system/syncrescendence/orchestration/state/WRAPPER-RETIREMENT-RESULT-v1.md)

## Anchors

- [HAZEL-LIVE-CALLER-CUTOVER-RECEIPT-v1.md](/Users/system/syncrescendence/orchestration/state/HAZEL-LIVE-CALLER-CUTOVER-RECEIPT-v1.md)
- [ROOT-WRAPPER-RETIREMENT-PATCHSET-v1.md](/Users/system/syncrescendence/orchestration/state/ROOT-WRAPPER-RETIREMENT-PATCHSET-v1.md)
- [WAVE-7-HAZEL-CUTOVER-AND-RETIREMENT-PREP-SYNTHESIS-v1.md](/Users/system/syncrescendence/orchestration/state/impl/WAVE-7-HAZEL-CUTOVER-AND-RETIREMENT-PREP-SYNTHESIS-v1.md)

## Required Output

1. identify a safe way to obtain one post-cutover Hazel-triggered finalization, using live Hazel evidence rather than guesswork
2. if successful, record the proof clearly in the receipt artifact
3. only if that success proof exists, apply the prepared retirement patch set:
   - delete [finalize_cowork_relay_job.py](/Users/system/syncrescendence/finalize_cowork_relay_job.py)
   - remove the transitional entry in [validate_constitution.py](/Users/system/syncrescendence/operators/validators/validate_constitution.py)
   - remove the transitional root-operator entry in [artifact_law_inventory.py](/Users/system/syncrescendence/operators/validators/artifact_law_inventory.py)
   - regenerate constitution and artifact-law outputs as applicable
4. if proof is absent, leave those repo edits unapplied and report the exact blocker
5. write a short response artifact summarizing whether the wrapper remains blocked or has been retired
6. run `git diff --check`
7. report `complete / partial / blocked`
