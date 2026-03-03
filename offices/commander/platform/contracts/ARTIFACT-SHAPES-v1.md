# Commander Artifact Shapes v1

Commander uses these local forms:

- `TASK` / dispatch envelope
- `RECEIPT`
- `RESULT`
- `CONFIRM`
- `ALERT`
- `BRIEFING`
- `EXECLOG`

These are local office envelopes first. They become federal truth only after lawful promotion into `communications/`, `executive/`, `program/`, `runtime/`, or another sanctioned lane.

Local routing:

- dispatches -> [outbox/dispatches](/Users/system/syncrescendence/offices/commander/outbox/dispatches)
- receipts -> [outbox/receipts](/Users/system/syncrescendence/offices/commander/outbox/receipts)
- results -> [outbox/results](/Users/system/syncrescendence/offices/commander/outbox/results)
- confirms / alerts / briefings arrive through inbox state lanes
- raw execution traces belong in [platform/logs](/Users/system/syncrescendence/offices/commander/platform/logs)

## Mandatory Envelope Fields

Every cross-office artifact should preserve enough metadata to support:

- routing
- receipt discipline
- escalation
- lawful closure
- retrospective audit

Minimum live fields by shape:

- `TASK`: from, to, reply-to, issued-at, line id or task id, objective, expected output, decision envelope, completion condition
- `RECEIPT`: task reference, claimer, claimed-at, acceptance or refusal state, next action
- `RESULT`: line/task reference, producer, status, summary, artifacts changed, verification/evidence, next promotion target
- `CONFIRM`: result reference, recipient, completion state, closure timestamp, remaining follow-up if any
- `ALERT`: subject, severity, affected lane/office, immediate implication, expected owner
- `BRIEFING`: situation, scope, stakes, current state, requested decision or orientation
- `EXECLOG`: bounded execution trace, not hidden reasoning canon

## Templates

- [TASK-ENVELOPE-TEMPLATE.md](/Users/system/syncrescendence/offices/commander/platform/contracts/TASK-ENVELOPE-TEMPLATE.md)
- [RECEIPT-TEMPLATE.md](/Users/system/syncrescendence/offices/commander/platform/contracts/RECEIPT-TEMPLATE.md)
- [RESULT-TEMPLATE.md](/Users/system/syncrescendence/offices/commander/platform/contracts/RESULT-TEMPLATE.md)
- [CONFIRM-TEMPLATE.md](/Users/system/syncrescendence/offices/commander/platform/contracts/CONFIRM-TEMPLATE.md)

## Translation from Pedigree

Recovered predecessor strengths that survive here:

- explicit `Reply-To` and `CC` expectations
- objective lock before work starts
- receipts as closure gate
- results and confirms as separate artifacts
- execution traces kept distinct from results

Federal promotion still applies. These are local forms first, not automatic federal truth.
