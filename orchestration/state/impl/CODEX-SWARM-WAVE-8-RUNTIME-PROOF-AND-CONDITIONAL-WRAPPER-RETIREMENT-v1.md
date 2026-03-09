# Codex Swarm — Wave 8 Runtime Proof And Conditional Wrapper Retirement v1

**Date**: 2026-03-08  
**Status**: staged  
**Purpose**: obtain runtime proof for the cut-over Hazel path and, if that proof lands, retire the root wrapper and clear the related constitutional debt

## 0. Why Wave 8 Exists

Wave 7 completed Hazel storage cutover and prepared the repo-side retirement patch.

The only remaining gate is runtime proof.

Primary anchors:

- [WAVE-7-HAZEL-CUTOVER-AND-RETIREMENT-PREP-SYNTHESIS-v1.md](/Users/system/syncrescendence/orchestration/state/impl/WAVE-7-HAZEL-CUTOVER-AND-RETIREMENT-PREP-SYNTHESIS-v1.md)
- [HAZEL-LIVE-CALLER-CUTOVER-RECEIPT-v1.md](/Users/system/syncrescendence/orchestration/state/HAZEL-LIVE-CALLER-CUTOVER-RECEIPT-v1.md)
- [ROOT-WRAPPER-RETIREMENT-PATCHSET-v1.md](/Users/system/syncrescendence/orchestration/state/ROOT-WRAPPER-RETIREMENT-PATCHSET-v1.md)

## 1. Recommended Parallelism

Recommended:

- `1` core worker lane
- `1` optional side lane
- `1` coordinator lane

## 2. Wave 8 Swarm Law

All sessions must obey:

1. do not delete the wrapper unless runtime success evidence is obtained in this wave
2. keep naming work non-blocking and secondary
3. if runtime proof fails or remains absent, leave the wrapper untouched and report the exact blocker
4. run `git diff --check` before closing

## 3. Lane Set

### Lane 01 — Runtime Proof And Conditional Retirement

Goal:

- obtain one successful post-cutover Hazel-triggered finalization and, if that proof lands, apply the prepared wrapper-retirement patch and refresh the affected reports

Recommended reasoning:

- `extra high`

Packet:

- [PACKET-CODEX-SWARM-WAVE-8-LANE-01-RUNTIME-PROOF-AND-CONDITIONAL-RETIREMENT.md](/Users/system/syncrescendence/communications/prompts/PACKET-CODEX-SWARM-WAVE-8-LANE-01-RUNTIME-PROOF-AND-CONDITIONAL-RETIREMENT.md)

### Optional Lane 02 — Rename Tranche Preflight

Goal:

- preflight the later rename tranche for the `4` remaining rename-required prompt artifacts without executing it

Recommended reasoning:

- `medium`

Packet:

- [PACKET-CODEX-SWARM-WAVE-8-LANE-02-RENAME-TRANCHE-PREFLIGHT.md](/Users/system/syncrescendence/communications/prompts/PACKET-CODEX-SWARM-WAVE-8-LANE-02-RENAME-TRANCHE-PREFLIGHT.md)

### Lane 00 — Coordinator

Goal:

- synthesize the runtime proof result and decide whether wrapper retirement is complete or still blocked

Recommended reasoning:

- `high`

Packet:

- [PACKET-CODEX-SWARM-WAVE-8-LANE-00-COORDINATOR.md](/Users/system/syncrescendence/communications/prompts/PACKET-CODEX-SWARM-WAVE-8-LANE-00-COORDINATOR.md)

## 4. Launch Order

Recommended launch order:

1. Lane 01
2. optional Lane 02
3. Lane 00 last

## 5. Success Criteria

Wave 8 succeeds when:

- one successful post-cutover Hazel-triggered finalization is evidenced
- the wrapper is deleted only if that proof exists
- constitution and artifact-law signals clear if retirement lands
- naming rename work remains optional and non-blocking
