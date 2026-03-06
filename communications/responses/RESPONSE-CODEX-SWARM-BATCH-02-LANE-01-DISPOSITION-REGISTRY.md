# Response

**Response ID**: `RSP-20260306-disposition-registry`
**Surface**: `codex_parallel_session`
**Date received**: `2026-03-06`
**Dispatch packet**: `communications/prompts/PACKET-CODEX-SWARM-BATCH-02-LANE-01-DISPOSITION-REGISTRY.md`
**Result state**: `complete`
**Receipt artifacts**:
  - `communications/responses/RESPONSE-CODEX-SWARM-BATCH-02-LANE-01-DISPOSITION-REGISTRY.md`

## Returned Content

### 1. Recommended canonical file location

Recommended canonical registry location:

- `/Users/system/syncrescendence/orchestration/state/registry/tributary-disposition-registry.csv`

Recommended companion ledger and schema artifacts:

- `/Users/system/syncrescendence/orchestration/state/registry/tributary-disposition-ledger.jsonl`
- `/Users/system/syncrescendence/orchestration/state/registry/tributary-disposition-schema-v1.md`

Rationale:

- `orchestration/state/` is already the lawful state-bearing surface for implementation references and validator-facing control artifacts.
- `registry/` keeps the migration authority visible and singular without smearing it across `pedigree/`, `communications/`, or lane-local notebooks.
- the registry should be easy for humans to inspect and easy for validators to parse, so a flat canonical table plus append-only event ledger is the least-dangerous contract.

Contract:

- the `csv` file is the canonical current-state registry, one row per migration candidate
- the `jsonl` file is the append-only mutation ledger, one event per state change or field correction
- the schema markdown defines required columns, enumerations, and invariants

### 2. Field-level schema for each migration candidate

One row represents one source artifact identity, not one decision meeting and not one destination copy.

Mandatory identity and provenance fields:

- `candidate_id`: stable unique identifier for the source artifact row
- `source_tributary`: one of `live_shell`, `syncrescendence_old`, `syncrescendence_pre_schematic_design`
- `source_path`: path of the original artifact at the time of intake
- `source_relpath_hash`: deterministic hash of tributary + normalized source path, used to prevent duplicate rows
- `artifact_class`: controlled class such as `law`, `reference`, `playbook`, `operator`, `pattern`, `executive`, `office_state`, `manifest`, `source`, `log`, `other`
- `artifact_format`: `md`, `json`, `yaml`, `py`, `sh`, `directory_manifest`, `binary`, `mixed`, or another bounded machine-readable token
- `lineage_witness`: pointer to any upstream witness set if the artifact is one of several duplicates or merged witnesses
- `provenance_sensitivity`: `low`, `medium`, `high`, `restricted`

Mandatory evaluation fields:

- `authority_score`: bounded numeric score, recommended `0-5`
- `present_relevance`: bounded numeric score, recommended `0-5`
- `compaction_yield`: bounded numeric score, recommended `0-5`
- `duplication_status`: `unique`, `duplicate_family`, `superseded`, `derived`, `unknown`
- `review_basis`: short token describing the basis of evaluation, such as `manual_read`, `family_sample`, `validator_scan`, `merged_adjudication`

Mandatory disposition fields:

- `chosen_disposition`: exactly one of:
  - `promote_live_law`
  - `promote_reference`
  - `promote_playbook`
  - `promote_operator`
  - `promote_validated_pattern`
  - `retain_pedigree`
  - `retain_archive_manifest_only`
  - `externalize_to_exocortex`
  - `cull_with_receipt`
- `destination_lane`: canonical target lane or `none`
- `destination_artifact_path`: final promoted or retained artifact path if one exists, else `none`
- `archive_manifest_path`: path to the manifest row or file if the artifact is manifested rather than kept live
- `receipt_path`: path to the authoritative receipt recording the action taken
- `justification`: concise human-readable reason for the disposition
- `merge_family_id`: shared identifier when several sources collapse into one promoted artifact; `none` otherwise

Mandatory process and control fields:

- `record_state`: current workflow state, from the controlled transition set below
- `intake_batch_id`: packet, tranche, or run identifier that first enrolled the artifact
- `last_action_at`: ISO-8601 timestamp of the latest ledgered mutation
- `last_action_by`: office, agent, or operator id that performed the latest mutation
- `schema_version`: registry schema version, initially `v1`

Optional but recommended fields:

- `dest_artifact_hash`: content hash of the final promoted or retained artifact when one exists
- `external_pointer`: exocortex or off-repo storage pointer when disposition externalizes or manifests only
- `supersedes_candidate_id`: prior row replaced by this one in rare intake-correction cases
- `notes`: narrow clarifying note, not freeform essay space

Invariants:

- one `candidate_id` maps to one original source artifact identity
- one row has exactly one `chosen_disposition`
- if `chosen_disposition` starts with `promote_`, `destination_lane` and `destination_artifact_path` must be populated
- if `chosen_disposition` is `retain_archive_manifest_only`, `archive_manifest_path` and `receipt_path` must be populated
- if `chosen_disposition` is `externalize_to_exocortex`, `external_pointer` and `receipt_path` must be populated
- if `chosen_disposition` is `cull_with_receipt`, `receipt_path` is mandatory and `destination_artifact_path` must be `none`
- merged outcomes do not create multiple registry rows for one source; they create multiple source rows sharing one `merge_family_id` and one destination artifact

### 3. Allowed state transitions for candidate records

Recommended controlled states:

- `intake_pending`
- `triaged`
- `adjudicated`
- `scheduled`
- `executed`
- `verified`
- `closed`
- `exception`

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

State meanings:

- `intake_pending`: row exists but evaluation fields are incomplete
- `triaged`: artifact class and scoring are populated enough for decision work
- `adjudicated`: disposition and destination contract are decided
- `scheduled`: execution is assigned or batched, but file movement or promotion is not yet complete
- `executed`: promotion, manifesting, externalization, or culling action has happened and receipt exists
- `verified`: destination, manifest, receipt, and hash/pointer checks have passed
- `closed`: no further action expected under the current schema version
- `exception`: blocked, disputed, corrupted, or otherwise nonstandard case needing explicit recovery

Transition rules:

- `chosen_disposition` may first be set in `triaged` but becomes binding only at `adjudicated`
- `receipt_path` is required no later than entry into `executed`
- `destination_artifact_path` must not be treated as authoritative until `verified`
- direct `triaged -> executed` and `adjudicated -> verified` jumps should be illegal because they erase assignment and verification visibility
- corrections do not overwrite history; they append ledger events and update the current-state row

### 4. Relationship between registry rows, manifests, receipts, and final destination artifacts

The safest relationship is:

1. registry row = the authoritative identity and present state of one migration candidate
2. ledger event = every meaningful mutation to that row
3. manifest = inventory record for artifacts retained only as pedigree, archive-presence, or externalized source mass
4. receipt = evidence that a disposition action actually occurred
5. destination artifact = the promoted or retained artifact now occupying its lawful place

More concretely:

- a registry row answers: what is this source artifact, what was decided, and where does its proof live
- a manifest answers: what exists in preserved or externalized inventory, in what bundle, with what pointer or hash
- a receipt answers: what action was performed, by whom, when, against which candidate row, and with what result
- a destination artifact answers: what current live artifact now bears the promoted meaning, if any

Required joins:

- `registry.candidate_id -> ledger.candidate_id`
- `registry.archive_manifest_path -> manifest.manifest_id or manifest file`
- `registry.receipt_path -> receipt.receipt_id or receipt file`
- `registry.destination_artifact_path -> actual artifact path`
- `registry.merge_family_id -> all sibling rows contributing to one promoted destination`

Operational rules:

- manifests are for preserved existence and bundle accounting; they are not substitutes for the registry
- receipts are proof of action; they are not substitutes for present state
- destination artifacts remain the place of live meaning; they are not substitutes for provenance
- if a destination artifact later changes independently, the registry row does not become a changelog for that artifact; it remains the migration record
- if an artifact is compacted into another artifact, the registry row should point to the promoted destination and also cite the receipt that explains the compaction logic

Minimal receipt contract:

- `receipt_id`
- `candidate_id`
- `action_type`
- `performed_at`
- `performed_by`
- `source_path`
- `chosen_disposition`
- `destination_artifact_path` or `external_pointer`
- `manifest_path` if applicable
- `outcome`

### 5. Top failure modes if the registry is overdesigned or underdesigned

If overdesigned:

- too many states cause fake precision and encourage side-ledgers because workers cannot tell which state is actually decisive
- too many scoring dimensions create ceremonial arithmetic instead of lawful disposition
- registry rows become mini-essays, making validator use and batch execution impractical
- the registry starts impersonating doctrine, receipts, manifests, and execution logs all at once
- mutation rules become so heavy that people bypass the canonical registry and recreate hidden local authority

If underdesigned:

- multiple artifacts collapse into one vague row, destroying artifact-level traceability
- dispositions become informal prose and cannot be validated or batch-operated
- culls and externalizations lose proof, recreating untraceable disappearance
- merged promotions lose source pedigree, so later doctrine disputes cannot reconstruct why one witness won
- destination artifacts become impossible to distinguish from preserved originals, corrupting authority boundaries

Recommended design discipline:

- keep the current-state registry tabular and narrow
- keep mutation history append-only in a separate ledger
- require one disposition and one receipt pointer per executed candidate
- allow shared destination artifacts through `merge_family_id` rather than duplicate destination rows
- let manifests and receipts stay separate artifacts with explicit joins instead of trying to inline everything into the registry

## Immediate Notes

- the registry should be validator-friendly before it is optimizer-friendly
- append-only ledger semantics are necessary to prevent silent reinterpretation of migration history
- `knowledge/references/` naming remains unresolved at shell level, but that does not block the registry contract because `destination_lane` is a value, not a topology redesign

## Open Ambiguities

- exact destination enumeration for the lower-than-canon knowledge lane remains a separate tranche-U decision
- whether receipts should live under `communications/receipts/` or a dedicated migration receipt lane was not decided in this packet and should remain outside this contract
