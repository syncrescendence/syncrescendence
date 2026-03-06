# Tributary Contract Hardening Synthesis v1

**Date**: 2026-03-06  
**Class**: assessment + adjudication + implementation handoff  
**Scope**: Batch 02 Codex swarm on tributary contract hardening

## 1. Executive Synthesis

Batch 02 is sufficient.

The contract layer is now defined well enough that the next wave should draft concrete artifacts instead of continuing interpretive archaeology. The main remaining work is to ratify and physicalize the narrow write set the coordinator identified.

The strongest adjudications are:

- one canonical migration control plane under `orchestration/state/registry/`
- restoration of `knowledge/sigma/` as the true lower-than-canon rung
- `knowledge/references/` demoted from whole-tier identity to housed subtype under Sigma
- `pedigree/` defined as a custody lane, not a generic archive shelf
- migration receipts routed to `pedigree/rehousing-receipts/`, not `communications/`
- `offices/` retained as the live root lane
- office directories anchored by stable office identity, not harness naming
- witness class, not prose quality, governs duplicate doctrine merge
- externalization permitted only after classification and compaction judgment
- repo ratifies, exocortex coordinates, ontology projects

## 2. Stable Convergences

### 2.1 Migration control plane

The registry is no longer optional.

The converged design is:

- `orchestration/state/registry/tributary-disposition-schema-v1.md`
- `orchestration/state/registry/tributary-disposition-registry.csv`
- `orchestration/state/registry/tributary-disposition-ledger.jsonl`

The registry holds current state per source artifact.

The ledger holds append-only mutation history.

Receipts, manifests, and promoted artifacts remain separate surfaces joined through explicit fields such as `candidate_id`, `merge_family_id`, `receipt_path`, `archive_manifest_path`, and `destination_artifact_path`.

### 2.2 Canon / Sigma / references

Batch 02 decisively restored the missing rung.

The governing stratification is:

- `knowledge/canon/` = bind-on-default operative scripture
- `knowledge/sigma/` = secondary doctrine repeatedly consulted by the shell
- `knowledge/sigma/references/` = compendia and evidence-rich substrates housed within Sigma
- `knowledge/feedstock/` = intake floor

The key clarification is that bare `references/` was naming part of the current occupant, not the real constitutional role of the tier.

### 2.3 Pedigree custody

`pedigree/` now has a real contract.

The converged split is:

- `pedigree/originals/`
- `pedigree/rehoused/`
- `pedigree/archive-manifests/`
- `pedigree/rehousing-receipts/`
- mandatory cautionary status, with physical `pedigree/cautionary/` optional in the first write set

Pedigree is for ancestry, custody, and warning, not for soft authority.

### 2.4 Agent-local promotion law

The most important routing distinction is now clear:

- `offices/` keeps local state, scratch, queue residue, and local logs
- `communications/` keeps routed lineage and durable inter-office artifacts
- `executive/` keeps only steering artifacts: `briefing`, `escalation`, or `summit`

Nothing should move directly from `offices/` to `executive/`.

The recommended root lane remains `offices/`, not `agents/`.

### 2.5 Witness precedence

Duplicate doctrine should be governed by witness class:

- live shell controls present behavior
- `neo` supplies default successor wording
- `old` remains mandatory annex witness where burden-bearing rationale would otherwise be lost
- unresolved families stay explicitly plural

This preserves compression without laundering authenticity.

### 2.6 Externalization and control-plane law

The externalization sequence is:

1. classify and bound
2. compact or designate residue
3. externalize or cull
4. ratify and register

The repo / exocortex / ontology boundary remains:

- repo ratifies
- exocortex coordinates
- ontology projects

No direction-changing truth may live only in exocortex or ontology form.

## 3. Adjudicated Collisions

### 3.1 Sigma restoration without abrupt breakage

`knowledge/references/` cannot remain the permanent name of the lower tier.

The coordinator’s two-step settlement is correct:

1. ratify `knowledge/sigma/` and `knowledge/sigma/references/`
2. then rehouse current `knowledge/references/*` into the Sigma subtree with receipts and compatibility notes

This avoids flattening Sigma while also avoiding a blind hard rename.

### 3.2 Migration receipts do not belong in communications

Live routing receipts and migration custody receipts are not the same artifact class.

The correct home for migration, rehousing, externalization, and cull proofs is `pedigree/rehousing-receipts/`.

### 3.3 Cautionary status is mandatory now; the folder is optional now

The semantic class must exist immediately.

The physical `pedigree/cautionary/` folder may be deferred if minimizing the first write pass matters more than immediate physical completeness.

### 3.4 `communications/dispatches/` should be physicalized immediately

The shell law already assumes a dispatch lane, but the directory is absent.

That is a small but real gap. It should be fixed in the next direct write pass.

## 4. Holistic Evaluation

Batch 02 succeeded for a specific reason: it stopped treating the migration problem as a folder-mapping problem and treated it instead as a contract problem.

The result is narrow, usable, and surprisingly coherent. There are very few open worldview disputes left in this layer. Most of the remaining uncertainty is implementation sequencing, compatibility handling, and how much to physicalize in the first write set.

The main remaining risks are:

1. delaying the direct write pass and letting the contract layer remain chat-only
2. over-expanding the first write set until it becomes another redesign program
3. hard-renaming `knowledge/references/` without compatibility notes
4. letting custody receipts leak into `communications/`
5. overloading `Sigma` with executable mechanics that belong elsewhere
6. failing to encode cautionary status in machine-readable form from the beginning

## 5. Smallest Safe Write Set

The coordinator’s minimum safe write set is correct:

1. `orchestration/state/registry/tributary-disposition-schema-v1.md`
2. `orchestration/state/registry/tributary-disposition-registry.csv`
3. `orchestration/state/registry/tributary-disposition-ledger.jsonl`
4. one compact law artifact for witness precedence, collision recording, externalization gating, and repo/exocortex/ontology lineage requirements
5. one knowledge-law update ratifying `knowledge/sigma/` and `knowledge/sigma/references/`
6. `knowledge/sigma/README.md`
7. one compact pedigree custody law artifact covering manifests, rehousing receipts, and cautionary status
8. one compact promotion-threshold law artifact for `offices/`, `communications/`, and `executive/`
9. `communications/dispatches/README.md`

That set is small enough to execute without reopening shell-wide redesign.

## 6. Next Batch Mandate

The next swarm should not ask what the contracts are.

It should ask for patch-ready drafts of the specific artifact set above.

That means Batch 03 should be a writing swarm with lanes for:

1. registry artifacts
2. Sigma ratification
3. pedigree custody law
4. promotion thresholds plus dispatch physicalization
5. witness / externalization / lineage law
6. first migration seed set
7. optional validator and template pack

## 7. Inputs

Primary response artifacts:

- `/Users/system/syncrescendence/communications/responses/RESPONSE-CODEX-SWARM-BATCH-02-LANE-00-COORDINATOR.md`
- `/Users/system/syncrescendence/communications/responses/RESPONSE-CODEX-SWARM-BATCH-02-LANE-01-DISPOSITION-REGISTRY.md`
- `/Users/system/syncrescendence/communications/responses/RESPONSE-CODEX-SWARM-BATCH-02-LANE-02-CANON-SIGMA-REFERENCE.md`
- `/Users/system/syncrescendence/communications/responses/RESPONSE-CODEX-SWARM-BATCH-02-LANE-03-PEDIGREE-AND-MANIFESTS.md`
- `/Users/system/syncrescendence/communications/responses/RESPONSE-CODEX-SWARM-BATCH-02-LANE-04-PROMOTION-THRESHOLDS.md`
- `/Users/system/syncrescendence/communications/responses/RESPONSE-CODEX-SWARM-BATCH-02-LANE-05-DUPLICATE-DOCTRINE-MERGE.md`
- `/Users/system/syncrescendence/communications/responses/RESPONSE-CODEX-SWARM-BATCH-02-LANE-06-SOURCE-LOG-EXTERNALIZATION.md`
- `/Users/system/syncrescendence/communications/responses/RESPONSE-CODEX-SWARM-BATCH-02-LANE-07-EXOCORTEX-ONTOLOGY-CONTRACT.md`
