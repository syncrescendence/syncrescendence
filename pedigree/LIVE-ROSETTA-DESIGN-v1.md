# Live Rosetta Design v1

**Date**: 2026-03-02  
**Status**: constitutional redesign package  
**Purpose**: define the required live Rosetta surface, its relationship to pedigree material, and the minimum viable shape needed to restore semantic constitutional authority

---

## 0. Why This Exists

The repo currently demonstrates a clear contradiction:

- Rosetta is still cited as a constitutional vocabulary authority
- ontology gates and historical prompts still depend on it
- historical references point to paths like `engine/REF-ROSETTA_STONE.md`
- those paths do not currently resolve as a live authoritative file

So the system still relies on Rosetta conceptually while lacking a clearly surfaced live Rosetta institutionally.

This document defines what the live Rosetta must be.

---

## 1. Role of the Live Rosetta

The live Rosetta is the constitutional vocabulary surface for the current shell.

It exists to answer, in compact operational form:

- what does this term mean here?
- what are the current semantic families?
- what aliases or supersessions exist?
- which terms are live, historical, deprecated, or superseded?
- which categories are allowed for canonical and ontological use?

It is not the complete archaeology of every formulation.

---

## 2. Why Rosetta Is Still Load-Bearing

The repo still depends on it in several ways:

1. ontology gates refer to Rosetta-based category alignment
2. historical prompts and mise-en-place materials still cite `REF-ROSETTA_STONE.md`
3. canon still treats Rosetta as part of the constitutional layer
4. the shell redesign itself requires a semantic DNA source

Without a live Rosetta:

- category law becomes fuzzy
- ontology binding becomes partially ghosted
- playbooks lose a shared vocabulary substrate

---

## 3. Split Rosetta into Two Legal Surfaces

## 3.1 Rosetta Pedigree

**Purpose**
- preserve the original conceptual inventions, historical formulations, supersessions, and semantic archaeology

**Class**
- constitutional provenance

**Properties**
- larger
- richer
- historical
- may include multiple formulations and prior variants

## 3.2 Rosetta Live

**Purpose**
- provide the currently binding constitutional vocabulary

**Class**
- constitutional source

**Properties**
- compact
- operational
- explicit about status and aliases
- sufficient for ontology, canon, playbooks, and backlog linkage

---

## 4. Minimum Viable Contents

The live Rosetta does not need to reproduce all historical nuance on day one.

It must, at minimum, include:

1. **term**
2. **canonical definition**
3. **semantic family / category**
4. **status**
   - live
   - deprecated
   - superseded
   - historical-alias
5. **aliases**
6. **pedigree reference**
7. **notes on current operational usage**

---

## 5. Suggested Shape

A practical v1 live Rosetta should likely look like:

```text
ROSETTA-STONE-v1.md
  preamble
  semantic families
  term registry
  alias and supersession notes
  operational usage notes
  linkage to pedigree
```

Possible future structured companion:

```text
ROSETTA-STONE-v1.json
```

for machine validation and ontology/binding support.

---

## 6. Semantic Families the Live Rosetta Must Support

The exact set should be derived from pedigree and current usage, but the live file should be able to express at least:

- constitutional / governance terms
- orchestration terms
- agent / harness roles
- memory and compaction terms
- exocortex terms
- ontology / registry terms
- production / feed / IIC terms where already mature

The live Rosetta should not attempt to canonize immature vocabulary prematurely.

---

## 7. Design Rules

## 7.1 Compactness

Live Rosetta must remain compact enough to be:

- read by humans quickly
- cited by validators and gates
- referenced by playbooks

## 7.2 Pedigree linkage

Every major live term should point back to pedigree rather than trying to embed all history inline.

## 7.3 No ghost terms

If a term is required by ontology, playbook law, canon, or backlog binding, it must exist either:

- in live Rosetta,
- or as a clearly marked unresolved required term queue.

## 7.4 No silent aliasing

Historical variants should not float invisibly.
If a term was renamed, superseded, or narrowed, the live Rosetta must say so.

---

## 8. Operational Consumers

The live Rosetta should be usable by:

- ontology gates
- canon promotion logic
- backlog/program binding
- harness playbooks
- communications and packet conventions

This is why it must remain compact and explicitly current.

---

## 9. Edge Cases

## 9.1 Term exists only in pedigree

That means it is not currently binding unless promoted into live Rosetta.

## 9.2 Term is widely used but poorly defined

It should enter the live Rosetta as a minimal provisional entry rather than remain invisible.

## 9.3 Term is philosophically important but operationally immature

Pedigree may contain it richly while live Rosetta gives it:

- deferred
- not-yet-binding
- reserved

status.

## 9.4 Category disagreement

If a term’s family is contested, the live Rosetta should record the current operational choice and point to pedigree debate.

---

## 10. Recovery Sequence

1. enumerate all references to Rosetta in canon, engine, runtime law, and current doctrine
2. extract the minimum currently-required live term set
3. build the compact live Rosetta file
4. mark aliases and supersessions
5. preserve larger archaeology as pedigree
6. redirect validators and canon references to the live surface

---

## 11. Net Rule

The live Rosetta is not optional lore.

It is the compact constitutional vocabulary surface without which the rest of the shell cannot remain semantically coherent.
