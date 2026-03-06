# Response

**Response ID**: `RSP-20260306-sigma-ratification`
**Surface**: `codex_parallel_session`
**Date received**: `2026-03-06`
**Dispatch packet**: `communications/prompts/PACKET-CODEX-SWARM-BATCH-03-LANE-02-SIGMA-RATIFICATION.md`
**Result state**: `complete`
**Receipt artifact**:
  - `communications/responses/RESPONSE-CODEX-SWARM-BATCH-03-LANE-02-SIGMA-RATIFICATION.md`

## Returned Content

### Executive Settlement

This draft treats `knowledge/sigma/` as already ratified and does not reopen that decision.

The narrow implementation rule is:

- `knowledge/sigma/` is the live secondary knowledge tier
- bare `knowledge/references/` is no longer a sovereign lane name in law
- the existing `knowledge/references/` tree remains temporarily in place as a housed compatibility subtree equivalent to `knowledge/sigma/references/`
- new drafting should target Sigma semantics immediately, even while physical rehousing happens in stages

Because the current law is short and the ratification changes multiple sections at once, the cleanest patch is a full replacement rather than a line-level amendment.

## 1. Patch-Ready Replacement for `KNOWLEDGE-LANE-LAW-v1.md`

```md
# Knowledge Lane Law v1

## Purpose

`knowledge/` exists because the predecessor shells repeatedly carried a distinct research and feedstock subsystem that cannot be reduced to pedigree, runtime, or validated patterns without losing semantic resolution.

The successor shell uses `knowledge/` for living domain knowledge that is neither:

- constitutional law,
- executive direction,
- program sequencing,
- communications lineage,
- nor raw runtime state.

## Internal Sub-Lanes

- `knowledge/canon/`: bind-on-default domain knowledge that has been promoted into durable live shell doctrine.
- `knowledge/sigma/`: the live secondary tier for repeated-use doctrine, annex knowledge, and bounded but durable judgment material below canon.
- `knowledge/sigma/references/`: housed reference substrates, compendia, and evidence-rich syntheses that support Sigma and canon but are not yet localized into shell-native doctrine.
- `knowledge/feedstock/`: lawful intake for incoming source bundles, raw research drops, and pre-compaction material.

## Distinctions

- `pedigree/` preserves ancestry and predecessor evidence.
- `knowledge/canon/` holds domain knowledge that should bind default shell judgment.
- `knowledge/sigma/` holds live secondary doctrine that should repeatedly inform judgment without binding every pass.
- `knowledge/sigma/references/` holds support substrates that Sigma and canon may cite, compact, or elevate from.
- `validated-patterns/` holds already-proven operators and operating patterns.
- `communications/` holds prompts, responses, handoffs, and assessments, not topic knowledge.

## Promotion Ladder

The live promotion ladder inside `knowledge/` is:

`feedstock -> sigma/references -> sigma -> canon`

with explicit exits to:

- `playbooks/`
- `operators/`
- `validated-patterns/`
- `pedigree/`

Artifacts should not skip directly from raw intake to canon unless they are being rewritten as compact shell law with explicit evidence and supersession handling.

## Intake Rule

New research should land in `knowledge/feedstock/` first when it is still raw, incoming, or insufficiently adjudicated.

Once compacted, knowledge should rise into:

- `knowledge/sigma/references/` if it is still primarily a housed reference substrate,
- `knowledge/sigma/` if it has become repeated-use secondary doctrine,
- `knowledge/canon/` if it has become bind-on-default doctrine,
- or another lawful surface such as `playbooks/`, `operators/`, `validated-patterns/`, or `pedigree/` as appropriate.

## Compatibility Rule

During staged Sigma ratification, the pre-existing bare `knowledge/references/` tree is treated as a housed compatibility form of `knowledge/sigma/references/`.

This means:

- existing artifacts under `knowledge/references/` remain live and citable,
- they should be interpreted semantically as Sigma reference substrates rather than as an independent top-level lane,
- new law, README language, and classification decisions should use Sigma terminology,
- and staged rehousing may move the physical tree later without reopening the lane contract.

No net-new doctrine should rely on bare `references/` as if it were the enduring constitutional lane name.

## Initial Occupants

The first explicit Sigma reference occupant is the distilled archived `neocorpus`, presently housed under the compatibility path `knowledge/references/neocorpus/` and semantically treated as `knowledge/sigma/references/neocorpus/` until rehoused into its final location.

The associated compatibility witnesses presently include:

- `knowledge/references/NEOCORPUS-CATEGORY-INDEX-v1.md`
- `knowledge/references/NEOCORPUS-INTERNALIZATION-v1.md`
```

## 2. Patch-Ready Draft for `knowledge/sigma/README.md`

```md
# Sigma

`knowledge/sigma/` is the live secondary knowledge tier.

It houses durable, repeated-use doctrine that sharpens shell judgment but does not bind every pass the way canon does.

## What Belongs Here

- bounded but durable doctrine that is consulted across multiple tasks
- annex knowledge that improves design, synthesis, adjudication, or planning
- shell-native compactions that are stronger than references but not yet canon

## What Does Not Belong Here

- raw intake that still belongs in `knowledge/feedstock/`
- default-binding doctrine that belongs in `knowledge/canon/`
- deterministic mechanics that belong in `playbooks/`, `operators/`, or `validated-patterns/`
- ancestry-only material that belongs in `pedigree/`

## Housed Subtype

`knowledge/sigma/references/` is the housed subtype for evidence-rich reference substrates, imported compendia, and other source-proximate syntheses that Sigma and canon may compact upward from.

## Compatibility State

The shell currently carries an older physical tree at `knowledge/references/`.

Until staged rehousing is complete:

- treat `knowledge/references/` as the compatibility form of `knowledge/sigma/references/`
- place new classification language under Sigma terminology
- do not describe bare `references/` as the sovereign lane name

## Promotion Paths

- `knowledge/feedstock/` -> `knowledge/sigma/references/`
- `knowledge/sigma/references/` -> `knowledge/sigma/`
- `knowledge/sigma/` -> `knowledge/canon/`

Artifacts may also exit laterally to `playbooks/`, `operators/`, `validated-patterns/`, or `pedigree/` if that is their true class.
```

## 3. Compatibility Note Draft for the Existing `knowledge/references/` Tree

Recommended as a standalone note for insertion wherever the migration is announced:

```md
## Compatibility Note: Existing `knowledge/references/`

`knowledge/sigma/` is the ratified live secondary tier.

The pre-existing `knowledge/references/` tree remains in place temporarily as a housed compatibility subtree for `knowledge/sigma/references/`.

Until staged rehousing is complete:

- interpret `knowledge/references/*` as semantically equivalent to `knowledge/sigma/references/*`
- keep existing reference artifacts live and citable at their current paths
- route new secondary-tier doctrine to `knowledge/sigma/`
- route new reference substrates to Sigma semantics rather than treating bare `references/` as a separate lane
- do not use the legacy bare lane name in new law text, README text, or structural decisions

This compatibility rule preserves continuity for links, indexes, and downstream tooling while making Sigma the only live lane contract.
```

## 4. Minimal Migration Cautions for Staged Rehousing

- Do not create two authoritative roots. `knowledge/sigma/references/` and bare `knowledge/references/` cannot both behave as sovereign long-term lanes.
- Do not hard-rename the entire tree before README text, law text, and compatibility wording are in place. That only turns a semantic ratification into a path break.
- Do not treat physical relocation as promotion. Moving a file from bare `references/` into Sigma housing does not by itself make it Sigma doctrine.
- Preserve citation continuity. If any files are moved later, receipts or indexes need to capture the old-to-new path relationship.
- Freeze the terminology first. New docs should stop describing bare `references/` as the live tier even if the old tree remains on disk for a while.

## 5. Top Failure Modes If Sigma Ratification Is Implemented Naively

1. Bare `references/` survives as a de facto parallel lane, so Sigma exists in theory while the old name still governs practice.
2. A hard rename breaks links, indexes, prompts, and tooling that still point at `knowledge/references/`, creating unnecessary migration churn.
3. Imported reference substrates get misclassified as already-ratified Sigma doctrine merely because they were rehoused under a Sigma path.
4. Canon inflation resumes because teams bypass Sigma and promote material straight out of housed references.
5. Duplicate trees drift apart when some artifacts are edited under `knowledge/references/` and others under `knowledge/sigma/references/`.
6. README and law text diverge from the actual migration policy, leaving operators unsure whether to follow path reality or lane semantics.
7. Rehousing work gets mistaken for doctrinal adjudication, so the shell loses the distinction between taxonomy cleanup and knowledge promotion.

## Net Recommendation

Ratify Sigma in language immediately, house `references` under Sigma semantically, and keep the current `knowledge/references/` tree only as a temporary compatibility form until staged rehousing is ready.

That yields a stable near-term contract without reopening the decision:

- law speaks in Sigma terms
- README speaks in Sigma terms
- existing references remain readable in place
- future movement stays staged, receipted, and non-destructive
