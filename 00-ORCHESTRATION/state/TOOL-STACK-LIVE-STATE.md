# Tool Stack Live State

**Date**: 2026-03-02  
**Purpose**: factual live runtime snapshot for repo↔harness reconciliation  
**Status**: ACTIVE reference for current tool-stack truth

---

## Live Runtime Facts

- `syncrescendence.com` is secured
- OpenClaw gateway is live on the MacBook Air at `127.0.0.1:18789`
- Ajna's current primary model in live OpenClaw config is `anthropic/claude-sonnet-4-5`
- OpenClaw workspace path is `/Users/system/.openclaw/workspace`
- Browser is not denied in OpenClaw
- Ajna has `playwright-mcp` skill installed
- Slack channel is currently disabled
- Discord channel is currently disabled
- `exec`, `process`, and `apply_patch` remain denied in OpenClaw
- Rendered + validated config scaffold now exists locally:
  - `harness/*.json`
  - `machine/*.json`
  - `render-configs.py`
  - `validate-configs.py`
  - `configs/manifest.json`
- OpenClaw repo↔runtime tooling now exists locally:
  - `make deploy-ajna`
  - `make sync-openclaw`
  - `sync-openclaw.py`
  - `00-ORCHESTRATION/state/OPENCLAW-RUNTIME-SNAPSHOT.md`
  - `memory/AJNA-RUNTIME-SYNTHESIS.md`
- Ajna event reconciliation now exists locally:
  - `make reconcile-ajna-events`
  - `reconcile-ajna-events.py`
  - `memory/AJNA-EVENT-LEDGER.jsonl`
  - `memory/AJNA-EVENT-SUMMARY.md`
  - `00-ORCHESTRATION/state/AJNA-EVENT-RECONCILIATION.json`
- Ajna's OpenClaw workspace instruction surface has been compacted below the 20k bootstrap ceiling

## Current Truth Split

- Repo constitutional/orientation docs have been partially reconciled, but historical artifacts still narrate Ajna as Kimi-primary
- Live OpenClaw runtime has already moved Ajna onto Claude Sonnet
- Config scaffold is implemented in-repo and Ajna workspace deployment is now repo-driven
- Memory remains split across repo memory, OpenClaw workspace memory, and session logs, but there is now a first synthesis loop back into repo memory
- Ajna can now emit durable event files into a landing zone that Commander reconciles into repo state

## Immediate Blockers

1. The current sync loop is snapshot-first and still needs richer normalization rules
2. Memory synthesis is still first-pass and not yet canon-promotion aware
3. Historical documents still preserve pre-rewire Ajna/Kimi assumptions
4. OpenClaw LaunchAgent restart path is still brittle; the gateway currently recovers cleanly in foreground mode
5. `gcloud` still needs one-time browser OAuth
6. `wrangler` still needs one-time browser OAuth

## Authority

- Strategic architecture: `engine/CC65-TOOL-STACK-FINAL.md`
- Current narrowing brief: `engine/CC72b-IMPLEMENTATION-BRIEF.md`
- This file is the factual runtime snapshot, not the long-term architecture
