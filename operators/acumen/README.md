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

## Runtime Contract

Current repo-native Acumen execution is local and file-based.

1. `poll_youtube_registry.py` consumes a YouTube Data API key only through an external env var (`ACUMEN_YOUTUBE_API_KEY` by default, overrideable with `--api-key-env`).
2. `build_triage_packet.py` writes a deterministic packet JSON artifact and can optionally emit a prompt preview. It does not call Gemini itself.
3. `run_gemini_triage.py` is the single-packet Gemini adapter. `run_triage.py` is the batch runner that consumes poll output, builds packets, invokes Gemini when enabled, and appends queue/training artifacts.
4. `identity_binding_probe.py` shells out to `gcloud` and macOS `security` when present. Strict mode fails only on detected canonical-identity mismatches, not on missing tools.
5. `record_evidence.py` accepts only sanitized model-call and decision metadata. Raw prompt bodies, raw response bodies, and secret-bearing fields are forbidden.

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
8. hand off YouTube bridge capture into Acumen intake:
   - `python3 operators/exocortex/youtube_feed_bridge.py --resource-kind video --resource-id sample-video --summary "Architecture update checkpoint" --title "Gemini 3.1 Architecture Update" --channel-id UC_x5XG1OV2P6uZZ5FSM9Ttw --payload '{"duration":"01:02:11","description":"DeepMind team discusses Gemini architecture updates.","initial_transcript":"today demis hassabis outlines gemini architecture changes"}' --acumen-registry runtime/acumen/registry.json`
   - outputs: `runtime/acumen/intake/youtube/*.json`, `runtime/acumen/intake/triage-packets/*.json`, and prompt previews in `runtime/acumen/intake/triage-prompts/*.md`
   - sovereignty rule: channels absent from the Acumen registry are skipped rather than admitted through the bridge
9. run batch triage from poll output:
   - `python3 operators/acumen/run_triage.py --registry runtime/acumen/registry.json --poll-jsonl runtime/acumen/poll-candidates.jsonl --queue-jsonl runtime/acumen/triage-decisions.jsonl --training-jsonl runtime/acumen/training-corpus.jsonl --status-json runtime/acumen/triage-status.json --artifact-dir runtime/acumen/out/triage --mode gemini`
   - outputs: queue records, training-corpus metadata, packet JSON artifacts, prompt previews, and triage status
10. compile Dawn Brief:
   - `python3 operators/acumen/build_dawn_brief.py --input-jsonl runtime/acumen/triage-decisions.sample.jsonl --output runtime/acumen/out/DAWN-BRIEF-sample.md`
   - output: Dawn Brief markdown synthesized from an existing decision queue
11. run sequential runtime wrapper:
   - `python3 operators/acumen/pipeline_flow.py --registry runtime/acumen/registry.json --queue runtime/acumen/triage-decisions.sample.jsonl --out runtime/acumen/out --status-json orchestration/state/ACUMEN-PIPELINE-STATUS.json --identity-binding orchestration/state/ACUMEN-IDENTITY-BINDING-CC87.json --strict-identity`
   - outputs:
     - `runtime/acumen/out/DAWN-BRIEF-YYYYMMDD.md`
     - `orchestration/state/ACUMEN-PIPELINE-STATUS.json`
     - `orchestration/state/ACUMEN-IDENTITY-STATUS.json`
   - failure modes: missing queue or binding file, Dawn Brief compile failure, strict identity mismatch
12. repeatable sample smoke via Make:
   - `make acumen-sample-run`
   - optional knobs: `STRICT=1`, `POLISH=charitable`, `STATUS_JSON=/abs/path/status.json`
13. record a sanitized triage decision event:
   - `python3 operators/acumen/record_evidence.py decision --input-json /abs/path/decision.json --actor acumen.triage`
   - output: append-only event in `orchestration/state/registry/acumen-triage-decision-ledger.jsonl` plus rebuilt `runtime/acumen/triage-decisions.jsonl`
14. record a sanitized model-call event:
   - `python3 operators/acumen/record_evidence.py model-call --input-json /abs/path/model-call.json --actor acumen.triage`
   - output: append-only event in `orchestration/state/registry/acumen-training-corpus-ledger.jsonl` plus rebuilt `runtime/acumen/training-corpus.jsonl`
15. rebuild runtime evidence from ledgers:
   - `python3 operators/acumen/rematerialize_evidence.py`
16. validate the evidence family:
   - `python3 operators/validators/validate_acumen_evidence.py`
