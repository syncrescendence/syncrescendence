# Live Ledger Rollout Gates v1

**Status**: live-v1
**Class**: implementation law
**Purpose**: define the first shared rollout gates for live-ledger widening so domain registers can widen without outrunning the family contract

## Compact Contract

- the widening register is a control surface, not a new sovereign layer
- no candidate domain may claim live-ledger completion from current-state shape alone
- the first widening phases are lawful seed, repo proof, family-default readiness, and projection opening
- already-live proof families must widen non-breakingly

This artifact applies the [LIVE-LEDGER-FAMILY-CONTRACT-v1.md](/Users/system/syncrescendence/orchestration/state/impl/LIVE-LEDGER-FAMILY-CONTRACT-v1.md) to the first shared domain register at [live-ledger-domain-register.csv](/Users/system/syncrescendence/orchestration/state/registry/live-ledger-domain-register.csv).

## 1. Governing Scope

The first governed register is:

- `orchestration/state/registry/live-ledger-domain-register.csv`

The register may name:

- already-active live-ledger families
- candidate domains that currently have only a lawful seed surface
- the gate profile and rollout state for each domain

The register does not itself ratify authority-bearing meaning.
It records which sovereign artifact governs a domain and which widening gates remain open.

## 2. Shared Gate Definitions

| Gate ID | Name | Pass condition | Failure meaning |
|---|---|---|---|
| `LG-01` | sovereign_anchor | a repo-ratified artifact names the domain's meaning, burden split, and allowed reliance | the domain has no lawful sovereign home |
| `LG-02` | current_state_surface_named | one machine-addressable current-state surface is named and explicitly subordinate to repo law | the domain has no stable present-state surface |
| `LG-03` | append_only_substrate_named | one append-only substrate is named or the register explicitly records `pending` and keeps the domain in seed state | the domain is pretending current state is enough |
| `LG-04` | materialization_rule_bound | the domain has a ratified derivation or rematerialization rule from substrate to current state | current state cannot be lawfully rebuilt |
| `LG-05` | projection_subordination | reports, dashboards, effective registries, and ontology views are declared derivative rather than sovereign | a projection surface is trying to become authority |
| `LG-06` | proof_preservation | if a live proof family already exists, widening preserves the current proof baseline through compatibility treatment or non-breaking rollout law | widening would break a relied-on live proof |

`LG-03` allows `pending` only for `phase0_lawful_seed`.
Any domain beyond seed state must name a real append-only substrate.

## 3. Rollout Phases

### `phase0_lawful_seed`

Required gates:

- `LG-01`
- `LG-02`
- `LG-05`

Expected state:

- a lawful sovereign anchor exists
- one machine-addressable current-state or read-model surface is named
- append-only substrate may still be `pending`
- the domain is informative for widening planning, not yet a completed live-ledger family

### `phase1_repo_proof`

Required gates:

- `LG-01`
- `LG-02`
- `LG-03`
- `LG-04`
- `LG-05`

Conditional requirement:

- `LG-06` if the domain already carries relied-on live proof

Expected state:

- linked current-state and append-only surfaces exist
- repo-native proof remains lawful and non-breaking
- the family is active even if exocortex-first widening has not yet occurred

### `phase2_family_default_ready`

Required gates:

- `LG-01`
- `LG-02`
- `LG-03`
- `LG-04`
- `LG-05`
- `LG-06` when applicable

Expected state:

- the domain is ready for the family default path
- exocortex substrate residence, deterministic synthesis, or equivalent widening treatment is named without shifting sovereignty away from repo law

### `phase3_projection_open`

Required gates:

- all prior required gates remain passing

Expected state:

- optional dashboards, reports, effective registries, and ontology projections may widen around the domain
- those surfaces remain derivative and replaceable

## 4. Gate Profiles

### `GL-SHARED-V1`

This is the default profile for newly named domains in the first register.

It requires:

1. `phase0_lawful_seed` before a domain is treated as a real widening candidate
2. `phase1_repo_proof` before a domain is treated as an active live-ledger family
3. `phase2_family_default_ready` before exocortex-first widening is described as ready
4. `phase3_projection_open` before dashboard or ontology widening is described as open

### `GL-TRIBUTARY-V1`

This is the stricter profile for the existing tributary proof family.

It inherits `GL-SHARED-V1` and adds:

- `LG-06` is mandatory before any schema, validator, or header widening step
- ratification-pointer rollout remains ordered by `schema law first -> validator compatibility second -> header change last`

The tributary family may not widen by breaking the current proof baseline.

## 5. Initial Register Application

| Domain ID | Gate profile | Current state | Current lawful reading |
|---|---|---|---|
| `tributary_disposition` | `GL-TRIBUTARY-V1` | `phase1_repo_proof` | active repo-native proof family with non-breaking widening constraints |
| `office_harness_state` | `GL-SHARED-V1` | `phase0_lawful_seed` | subordinate read-model seed, not yet a complete live-ledger family |
| `config_surface_state` | `GL-SHARED-V1` | `phase0_lawful_seed` | machine-addressable current-state seed, not yet a complete live-ledger family |

These are intentionally the only first-register rows.
The shell should prove the gate discipline on a small set before naming additional families.

## 6. Register Mutation Law

Adding a new register row requires:

- one stable `domain_id`
- one sovereign artifact path
- one named current-state surface
- one gate profile
- one explicit rollout state

Advancing a row beyond `phase0_lawful_seed` requires:

- naming a real append-only substrate
- binding the materialization rule
- stating whether `LG-06` applies

The register may grow.
It may not silently reclassify a seed domain as an active family without the required gate changes.

## 7. Out Of Scope For v1

This artifact does not define:

- per-domain validator implementations
- exocortex storage vendor choice
- freshness or decay adjuncts
- dashboard design
- a full domain census

It only defines the first shared widening gate language needed to keep the initial register small and lawful.
