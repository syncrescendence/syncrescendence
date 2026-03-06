# Response

**Response ID**: `RSP-20260306-pedigree-and-manifests`
**Surface**: `codex_parallel_session`
**Date received**: `2026-03-06`
**Dispatch packet**: `communications/prompts/PACKET-CODEX-SWARM-BATCH-02-LANE-03-PEDIGREE-AND-MANIFESTS.md`
**Result state**: `complete`
**Receipt artifacts**:
  - `communications/responses/RESPONSE-CODEX-SWARM-BATCH-02-LANE-03-PEDIGREE-AND-MANIFESTS.md`

## Returned Content

`pedigree/` should be treated as a custody lane, not a generic archive shelf. Its contract is to preserve ancestry, prove movement, and mark danger conditions without quietly granting present authority.

The governing split should be:

- `pedigree/originals/` for thin authenticity reserve items whose original wording or structure matters
- `pedigree/rehoused/` for preserved predecessor artifacts copied into the successor shell for ancestry and study
- `pedigree/archive-manifests/` for family-level or root-level inventories describing what was retained, externalized, or left manifest-only
- `pedigree/rehousing-receipts/` for event-level chain-of-custody records proving a move, sync, extraction, or compaction act
- `pedigree/cautionary/` for exemplars kept primarily because they demonstrate a failure mode, rejected topology, hidden-authority pattern, or superseded doctrine hazard

If a separate `pedigree/cautionary/` physical lane is not added immediately, the semantic class must still exist and be machine-readable on artifacts, manifests, and receipts. The class matters more than the folder.

## 1. Proposed Physical Layout

### A. Preserved originals

Use `pedigree/originals/` only for artifacts where the original form is itself evidence. This is the authenticity reserve, not the bulk holding area.

Inclusion rule:

- keep only thin exemplars, canonical predecessor wording, or burden-bearing source artifacts whose exact body must remain inspectable

### B. Rehoused preserved artifacts

Use `pedigree/rehoused/<tributary>/...` for preserved predecessor artifacts that need to stay legible inside the live shell but are not live authority.

Contract:

- preserve source-relative path shape where useful for provenance
- never imply live authority by destination alone
- require a paired rehousing receipt for every preserved artifact or synchronized subtree

### C. Archive manifests

Use `pedigree/archive-manifests/` for inventories of roots, families, tranches, or externalized bodies.

Manifest classes:

- shell manifest: top-level census of a predecessor root
- family manifest: one source family or subtree
- tranche manifest: one migration or shedding batch
- manifest-only disposition record: family retained as description plus pointer, without body in repo

### D. Rehousing receipts

Use `pedigree/rehousing-receipts/` for atomic custody events.

Receipt classes:

- preserve-copy
- subtree-sync
- compact-then-promote
- externalize-with-manifest
- cull-with-receipt

### E. Cautionary material

Use `pedigree/cautionary/` or explicit `cautionary` tagging for artifacts preserved because they explain a danger, not because they should be copied forward.

Typical contents:

- root-queue specimens such as old mixed sovereign/inbox/outbox topologies
- hidden-authority documents
- superseded shell contracts that are still easy to misread as live law
- negative exemplars that shaped current office, communications, or executive boundaries

## 2. Minimum Metadata For A Pedigree Manifest

Every pedigree manifest should include these minimum fields:

- `manifest_id`
- `manifest_type`
  Values should be constrained to `shell`, `family`, `tranche`, or `manifest_only`
- `label`
- `source_tributary`
- `source_root`
- `source_scope`
  Path, subtree, or pattern the manifest covers
- `created_at_utc`
- `created_by`
  Operator, office, or tool surface
- `disposition_status`
  Such as `retained_pedigree`, `externalized_with_manifest`, `mixed`, `culled_with_receipt`
- `authority_status`
  Must explicitly say this material is not live authority
- `cautionary_status`
  `none`, `partial`, or `full`
- `summary`
  Short natural-language description
- `entry_count`
  Or `estimated_entry_count` when exact count is unavailable
- `artifact_classes`
  Controlled list such as `constitution`, `communications`, `office-contract`, `source-body`, `runtime-log`, `operator`, `executive-lineage`
- `disposition_rules`
  Short list or mapping of allowed destination outcomes for covered entries
- `retained_derivatives`
  Live references, validated patterns, playbooks, operators, or executive artifacts derived from this source
- `receipt_links`
  Paths to related rehousing or cull receipts
- `external_pointers`
  Required when any covered body is offloaded
- `notes_on_ambiguity`
  Required when classification remains unresolved

Recommended but not strictly minimum:

- `bytes_at_capture`
- `review_state`
- `promotion_candidates`
- `supersedes` / `superseded_by`

## 3. Minimum Metadata For A Rehousing Receipt

Every rehousing receipt should include these minimum fields:

- `receipt_id`
- `receipt_type`
  `preserve-copy`, `subtree-sync`, `promotion`, `externalization`, or `cull`
- `label`
- `timestamp_utc`
- `actor`
  Office, operator, or automation identity
- `source_path` or `source_root`
- `destination_path` or `destination_root`
  For culls, destination may be omitted only if `external_pointer` or replacement artifact is present
- `dest_rel`
  Relative path inside the successor shell when applicable
- `artifact_class`
- `reason`
- `disposition`
- `authority_status`
  Must explicitly state `not-live-authority` for pedigree-preserved artifacts
- `cautionary_status`
- `related_manifest`
  Required for subtree-level events and externalization events
- `related_derivatives`
  Any live artifacts produced from the source
- `content_integrity`
  At minimum one of: exact copy, normalized copy, partial extract, compacted derivative, family move

For `externalization` or `cull` receipts, also require:

- `external_pointer` or `deletion_scope`
- `replacement_artifact`
  Use `none` if nothing replaces it
- `reconstructability`
  Whether provenance can be reconstructed from manifest plus receipt

## 4. When A Preserved Artifact Also Needs A Cautionary Tag

A preserved artifact requires a cautionary tag when any of these hold:

- it encodes a rejected topology, especially root-global queues or folder-driven authority
- it previously acted as live law but is now superseded and still easy to misread as current instruction
- it mixes historical value with dangerous operational advice
- it records a failure mode, governance breach, provenance break, or hidden-authority pattern that future automation must not reenact
- it contains stale credentials, machine-local assumptions, or environment-specific execution logic that should be studied but not reused blindly
- it is preserved primarily as a negative exemplar rather than as a reusable source

Tagging rule:

- `cautionary_status: full` when the main reason to preserve the artifact is warning value
- `cautionary_status: partial` when the artifact contains both reusable signal and dangerous obsolete assumptions
- `cautionary_status: none` only when the artifact is ancestry without a meaningful risk of operational misuse

Each cautionary artifact should also carry a short `caution_reason` field with controlled values such as:

- `hidden_authority`
- `rejected_topology`
- `superseded_doctrine`
- `unsafe_runtime_assumption`
- `negative_exemplar`

## 5. Top Failure Modes If Pedigree Remains Semantically Soft

1. Preserved ancestry will be mistaken for live law.
   Automation and humans will treat preserved files as current instruction because custody status is implicit instead of declared.

2. Archive manifests will degrade into vague shelf labels.
   Without minimum metadata, `archive-manifests/` will describe that something existed without proving what was covered, moved, externalized, or left unresolved.

3. Rehousing receipts will stop being chain-of-custody evidence.
   Minimal “source to destination” JSON is enough to show a copy occurred, but not enough to defend why it was lawful, what changed, or whether the body stayed authoritative.

4. Negative exemplars will be silently re-imported.
   If cautionary status is not explicit, root-queue patterns, mixed sovereign folders, and hidden office constitutions can return as “historically validated” practice.

5. Manifest-only and preserved-original classes will collapse together.
   The repo will lose the difference between “kept as exact evidence,” “kept as a preserved working copy,” and “represented only by manifest plus pointer.”

6. Pedigree will absorb low-signal debris.
   Without artifact classes and disposition rules, `pedigree/` becomes the place where unresolved material accumulates instead of the place where ancestry is disciplined.

7. Promotion lineage will become untraceable.
   Future readers will see live patterns and preserved ancestors but not the custody chain linking them.

## Net Recommendation

The minimum contract is simple:

- `originals` preserve exact evidence
- `rehoused` preserves inspectable ancestry
- `archive-manifests` preserves family-level description and external pointers
- `rehousing-receipts` preserves event-level custody
- `cautionary` preserves warnings against reenactment

Pedigree should remain legible, queryable, and automation-safe by making three statuses explicit on every preserved item or record:

- what it is
- how it got here
- whether it is dangerous to treat as live law
