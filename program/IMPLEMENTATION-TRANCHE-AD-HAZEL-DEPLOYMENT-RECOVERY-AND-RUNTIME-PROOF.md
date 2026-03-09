# Implementation Tranche AD — Hazel Deployment Recovery And Runtime Proof

**Tranche**: AD  
**Intent bindings**: `INT-SHELL-001`, `INT-SHELL-003`, `INT-SHELL-005`

## Purpose

Clear the live external blocker revealed by Wave 8.

This tranche is not a redesign wave.
It is a machine-local runtime recovery wave that should restore or verify the correct Hazel deployment for the outgoing cowork folder, prove that Hazel polling is alive again, and only then attempt one bounded post-cutover runtime proof.

## Tasks

1. reconcile the live Hazel deployed-folder set with the outgoing cowork folder and recover the missing deployment only if the exact target surface is confirmed
2. verify that Hazel polling resumes on the outgoing cowork folder and record evidence of that recovery
3. prepare one repo-valid synthetic proof candidate with current response and ledger targets
4. attempt one bounded post-recovery Hazel-triggered finalization
5. only if that runtime proof succeeds, apply the already prepared retirement patch from [ROOT-WRAPPER-RETIREMENT-PATCHSET-v1.md](/Users/system/syncrescendence/orchestration/state/ROOT-WRAPPER-RETIREMENT-PATCHSET-v1.md)
6. regenerate constitution and artifact-law reports only if step `5` lands

## Promotion / Completion Criteria

- [WAVE-8-RUNTIME-PROOF-AND-CONDITIONAL-WRAPPER-RETIREMENT-SYNTHESIS-v1.md](/Users/system/syncrescendence/orchestration/state/impl/WAVE-8-RUNTIME-PROOF-AND-CONDITIONAL-WRAPPER-RETIREMENT-SYNTHESIS-v1.md) exists as the binding synthesis for the failed proof attempt
- the Wave 9 swarm packets exist for deployment recovery, proof-candidate hygiene, and conditional proof/retirement
- wrapper deletion remains conditional on successful post-recovery runtime proof rather than on storage-level cutover alone

## Receipts

- [WAVE-8-RUNTIME-PROOF-AND-CONDITIONAL-WRAPPER-RETIREMENT-SYNTHESIS-v1.md](/Users/system/syncrescendence/orchestration/state/impl/WAVE-8-RUNTIME-PROOF-AND-CONDITIONAL-WRAPPER-RETIREMENT-SYNTHESIS-v1.md)
- [HAZEL-LIVE-CALLER-CUTOVER-RECEIPT-v1.md](/Users/system/syncrescendence/orchestration/state/HAZEL-LIVE-CALLER-CUTOVER-RECEIPT-v1.md)
- [WRAPPER-RETIREMENT-RESULT-v1.md](/Users/system/syncrescendence/orchestration/state/WRAPPER-RETIREMENT-RESULT-v1.md)
- [IMPLEMENTATION-BACKLOG.live.md](/Users/system/syncrescendence/program/IMPLEMENTATION-BACKLOG.live.md)
