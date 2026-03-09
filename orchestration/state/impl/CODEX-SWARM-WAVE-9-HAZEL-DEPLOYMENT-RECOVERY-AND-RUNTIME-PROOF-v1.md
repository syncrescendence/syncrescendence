# Codex Swarm — Wave 9 Hazel Deployment Recovery And Runtime Proof v1

**Date**: 2026-03-09  
**Status**: staged  
**Purpose**: recover the live Hazel deployment and polling surface for the outgoing cowork folder, prepare one repo-valid runtime-proof candidate, and conditionally retry runtime proof plus wrapper retirement

## 0. Why Wave 9 Exists

Wave 8 proved that wrapper retirement is blocked by live Hazel deployment and polling state, not by repo-path ambiguity or missing retirement patches.

Primary anchors:

- [WAVE-8-RUNTIME-PROOF-AND-CONDITIONAL-WRAPPER-RETIREMENT-SYNTHESIS-v1.md](/Users/system/syncrescendence/orchestration/state/impl/WAVE-8-RUNTIME-PROOF-AND-CONDITIONAL-WRAPPER-RETIREMENT-SYNTHESIS-v1.md)
- [HAZEL-LIVE-CALLER-CUTOVER-RECEIPT-v1.md](/Users/system/syncrescendence/orchestration/state/HAZEL-LIVE-CALLER-CUTOVER-RECEIPT-v1.md)
- [WRAPPER-RETIREMENT-RESULT-v1.md](/Users/system/syncrescendence/orchestration/state/WRAPPER-RETIREMENT-RESULT-v1.md)

## 1. Recommended Parallelism

Recommended:

- `2` core worker lanes
- `1` conditional execution lane
- `1` coordinator lane

## 2. Wave 9 Swarm Law

All sessions must obey:

1. do not delete the wrapper unless a successful post-recovery Hazel-triggered finalization is obtained in this wave
2. do not guess at Hazel folder IDs, deployment state, or trigger surfaces; prove them from live machine-local evidence
3. restore or verify Hazel deployment and polling before attempting runtime proof
4. keep rename work out of scope in this wave
5. run `git diff --check` before closing

## 3. Lane Set

### Lane 01 — Hazel Deployment And Polling Recovery

Goal:

- reconcile the live Hazel deployed-folder set with the outgoing cowork folder and, only if the target surface is proven exactly, recover or restore deployment and verify polling resumes

Recommended reasoning:

- `extra high`

Packet:

- [PACKET-CODEX-SWARM-WAVE-9-LANE-01-HAZEL-DEPLOYMENT-AND-POLLING-RECOVERY.md](/Users/system/syncrescendence/communications/prompts/PACKET-CODEX-SWARM-WAVE-9-LANE-01-HAZEL-DEPLOYMENT-AND-POLLING-RECOVERY.md)

### Lane 02 — Runtime Proof Candidate Hygiene

Goal:

- prepare one current repo-valid synthetic proof candidate and verify the expected response and ledger evidence surfaces without depending on Hazel execution

Recommended reasoning:

- `high`

Packet:

- [PACKET-CODEX-SWARM-WAVE-9-LANE-02-RUNTIME-PROOF-CANDIDATE-HYGIENE.md](/Users/system/syncrescendence/communications/prompts/PACKET-CODEX-SWARM-WAVE-9-LANE-02-RUNTIME-PROOF-CANDIDATE-HYGIENE.md)

### Lane 03 — Conditional Runtime Proof And Retirement

Goal:

- after Lane `01` and Lane `02` land, attempt one bounded post-recovery runtime proof and retire the wrapper only if success evidence is obtained

Recommended reasoning:

- `extra high`

Packet:

- [PACKET-CODEX-SWARM-WAVE-9-LANE-03-CONDITIONAL-RUNTIME-PROOF-AND-RETIREMENT.md](/Users/system/syncrescendence/communications/prompts/PACKET-CODEX-SWARM-WAVE-9-LANE-03-CONDITIONAL-RUNTIME-PROOF-AND-RETIREMENT.md)

### Lane 00 — Coordinator

Goal:

- adjudicate whether the wave cleared only recovery, or also cleared runtime proof and wrapper retirement

Recommended reasoning:

- `high`

Packet:

- [PACKET-CODEX-SWARM-WAVE-9-LANE-00-COORDINATOR.md](/Users/system/syncrescendence/communications/prompts/PACKET-CODEX-SWARM-WAVE-9-LANE-00-COORDINATOR.md)

## 4. Launch Order

Recommended launch order:

1. Lane 01
2. Lane 02
3. Lane 03
4. Lane 00 last

## 5. Success Criteria

Wave 9 succeeds when:

- the outgoing cowork folder is confirmed as a live deployed Hazel surface again
- Hazel polling is shown to be alive on that surface
- one repo-valid proof candidate is prepared against current expected outputs
- one successful post-cutover Hazel-triggered finalization is obtained, or the exact remaining external blocker is narrowed further without unsafe repo edits
- the wrapper is retired only if that runtime proof exists
