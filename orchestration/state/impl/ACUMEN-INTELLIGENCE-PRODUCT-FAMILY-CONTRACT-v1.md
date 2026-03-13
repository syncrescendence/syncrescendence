# Acumen Intelligence Product Family Contract v1

**Status**: staged  
**Class**: implementation law  
**Purpose**: define the first lawful Acumen product family that renders the now-real post-triage chain without creating a parallel authority plane

## Why This Family Exists

Campaign 11 made the post-triage chain real:

`triage decision -> verification dossier -> Augur packet -> Augur response -> repo-side assessment -> primary-source queue`

What remained missing was the product layer that an operator can actually consume.

That product layer must stay narrow:

- `Dawn Brief` remains the triage-era awareness product
- post-triage products must consume repo-side assessment and queue surfaces, not bypass them
- no brief may claim authority that belongs to ledgers, dossiers, responses, assessments, or queue state

## Product Law

The first lawful Acumen product family has exactly three products:

1. `Dawn Brief`
2. `Verified Signal Brief`
3. `Primary-Source Queue Readout`

This family is derivative-only.
It does not introduce a new truth class.

## State Placement

### 1. Dawn Brief

- output: `runtime/acumen/out/DAWN-BRIEF-*.md`
- consumes: `runtime/acumen/triage-decisions.jsonl`
- state class: triage-era awareness

### 2. Verified Signal Brief

- output: `runtime/acumen/out/VERIFIED-SIGNAL-BRIEF-*.md`
- consumes:
  - `runtime/acumen/out/augur-return-assessments/*.json`
  - `orchestration/state/ACUMEN-AUGUR-PRIMARY-SOURCE-QUEUE.json`
- state class: post-assessment derivative brief

### 3. Primary-Source Queue Readout

- output: `runtime/acumen/out/PRIMARY-SOURCE-QUEUE-READOUT-*.md`
- consumes:
  - `orchestration/state/ACUMEN-AUGUR-PRIMARY-SOURCE-QUEUE.json`
  - linked assessment artifacts for enrichment only
- state class: escalation readout

## Authority Boundary

Authority stays distributed across the upstream surfaces:

1. triage authority remains in the Acumen evidence ledgers and rematerialized triage queue
2. verification bridge authority remains in the verification dossier and Augur packet family
3. witness authority for external verification remains in the landed Augur response path
4. classification authority for post-triage interpretation remains in repo-side assessment artifacts
5. escalation authority remains in the primary-source queue state

The products in this family may summarize those surfaces.
They may not replace them.

## Builder Law

The minimum lawful builders are:

1. `operators/acumen/build_dawn_brief.py`
2. `operators/acumen/build_verified_signal_brief.py`
3. `operators/acumen/build_primary_source_queue_readout.py`

Each builder must render from an already-materialized upstream state.

That means:

- `Dawn Brief` does not read ledgers directly when a rematerialized triage queue exists
- `Verified Signal Brief` does not read Augur response markdown directly
- `Primary-Source Queue Readout` does not invent queue membership or alter queue status

## Deliberate Deferrals

The first family does not include:

1. executive rollups
2. weekly or channel-specific variants
3. doctrine or constitutional synthesis products
4. a separate pre-verification human brief that would duplicate the dossier and packet layer

Those remain deferred until the first three-product family proves stable.
