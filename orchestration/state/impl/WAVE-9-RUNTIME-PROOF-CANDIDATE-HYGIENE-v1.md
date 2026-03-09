# Wave 9 Runtime Proof Candidate Hygiene v1

**Date**: `2026-03-09`  
**Status**: `complete`  
**Packet ID**: `PKT-20260309-codex-swarm-wave-9-lane-02-runtime-proof-candidate-hygiene`  
**Subject**: `current repo-valid synthetic runtime-proof candidate for the cowork outgoing flow`

## 1. Decision

One clean synthetic runtime-proof candidate is now defined against current repo-valid surfaces.

It uses a dedicated Perplexity packet and response target so the proof surface is isolated from swarm-lane artifacts:

- packet source: [PACKET-PERPLEXITY-wave-9-runtime-proof-candidate.md](/Users/system/syncrescendence/communications/prompts/PACKET-PERPLEXITY-wave-9-runtime-proof-candidate.md)
- expected final response: [RESPONSE-PERPLEXITY-wave-9-runtime-proof-candidate.md](/Users/system/syncrescendence/communications/responses/RESPONSE-PERPLEXITY-wave-9-runtime-proof-candidate.md)

Tracked candidate fixtures:

- job fixture: [perplexity-20260309-000000-wave-9-runtime-proof-candidate.job.json](/Users/system/syncrescendence/orchestration/state/runtime-proof-candidate/perplexity-20260309-000000-wave-9-runtime-proof-candidate.job.json)
- status fixture: [perplexity-20260309-000000-wave-9-runtime-proof-candidate.status.json](/Users/system/syncrescendence/orchestration/state/runtime-proof-candidate/perplexity-20260309-000000-wave-9-runtime-proof-candidate.status.json)

No runtime success is claimed here.
This lane only proves that the candidate shape and evidence targets are now clean.

## 2. Why This Candidate Is Clean

The Wave 8 smoke candidates were untrustworthy because they still pointed at dead `00-ORCHESTRATION/...` paths and a missing packet target.

This candidate removes those faults:

- `packet` points at a live Perplexity-facing repo file under `communications/prompts/`
- `packet_staging_path`, `response_staging_path`, and `status_path` use current `orchestration/relay/cowork-v1/...` paths
- `response_artifact` points at a fresh synthetic proof target under `communications/responses/`
- the finalizer path already proven live in storage cutover remains [finalize_cowork_relay_job.py](/Users/system/syncrescendence/operators/cli-web-gap/finalize_cowork_relay_job.py)

The more obvious alternative was rejected after verification:

- [RESPONSE-CODEX-SWARM-WAVE-9-LANE-03-CONDITIONAL-RUNTIME-PROOF-AND-RETIREMENT.md](/Users/system/syncrescendence/communications/responses/RESPONSE-CODEX-SWARM-WAVE-9-LANE-03-CONDITIONAL-RUNTIME-PROOF-AND-RETIREMENT.md) already exists as an untracked artifact, so it is not a clean proof target
- the Lane `03` dispatch packet is a Codex swarm instruction packet, not a Perplexity-facing verification packet

## 3. Target Verification

Verified now:

- source packet exists: [PACKET-PERPLEXITY-wave-9-runtime-proof-candidate.md](/Users/system/syncrescendence/communications/prompts/PACKET-PERPLEXITY-wave-9-runtime-proof-candidate.md)
- response parent exists: [communications/responses](/Users/system/syncrescendence/communications/responses)
- cowork inbox exists for the job file: [jobs/inbox](/Users/system/syncrescendence/orchestration/relay/cowork-v1/jobs/inbox)
- outgoing artifact folder exists for staged response and status files: [artifacts/outgoing](/Users/system/syncrescendence/orchestration/relay/cowork-v1/artifacts/outgoing)

Verified safe to stage under current shell law:

- `orchestration/relay/cowork-v1/packets/...` is the live packet-copy location documented in the relay schema and folder instructions
- `orchestration/relay/cowork-v1/jobs/inbox/...` is one of the locations the finalizer can resolve via `load_job()`
- `orchestration/relay/cowork-v1/artifacts/outgoing/...status.json` is accepted by the live Hazel caller and by `--status-file`
- [RESPONSE-PERPLEXITY-wave-9-runtime-proof-candidate.md](/Users/system/syncrescendence/communications/responses/RESPONSE-PERPLEXITY-wave-9-runtime-proof-candidate.md) does not exist yet, so a future landing remains unambiguous
- [SANDBOX-EVENT-LEDGER.jsonl](/Users/system/syncrescendence/orchestration/state/SANDBOX-EVENT-LEDGER.jsonl) does not exist yet, but `operators/sandbox_event_bridge.py` creates `orchestration/state/` if needed and appends the ledger there on first success

## 4. Exact Candidate Shape

Expected runtime staging surfaces for a real attempt:

1. copy the live packet into `orchestration/relay/cowork-v1/packets/perplexity-20260309-000000-wave-9-runtime-proof-candidate-PACKET-PERPLEXITY-wave-9-runtime-proof-candidate.md`
2. place the job JSON into `orchestration/relay/cowork-v1/jobs/inbox/perplexity-20260309-000000-wave-9-runtime-proof-candidate.json`
3. after web completion, write the response markdown into `orchestration/relay/cowork-v1/artifacts/outgoing/RESPONSE-PERPLEXITY-wave-9-runtime-proof-candidate.md`
4. write the status JSON into `orchestration/relay/cowork-v1/artifacts/outgoing/perplexity-20260309-000000-wave-9-runtime-proof-candidate.status.json`

Expected success evidence surfaces after finalization:

- completed job: `orchestration/relay/cowork-v1/jobs/completed/perplexity-20260309-000000-wave-9-runtime-proof-candidate.json`
- final response artifact: [RESPONSE-PERPLEXITY-wave-9-runtime-proof-candidate.md](/Users/system/syncrescendence/communications/responses/RESPONSE-PERPLEXITY-wave-9-runtime-proof-candidate.md)
- rewritten final status file at `orchestration/relay/cowork-v1/artifacts/outgoing/perplexity-20260309-000000-wave-9-runtime-proof-candidate.status.json` containing at least:
  - `job_id`
  - `surface`
  - `result`
  - `note`
  - `response_artifact`
  - optional `citation_count`
- ledger append in [SANDBOX-EVENT-LEDGER.jsonl](/Users/system/syncrescendence/orchestration/state/SANDBOX-EVENT-LEDGER.jsonl) with:
  - `type = "perplexity_response_landed"`
  - `artifact_class = "repo_markdown_change"`
  - `repo_paths` including the proof packet and proof response artifact
  - payload keys `web_surface`, `dispatch_packet`, and `response_artifact`

## 5. Readiness Judgment

Judgment:

- proof candidate clean: `yes`
- repo-valid paths only: `yes`
- expected response surface defined: `yes`
- expected ledger surface defined: `yes`
- Hazel runtime success claimed: `no`

Tranche outcome: `complete`
