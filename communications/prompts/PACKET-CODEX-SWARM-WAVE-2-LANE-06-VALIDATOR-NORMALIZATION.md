# Dispatch Packet

**Packet ID**: `PKT-20260306-codex-swarm-wave-2-lane-06-validator-normalization`  
**Surface**: `codex_parallel_session`  
**Role**: `drafting`  
**Date**: `2026-03-06`  
**Objective**: normalize the optional validator/template pack to the ratified schema and decide what enforcement should happen immediately versus later  
**Origin lane**: `communications/prompts`  
**Expected response**: `communications/responses/RESPONSE-CODEX-SWARM-WAVE-2-LANE-06-VALIDATOR-NORMALIZATION.md`

## Decision Envelope

- **Trigger**: the validator lane is still useful, but its earlier draft used pre-ratification vocabulary drift
- **Selected approach**: rewrite it narrowly against the current schema and law, without turning it into a general migration engine
- **Alternatives considered**:
  - full validator rollout now — rejected because the enforcement layer should stay subordinate and thin
- **Assumptions**:
  - validator work remains optional after the core compatibility and seed work
- **Inherited constraints**:
  - write only to your assigned response file
  - do not edit shared files

## Anchors

- [tributary-disposition-schema-v1.md](/Users/system/syncrescendence/orchestration/state/registry/tributary-disposition-schema-v1.md)
- [PEDIGREE-CUSTODY-LAW-v1.md](/Users/system/syncrescendence/pedigree/PEDIGREE-CUSTODY-LAW-v1.md)
- [PROMOTION-THRESHOLDS-v1.md](/Users/system/syncrescendence/orchestration/state/impl/PROMOTION-THRESHOLDS-v1.md)
- [RESPONSE-CODEX-SWARM-BATCH-03-LANE-07-VALIDATOR-TEMPLATES.md](/Users/system/syncrescendence/communications/responses/RESPONSE-CODEX-SWARM-BATCH-03-LANE-07-VALIDATOR-TEMPLATES.md)

## Required Output

1. normalized validator rule set using current schema vocabulary only
2. normalized template blocks using current path and enum forms
3. a recommended immediate versus deferred enforcement split
4. top failure modes if validator rollout outruns law maturity
5. complete / partial / blocked status
