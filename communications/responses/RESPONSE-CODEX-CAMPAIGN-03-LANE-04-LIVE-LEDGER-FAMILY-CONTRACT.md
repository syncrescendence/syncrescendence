# Response

**Response ID**: `RSP-20260309-codex-campaign-03-lane-04-live-ledger-family-contract`
**Surface**: `codex_parallel_session`
**Date received**: `2026-03-09`
**Dispatch packet**: `communications/prompts/PACKET-CODEX-CAMPAIGN-03-LANE-04-LIVE-LEDGER-FAMILY-CONTRACT.md`
**Result state**: `complete`
**Receipt artifact**: `communications/responses/RESPONSE-CODEX-CAMPAIGN-03-LANE-04-LIVE-LEDGER-FAMILY-CONTRACT.md`

## Returned Content

The shell should ratify a generalized **live-ledger family contract** before it widens domain-ledger rollout.

The tributary control plane already proves the minimum lawful pattern:

- explicit schema
- current-state surface
- append-only mutation ledger
- reportable validation

The imported live-ledger architecture adds the missing scale law:

- substrate / synthesis / dashboard layering
- visible freshness and decay
- repo crystallization versus exocortex accumulation

The correct generalized contract is therefore:

`repo-ratified law -> exocortex append-only substrate -> derived current-state surface -> repo-ratified synthesis snapshot -> optional dashboard and ontology projections`

## Generic Live-Ledger Family Contract

### 1. Layering Law

Every ledger family should define three operational layers plus one sovereignty layer.

| Layer | Purpose | Primary home | Contract |
|---|---|---|---|
| Sovereignty | meaning, schema law, rollout gates, ratification pointers | repo | nothing direction-bearing becomes shell truth without repo ratification |
| Substrate | agent-resolution events, observations, receipts, provenance, conflicts | exocortex by default | append-only, source-rich, high-churn, queryable |
| Synthesis | compaction, reconciliation, analysis, derived summaries | exocortex first, repo on ratification | transforms substrate into reusable intelligence with explicit provenance |
| Dashboard / Projection | human-resolution FIDS views and ontology projections | exocortex / ontology | read-only derivative surfaces; never sovereign |

The shell should treat dashboards and projections as consumers of a lawful substrate, not as substitute storage systems.

### 2. Append-Only Versus Current-State Surfaces

The family contract should require both an append-only surface and a current-state surface whenever a ledger represents changing live state.

- The append-only surface is the historical memory.
- The current-state surface is the operational convenience layer.
- The current-state surface may be updated or rematerialized, but only as a deterministic consequence of append-only events plus ratified derivation rules.
- No mutation that matters operationally should exist only in current state.
- No dashboard should read from a hand-maintained status table that cannot be rebuilt from substrate plus compaction rules.

The tributary pattern should generalize as:

- one append-only event ledger for every meaningful observation or mutation
- one materialized current-state registry or view for the latest lawful state
- one validator that proves the two still agree

### 3. Freshness And Decay Law

Freshness should attach to volatile intelligence, not to constitutional law.

- Repo law, schemas, and ratified contracts get version timestamps, not decay timers.
- Substrate observations and synthesis entries must carry explicit temporality and reliance metadata.
- Decay must reduce reliance class, not erase history.
- A stale row remains visible, queryable, and attributable.
- Dashboards must show staleness, conflicts, and sensing gaps explicitly.

Minimum field families for live ledgers:

- identity: `ledger_family`, `ledger_domain`, `entity_id`
- provenance: `source_pointer`, `source_type`, `observed_by`, `receipt_pointer`
- temporality: `occurred_at`, `observed_at`, `recorded_at`, `fresh_until`, `stale_after`
- epistemics: `confidence`, `epistemic_status`, `conflict_state`
- derivation: `row_version`, `last_event_id`, `materialized_from`
- sovereignty: `ratification_pointer`, `allowed_reliance_class`

The shell should standardize a small freshness vocabulary across ledgers:

- `fresh`
- `aging`
- `stale`
- `expired`
- `conflicted`

`conflicted` matters because not all decay is time-only; some decay is contradiction between sources or unresolved synthesis.

### 4. Repo Versus Exocortex Burden Split

The sovereignty split from the control-plane contract should bind all future ledgers.

Repo should hold:

- ledger family law
- domain-specific ledger contracts
- schema definitions
- validator specifications
- ratification pointers
- compacted snapshots
- approved synthesis worth loading into future sessions

Exocortex should hold:

- high-churn append-only substrate events
- live current-state materializations
- freshness calculations
- relation wiring and query joins
- dashboard views
- transient analysis entries before ratification

Ontology should hold:

- typed projections over repo and exocortex state
- lineage and relation surfaces
- contradiction visibility

Ontology must not hold:

- hidden semantic invention
- the only copy of authority-bearing meaning
- unratified field families or statuses

### 5. Exception Rule

The tributary-disposition plane is a lawful proof and can remain repo-native for now because it is:

- low-volume
- shell-sovereign
- authority-bearing
- already validated cleanly

That proof should not become the default storage policy for future high-churn domain ledgers.
For widened rollout, the default should be repo law plus exocortex live state.

## What Must Exist Before Dashboards And Projections Expand

No new dashboard or ontology projection should widen until the target ledger has all of the following:

1. a repo-ratified domain contract defining meaning, entity identity, and event types
2. a repo-ratified schema defining both append-only and current-state surfaces
3. a deterministic materialization rule from append-only substrate to current state
4. an explicit freshness / decay policy with visible status classes
5. validator logic that checks schema legality, event contiguity, state agreement, and freshness legality
6. at least one clean validation report on real data
7. at least one successful synthesis compaction cycle from substrate into ratified snapshot
8. ratification-pointer handling for any authority-bearing fields
9. contradiction and sensing-gap states that propagate upward instead of disappearing

Until those exist, dashboard expansion is decorative and projection expansion is dangerous.

## Proposed Durable Artifact Set

### Family-Level Repo Artifacts

- `orchestration/state/impl/LIVE-LEDGER-FAMILY-CONTRACT-v1.md`
  Defines the common law for substrate, synthesis, dashboard, and sovereignty boundaries.
- `orchestration/state/impl/LIVE-LEDGER-FRESHNESS-AND-DECAY-CONTRACT-v1.md`
  Defines freshness classes, decay semantics, and reliance rules.
- `orchestration/state/impl/LIVE-LEDGER-ROLLOUT-GATES-v1.md`
  Defines the mandatory gate checklist before any new ledger gets dashboard or projection surfaces.
- `orchestration/state/impl/LIVE-LEDGER-VALIDATOR-SPEC-v1.md`
  Defines the shared validator expectations across all ledgers.
- `orchestration/state/registry/live-ledger-family-schema-v1.md`
  Defines the common field families and required joins for event and current-state surfaces.
- `orchestration/state/registry/live-ledger-domain-register.csv`
  One row per ledger domain with volatility class, authority class, substrate pointer, snapshot path, and rollout state.
- `orchestration/state/registry/live-ledger-domain-register-ledger.jsonl`
  Append-only mutation ledger for the domain register itself.

### Per-Domain Minimum Artifact Pattern

- `orchestration/state/impl/<DOMAIN>-LEDGER-CONTRACT-v1.md`
  Domain semantics, event classes, authority class, and ratification rules.
- `orchestration/state/registry/<domain>-ledger-schema-v1.md`
  Domain schema for append-only events and current-state materialization.
- `exocortex://ledgers/<domain>/events`
  Append-only substrate events.
- `exocortex://ledgers/<domain>/current-state`
  Materialized latest state.
- `exocortex://ledgers/<domain>/analysis`
  Linked synthesis entries and compaction candidates.
- `orchestration/state/<DOMAIN>-LEDGER-VALIDATION-REPORT.md`
  Proof that the live surfaces remain lawful.
- `knowledge/sigma/<DOMAIN>-LEDGER-SNAPSHOT-v1.md`
  Repo-ratified compacted snapshot worth future session loading.

### Optional Only After Gates Pass

- `exocortex://dashboards/<domain>`
  Human-resolution FIDS view.
- `ontology://live-ledgers/<domain>`
  Typed projection layer.

Those two surfaces should remain optional consumers, not required primitives.

## First Safe Rollout Order

### Order For Shared Infrastructure

1. Ratify the family contract, freshness contract, validator spec, and rollout gates.
2. Register existing tributary-disposition as the reference proof rather than migrating it prematurely.
3. Stand up the shared domain register so widening does not become invisible sprawl.
4. Prove one low-sovereignty domain ledger end to end.
5. Prove a second domain ledger with higher synthesis burden.
6. Only then widen dashboards and ontology projections across multiple domains.

### Order For First Domain Ledgers

1. **Token Economics / Pricing Ledger**
   Safest first domain because sources are externally legible, source URLs are stable, decay is naturally time-based, and semantic risk is low.
2. **Model Capability / Benchmark Ledger**
   Good second domain because it is still externally grounded, but it introduces comparison logic, confidence handling, and contradiction management.
3. **Platform Constraints Ledger**
   Safe third because it is discrete and structured, but operationally closer to workflow-shaping law.
4. **Model Profile Ledger**
   Later because it blends observed facts with synthesis and steering interpretation.
5. **Lessons Ledger**
   Later still because it is high-yield but epistemically interpretive; it should not become a semantic junk drawer.

### Surfaces To Keep Repo-First Until The Family Proves Itself

- Canonical CI Registry
- Structural Primitives Codex
- Methodology Playbook
- Inter-Model Interface Protocol

Those surfaces are direction-bearing and should remain primarily repo-ratified documents until the live-ledger family has already proven:

- clean substrate behavior
- lawful compaction
- drift-resistant freshness handling
- projection discipline

## Decision Summary

The shell should not widen by creating many ledgers at once.
It should widen by ratifying one generic contract family and then instantiating it selectively.

The governing rule is:

- append-only substrate for history
- materialized current state for operations
- repo-ratified synthesis for durable loading
- dashboards and projections only as derivative surfaces

That is the narrow bridge between the proven tributary control plane and the larger seven-ledger ambition.

## Status

`complete`

`git diff --check` was run after writing this artifact and returned clean.
