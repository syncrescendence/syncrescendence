# Acumen Operators

Operator lane for the Acumen Intelligence Pipeline.

This lane provides:

1. feed registry contract and validation
2. identity drift probe against the canonical Google binding
3. cadence-aware YouTube polling over the Acumen registry
4. deterministic transcript processing primitives
5. triage prompt rendering from registry plus video metadata
6. Acumen-owned YouTube bridge handoff materialization
7. Dawn Brief compilation
8. sequential runtime wrapper that probes identity and compiles a Dawn Brief
9. repo-native evidence logging, rematerialization, and validation
10. post-triage dossier and Augur verification packet generation for promoted or flagged items
11. promoted-item dossier and Augur verification bridge generation
12. live-batch proof receipting, proof-status projection, and validator reporting
13. Augur return ingestion, repo-side assessment, and primary-source queue generation
14. derivative Verified Signal Brief rendering from repo-side assessments
15. derivative primary-source queue readout rendering from queue state plus linked assessments

## Runtime Contract

Current repo-native Acumen execution is local and file-based.

1. `poll_youtube_registry.py` consumes a YouTube Data API key only through an external env var (`ACUMEN_YOUTUBE_API_KEY` by default, overrideable with `--api-key-env`).
2. `build_triage_packet.py` writes a deterministic packet JSON artifact and can optionally emit a prompt preview. It does not call Gemini itself.
3. `run_gemini_triage.py` is the single-packet Gemini adapter. `run_triage.py` is the batch runner that consumes poll output, builds packets, invokes Gemini when enabled, and appends runtime queue/training artifacts.
4. `identity_binding_probe.py` shells out to `gcloud` and macOS `security` when present. Strict mode fails only on detected canonical-identity mismatches, not on missing tools.
5. `record_evidence.py` accepts only sanitized model-call and decision metadata. Raw prompt bodies, raw response bodies, and secret-bearing fields are forbidden.
6. `make acumen-live-batch` is the narrow operator entrypoint for a first true live batch. It now writes an append-only proof receipt and a derived proof-status/report surface for each attempt without storing secrets in repo.

## Truth Boundary

1. code presence:
   - live YouTube polling, Gemini triage, evidence ledgers, rematerialization, and the sequential wrapper are all landed in repo
2. fixture-safe proof:
   - the repeatable proof path is `make acumen-sample-run`, which uses fixture polling plus heuristic triage and writes status artifacts under `runtime/acumen/` and `orchestration/state/`
   - the current evidence family validates through `python3 operators/validators/validate_acumen_evidence.py`
3. live external proof:
   - the repo now has a lawful witness family for blocked, failed, incomplete, and proven live-batch attempts
   - no committed Acumen receipt here yet proves a live YouTube poll plus at least one live Gemini triage call
4. current remaining boundary:
   - the normal batch runner is now evidence-native and the repeatable sample path passes
   - the remaining repo-external gap is first `live_batch_proven` receipt with credentials present
   - the Augur return path is now wired repo-side; the remaining external boundary is a cited Augur response landing in the declared response path

## Commands

1. initialize registry:
   - `python3 operators/acumen/init_registry.py --seed operators/acumen/channel_seed.example.json --output runtime/acumen/registry.json`
   - output: `runtime/acumen/registry.json`
2. validate registry:
   - `python3 operators/acumen/validate_registry.py --registry runtime/acumen/registry.json --strict`
   - failure modes: missing registry file, invalid channel contract, strict Tier 1 density warning
3. probe canonical identity (`syncrescendence@gmail.com`):
   - `python3 operators/acumen/identity_binding_probe.py --binding orchestration/state/ACUMEN-IDENTITY-BINDING-CC87.json --output orchestration/state/ACUMEN-IDENTITY-STATUS.json --strict`
   - output: `orchestration/state/ACUMEN-IDENTITY-STATUS.json`
   - failure mode: strict mismatch between canonical identity and detected active `gcloud` or stored keychain account
4. poll the registry against YouTube:
   - `ACUMEN_YOUTUBE_API_KEY=... python3 operators/acumen/poll_youtube_registry.py --registry runtime/acumen/registry.json --cursor runtime/acumen/poll_cursor.json --output-jsonl runtime/acumen/poll-candidates.jsonl --status-json orchestration/state/ACUMEN-YOUTUBE-POLL-STATUS.json --strict-identity`
   - outputs:
     - `runtime/acumen/poll_cursor.json`
     - `runtime/acumen/poll-candidates.jsonl`
     - `orchestration/state/ACUMEN-YOUTUBE-POLL-STATUS.json`
   - failure modes: missing API key env var, invalid registry, strict identity mismatch, explicit per-channel poll failure with `partial` status when other channels continue
5. deterministic processing:
   - `python3 operators/acumen/deterministic_track.py --input-text runtime/acumen/sample-transcript.txt --genre Commentary --target-depth Precis --target-polish clean_verbatim --output runtime/acumen/out/deterministic-sample.md --debug-json runtime/acumen/out/deterministic-sample.debug.json`
   - outputs: deterministic markdown artifact, optional debug JSON
   - note: `charitable` and `editorial` emit a deterministic base plus an explicit `Intelligent Track Required` marker rather than performing semantic rewriting
6. build triage packet:
   - `python3 operators/acumen/build_triage_packet.py --registry runtime/acumen/registry.json --channel-id UC_x5XG1OV2P6uZZ5FSM9Ttw --video runtime/acumen/sample-video.json --output runtime/acumen/out/triage-packet.sample.json --prompt-output runtime/acumen/out/triage-prompt.sample.md`
   - output: deterministic packet JSON plus optional human-readable prompt preview
   - failure modes: unknown `channel_id`, missing video metadata keys
7. run Gemini for one packet (`GEMINI_API_KEY` stays external to the repo):
   - `python3 operators/acumen/run_gemini_triage.py --packet runtime/acumen/out/triage-packet.sample.json --output runtime/acumen/out/triage-decision.sample.json --append-jsonl runtime/acumen/triage-decisions.jsonl`
   - guardrails: strict response schema, prompt/token budgets, retry on malformed/retryable responses
   - note: `--append-jsonl` writes the runtime current-state queue directly; it is not the append-only ledger path
8. hand off YouTube bridge capture into Acumen intake:
   - `python3 operators/exocortex/youtube_feed_bridge.py --resource-kind video --resource-id sample-video --summary "Architecture update checkpoint" --title "Gemini 3.1 Architecture Update" --channel-id UC_x5XG1OV2P6uZZ5FSM9Ttw --payload '{"duration":"01:02:11","description":"DeepMind team discusses Gemini architecture updates.","initial_transcript":"today demis hassabis outlines gemini architecture changes"}' --acumen-registry runtime/acumen/registry.json`
   - outputs: `runtime/acumen/intake/youtube/*.json`, `runtime/acumen/intake/triage-packets/*.json`, and prompt previews in `runtime/acumen/intake/triage-prompts/*.md`
   - sovereignty rule: channels absent from the Acumen registry are skipped rather than admitted through the bridge
9. run batch triage from poll output:
   - `python3 operators/acumen/run_triage.py --registry runtime/acumen/registry.json --poll-jsonl runtime/acumen/poll-candidates.jsonl --queue-jsonl runtime/acumen/triage-decisions.jsonl --training-jsonl runtime/acumen/training-corpus.jsonl --status-json runtime/acumen/triage-status.json --artifact-dir runtime/acumen/out/triage --mode gemini`
   - outputs: append-only decision and model-call evidence, rematerialized runtime queue and training views, packet JSON artifacts, prompt previews, and triage status
   - note: this is now the evidence-native default batch route for Acumen
10. compile Dawn Brief:
   - `python3 operators/acumen/build_dawn_brief.py --input-jsonl runtime/acumen/triage-decisions.sample.jsonl --output runtime/acumen/out/DAWN-BRIEF-sample.md`
   - output: Dawn Brief markdown synthesized from an existing decision queue
11. run sequential runtime wrapper:
   - `python3 operators/acumen/pipeline_flow.py --registry runtime/acumen/registry.json --queue runtime/acumen/triage-decisions.jsonl --out runtime/acumen/out --status-json orchestration/state/ACUMEN-PIPELINE-STATUS.json --identity-binding orchestration/state/ACUMEN-IDENTITY-BINDING-CC87.json --poll-mode fixture --fixture-feed runtime/acumen/poll-fixture.sample.json --triage-mode heuristic --strict-identity`
   - outputs:
     - `runtime/acumen/out/DAWN-BRIEF-YYYYMMDD.md`
     - `orchestration/state/ACUMEN-PIPELINE-STATUS.json`
     - `orchestration/state/ACUMEN-IDENTITY-STATUS.json`
   - failure modes: missing queue or binding file, Dawn Brief compile failure, strict identity mismatch, live-mode credential failures when `poll-mode=live` or `triage-mode=gemini`
12. repeatable sample smoke via Make:
   - `make acumen-sample-run`
   - current proof class: fixture poll plus heuristic triage, not live external execution
   - optional knobs: `STRICT=1`, `POLISH=charitable`, `STATUS_JSON=/abs/path/status.json`
13. one-command live batch via Make:
   - `ACUMEN_YOUTUBE_API_KEY=... GEMINI_API_KEY=... make acumen-live-batch`
   - fixed path:
     - appends a receipt event into `orchestration/state/registry/acumen-live-batch-proof-ledger.jsonl`
     - derives current proof state at `orchestration/state/ACUMEN-LIVE-BATCH-PROOF-STATUS.json`
     - validates and reports the family at `orchestration/state/ACUMEN-LIVE-BATCH-PROOF-REPORT.{json,md}`
     - when credentials are present, validates `runtime/acumen/registry.json`
     - when credentials are present, enforces strict identity with `orchestration/state/ACUMEN-IDENTITY-BINDING-CC87.json`
     - when credentials are present, writes live poll status to `orchestration/state/ACUMEN-YOUTUBE-POLL-STATUS.json`
     - when credentials are present, writes triage status to `runtime/acumen/triage-status.json`
     - when credentials are present, writes top-level pipeline status to `orchestration/state/ACUMEN-PIPELINE-STATUS.json`
   - bounded live failure classes:
     - `credential`
     - `identity`
     - `external_service`
   - bounded proof outcomes:
     - `blocked`
     - `failed`
     - `completed_not_proven`
     - `proven`
14. record a sanitized triage decision event:
   - `python3 operators/acumen/record_evidence.py decision --input-json /abs/path/decision.json --actor acumen.triage`
   - output: append-only event in `orchestration/state/registry/acumen-triage-decision-ledger.jsonl` plus rebuilt `runtime/acumen/triage-decisions.jsonl`
15. record a sanitized model-call event:
   - `python3 operators/acumen/record_evidence.py model-call --input-json /abs/path/model-call.json --actor acumen.triage`
   - output: append-only event in `orchestration/state/registry/acumen-training-corpus-ledger.jsonl` plus rebuilt `runtime/acumen/training-corpus.jsonl`
16. rebuild runtime evidence from ledgers:
   - `python3 operators/acumen/rematerialize_evidence.py`
17. validate the evidence family:
   - `python3 operators/validators/validate_acumen_evidence.py`
18. validate the live-batch proof family:
   - `python3 operators/validators/validate_acumen_live_batch_proof.py`
   - outputs:
     - `orchestration/state/ACUMEN-LIVE-BATCH-PROOF-REPORT.json`
     - `orchestration/state/ACUMEN-LIVE-BATCH-PROOF-REPORT.md`
19. build post-triage dossiers and Augur verification packets for eligible items:
   - `python3 operators/acumen/build_verification_bridge.py --video-id deepmind-gemini-31-architecture`
   - outputs:
     - `runtime/acumen/out/verification-dossiers/deepmind-gemini-31-architecture.json`
     - `communications/prompts/PACKET-PERPLEXITY-acumen-deepmind-gemini-31-architecture.md`
     - expected return target in `communications/responses/RESPONSE-PERPLEXITY-acumen-deepmind-gemini-31-architecture.md`
     - bridge state at `orchestration/state/ACUMEN-AUGUR-VERIFICATION-BRIDGE.json`
     - runtime portfolio views at `runtime/acumen/out/verification-portfolio.json` and `runtime/acumen/out/verification-portfolio.md`
   - guardrail: only `Promote` or `Flag-for-Primary` decision records are eligible
20. emit a repeatable verification batch and queue surface:
   - `python3 operators/acumen/build_verification_bridge.py --max-items 10`
   - optional controls:
     - `--include-ingested` to regenerate already closed items
     - `--decision Flag-for-Primary` or `--video-id <id>` to narrow the batch
   - outputs:
     - `runtime/acumen/out/verification-dossiers/*.json` for selected batch items
     - `communications/prompts/PACKET-PERPLEXITY-acumen-*.md` for selected batch items
     - `orchestration/state/ACUMEN-AUGUR-VERIFICATION-BRIDGE.json` with queue status for all eligible items
     - `runtime/acumen/out/verification-portfolio.json`
     - `runtime/acumen/out/verification-portfolio.md`
   - routing rule: Acumen stays sovereign over intake and triage; Augur receives only sanitized downstream verification packets
21. validate the dossier and bridge family:
   - `python3 operators/validators/validate_acumen_verification_bridge.py`
   - outputs:
     - `orchestration/state/ACUMEN-AUGUR-VERIFICATION-BRIDGE-REPORT.json`
     - `orchestration/state/ACUMEN-AUGUR-VERIFICATION-BRIDGE-REPORT.md`
22. ingest landed Augur responses into repo-side assessments and the primary-source queue:
   - `python3 operators/acumen/ingest_augur_returns.py`
   - optional controls:
     - `--video-id <id>` or `--triage-event-id <id>` to narrow the run
   - outputs:
     - `runtime/acumen/out/augur-return-assessments/*.json`
     - `communications/assessments/ACUMEN-AUGUR-RETURN-ASSESSMENT-*.md`
     - `orchestration/state/ACUMEN-AUGUR-PRIMARY-SOURCE-QUEUE.json`
     - `orchestration/state/ACUMEN-AUGUR-PRIMARY-SOURCE-QUEUE.md`
   - routing rule: the repo assessment classifies Augur as witness input only and keeps verified fact, inference, and next-source recommendations separate
23. validate the Augur return family:
   - `python3 operators/validators/validate_acumen_augur_returns.py`
   - outputs:
     - `orchestration/state/ACUMEN-AUGUR-RETURN-REPORT.json`
     - `orchestration/state/ACUMEN-AUGUR-RETURN-REPORT.md`
24. build the Verified Signal Brief:
   - `python3 operators/acumen/build_verified_signal_brief.py --assessment-json-dir runtime/acumen/out/augur-return-assessments --queue-json orchestration/state/ACUMEN-AUGUR-PRIMARY-SOURCE-QUEUE.json --output runtime/acumen/out/VERIFIED-SIGNAL-BRIEF-YYYYMMDD.md`
   - output:
     - `runtime/acumen/out/VERIFIED-SIGNAL-BRIEF-YYYYMMDD.md`
   - routing rule: the brief is derivative only and may summarize only repo-side assessment plus queue state
25. build the primary-source queue readout:
   - `python3 operators/acumen/build_primary_source_queue_readout.py --queue-json orchestration/state/ACUMEN-AUGUR-PRIMARY-SOURCE-QUEUE.json --assessment-json-dir runtime/acumen/out/augur-return-assessments --output runtime/acumen/out/PRIMARY-SOURCE-QUEUE-READOUT-YYYYMMDD.md`
   - output:
     - `runtime/acumen/out/PRIMARY-SOURCE-QUEUE-READOUT-YYYYMMDD.md`
   - routing rule: the readout renders queue state for operators without changing queue admission
26. build the first post-triage product family in one step:
   - `make acumen-build-intelligence-product-family DATESTAMP=YYYYMMDD`
   - outputs:
     - `runtime/acumen/out/VERIFIED-SIGNAL-BRIEF-YYYYMMDD.md`
     - `runtime/acumen/out/PRIMARY-SOURCE-QUEUE-READOUT-YYYYMMDD.md`

## Operator Notes

1. `make acumen-sample-run` remains the fixture-safe proof path and is unchanged by the live-batch target.
2. `make acumen-live-batch` consumes only env-var credential names. It never echoes, persists, or ledgers raw secrets.
3. `orchestration/state/registry/acumen-live-batch-proof-ledger.jsonl` is the durable witness for blocked, failed, incomplete, and proven live attempts.
4. `orchestration/state/ACUMEN-LIVE-BATCH-PROOF-STATUS.json` is a derived current summary and must stay subordinate to the append-only proof ledger.
5. `orchestration/state/ACUMEN-PIPELINE-STATUS.json` still surfaces `failure_domain`, `failure_code`, `failure_message`, and nested poll / triage status snapshots so a live attempt is diagnosable without widening the secret surface.
6. `orchestration/state/ACUMEN-AUGUR-VERIFICATION-BRIDGE.json` is now the canonical queue state, while `runtime/acumen/out/verification-portfolio.*` are the operator-facing throughput views.
7. `communications/assessments/ACUMEN-AUGUR-RETURN-ASSESSMENT-*.md` are repo-native classification artifacts, not doctrine surfaces.
8. `orchestration/state/ACUMEN-AUGUR-PRIMARY-SOURCE-QUEUE.*` is a routing surface only; queue admission does not ratify the Augur response.
9. `runtime/acumen/out/VERIFIED-SIGNAL-BRIEF-*.md` and `runtime/acumen/out/PRIMARY-SOURCE-QUEUE-READOUT-*.md` are derivative products over assessment and queue state, not new authority surfaces.
