# Operators

This lane holds executable shell operators.

Current staged classes:
- validators
- CLI↔web-gap packet/bridge operators
- communications migration operators
- office bootstrap operators
- office topology refinement operators
- config operators
- runtime/reconciliation operators
- exocortex bridge operators
- acumen intelligence pipeline operators
- ontology operators
- machine/bootstrap operators
- development webshell operators

## Key surfaces

- [validators/artifact_law_inventory.py](/Users/system/syncrescendence/operators/validators/artifact_law_inventory.py)
- [validators/validate_tributary_disposition.py](/Users/system/syncrescendence/operators/validators/validate_tributary_disposition.py)
- [cli-web-gap](/Users/system/syncrescendence/operators/cli-web-gap)
- [migrate_communications_chain.py](/Users/system/syncrescendence/operators/migrate_communications_chain.py)
- [bootstrap_office.py](/Users/system/syncrescendence/operators/bootstrap_office.py)
- [office](/Users/system/syncrescendence/operators/office)
- [config](/Users/system/syncrescendence/operators/config)
- [runtime](/Users/system/syncrescendence/operators/runtime)
- [exocortex](/Users/system/syncrescendence/operators/exocortex)
- [acumen](/Users/system/syncrescendence/operators/acumen)
- [ontology](/Users/system/syncrescendence/operators/ontology)
- [machines](/Users/system/syncrescendence/operators/machines)
- [webshell](/Users/system/syncrescendence/operators/webshell)
- [migrate](/Users/system/syncrescendence/operators/migrate)

## Rule

New redesign operators should land here by default rather than at the repo root.

Legacy root operators are being internalized here in tranches; top-level copies remain transitional only until the shell cutover is complete.

## Authority

- [SCRIPT-OPERATOR-TAXONOMY-v1.md](/Users/system/syncrescendence/orchestration/state/impl/SCRIPT-OPERATOR-TAXONOMY-v1.md)
- [ARTIFACT-LAW-VALIDATOR-SPEC-v1.md](/Users/system/syncrescendence/orchestration/state/impl/ARTIFACT-LAW-VALIDATOR-SPEC-v1.md)

## Tributary Validator

`validate_tributary_disposition.py` is a deterministic, report-only validator for the tributary disposition CSV and ledger. It checks structural legality, legal transition sequences, custody joins, and verified-state hash obligations without mutating registry state or acting as an adjudication engine.

Repo-native report artifacts land at:
- [orchestration/state/TRIBUTARY-DISPOSITION-VALIDATION-REPORT.md](/Users/system/syncrescendence/orchestration/state/TRIBUTARY-DISPOSITION-VALIDATION-REPORT.md)
- [orchestration/state/TRIBUTARY-DISPOSITION-VALIDATION-REPORT.json](/Users/system/syncrescendence/orchestration/state/TRIBUTARY-DISPOSITION-VALIDATION-REPORT.json)
