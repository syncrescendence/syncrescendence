# Response

**Response ID**: `RSP-20260306-first-migration-seed-set`  
**Surface**: `codex_parallel_session`  
**Date received**: `2026-03-06`  
**Dispatch packet**: `PKT-20260306-codex-swarm-batch-03-lane-06-first-migration-seed-set`  
**Result state**: `complete`  
**Receipt artifact**:
  - `communications/responses/RESPONSE-CODEX-SWARM-BATCH-03-LANE-06-FIRST-MIGRATION-SEED-SET.md`

## Returned Content

Assumption for this tranche:

- seed rows should enter the registry as `adjudicated` or `scheduled`, not `executed`, unless the move is a pure compatibility-safe custody action
- the first tranche should prefer doctrinal families with clear witness hierarchy and low topology risk
- Sigma moves should start with compatibility rehousing, not mass semantic promotion

## 1. First Candidate Rows To Enter The Registry

These are the first ten rows worth seeding because they are high-authority, repeatedly cited, and narrow enough to batch without reopening whole-repo census work.

| candidate_id | source_tributary | source_path | target_class | proposed disposition | planned destination_artifact_path | merge_family_id | why first |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `cand-old-artifact-protocol-01` | `syncrescendence_old` | `/Users/system/Desktop/syncrescendence.old/01-CANON/CANON-00011-ARTIFACT_PROTOCOL-cosmos.md` | `canon` | `merge-promote` with `old` as annex witness | `/Users/system/syncrescendence/orchestration/state/impl/SYNCRESCENDENT-ARTIFACT-LAW-v1.md` | `mf-artifact-protocol-v1` | already has a live shell counterpart; high authority and low ambiguity |
| `cand-neo-artifact-protocol-01` | `syncrescendence_pre_schematic_design` | `/Users/system/Desktop/syncrescendence_pre_schematic_design/neocanon/CANON-1003-ARTIFACT_PROTOCOL.md` | `canon` | `merge-promote` with `neo` as base witness | `/Users/system/syncrescendence/orchestration/state/impl/SYNCRESCENDENT-ARTIFACT-LAW-v1.md` | `mf-artifact-protocol-v1` | strongest successor-shell wording for artifact governance |
| `cand-old-memory-architecture-01` | `syncrescendence_old` | `/Users/system/Desktop/syncrescendence.old/01-CANON/CANON-25000-MEMORY_ARCH-lattice.md` | `canon` | `merge-promote` with `old` as burden witness | `/Users/system/syncrescendence/knowledge/canon/MEMORY-ARCHITECTURE-v1.md` | `mf-memory-architecture-v1` | shell-sovereignty family with strong current relevance |
| `cand-neo-memory-architecture-01` | `syncrescendence_pre_schematic_design` | `/Users/system/Desktop/syncrescendence_pre_schematic_design/neocanon/CANON-3004-MEMORY_ARCHITECTURE.md` | `canon` | `merge-promote` with `neo` as base witness | `/Users/system/syncrescendence/knowledge/canon/MEMORY-ARCHITECTURE-v1.md` | `mf-memory-architecture-v1` | clearest shell-fit formulation of memory law |
| `cand-old-context-transition-01` | `syncrescendence_old` | `/Users/system/Desktop/syncrescendence.old/01-CANON/CANON-25100-CONTEXT_TRANS-lattice.md` | `canon` | `merge-promote` with `old` as annex witness | `/Users/system/syncrescendence/knowledge/canon/CONTEXT-TRANSITION-v1.md` | `mf-context-transition-v1` | directly governs continuation, resumability, and deletion discipline |
| `cand-neo-context-transition-01` | `syncrescendence_pre_schematic_design` | `/Users/system/Desktop/syncrescendence_pre_schematic_design/neocanon/CANON-3005-CONTEXT_TRANSITION.md` | `canon` | `merge-promote` with `neo` as base witness | `/Users/system/syncrescendence/knowledge/canon/CONTEXT-TRANSITION-v1.md` | `mf-context-transition-v1` | strongest successor-shell framing for handoff and continuity |
| `cand-old-research-protocols-01` | `syncrescendence_old` | `/Users/system/Desktop/syncrescendence.old/01-CANON/CANON-30330-RESEARCH_PROTOCOLS-asteroid-TECH_STACK-comet-INTELLIGENCE.md` | `sigma` | `merge-promote` with `old` as annex witness | `/Users/system/syncrescendence/knowledge/sigma/RESEARCH-PROTOCOLS-v1.md` | `mf-research-protocols-v1` | durable doctrine with clear Sigma placement and high operational yield |
| `cand-neo-research-protocols-01` | `syncrescendence_pre_schematic_design` | `/Users/system/Desktop/syncrescendence_pre_schematic_design/neocanon/CANON-3006-RESEARCH_PROTOCOLS.md` | `sigma` | `merge-promote` with `neo` as base witness | `/Users/system/syncrescendence/knowledge/sigma/RESEARCH-PROTOCOLS-v1.md` | `mf-research-protocols-v1` | portable, successor-fit substrate for the same family |
| `cand-old-lineage-01` | `syncrescendence_old` | `/Users/system/Desktop/syncrescendence.old/01-CANON/CANON-00002-LINEAGE-cosmos.md` | `pedigree` | `dual-witness retain` | `/Users/system/syncrescendence/pedigree/ROSETTA-STONE.live.md` | `dwf-lineage-v1` | high-authority ancestry material that should not be flattened into one paragraph |
| `cand-neo-lineage-01` | `syncrescendence_pre_schematic_design` | `/Users/system/Desktop/syncrescendence_pre_schematic_design/neocanon/CANON-2009-INTELLECTUAL_LINEAGE.md` | `pedigree` | `dual-witness retain` | `/Users/system/syncrescendence/pedigree/ROSETTA-STONE.live.md` | `dwf-lineage-v1` | compatible successor-shell summary witness for the same ancestry family |

Registry note:

- rows 1-8 should be seeded as `adjudicated`
- rows 9-10 should be seeded as `scheduled` if the dual-witness custody artifacts are not yet written
- the planned canon and Sigma destination paths above are future promotion targets, not proof that those files already exist

## 2. First Merge Families And Dual-Witness Families To Seed

### A. Merge families to seed immediately

These are the safest first families because witness hierarchy is already clear.

| family_id | family | base witness | required annex witness | first destination |
| --- | --- | --- | --- | --- |
| `mf-artifact-protocol-v1` | artifact protocol | `neo CANON-1003-ARTIFACT_PROTOCOL.md` | `old CANON-00011-ARTIFACT_PROTOCOL-cosmos.md` | `/Users/system/syncrescendence/orchestration/state/impl/SYNCRESCENDENT-ARTIFACT-LAW-v1.md` |
| `mf-memory-architecture-v1` | memory architecture | `neo CANON-3004-MEMORY_ARCHITECTURE.md` | `old CANON-25000-MEMORY_ARCH-lattice.md` | `/Users/system/syncrescendence/knowledge/canon/MEMORY-ARCHITECTURE-v1.md` |
| `mf-context-transition-v1` | context transition | `neo CANON-3005-CONTEXT_TRANSITION.md` | `old CANON-25100-CONTEXT_TRANS-lattice.md` | `/Users/system/syncrescendence/knowledge/canon/CONTEXT-TRANSITION-v1.md` |
| `mf-research-protocols-v1` | research protocols | `neo CANON-3006-RESEARCH_PROTOCOLS.md` | `old CANON-30330-RESEARCH_PROTOCOLS-asteroid-TECH_STACK-comet-INTELLIGENCE.md` | `/Users/system/syncrescendence/knowledge/sigma/RESEARCH-PROTOCOLS-v1.md` |

### B. Dual-witness families to seed, not force-merge, in tranche 1

These should enter the registry now, but should remain explicitly plural until a later pass writes honest live derivatives.

| family_id | family | reason to hold dual witness |
| --- | --- | --- |
| `dwf-lineage-v1` | lineage / intellectual lineage | ancestry and tributary debt are the point; flattening destroys provenance |
| `dwf-principles-v1` | principles | clause harvest is lawful, but neither witness should be silently swallowed whole |
| `dwf-evaluation-v1` | evaluation / resolutions | live shell has fragments only; full singular promotion would overclaim current ratification |
| `dwf-agentic-constitution-v1` | agentic constitution / operating laws | live shell controls present behavior, but upstream rationale remains burden-bearing |
| `dwf-syncrescendence-v1` | north-star / scripture family | teleology is authoritative but not yet suited for single live constitutional promotion |
| `dwf-feed-curation-v1` | feed curation / IIC residue | still tied to non-restored topology; preserve dual witness rather than laundering the conflict |

## 3. First Sigma Rehousing Targets

These are compatibility-safe because they are already clearly reference substrates. The first move is semantic and custody-safe: rehouse them under Sigma without pretending that path motion equals doctrinal promotion.

| source_path | first target_path | move type | why safe first |
| --- | --- | --- | --- |
| `/Users/system/syncrescendence/knowledge/references/README.md` | `/Users/system/syncrescendence/knowledge/sigma/references/README.md` | `subtree-sync` | sets the lane contract and stops new docs from treating bare `references/` as sovereign |
| `/Users/system/syncrescendence/knowledge/references/NEOCORPUS-CATEGORY-INDEX-v1.md` | `/Users/system/syncrescendence/knowledge/sigma/references/NEOCORPUS-CATEGORY-INDEX-v1.md` | `subtree-sync` | index artifact is pure compatibility scaffolding |
| `/Users/system/syncrescendence/knowledge/references/NEOCORPUS-INTERNALIZATION-v1.md` | `/Users/system/syncrescendence/knowledge/sigma/references/NEOCORPUS-INTERNALIZATION-v1.md` | `subtree-sync` | already functions as an internalization note rather than live law |
| `/Users/system/syncrescendence/knowledge/references/neocorpus/multi-agent-systems/` | `/Users/system/syncrescendence/knowledge/sigma/references/neocorpus/multi-agent-systems/` | `subtree-sync` | directly supports current orchestration and constitution work while remaining clearly reference-first |
| `/Users/system/syncrescendence/knowledge/references/neocorpus/prompt-engineering/` | `/Users/system/syncrescendence/knowledge/sigma/references/neocorpus/prompt-engineering/` | `subtree-sync` | high-yield repeated-use substrate, but not canon or live shell law |
| `/Users/system/syncrescendence/knowledge/references/neocorpus/openclaw/` | `/Users/system/syncrescendence/knowledge/sigma/references/neocorpus/openclaw/` | `subtree-sync` | clearly bounded, evidence-rich technical reference family with no claim to live authority |

Sigma rehousing rule:

- write one compatibility receipt per subtree or metadata artifact
- keep the original path live until the compatibility note and receipts exist
- do not count bare path relocation as promotion into Sigma doctrine

## 4. First Manifest And Rehousing-Receipt Candidates

### A. Manifest candidates

| candidate path | manifest type | scope |
| --- | --- | --- |
| `/Users/system/syncrescendence/pedigree/archive-manifests/MANIFEST-old-doctrinal-tranche-01-20260306.md` | `tranche` | rows 1, 3, 5, 7, 9 from the first registry seed set |
| `/Users/system/syncrescendence/pedigree/archive-manifests/MANIFEST-neo-doctrinal-tranche-01-20260306.md` | `tranche` | rows 2, 4, 6, 8, 10 from the first registry seed set |
| `/Users/system/syncrescendence/pedigree/archive-manifests/MANIFEST-lineage-dual-witness-tranche-01-20260306.md` | `family` | `dwf-lineage-v1` preserved witnesses and their relationship to `ROSETTA-STONE.live.md` |
| `/Users/system/syncrescendence/pedigree/archive-manifests/MANIFEST-sigma-compatibility-tranche-01-20260306.md` | `tranche` | the six Sigma rehousing targets above |

### B. Rehousing-receipt candidates

| candidate path | receipt type | covers |
| --- | --- | --- |
| `/Users/system/syncrescendence/pedigree/rehousing-receipts/RECEIPT-compact-then-promote-artifact-protocol-20260306-01.md` | `compact-then-promote` | `mf-artifact-protocol-v1` source witnesses to live artifact-law destination |
| `/Users/system/syncrescendence/pedigree/rehousing-receipts/RECEIPT-compact-then-promote-memory-architecture-20260306-02.md` | `compact-then-promote` | `mf-memory-architecture-v1` source witnesses to planned canon destination |
| `/Users/system/syncrescendence/pedigree/rehousing-receipts/RECEIPT-compact-then-promote-context-transition-20260306-03.md` | `compact-then-promote` | `mf-context-transition-v1` source witnesses to planned canon destination |
| `/Users/system/syncrescendence/pedigree/rehousing-receipts/RECEIPT-compact-then-promote-research-protocols-20260306-04.md` | `compact-then-promote` | `mf-research-protocols-v1` source witnesses to planned Sigma destination |
| `/Users/system/syncrescendence/pedigree/rehousing-receipts/RECEIPT-preserve-copy-lineage-dual-witness-20260306-05.md` | `preserve-copy` | `dwf-lineage-v1` witnesses retained explicitly under pedigree law |
| `/Users/system/syncrescendence/pedigree/rehousing-receipts/RECEIPT-subtree-sync-sigma-compatibility-20260306-06.md` | `subtree-sync` | `knowledge/references/*` compatibility rehousing into `knowledge/sigma/references/*` |

## 5. Top Failure Modes If The Seed Set Is Too Ambitious Or Too Timid

### A. If too ambitious

1. The tranche silently becomes a full migration census and stalls before any registry rows are actually ratified.
2. Mixed families such as `agentic constitution`, `principles`, or `feed curation` get force-merged before topology conflicts are preserved.
3. Sigma rehousing turns into a hard rename of all `knowledge/references/`, breaking compatibility before receipts and notes exist.
4. Planned canon targets are treated as already-written law, so the registry overstates what has actually been promoted.
5. `pedigree/` absorbs bulk doctrinal debris without bounded manifests, recreating an undisciplined archive shelf.

### B. If too timid

1. The registry starts with only metadata or receipts and still lacks any burden-bearing doctrinal families.
2. Merge-family law stays theoretical because no family is actually seeded with candidate rows and destination paths.
3. Sigma remains ratified only in prose while bare `knowledge/references/` continues acting like the real lane.
4. Lineage and other dual-witness families stay unregistered, so later promotions lose the ancestry record that should constrain them.
5. The next pass has to re-decide the same first tranche instead of executing it.

## Bottom Line

The smallest useful first seed set is:

- four merge families with eight doctrinal source rows
- one explicit dual-witness family with two pedigree rows
- six compatibility-safe Sigma rehousing targets
- four manifests and six receipts to prove the moves

That is large enough to make the registry real, but still narrow enough to avoid reopening contract settlement or attempting whole-repo migration in one pass.
