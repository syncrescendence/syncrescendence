# RESPONSE-CODEX-CAMPAIGN-09-LANE-02-GEMINI-TRIAGE-ADAPTER-AND-GUARDRAILS

**status**: `complete`

## What landed

The Acumen triage surface now has a real Gemini adapter with strict packet and decision contracts instead of a prompt-only stub.

Implemented:

1. `operators/acumen/triage_contract.py`
   - canonical Acumen triage packet schema
   - deterministic packet IDs
   - strict decision schema and decision-coupling rules
   - packet rendering separated from invocation
2. `operators/acumen/gemini_triage_adapter.py`
   - official Gemini REST invocation surface
   - external API-key resolution via env var only
   - strict JSON schema request
   - retry handling for retryable HTTP/malformed-response cases
   - prompt/token budget guardrails
3. `operators/acumen/run_gemini_triage.py`
   - single-packet CLI adapter
   - emits strict JSON decision records
   - can append directly to a JSONL queue
4. `operators/acumen/build_triage_packet.py`
   - now writes deterministic packet JSON by default
   - can still emit a human-readable prompt preview
   - bridge handoff now materializes packet JSON plus prompt preview
5. `operators/acumen/run_triage.py`
   - batch runner now builds packet artifacts, calls the shared Gemini adapter, and writes guarded decision/training metadata
   - heuristic mode remains available, but Gemini failures no longer silently degrade after a live attempt
6. `operators/acumen/pipeline_flow.py`
   - passes through the new Gemini guardrail settings
7. docs and make surfaces
   - `Makefile`
   - `operators/acumen/README.md`
   - `runtime/acumen/README.md`

## Guardrails

Added:

1. API key stays external to the repo through `GEMINI_API_KEY` or an override env-var name
2. prompt-size ceiling before invocation
3. output-token ceiling in generation config
4. total-token ceiling after response validation
5. bounded retry count with backoff
6. strict response JSON schema plus post-parse contract validation
7. malformed-response retry path instead of accepting bad JSON

## Verification

Executed:

1. `python3 -m py_compile operators/acumen/triage_contract.py operators/acumen/gemini_triage_adapter.py operators/acumen/run_gemini_triage.py operators/acumen/build_triage_packet.py operators/acumen/run_triage.py operators/acumen/pipeline_flow.py`
2. `python3 operators/acumen/build_triage_packet.py --registry runtime/acumen/registry.json --channel-id UC_x5XG1OV2P6uZZ5FSM9Ttw --video runtime/acumen/sample-video.json --output /private/tmp/acumen-triage-test/triage-packet.json --prompt-output /private/tmp/acumen-triage-test/triage-prompt.md`
3. single-packet Gemini adapter smoke against a local mock Gemini server
   - first response intentionally malformed JSON
   - second response valid JSON
   - result: success with `attempts_used=2`
4. batch triage smoke in heuristic mode against a JSONL fixture
   - outputs created for queue, training metadata, packet artifacts, and status
5. pipeline smoke with `--poll-mode fixture --triage-mode heuristic`
   - result: poll, triage, and Dawn Brief stages all completed successfully
6. `git diff --check`

## Note

I did not execute a live Google Gemini call because the credential is intentionally repo-external and no live key was supplied. The adapter itself was exercised through a local mock that verified the retry and malformed-response path without weakening the external-secret rule.
