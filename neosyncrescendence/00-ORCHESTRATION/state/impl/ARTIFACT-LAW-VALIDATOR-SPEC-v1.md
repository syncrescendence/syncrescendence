# Artifact Law Validator Spec v1

**Date**: 2026-03-02  
**Status**: executable design spec  
**Purpose**: define the first validator regime required to enforce shell redesign law without prematurely breaking the live system

---

## 0. Why This Exists

The redesign package is now clear enough to specify enforcement.

The key lesson from repo history is already canonical:

- validate before rename
- redirect before block
- do not rely on operator memory for compliance

This document defines the validator regime that should follow from the redesign package.

---

## 1. Scope

This validator should eventually enforce:

- artifact-class law
- sunset law
- lineage law
- authority law
- root-shell discipline

But it should do so in staged mode.

---

## 2. Staged Enforcement Modes

## Mode 0 — Inventory only

Behavior:

- detect possible violations
- emit report only
- never fail build

Use:

- initial archaeology
- baseline measurement

## Mode 1 — Warn only

Behavior:

- emit warnings
- return nonzero only if explicitly configured

Use:

- once successor lanes exist
- while habits are still changing

## Mode 2 — Quarantine eligible

Behavior:

- warn
- optionally route machine-generated outputs into quarantine
- fail on only the clearest violations

Use:

- once primary writers have been redirected

## Mode 3 — Hard fail

Behavior:

- block noncompliant new writes

Use:

- only after successor lanes and compatibility wrappers are proven

---

## 3. Validator Families

## 3.1 Path validator

Checks:

- forbidden artifact classes in forbidden lanes
- new root-level spill
- writes to sunsetted directories

## 3.2 Naming validator

Checks:

- prompt/response/handoff naming conventions
- missing stable identifiers
- ambiguous filename classes

## 3.3 Lineage validator

Checks:

- prompt without terminal state
- response without prompt linkage or orphan marker
- handoff without workstream linkage
- assessment without cited lineage

## 3.4 Authority validator

Checks:

- generated file edited directly
- runtime artifact treated as constitutional source
- projection artifact treated as authority

## 3.5 Program-binding validator

Checks:

- mature backlog items lacking `intent_ref`
- mature backlog items lacking `rosetta_ref`
- missing execution surface or playbook references where required

---

## 4. First Violation Set

The first version should be conservative.

Recommended first hard checks:

1. new `PROMPT-*` outside approved prompt lanes
2. new `RESPONSE-*` outside approved response lanes
3. new handoff files outside approved handoff lane
4. new root-level `.py` or `.sh` files outside an explicit allowlist
5. direct edits to generated harness outputs

Recommended warn-only checks:

1. prompt with no response yet
2. response without explicit linkage
3. writes to `-INBOX` after successor lane exists
4. backlog items missing upward binding

---

## 5. Allowlists

Because the current shell is transitional, validator must support explicit allowlists.

Examples:

- compatibility wrappers like [finalize_cowork_relay_job.py](/Users/system/syncrescendence/finalize_cowork_relay_job.py)
- current root constitutional veneers
- still-live transitional lanes

Allowlists must be:

- small
- explicit
- reviewed regularly

An allowlist is a temporary membrane, not a permanent excuse.

---

## 6. Quarantine Behavior

Machine-emitted violations should prefer quarantine where safe.

Example flows:

- misfiled machine-generated response -> quarantine + warning
- machine-generated report in wrong lane -> quarantine + warning
- direct human edit to generated file -> hard fail, no quarantine

Not every violation is recoverable automatically.

---

## 7. Output Artifacts

The validator itself should emit:

- human-readable report
- machine-readable report
- optional quarantine manifest

Suggested future locations:

- `runtime/state/`
- or transitional equivalent under `00-ORCHESTRATION/state/`

---

## 8. Rollout Order

1. inventory mode against current shell
2. warn-only mode in CI
3. add successor lanes
4. redirect active writers
5. enable first hard failures
6. expand enforcement gradually

This preserves the canonical rule:

**validation before structural change**

---

## 9. Net Rule

The validator should make illegal filing visible early, inconvenient next, and impossible only after the compliant path exists and works.
