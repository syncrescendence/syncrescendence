# Shell Risk and Edge-Case Register v1

**Date**: 2026-03-02  
**Status**: constitutional redesign package  
**Purpose**: enumerate the recurring failure modes, migration hazards, edge cases, and regime-level risks that the next Syncrescendent shell must explicitly handle

---

## 0. Why This Exists

The shell redesign will fail if it only models the clean case.

The repo’s history shows repeated pain points:

- stale authorities
- orphaned responses
- near-duplicate files and directories
- partial migrations
- context compaction loss
- free-floating backlog
- scripts proliferating faster than filing law

This register turns those into explicit design constraints.

---

## 1. Constitutional Risks

## 1.1 Ghost authority

**Pattern**
- a file is cited as authoritative across the system but does not cleanly exist at the expected live path

**Current example class**
- Rosetta and Intent Compass lineage

**Risk**
- ontology and canon gates depend on references with no visible living authority

**Design response**
- separate pedigree from live authority
- make live authority explicit and compact

## 1.2 Constitutional overgrowth

**Pattern**
- the constitution absorbs too many harness-specific details

**Risk**
- larger system prompts
- lower progressive disclosure
- more contradictions

**Design response**
- move native-grain doctrine into playbooks

---

## 2. Executive / Program Risks

## 2.1 Free-floating backlog

**Pattern**
- backlog exists as tasks but not as a visibly intention-bound program

**Risk**
- busywork queue replaces strategic execution

**Design response**
- mandatory Rosetta / Intent / playbook linkage for mature items

## 2.2 Intention drift

**Pattern**
- implementation continues after the active strategic frame has changed

**Risk**
- stale campaigns live on by inertia

**Design response**
- executive status fields and explicit deferred/parked/superseded law

---

## 3. Communications Risks

## 3.1 Orphaned response

**Pattern**
- response exists without prompt or explicit orphaned-historical status

**Risk**
- conclusions cannot be audited or compacted correctly

## 3.2 Prompt graveyard

**Pattern**
- prompts accumulate with no response, status, or derivative output

**Risk**
- fake lineage and noisy communications layer

## 3.3 Handoff collapse

**Pattern**
- handoffs become vague recaps rather than true state transfer

**Risk**
- context loss and recomputation loops

## 3.4 Log monoculture

**Pattern**
- everything becomes "a log"

**Risk**
- prompts, responses, reports, state, and retros all blur

---

## 4. Runtime Risks

## 4.1 Runtime as authority

**Pattern**
- whatever the live tool currently says becomes treated as truth

**Risk**
- repo sovereignty collapses

**Design response**
- runtime must reconcile back into repo truth rather than replace it

## 4.2 Projection inversion

**Pattern**
- ontology or dashboard starts being treated as the source rather than the mirror

**Risk**
- second brain / second canon

## 4.3 Hidden local state

**Pattern**
- a dotfile or app cache silently becomes the operative authority

**Risk**
- invisible drift and impossible archaeology

---

## 5. Exocortex Risks

## 5.1 Surface proliferation without taxonomy

**Pattern**
- every new external tool invents its own ingestion logic

**Risk**
- exocortex becomes a swamp

## 5.2 Subscription-worker fragility

**Pattern**
- browser relay works but is slow, gesture-heavy, and monopolizes the user’s interaction surface

**Risk**
- low operator trust, intermittent use, fragile fusion

**Design response**
- stronger gesture-vs-script bifurcation
- dedicated execution contexts
- queue discipline

## 5.3 API-cost inversion

**Pattern**
- a cheap subscription problem gets "solved" by expensive API usage

**Risk**
- unnecessary metered surface sprawl

---

## 6. Operator Risks

## 6.1 Root-script sprawl

**Pattern**
- operators accumulate at repo root because they are useful

**Risk**
- root loses institutional meaning

## 6.2 Bridge-reconcile conflation

**Pattern**
- external surface logic and truth normalization collapse into one operator

**Risk**
- brittle coupling and authority confusion

## 6.3 Transitional wrapper ossification

**Pattern**
- compatibility wrappers never die

**Risk**
- the transition layer becomes the permanent shell

---

## 7. Migration Risks

## 7.1 Rename-before-law

**Pattern**
- directories get renamed before artifact law and validators exist

**Risk**
- same chaos, new names

## 7.2 Double-live shells

**Pattern**
- successor lanes exist but legacy lanes remain active writers

**Risk**
- permanent near-duplicate system

## 7.3 Salvage overreach

**Pattern**
- historical cleanup mutates provenance too aggressively

**Risk**
- archaeology loss

## 7.4 Enforcement too early

**Pattern**
- validators block before successor lanes and wrappers are ready

**Risk**
- live system breakage and resentment toward the redesign

---

## 8. Harness-Specific Risks

## 8.1 False unification

**Pattern**
- system tries to make every harness behave identically

**Risk**
- lower performance and more fighting the tool

## 8.2 Prompt portability fantasy

**Pattern**
- a prompt or workflow is assumed transferable across surfaces

**Risk**
- degraded behavior and apparent inconsistency

## 8.3 Context overloading

**Pattern**
- too much doctrine loaded into active harness context

**Risk**
- attention diffusion and compaction loss

---

## 9. Human Factors Risks

## 9.1 Filing fatigue

**Pattern**
- the shell becomes so ceremonious that people revert to ad hoc habits

**Risk**
- the redesign gets bypassed in practice

**Design response**
- compliance must be simpler than improvisation

## 9.2 "We’ll sort it later"

**Pattern**
- temporary staging becomes permanent filing

**Risk**
- entropy returns immediately

## 9.3 Invisible edge ownership

**Pattern**
- no one knows who is responsible for moving an artifact to its lawful home

**Risk**
- stuck transitional states everywhere

---

## 10. Net Rule

The shell should not merely optimize for elegance in the happy path.

It should be designed so that:

- stale authorities are surfaced,
- illegal writes are intercepted,
- ambiguous lineage becomes visible,
- provenance survives migration,
- and the common failure modes are structurally harder than the compliant path.
