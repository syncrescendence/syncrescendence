# Config-Surface Chat-CI Widening Contract v1

**Status**: live-v1
**Class**: implementation law
**Purpose**: define the first narrow lawful outwardization path for `config_surface_state` through `chat_ci` while keeping the path repo-sovereign, derivative, manual, and explicitly non-automated

## Compact Contract

- `config_surface_state` may widen outward only through the existing repo-resident `chat_ci` derivative stack: `cfgs-013`, `cfgs-018`, and `cfgs-019`
- the lawful v1 outward act is human manual export from a repo-derived pack into a named provider surface, optionally preceded or followed by a repo-resident readiness or receipt artifact
- the config kernel, rematerialization law, ledger, and current-state pair remain sovereign; provider UIs are downstream targets only
- readiness and receipt artifacts are evidence of packing or manual export, not new constitutions and not a second source of truth
- widening artifacts inherit the shared projection sovereignty envelope from `PROJECTION-FAMILY-SOVEREIGNTY-NORMALIZATION-v1.md`
- no automation, provider API sync, browser control, scraping, or hidden local export cache is allowed

## 1. Narrow Scope

The v1 widening path is limited to `chat_ci` only.

Its lawful target set is the provider set already ratified in `CHAT-CI-PROVIDER-PROFILES-v1.json` and `CHAT-CI-PROJECTION-PACK-v1.json`:

- `chatgpt`
- `claude`
- `grok`
- `gemini_web_app`
- `gemini_ai_studio`

Additional scope rules:

- a provider is eligible only if its provider-profile row is `projection_ready`
- a provider pack row is eligible only if its state is `projection_ready_manual_export_only`
- the path may carry only custom-instruction or saved-context payloads that are already expressible through the current `chat_ci` profiles and slot packs
- this contract does not widen to API system prompts, harness constitutions, exocortex projection families, browser automation, or provider surfaces not already named in the ratified provider-profile registry

## 2. Existing Surfaces This Path Must Bind To

This path must bind upward to the current config kernel and proof chain:

1. `knowledge/sigma/CHAT-APP-CUSTOM-INSTRUCTION-ARCHITECTURE-v1.md`
2. `knowledge/sigma/CONFIG-BEHAVIOR-ATOMS-AND-SURFACE-PROFILES-v1.md`
3. `knowledge/sigma/CONFIG-SOURCE-OF-TRUTH-ARCHITECTURE-v1.md`
4. `orchestration/state/impl/CONFIG-SURFACE-LEDGER-REMATERIALIZATION-v1.md`
5. `orchestration/state/registry/config-surface-state-ledger.jsonl`
6. `orchestration/state/registry/CONFIG-SURFACE-REGISTRY-v1.json`
7. `orchestration/state/registry/CONFIG-SURFACE-PROJECTION-MATRIX-v1.json`

It must bind downward only to the current `chat_ci` derivative surfaces:

- `cfgs-013` -> `orchestration/state/registry/CHAT-CI-RENDER-SURFACE-v1.md`
- `cfgs-018` -> `orchestration/state/registry/CHAT-CI-PROVIDER-PROFILES-v1.json`
- `cfgs-019` -> `orchestration/state/registry/CHAT-CI-PROJECTION-PACK-v1.json`

Any future readiness or receipt family for this widening path may join only to provider IDs, slot IDs, pack unit IDs, and omission discipline already named in those three artifacts.
It must not introduce a second provider taxonomy, alternative slot map, or hidden packing registry.

## 3. Lawful Widening Path

`config_surface_state` may widen outward through `chat_ci` only by the following ordered path:

1. read the rematerialized current-state pair for `config_surface_state` from `CONFIG-SURFACE-REGISTRY-v1.json` and `CONFIG-SURFACE-PROJECTION-MATRIX-v1.json`
2. resolve the `chat_ci` surface class and its concrete surfaces `cfgs-013`, `cfgs-018`, and `cfgs-019`
3. select one eligible provider row from `CHAT-CI-PROVIDER-PROFILES-v1.json` and one matching manual-export-only pack row from `CHAT-CI-PROJECTION-PACK-v1.json`
4. derive the provider-scoped payload in repo form using the render surface, profile slot model, pack-unit assignments, and the existing AF priority order
5. declare any compression or omission in repo-resident readiness or receipt state before a human relies on the packed payload
6. a human may manually copy the repo-derived payload into the named provider UI
7. if that manual act needs auditability, the repo records a readiness artifact or append-only receipt that points back to the exact repo-derived payload and its source surfaces

No other widening path is lawful in v1.

## 4. Source-Of-Truth Discipline

The precedence chain for this widening path is:

1. Sigma config kernel doctrine
2. config-surface rematerialization law
3. config-surface append-only ledger
4. rematerialized current-state pair
5. `chat_ci` render, provider-profile, and pack surfaces
6. future `chat_ci` readiness or manual-export receipt artifacts
7. provider UI state reached by human copy

Consequences:

- provider-local text may reflect repo law, but it does not outrank repo law
- a receipt may attest that a human copied a repo-derived payload, but it may not redefine atom families, slot law, or provider packing rules
- if provider-local content drifts, repair must happen by editing the repo sources and issuing a new readiness or receipt event, not by treating the provider UI as the hidden canonical copy
- no consumer may infer new constitutional behavior from provider-local wording that is absent from the repo-native surfaces

## 5. Required Envelope For Future Readiness Or Receipt Artifacts

The first lawful outwardization family may be either:

- a repo-resident readiness surface that says a specific provider pack is ready for manual export
- an append-only manual-export receipt family that records a specific human copy event

Either shape must carry at least:

- `schema_version`
- `family_id`
- `projection_governance`
- `provider_id`
- `provider_surface`
- `source_surface_class`
- `source_surface_ids`
- `source_config_state_version` or `source_event_id`
- `pack_unit_ids`
- `slot_ids`
- `omission_declarations`
- `payload_sha256` or per-slot digests
- `manual_operation_state`
- `actor`
- `recorded_at`

Field law:

- `projection_governance.shared_contract_path` is `orchestration/state/impl/PROJECTION-FAMILY-SOVEREIGNTY-NORMALIZATION-v1.md`
- `projection_governance.sovereignty_rule` is `repo_ratifies_exocortex_coordinates_projection_derives`
- `projection_governance.capture_policy` is `manual_export_only`
- `projection_governance.reliance_ceiling` is `informative_only_until_receipted_export`
- `projection_governance.hidden_second_control_plane` is `prohibited`
- `source_surface_class` is always `chat_ci`
- `source_surface_ids` must point back to `cfgs-013`, `cfgs-018`, and `cfgs-019`
- `manual_operation_state` may distinguish `ready_for_manual_export` from `manually_exported`, but it may not imply automated sync, live provider introspection, or runtime enforcement
- hashes bind to repo-derived payload bytes, not provider-scraped bytes
- provider-local screenshots, UI IDs, or browser-state captures are optional witness only and may not become the only operative record

## 6. Forbidden Drift

The following are forbidden in v1:

- automated export into provider UIs
- browser scripting, UI macros, MCP control, or API writes that claim to perform the export
- maintaining a hidden local folder, note, or clipboard cache as the real packing source
- inventing provider-specific behavior law outside the config kernel, `cfgs-018`, or `cfgs-019`
- treating a readiness or receipt artifact as if it were the new chat constitution
- using provider-side state as the only place where current packed text can be reconstructed

## 7. Current Effect

This contract is immediately binding on:

- any future `chat_ci` export-readiness or manual-export receipt family
- any pack emitter, checklist, or report that claims lawful `config_surface_state` outwardization through `chat_ci`
- any future validator for that family

This contract does not:

- promote provider automation
- create a second hidden source of truth
- by itself change `config_surface_state` beyond `phase1_repo_proof`

Until later repo law widens it further, `config_surface_state` may move outward through `chat_ci` only as a repo-sovereign, derivative, manual-export or receipt-governed path.
