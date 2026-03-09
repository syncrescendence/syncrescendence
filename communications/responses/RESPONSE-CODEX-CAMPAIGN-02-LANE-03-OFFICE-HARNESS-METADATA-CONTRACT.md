# Response

**Response ID**: `RSP-20260309-office-harness-metadata-contract`
**Surface**: `codex_parallel_session`
**Date**: `2026-03-09`
**Date received**: `2026-03-09`
**Dispatch packet**: `communications/prompts/PACKET-CODEX-CAMPAIGN-02-LANE-03-OFFICE-HARNESS-METADATA-CONTRACT.md`
**Result state**: `complete`
**Observed**: office law is ratified, Commander already has the deepest local contract surface, and Ajna/Psyche carry the heaviest harness-specific burden through OpenClaw while Adjudicator and Cartographer remain thinner office-local shells.
**Receipt artifacts**:
  - `communications/responses/RESPONSE-CODEX-CAMPAIGN-02-LANE-03-OFFICE-HARNESS-METADATA-CONTRACT.md`

## Returned Content

The first office-to-harness metadata contract should be a single per-office file at:

- `offices/<office>/platform/contracts/OFFICE-HARNESS-METADATA.v1.yaml`

This keeps office identity path-stable while making current harness binding explicit and machine-checkable.

### 1. Contract Purpose

The contract exists to answer, without inference:

- which federal office this directory is
- which harness is currently bound to it
- what machine and auth mode carry that binding
- what playbook and runtime surfaces govern that binding
- which lanes the office may promote into

It must never contain secrets, raw tokens, cookies, or hidden sovereign state.

### 2. Contract Shape

```yaml
schema_version: office-harness-metadata/v1
office_id: ajna
office_title: Ajna
office_epithet: Strategos
federal_role: strategic-office
office_root: /Users/system/syncrescendence/offices/ajna
playbook_path: /Users/system/syncrescendence/playbooks/ajna/PLAYBOOK.md
binding:
  primary_harness: openclaw_macbook_air
  harness_family: openclaw
  provider: anthropic
  model: claude-sonnet-4-5
  machine: macbook-air
  auth_mode: setup-token
  account_ref: claude-subscription
  avatar_label: Ajna
runtime:
  surface_class: persistent-runtime
  capabilities:
    - browser
    - exocortex
    - relay-mediated
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
    - /Users/system/syncrescendence/playbooks/openclaw/PLAYBOOK.md
  required_local_paths:
    - inbox
    - memory
    - outbox
    - platform/contracts
status:
  binding_state: active
  contract_state: minimum
  last_verified_on: 2026-03-09
```

### 3. Required Fields

- `schema_version`: fixed contract identifier.
- `office_id`: stable filesystem identity; never derived from harness names.
- `office_title`, `office_epithet`, `federal_role`: office identity and burden.
- `office_root`, `playbook_path`: join points to live repo truth.
- `binding.primary_harness`: current harness binding.
- `binding.harness_family`: stable family label for grouped validator logic.
- `binding.provider`, `binding.model`, `binding.machine`, `binding.auth_mode`, `binding.account_ref`: operational binding facts, but no secrets.
- `binding.avatar_label`: symbolic routing label only.
- `runtime.surface_class`, `runtime.capabilities`: declared native grain.
- `promotion.may_promote_to`, `promotion.local_only_classes`: promotion law made explicit.
- `coherence.required_sources`, `coherence.required_local_paths`: validator targets.
- `status.binding_state`, `status.contract_state`, `status.last_verified_on`: rollout and verification state.

### 4. Binding Rules

- One live contract per federal office.
- Office folders never rename when harness bindings change.
- `primary_harness` must align with the live avatar registry in `AGENTS.md`.
- `account_ref` is a descriptive handle, not a credential.
- OpenClaw-bound offices must declare machine and auth mode explicitly.
- Contracts are minimum operational truth, not narrative essays.

### 5. First Rollout Order

#### 5.1 Ajna and Psyche first

These two offices should reach minimum contract depth first because they carry the most runtime-specific burden today.

Minimum for both:

- `OFFICE-HARNESS-METADATA.v1.yaml`
- OpenClaw-specific receipt/result/event notes under `platform/contracts/`
- explicit machine, provider, auth-mode, and runtime-surface declaration
- explicit promotion boundary between office-local runtime state and promoted repo truth

Initial binding expectations:

- `ajna -> openclaw_macbook_air`
- `psyche -> openclaw_mac_mini`

#### 5.2 Adjudicator and Cartographer second

After Ajna and Psyche are stable, bring Adjudicator and Cartographer to the same minimum contract depth:

- `adjudicator -> codex`
- `cartographer -> gemini_cli`

Minimum means:

- the same metadata contract file
- the same required local-path declarations
- the same promotion metadata
- office-specific template parity at least matching Commander's artifact-shape minimum

Commander is already the baseline reference because it has the strongest local contract/template physicalization today.

## 6. First Office/Harness Coherence Validator Plan

The first validator should be:

- `operators/validators/validate_office_harness_coherence.py`

It should start in report-only mode and emit:

- `orchestration/state/OFFICE-HARNESS-COHERENCE-REPORT.json`
- `orchestration/state/OFFICE-HARNESS-COHERENCE-REPORT.md`

### 6.1 Phase 1 checks

- all five federal offices exist under `offices/`
- each office has a matching office playbook
- each targeted office has `platform/contracts/OFFICE-HARNESS-METADATA.v1.yaml`
- `office_id` matches the folder name
- `office_root` and `playbook_path` resolve to real paths
- `primary_harness` is one of the certified live harness labels
- office-to-harness pairing matches current federal law:
  - `commander -> claude_code`
  - `adjudicator -> codex`
  - `cartographer -> gemini_cli`
  - `ajna -> openclaw_macbook_air`
  - `psyche -> openclaw_mac_mini`
- OpenClaw offices declare `machine`, `provider`, and `auth_mode`
- required local paths exist
- no obvious secret material appears in the metadata file

### 6.2 Phase 2 checks

- `required_sources` paths exist and mention the office/harness pair
- office playbook and metadata do not contradict each other on role or surface class
- promotion declarations stay inside lawful federal lanes
- stage0 surfaces do not appear as federal offices

### 6.3 Enforcement path

Rollout should be:

1. report-only while Ajna and Psyche contracts are added
2. expand report-only coverage to Adjudicator and Cartographer
3. add `--strict` once all four offices pass cleanly
4. add a Make target such as `make check-office-harness-coherence`

### 6.4 Failure classes

The validator should classify findings at minimum as:

- `missing_contract`
- `path_mismatch`
- `illegal_harness_binding`
- `missing_runtime_binding_fact`
- `promotion_scope_drift`
- `secret_like_material`
- `playbook_contract_contradiction`

## 7. Net Decision

The first contract should be a small typed YAML file per office, not a new registry lane and not a harness-named directory scheme.

The first validator should enforce office identity, harness binding legality, and minimum operational completeness in report-only mode first.

The correct execution sequence is:

1. Ajna minimum
2. Psyche minimum
3. Adjudicator minimum
4. Cartographer minimum
5. strict validator after all four are clean

## 8. `git diff --check`

`git diff --check` ran clean after this response write. No other file edits were required for this packet.

## Status

`complete`
