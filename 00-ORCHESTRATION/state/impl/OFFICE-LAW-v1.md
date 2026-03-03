# Office Law v1

**Date**: 2026-03-02  
**Status**: constitutional redesign package  
**Purpose**: define the lawful role of agent- or harness-local offices inside the successor shell

---

## 0. Why This Exists

The pre-syncrephoenix `agents/` structure proved something important:

- local offices are real
- local intake, memory, scratch space, and outgoing work are useful
- not all work should be funneled through one federal intake lane

What failed was not the office concept.
What failed was the coexistence of office-local logistics with ambiguous repo-global logistics.

This document preserves the office concept while forbidding that ambiguity.

---

## 1. Definition

An **office** is the local working domain of an agent or harness.

An office may contain:

- intake queues
- local memory
- scratch space
- outgoing work
- runtime-local state

An office is not the constitution, the executive, the backlog, or the registry.
It is a state/local execution surface inside the federal shell.

---

## 2. Federal Distinction

### Federal lanes

These remain repo-wide and authoritative:

- constitution
- executive
- program
- communications law
- operators
- pedigree
- registry

### Office-local lanes

These are allowed to differ by harness/agent:

- local inbox
- local memory cache
- local scratchpad
- local outbox
- local platform notes

The rule is simple:

- **federal lanes set the law**
- **offices do the situated work**

---

## 3. Office Functions

Offices are for:

1. local working-state that would create noise if promoted immediately
2. harness-specific control surfaces
3. resumable local execution
4. staging before promotion into federal communications or program lanes

Offices are not for:

1. replacing the communications lane
2. becoming hidden canonical memory
3. storing untraceable directives
4. shadowing federal backlog or intent

---

## 4. Minimal Office Shape

The old `agents/*` pattern remains the best pedigree.

Minimal lawful office shape:

- `inbox/`
- `memory/`
- `scratchpad/`
- `outbox/`
- `platform/` or equivalent harness-local control surface

Optional:

- `blocked/`, `done/`, `failed/`, `pending/` subdivisions under `inbox/`
- local runtime cache

---

## 5. Promotion Rules

Material leaves an office and becomes federal when it crosses one of these thresholds:

1. it becomes a prompt/packet or response with enduring lineage value
2. it becomes a handoff
3. it becomes a stable playbook insight
4. it affects executive or program truth
5. it becomes evidence used by the registry/ontology

If it does not cross those thresholds, it may remain office-local.

---

## 6. Anti-Patterns

Forbidden:

1. office-local `-INBOX` style graveyards
2. storing federal backlog items only in one office
3. letting office memory become the only copy of reasoning or state
4. using offices as silent archives
5. duplicating federal prompts/responses in multiple offices without lineage

---

## 7. Successor-Shell Implication

The successor shell now has an explicit office lane at:

- [offices](/Users/system/syncrescendence/offices)

That physicalization preserves the old `agents/` strength while keeping federal truth elsewhere.

The operating rule is:

- office-local work may live in `offices/`
- anything with federal lineage value must still be promoted into communications, executive, program, pedigree, or runtime

Office law is therefore no longer only a migration target.
It is live constitutional doctrine and a physically instantiated local layer.
