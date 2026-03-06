# Dispatch Packet

**Packet ID**: `PKT-20260306-codex-swarm-wave-2-lane-07-macro-drift-scan`  
**Surface**: `codex_parallel_session`  
**Role**: `analysis`  
**Date**: `2026-03-06`  
**Objective**: identify live-facing docs that still lack the macro anchor or still speak in now-superseded lane terms  
**Origin lane**: `communications/prompts`  
**Expected response**: `communications/responses/RESPONSE-CODEX-SWARM-WAVE-2-LANE-07-MACRO-DRIFT-SCAN.md`

## Decision Envelope

- **Trigger**: the macro doctrine now exists, but many live-facing docs predate it or the Sigma/dispatch ratification
- **Selected approach**: identify only the highest-yield drift surfaces, not every possible stale reference
- **Alternatives considered**:
  - sweeping whole-repo terminology rewrite — rejected because Wave 2 should stay bounded
- **Assumptions**:
  - future stateless rehydration should have a small number of obvious front doors
- **Inherited constraints**:
  - write only to your assigned response file
  - do not edit shared files

## Anchors

- [SYNCRESCENDENCE-HOLISTIC-STRATEGIC-ENDEAVOR-v1.md](/Users/system/syncrescendence/knowledge/canon/SYNCRESCENDENCE-HOLISTIC-STRATEGIC-ENDEAVOR-v1.md)
- [HANDOFF-20260306-STATELESS-REHYDRATION-CC91.md](/Users/system/syncrescendence/communications/handoffs/HANDOFF-20260306-STATELESS-REHYDRATION-CC91.md)
- [README.md](/Users/system/syncrescendence/README.md)
- [knowledge/README.md](/Users/system/syncrescendence/knowledge/README.md)

## Required Output

1. the top live-facing docs with macro or nomenclature drift
2. minimal patch-ready wording for the highest-yield ones
3. a recommendation on whether this should be bundled into Wave 2 direct writes or deferred
4. top failure modes if macro drift is ignored
5. complete / partial / blocked status
