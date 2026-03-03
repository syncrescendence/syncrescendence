# OpenClaw Kaizen Log

**Status**: initialized

Use this file to record compacted lessons that improve the OpenClaw playbook.

## Entry format

- **Date**
- **Source lineage**
- **Observed pattern or failure**
- **Compacted lesson**
- **Promotion target**
  - playbook doctrine
  - operator
  - hook
  - validator
  - runtime policy
  - constitutional law

## Initial seed lessons

### 2026-03-02 — Runtime identity must stay explicit

- **Source lineage**
  - live Ajna/Psyche repair work
  - [AGENT-RUNTIME-IDENTITIES-CC75.md](/Users/system/syncrescendence/00-ORCHESTRATION/state/impl/AGENT-RUNTIME-IDENTITIES-CC75.md)
- **Observed pattern or failure**
  - It is easy to accidentally conflate provider, account, and agent identity when repairing local runtime state.
- **Compacted lesson**
  - Runtime identity must be recorded explicitly and treated as shell structure, not incidental setup.
- **Promotion target**
  - playbook doctrine

### 2026-03-02 — Workspace memory is real but not sovereign

- **Source lineage**
  - OpenClaw memory architecture
  - Syncrescendence runtime/repo reconciliation work
- **Observed pattern or failure**
  - Workspace files are useful always-on memory but become dangerous when they drift from repo truth.
- **Compacted lesson**
  - Use workspace memory for live operation and continuity, but reconcile durable truth back into the repo.
- **Promotion target**
  - runtime policy

### 2026-03-02 — Event emission is the bridge out of runtime isolation

- **Source lineage**
  - Ajna event loop implementation
  - tool-stack reconciliation work
- **Observed pattern or failure**
  - Runtime state left inside OpenClaw becomes invisible and non-reviewable.
- **Compacted lesson**
  - Durable state changes should emit structured events that reconcile into repo memory and ontology.
- **Promotion target**
  - operator
