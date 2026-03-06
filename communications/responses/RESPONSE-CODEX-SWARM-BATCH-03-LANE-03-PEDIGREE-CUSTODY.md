# Response

**Response ID**: `RSP-20260306-codex-swarm-batch-03-lane-03-pedigree-custody`  
**Surface**: `codex_parallel_session`  
**Date received**: `2026-03-06`  
**Dispatch packet**: `communications/prompts/PACKET-CODEX-SWARM-BATCH-03-LANE-03-PEDIGREE-CUSTODY.md`  
**Result state**: `complete`  
**Receipt artifacts**:
  - `communications/responses/RESPONSE-CODEX-SWARM-BATCH-03-LANE-03-PEDIGREE-CUSTODY.md`

## Returned Content

This draft keeps the write set narrow and concrete. It supplies one compact pedigree custody law artifact, one README for `pedigree/archive-manifests/`, one README for `pedigree/rehousing-receipts/`, explicit machine-readable cautionary fields, and the main failure modes if custody is left loose.

## 1. Patch-Ready Draft: `pedigree/PEDIGREE-CUSTODY-LAW-v1.md`

```md
# Pedigree Custody Law v1

**Status**: proposed  
**Scope**: `pedigree/` custody, manifests, receipts, and cautionary status  
**Purpose**: preserve ancestry, prove movement, and prevent preserved material from silently regaining live authority

## 1. Law

`pedigree/` is a custody lane, not a live authority lane.

Artifacts in `pedigree/` exist to preserve provenance, demonstrate movement, retain evidence, and warn against reenactment. Presence in `pedigree/` does not grant present operational authority.

The lane is divided by burden:

- `pedigree/originals/` preserves thin exact-form evidence whose original wording, layout, or file body matters
- `pedigree/rehoused/` preserves inspectable predecessor material copied into the successor shell for ancestry and study
- `pedigree/archive-manifests/` preserves family-level, tranche-level, or root-level inventory records
- `pedigree/rehousing-receipts/` preserves event-level custody proofs for moves, syncs, extractions, compactions, externalizations, and culls
- `pedigree/cautionary/` may exist physically, but cautionary status must exist semantically even when the folder is deferred

## 2. Binding Rules

1. Every preserved subtree or preserved artifact class must be covered by either:
   - a manifest plus one or more linked receipts, or
   - an artifact-local receipt when the event is genuinely atomic

2. Every artifact preserved under `pedigree/rehoused/` must be explicitly marked `authority_status: not-live-authority`.

3. Every event recorded in `pedigree/rehousing-receipts/` must state:
   - what moved
   - why it moved
   - what custody class it entered
   - whether the body is exact, normalized, partial, compacted, or manifest-only

4. Cautionary status is mandatory metadata.
   The physical `pedigree/cautionary/` lane is optional in the first write set, but `cautionary_status` and `cautionary_reason` are not optional when risk exists.

5. `pedigree/originals/` is a thin authenticity reserve.
   It must not become the bulk holding area for all predecessor material.

6. `pedigree/archive-manifests/` describes bounded custody scope.
   A manifest must not be a vague shelf label. It must identify source scope, disposition, and linked receipts or pointers.

7. `pedigree/rehousing-receipts/` is chain-of-custody evidence.
   A receipt must not merely say that a copy occurred. It must state lawful reason, result, and reconstructability.

8. Manifest-only retention is lawful.
   When a body is externalized or intentionally not retained in-repo, the manifest and receipt pair must still preserve source scope, disposition, and retrieval pointer.

9. Preserved negative exemplars must not be silently reusable.
   If an artifact is kept partly or primarily as a warning, it must carry cautionary metadata that automation can test.

10. Promotion lineage must remain joinable.
    If a live artifact is derived from a pedigree source, the relevant manifest and/or receipt must link the derived artifact path.

## 3. Minimum Required Metadata

### 3.1 Manifest minimums

Every manifest must include:

- `manifest_id`
- `manifest_type`
- `label`
- `source_tributary`
- `source_root`
- `source_scope`
- `created_at_utc`
- `created_by`
- `disposition_status`
- `authority_status`
- `cautionary_status`
- `summary`
- `artifact_classes`
- `receipt_links`

Allowed `manifest_type` values:

- `shell`
- `family`
- `tranche`
- `manifest_only`

Allowed `authority_status` values:

- `not-live-authority`
- `mixed-authority-risk`

Allowed `cautionary_status` values:

- `none`
- `partial`
- `full`

Additional fields become required by circumstance:

- `external_pointers` when any covered body is externalized or retained only by pointer
- `notes_on_ambiguity` when classification or family boundaries remain unresolved
- `retained_derivatives` when live artifacts were produced from the covered source

### 3.2 Receipt minimums

Every receipt must include:

- `receipt_id`
- `receipt_type`
- `label`
- `timestamp_utc`
- `actor`
- `source_path` or `source_root`
- `destination_path`, `destination_root`, or `external_pointer`
- `artifact_class`
- `reason`
- `disposition`
- `authority_status`
- `cautionary_status`
- `content_integrity`

Allowed `receipt_type` values:

- `preserve-copy`
- `subtree-sync`
- `compact-then-promote`
- `externalize-with-manifest`
- `cull-with-receipt`

Allowed `content_integrity` values:

- `exact-copy`
- `normalized-copy`
- `partial-extract`
- `compacted-derivative`
- `family-move`
- `manifest-only`

Additional fields become required by circumstance:

- `related_manifest` for subtree-level, family-level, and externalization events
- `related_derivatives` when live derivatives were produced
- `replacement_artifact` for culls and compactions
- `reconstructability` for externalization and cull events
- `deletion_scope` when the event removes in-repo body material

## 4. Cautionary Status

Cautionary status exists to stop historical preservation from being mistaken for present endorsement.

An artifact, manifest, or receipt must carry cautionary metadata when any of the following is true:

- it encodes a rejected topology
- it records hidden-authority behavior
- it is superseded doctrine still easy to misread as live law
- it contains unsafe runtime assumptions or stale environment bindings
- it is preserved mainly as a negative exemplar

Allowed `cautionary_reason` values:

- `hidden_authority`
- `rejected_topology`
- `superseded_doctrine`
- `unsafe_runtime_assumption`
- `negative_exemplar`
- `mixed_reuse_risk`

Interpretation:

- `cautionary_status: full` means warning value is primary
- `cautionary_status: partial` means the artifact mixes durable signal with operational risk
- `cautionary_status: none` means no meaningful reenactment risk is known

## 5. Naming and Join Rules

- Manifests should be named with stable bounded scope, for example: `MANIFEST-<tributary>-<family>-<date>.md`
- Receipts should be named with one custody event per file, for example: `RECEIPT-<event-class>-<date>-<seq>.md`
- `manifest_id` and `receipt_id` must be globally unique within the repo
- Receipts may link multiple source paths only when they are one bounded event under one reason and one disposition
- A manifest may summarize many artifacts, but it must resolve to bounded scope rather than broad narrative prose

## 6. Prohibitions

- do not treat preserved pedigree files as live authority by location alone
- do not store unresolved debris in `pedigree/` without manifest or receipt coverage
- do not externalize a family without leaving manifest plus receipt evidence
- do not preserve hazardous exemplars without machine-readable cautionary status
- do not use `pedigree/rehousing-receipts/` for ordinary inter-office routing receipts

## 7. Operational Effect

If custody is uncertain, preserve the source with explicit `not-live-authority` status, write the receipt, and record ambiguity in the manifest. Ambiguity is lawful if declared. Silent status is not lawful.
```

## 2. Patch-Ready Draft: `pedigree/archive-manifests/README.md`

```md
# Archive Manifests

This directory holds bounded inventory records for preserved lineage.

An archive manifest does not prove that a move happened by itself. It proves what source scope was evaluated, how that scope was dispositioned, and which receipts or external pointers complete the custody chain.

## What belongs here

- root-level census of a predecessor shell
- family-level inventory of a preserved subtree
- tranche-level inventory for one migration batch
- manifest-only records for material kept by description plus pointer rather than in-repo body

## What does not belong here

- event-level copy or move proofs
- ordinary communications receipts
- live authority documents
- unbounded narrative archaeology without declared source scope

## Required fields

Every manifest must declare at least:

```yaml
manifest_id: MANIFEST-example-20260306-01
manifest_type: family
label: "Example family retention manifest"
source_tributary: old-shell
source_root: /source/root
source_scope:
  - old/family/**
created_at_utc: "2026-03-06T00:00:00Z"
created_by: codex_parallel_session
disposition_status: retained_pedigree
authority_status: not-live-authority
cautionary_status: partial
summary: "Family preserved for ancestry; some topology assumptions are hazardous."
artifact_classes:
  - constitution
  - communications
receipt_links:
  - pedigree/rehousing-receipts/RECEIPT-subtree-sync-20260306-01.md
external_pointers: []
retained_derivatives:
  - knowledge/sigma/example-derived-note.md
notes_on_ambiguity: []
```

## Manifest rules

1. `source_scope` must be bounded.
   Use explicit paths, subtrees, or narrow patterns.

2. `disposition_status` must describe the result for the covered scope.
   Recommended values:
   - `retained_pedigree`
   - `externalized_with_manifest`
   - `mixed`
   - `culled_with_receipt`

3. `authority_status` must not imply live authority.
   Use `not-live-authority` unless the manifest is warning about mixed-authority residue, in which case use `mixed-authority-risk`.

4. `receipt_links` is required.
   A manifest without linked receipts is inventory without custody proof.

5. `external_pointers` is required when material is not retained in-repo.

6. `notes_on_ambiguity` is required when family boundaries, classifications, or source completeness are uncertain.

## Minimum authoring guidance

- one manifest per bounded scope
- prefer family manifests over giant omnibus manifests
- when a root is too large, use one shell manifest that points to family manifests
- keep the summary short and the source scope explicit
- if a manifest exists mainly to warn, set `cautionary_status` to `full` or `partial`
```

## 3. Patch-Ready Draft: `pedigree/rehousing-receipts/README.md`

```md
# Rehousing Receipts

This directory holds event-level chain-of-custody records.

A rehousing receipt proves that one bounded preservation, sync, extraction, compaction, externalization, or cull event occurred. If a manifest explains the family, the receipt explains the act.

## What belongs here

- preserve-copy receipts
- subtree-sync receipts
- compact-then-promote receipts
- externalize-with-manifest receipts
- cull-with-receipt records

## What does not belong here

- ordinary communications acknowledgements
- dispatch receipts for live office routing
- broad family inventories without a concrete event

## Required fields

Every receipt must declare at least:

```yaml
receipt_id: RECEIPT-subtree-sync-20260306-01
receipt_type: subtree-sync
label: "Sync predecessor family into pedigree rehoused lane"
timestamp_utc: "2026-03-06T00:00:00Z"
actor: codex_parallel_session
source_root: /source/root
source_path:
  - old/family/**
destination_root: pedigree/rehoused/old-shell/
destination_path:
  - pedigree/rehoused/old-shell/old/family/**
artifact_class: communications
reason: preserve ancestry during tributary compaction
disposition: retained_pedigree
authority_status: not-live-authority
cautionary_status: partial
cautionary_reason:
  - superseded_doctrine
content_integrity: normalized-copy
related_manifest: pedigree/archive-manifests/MANIFEST-old-shell-family-20260306.md
related_derivatives:
  - knowledge/sigma/example-derived-note.md
replacement_artifact: none
reconstructability: manifest_plus_receipt_sufficient
deletion_scope: []
external_pointer: null
```

## Receipt rules

1. One receipt should capture one bounded event.
   If the reason or disposition changes, write another receipt.

2. `receipt_type` and `content_integrity` must be explicit.
   A copy is not the same as a partial extract, compacted derivative, or manifest-only retention.

3. `authority_status` must be present on every receipt.
   Pedigree custody without authority marking is unsafe.

4. `related_manifest` is required for subtree-scale and externalization events.

5. `replacement_artifact` is required for culls and compactions.
   Use `none` only when no replacement exists.

6. `reconstructability` is required when material leaves the repo or is removed from the repo.
   Recommended values:
   - `receipt_only`
   - `manifest_plus_receipt_sufficient`
   - `pointer_required`
   - `not_reconstructable`

## Minimum authoring guidance

- prefer stable IDs and UTC timestamps
- keep reasons concrete rather than ceremonial
- link any live derivatives produced from the source
- if the event preserves a hazardous exemplar, include `cautionary_reason`
- do not reuse these receipts for ordinary communications routing
```

## 4. Explicit Machine-Readable Cautionary Fields

Use the same fields across preserved artifacts, manifests, and receipts:

```yaml
cautionary_status: none | partial | full
cautionary_reason:
  - hidden_authority
  - rejected_topology
  - superseded_doctrine
  - unsafe_runtime_assumption
  - negative_exemplar
  - mixed_reuse_risk
cautionary_note: "Short sentence describing the specific hazard."
reuse_posture: review_before_reuse | do_not_reenact | safe_for_reference_only
authority_status: not-live-authority | mixed-authority-risk
```

Minimum clause set when a physical `pedigree/cautionary/` lane is deferred:

```md
This artifact is preserved for ancestry and warning value.
It is not live authority.
Automation must test `cautionary_status` and `reuse_posture` before reusing the artifact body, path shape, or embedded procedure.
```

## 5. Top Failure Modes If Custody Is Implemented Loosely

1. Preserved material will be mistaken for live law.
   Folder placement alone will be read as endorsement and old doctrine will quietly reactivate.

2. Manifests will degrade into vague archive labels.
   Future readers will know that something existed but not what exact scope was retained, externalized, or culled.

3. Rehousing receipts will stop functioning as evidence.
   A minimal source-destination note will not explain why the move was lawful, what integrity class was preserved, or whether the result is reconstructable.

4. Negative exemplars will be re-imported as precedent.
   Rejected topology, hidden-authority patterns, and unsafe runtime assumptions will return because cautionary status was not machine-testable.

5. Originals, rehoused copies, and manifest-only holdings will collapse into one soft category.
   The shell will lose the distinction between exact evidence, preserved working ancestry, and pointer-only retention.

6. Promotion lineage will become non-joinable.
   Derived live artifacts will no longer be traceable back to preserved source scope, which breaks auditability and compaction safety.

7. `pedigree/` will become an unresolved debris shelf.
   Without bounded manifests and receipts, the custody lane will absorb low-signal leftovers instead of disciplined ancestry.

## Immediate Notes

- This draft assumes the cautionary semantic contract must ship before any optional physical `pedigree/cautionary/` directory is created.
- The law artifact stays narrow on purpose and only hardens manifests, receipts, authority marking, and cautionary status.

## Open Ambiguities

- None that block the first write set. The main optional decision is whether to create `pedigree/cautionary/` immediately or defer the physical lane while keeping the metadata mandatory.
