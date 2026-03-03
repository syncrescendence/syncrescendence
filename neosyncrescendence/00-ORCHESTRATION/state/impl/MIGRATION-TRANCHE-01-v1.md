# Migration Tranche 01 v1

**Date**: 2026-03-02  
**Status**: executable design spec  
**Purpose**: define the first low-risk migration tranche that begins shell reconstitution without repeating rename-first or cleanup-first failure patterns

---

## 0. Goal

Tranche 01 is not the file move.

It is the first safe transition from:

- design package

to:

- executable shell change

without destabilizing the live system.

---

## 1. Tranche 01 Objectives

1. establish successor lanes conceptually and minimally physically
2. introduce validator inventory mode
3. define compatibility exceptions explicitly
4. stop new entropy before large migration begins

This tranche is about control surfaces, not mass movement.

---

## 2. What Tranche 01 Should Do

## 2.1 Create lane charters only

Create the minimal successor-lane documentation for:

- communications
- playbooks
- operators
- executive
- program

These can begin as README or charter files.

The purpose is:

- make the future lanes real,
- give writers somewhere lawful to target,
- avoid premature relocation.

## 2.2 Add validator inventory mode

Implement a first validator that:

- inventories prompt/response/handoff placement
- inventories root-level operator sprawl
- inventories direct writes to transitional legacy lanes

It should report only, not block.

## 2.3 Define compatibility allowlist

Examples:

- root wrappers required by Hazel or existing automations
- root constitutional entrypoints
- still-live generated veneers

## 2.4 Mark lane statuses

At minimum, document whether these are:

- live
- live-transitional
- legacy-readonly
- archive

for:

- `engine/`
- `-INBOX/`
- `ascertescence/`
- `00-ORCHESTRATION/state/`
- root operator files

---

## 3. What Tranche 01 Should Not Do

1. no mass file relocation
2. no broad top-level renames
3. no hard-fail validators yet
4. no deletion of historical material except confirmed duplicates
5. no breakage of current relay, runtime, or bridge paths

This is how Tranche 01 avoids the INT-2210 pattern.

---

## 4. Why This Tranche First

Because the repo’s repeated failure mode is:

- feeling the disorder,
- moving a lot of things,
- then discovering the law was still implicit

Tranche 01 inverts that:

- name the new lanes
- measure drift
- preserve compatibility
- then move

---

## 5. Deliverables

Tranche 01 should end with:

1. lane-charter docs
2. first validator in inventory mode
3. allowlist file
4. lane-status matrix
5. zero breakage of live tool stack

---

## 6. Exit Criteria

Tranche 01 is complete when:

- successor lanes exist in documented form
- the validator can tell you where the current shell violates the new law
- compatibility exceptions are explicit rather than implicit
- no live automation or bridge path was broken

---

## 7. Net Rule

Tranche 01 succeeds if it makes the shell measurable and steerable without yet making it brittle.
