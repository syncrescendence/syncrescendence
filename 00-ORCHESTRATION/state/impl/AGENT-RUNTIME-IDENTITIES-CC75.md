# Agent Runtime Identities

**Date**: 2026-03-02  
**Purpose**: freeze the current live agent/account split after local OpenClaw repair work

## Current Assignment

- `Ajna`
  - machine: `Lisa's MacBook Air`
  - OpenClaw state dir: `/Users/system/.openclaw`
  - provider: `anthropic`
  - model: `claude-sonnet-4-5`
  - auth mode: Claude setup-token / token-mode profile
  - role: Claude-backed browser-capable operational agent

- `Psyche`
  - machine: `M1-Mac-mini.local`
  - OpenClaw state dir: `/Users/home/.openclaw`
  - provider: `openai-codex`
  - model: `gpt-5.3-codex`
  - auth mode: OAuth profile
  - account: `truongphillipthanh@icloud.com`
  - subscription: ChatGPT Plus
  - role: ChatGPT Plus-backed constellation agent on the Mac mini

## What Was Repaired

- Ajna:
  - Claude token auth restored
  - gateway daemon repaired
  - stale session-store shape repaired
  - OpenClaw upgraded to `2026.3.1`

- Psyche:
  - OpenClaw upgraded to `2026.3.1`
  - repo-managed workspace surface redeployed
  - gateway daemon reinstalled
  - session-store reset and revalidated
  - final runtime moved back to ChatGPT Plus / `openai-codex`

## Operational Rule

Do not collapse both agents onto the same auth surface by accident.

- Ajna stays on Claude unless explicitly changed.
- Psyche stays on ChatGPT Plus / `openai-codex` unless explicitly changed.
- Any future rewiring must update:
  - `00-ORCHESTRATION/state/TOOL-STACK-LIVE-STATE.md`
  - `00-ORCHESTRATION/state/MINI-CONSTELLATION-STATUS.md`
  - local workspace `MEMORY.md` files
