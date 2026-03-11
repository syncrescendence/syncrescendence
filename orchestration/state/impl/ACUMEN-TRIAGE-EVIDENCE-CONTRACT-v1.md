# Acumen Triage Evidence Contract v1

**Status**: staged  
**Class**: implementation law  
**Purpose**: define the repo-sovereign evidence family for Acumen triage decisions and sanitized model-call training receipts

## Why This Family Exists

Campaign 09 moves Acumen from scaffold into live operational flow.

That shift creates a new burden:

- triage decisions must survive beyond one runtime session
- model-call cost and failure metadata must be auditable
- prompt capture must stay within repo law and secret hygiene

The repo therefore keeps a small repo-native exception family for Acumen evidence.
This is lawful under the live-ledger family contract because the burden is still low-churn, authority-bearing, and easier to audit in-repo than through a hidden side channel.

## Surfaces

Append-only substrate:

1. `orchestration/state/registry/acumen-triage-decision-ledger.jsonl`
2. `orchestration/state/registry/acumen-training-corpus-ledger.jsonl`

Derived runtime surfaces:

1. `runtime/acumen/triage-decisions.jsonl`
2. `runtime/acumen/training-corpus.jsonl`

Validation and report surfaces:

1. `operators/acumen/rematerialize_evidence.py`
2. `operators/validators/validate_acumen_evidence.py`
3. `orchestration/state/ACUMEN-TRIAGE-EVIDENCE-REPORT.json`
4. `orchestration/state/ACUMEN-TRIAGE-EVIDENCE-REPORT.md`

## Derivation Rule

The append-only ledgers are the historical witness.

The runtime files are operational convenience views and must be rebuilt only from those ledgers.
If runtime rows drift from the deterministic rebuild, runtime becomes informative only until repaired.

## Capture Policy

Allowed in repo evidence:

- decision outcome
- channel and video identity
- packet path and packet digest
- prompt digest or input-summary metadata
- structured response digest
- usage, latency, retry, cost, and failure metadata

Forbidden in repo evidence:

- API keys
- authorization headers
- raw prompt bodies
- raw response bodies
- hidden prompt internals that exceed packet provenance, digest, or summary

## Family Rule

`decision_recorded` events carry the structured decision row used by Dawn Brief compilation.

`model_call_recorded` and `model_call_failed` events carry sanitized training-corpus rows that preserve:

- provider and model identity
- bounded request context
- packet provenance
- structured response validity
- retry, latency, usage, cost, and failure class

The training corpus is evidence for future analysis and tuning.
It is not permission to store raw prompts or secrets.

## Operational Expectation

Any real Acumen triage adapter must append a model-call event first or alongside the decision event, then rematerialize runtime surfaces and validate the family.

This keeps the call path explicit:

`runtime packet -> repo-native append-only evidence -> derived runtime queue -> Dawn Brief`
