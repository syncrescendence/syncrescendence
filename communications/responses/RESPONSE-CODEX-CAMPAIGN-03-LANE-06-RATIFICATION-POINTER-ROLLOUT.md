# Response

**Packet ID**: `PKT-20260309-codex-campaign-03-lane-06-ratification-pointer-rollout`
**Date**: `2026-03-09`
**Role**: `synthesis`
**Status**: `complete`

## Decision

The shell should introduce the ratification-pointer rule as schema-law first, then validator compatibility, and only later as an inline registry/header change.

That order is the non-breaking path because:

- the live tributary validator currently requires the exact v1 CSV header and would fail on immediate column churn
- the live proof surface currently passes with `10` rows and `50` ledger events
- a validator-only rollout would wrongly let tooling, rather than repo law, decide what counts as authority

So the first rollout should be:

1. schema-law transition
2. validator dual-mode enforcement
3. header/schema revision last

## First Surfaces

Adopt the rule first on the current authority-bearing control-plane family under `orchestration/state/registry/`:

1. [tributary-disposition-schema-v1.md](/Users/system/syncrescendence/orchestration/state/registry/tributary-disposition-schema-v1.md)
2. the tributary validator and its report surface
3. only after that, the live CSV and JSONL artifacts

This family should go first because it is the only live canonical registry/schema pair currently carrying current-state disposition meaning in the repo. Exocortex registries, ontology projections, and report artifacts should not lead the rollout because the sovereignty contract makes them downstream of repo ratification, not the source of it.

## Transition Rule

The schema should ratify a temporary compatibility rule for `v1`:

- the existing CSV header remains the normative `v1` header
- the existing JSONL event shape remains the normative `v1` ledger shape
- a `v1` row counts as authority-bearing during transition only if a repo-native compatibility receipt binds that row to the required pointer fields
- a `v1` row with no such binding remains informative only

This preserves the sovereignty contract without pretending the old header already carries fields it does not have.

## Informative Versus Authority-Bearing

During transition, row class should be determined by ratification binding, not by prose, freshness, or artifact class alone.

An informative row is one that:

- has no inline pointer fields
- is not listed in the compatibility receipt
- may still describe custody, intake, or candidate state
- must not be relied on as law by downstream operators, dashboards, or ontology projections

An authority-bearing row is one that:

- is explicitly bound by the compatibility receipt in `v1`, or
- later carries inline pointer fields in a `v2` schema/header

The compatibility receipt should key by `candidate_id` and record:

- `ratification_pointer`
- `ratified_by_artifact_path`
- `ratified_by_artifact_id`
- `ratified_at`

This is the cleanest way to distinguish legacy informative rows from ratified rows without immediate header churn.

## Validator Path

The validator should be updated only after the schema-law transition is ratified.

Validator behavior should roll out in two steps:

1. Preserve the current structural checks and exact `v1` header acceptance unchanged.
2. Add compatibility checks that read the ratification-binding receipt and classify rows as either `authority_bound` or `informative_only`.

Failure policy during the transition window:

- existing grandfathered `v1` rows may remain valid if they are covered by the compatibility receipt
- new authority-bearing rows added after the rollout effective date should fail if they have neither inline pointer fields nor a compatibility binding
- informative-only rows may still exist, but validators and reports must state that they are non-authoritative

The validation report should therefore remain report-only, but it should gain one extra compatibility section once the validator is updated:

- structural legality
- pointer-binding coverage
- any rows still informative-only

## Header Change Timing

Do not start with a header change.

A header change should happen only after:

1. the schema has already ratified the temporary `v1` compatibility rule
2. the validator can read both legacy `v1` rows and future pointer-bearing rows
3. a backfill receipt exists for the authority-bearing legacy rows

Then the shell can publish a `v2` schema that adds inline pointer fields to the CSV and matching keys to ledger `field_changes` for any migration corrections.

At that stage:

- the validator should accept both `v1` and `v2` for one bounded compatibility window
- legacy rows should be migrated with `row_corrected` events that do not rewrite state history
- after migration completion, inline pointers can become mandatory for all authority-bearing rows

## Required Receipts And Compatibility Steps

Minimum required artifacts:

1. A ratified rollout receipt that freezes the current proof baseline: `10` rows, `50` ledger events, validation `PASS` as of `2026-03-09`.
2. A ratification-binding compatibility receipt keyed by `candidate_id` for every legacy row that the shell still wants treated as authority-bearing.
3. A validator rollout receipt stating the effective date after which new authority-bearing rows must have either compatibility binding or inline pointer fields.
4. A later `v1 -> v2` migration receipt covering header adoption, row backfill, and any `row_corrected` ledger append.

## Phased Rollout

### Phase 1. Ratify Transition Law

- Amend schema law first.
- Keep live registry and ledger files unchanged.
- Define compatibility receipt semantics for `v1`.

### Phase 2. Ship Validator Compatibility

- Keep exact `v1` header acceptance.
- Add authority-binding classification against the compatibility receipt.
- Report informative-only rows explicitly.

### Phase 3. Bind Legacy Authority Rows

- Issue compatibility bindings for the current authority-bearing row set.
- Leave unbound rows informative-only.
- Do not rewrite historical ledger events.

### Phase 4. Introduce Inline `v2`

- Add pointer columns and ledger support in a new schema version.
- Run dual-read validation for a bounded window.
- Append non-state-changing correction events for migrated rows.

### Phase 5. End Compatibility Mode

- Require inline pointers for every new authority-bearing row and schema change.
- Retire the sidecar compatibility receipt once all relied-on rows are migrated.

## Final Answer

The shell should not introduce ratification pointers by changing the live tributary header first. It should first ratify the rule in schema law, attach pointer authority to existing `v1` rows through a repo-native compatibility receipt keyed by `candidate_id`, teach validators to distinguish `authority_bound` from `informative_only`, and only then publish a `v2` header with inline pointer fields. That is the smallest rollout that preserves current control-plane proofs, avoids premature header churn, and still makes unratified rows explicitly non-sovereign.
