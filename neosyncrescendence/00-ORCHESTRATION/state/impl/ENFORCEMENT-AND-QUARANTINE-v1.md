# Enforcement and Quarantine v1

**Date**: 2026-03-02  
**Status**: constitutional redesign package  
**Purpose**: define the validator regime, sunset mechanics, quarantine flow, and enforcement thresholds required to make the next Syncrescendent shell durable under pressure

---

## 0. Why This Exists

The repo has already demonstrated the core lesson:

noncompliance persists wherever compliance is merely aesthetic.

This is why:

- `-INBOX` was "sunsetted" but continued to function as live response storage
- root kept accreting operators
- historical lanes remained active by habit
- artifact classes continued to bleed together

The shell will only harden if:

- legal classes exist,
- validator rules exist,
- misfiled work becomes expensive,
- and illegality routes into quarantine rather than silently becoming normal.

---

## 1. Core Doctrine

### 1.1 Compliance must be cheaper than drift

If the fastest path is still the wrong path, people and agents will continue using it.

Therefore:

- legal storage lanes must exist first,
- then writers redirect,
- then validators block,
- then legacy lanes become readonly or quarantined.

### 1.2 Quarantine is preferable to rejection

In a research system under active evolution, strict deletion is too destructive.

The right first response to illegality is usually:

- quarantine,
- reclassification,
- salvage,
- archive,

not destruction.

### 1.3 Provenance must survive enforcement

Enforcement should stop **new** entropy without erasing old evidence.

---

## 2. Enforcement Layers

## 2.1 Soft law

Examples:

- README guidance
- AGENTS instructions
- playbooks
- docs

Useful, but insufficient.

## 2.2 Build-time law

Examples:

- `make validate`
- path validation
- metadata checks

This is where most future shell law should live.

## 2.3 Write-time law

Examples:

- wrappers that write only into approved lanes
- bridge scripts that emit canonical metadata
- generated path normalization

This is how new work should be born correctly.

## 2.4 Commit-time law

Examples:

- pre-commit checks
- CI enforcement
- file-class violation checks

This is how drift becomes harder than compliance.

## 2.5 Runtime law

Examples:

- sanitizers
- event-id normalization
- runtime state collectors
- quarantine automation

This prevents live systems from leaking garbage back into durable truth.

---

## 3. Validator Classes

## 3.1 Artifact-class validator

Should eventually fail on:

- `PROMPT-*` outside prompt lanes
- `RESPONSE-*` outside response lanes
- handoffs outside handoff lanes
- generated configs modified at the wrong layer
- reports filed as responses

## 3.2 Sunset validator

Should eventually fail or warn on:

- new durable writes into deprecated lanes
- new top-level directories created without approval
- new root-level operators outside approved exceptions

## 3.3 Lineage validator

Should eventually fail or quarantine:

- prompt with no response/failure state
- response with no prompt reference and no orphaned-historical marker
- handoff with no workstream linkage
- backlog item with no Rosetta/Intent binding once the triad is live

## 3.4 Metadata validator

Should enforce minimum headers/frontmatter/sidecars for mature artifact classes.

## 3.5 Authority validator

Should prevent:

- generated files being treated as sources
- runtime state overwriting constitution
- projection/ontology artifacts being used as authority sources

---

## 4. Quarantine Model

## 4.1 What quarantine is for

Quarantine is the holding zone for artifacts that are:

- real
- non-duplicate
- probably useful
- but illegally filed or insufficiently linked

## 4.2 What quarantine is not for

- confirmed trash
- confirmed duplicates
- intentional canonical artifacts

Those should instead be:

- deleted if true duplicates,
- archived if historical,
- or properly filed if canonical.

## 4.3 Quarantine states

An artifact in quarantine should carry a reason:

- `misfiled`
- `missing-lineage`
- `deprecated-lane-write`
- `mixed-class`
- `unknown-authority`
- `needs-salvage`

## 4.4 Quarantine resolution outcomes

1. refile to proper lane
2. archive to provenance
3. compact into derivative artifact while preserving original
4. mark as duplicate and remove
5. leave in historical quarantine with explicit status

---

## 5. Sunset Law

Deprecation has four stages.

## Stage 1 — Announced

The successor lane exists.
Writers are informed.
No enforcement yet.

## Stage 2 — Redirected

Primary writers now use the new lane.
Legacy lane still accepts historical reads.

## Stage 3 — Warn-only enforcement

New writes to the old lane emit warnings or CI failures.

## Stage 4 — Hard sunset

New durable writes are blocked or quarantined.
Old lane becomes readonly or archival.

This is the correct treatment for lanes like `-INBOX`.

---

## 6. Root-Shell Enforcement

The root is where drift is most visible and most dangerous.

### Allowed at root

- deliberate constitutional entrypoints
- generated entrypoints meant to be root-facing
- core build entrypoints
- a narrow set of compatibility wrappers

### Not allowed at root by default

- new ad hoc reports
- new prompt/response artifacts
- new random operators
- runtime spill
- migration debris

Future validator should fail or warn on these automatically.

---

## 7. Pain Points this Must Address

## 7.1 Partial migration

The system currently contains many "we migrated, except not really" states.
Enforcement must prevent these from persisting indefinitely.

## 7.2 Near-duplicate shells

A new lane without redirect and block rules simply creates another near-duplicate shell.

## 7.3 Manual habit override

If humans or agents still need to remember where a file "should probably go," the law is too weak.

## 7.4 Imported history

Historical salvage must be exemptable without weakening the law for new work.

That implies separate modes:

- `live`
- `salvage`
- `archive-import`

## 7.5 Generator breakage

Enforcement cannot blindly break working automations like Hazel, Cowork, or Make.
Compatibility wrappers and transitional aliases are lawful and often necessary.

---

## 8. Suggested Rollout Sequence

1. finalize legal classes
2. create successor lanes
3. redirect active writers
4. add warn-only validators
5. add quarantine flow
6. harden to blocking validators
7. mark old lanes readonly

Do not invert this order.

---

## 9. Net Rule

The next shell is only real when illegal writes become mechanically difficult, visibly suspicious, and recoverable through quarantine rather than silently becoming the new normal.
