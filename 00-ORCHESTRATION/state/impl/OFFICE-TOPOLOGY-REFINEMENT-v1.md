# Office Topology Refinement v1

## Purpose

Refine the first successor-shell office layer using the highest-signal predecessor office contracts.

Primary pedigree inputs:

- [commander/INIT.md](/Users/system/Desktop/syncrescendence-pre-syncrephoenix/agents/commander/INIT.md)
- [commander memory](/Users/system/Desktop/syncrescendence-pre-syncrephoenix/agents/commander/memory/MEMORY.md)
- [ajna/INIT.md](/Users/system/Desktop/syncrescendence-pre-syncrephoenix/agents/ajna/INIT.md)
- [psyche/INIT.md](/Users/system/Desktop/syncrescendence-pre-syncrephoenix/agents/psyche/INIT.md)

## Design Decision

The predecessor office model was right that a flat `inbox/` and flat `outbox/` are too weak once office-local work becomes nontrivial.

The successor shell therefore promotes the following lawful substructure:

- `inbox/pending`
- `inbox/active`
- `inbox/done`
- `inbox/failed`
- `inbox/blocked`
- `outbox/dispatches`
- `outbox/receipts`
- `outbox/results`
- `memory/journal`
- `memory/cache`
- `memory/sync`

## Why This Survives

This keeps the useful parts of the predecessor office contract:

- local triage state
- resumable execution
- explicit failure and blockage lanes
- receipts as first-class office outputs
- memory tiers instead of one undifferentiated office cache

## What Is Still Forbidden

This refinement does not revive:

- root-global `-INBOX` / `-OUTBOX`
- shadow federal backlog
- office-local hidden canon
- shell-hostile dashed topologies

## Operatorization

This refinement is implemented by:

- [bootstrap_office.py](/Users/system/syncrescendence/operators/bootstrap_office.py) for new offices
- [upgrade_existing_offices.py](/Users/system/syncrescendence/operators/office/upgrade_existing_offices.py) for current live offices
