# Response

**Response ID**: `RSP-20260309-codex-campaign-03-lane-05-office-harness-contract-and-validator`
**Surface**: `codex_parallel_session`
**Date received**: `2026-03-09`
**Dispatch packet**: `communications/prompts/PACKET-CODEX-CAMPAIGN-03-LANE-05-OFFICE-HARNESS-CONTRACT-AND-VALIDATOR.md`
**Result state**: `complete`
**Receipt artifact**: `communications/responses/RESPONSE-CODEX-CAMPAIGN-03-LANE-05-OFFICE-HARNESS-CONTRACT-AND-VALIDATOR.md`

## Returned Content

The shell should make office-to-harness bindings lawful by treating office identity as durable constitutional truth and harness binding as mutable repo-resident metadata plus validator-checked state.

The governing rule is:

- office path is durable
- harness binding is metadata
- binding changes are ratified in repo artifacts, not inferred from directory names, veneers, or runtime habit

That yields the correct non-drift chain:

`AGENTS.md -> office-harness binding law -> per-office binding contract -> rendered effective registry -> validator reports -> exocortex or ontology projection`

This keeps office identity stable across harness churn while still making the current binding explicit, machine-checkable, and lawful.

## 1. Durable Law Artifact Set

The next durable artifact family should be:

1. `orchestration/state/impl/OFFICE-HARNESS-BINDING-CONTRACT-v1.md`
2. `offices/<office>/platform/contracts/OFFICE-HARNESS-METADATA.v1.yaml`
3. `operators/validators/validate_office_harness_coherence.py`
4. `orchestration/state/registry/office-harness-bindings.effective.json`
5. `orchestration/state/registry/office-harness-binding-ledger.jsonl`
6. `orchestration/state/OFFICE-HARNESS-COHERENCE-REPORT.json`
7. `orchestration/state/OFFICE-HARNESS-COHERENCE-REPORT.md`

### 1.1 What each artifact does

- `OFFICE-HARNESS-BINDING-CONTRACT-v1.md`: ratified repo law for schema, invariants, precedence, and validator obligations.
- `OFFICE-HARNESS-METADATA.v1.yaml`: one hand-authored current-state contract per office.
- `validate_office_harness_coherence.py`: deterministic validator and report renderer.
- `office-harness-bindings.effective.json`: rendered read model compiled from per-office contracts; query surface, not separate doctrine.
- `office-harness-binding-ledger.jsonl`: append-only rebinding history and evidence trail when bindings change.
- `OFFICE-HARNESS-COHERENCE-REPORT.{json,md}`: report surfaces for humans, automation, and CI.

### 1.2 Authority split

- `AGENTS.md` remains constitutional authority for office identity, federal roles, and certified harness labels.
- `OFFICE-HARNESS-BINDING-CONTRACT-v1.md` becomes the binding-law authority for how office and harness facts are represented.
- `OFFICE-HARNESS-METADATA.v1.yaml` is the canonical current-state binding declaration for each office.
- `office-harness-bindings.effective.json` is rendered from the office contracts and must never become a second hand-authored constitution.
- ledger rows preserve change history; they do not redefine office meaning.

This matches the control-plane sovereignty rule:

- repo ratifies
- validators and registries coordinate
- downstream projections repeat but do not replace repo meaning

## 2. Repo-Law Candidate

`OFFICE-HARNESS-BINDING-CONTRACT-v1.md` should ratify the following rules.

### 2.1 Identity rule

- office identity is keyed by `office_id` and office path
- office directories are never named after harnesses
- rebinding a harness must not require renaming an office, playbook, or promotion lane

### 2.2 Binding rule

- every federal office must declare exactly one current primary harness
- a harness may back one or more offices if law allows it
- stage0 surfaces may appear in playbooks or registries, but they do not become offices by binding alone

### 2.3 Source-precedence rule

Precedence should be:

1. `AGENTS.md`
2. `orchestration/state/impl/OFFICE-HARNESS-BINDING-CONTRACT-v1.md`
3. `offices/<office>/platform/contracts/OFFICE-HARNESS-METADATA.v1.yaml`
4. `orchestration/state/registry/office-harness-bindings.effective.json`
5. exocortex or ontology projections

If any lower layer disagrees with a higher one, the higher layer wins and the validator reports drift.

### 2.4 Rebinding rule

When an office changes harness:

1. the office directory stays fixed
2. the per-office metadata file changes
3. a ledger event is appended
4. the effective registry is re-rendered
5. the validator must pass before the new binding can be treated as operative

### 2.5 Ratification-pointer rule

Because binding registries and ledger rows are authority-bearing enough to affect downstream routing, they should carry the control-plane sovereignty pointer family:

- `ratification_pointer`
- `ratified_by_artifact_path`
- `ratified_by_artifact_id`
- `ratified_at`

For the effective rendered registry, these fields may be copied from the office-local contract or the governing law artifact.

## 3. Minimum Metadata Contract

The minimum per-office contract should stay small and typed.

Recommended file:

- `offices/<office>/platform/contracts/OFFICE-HARNESS-METADATA.v1.yaml`

Recommended minimum:

```yaml
schema_version: office-harness-metadata/v1
office_id: ajna
office_title: Ajna
federal_role: strategic-office
office_root: /Users/system/syncrescendence/offices/ajna
playbook_path: /Users/system/syncrescendence/playbooks/ajna/PLAYBOOK.md
binding:
  primary_harness: openclaw_macbook_air
  harness_family: openclaw
  avatar_label: Ajna
  surface_class: persistent-runtime
  provider: anthropic
  model: claude-sonnet-4-5
  machine: macbook-air
  auth_mode: setup-token
  account_ref: claude-subscription
promotion:
  may_promote_to:
    - communications
    - runtime
    - executive
  local_only_classes:
    - platform-logs
    - scratch-notes
coherence:
  required_sources:
    - /Users/system/syncrescendence/AGENTS.md
    - /Users/system/syncrescendence/playbooks/ajna/PLAYBOOK.md
  required_local_paths:
    - inbox
    - memory
    - outbox
    - platform/contracts
authority:
  ratification_pointer: office-harness-binding-contract/v1
  ratified_by_artifact_path: /Users/system/syncrescendence/orchestration/state/impl/OFFICE-HARNESS-BINDING-CONTRACT-v1.md
  ratified_by_artifact_id: OFFICE-HARNESS-BINDING-CONTRACT-v1
status:
  binding_state: active
  last_verified_on: 2026-03-09
```

### 3.1 Required fields

- `schema_version`
- `office_id`
- `office_title`
- `federal_role`
- `office_root`
- `playbook_path`
- `binding.primary_harness`
- `binding.harness_family`
- `binding.avatar_label`
- `binding.surface_class`
- `promotion.may_promote_to`
- `coherence.required_sources`
- `coherence.required_local_paths`
- `authority.ratification_pointer`
- `authority.ratified_by_artifact_path`
- `authority.ratified_by_artifact_id`
- `status.binding_state`

### 3.2 Conditionally required fields

- `binding.machine`, `binding.auth_mode`, `binding.provider`: required for OpenClaw-bound offices
- `binding.model`: required when the office relies on a model-specific surface contract
- `binding.account_ref`: required when multiple lawful accounts could make the same harness label ambiguous

### 3.3 Explicitly forbidden

- secrets
- raw tokens
- cookies
- session dumps
- unratified role claims
- office renames hidden inside metadata rewrites

## 4. Rollout Order Across Offices

The correct rollout is not alphabetical. It should follow proof burden.

### 4.1 Phase 0: law plus one reference specimen

Write the law artifact first, then add one reference contract for `commander`.

Why `commander` first:

- it already has the deepest office-local contract surface
- the `commander -> claude_code` binding is least ambiguous
- it provides the cleanest validator fixture before the heavier OpenClaw cases

### 4.2 Phase 1: highest-burden runtime offices

Add full contracts for:

- `ajna -> openclaw_macbook_air`
- `psyche -> openclaw_mac_mini`

These offices should be first operational targets because they carry the most runtime-specific facts:

- machine binding
- auth mode
- persistent runtime surface
- stronger risk of hidden drift between playbooks and reality

### 4.3 Phase 2: remaining federal offices

Add contracts for:

- `adjudicator -> codex`
- `cartographer -> gemini_cli`

These are lighter than the OpenClaw offices but still need explicit binding law so the shell does not infer them from veneers or habit.

### 4.4 Phase 3: all-office strictness

Once all five offices have clean contracts and the validator is stable:

- render the effective registry on every run
- require validator clean pass before rebinding is accepted
- add a Make target such as `make check-office-harness-coherence`

## 5. Validator Phases And Output Surfaces

The validator should start report-first and become strict only after the contract family exists everywhere.

### 5.1 Phase A: structural report-only

Checks:

- all five federal offices exist
- each office has a playbook
- each target office has `platform/contracts/OFFICE-HARNESS-METADATA.v1.yaml`
- `office_id` matches the folder name
- `office_root` and `playbook_path` resolve
- `primary_harness` is a certified harness label from `AGENTS.md`
- required local paths exist
- no secret-like material appears

Outputs:

- `orchestration/state/OFFICE-HARNESS-COHERENCE-REPORT.json`
- `orchestration/state/OFFICE-HARNESS-COHERENCE-REPORT.md`
- exit code `0` even with findings

### 5.2 Phase B: law and cross-source coherence

Add checks for:

- office-to-harness pair matches current repo law
- OpenClaw offices declare `machine`, `provider`, and `auth_mode`
- office playbook and metadata do not contradict each other
- promotion scopes stay inside lawful federal lanes
- stage0 surfaces do not appear as federal offices
- authority pointers are present

Outputs:

- the same JSON and Markdown reports
- rendered `orchestration/state/registry/office-harness-bindings.effective.json`
- exit code still `0` by default

### 5.3 Phase C: strict enforcement

Add:

- `--strict`
- non-zero exit on drift, missing contracts, illegal bindings, or pointer failures
- CI and pre-promotion use

### 5.4 Minimum finding classes

- `missing_contract`
- `path_mismatch`
- `illegal_harness_binding`
- `missing_runtime_binding_fact`
- `promotion_scope_drift`
- `secret_like_material`
- `playbook_contract_contradiction`
- `authority_pointer_missing`
- `rendered_registry_drift`

## 6. Relation To The Broader Configuration-Source Architecture

This contract family should sit inside the shell's config architecture exactly as follows.

### 6.1 Constitutional source

`AGENTS.md` defines:

- which offices exist
- what burdens they carry
- which harness labels are certified

It does not carry current machine-binding facts for every office.

### 6.2 Canonical office-local source

`OFFICE-HARNESS-METADATA.v1.yaml` carries current office-binding facts because the office is the durable constitutional unit and the binding is its mutable operating attachment.

This is the key anti-drift move:

- do not encode binding truth in folder names
- do not encode binding truth only in root veneers
- do not encode binding truth only in runtime memory or exocortex state

### 6.3 Rendered read model

`office-harness-bindings.effective.json` is the cross-office query surface.

It exists so operators, dashboards, CI, or ontology projections can answer:

- which harness is each office on now
- which office changed binding
- which bindings are missing required facts

But it remains rendered, not sovereign.

### 6.4 Ledger layer

`office-harness-binding-ledger.jsonl` preserves rebinding history.

This is the correct place for harness churn evidence because churn is temporal state, not office identity.

### 6.5 Projection layer

Exocortex and ontology may project office-harness data for routing or query, but they may not redefine office meaning or silently become the only source of binding law.

That is the direct application of the control-plane sovereignty contract to office-harness state.

## 7. Ordered Write Set That Should Exist Next

The next write set should be:

1. `orchestration/state/impl/OFFICE-HARNESS-BINDING-CONTRACT-v1.md`
2. `offices/commander/platform/contracts/OFFICE-HARNESS-METADATA.v1.yaml`
3. `offices/ajna/platform/contracts/OFFICE-HARNESS-METADATA.v1.yaml`
4. `offices/psyche/platform/contracts/OFFICE-HARNESS-METADATA.v1.yaml`
5. `offices/adjudicator/platform/contracts/OFFICE-HARNESS-METADATA.v1.yaml`
6. `offices/cartographer/platform/contracts/OFFICE-HARNESS-METADATA.v1.yaml`
7. `operators/validators/validate_office_harness_coherence.py`
8. `orchestration/state/registry/office-harness-bindings.effective.json`
9. `orchestration/state/registry/office-harness-binding-ledger.jsonl`
10. `orchestration/state/OFFICE-HARNESS-COHERENCE-REPORT.json`
11. `orchestration/state/OFFICE-HARNESS-COHERENCE-REPORT.md`
12. `Makefile` target addition for `check-office-harness-coherence`

## 8. Net Decision

The shell should not rename offices around harness churn.

It should ratify a compact office-harness binding law, store current binding facts in one per-office contract, render a cross-office effective registry from those contracts, record rebinding history in a ledger, and enforce coherence through a report-first validator that later becomes strict.

That gives the shell exactly what it needs:

- durable office identity
- explicit mutable harness binding
- machine-checkable coherence
- lawful source precedence
- control-plane and ontology projections without hidden sovereignty

## Status

`complete`

`git diff --check` was run after writing this artifact and returned clean.
