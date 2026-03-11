# Live-Ledger Domain Register Audit Report

Report-first audit of register coherence against landed family artifacts.

## Summary

- register: `orchestration/state/registry/live-ledger-domain-register.csv`
- rows: 3
- coherent rows: 3
- findings: 0
- errors: 0
- warnings: 0
- phase drift findings: 0
- append-only drift findings: 0
- stale note findings: 0
- status: `PASS`

## Domain Readout

| Domain | Claimed Phase | Expected Phase | Claimed Append Surface | Actual Append Surface | Findings |
|---|---|---|---|---|---|
| tributary_disposition | `phase1_repo_proof` | `phase1_repo_proof` | `orchestration/state/registry/tributary-disposition-ledger.jsonl` | `orchestration/state/registry/tributary-disposition-ledger.jsonl` | 0 |
| office_harness_state | `phase3_projection_open` | `phase3_projection_open` | `orchestration/state/registry/office-harness-binding-ledger.jsonl` | `orchestration/state/registry/office-harness-binding-ledger.jsonl` | 0 |
| config_surface_state | `phase1_repo_proof` | `phase1_repo_proof` | `orchestration/state/registry/config-surface-state-ledger.jsonl` | `orchestration/state/registry/config-surface-state-ledger.jsonl` | 0 |

## Findings

- none
