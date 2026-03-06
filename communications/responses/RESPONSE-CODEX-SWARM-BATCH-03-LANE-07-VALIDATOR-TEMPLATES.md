# Response

**Response ID**: `RSP-20260306-codex-swarm-batch-03-lane-07-validator-templates`  
**Surface**: `codex_parallel_session`  
**Date received**: `2026-03-06`  
**Dispatch packet**: `communications/prompts/PACKET-CODEX-SWARM-BATCH-03-LANE-07-VALIDATOR-TEMPLATES.md`  
**Result state**: `complete`  
**Receipt artifacts**:
  - `communications/responses/RESPONSE-CODEX-SWARM-BATCH-03-LANE-07-VALIDATOR-TEMPLATES.md`

## Returned Content

This lane should remain a thin optional tooling pack. The right first move is not a general migration engine. The right first move is a small validator and template layer that makes the Batch 02 contracts machine-checkable at their narrowest seams: registry rows, manifests, receipts, cautionary status, and promotion metadata.

## 1. Thin Validator Rule Set

The validator should begin with five narrow rule families.

### 1.1 Registry rules

Enforce immediately:

- required field presence on every registry row:
  - `candidate_id`
  - `source_tributary`
  - `source_path`
  - `artifact_class`
  - `chosen_disposition`
  - `record_state`
  - `receipt_path`
  - `schema_version`
- allowed enumeration checks for:
  - `chosen_disposition`
  - `record_state`
  - `duplication_status`
  - `provenance_sensitivity`
- disposition-path invariants:
  - promoted rows must have `destination_lane` and `destination_artifact_path`
  - `retain_archive_manifest_only` rows must have `archive_manifest_path`
  - `externalize_to_exocortex` rows must have `external_pointer`
  - `cull_with_receipt` rows must keep `destination_artifact_path: none`
- join invariant:
  - `receipt_path` must resolve to an existing receipt artifact by the time a row reaches `executed` or beyond

Defer:

- scoring validation beyond shape/range checks
- duplicate-family adjudication logic
- automatic reconciliation of stale destination pointers

### 1.2 Manifest rules

Enforce immediately:

- required field presence:
  - `manifest_id`
  - `manifest_type`
  - `source_tributary`
  - `source_root`
  - `source_scope`
  - `disposition_status`
  - `authority_status`
  - `cautionary_status`
  - `receipt_links`
- allowed enumeration checks for:
  - `manifest_type`
  - `authority_status`
  - `cautionary_status`
- circumstance rules:
  - if `disposition_status` implies externalization, `external_pointers` must be present
  - if `cautionary_status` is not `none`, `cautionary_reason` must exist
  - if live derivatives are declared, `retained_derivatives` must be non-empty

Defer:

- manifest coverage completeness for whole trees
- exact `entry_count` correctness
- semantic judgment about whether a family should have been manifest-only

### 1.3 Receipt rules

Enforce immediately:

- required field presence:
  - `receipt_id`
  - `receipt_type`
  - `timestamp_utc`
  - `actor`
  - `artifact_class`
  - `reason`
  - `disposition`
  - `authority_status`
  - `cautionary_status`
  - `content_integrity`
- path/pointer minimum:
  - at least one source locator must exist
  - at least one destination locator, replacement artifact, or external pointer must exist
- allowed enumeration checks for:
  - `receipt_type`
  - `authority_status`
  - `cautionary_status`
  - `content_integrity`
- circumstance rules:
  - externalization and cull receipts must declare reconstructability
  - subtree or family events must carry `related_manifest`
  - if `cautionary_status` is not `none`, `cautionary_reason` must exist

Defer:

- cryptographic integrity verification
- content diff classification
- one-to-many event normalization rules beyond the minimum bounded-event check

### 1.4 Cautionary status rules

Enforce immediately:

- any artifact carrying `cautionary_status` must use only `none`, `partial`, or `full`
- any `partial` or `full` artifact must declare `cautionary_reason`
- `cautionary_reason` should be restricted to:
  - `hidden_authority`
  - `rejected_topology`
  - `superseded_doctrine`
  - `unsafe_runtime_assumption`
  - `negative_exemplar`
  - `mixed_reuse_risk`
- preserved pedigree artifacts must always declare `authority_status`

Defer:

- automatic inference of cautionary status from body text
- broad scanning for topology anti-patterns
- policy heuristics about when `partial` should escalate to `full`

### 1.5 Promotion metadata rules

Enforce immediately:

- artifacts that cross office or migration thresholds must declare:
  - `artifact_class`
  - `artifact_id`
  - `promotion_scope`
- if an artifact is sovereign-facing or executive-eligible, it must also declare `steering_class`
- `promotion_scope` should be restricted to a small set such as:
  - `local_only`
  - `cross_lane`
  - `sovereign_candidate`
- `steering_class` should be restricted to:
  - `none`
  - `briefing`
  - `escalation`
  - `summit`
- validator should reject executive-targeted artifacts with `steering_class: none`

Defer:

- full promotion routing logic
- automatic office-to-communications classification
- semantic validation that a sovereign candidate truly deserves escalation

## 2. Template Skeletons And Field Blocks

These should be treated as reusable field blocks, not heavyweight document formats.

### 2.1 Registry row block

```yaml
candidate_id: CAND-0001
source_tributary: live_shell
source_path: /source/path/example.md
source_relpath_hash: sha256:...
artifact_class: law
artifact_format: md
lineage_witness: none
provenance_sensitivity: medium
authority_score: 4
present_relevance: 4
compaction_yield: 3
duplication_status: unique
review_basis: manual_read
chosen_disposition: promote_reference
destination_lane: knowledge/references
destination_artifact_path: /dest/path/example.md
archive_manifest_path: none
receipt_path: pedigree/rehousing-receipts/RECEIPT-compact-then-promote-20260306-01.md
external_pointer: none
justification: "Retain as current reference after migration review."
merge_family_id: none
record_state: executed
intake_batch_id: PKT-20260306-example
last_action_at: "2026-03-06T12:00:00Z"
last_action_by: codex_parallel_session
schema_version: v1
```

### 2.2 Manifest block

```yaml
manifest_id: MANIFEST-example-family-20260306-01
manifest_type: family
label: "Example family manifest"
source_tributary: syncrescendence_old
source_root: /source/root
source_scope:
  - old/example-family/**
created_at_utc: "2026-03-06T12:00:00Z"
created_by: codex_parallel_session
disposition_status: retained_pedigree
authority_status: not-live-authority
cautionary_status: partial
cautionary_reason: rejected_topology
summary: "Preserved for lineage; not current law."
artifact_classes:
  - law
  - operator
receipt_links:
  - pedigree/rehousing-receipts/RECEIPT-subtree-sync-20260306-01.md
external_pointers: []
retained_derivatives:
  - /dest/path/example-derived.md
notes_on_ambiguity: []
```

### 2.3 Receipt block

```yaml
receipt_id: RECEIPT-compact-then-promote-20260306-01
receipt_type: compact-then-promote
label: "Example promotion receipt"
timestamp_utc: "2026-03-06T12:10:00Z"
actor: codex_parallel_session
source_path: /source/path/example.md
destination_path: /dest/path/example.md
artifact_class: law
reason: "Merged source into promoted reference artifact."
disposition: promote_reference
authority_status: not-live-authority
cautionary_status: none
content_integrity: compacted-derivative
related_manifest: pedigree/archive-manifests/MANIFEST-example-family-20260306-01.md
related_derivatives:
  - /dest/path/example.md
replacement_artifact: /dest/path/example.md
reconstructability: manifest-plus-receipt
```

### 2.4 Cautionary metadata block

```yaml
authority_status: not-live-authority
cautionary_status: partial
cautionary_reason: mixed_reuse_risk
```

### 2.5 Promotion metadata block

```yaml
artifact_class: response
artifact_id: RSP-20260306-example
promotion_scope: cross_lane
steering_class: none
derived_from:
  - PKT-20260306-example
related_outputs:
  - /dest/path/example.md
```

## 3. Immediate Versus Deferred Enforcement

Recommendation:

Enforce immediately:

- required field presence
- enum validation
- simple conditional requirements
- minimal path or pointer existence checks
- registry-to-receipt join checks for executed-or-later records
- executive-target metadata sanity checks

Defer:

- hard-fail enforcement on missing optional metadata outside the narrow core
- semantic scoring logic
- body-content inspection
- auto-quarantine for migration artifacts
- automatic rewrite or fix-up behavior
- broad completeness checks across whole trees or whole batches

The immediate layer should be able to say:

- this row is missing required machine-readable contract data
- this receipt or manifest cannot be joined
- this preserved artifact forgot its cautionary or authority declaration
- this promotion artifact claims a routing burden it cannot legally carry

It should not yet try to say:

- this migration decision was substantively wrong
- this family was optimally compacted
- this artifact should have been promoted instead of preserved

## 4. Failure Modes If The Validator Layer Is Overbuilt Too Early

Top risks:

1. The validator becomes a shadow constitution.
   Tooling starts inventing doctrine instead of enforcing already-ratified contract fields.

2. Writers route around the system.
   If the first validator requires too much semantic ceremony, people will keep side ledgers and ad hoc notes.

3. False precision replaces lawful minimalism.
   Overly rich states, scores, and remediation branches create the appearance of rigor while reducing adoption.

4. The main artifact set gets blocked on incomplete automation.
   Migration law, manifests, receipts, and promotion rules are the primary deliverables. Tooling must not become the gate for writing them.

5. Repair logic silently mutates authority.
   Early auto-fix or auto-quarantine behavior can move files or rewrite metadata before the constitutional paths are fully stable.

6. Validator maintenance cost outruns contract stability.
   If the law artifacts are still settling, a feature-heavy validator will thrash and lose trust.

## 5. Deferral Judgment

This lane can be deferred without harming the core write set, provided one condition is met:

- the main law artifacts and template-bearing artifacts must still include the machine-readable fields named above

In other words:

- the validator implementation is deferrable
- the metadata discipline is not deferrable

That is the narrow recommendation. Put the fields into the artifacts now. Enforce them first with templates and human review. Add the thin validator afterward. Keep the tooling pack subordinate to the constitutional and migration-law artifacts rather than allowing it to become a parallel design center.
