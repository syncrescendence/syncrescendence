# Tool Stack Live State

**Date**: 2026-03-02  
**Purpose**: factual live runtime snapshot for repo↔harness reconciliation  
**Status**: ACTIVE reference for current tool-stack truth

---

## Live Runtime Facts

- `syncrescendence.com` is secured
- OpenClaw gateway is live on the MacBook Air at `127.0.0.1:18789`
- Ajna's current primary model in live OpenClaw config is `anthropic/claude-sonnet-4-5`
- Ajna is now running cleanly on OpenClaw `2026.3.1`
- OpenClaw workspace path is `/Users/system/.openclaw/workspace`
- Browser is not denied in OpenClaw
- Ajna has `playwright-mcp` skill(s) installed
- Slack channel is currently enabled
- Discord channel is currently enabled
- Slack socket mode tokens are configured in runtime: bot=`True` app=`True`
- Slack keychain entries are present: bot=`True` app=`True`
- Slack probe status: running=`True` probeOk=`True` inbound=`None` outbound=`None`
- Discord bot token is configured in runtime: `True`
- Discord keychain entry is present: `True`
- Discord probe status: running=`True` probeOk=`True` inbound=`None` outbound=`None`
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
- Mac mini OpenClaw gateway is live on `127.0.0.1:18789`
- Psyche now runs on `openai-codex/gpt-5.3-codex` using the ChatGPT Plus account `truongphillipthanh@icloud.com`
- Mac mini OpenClaw is now running `2026.3.1`
- Mac mini channels are intentionally cleared in runtime config pending future re-onboarding

## Current Truth Split

- Repo constitutional/orientation docs have been partially reconciled, but historical artifacts still narrate Ajna as Kimi-primary
- Live OpenClaw runtime has already moved Ajna onto Claude Sonnet
- Live OpenClaw runtime on the Mac mini now keeps Psyche on ChatGPT Plus / `openai-codex`
- Config scaffold is implemented in-repo and Ajna workspace deployment is now repo-driven
- Memory remains split across repo memory, OpenClaw workspace memory, and session logs, but there is now a first synthesis loop back into repo memory
- Ajna can now emit durable event files into a landing zone that Commander reconciles into repo state

## Active Runtime Split

- `Ajna`:
  - machine: MacBook Air
  - provider: `anthropic`
  - model: `claude-sonnet-4-5`
  - role: browser-capable Claude/OpenClaw operational agent
- `Psyche`:
  - machine: Mac mini
  - provider: `openai-codex`
  - model: `gpt-5.3-codex`
  - role: tmux constellation substrate + ChatGPT Plus-backed agent surface

## Immediate Blockers

1. The current sync loop is snapshot-first and still needs richer normalization rules
2. Memory synthesis is still first-pass and not yet canon-promotion aware
3. Historical documents still preserve pre-rewire Ajna/Kimi assumptions
4. Slack and Discord are healthy on the MacBook Air at the provider layer, but no inbound/outbound traffic has been observed in runtime yet
5. OpenClaw stores active channel credentials in local runtime config; repo truth remains pointer-only and repo-safe
6. Mac mini role and account split must remain explicit so future rewiring does not collapse Psyche back onto Claude by accident

## Authority

- Strategic architecture: `engine/CC65-TOOL-STACK-FINAL.md`
- Current narrowing brief: `engine/CC72b-IMPLEMENTATION-BRIEF.md`
- This file is the factual runtime snapshot, not the long-term architecture
