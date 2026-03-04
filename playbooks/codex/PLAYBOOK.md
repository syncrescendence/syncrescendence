# Codex Playbook

**Status**: stage0-v1  
**Class**: harness playbook  
**Authority chain**: constitution -> executive intention -> program -> playbook -> runtime surface / operators  
**Primary sources**:
- [AGENTS.md](/Users/system/syncrescendence/AGENTS.md)
- [CODEX-COMMAND-ATOMS-CC79.md](/Users/system/syncrescendence/playbooks/codex/references/CODEX-COMMAND-ATOMS-CC79.md)
- [HARNESS-CAPABILITY-REGISTRY-CC79.md](/Users/system/syncrescendence/orchestration/state/impl/HARNESS-CAPABILITY-REGISTRY-CC79.md)
- [CC79-HARNESS-INGEST-AND-GRADING.md](/Users/system/syncrescendence/communications/assessments/CC79-HARNESS-INGEST-AND-GRADING.md)

## 0. What This Surface Is For

Codex is the terminal coding harness bound to the Adjudicator lane and used for implementation + verification where repo-native execution is required.

## 1. Verified Command Atoms (CC79 Local)

- `codex --telemetry`
- `codex apply --patch <file>`

These are the only command atoms currently promoted from the CC79 registry as `T0/probe_pass`.

## 2. Guardrails

- treat all non-`T0/T1` codex command claims as unverified
- do not promote speculative codex subcommands into operators
- keep codex behavior subordinate to artifact law and federal lane law

## 3. Promotion Rule

New codex capabilities require:

1. command probe evidence in the capability registry
2. provenance link to source response segment
3. explicit playbook or operator delta commit
