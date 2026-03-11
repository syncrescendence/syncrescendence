# Office-Harness Exocortex Projection Contract v1

**Status**: live-v1
**Class**: implementation law
**Purpose**: define the first narrow exocortex-facing derivative family for office-harness state without inventing a second hidden topology

## Compact Contract

- the first office-harness exocortex projection is a narrow derivative family over runtime offices only
- repo ratifies office identity and binding
- exocortex-facing rows are derivative and pointer-carrying, not sovereign
- projected rows may join only to already-ratified exocortex and control-plane surfaces
- the family must be rebuildable from repo-native proof state

## 1. Narrow Family Scope

The v1 family is:

- `office-harness-exocortex-projection/v1`

Its lawful scope is limited to office-harness effective rows that are:

- `surface_class: persistent-runtime`
- `harness_family: openclaw`

Under current repo state, that means:

- `ajna`
- `psyche`

This contract does not yet widen to:

- repo-native coding harnesses
- sensing-only harnesses
- provisional stage0 surfaces
- any office or harness that lacks a ratified mapping into the existing exocortex surface registry family

## 2. Existing Surfaces This Family Must Bind To

This family must bind to the already-ratified exocortex and control-plane surfaces:

1. `orchestration/state/registry/office-harness-bindings.effective.json`
2. `orchestration/state/EXOCORTEX-SURFACE-REGISTRY-CC90.json`
3. `orchestration/state/EXOCORTEX-TELEOLOGY-REGISTRY-CC90.json`
4. `orchestration/state/EXOCORTEX-CONTROL-PLANE-STATUS-CC91.json`

It may also rely on the higher-precedence proof chain behind the effective registry:

1. `AGENTS.md`
2. `orchestration/state/impl/OFFICE-HARNESS-BINDING-CONTRACT-v1.md`
3. `orchestration/state/impl/OFFICE-HARNESS-LEDGER-REMATERIALIZATION-v1.md`
4. `orchestration/state/registry/office-harness-binding-ledger.jsonl`
5. per-office `OFFICE-HARNESS-METADATA.v1.yaml`

The projection family is lawful only if it remains a derivative join across those existing surfaces.

It must not invent:

- office-local exocortex IDs
- hidden runtime classes
- unofficial provider slugs
- second control-plane status families
- machine-specific topology that exists nowhere in repo law

## 3. Ratified Join Rule

The join from runtime office binding to exocortex surface must be explicit and narrow.

The v1 provider mapping is:

| Source provider | Required projected surface slug |
|---|---|
| `anthropic` | `claude_anthropic_surface` |
| `openai-codex` | `chatgpt_openai_surface` |

Rules:

1. `projected_surface_slug` must be resolved from this ratified mapping, not guessed from office title, avatar label, machine name, or harness label.
2. The resolved slug must exist in both `EXOCORTEX-SURFACE-REGISTRY-CC90.json` and `EXOCORTEX-TELEOLOGY-REGISTRY-CC90.json`.
3. The projected row may copy surface facts already present in those artifacts, but may not rename, merge, or specialize the surface.
4. If no ratified mapping exists for a source row, the row is blocked from operative projection until repo law adds that mapping.
5. `EXOCORTEX-CONTROL-PLANE-STATUS-CC91.json` may be cited only as the current control-plane status artifact for this family; it must not be reinterpreted into office-specific readiness law.

## 4. Required Projection Envelope

The first emitted current-state artifact for this family should be a single repo-resident control-plane surface:

- `orchestration/state/EXOCORTEX-OFFICE-HARNESS-PROJECTION-CC92.json`

Its minimum top-level fields must be:

- `schema_version`
- `projection_family`
- `projection_scope`
- `projection_contract_path`
- `source_effective_registry_path`
- `source_surface_registry_path`
- `source_teleology_registry_path`
- `source_control_plane_status_path`
- `rows`

Required values:

- `schema_version: office-harness-exocortex-projection/v1`
- `projection_family: office_harness_exocortex_projection`
- `projection_scope: persistent-runtime-openclaw-offices`
- `projection_contract_path: orchestration/state/impl/OFFICE-HARNESS-EXOCORTEX-PROJECTION-CONTRACT-v1.md`

## 4A. Append-Only Snapshot Receipt History

If this family keeps repo-native mutation history, that history must remain an append-only receipt ledger over derivative snapshots rather than a second sovereign state family.

The v1 receipt surface is:

- `orchestration/state/registry/office-harness-exocortex-projection-ledger.jsonl`

Receipt-law obligations:

1. Each event must point back to the same repo-native proof inputs named by this contract.
2. Each event must carry the emitted projection digest so snapshot drift is auditable without hand comparison.
3. The ledger may record snapshot refresh history, but it must not become the only place where current projected meaning lives.
4. New receipt events must append; corrections arrive as later receipt events rather than line edits.
5. The receipt ledger does not outrank the current-state projection artifact, the effective office-harness registry, or the higher-precedence proof chain behind them.

## 5. Required Row Fields

Each projected row must carry the minimum binding identity, exocortex join, and pointer family.

Required row fields:

- `office_id`
- `office_title`
- `primary_harness`
- `harness_family`
- `surface_class`
- `provider`
- `model`
- `machine`
- `account_ref`
- `binding_state`
- `contract_state`
- `validator_state`
- `authority_state`
- `metadata_path`
- `source_effective_registry_path`
- `projected_surface_slug`
- `projected_surface_service`
- `projected_surface_class`
- `projected_surface_ontology_entity_id`
- `projected_surface_proper_role`
- `projected_surface_anti_role`
- `control_plane_status_path`
- `control_plane_status_version`
- `projection_state`
- `allowed_reliance`
- `ratification_pointer`
- `ratified_by_artifact_path`
- `ratified_by_artifact_id`
- `ratified_at`

Field law:

1. Office and binding fields must be copied from the effective registry or its higher-precedence rematerialized source, not rewritten.
2. `projected_surface_*` fields must be copied from the CC90 surface and teleology registries.
3. `control_plane_status_path` and `control_plane_status_version` must point back to the CC91 control-plane artifact rather than flattening that artifact into new office-local status law.
4. The ratification pointer family must be copied from the source office-harness binding row so downstream consumers can trace authority back to repo law.
5. The row may add no hidden semantic fields beyond those ratified here.

## 6. Derivative-Only Obligations

This family is a projection, not a sovereign registry.

Minimum obligations:

1. No projected row may be hand-authored.
2. No projected row may outrank office metadata, ledger history, or the effective registry.
3. No projected row may change office identity, harness identity, provider, model, machine, or account meaning.
4. No projected row may invent a new exocortex relation name or office class.
5. `projection_state` must be `operative` only when:
   - `binding_state` is `active`
   - `contract_state` is `operative`
   - `validator_state` is `clean`
   - `authority_state` is `operative`
   - the mapped surface slug resolves cleanly in both CC90 registries
6. If any of those conditions fail, `projection_state` must be `informative_only` and `allowed_reliance` must also be `informative_only`.
7. Missing joins, missing pointers, or source drift must be reported in a report or audit surface rather than patched silently in the projection rows.

## 7. Rebuildability From Repo-Native Proof State

The family must be rebuildable without:

- exocortex API calls
- hidden local caches
- OpenClaw workspace inspection
- browser scraping
- manual repair of projected rows

The deterministic rebuild chain is:

1. rebuild `office-harness-bindings.effective.json` from `office-harness-binding-ledger.jsonl` if needed
2. select source rows matching the v1 scope
3. resolve `projected_surface_slug` by the ratified provider mapping in this contract
4. join the resolved slug against `EXOCORTEX-SURFACE-REGISTRY-CC90.json`
5. join the same slug against `EXOCORTEX-TELEOLOGY-REGISTRY-CC90.json`
6. attach the control-plane artifact reference from `EXOCORTEX-CONTROL-PLANE-STATUS-CC91.json`
7. copy the source row's ratification pointer family unchanged
8. sort projected rows by federal office order from `AGENTS.md`

Renderer-time timestamps do not belong in the current-state projection artifact.
If timing, freshness, or join failures need to be reported, they belong in a separate report or audit surface.

## 8. Forbidden Drift

The following are forbidden in v1:

- projecting all offices before lawful mappings exist
- treating provider names as free-form exocortex slugs
- creating a separate office-harness control plane outside the CC90 or CC91 families
- using runtime-local OpenClaw state as the only source of projected truth
- allowing the projection artifact to become the only place where office-to-exocortex attachment can be discovered

## 9. Current Effect

This contract is immediately binding on:

- the first office-harness exocortex projection artifact for runtime offices
- the append-only snapshot receipt ledger for that projection family
- any bridge that emits that artifact
- any report or audit surface that claims to validate that projection

Until widened by later repo law, the family remains intentionally narrow.
