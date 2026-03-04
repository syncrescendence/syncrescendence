# Exocortex Annealing Path — CC80

**Date**: 2026-03-04  
**Status**: active execution contract  
**Class**: staged convergence plan

## Objective

Use the new teleology map to converge on a non-duplicative, enforceable exocortex that preserves sovereignty in-repo while letting external surfaces execute their best role.

Primary references:

- [EXOCORTEX-CANDIDATE-TELEOLOGY-CC80.md](/Users/system/syncrescendence/orchestration/state/impl/EXOCORTEX-CANDIDATE-TELEOLOGY-CC80.md)
- [EXOCORTEX-SURFACE-TAXONOMY-CC75.md](/Users/system/syncrescendence/orchestration/state/impl/EXOCORTEX-SURFACE-TAXONOMY-CC75.md)
- [CHAT-BUS-ARCHITECTURE-v1.md](/Users/system/syncrescendence/orchestration/state/impl/CHAT-BUS-ARCHITECTURE-v1.md)
- [IIC-GOVERNANCE-STAGE0-CC76.md](/Users/system/syncrescendence/orchestration/state/impl/IIC-GOVERNANCE-STAGE0-CC76.md)

## Annealing Rules

1. One primary surface per function, all others explicitly secondary.
2. Repo remains constitutional authority; no external tool can become law.
3. Promotion from stage0 to active requires replayable evidence.
4. Every active surface must have deterministic ingress and egress.
5. If a surface duplicates an existing primary and adds no unique leverage, quarantine it.

## Functional Rails (Locked)

- Repo force multiplier: `obsidian_repo_surface`.
- Context lakehouse and ontology data center: `notion_surface`.
- Source-to-canon mutability workflows: `coda_surface`.
- Technical know-how base: `confluence_surface`.
- Technical execution in-repo: `linear_surface`.
- Technical execution outside repo: `jira_surface`.
- Non-technical program aggregation: `clickup_surface`.
- Project breakout rooms: `basecamp_surface`.
- Metaconnections/databasal wiring: `airtable_surface`.
- Procedural knowledge execution: `ticktick_surface`.
- Project-based GTD execution: `todoist_surface`.
- Private manual lane: `things_surface` (non-automated).

## Modality Decision (Agentified vs Headless)

1. `headless` by default when the surface is a wiring/data plane:
   - `airtable_surface`
2. `agentified` by default when the surface is primarily human coordination UX:
   - `confluence_surface`, `clickup_surface`, `basecamp_surface`, `ticktick_surface`, `todoist_surface`
3. `hybrid` when both UI deliberation and machine integration are first-class:
   - `obsidian_repo_surface`, `notion_surface`, `coda_surface`, `linear_surface`, `jira_surface`
4. `manual_only` when platform capabilities block reliable automation:
   - `things_surface` (no official public API)
5. Promotion to headless backend is allowed only after stable API-based replay evidence and governance receipts.

## Phased Path

### Phase A — Freeze and Clean Boundaries (now)

Deliverables:

1. Write a surface registry that marks each candidate as `primary`, `secondary`, or `quarantined`.
2. For each non-primary surface, declare a single activation trigger (the condition that justifies use).
3. Add a policy check that rejects new surface docs unless role + anti-role are both present.

Exit criteria:

- No surface has ambiguous ownership.
- No function has two primaries.

### Phase B — Harden the P1 Core

Scope: `obsidian_repo_surface`, `notion_surface`, `coda_surface`, `linear_surface`, `airtable_surface`, existing chat bus.

Deliverables:

1. Obsidian promotion protocol: define exactly which notes can promote into repo artifacts and where.
2. Notion lakehouse contract: define context classes, ownership, and promotion boundaries.
3. Coda mutability contract: define source -> candidate -> canon state transitions.
4. Linear bridge protocol: map issue state transitions to repo events and artifact expectations.
5. Airtable wiring contract: define canonical keys and relationship contracts for cross-surface joins.
6. Chat bus archival policy: classify what is transient chat vs durable decision record.

Exit criteria:

- Every P1 surface emits durable artifacts through a deterministic path.
- Decision lineage can be reconstructed without reading full chat transcripts.

### Phase C — Controlled P2 Activation

Scope: `confluence_surface`, `jira_surface`, `clickup_surface`, `basecamp_surface`, `ticktick_surface`, `todoist_surface`, `things_surface`.

Deliverables:

1. Per-surface entry contract:
   - auth substrate
   - owner
   - allowed workloads
   - mandatory capture mode
   - modality class (`agentified`, `headless`, `hybrid`, `manual_only`)
   - promotion destination in repo
2. A quarantine rule for overlap:
   - if workload can already be completed by a primary + existing bridge, block activation.
3. One real workload pilot per activated surface before broader use.
4. `things_surface` governance note: explicit manual-only handling and no automation obligations.

Exit criteria:

- Each activated P2 surface passes one replay test and one lineage audit.
- No duplicate systems of record introduced.

### Phase D — Automation and Compression

Deliverables:

1. Auto-compaction flow:
   - chat and prompt/response residues -> periodic synthesis artifacts
   - synthesis artifacts -> policy/playbook updates where applicable
2. Add weekly drift checks:
   - role drift
   - ownership drift
   - capture mode drift
3. Build deprecation workflow:
   - mark stale surfaces
   - migration instructions
   - closure receipt

Exit criteria:

- Drift checks run on schedule.
- Stale surface count trends down, not up.

## Assignment Matrix

- Commander:
  - policy docs, wrappers, capture enforcement, repo-native validators.
- Manus:
  - external execution where bounded API runs are stronger than local relay.
- Human actions:
  - any browser OAuth, token rotation, or trust-bound account operations.

## Immediate Next Actions

1. Create `EXOCORTEX-SURFACE-REGISTRY.json` with `tier`, `role`, `anti_role`, `owner`, `status`.
2. Add `SURFACE-ACTIVATION-TRIGGERS.md` with one explicit trigger per secondary surface.
3. Add a validator script that fails when a surface artifact omits role/anti-role.
4. Write `OBSIDIAN-PROMOTION-CONTRACT.md` and wire it to artifact destinations.
5. Write `NOTION-LAKEHOUSE-CONTRACT.md`, `CODA-MUTABILITY-CONTRACT.md`, and `LINEAR-BRIDGE-CONTRACT.md`.
6. Write `AIRTABLE-METACONNECTIONS-CONTRACT.md` for keying/wiring across surfaces.
7. Add weekly drift report scaffold under `orchestration/state/impl/` and open execution tickets with acceptance tests.

## Risks and Countermeasures

- Risk: surface sprawl resumes through ad hoc exceptions.
  - Countermeasure: no exception without written trigger and owner.
- Risk: chat surfaces silently become systems of record.
  - Countermeasure: enforce mandatory promotion receipts for decisions.
- Risk: excessive governance slows execution.
  - Countermeasure: strict distinction between primary rails (fast path) and compliance rails (conditional path).

## Definition of Converged Exocortex

The exocortex is converged when:

1. Function-to-surface mapping is one-to-one at primary level.
2. All active surfaces have deterministic ingress/egress and replayable proofs.
3. Repo artifacts, not chat logs, are the durable decision memory.
4. New surfaces can be added without architectural drift or naming collisions.
