# Dispatch Packet

**Packet ID**: `PKT-20260310-codex-campaign-09-lane-01-youtube-ingestion-worker-and-poll-cursor`  
**Surface**: `codex_parallel_session`  
**Role**: `direct_write`  
**Date**: `2026-03-10`  
**Objective**: implement the first real Acumen YouTube ingestion worker over the feed registry  
**Priority**: `extra_high`  
**Target**: `registry-driven YouTube polling`  
**Origin lane**: `communications/prompts`  
**Expected response**: `communications/responses/RESPONSE-CODEX-CAMPAIGN-09-LANE-01-YOUTUBE-INGESTION-WORKER-AND-POLL-CURSOR.md`

## Required Output

1. create a registry-driven YouTube ingestion worker with cadence-aware polling and cursor discipline
2. keep credentials external to repo and failure states explicit
3. produce or update runtime/status artifacts only where needed
4. avoid inventing a second intake authority outside the Acumen registry/runtime lane
5. run `git diff --check`
6. report `complete / partial / blocked`
