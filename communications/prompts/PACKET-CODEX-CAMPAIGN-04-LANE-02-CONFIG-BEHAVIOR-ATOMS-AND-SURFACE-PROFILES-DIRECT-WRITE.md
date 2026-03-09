# Dispatch Packet

**Packet ID**: `PKT-20260309-codex-campaign-04-lane-02-config-behavior-atoms-and-surface-profiles-direct-write`
**Surface**: `codex_parallel_session`
**Role**: `direct_write`
**Date**: `2026-03-09`
**Objective**: write the shell's reusable behavior-atom and surface-profile layer
**Priority**: `highest`
**Target**: `knowledge/sigma/CONFIG-BEHAVIOR-ATOMS-AND-SURFACE-PROFILES-v1.md`
**Origin lane**: `communications/prompts`
**Expected response**: `communications/responses/RESPONSE-CODEX-CAMPAIGN-04-LANE-02-CONFIG-BEHAVIOR-ATOMS-AND-SURFACE-PROFILES-DIRECT-WRITE.md`

## Required Output

1. create `knowledge/sigma/CONFIG-BEHAVIOR-ATOMS-AND-SURFACE-PROFILES-v1.md`
2. define the first atom families that should be stable across chat, CLI, skills, hooks, schemas, templates, and ledgers
3. define surface profiles and lawful compression rules for each surface class
4. bind the atoms to the custom-instruction witness corpus without copying vendor phrasing downward
5. run `git diff --check`
6. report `complete / partial / blocked`
