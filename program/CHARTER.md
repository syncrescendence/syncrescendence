# Program Charter

- **Status**: live program authority contract
- **Last reviewed**: `2026-03-09`
- **Review cadence**: campaign boundary or when the active tranche set changes
- **Semantic authority**: [ROSETTA-STONE.live.md](/Users/system/syncrescendence/orchestration/state/ROSETTA-STONE.live.md)
- **Executive authority**: [INTENT-COMPASS.live.md](/Users/system/syncrescendence/executive/INTENT-COMPASS.live.md)
- **Control-plane contract**: [CONTROL-PLANE-SOVEREIGNTY-CONTRACT-v1.md](/Users/system/syncrescendence/orchestration/state/impl/CONTROL-PLANE-SOVEREIGNTY-CONTRACT-v1.md)

This lane holds implementation programs and active queues.

Primary function:
- backlog
- tranche plans
- implementation maps
- delivery sequencing

## Visible Binding Grammar

Every live backlog tranche and standalone tranche file should expose:

- `program_id`
- `intent_refs`
- `rosetta_refs`
- `execution_surface`
- `lineage_or_origin`

Meaning:

- `program_id` gives the work item a stable program address
- `intent_refs` bind execution to live executive steering
- `rosetta_refs` bind execution to live semantic law
- `execution_surface` names the concrete file, operator, or venue where the work lands
- `lineage_or_origin` records the campaign, pedigree witness, or predecessor tranche that produced the work item

Rules:
- every major program item should trace upward to live intent and live Rosetta authority
- this lane is execution-facing, not constitutional
- stale or completed program artifacts should be compacted, not left to sprawl
- items missing the visible binding grammar are not promotion-ready
