# Dispatch Packet

**Packet ID**: `PKT-20260306-codex-swarm-batch-03-lane-06-first-migration-seed-set`  
**Surface**: `codex_parallel_session`  
**Role**: `drafting`  
**Date**: `2026-03-06`  
**Objective**: draft the first concrete migration seed set once the contract layer is assumed settled  
**Origin lane**: `communications/prompts`  
**Expected response**: `communications/responses/RESPONSE-CODEX-SWARM-BATCH-03-LANE-06-FIRST-MIGRATION-SEED-SET.md`

## Decision Envelope

- **Trigger**: Batch 02 identified that the next execution pass needs initial registry rows, merge families, Sigma rehousings, manifests, and receipts
- **Selected approach**: propose a small first tranche rather than a huge migration census
- **Alternatives considered**:
  - attempting whole-repo seeding immediately — rejected because it would be too brittle
- **Assumptions**:
  - the first tranche should privilege high-authority doctrinal families and compatibility-safe custody moves
- **Inherited constraints**:
  - write only to your assigned response file
  - do not edit shared files
- **Prior lineage**:
  - [TRIBUTARY-CONTRACT-HARDENING-SYNTHESIS-v1.md](/Users/system/syncrescendence/orchestration/state/impl/TRIBUTARY-CONTRACT-HARDENING-SYNTHESIS-v1.md)
  - Batch 01 and Batch 02 response artifacts

## Required Output

1. the first 10-20 candidate rows that should enter the registry
2. the first merge families and dual-witness families to seed
3. the first Sigma rehousing targets
4. the first manifest and rehousing-receipt candidates
5. top failure modes if the seed set is too ambitious or too timid

## Constraints

- write only to `communications/responses/RESPONSE-CODEX-SWARM-BATCH-03-LANE-06-FIRST-MIGRATION-SEED-SET.md`
- prioritize compatibility-safe, high-authority initial moves

## Return Path

`communications/responses/RESPONSE-CODEX-SWARM-BATCH-03-LANE-06-FIRST-MIGRATION-SEED-SET.md`
