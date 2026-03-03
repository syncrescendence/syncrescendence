# Syncrescendent Artifact Law v1

**Date**: 2026-03-02  
**Status**: constitutional redesign package  
**Purpose**: define the legal artifact classes, allowed writers, storage law, lineage rules, and enforcement contract for the next Syncrescendent shell

---

## 0. Why This Exists

The current system has already proven that these layers can work:

- compiled constitutional configs
- live agent runtimes
- event reconciliation
- exocortex bridges
- ontology projection
- CLI-to-web relay

What has not been formalized with equal rigor is **artifact law**.

That gap is what causes:

- root-shell cruft
- orphaned prompts and responses
- mixed classes of documents in the same directory
- unclear authority boundaries
- duplicate or near-duplicate files
- partial migrations like `-INBOX` being "sunsetted" without true enforcement

This document defines the legal classes of artifacts in the next shell and the rules that govern them.

---

## 1. Core Doctrine

### 1.1 Four Distinctions

Every durable file belongs to exactly one of these domains:

1. **Law**  
   Defines what the system is allowed to be and do.

2. **Direction**  
   Defines what the system is currently trying to do.

3. **Execution**  
   Captures what the system is currently doing or has just done.

4. **Provenance**  
   Preserves where knowledge, decisions, or artifacts came from.

Most repo cruft came from collapsing these domains together.

### 1.2 Authority Ladder

From highest to lowest:

1. Metaphysics / Teleology
2. Constitution
3. Executive Intention
4. Program / Backlog
5. Playbook
6. Communications lineage
7. Runtime / state
8. Projection / registry
9. Archive / provenance

Lower layers may not silently overwrite higher layers.

### 1.3 One File, One Class

A file may have multiple references and many consumers, but only one legal class.

Examples:

- A prompt is not a log.
- A response is not a handoff.
- A handoff is not a retrospective.
- A generated config is not a constitutional source.
- A runtime snapshot is not an ontology source of truth.

---

## 2. Legal Artifact Classes

## 2.1 Constitutional Sources

**Purpose**
- define shared law, invariants, vocabulary, and governing contracts

**Examples**
- `AGENTS.md`
- live Rosetta artifact
- boundary contract
- ontology gate
- execution routing doctrine

**Allowed writers**
- Sovereign-approved agent edits only
- validated build or policy pipeline may render derivative artifacts from these

**Storage rule**
- lives in constitution-bearing lanes only
- must never be buried in inboxes, logs, or reports

**Lineage rule**
- every constitutional change must have:
  - a semantic commit
  - a derived output refresh if relevant
  - regression validation if it affects generated or enforced behavior

## 2.2 Executive Direction

**Purpose**
- encode current strategic priorities, active intentions, campaigns, and sovereign focus

**Examples**
- live Intent Compass
- active campaign directives
- explicit deferred commitments

**Allowed writers**
- Sovereign or delegated executive orchestration surface

**Storage rule**
- lives in executive lane, not mixed with backlog or reports

**Lineage rule**
- every major program or implementation item must link upward to one or more executive directives

## 2.3 Program / Backlog

**Purpose**
- convert intention into sequenced work

**Examples**
- implementation backlog
- implementation map
- migration queue
- tranche lists

**Allowed writers**
- Commander / delegated execution planners / validated program generators

**Storage rule**
- backlog files live in the program lane
- not in corpus, not in canon, not in engine

**Lineage rule**
- every program item should bind upward to:
  - intention
  - Rosetta concept(s)
  - owning playbook if applicable

## 2.4 Playbooks

**Purpose**
- preserve native grain for each harness or operational surface

**Examples**
- Claude Code playbook
- Codex playbook
- Gemini playbook
- OpenClaw playbook
- Oracle playbook
- Perplexity playbook
- Cowork playbook
- Manus playbook
- Feedcraft surface playbook

**Allowed writers**
- agents working in that harness domain
- synthesis and compaction pipelines that promote repeated patterns into doctrine

**Storage rule**
- playbooks are first-class and separate from prompts, logs, and runtime

**Lineage rule**
- playbooks may cite prompts/responses/logs but are not themselves those things

## 2.5 Communications Lineage

Communications artifacts are not all the same.

### Prompt

**Purpose**
- outbound dispatch packet or prompt artifact

**Rule**
- must have a corresponding response, failure record, or explicit abandoned status

### Response

**Purpose**
- inbound answer or return payload from an external surface or agent

**Rule**
- must remain sibling or linked lineage to its originating prompt

### Dispatch Record

**Purpose**
- metadata about a run: when sent, by whom, via which surface, for what role

### Handoff

**Purpose**
- transfer state between sessions or agents

**Rule**
- handoffs are lossless operational continuity artifacts
- they are not generic summaries

### Assessment / Retrospective

**Purpose**
- evaluate what a prompt-response cycle, system run, or migration taught

**Rule**
- assessments point to lineage; they do not replace it

## 2.6 Operational Outputs

**Purpose**
- derived but durable products of work

**Examples**
- sitreps
- implementation briefs
- migration plans
- assessments
- schematic docs
- compliance audits

**Allowed writers**
- execution surfaces and synthesis agents

**Storage rule**
- outputs live in output or implementation lanes, not in inboxes or constitutional lanes

## 2.7 Runtime State

**Purpose**
- factual records of what is currently running or recently happened

**Examples**
- runtime snapshots
- surface status files
- event ledgers
- reconciliation status
- generated manifests

**Allowed writers**
- runtime probes
- reconciler scripts
- deployment/status collectors

**Storage rule**
- runtime state is explicit, localizable, and dated
- runtime state never pretends to be constitutional law

## 2.8 Projection / Registry

**Purpose**
- typed downstream mirror of already-normalized truth

**Examples**
- ontology records
- dashboards
- public API outputs

**Rule**
- projection cannot authoritatively mutate law, playbooks, or lineage

## 2.9 Provenance / Archive

**Purpose**
- preserve originals, superseded artifacts, and historical shells

**Examples**
- corpus
- superseded responses
- archived prompts
- pre-remediation shells

**Rule**
- provenance is lossless
- archival does not equal authority

---

## 3. Metadata Law

Every durable artifact class should eventually carry a minimum metadata contract.

## 3.1 Required fields by default

- `artifact_class`
- `authority_level`
- `status`
- `origin`
- `lineage_parent` or explicit `lineage_root`
- `last_verified` when applicable

## 3.2 Additional required fields for dispatch lineage

- `surface`
- `sender`
- `recipient_role`
- `prompt_id`
- `response_id`
- `dispatch_date`
- `derived_outputs`

## 3.3 Additional required fields for program items

- `intent_ref`
- `rosetta_ref`
- `playbook_ref` when applicable
- `execution_surface`

---

## 4. Storage Law

## 4.1 The next shell must separate these physically

- constitutional sources
- executive direction
- program / backlog
- playbooks
- communications lineage
- outputs
- runtime state
- archive / provenance

## 4.2 Co-location rules

Allowed:
- prompt and response as siblings within a lineage lane
- report and the lineage it references linked by metadata or path
- runtime snapshot and its JSON twin in the same state lane

Forbidden:
- prompts mixed with canon or constitutional sources
- responses landing in a deprecated inbox with no lineage metadata
- handoffs living among prompts or generic logs
- outputs mixed with constitutional files at root

## 4.3 Root-shell law

Repo root should contain only:

- constitutional entrypoints
- generated surface entrypoints that are intentionally root-facing
- build and validation machinery
- top-level sovereign identity files explicitly designated as such
- no drifting operational artifacts

Root should not become a script graveyard, response graveyard, or runtime spill zone.

---

## 5. Compaction Law

Compaction is not cleanup. It is an architectural process.

## 5.1 Canonical compaction paths

- logs -> regulation / QA / automation
- prompts + responses -> prompt primitives / reusable patterns / skills / hooks
- research -> neocorpus -> canon or program delta
- repeated scripts -> hardened operators
- recurring outputs -> dashboards / registries / automated reports

## 5.2 Provenance preservation

Compaction never destroys provenance by default.

Instead:

- original remains in archive/provenance lane
- distilled form becomes the live artifact
- linkage remains explicit

## 5.3 Anti-pattern

Deleting the raw lineage because a distilled derivative exists is constitutionally wrong unless a file is confirmed duplicate garbage.

---

## 6. Enforcement Contract

Taste and reminders are insufficient. Enforcement must be mechanical.

## 6.1 Validator responsibilities

The next validator layer should eventually fail on:

- new `PROMPT-*` files outside approved communications lanes
- new `RESPONSE-*` files outside approved communications lanes
- new handoffs outside approved handoff lane
- writes into explicitly sunsetted directories
- constitutional files written by generated pipelines
- generated files edited directly

## 6.2 Quarantine

Files that violate artifact law should not silently become canonical.

They should be routed to a quarantine/staging lane where they can be:

- reclassified
- linked correctly
- archived
- or rejected

## 6.3 Deprecation

A directory is not deprecated because a memo says so.

A directory is deprecated when:

1. a successor lane exists,
2. writers are redirected,
3. validation detects new writes,
4. migration/alias policy is explicit.

---

## 7. Edge Cases and Pain Points

## 7.1 Prompt without response

Allowed only if explicitly marked:

- `abandoned`
- `superseded`
- `failed_to_dispatch`

Otherwise it is incomplete lineage.

## 7.2 Response without prompt

May happen during salvage or imported history, but must be marked:

- `orphaned_historical_response`

and queued for linkage or archival.

## 7.3 Handoff vs log

If the file exists to let another session continue the work, it is a handoff.
If it merely records what happened, it is a log.

## 7.4 Assessment vs output

If it evaluates lineage or decisions, it is an assessment.
If it exists as a direct product or deliverable, it is an output.

## 7.5 Script-generated reports

The fact that a report is generated does not make it runtime state.
Its class depends on its function:

- status snapshot -> runtime state
- compliance report -> output / assessment
- manifest -> generated state

## 7.6 Old shell remnants

Historical directories can remain for provenance, but their legal status must be explicit:

- `live`
- `legacy-readonly`
- `quarantined`
- `superseded`

---

## 8. Immediate Implications

This document implies the next redesign pass must produce:

1. a Rosetta / Intent / Backlog triad restoration design,
2. a playbook layer,
3. a communications-law directory design,
4. a script/operator taxonomy,
5. validators that enforce these classes.

---

## 9. Net Rule

The next shell must make the legal class of every durable artifact obvious.

If an informed operator cannot answer, at a glance:

- what class this file is,
- what authority it has,
- where it should live,
- what it derives from,
- and what may legally rewrite it,

then the shell is still underdesigned.
