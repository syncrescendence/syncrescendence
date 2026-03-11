# Acumen Runtime Lane

Runtime lane for Acumen Intelligence Pipeline generated artifacts and operator outputs.

## Current Scope

This lane stores files produced by the repo-native Acumen flow that actually exists today.

1. registry generation and validation
2. YouTube poll cursor state and poll-candidate output
3. identity probe status
4. triage packet artifacts and prompt previews
5. deterministic transcript artifacts
6. Dawn Brief compilation from an existing JSONL queue
7. sequential status snapshots

This lane now proves repo-native YouTube polling against the Acumen registry.
It now includes a repo-native Gemini triage path with explicit guardrails, while keeping all credentials external and storing only sanitized decision/training metadata.

## Environment Variables

The poll worker requires one repo-external credential.

1. `ACUMEN_YOUTUBE_API_KEY` is required by `operators/acumen/poll_youtube_registry.py` unless `--api-key-env` points at a different env var.
2. Strict identity checks still rely on local `gcloud` state and the macOS keychain entry `syncrescendence/gcloud-account`, not on repo env vars.
3. `make acumen-sample-run` remains file-based and does not require the YouTube API key.
4. `GEMINI_API_KEY` is consumed only by the Gemini triage adapter or batch runner when those surfaces are used.
5. Model credentials must stay external and may not be copied into Acumen evidence surfaces.

## Expected Local Artifacts

1. `registry.json`
2. `poll_cursor.json`
3. `poll-candidates.jsonl`
4. `intake/youtube/*.json` for Acumen-owned YouTube bridge handoffs
5. `intake/triage-packets/*.json` when a handoff includes enough metadata to build a triage packet
6. `intake/triage-prompts/*.md` for optional prompt previews
7. `out/triage-packet.sample.json` and `out/triage-prompt.sample.md` or equivalent packet outputs
8. `out/triage-decision*.json` for single-packet Gemini runs
9. `out/deterministic-*.md` and optional `out/*.debug.json`
10. `out/DAWN-BRIEF-*.md`
11. sample or real decision queues such as `triage-decisions.sample.jsonl`
12. repo-derived runtime evidence surfaces:
   - `triage-decisions.jsonl`
   - `training-corpus.jsonl`
13. status files under `/Users/system/syncrescendence/orchestration/state/`:
   - `ACUMEN-IDENTITY-STATUS.json`
   - `ACUMEN-YOUTUBE-POLL-STATUS.json`
   - `ACUMEN-PIPELINE-STATUS.json`
14. sample fixtures:
   - `sample-video.json`
   - `sample-transcript.txt`
   - `triage-decisions.sample.jsonl`

## Repo-Sovereign Evidence

Append-only evidence for the runtime files lives at:

1. `orchestration/state/registry/acumen-triage-decision-ledger.jsonl`
2. `orchestration/state/registry/acumen-training-corpus-ledger.jsonl`

Those ledgers are the witness surfaces.
`runtime/acumen/triage-decisions.jsonl` and `runtime/acumen/training-corpus.jsonl` are derivative current-state views only.

## Repeatable Entry Point

From repo root:

```bash
make acumen-sample-run
```

For real registry polling:

```bash
ACUMEN_YOUTUBE_API_KEY=... make acumen-poll-youtube STRICT=1
```

Useful overrides:

1. `STRICT=1` to fail on canonical-identity mismatch during preflight and pipeline run
2. `POLISH=charitable` or `POLISH=editorial` to mark the deterministic artifact as needing an intelligent follow-up pass
3. `STATUS_JSON=/abs/path/status.json` to redirect pipeline status output

## Failure Modes

1. `registry missing` or `registry=invalid`: seed or registry contract issue
2. `missing_api_key`: the poll worker's configured API key env var is unset
3. `partial`: one or more registry channels failed poll while the rest completed and advanced cursor state
4. `channel not found in registry`: `CHANNEL_ID` does not exist in the registry passed to triage packet rendering
5. `video metadata missing required keys`: video JSON omitted one of `title`, `duration`, `description`, `initial_transcript`
6. identity probe mismatch in strict mode: active `gcloud` account or stored keychain account differs from canonical Acumen identity
7. queue or binding file missing: pipeline wrapper cannot compile Dawn Brief or perform identity preflight
8. deterministic artifact with `Intelligent Track Required`: requested polish exceeds current deterministic operator capability

This lane is operational output, not constitutional source.
