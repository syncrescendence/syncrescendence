# Communications Naming Rename Preflight v1

**Date**: `2026-03-08`  
**Status**: `planning only`  
**Scope**: later coordinated rename tranche for the remaining `4` prompt-lane filename mismatches  
**Source debt map**: [COMMUNICATIONS-NAMING-REMAINING-DEBT-v1.md](/Users/system/syncrescendence/orchestration/state/COMMUNICATIONS-NAMING-REMAINING-DEBT-v1.md)

## 1. Objective

Prepare the later rename tranche precisely without renaming files in this wave.

This artifact maps:

- the `4` rename-required prompt artifacts
- the likely target filenames
- the repo reference-update surfaces that should move in the same change set
- bundling guidance for the eventual coordinated tranche

## 2. Proposed Later Rename Sequence

The prompts lane is now predominantly `PACKET-*` / `PROMPT-*`.

The remaining `DISPATCH-*` prompt artifacts are the outliers and should be renamed to `PACKET-*` in the later tranche:

1. `communications/prompts/DISPATCH-AJNA-cc79-openclaw-command-verification.md`
   -> `communications/prompts/PACKET-AJNA-cc79-openclaw-command-verification.md`
2. `communications/prompts/DISPATCH-MANUS-cc79-harness-command-verification.md`
   -> `communications/prompts/PACKET-MANUS-cc79-harness-command-verification.md`
3. `communications/prompts/DISPATCH-AJNA-cc91-connector-verification-tranche-01.md`
   -> `communications/prompts/PACKET-AJNA-cc91-connector-verification-tranche-01.md`
4. `communications/prompts/DISPATCH-PSYCHE-cc81-node-pairing-and-runtime-audit.md`
   -> `communications/prompts/PACKET-PSYCHE-cc81-node-pairing-and-runtime-audit.md`

Rationale:

- sibling prompt artifacts already use `PACKET-*`
- the two Ajna and Manus files declare `**Packet type**: `verification_dispatch``, which supports `PACKET-*` as the filename surface
- the Psyche artifact is also a prompt-lane work packet rather than a durable log or response artifact

## 3. Reference-Update Surfaces

### A. `DISPATCH-AJNA-cc79-openclaw-command-verification.md`

Likely same-change reference updates:

- [CC79-HARNESS-EXTERNAL-VERIFICATION-QUEUE.md](/Users/system/syncrescendence/orchestration/state/impl/CC79-HARNESS-EXTERNAL-VERIFICATION-QUEUE.md)
- [COMMUNICATIONS-NAMING-REPORT.md](/Users/system/syncrescendence/orchestration/state/COMMUNICATIONS-NAMING-REPORT.md)
- [COMMUNICATIONS-NAMING-REPORT.json](/Users/system/syncrescendence/orchestration/state/COMMUNICATIONS-NAMING-REPORT.json)
- [COMMUNICATIONS-NAMING-TRIAGE-v1.md](/Users/system/syncrescendence/orchestration/state/COMMUNICATIONS-NAMING-TRIAGE-v1.md)
- [COMMUNICATIONS-NAMING-REMAINING-DEBT-v1.md](/Users/system/syncrescendence/orchestration/state/COMMUNICATIONS-NAMING-REMAINING-DEBT-v1.md)
- historical response artifacts that enumerate the remaining debt:
  - [RESPONSE-CODEX-SWARM-WAVE-5-LANE-03-COMMUNICATIONS-NAMING-DEBT-CLASSIFICATION.md](/Users/system/syncrescendence/communications/responses/RESPONSE-CODEX-SWARM-WAVE-5-LANE-03-COMMUNICATIONS-NAMING-DEBT-CLASSIFICATION.md)
  - [RESPONSE-CODEX-SWARM-WAVE-7-LANE-03-REMAINING-NAMING-DEBT-MAP.md](/Users/system/syncrescendence/communications/responses/RESPONSE-CODEX-SWARM-WAVE-7-LANE-03-REMAINING-NAMING-DEBT-MAP.md)

### B. `DISPATCH-MANUS-cc79-harness-command-verification.md`

Likely same-change reference updates:

- [CC79-HARNESS-EXTERNAL-VERIFICATION-QUEUE.md](/Users/system/syncrescendence/orchestration/state/impl/CC79-HARNESS-EXTERNAL-VERIFICATION-QUEUE.md)
- [COMMUNICATIONS-NAMING-REPORT.md](/Users/system/syncrescendence/orchestration/state/COMMUNICATIONS-NAMING-REPORT.md)
- [COMMUNICATIONS-NAMING-REPORT.json](/Users/system/syncrescendence/orchestration/state/COMMUNICATIONS-NAMING-REPORT.json)
- [COMMUNICATIONS-NAMING-TRIAGE-v1.md](/Users/system/syncrescendence/orchestration/state/COMMUNICATIONS-NAMING-TRIAGE-v1.md)
- [COMMUNICATIONS-NAMING-REMAINING-DEBT-v1.md](/Users/system/syncrescendence/orchestration/state/COMMUNICATIONS-NAMING-REMAINING-DEBT-v1.md)
- historical response artifacts that enumerate the remaining debt:
  - [RESPONSE-CODEX-SWARM-WAVE-5-LANE-03-COMMUNICATIONS-NAMING-DEBT-CLASSIFICATION.md](/Users/system/syncrescendence/communications/responses/RESPONSE-CODEX-SWARM-WAVE-5-LANE-03-COMMUNICATIONS-NAMING-DEBT-CLASSIFICATION.md)
  - [RESPONSE-CODEX-SWARM-WAVE-7-LANE-03-REMAINING-NAMING-DEBT-MAP.md](/Users/system/syncrescendence/communications/responses/RESPONSE-CODEX-SWARM-WAVE-7-LANE-03-REMAINING-NAMING-DEBT-MAP.md)

### C. `DISPATCH-AJNA-cc91-connector-verification-tranche-01.md`

Likely same-change reference updates:

- [LOG-CC91-connector-verification-pipeline.md](/Users/system/syncrescendence/communications/logs/LOG-CC91-connector-verification-pipeline.md)
- [CC91-CONNECTOR-VERIFICATION-QUEUE.md](/Users/system/syncrescendence/orchestration/state/impl/CC91-CONNECTOR-VERIFICATION-QUEUE.md)
- [COMMUNICATIONS-NAMING-REPORT.md](/Users/system/syncrescendence/orchestration/state/COMMUNICATIONS-NAMING-REPORT.md)
- [COMMUNICATIONS-NAMING-REPORT.json](/Users/system/syncrescendence/orchestration/state/COMMUNICATIONS-NAMING-REPORT.json)
- [COMMUNICATIONS-NAMING-TRIAGE-v1.md](/Users/system/syncrescendence/orchestration/state/COMMUNICATIONS-NAMING-TRIAGE-v1.md)
- [COMMUNICATIONS-NAMING-REMAINING-DEBT-v1.md](/Users/system/syncrescendence/orchestration/state/COMMUNICATIONS-NAMING-REMAINING-DEBT-v1.md)
- historical response artifacts that enumerate the remaining debt:
  - [RESPONSE-CODEX-SWARM-WAVE-5-LANE-03-COMMUNICATIONS-NAMING-DEBT-CLASSIFICATION.md](/Users/system/syncrescendence/communications/responses/RESPONSE-CODEX-SWARM-WAVE-5-LANE-03-COMMUNICATIONS-NAMING-DEBT-CLASSIFICATION.md)
  - [RESPONSE-CODEX-SWARM-WAVE-7-LANE-03-REMAINING-NAMING-DEBT-MAP.md](/Users/system/syncrescendence/communications/responses/RESPONSE-CODEX-SWARM-WAVE-7-LANE-03-REMAINING-NAMING-DEBT-MAP.md)

### D. `DISPATCH-PSYCHE-cc81-node-pairing-and-runtime-audit.md`

Likely same-change reference updates:

- [LOG-CC81-identity-cutover-dispatch.md](/Users/system/syncrescendence/communications/logs/LOG-CC81-identity-cutover-dispatch.md)
- [CC81-IDENTITY-CUTOVER-RUNBOOK-v1.md](/Users/system/syncrescendence/orchestration/state/impl/CC81-IDENTITY-CUTOVER-RUNBOOK-v1.md)
- [COMMUNICATIONS-NAMING-REPORT.md](/Users/system/syncrescendence/orchestration/state/COMMUNICATIONS-NAMING-REPORT.md)
- [COMMUNICATIONS-NAMING-REPORT.json](/Users/system/syncrescendence/orchestration/state/COMMUNICATIONS-NAMING-REPORT.json)
- [COMMUNICATIONS-NAMING-TRIAGE-v1.md](/Users/system/syncrescendence/orchestration/state/COMMUNICATIONS-NAMING-TRIAGE-v1.md)
- [COMMUNICATIONS-NAMING-REMAINING-DEBT-v1.md](/Users/system/syncrescendence/orchestration/state/COMMUNICATIONS-NAMING-REMAINING-DEBT-v1.md)
- historical response artifacts that enumerate the remaining debt:
  - [RESPONSE-CODEX-SWARM-WAVE-5-LANE-03-COMMUNICATIONS-NAMING-DEBT-CLASSIFICATION.md](/Users/system/syncrescendence/communications/responses/RESPONSE-CODEX-SWARM-WAVE-5-LANE-03-COMMUNICATIONS-NAMING-DEBT-CLASSIFICATION.md)
  - [RESPONSE-CODEX-SWARM-WAVE-7-LANE-03-REMAINING-NAMING-DEBT-MAP.md](/Users/system/syncrescendence/communications/responses/RESPONSE-CODEX-SWARM-WAVE-7-LANE-03-REMAINING-NAMING-DEBT-MAP.md)

## 4. Bundling Guidance

### Bundle 1: CC79 paired verification prompts

Rename together:

- `DISPATCH-AJNA-cc79-openclaw-command-verification.md`
- `DISPATCH-MANUS-cc79-harness-command-verification.md`

Reason:

- both are referenced by the same CC79 implementation queue
- both are part of the same command-verification lineage
- splitting them would force two edits against the same queue and naming-report surfaces

### Bundle 2: CC81 and CC91 operational prompts

Rename together:

- `DISPATCH-AJNA-cc91-connector-verification-tranche-01.md`
- `DISPATCH-PSYCHE-cc81-node-pairing-and-runtime-audit.md`

Reason:

- both have dedicated operational logs and implementation runbooks/queues
- both sit in the same remaining rename tranche and hit the same naming-report surfaces

### Tranche recommendation

If operationally simple, the cleanest execution remains one coordinated tranche containing all `4` renames plus all reference updates.

If partial sequencing is unavoidable later, the CC79 pair should stay atomic.

## 5. Execution Boundary

This preflight does not:

- rename files
- edit validator logic
- rewrite historical narrative beyond identifying likely update surfaces

The later tranche should perform:

1. filesystem rename of the `4` prompt artifacts
2. same-change reference replacement across the surfaces above
3. report regeneration to confirm the active rename-required bucket is cleared

## 6. Preflight Result

- rename-required artifacts mapped: `4`
- likely target filenames proposed: `4`
- reference-update surfaces identified: `yes`
- bundled execution guidance provided: `yes`
- execution performed in this wave: `none`
- status: `complete`
