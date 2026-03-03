# Lane Status Matrix v1

**Date**: 2026-03-02  
**Status**: tranche-01 control artifact  
**Purpose**: explicitly classify the legal status of the current major lanes so migration can proceed without hidden assumptions

---

## Status Vocabulary

- `live` — current authoritative lane for its class
- `live-transitional` — currently used and still lawful, but expected to hand off to a successor lane
- `legacy-readonly` — preserved for reading and provenance, no new durable writes should be encouraged
- `archive` — provenance storage, not active filing
- `mixed` — contains multiple artifact classes or legal roles and needs future disentangling

---

## Current Lane Classification

## Root constitutional veneers

- [AGENTS.md](/Users/system/syncrescendence/AGENTS.md): `live`
- [CLAUDE.md](/Users/system/syncrescendence/CLAUDE.md): `live` generated veneer
- [GEMINI.md](/Users/system/syncrescendence/GEMINI.md): `live` generated veneer
- root identity/extension files: `live-transitional`

## `engine/`

**Status**
- `live-transitional`

**Why**
- currently the dominant lawful prompt/packet lane
- still mixes prompt lineage with some older response artifacts and mise-en-place state

**Future**
- should hand off prompt filing authority to communications-law successor lanes

## `-INBOX/`

**Status**
- `live-transitional`

**Why**
- still actively used for responses
- already declared sunset in spirit, but not yet mechanically sunset

**Future**
- should become intake-only, then legacy-readonly or archive once successor response lane is live

## `agents/commander/outbox/handoffs/`

**Status**
- `live`

**Why**
- currently the cleanest handoff lane
- inventory confirms handoffs here are correctly filed

## `memory/`

**Status**
- `mixed`

**Why**
- contains legitimate runtime memory artifacts
- also contains legacy handoffs that are now misfiled under the new law

**Future**
- should remain for runtime/memory artifacts only
- historical/misfiled handoffs should move or be marked legacy

## `ascertescence/`

**Status**
- `mixed`

**Why**
- contains valuable provenance and historical synthesis
- also contains prompts and responses that are misfiled under the emerging communications law

**Future**
- likely split by class over time:
  - assessments / retros remain valuable
  - prompt/response items become historical lineage or archive

## `00-ORCHESTRATION/state/`

**Status**
- `live-transitional`

**Why**
- current runtime/state/implementation lane
- already serving as the practical control plane for many generated artifacts

**Future**
- should likely split into clearer runtime / program / registry / implementation outputs over time

## `00-ORCHESTRATION/state/impl/`

**Status**
- `live-transitional`

**Why**
- currently the design/package/output lane for major implementation artifacts
- useful and active, but broad

**Future**
- portions may eventually differentiate into:
  - assessments
  - implementation outputs
  - shell redesign package

## Successor charter lanes

- [communications](/Users/system/syncrescendence/communications): `live-transitional`
- [playbooks](/Users/system/syncrescendence/playbooks): `live-transitional`
- [operators](/Users/system/syncrescendence/operators): `live-transitional`
- [executive](/Users/system/syncrescendence/executive): `live-transitional`
- [program](/Users/system/syncrescendence/program): `live-transitional`

These now exist physically as tranche-01 charter lanes, but they are not yet the dominant write surfaces for most live workflows.

## `canon/`

**Status**
- `live`

**Why**
- still the active canonical knowledge and law lane

## `neocorpus/`

**Status**
- `live`

**Why**
- active distilled doctrine layer

## `corpus/`

**Status**
- `archive`

**Why**
- cold provenance and historical substrate

## `CLI-WEB-GAP/`

**Status**
- `live-transitional`

**Why**
- active design and script surface for a working subsystem
- likely to compact later into playbooks, operators, and exocortex lanes

---

## Immediate Implications

1. handoffs should continue using `agents/commander/outbox/handoffs/`
2. new prompts should continue using `engine/` until successor lanes exist
3. new responses may still land in `-INBOX/` for now, but this is transitional debt, not a solved state
4. `ascertescence/` should be treated as mixed historical value, not as a clean live communications lane
5. `memory/` needs selective cleanup because it still contains legacy misfiled handoffs

---

## Net Rule

No lane should be described as "deprecated" or "migrated" unless its current legal status is explicitly named in this matrix or a later successor to it.
