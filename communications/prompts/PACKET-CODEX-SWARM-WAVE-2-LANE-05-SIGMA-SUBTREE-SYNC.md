# Dispatch Packet

**Packet ID**: `PKT-20260306-codex-swarm-wave-2-lane-05-sigma-subtree-sync`  
**Surface**: `codex_parallel_session`  
**Role**: `drafting`  
**Date**: `2026-03-06`  
**Objective**: draft a bounded, compatibility-safe tranche for the first `knowledge/references/*` to `knowledge/sigma/references/*` subtree sync  
**Origin lane**: `communications/prompts`  
**Expected response**: `communications/responses/RESPONSE-CODEX-SWARM-WAVE-2-LANE-05-SIGMA-SUBTREE-SYNC.md`

## Decision Envelope

- **Trigger**: Sigma is ratified semantically, but the physical subtree sync remains deferred
- **Selected approach**: define the first bounded sync tranche, receipts, and compatibility notes without executing a mass move
- **Alternatives considered**:
  - full subtree relocation — rejected because compatibility and receipts must precede broad path motion
- **Assumptions**:
  - the current `knowledge/references/` tree remains live until a staged sync is completed
- **Inherited constraints**:
  - write only to your assigned response file
  - do not edit shared files

## Anchors

- [KNOWLEDGE-LANE-LAW-v1.md](/Users/system/syncrescendence/orchestration/state/impl/KNOWLEDGE-LANE-LAW-v1.md)
- [knowledge/sigma/README.md](/Users/system/syncrescendence/knowledge/sigma/README.md)
- [knowledge/references/README.md](/Users/system/syncrescendence/knowledge/references/README.md)
- [RESPONSE-CODEX-SWARM-BATCH-03-LANE-06-FIRST-MIGRATION-SEED-SET.md](/Users/system/syncrescendence/communications/responses/RESPONSE-CODEX-SWARM-BATCH-03-LANE-06-FIRST-MIGRATION-SEED-SET.md)

## Required Output

1. exact bounded subtree scope for the first sync tranche
2. compatibility rules before, during, and after sync
3. draft receipt set for the sync tranche
4. direct-write safe sequencing recommendations
5. top failure modes if sync is too broad or too early
6. complete / partial / blocked status
