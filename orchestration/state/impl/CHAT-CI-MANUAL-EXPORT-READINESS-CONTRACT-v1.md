# Chat-CI Manual Export Readiness Contract v1

**Status**: live-v1
**Class**: implementation law
**Purpose**: define the first narrow lawful outwardization family for `chat_ci` without creating vendor automation, hidden control planes, or a second source of truth

## Compact Rule

- repo truth for `chat_ci` still lives in Sigma doctrine, the config-surface proof family, and the repo-native `chat_ci` render and packing surfaces
- manual export readiness is derivative of that proof state and may not outrank it
- provider UIs remain non-sovereign runtime destinations, not constitutional storage
- readiness and later copy evidence must arrive as append-only receipts, never as hidden automation
- readiness artifacts inherit the shared projection sovereignty envelope from `PROJECTION-FAMILY-SOVEREIGNTY-NORMALIZATION-v1.md`

This contract governs:

- `orchestration/state/registry/CHAT-CI-MANUAL-EXPORT-READINESS-v1.json`
- `orchestration/state/registry/chat-ci-manual-export-ledger.jsonl`
- `operators/validators/validate_chat_ci_manual_export_readiness.py`

## 1. Lawful Inputs

The readiness family is derivative of:

1. `knowledge/sigma/CHAT-APP-CUSTOM-INSTRUCTION-ARCHITECTURE-v1.md`
2. `knowledge/sigma/CONFIG-BEHAVIOR-ATOMS-AND-SURFACE-PROFILES-v1.md`
3. `knowledge/sigma/CONFIG-SOURCE-OF-TRUTH-ARCHITECTURE-v1.md`
4. `orchestration/state/registry/CONFIG-SURFACE-REGISTRY-v1.json`
5. `orchestration/state/registry/CONFIG-SURFACE-PROJECTION-MATRIX-v1.json`
6. `orchestration/state/registry/CHAT-CI-RENDER-SURFACE-v1.md`
7. `orchestration/state/registry/CHAT-CI-PROVIDER-PROFILES-v1.json`
8. `orchestration/state/registry/CHAT-CI-PROJECTION-PACK-v1.json`

No provider-local edit, browser state, or vendor-hosted field may outrank those repo artifacts.

## 2. Readiness Family Shape

The first lawful family is intentionally narrow:

- one current-state readiness record
- one append-only ledger
- one report-first validator

The readiness record states whether each provider surface is ready for a human to copy a derivative pack manually.
It does not claim that a copy has already occurred.
The readiness record must carry:

- `projection_governance.shared_contract_path: orchestration/state/impl/PROJECTION-FAMILY-SOVEREIGNTY-NORMALIZATION-v1.md`
- `projection_governance.sovereignty_rule: repo_ratifies_exocortex_coordinates_projection_derives`
- `projection_governance.capture_policy: manual_export_only`
- `projection_governance.reliance_ceiling: informative_only_until_receipted_export`
- `projection_governance.hidden_second_control_plane: prohibited`

The append-only ledger records readiness receipts and later manual-copy receipts if those are ever added.

## 3. Outwardization Constraints

The v1 path is lawful only when all of the following remain true:

- manual export is initiated by a human
- no provider API write is performed by repo code
- no browser automation or scripted form fill is performed by repo code
- no vendor-local mutation is treated as durable truth without a new repo receipt
- omissions, compression, or provider-specific repacking remain explicit in repo artifacts

If any provider requires automation, background sync, or hidden field mutation to stay current, that path is out of scope for this family and requires separate ratification.

## 4. Receipt Discipline

Every ledger line is one JSON object.

The first event type set is:

- `readiness_receipt`
- `readiness_refresh`
- `manual_export_receipt`
- `supersession_receipt`

Field law:

- the family id is always `chat_ci_manual_export_state`
- readiness receipts bind to the latest relied-on `config_surface_state` receipt event
- file digests must cover the readiness record, provider profiles, projection pack, and config current-state pair
- repairs and supersessions happen by new ledger lines, never by rewriting prior lines

## 5. Subordination And Replaceability

The precedence chain is:

1. Sigma doctrine
2. `orchestration/state/impl/CHAT-CI-MANUAL-EXPORT-READINESS-CONTRACT-v1.md`
3. `config_surface_state` proof artifacts and receipts
4. `chat-ci-manual-export-ledger.jsonl`
5. `CHAT-CI-MANUAL-EXPORT-READINESS-v1.json`
6. derived reports

Consequences:

- the readiness record is disposable and may be regenerated from lawful repo state
- the ledger is witness and audit substrate, not a sovereign text source
- provider UIs remain downstream effects, not authority-bearing storage

## 6. Validator

The v1 honesty gate is:

- `operators/validators/validate_chat_ci_manual_export_readiness.py`

It checks only repo-resident structure:

- manual-export-only constraints stay explicit
- the shared projection sovereignty envelope stays explicit
- provider ids and pack states stay aligned
- the readiness family stays self-registered in config-surface proof
- the latest readiness ledger event matches the committed repo artifacts
