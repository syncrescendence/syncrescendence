# Response

**Response ID**: `RSP-20260306-registry-artifacts`  
**Surface**: `codex_parallel_session`  
**Date received**: `2026-03-06`  
**Dispatch packet**: `PKT-20260306-codex-swarm-batch-03-lane-01-registry-artifacts`  
**Result state**: `complete`  
**Receipt artifacts**:
- `communications/responses/RESPONSE-CODEX-SWARM-BATCH-03-LANE-01-REGISTRY-ARTIFACTS.md`

## Returned Content

### 1. Patch-ready draft for `orchestration/state/registry/tributary-disposition-schema-v1.md`

```md
# Tributary Disposition Schema v1

**Version**: `v1`  
**Canonical location**: `orchestration/state/registry/tributary-disposition-schema-v1.md`

## Purpose

This schema defines the canonical current-state registry and append-only mutation ledger for tributary artifact disposition.

The contract is:

- one CSV row per source artifact identity
- one JSONL event per meaningful mutation to that row
- receipts, manifests, and promoted artifacts remain separate artifacts joined by explicit fields

Canonical artifacts:

- `orchestration/state/registry/tributary-disposition-schema-v1.md`
- `orchestration/state/registry/tributary-disposition-registry.csv`
- `orchestration/state/registry/tributary-disposition-ledger.jsonl`

## Encoding and serialization

- All three files must be UTF-8 with LF line endings.
- CSV must have a single header row and no embedded newlines in any cell.
- JSONL must contain exactly one JSON object per line with no pretty-print wrapping.
- Repo-relative paths must not begin with `/`.
- The literal token `none` is the only null sentinel for optional string and path fields.
- Timestamps must be ISO-8601 UTC with a trailing `Z`.

## Current-state CSV contract

The CSV column order is normative and must match this exact header:

`candidate_id,schema_version,source_tributary,source_path,source_relpath_hash,artifact_class,artifact_format,lineage_witness,provenance_sensitivity,authority_score,present_relevance,compaction_yield,duplication_status,review_basis,chosen_disposition,destination_lane,destination_artifact_path,archive_manifest_path,receipt_path,external_pointer,merge_family_id,justification,record_state,intake_batch_id,last_action_at,last_action_by,dest_artifact_hash,supersedes_candidate_id,notes`

Field contract:

| Column | Type | Rule |
| --- | --- | --- |
| `candidate_id` | string | Unique row identity. Pattern: `^tdc-[a-z0-9-]+-[0-9]{4}$` |
| `schema_version` | string | Must be `v1` |
| `source_tributary` | enum | `live_shell`, `syncrescendence_old`, `syncrescendence_pre_schematic_design` |
| `source_path` | path | Repo-relative source artifact path |
| `source_relpath_hash` | string | Deterministic `sha256:` hash over normalized tributary plus source path |
| `artifact_class` | enum | `law`, `reference`, `playbook`, `operator`, `executive`, `office_state`, `manifest`, `source`, `log`, `other` |
| `artifact_format` | enum | `md`, `json`, `yaml`, `py`, `sh`, `directory_manifest`, `binary`, `mixed`, `other` |
| `lineage_witness` | string | Witness family or source note. Use `none` if not needed |
| `provenance_sensitivity` | enum | `low`, `medium`, `high`, `restricted` |
| `authority_score` | integer | Integer `0` through `5` |
| `present_relevance` | integer | Integer `0` through `5` |
| `compaction_yield` | integer | Integer `0` through `5` |
| `duplication_status` | enum | `unique`, `duplicate_family`, `superseded`, `derived`, `unknown` |
| `review_basis` | enum | `manual_read`, `family_sample`, `validator_scan`, `merged_adjudication`, `other` |
| `chosen_disposition` | enum | `none`, `promote_live_law`, `promote_sigma`, `promote_sigma_reference`, `promote_playbook`, `promote_operator`, `retain_pedigree_rehoused`, `retain_archive_manifest_only`, `externalize_to_exocortex`, `cull_with_receipt` |
| `destination_lane` | string | Repo-relative lane root or `none` |
| `destination_artifact_path` | path | Repo-relative destination artifact path or `none` |
| `archive_manifest_path` | path | Repo-relative manifest path or `none` |
| `receipt_path` | path | Repo-relative custody receipt path or `none` |
| `external_pointer` | string | External pointer such as `exocortex://...` or `none` |
| `merge_family_id` | string | `mf-...` family id or `none` |
| `justification` | string | Single-line disposition reason |
| `record_state` | enum | `intake_pending`, `triaged`, `adjudicated`, `scheduled`, `executed`, `verified`, `closed`, `exception` |
| `intake_batch_id` | string | Batch or packet identifier that first enrolled the row |
| `last_action_at` | timestamp | Latest mutation time |
| `last_action_by` | string | Latest actor id |
| `dest_artifact_hash` | string | `sha256:` hash of the final destination artifact or `none` |
| `supersedes_candidate_id` | string | Prior row replaced by an intake correction or `none` |
| `notes` | string | Single-line narrow clarification or `none` |

## Controlled state transitions

Allowed forward transitions:

- `intake_pending -> triaged`
- `triaged -> adjudicated`
- `adjudicated -> scheduled`
- `scheduled -> executed`
- `executed -> verified`
- `verified -> closed`

Allowed exception transitions:

- `intake_pending -> exception`
- `triaged -> exception`
- `adjudicated -> exception`
- `scheduled -> exception`
- `executed -> exception`
- `verified -> exception`
- `exception -> triaged`
- `exception -> adjudicated`

Illegal transitions include:

- `triaged -> executed`
- `adjudicated -> verified`
- `closed -> *`

## Disposition requirements

- `promote_live_law`, `promote_sigma`, `promote_sigma_reference`, `promote_playbook`, and `promote_operator` require populated `destination_lane`, `destination_artifact_path`, and `receipt_path` no later than `executed`.
- `retain_pedigree_rehoused` requires `destination_lane=pedigree/rehoused`, populated `destination_artifact_path`, and populated `receipt_path` no later than `executed`.
- `retain_archive_manifest_only` requires populated `archive_manifest_path` and `receipt_path`, with `destination_lane=none` and `destination_artifact_path=none`.
- `externalize_to_exocortex` requires populated `external_pointer` and `receipt_path`, with `destination_lane=none` and `destination_artifact_path=none`.
- `cull_with_receipt` requires populated `receipt_path`, with `destination_lane=none`, `destination_artifact_path=none`, `archive_manifest_path=none`, and `external_pointer=none`.

## Ledger JSONL contract

Each line in `tributary-disposition-ledger.jsonl` must be a JSON object with this shape:

| Key | Type | Rule |
| --- | --- | --- |
| `schema_version` | string | Must be `v1` |
| `event_id` | string | Unique ledger event id. Pattern: `^tdl-[0-9]{8}-[0-9]{4}$` |
| `event_type` | enum | `row_intake`, `row_triaged`, `row_adjudicated`, `row_scheduled`, `row_executed`, `row_verified`, `row_closed`, `row_exception`, `row_corrected` |
| `occurred_at` | timestamp | Event timestamp in UTC |
| `actor` | string | Office, agent, or operator id |
| `candidate_id` | string | Must match an existing or newly-created row id |
| `row_version` | integer | Starts at `1` and increments by `1` for each event for the same `candidate_id` |
| `record_state_before` | string or null | Prior row state |
| `record_state_after` | string | New row state |
| `field_changes` | object | Only mutated fields. Each key maps to `{ "before": <value>, "after": <value> }` |
| `reason` | string | Single-line reason for the mutation |
| `receipt_path` | path | Repo-relative receipt path or `none` |
| `notes` | string | Single-line note or `none` |

Event semantics:

- `field_changes` must only include fields that changed in that event.
- `last_action_at` in the CSV row must equal the latest ledger `occurred_at` for that `candidate_id`.
- `last_action_by` in the CSV row must equal the latest ledger `actor` for that `candidate_id`.
- The latest ledger event for a `candidate_id` must reproduce the CSV row's current `record_state`.
- Intake may create a row in `intake_pending` or `triaged`.
- `row_corrected` is for non-state corrections that still change current-state data and must not delete prior events.

## Minimal invariants

- `candidate_id` is unique in the CSV.
- `source_relpath_hash` is unique in the CSV unless `supersedes_candidate_id` is populated on the newer row.
- Each CSV row represents exactly one source artifact identity.
- Exactly one current `record_state` exists per `candidate_id`.
- `chosen_disposition=none` is allowed only in `intake_pending`, `triaged`, or `exception`.
- `receipt_path` must be populated for all rows in `executed`, `verified`, or `closed`.
- `destination_artifact_path` must be populated for promotion and rehousing dispositions by `executed`.
- `dest_artifact_hash` must be populated for promotion and rehousing dispositions by `verified`.
- `merge_family_id` may be shared across rows, but `candidate_id` may not.
- Ledger history is append-only. Prior ledger lines must never be edited in place.

## Minimal validator checks

1. CSV header matches the normative header exactly.
2. Every enum value is inside its allowed set.
3. Every score is an integer in `0..5`.
4. Every path field is repo-relative or `none`.
5. Every timestamp is parseable UTC ISO-8601 with `Z`.
6. Every `candidate_id` is unique in the CSV.
7. Every `event_id` is unique in the JSONL.
8. `row_version` is contiguous per `candidate_id`.
9. Ledger state transitions are legal under the transition table.
10. Latest ledger state and actor match the CSV row.
11. Disposition-specific required fields are populated by the required state.
12. Rows in `closed` must previously pass through `verified`.
```

### 2. Exact CSV header row and illustrative rows for `tributary-disposition-registry.csv`

```csv
candidate_id,schema_version,source_tributary,source_path,source_relpath_hash,artifact_class,artifact_format,lineage_witness,provenance_sensitivity,authority_score,present_relevance,compaction_yield,duplication_status,review_basis,chosen_disposition,destination_lane,destination_artifact_path,archive_manifest_path,receipt_path,external_pointer,merge_family_id,justification,record_state,intake_batch_id,last_action_at,last_action_by,dest_artifact_hash,supersedes_candidate_id,notes
tdc-old-0001,v1,syncrescendence_old,knowledge/references/duplicate-doctrine-matrix.md,sha256:5f7833d37f1f9f2557d70f610e9e8f8a0af1c70a7ce62c4c1d0f4f2a5e7d910c,reference,md,family:duplicate-doctrine,low,3,5,4,duplicate_family,manual_read,promote_sigma_reference,knowledge/sigma/references,knowledge/sigma/references/duplicate-doctrine-matrix.md,none,pedigree/rehousing-receipts/receipt-tdc-old-0001.md,none,mf-duplicate-doctrine-001,Strong evidence table belongs in Sigma reference housing.,verified,PKT-20260306-codex-swarm-batch-03,2026-03-06T18:21:00Z,codex_swarm.batch03.lane01,sha256:4e1c52eb0f7f829ebf67f2f9c2f2f1fd4e073c4cdb8877cb7eb3e6ae246e11aa,none,Merge family remains explicit.
tdc-pre-schematic-0002,v1,syncrescendence_pre_schematic_design,logs/discovery-session-2024-09-18.md,sha256:8af55c6fb2a134b7e4a94af0ad1a2fbf6bd9fce65e5f4acb88e9f60450a41dd1,log,md,none,medium,1,1,2,unique,manual_read,retain_archive_manifest_only,none,none,pedigree/archive-manifests/manifest-batch03-001.md,pedigree/rehousing-receipts/receipt-tdc-pre-schematic-0002.md,none,none,Preserve provenance only without live promotion.,executed,PKT-20260306-codex-swarm-batch-03,2026-03-06T18:24:00Z,codex_swarm.batch03.lane01,none,none,Awaiting final verification pass.
tdc-live-shell-0003,v1,live_shell,raw_exports/ontology-dump-2025-01-14.json,sha256:7f2c9071f14b28f8810c2914346b613a2ca20aa693f912847d7762ee76e0ff1f,source,json,none,restricted,0,1,5,derived,validator_scan,externalize_to_exocortex,none,none,none,pedigree/rehousing-receipts/receipt-tdc-live-shell-0003.md,exocortex://tributaries/live-shell/ontology-dump-2025-01-14.json,none,Bounded machine export moved out of repo after classification.,verified,PKT-20260306-codex-swarm-batch-03,2026-03-06T18:29:00Z,codex_swarm.batch03.lane01,none,none,External pointer is authoritative for retained access.
```

### 3. Exact JSONL event examples for `tributary-disposition-ledger.jsonl`

```jsonl
{"schema_version":"v1","event_id":"tdl-20260306-0001","event_type":"row_intake","occurred_at":"2026-03-06T18:05:00Z","actor":"codex_swarm.batch03.lane01","candidate_id":"tdc-old-0001","row_version":1,"record_state_before":null,"record_state_after":"triaged","field_changes":{"candidate_id":{"before":null,"after":"tdc-old-0001"},"source_tributary":{"before":null,"after":"syncrescendence_old"},"source_path":{"before":null,"after":"knowledge/references/duplicate-doctrine-matrix.md"},"artifact_class":{"before":null,"after":"reference"},"duplication_status":{"before":null,"after":"duplicate_family"},"review_basis":{"before":null,"after":"manual_read"},"merge_family_id":{"before":null,"after":"mf-duplicate-doctrine-001"},"justification":{"before":null,"after":"Family witness retained until merge decision is final."},"last_action_at":{"before":null,"after":"2026-03-06T18:05:00Z"},"last_action_by":{"before":null,"after":"codex_swarm.batch03.lane01"}},"reason":"Initial intake and triage.","receipt_path":"none","notes":"none"}
{"schema_version":"v1","event_id":"tdl-20260306-0002","event_type":"row_adjudicated","occurred_at":"2026-03-06T18:13:00Z","actor":"codex_swarm.batch03.lane01","candidate_id":"tdc-old-0001","row_version":2,"record_state_before":"triaged","record_state_after":"adjudicated","field_changes":{"chosen_disposition":{"before":"none","after":"promote_sigma_reference"},"destination_lane":{"before":"none","after":"knowledge/sigma/references"},"destination_artifact_path":{"before":"none","after":"knowledge/sigma/references/duplicate-doctrine-matrix.md"},"receipt_path":{"before":"none","after":"pedigree/rehousing-receipts/receipt-tdc-old-0001.md"},"justification":{"before":"Family witness retained until merge decision is final.","after":"Strong evidence table belongs in Sigma reference housing."},"last_action_at":{"before":"2026-03-06T18:05:00Z","after":"2026-03-06T18:13:00Z"},"last_action_by":{"before":"codex_swarm.batch03.lane01","after":"codex_swarm.batch03.lane01"}},"reason":"Disposition settled after family comparison.","receipt_path":"pedigree/rehousing-receipts/receipt-tdc-old-0001.md","notes":"Merge family remains explicit."}
{"schema_version":"v1","event_id":"tdl-20260306-0003","event_type":"row_executed","occurred_at":"2026-03-06T18:24:00Z","actor":"codex_swarm.batch03.lane01","candidate_id":"tdc-pre-schematic-0002","row_version":3,"record_state_before":"scheduled","record_state_after":"executed","field_changes":{"archive_manifest_path":{"before":"none","after":"pedigree/archive-manifests/manifest-batch03-001.md"},"receipt_path":{"before":"none","after":"pedigree/rehousing-receipts/receipt-tdc-pre-schematic-0002.md"},"last_action_at":{"before":"2026-03-06T18:17:00Z","after":"2026-03-06T18:24:00Z"},"last_action_by":{"before":"migration_coordinator","after":"codex_swarm.batch03.lane01"}},"reason":"Manifest and custody receipt written.","receipt_path":"pedigree/rehousing-receipts/receipt-tdc-pre-schematic-0002.md","notes":"Awaiting final verification pass."}
{"schema_version":"v1","event_id":"tdl-20260306-0004","event_type":"row_verified","occurred_at":"2026-03-06T18:29:00Z","actor":"codex_swarm.batch03.lane01","candidate_id":"tdc-live-shell-0003","row_version":4,"record_state_before":"executed","record_state_after":"verified","field_changes":{"external_pointer":{"before":"exocortex://tributaries/live-shell/ontology-dump-2025-01-14.pending","after":"exocortex://tributaries/live-shell/ontology-dump-2025-01-14.json"},"receipt_path":{"before":"pedigree/rehousing-receipts/receipt-tdc-live-shell-0003-draft.md","after":"pedigree/rehousing-receipts/receipt-tdc-live-shell-0003.md"},"last_action_at":{"before":"2026-03-06T18:26:00Z","after":"2026-03-06T18:29:00Z"},"last_action_by":{"before":"migration_coordinator","after":"codex_swarm.batch03.lane01"}},"reason":"External pointer and receipt were verified against the control plane.","receipt_path":"pedigree/rehousing-receipts/receipt-tdc-live-shell-0003.md","notes":"External pointer is authoritative for retained access."}
```

### 4. Minimal invariants and validator checks

Minimal invariants:

- The CSV is the only canonical current-state surface.
- The JSONL ledger is append-only and never rewritten in place.
- One CSV row maps to one source artifact identity.
- `candidate_id` and `event_id` are globally unique in their respective files.
- `chosen_disposition` may be `none` only before adjudication or during an exception.
- `receipt_path` is mandatory for every row at `executed`, `verified`, or `closed`.
- Promotion and rehousing outcomes require destination path material by `executed` and destination hash by `verified`.
- Manifest-only and externalized outcomes must keep `destination_lane=none` and `destination_artifact_path=none`.
- Closed rows must have passed through `verified`.

Minimal validator checks:

1. Header equality check against the exact normative CSV header.
2. Enum membership check for every controlled field.
3. Range check for `authority_score`, `present_relevance`, and `compaction_yield`.
4. Regex check for `candidate_id`, `event_id`, timestamps, and `sha256:` fields.
5. Path-form check that repo paths are relative and external pointers use a non-file scheme.
6. Uniqueness check for `candidate_id`, `source_relpath_hash`, and `event_id`.
7. Contiguous `row_version` check per `candidate_id`.
8. Legal state transition check over ledger history.
9. Cross-file parity check that the latest ledger mutation reproduces the CSV row's `record_state`, `last_action_at`, and `last_action_by`.
10. Disposition-field obligation check keyed by both `chosen_disposition` and `record_state`.

### 5. Top failure modes if implemented sloppily

- Free-text enums or blank optional fields will cause silent drift and make validator enforcement impossible.
- Reusing one row for multiple source artifacts will destroy pedigree and make merge disputes unrecoverable.
- Allowing direct `triaged -> executed` jumps will erase adjudication visibility and bury disputed decisions.
- Treating receipts as optional will create unprovable culls, externalizations, and rehousing claims.
- Rewriting ledger history instead of appending corrections will destroy mutation traceability and invite retroactive laundering.
- Mixing absolute paths, repo-relative paths, and external pointers in the same field will break joins and downstream tooling.
- Letting destination artifacts stand in for the registry will collapse current-state authority and provenance into one mutable surface.
