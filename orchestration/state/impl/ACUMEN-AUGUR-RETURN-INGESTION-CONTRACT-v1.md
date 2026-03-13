# Acumen Augur Return Ingestion Contract v1

**Status**: staged
**Class**: implementation law
**Purpose**: define the first lawful repo-side path from a landed Augur verification response into assessment and primary-source escalation

## Why This Family Exists

The outbound Acumen -> Augur bridge now exists.
That creates the next bounded need:

- a landed Augur response must be ingested without treating Augur as constitutional authority
- repo-side assessment must separate verified fact, inference, and next-source recommendations
- primary-source escalation must become a visible repo surface rather than an ad hoc follow-up

This family satisfies that need with one narrow chain:

`Augur packet -> Augur response -> repo-side assessment -> primary-source escalation queue`

## Placement Law

Augur remains a cited witness surface.
It is not intake authority, not triage authority, and not final doctrine.

Acumen remains authoritative for:

- the item identity
- the triage decision that opened the verification path
- dossier and packet provenance

The repo-side assessment is authoritative only for how the repo classifies the landed Augur response.
It does not convert that response into doctrine automatically.

## Surfaces

Response witness surface:

1. `communications/responses/RESPONSE-PERPLEXITY-acumen-*.md`

Assessment family:

1. `runtime/acumen/out/augur-return-assessments/*.json`
2. `communications/assessments/ACUMEN-AUGUR-RETURN-ASSESSMENT-*.md`

Primary-source queue surface:

1. `orchestration/state/ACUMEN-AUGUR-PRIMARY-SOURCE-QUEUE.json`
2. `orchestration/state/ACUMEN-AUGUR-PRIMARY-SOURCE-QUEUE.md`

Ingestion and validation helpers:

1. `operators/acumen/ingest_augur_returns.py`
2. `operators/validators/validate_acumen_augur_returns.py`
3. `orchestration/state/ACUMEN-AUGUR-RETURN-REPORT.json`
4. `orchestration/state/ACUMEN-AUGUR-RETURN-REPORT.md`

## Ingestion Law

The ingestion operator may read only the response path declared by the verification bridge family.

It must:

- preserve the Augur response as a witness artifact
- create a repo-side assessment artifact for each bridged item
- classify each item into pending, held, or queued-for-primary state

It must not:

- rewrite the Augur response into doctrine
- treat citation count alone as sufficient for queue promotion
- erase the distinction between missing response, malformed response, and assessed response

## Assessment Law

Every repo-side assessment must expose three explicit classes:

1. verified fact candidates
2. inference or tentative reading
3. next-source recommendations

Those classes may be empty when the response is missing or malformed, but the assessment must say so plainly.

The assessment may also preserve:

- disconfirming or complicating evidence
- confidence and gap notes
- queue rationale

The assessment must not collapse into final narrative doctrine.

## Queue Law

The primary-source queue is a routing surface.
It exists to nominate what should be read in original form next.

Queue admission means:

- the response landed
- the repo-side assessment extracted reusable next-source recommendations
- the item should move into a primary-source review pass

Queue admission does not mean:

- the topic is settled
- the Augur response is ratified as truth
- doctrine promotion is automatic

## Manual Boundary

The remaining external boundary is still real:

- Augur or the human relay must land the cited response markdown in the declared response path

Only after that witness artifact exists can the repo perform content-bearing assessment and queue escalation.
