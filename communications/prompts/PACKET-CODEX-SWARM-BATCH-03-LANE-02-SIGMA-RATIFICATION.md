# Dispatch Packet

**Packet ID**: `PKT-20260306-codex-swarm-batch-03-lane-02-sigma-ratification`  
**Surface**: `codex_parallel_session`  
**Role**: `drafting`  
**Date**: `2026-03-06`  
**Objective**: draft the exact knowledge-lane updates that ratify `knowledge/sigma/` and demote bare `references/` to a housed subtype  
**Origin lane**: `communications/prompts`  
**Expected response**: `communications/responses/RESPONSE-CODEX-SWARM-BATCH-03-LANE-02-SIGMA-RATIFICATION.md`

## Decision Envelope

- **Trigger**: Batch 02 restored Sigma and identified the need for compatibility handling
- **Selected approach**: draft the knowledge-law amendments, Sigma README, and compatibility note
- **Alternatives considered**:
  - hard-renaming everything immediately — rejected because compatibility notes and staged rehousing are required
- **Assumptions**:
  - `knowledge/sigma/` is now the live secondary tier
- **Inherited constraints**:
  - write only to your assigned response file
  - do not edit shared files
- **Prior lineage**:
  - [RESPONSE-CODEX-SWARM-BATCH-02-LANE-02-CANON-SIGMA-REFERENCE.md](/Users/system/syncrescendence/communications/responses/RESPONSE-CODEX-SWARM-BATCH-02-LANE-02-CANON-SIGMA-REFERENCE.md)
  - [KNOWLEDGE-LANE-LAW-v1.md](/Users/system/syncrescendence/orchestration/state/impl/KNOWLEDGE-LANE-LAW-v1.md)

## Required Output

1. patch-ready amendment or replacement text for `KNOWLEDGE-LANE-LAW-v1.md`
2. patch-ready draft for `knowledge/sigma/README.md`
3. compatibility note draft for handling the existing `knowledge/references/` tree
4. minimal migration cautions for staged rehousing
5. top failure modes if Sigma ratification is implemented naively

## Constraints

- write only to `communications/responses/RESPONSE-CODEX-SWARM-BATCH-03-LANE-02-SIGMA-RATIFICATION.md`
- do not reopen the Sigma decision itself

## Return Path

`communications/responses/RESPONSE-CODEX-SWARM-BATCH-03-LANE-02-SIGMA-RATIFICATION.md`
