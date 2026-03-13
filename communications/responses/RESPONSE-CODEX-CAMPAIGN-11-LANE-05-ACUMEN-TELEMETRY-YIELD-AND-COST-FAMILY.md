# RESPONSE-CODEX-CAMPAIGN-11-LANE-05-ACUMEN-TELEMETRY-YIELD-AND-COST-FAMILY

## Verdict

Acumen already has a partial telemetry family in repo truth:

- poll status snapshots
- triage status snapshots
- append-only triage and model-call ledgers
- verification-bridge status
- report-first validators

That is enough to inspect parts of poll yield, triage yield, promotion readiness, and lawful estimated cost metadata without inventing live facts.

It is not yet a coherent telemetry organ because the repo still lacks one derived report surface that composes those witnesses into a single inspectable view, and live latency / live-cost truth remains mostly absent.

Telemetry should remain derived from evidence and product artifacts.
It should not become a new authority plane.

## 1. Direct-Write Set

The smallest lawful direct-write set is:

1. `orchestration/state/impl/ACUMEN-TELEMETRY-FAMILY-CONTRACT-v1.md`
   - define scope, truth hierarchy, and labels for `observed`, `estimated`, and `unavailable`
   - state explicitly that telemetry is derivative of ledgers, status files, bridge state, and downstream product artifacts
   - forbid raw prompt, raw response, secret, and invented-live fields
2. `operators/acumen/build_telemetry_report.py`
   - derive one current-state report from:
   - `runtime/acumen/poll-status.json`
   - `runtime/acumen/triage-status.json`
   - `orchestration/state/ACUMEN-PIPELINE-STATUS.json`
   - `orchestration/state/registry/acumen-triage-decision-ledger.jsonl`
   - `orchestration/state/registry/acumen-training-corpus-ledger.jsonl`
   - `orchestration/state/ACUMEN-AUGUR-VERIFICATION-BRIDGE.json`
   - `orchestration/state/ACUMEN-TRIAGE-EVIDENCE-REPORT.json`
   - `orchestration/state/ACUMEN-AUGUR-VERIFICATION-BRIDGE-REPORT.json`
3. `operators/validators/validate_acumen_telemetry.py`
   - report-first validator that checks telemetry totals against the ledgers and bridge family
   - fail on contradictions, not on absent live fields
4. `orchestration/state/ACUMEN-TELEMETRY-REPORT.json`
5. `orchestration/state/ACUMEN-TELEMETRY-REPORT.md`

Not warranted yet:

- a new append-only `acumen-telemetry-ledger.jsonl`

Reason:

- append-only witness already exists in `acumen-triage-decision-ledger.jsonl` and `acumen-training-corpus-ledger.jsonl`
- promotion-readiness witness already exists in `ACUMEN-AUGUR-VERIFICATION-BRIDGE.json`
- adding a third historical ledger now would duplicate truth instead of improving inspectability

## 2. What Metrics Are Now Inspectable

The following are already inspectable from current repo surfaces.
Each item below is labeled as `observed`, `estimated`, or `unavailable`.

### Poll Surface

Source: `runtime/acumen/poll-status.json`

Observed in the latest fixture-safe snapshot at `2026-03-12T21:24:46Z`:

- `channels_total = 2`
- `new_uploads = 0`
- `failures = 0`
- per-channel status exists for both registered channels
- per-channel fields include `channel_id`, `channel_name`, `items_seen`, `new_items`, `source_mode`, and `status`

Inspectable now:

- registry coverage actually traversed in the last run
- per-channel candidate discovery counts
- partial-failure count
- source class of the run: `fixture` versus `live`

### Triage Surface

Sources:

- `runtime/acumen/triage-status.json`
- `orchestration/state/registry/acumen-triage-decision-ledger.jsonl`
- `orchestration/state/registry/acumen-training-corpus-ledger.jsonl`
- `orchestration/state/ACUMEN-TRIAGE-EVIDENCE-REPORT.json`

Observed in the latest fixture-safe triage snapshot at `2026-03-12T21:24:46Z`:

- `processed = 0`
- `queued = 0`
- `training_records = 0`
- `failures = 0`
- `skipped_existing = 0`
- `mode = heuristic`

Important distinction:

- the latest snapshot processed zero new items because the latest fixture run found zero new uploads
- cumulative witness still exists in the append-only ledgers from `2026-03-11T00:55:40Z`

Observed in cumulative ledger truth:

- `triage_event_count = 2`
- `training_event_count = 2`
- decision mix:
- `Promote = 1`
- `Compress = 1`
- promotion-eligible yield from observed triage decisions = `1 / 2 = 50%`

Inspectable now:

- decision distribution
- promotion-eligible rate
- per-item `decision`, `target_depth`, `target_polish`, `priority_band`, `channel_id`, `video_id`
- packet provenance via `packet_path` and `packet_sha256`
- model-call linkage via `model_call_event_id`
- evidence-family integrity:
- `status = PASS`
- `finding_count = 0`
- `triage_runtime_row_count = 2`
- `training_runtime_row_count = 2`

### Promotion And Verification-Ready Surface

Sources:

- `orchestration/state/ACUMEN-AUGUR-VERIFICATION-BRIDGE.json`
- `orchestration/state/ACUMEN-AUGUR-VERIFICATION-BRIDGE-REPORT.json`

Observed in bridge state at `2026-03-11T02:59:58Z`:

- `eligible_items_written = 1`
- `dossiers_written = 1`
- `augur_packets_written = 1`
- selected eligible item count = `1`

Observed in bridge validation at `2026-03-12T21:33:29Z`:

- `items_checked = 1`
- `ok = true`
- `findings = 0`

Inspectable now:

- triage-to-verification-ready yield
- observed bridge-ready yield from eligible items = `1 / 1 = 100%`
- dossier presence
- downstream packet presence
- packet / dossier path integrity
- whether verification handoff is merely eligible or actually materialized

Boundary:

- this is verification-ready yield, not downstream verification-complete yield

### Cost And Usage Surface

Sources:

- `runtime/acumen/triage-status.json`
- `orchestration/state/ACUMEN-PIPELINE-STATUS.json`
- `orchestration/state/registry/acumen-training-corpus-ledger.jsonl`

Observed now:

- all recorded training rows are local heuristic rows
- provider mix: `local = 2`
- model mix: `deterministic-heuristic = 2`
- each recorded training row has `cost.estimated_usd = 0.0`
- each recorded training row has `usage.attempts = 0`
- latest triage snapshot shows:
- `calls_used = 0`
- `estimated_cost_usd = 0.0`
- `estimated_cost_per_call_usd = 0.0`
- `max_estimated_cost_usd = 0.0`

Inspectable now:

- whether cost is `observed` or only `estimated`
- cost-guardrail configuration
- model/provider mix
- call-count usage at the batch snapshot level
- retry-attempt counts when model calls actually occur

Boundary:

- the current cost surface is lawful but mostly estimate-oriented
- no committed live Gemini run exists here, so no non-zero provider-backed cost evidence exists

### Failure Surface

Sources:

- `runtime/acumen/triage-status.json`
- `orchestration/state/ACUMEN-PIPELINE-STATUS.json`
- `operators/acumen/run_triage.py`
- `operators/acumen/pipeline_flow.py`

Inspectable now:

- top-level `ok`
- `failures`
- `failure_domain`
- `failure_code`
- `failure_message`
- summarized failure samples for triage batches
- bounded failure classes for the live batch:
- `credential`
- `identity`
- `external_service`

Observed now:

- no failure fields are populated in the current committed snapshots because the committed proof path passed

## 3. What Metrics Remain Unavailable Until Live Runs Occur

These remain unavailable because no committed live YouTube plus live Gemini batch is present.

### Unavailable Until Live Runs

- live poll discovery counts against real upstream channel state
- live poll partial-failure rates by real channel
- live Gemini call counts greater than zero
- live Gemini token-usage fields from provider `usageMetadata`
- non-zero estimated cost accumulation for Gemini batches
- real provider failure mix: HTTP, transport, malformed output, contract failure
- real retry burden above zero
- live promotion yield under external-model triage rather than heuristic local triage

### Still Unavailable Even If A Live Run Occurred Today

These are not just missing live receipts; they are not yet first-class telemetry fields.

- poll latency per channel
- model round-trip latency per call
- end-to-end cycle time from poll to triage to bridge
- verification completion yield from `packet sent` to `Augur response returned`
- repo-side assessment yield from `Augur response returned` to `accepted / rejected / escalated`
- product yield from `eligible signal` to `brief / assessment / primary-source queue / promotion artifact`

Reason:

- current code captures status, usage, estimated cost, and failure taxonomy
- it does not yet timestamp latency windows or ingest downstream verification returns into a measurable queue

## Closing Judgment

Acumen is no longer a blind runtime artifact set.
It already exposes real inspectable surfaces for:

- poll coverage
- triage decision yield
- promotion-ready yield
- evidence-family integrity
- lawful estimated cost and usage metadata

The next correct move is not a new telemetry ledger.
It is one derived telemetry report plus a validator, with strict `observed / estimated / unavailable` labeling and with telemetry kept subordinate to evidence ledgers and product-truth artifacts.
