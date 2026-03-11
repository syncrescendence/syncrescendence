# Acumen Intelligence Pipeline Wave0 Runbook — CC87

**Date**: 2026-03-04  
**Status**: active  
**Class**: execution runbook

## Goal

Run the repeatable repo-native Acumen flow that currently exists, with explicit boundaries around what is still external or not yet implemented.

## Preconditions

1. repo root available at `/Users/system/syncrescendence`
2. Python 3 available
3. for strict identity enforcement, local `gcloud` and macOS `security` tooling available
3. PRD feedstock intake present:
   - [20260305-prd-acumen-intelligence-pipeline-v2.md](/Users/system/syncrescendence/knowledge/feedstock/inbox/20260305-prd-acumen-intelligence-pipeline-v2.md)

## Execution Boundary

This runbook is intentionally limited to what the repo can execute today.

1. supported:
   - registry generation and validation
   - canonical identity probe
   - triage prompt rendering from existing video metadata JSON
   - deterministic transcript processing
   - Dawn Brief compilation from an existing JSONL queue
   - sequential pipeline status capture
2. not supported in-repo:
   - YouTube polling or cursor advancement
   - Gemini or other model invocation
   - automatic append to a triage decision ledger or training corpus

## Required Environment Variables

None for the current repo-native flow.

1. `make acumen-sample-run` does not require `GEMINI_API_KEY`, `YOUTUBE_API_KEY`, or other Acumen-specific env vars because those integrations are not implemented here.
2. Strict identity checks use local account state instead of env vars.

## Step 1: Preflight

```bash
make acumen-preflight
```

Expected:

1. `runtime/acumen/registry.json` exists
2. validator returns `registry=valid`
3. `orchestration/state/ACUMEN-IDENTITY-STATUS.json` is refreshed
4. non-strict preflight records identity observations even when `gcloud` or keychain state is absent

Strict variant:

```bash
make acumen-preflight STRICT=1
```

Strict identity passes only when detected account state matches `syncrescendence@gmail.com`.

If strict identity fails due active gcloud mismatch, run:

```bash
gcloud auth login syncrescendence@gmail.com
gcloud config set account syncrescendence@gmail.com
make acumen-preflight STRICT=1
```

Failure modes:

1. `registry missing` or `registry=invalid`
2. strict identity mismatch recorded in `ACUMEN-IDENTITY-STATUS.json`

## Step 2: Repeatable Sample Run

```bash
make acumen-sample-run
```

This single target executes the local repeatable path:

1. preflight
2. sample triage prompt render
3. sample deterministic transcript artifact
4. sample Dawn Brief compile
5. sequential pipeline wrapper over `triage-decisions.sample.jsonl`

Primary outputs:

1. `runtime/acumen/out/triage-packet.sample.md`
2. `runtime/acumen/out/deterministic-sample.md`
3. `runtime/acumen/out/DAWN-BRIEF-sample.md`
4. `runtime/acumen/out/DAWN-BRIEF-YYYYMMDD.md`
5. `orchestration/state/ACUMEN-IDENTITY-STATUS.json`
6. `orchestration/state/ACUMEN-PIPELINE-STATUS.json`

Useful overrides:

1. `STRICT=1`
2. `POLISH=charitable`
3. `STATUS_JSON=/abs/path/custom-status.json`
4. `QUEUE=/abs/path/triage-decisions.jsonl`

## Step 3: Build Triage Packet From Real Metadata

Create a local video metadata JSON with:

1. `title`
2. `duration`
3. `description`
4. `initial_transcript`

Then run:

```bash
make acumen-build-triage-packet CHANNEL_ID=UC_x5XG1OV2P6uZZ5FSM9Ttw VIDEO_JSON=/abs/path/video.json OUTPUT=/Users/system/syncrescendence/runtime/acumen/out/triage-packet.md
```

Expected output:

1. markdown prompt artifact only

Failure modes:

1. `channel not found in registry`
2. `video metadata missing required keys`

## Step 4: Run Deterministic Track

```bash
make acumen-deterministic-track INPUT_TEXT=/abs/path/transcript.txt GENRE=Commentary DEPTH=Precis POLISH=charitable OUTPUT=/Users/system/syncrescendence/runtime/acumen/out/deterministic-sample.md
```

Expected output:

1. deterministic artifact written to the requested path
2. if `POLISH=charitable` or `POLISH=editorial`, the artifact explicitly states `Intelligent Track Required`

## Step 5: Compile Dawn Brief

Prepare or supply an existing triage decision queue. The queue must already exist; this repo does not generate it automatically.

Example:

```bash
make acumen-build-dawn-brief INPUT_JSONL=/Users/system/syncrescendence/runtime/acumen/triage-decisions.jsonl OUTPUT=/Users/system/syncrescendence/runtime/acumen/out/DAWN-BRIEF.md
```

## Step 6: Run Sequential Pipeline Wrapper

```bash
make acumen-pipeline-run QUEUE=/Users/system/syncrescendence/runtime/acumen/triage-decisions.jsonl OUT=/Users/system/syncrescendence/runtime/acumen/out STRICT_IDENTITY=1
```

Expected:

1. identity probe is rerun against the configured binding
2. dated Dawn Brief artifact generated under the chosen `OUT` directory
3. status written to:
   - `orchestration/state/ACUMEN-PIPELINE-STATUS.json`

Failure modes:

1. missing queue file
2. missing binding file
3. Dawn Brief compile failure
4. strict identity mismatch returns non-zero even when Dawn Brief compilation succeeded

## Guardrails

1. deterministic track always runs before any intelligent-track adapter
2. canonical Google identity for Acumen surfaces is `syncrescendence@gmail.com`
3. strict runs must fail on identity drift
4. no secrets stored in repo artifacts
5. external model calls and polling remain out of scope for this runbook until those operators land in repo
