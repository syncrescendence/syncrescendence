# Dispatch Packet

**Packet ID**: `PKT-20260306-codex-swarm-wave-2-lane-03-registry-seed-normalization`  
**Surface**: `codex_parallel_session`  
**Role**: `drafting`  
**Date**: `2026-03-06`  
**Objective**: normalize the first migration seed set into schema-valid registry rows under the ratified control plane  
**Origin lane**: `communications/prompts`  
**Expected response**: `communications/responses/RESPONSE-CODEX-SWARM-WAVE-2-LANE-03-REGISTRY-SEED-NORMALIZATION.md`

## Decision Envelope

- **Trigger**: the seed set exists conceptually, but its ids, path forms, and disposition values are not yet valid under the ratified schema
- **Selected approach**: convert the first tranche into exact row-ready content without yet writing live CSV rows
- **Alternatives considered**:
  - populating the registry directly from the old seed draft — rejected because vocabulary drift would corrupt the control plane
- **Assumptions**:
  - Lane 01 schema from Wave 1 is authoritative
- **Inherited constraints**:
  - write only to your assigned response file
  - do not edit shared files

## Anchors

- [tributary-disposition-schema-v1.md](/Users/system/syncrescendence/orchestration/state/registry/tributary-disposition-schema-v1.md)
- [RESPONSE-CODEX-SWARM-BATCH-03-LANE-06-FIRST-MIGRATION-SEED-SET.md](/Users/system/syncrescendence/communications/responses/RESPONSE-CODEX-SWARM-BATCH-03-LANE-06-FIRST-MIGRATION-SEED-SET.md)
- [TRIBUTARY-RATIFICATION-WRITESET-SYNTHESIS-v1.md](/Users/system/syncrescendence/orchestration/state/impl/TRIBUTARY-RATIFICATION-WRITESET-SYNTHESIS-v1.md)

## Required Output

1. 10-20 schema-valid candidate rows in CSV-ready form
2. normalized `tdc-*` ids and `merge_family_id` values
3. exact `chosen_disposition` and `record_state` values from the schema
4. repo-relative source and destination paths only
5. top failure modes if these rows are populated prematurely or incorrectly
6. complete / partial / blocked status
