# Dispatch Packet

**Packet ID**: `PKT-20260309-codex-swarm-wave-9-lane-01-hazel-deployment-and-polling-recovery`  
**Surface**: `codex_parallel_session`  
**Role**: `direct_write`  
**Date**: `2026-03-09`  
**Objective**: reconcile the live Hazel deployment set with the outgoing cowork folder and recover or re-verify that deployment only if the target surface is proven exactly, then confirm polling resumes  
**Priority**: `highest`  
**Target**: `the machine-local Hazel deployment blocker`  
**Origin lane**: `communications/prompts`  
**Expected response**: `communications/responses/RESPONSE-CODEX-SWARM-WAVE-9-LANE-01-HAZEL-DEPLOYMENT-AND-POLLING-RECOVERY.md`

## Decision Envelope

- **Trigger**: Wave 8 showed that the outgoing-folder Hazel id `16777231-58660320` was no longer deployed and its poll time was frozen
- **Selected approach**: use live Hazel evidence to reconcile path, folder id, and deployment state before any new runtime-proof attempt
- **Alternatives considered**:
  - retrying runtime proof immediately against a stale deployment surface — rejected because Wave 8 already showed that path fails non-deterministically
  - deleting the wrapper despite missing runtime proof — rejected because the external runtime edge is not healthy enough
- **Assumptions**:
  - Hazel still exposes enough machine-local state to confirm the exact outgoing cowork folder surface and its deployment status
- **Inherited constraints**:
  - do not touch repo retirement files in this lane
  - do not guess at undeclared Hazel storage formats or folder identities
  - if safe deployment recovery cannot be proven, leave live files untouched and report the exact blocker

## Assigned Live Files

- [com.noodlesoft.Hazel.plist](/Users/system/Library/Preferences/com.noodlesoft.Hazel.plist)
- [16777231-58660320.hazelrules](/Users/system/Library/Application%20Support/Hazel/16777231-58660320.hazelrules)
- [16777231-58660320.hazellocalrulesdb](/Users/system/Library/Application%20Support/Hazel/16777231-58660320.hazellocalrulesdb)
- [16777231-58660320.hazeldb](/Users/system/Library/Application%20Support/Hazel/16777231-58660320.hazeldb)
- [HAZEL-LIVE-CALLER-CUTOVER-RECEIPT-v1.md](/Users/system/syncrescendence/orchestration/state/HAZEL-LIVE-CALLER-CUTOVER-RECEIPT-v1.md)
- [WRAPPER-RETIREMENT-RESULT-v1.md](/Users/system/syncrescendence/orchestration/state/WRAPPER-RETIREMENT-RESULT-v1.md)
- [orchestration/relay/cowork-v1/artifacts/outgoing](/Users/system/syncrescendence/orchestration/relay/cowork-v1/artifacts/outgoing)

## Anchors

- [WAVE-8-RUNTIME-PROOF-AND-CONDITIONAL-WRAPPER-RETIREMENT-SYNTHESIS-v1.md](/Users/system/syncrescendence/orchestration/state/impl/WAVE-8-RUNTIME-PROOF-AND-CONDITIONAL-WRAPPER-RETIREMENT-SYNTHESIS-v1.md)
- [ROOT-WRAPPER-EDGE-AUDIT-v1.md](/Users/system/syncrescendence/orchestration/state/ROOT-WRAPPER-EDGE-AUDIT-v1.md)
- [HAZEL-LIVE-CALLER-CUTOVER-RECEIPT-v1.md](/Users/system/syncrescendence/orchestration/state/HAZEL-LIVE-CALLER-CUTOVER-RECEIPT-v1.md)

## Required Output

1. prove the current outgoing cowork folder path and its corresponding Hazel deployment identity from live machine-local evidence
2. determine whether the outgoing folder is actually deployed and being polled
3. if the exact target surface is proven and a safe recovery is possible, recover or restore deployment for that surface
4. confirm whether polling resumes after the recovery step
5. write or update one repo-native receipt describing before/after deployment and polling state
6. write a short response artifact summarizing whether deployment recovery landed or blocked
7. run `git diff --check`
8. report `complete / partial / blocked`
