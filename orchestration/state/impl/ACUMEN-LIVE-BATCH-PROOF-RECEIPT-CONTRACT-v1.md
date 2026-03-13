# Acumen Live Batch Proof Receipt Contract v1

**Status**: staged  
**Class**: implementation law  
**Purpose**: define the smallest lawful receipt family for Acumen's first true credentialed live batch

## Why This Family Exists

Campaign 10 left Acumen truthfully live-batch ready.
That is not the same as live-batch proven.

The remaining gap is proof lineage:

- a blocked run should leave a durable blocked receipt instead of a chat claim
- a successful live poll with zero live Gemini calls should not be misclassified as full proof
- the first true credentialed run must survive later mutable status rewrites

This family closes that gap without widening authority.

## Surfaces

Append-only witness:

1. `orchestration/state/registry/acumen-live-batch-proof-ledger.jsonl`

Current status surface:

1. `orchestration/state/ACUMEN-LIVE-BATCH-PROOF-STATUS.json`

Operator surface:

1. `operators/acumen/run_live_batch_proof.py`
2. `make acumen-live-batch`

Validation and report surfaces:

1. `operators/validators/validate_acumen_live_batch_proof.py`
2. `orchestration/state/ACUMEN-LIVE-BATCH-PROOF-REPORT.json`
3. `orchestration/state/ACUMEN-LIVE-BATCH-PROOF-REPORT.md`

## Family Rule

Each invocation records exactly one append-only receipt event with one of four outcomes:

- `blocked`
- `failed`
- `completed_not_proven`
- `proven`

The lawful proven state is narrow:

- strict identity was required
- live polling actually ran
- live Gemini triage actually ran
- at least one live Gemini call was executed
- the pipeline completed successfully

If any of those conditions are not met, the receipt must not claim proof.

## Blocked Rule

Missing credentials are a blocked proof frontier, not a failed proof.

Identity mismatch is also blocking because the run is not lawful to continue under the wrong Google binding.

Blocked receipts must preserve only:

- env-var names
- presence or absence booleans
- bounded failure code and message

Blocked receipts must not store secrets.

## Durability Rule

`ACUMEN-PIPELINE-STATUS.json` remains mutable current state.

The live-batch proof ledger is the durable witness.
Each receipt therefore captures a bounded pipeline summary and a digest of the mutable pipeline status file when a pipeline attempt was made.

Later fixture runs may rewrite current status.
They do not erase prior proof receipts.

## Sovereignty Rule

Acumen remains sovereign over:

- intake
- triage
- proof classification
- repo-side witness state

Provider credentials remain external to repo state.
The receipt family may record credential presence, never credential values.
