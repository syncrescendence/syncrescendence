# Live Intent Compass Design v1

**Date**: 2026-03-02  
**Status**: constitutional redesign package  
**Purpose**: define the required live Intent Compass surface, its relationship to historical intention archaeology, and the minimum viable executive steering layer for the next shell

---

## 0. Why This Exists

The repo currently shows the same pattern as Rosetta:

- intent references remain load-bearing in canon, ontology contracts, and historical work
- many files still reference `ARCH-INTENTION_COMPASS.md`
- the live authoritative file is not cleanly surfaced in the current shell

This means executive direction is still conceptually central but institutionally obscured.

The shell needs a living executive surface again.

---

## 1. Role of the Live Intent Compass

The live Intent Compass is the executive steering surface for the current shell.

It exists to answer:

- what matters now?
- which campaigns are active?
- what has been deferred, parked, resolved, or superseded?
- which intentions steer current backlog and execution?
- which major directions are currently under review?

It is not the full archive of every historical intention.

---

## 2. Why It Is Load-Bearing

The current system still depends on it:

1. ontology gate requires `matched_intention`
2. canon still cites it as a governing executive artifact
3. backlog is supposed to bind upward to intention
4. many historical records and workstreams reference stable INT identifiers

Without a live Intent Compass:

- `matched_intention` becomes underconstrained
- backlog becomes free-floating
- executive direction has no compact operational home

---

## 3. Split Intent into Two Legal Surfaces

## 3.1 Intent Pedigree

**Purpose**
- preserve historical campaigns, prior intentions, supersessions, and why certain directions existed

**Class**
- executive provenance

## 3.2 Intent Live

**Purpose**
- expose the currently binding steering layer

**Class**
- executive source

**Properties**
- compact
- current
- operationally steerable
- explicit statuses

---

## 4. Minimum Viable Contents

The live Intent Compass should include, at minimum:

1. **intent_id**
2. **title**
3. **status**
   - active
   - deferred
   - parked
   - completed
   - superseded
4. **campaign / cluster**
5. **short statement of intent**
6. **review cadence or last review**
7. **pedigree reference**

Optional but useful:

- linked backlog/program items
- linked playbooks
- ownership / executive steward

---

## 5. Design Rules

## 5.1 Compactness

Live Intent must be short enough to actually steer work.
It cannot be a graveyard narrative.

## 5.2 Stability of IDs

Existing INT identifiers are valuable.
The live design should preserve them wherever possible rather than renumbering everything.

## 5.3 Explicit status

Intentions should not disappear by implication.
They should move between visible states.

## 5.4 Backlog binding

Mature backlog items should bind to live intentions.
If an intention is no longer live, the program should know whether the work is:

- obsolete,
- still valid under a new intention,
- or awaiting executive review.

---

## 6. Suggested Shape

A practical v1 file could look like:

```text
INTENT-COMPASS-v1.md
  executive preamble
  active intentions
  deferred intentions
  parked intentions
  resolved / superseded references
  campaign clusters
```

Possible future structured companion:

```text
INTENT-COMPASS-v1.json
```

for binding and validation.

---

## 7. Relationship to the Backlog

The live Intent Compass is not itself the backlog.

It should instead:

- define what deserves execution
- allow backlog items to bind upward
- make deferrals visible
- prevent program drift

This restores the lawful chain:

`Intent -> Program -> Execution`

instead of:

`Queue -> inertia -> ad hoc execution`

---

## 8. Relationship to the Ontology

The live Intent Compass should be upstream of ontology.

Ontology may project intention state, but must not originate or silently redefine it.

`matched_intention` should therefore point into a live executive surface, not a ghost reference.

---

## 9. Edge Cases

## 9.1 Historical intention only

May stay in pedigree without being live.

## 9.2 One backlog item maps to several intentions

Allowed, but one primary intention should be named.

## 9.3 Intention changes meaning over time

The live surface should preserve the stable ID if the continuity is real; otherwise use supersession explicitly.

## 9.4 Completed but still informative intentions

Do not delete them.
Mark them completed and keep lightweight references in the live surface or its immediate companion.

---

## 10. Recovery Sequence

1. enumerate currently referenced INT identifiers in canon, backlog, runtime, and lineage
2. recover the minimum active/deferred/parked set needed now
3. define the live executive surface with explicit statuses
4. preserve broader history as pedigree
5. update program items and future validators to bind against the live surface

---

## 11. Net Rule

The live Intent Compass is the compact executive surface that makes the shell teleologically steerable in the present tense.

Without it, the system can execute, but it cannot clearly say why now.
