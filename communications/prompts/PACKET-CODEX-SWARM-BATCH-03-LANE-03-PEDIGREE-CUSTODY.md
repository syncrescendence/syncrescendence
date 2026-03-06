# Dispatch Packet

**Packet ID**: `PKT-20260306-codex-swarm-batch-03-lane-03-pedigree-custody`  
**Surface**: `codex_parallel_session`  
**Role**: `drafting`  
**Date**: `2026-03-06`  
**Objective**: draft the concrete pedigree custody artifacts for originals, rehoused material, manifests, receipts, and cautionary status  
**Origin lane**: `communications/prompts`  
**Expected response**: `communications/responses/RESPONSE-CODEX-SWARM-BATCH-03-LANE-03-PEDIGREE-CUSTODY.md`

## Decision Envelope

- **Trigger**: Batch 02 defined pedigree custody but the shell lacks the exact law artifact
- **Selected approach**: draft the compact law artifact and the minimum directory-level guidance needed for manifests and receipts
- **Alternatives considered**:
  - creating a giant archive doctrine — rejected because the first write set should stay narrow
- **Assumptions**:
  - cautionary status must be machine-readable even if the physical cautionary folder is deferred
- **Inherited constraints**:
  - write only to your assigned response file
  - do not edit shared files
- **Prior lineage**:
  - [RESPONSE-CODEX-SWARM-BATCH-02-LANE-03-PEDIGREE-AND-MANIFESTS.md](/Users/system/syncrescendence/communications/responses/RESPONSE-CODEX-SWARM-BATCH-02-LANE-03-PEDIGREE-AND-MANIFESTS.md)
  - [TRIBUTARY-CONTRACT-HARDENING-SYNTHESIS-v1.md](/Users/system/syncrescendence/orchestration/state/impl/TRIBUTARY-CONTRACT-HARDENING-SYNTHESIS-v1.md)

## Required Output

1. patch-ready draft for one compact pedigree custody law artifact
2. patch-ready README or schema guidance for `pedigree/archive-manifests/`
3. patch-ready README or schema guidance for `pedigree/rehousing-receipts/`
4. explicit machine-readable cautionary fields or template clauses
5. top failure modes if custody is implemented loosely

## Constraints

- write only to `communications/responses/RESPONSE-CODEX-SWARM-BATCH-03-LANE-03-PEDIGREE-CUSTODY.md`
- return concrete draft text, not only taxonomies

## Return Path

`communications/responses/RESPONSE-CODEX-SWARM-BATCH-03-LANE-03-PEDIGREE-CUSTODY.md`
