# Implementation Tranche AN — Acumen CC88 Ingestion And Triage Operationalization

- **Tranche**: AN
- **program_id**: `TRANCHE-AN`
- **intent_refs**: `INT-SHELL-001`, `INT-SHELL-003`, `INT-SHELL-005`
- **rosetta_refs**: `operator`, `knowledge lane`, `exocortex`, `runtime`, `live-ledger`, `projection`
- **execution_surface**: `program/IMPLEMENTATION-TRANCHE-AN-ACUMEN-CC88-INGESTION-AND-TRIAGE-OPERATIONALIZATION.md`
- **lineage_or_origin**: Tranche S wave0 baseline, live wave0 execution proof, and the post-Campaign-08 pivot ruling

## Purpose

Take the Acumen pipeline from wave0 executable scaffold to the first real CC88 operational batch.

This tranche should close the gap between:

- sample metadata and manual fixtures
- real channel polling
- real triage invocation
- durable decision evidence
- repeatable Dawn Brief production

## Tasks

1. implement a YouTube ingestion worker over the Acumen registry with cadence-aware polling and cursor discipline
2. implement Gemini triage adapters with strict JSON output parsing, cost guardrails, and retry/failure logging
3. create triage-decision and training-corpus append-only surfaces
4. upgrade the Acumen pipeline flow to run poll -> triage -> queue -> Dawn Brief
5. harden Make targets, runtime outputs, and runbook instructions for repeated operation
6. integrate existing YouTube exocortex capture machinery only where it reduces duplication without splitting intake sovereignty

## Promotion / Completion Criteria

- the registry is not only valid but actually polled
- new uploads can become triage packets or triage decisions without handcrafted fixture files
- decision and model-call evidence land in append-only surfaces
- the pipeline can produce a Dawn Brief from a real poll/triage path
- cost, identity, and failure states are visible in runtime status

## Receipts

- [ACUMEN-INTELLIGENCE-PIPELINE-ADOPTION-CC87.md](/Users/system/syncrescendence/orchestration/state/impl/ACUMEN-INTELLIGENCE-PIPELINE-ADOPTION-CC87.md)
- [ACUMEN-INTELLIGENCE-PIPELINE-WAVE0-RUNBOOK-CC87.md](/Users/system/syncrescendence/orchestration/state/impl/ACUMEN-INTELLIGENCE-PIPELINE-WAVE0-RUNBOOK-CC87.md)
- [CAMPAIGN-08-PROJECTION-GOVERNANCE-AND-SECOND-WIDENING-PREP-SYNTHESIS-v1.md](/Users/system/syncrescendence/orchestration/state/impl/CAMPAIGN-08-PROJECTION-GOVERNANCE-AND-SECOND-WIDENING-PREP-SYNTHESIS-v1.md)
