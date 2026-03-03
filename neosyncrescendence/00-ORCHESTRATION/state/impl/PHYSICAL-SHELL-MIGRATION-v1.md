# Physical Shell Migration v1

**Date**: 2026-03-02  
**Status**: target shell and migration design  
**Purpose**: map the current physical repo shell to the target Syncrescendent shell, define what stays, what moves, what becomes legacy, and what must be enforced during migration

---

## 0. Why This Exists

The logical architecture is now clearer than the physical shell.

Current reality:

- root still mixes constitutional files, generated entrypoints, runtime-adjacent files, and many operators
- communications lineage is partially split between `engine/`, `-INBOX/`, `agents/.../handoffs/`, and `ascertescence/`
- playbooks are more conceptual than physically formalized
- operators are scattered

The goal is not cosmetic tidiness.
The goal is to make the physical shell express the institutional architecture.

---

## 1. Design Principles

1. **Logical shell first, migration second, rename last**
2. **Lossless migration by default**
3. **Explicit legacy state beats silent half-migration**
4. **Compatibility wrappers are allowed temporarily**
5. **Validation, aliases, and quarantines are part of migration**

---

## 2. Current Root-Shell Problem

Current root contains:

- constitutional entrypoints
- generated agent entrypoints
- build machinery
- bridge operators
- bootstrap scripts
- ontology service
- relay wrappers
- legacy directories

This is workable, but not institutionally legible.

---

## 3. Target Top-Level Shell

The next shell should converge toward these primary root lanes:

- `constitution/`
- `executive/`
- `program/`
- `playbooks/`
- `communications/`
- `operators/`
- `runtime/`
- `exocortex/`
- `registry/`
- `archive/`
- `knowledge/`
- `agents/`
- `machine/`

Not every lane must be physically introduced at once. Some can be staged through aliases and progressive migration.

---

## 4. Recommended Mapping from the Current Shell

## 4.1 Constitution

### Keep root-facing for now

- [AGENTS.md](/Users/system/syncrescendence/AGENTS.md)
- [CLAUDE.md](/Users/system/syncrescendence/CLAUDE.md)
- [GEMINI.md](/Users/system/syncrescendence/GEMINI.md)
- [CLAUDE-EXT.md](/Users/system/syncrescendence/CLAUDE-EXT.md)
- [GEMINI-EXT.md](/Users/system/syncrescendence/GEMINI-EXT.md)
- [OPENCLAW-EXT.md](/Users/system/syncrescendence/OPENCLAW-EXT.md)
- [IDENTITY.md](/Users/system/syncrescendence/IDENTITY.md)
- [SOUL.md](/Users/system/syncrescendence/SOUL.md)
- [TOOLS.md](/Users/system/syncrescendence/TOOLS.md)
- [USER.md](/Users/system/syncrescendence/USER.md)

### Longer-term target

- move constitutional sources under `constitution/`
- keep root entrypoints as deliberate public veneers or generated outputs

## 4.2 Executive

### Current partial lane

- `00-ORCHESTRATION/state/` contains some executive-adjacent material

### Target

- `executive/intent/`
- `executive/campaigns/`
- `executive/deferred/`

## 4.3 Program

### Current lane

- `00-ORCHESTRATION/state/IMPLEMENTATION-BACKLOG.md`
- `00-ORCHESTRATION/state/IMPLEMENTATION-MAP.md`

### Target

- `program/backlog/`
- `program/maps/`
- `program/tranches/`

## 4.4 Playbooks

### Current reality

- mostly diffuse across neocorpus, canon, AGENTS, and operational docs

### Target

- `playbooks/claude-code/`
- `playbooks/codex/`
- `playbooks/gemini/`
- `playbooks/openclaw/`
- `playbooks/oracle/`
- `playbooks/perplexity/`
- `playbooks/cowork/`
- `playbooks/manus/`

## 4.5 Communications

### Current fragmented lanes

- `engine/`
- `-INBOX/`
- `agents/.../handoffs/`
- `ascertescence/`
- assorted assessments in `00-ORCHESTRATION/state/impl/`

### Target

- `communications/prompts/`
- `communications/responses/`
- `communications/dispatches/`
- `communications/handoffs/`
- `communications/assessments/`
- `communications/retros/`

### Migration stance

- do not delete current lanes immediately
- first create mapping and validation
- then migrate writing surfaces
- then demote legacy lanes to readonly/archive

## 4.6 Operators

### Current state

- many root-level `.py` and `.sh` operators
- CLI-WEB-GAP scripts partly organized already

### Target

- `operators/stage/`
- `operators/validate/`
- `operators/reconcile/`
- `operators/bridge/`
- `operators/observe/`
- `operators/enforce/`
- `operators/bootstrap/`
- `operators/migrate/`

### Compatibility exception

Root wrappers may remain temporarily if external tools like Hazel or Make targets depend on stable paths.

## 4.7 Runtime

### Current lane

- `00-ORCHESTRATION/state/`
- `memory/`
- `configs/`

### Target

- `runtime/state/`
- `runtime/events/`
- `runtime/reconciliation/`
- `runtime/manifests/`

This can be staged gradually because current tooling already depends on `00-ORCHESTRATION/state/`.

## 4.8 Exocortex

### Current state

- bridges at root
- policies in orchestration state
- relay assets in `CLI-WEB-GAP/` and `00-ORCHESTRATION/relay/`

### Target

- `exocortex/surfaces/`
- `exocortex/accounts/`
- `exocortex/relay/`
- `exocortex/policies/`

## 4.9 Registry

### Current state

- ontology service files at root
- domain docs under `00-ORCHESTRATION/state/impl/`

### Target

- `registry/ontology/`
- `registry/api/`
- `registry/reports/`

## 4.10 Archive / Provenance

### Current state

- `corpus/`
- parts of `ascertescence/`
- superseded docs scattered

### Target

- `archive/corpus/`
- `archive/superseded/`
- `archive/historical-shells/`

`corpus/` may remain root-facing if its role as cold archive remains central, but its legal status should be explicit.

## 4.11 Knowledge

### Current state

- `neocorpus/`
- `canon/`

### Target

- `knowledge/neocorpus/`
- `knowledge/canon/`

This is a longer-term move and should not happen until artifact law and lineage are stricter.

---

## 5. Migration States

Every current lane should be labeled as one of:

- `live`
- `live-transitional`
- `legacy-readonly`
- `quarantined`
- `archive`

Suggested current statuses:

- `AGENTS.md` and rendered config surface: `live`
- `00-ORCHESTRATION/state/`: `live-transitional`
- `engine/`: `live-transitional`
- `-INBOX/`: `live-transitional` or `legacy-readonly` once replacement exists
- `ascertescence/`: `live-transitional`
- root operator scatter: `live-transitional`
- `corpus/`: `archive-live`
- `neocorpus/`: `live`
- `canon/`: `live`

---

## 6. Migration Order

## Phase 1 — Law before movement

1. artifact law
2. triad reconstitution
3. operator taxonomy
4. playbook law

## Phase 2 — New target lanes

1. introduce the new physical lanes
2. add README / charter docs in each
3. add alias/mapping notes

## Phase 3 — Writer redirection

1. redirect new prompts/responses to communications law lanes
2. redirect new operators into operator lanes
3. preserve wrappers where needed

## Phase 4 — Validator enforcement

1. reject new writes to sunset lanes
2. quarantine misfiled artifacts
3. verify lineage metadata

## Phase 5 — Historical salvage

1. map old prompts/responses
2. reclassify or archive old handoffs and logs
3. preserve provenance and aliases

## Phase 6 — Rename if still justified

Only after the logical shell has functionally taken over.

---

## 7. Edge Cases

## 7.1 Compatibility wrappers

If Hazel, Make, Cowork, or external automation expects a stable path, preserve a wrapper rather than breaking the live system mid-migration.

## 7.2 Dotfiles and local harness state

Tool-private dotfiles such as `.claude/` and `.openclaw/` are adapters and local runtime surfaces, not constitutional lanes. They should remain tool-native and not be treated as the shell’s authority.

## 7.3 Generated root veneers

Root-facing generated files are acceptable when they are clearly generated entrypoints rather than hand-edited authorities.

## 7.4 Archive relocation risk

Do not move archive/provenance lanes in a way that obscures original archaeology.

---

## 8. Pain-Point Corrections

This migration is explicitly designed to correct:

- root-shell script spill
- prompt/response orphaning
- partial deprecations
- playbook absence
- live law hidden inside reports
- runtime truth mixed with constitutional truth

---

## 9. Net Rule

The next shell should make it possible to infer, from path alone:

- the authority class of the artifact,
- the kind of work it belongs to,
- whether it is live or legacy,
- and what may legally write to it.

If path no longer carries institutional meaning, the shell has not been truly remade.
