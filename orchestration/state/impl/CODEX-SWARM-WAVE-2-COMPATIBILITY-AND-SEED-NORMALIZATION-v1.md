# Codex Swarm — Wave 2 Compatibility And Seed Normalization v1

**Date**: 2026-03-06  
**Status**: staged  
**Purpose**: follow the Wave 1 control-plane ratification with the smallest next wave that cleans up compatibility drift and normalizes the first migration seed set

## 0. Why Wave 2 Exists

Wave 1 ratified the control plane and landed the minimal law files.

The next safe move is not broad migration.

It is to:

- normalize live-facing docs that still speak the old lane vocabulary
- make the first migration seed set schema-valid
- prepare the first manifests and receipts under the new custody law
- bound the first Sigma subtree sync without executing it recklessly
- normalize the optional validator layer to the ratified schema

Primary anchors:

- [SYNCRESCENDENCE-HOLISTIC-STRATEGIC-ENDEAVOR-v1.md](/Users/system/syncrescendence/knowledge/canon/SYNCRESCENDENCE-HOLISTIC-STRATEGIC-ENDEAVOR-v1.md)
- [TRIBUTARY-RATIFICATION-WRITESET-SYNTHESIS-v1.md](/Users/system/syncrescendence/orchestration/state/impl/TRIBUTARY-RATIFICATION-WRITESET-SYNTHESIS-v1.md)

## 1. Recommended Parallelism

Recommended:

- `6` core worker lanes
- `1` optional drift-scan lane
- `1` coordinator lane

## 2. Wave 2 Swarm Law

All sessions must obey:

1. write only to the assigned response file
2. do not edit live repo files directly
3. return patch-ready drafts, normalized rows, or bounded tranche specs
4. do not reopen Sigma, custody, witness, or dispatch adjudications unless a direct repo contradiction exists
5. use repo-relative paths
6. use the ratified registry schema vocabulary exactly where relevant
7. include clear failure modes and reasoning discipline

## 3. Lane Set

### Lane 01 — Knowledge Compatibility Cleanup

Goal:

- identify and draft the minimal live-facing doc updates required so the repo stops treating bare `knowledge/references/` as the sovereign secondary lane

Recommended reasoning:

- `high`

Packet:

- [PACKET-CODEX-SWARM-WAVE-2-LANE-01-KNOWLEDGE-COMPATIBILITY.md](/Users/system/syncrescendence/communications/prompts/PACKET-CODEX-SWARM-WAVE-2-LANE-01-KNOWLEDGE-COMPATIBILITY.md)

### Lane 02 — Communications And Dispatch Cleanup

Goal:

- identify and draft the minimal communications-lane documentation updates required after `communications/dispatches/` physicalization

Recommended reasoning:

- `medium`

Packet:

- [PACKET-CODEX-SWARM-WAVE-2-LANE-02-COMMS-DISPATCH-CLEANUP.md](/Users/system/syncrescendence/communications/prompts/PACKET-CODEX-SWARM-WAVE-2-LANE-02-COMMS-DISPATCH-CLEANUP.md)

### Lane 03 — Registry Seed Normalization

Goal:

- convert the first migration seed set into schema-valid candidate rows using `tdc-*` ids, repo-relative paths, and ratified `chosen_disposition` values

Recommended reasoning:

- `extra high`

Packet:

- [PACKET-CODEX-SWARM-WAVE-2-LANE-03-REGISTRY-SEED-NORMALIZATION.md](/Users/system/syncrescendence/communications/prompts/PACKET-CODEX-SWARM-WAVE-2-LANE-03-REGISTRY-SEED-NORMALIZATION.md)

### Lane 04 — First Custody Artifacts

Goal:

- draft the first manifest and rehousing-receipt artifacts aligned to the new pedigree law and the normalized seed set

Recommended reasoning:

- `high`

Packet:

- [PACKET-CODEX-SWARM-WAVE-2-LANE-04-FIRST-CUSTODY-ARTIFACTS.md](/Users/system/syncrescendence/communications/prompts/PACKET-CODEX-SWARM-WAVE-2-LANE-04-FIRST-CUSTODY-ARTIFACTS.md)

### Lane 05 — Sigma Subtree Sync Tranche

Goal:

- draft a bounded, compatibility-safe tranche for the first `knowledge/references/*` to `knowledge/sigma/references/*` subtree sync

Recommended reasoning:

- `high`

Packet:

- [PACKET-CODEX-SWARM-WAVE-2-LANE-05-SIGMA-SUBTREE-SYNC.md](/Users/system/syncrescendence/communications/prompts/PACKET-CODEX-SWARM-WAVE-2-LANE-05-SIGMA-SUBTREE-SYNC.md)

### Lane 06 — Validator Normalization

Goal:

- normalize the optional validator/template pack to the ratified schema and decide what should be enforced immediately versus deferred

Recommended reasoning:

- `medium`

Packet:

- [PACKET-CODEX-SWARM-WAVE-2-LANE-06-VALIDATOR-NORMALIZATION.md](/Users/system/syncrescendence/communications/prompts/PACKET-CODEX-SWARM-WAVE-2-LANE-06-VALIDATOR-NORMALIZATION.md)

### Optional Lane 07 — Macro And Nomenclature Drift Scan

Goal:

- identify which top-level and live-facing docs still lack the macro anchor or still speak in now-superseded lane terms

Recommended reasoning:

- `medium`

Packet:

- [PACKET-CODEX-SWARM-WAVE-2-LANE-07-MACRO-DRIFT-SCAN.md](/Users/system/syncrescendence/communications/prompts/PACKET-CODEX-SWARM-WAVE-2-LANE-07-MACRO-DRIFT-SCAN.md)

### Lane 00 — Coordinator

Goal:

- synthesize Wave 2 outputs into the smallest safe direct-write pass after Wave 1

Recommended reasoning:

- `high`

Packet:

- [PACKET-CODEX-SWARM-WAVE-2-LANE-00-COORDINATOR.md](/Users/system/syncrescendence/communications/prompts/PACKET-CODEX-SWARM-WAVE-2-LANE-00-COORDINATOR.md)

## 4. Launch Order

Recommended launch order:

1. Lane 01
2. Lane 02
3. Lane 03
4. Lane 04
5. Lane 05
6. Lane 06
7. optional Lane 07
8. Lane 00 last

## 5. Success Criteria

Wave 2 succeeds when:

- the first registry population is normalized to the schema
- the first custody artifacts are draftable without vocabulary drift
- the first Sigma subtree sync is bounded and receipt-ready
- top-level documentation drift around Sigma and dispatches is identified and drafted
- the next direct-write pass can proceed without reopening contract law
