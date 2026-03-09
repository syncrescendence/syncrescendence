# Dispatch Packet

**Packet ID**: `PKT-20260309-codex-campaign-04-lane-03-office-harness-binding-contract-direct-write`
**Surface**: `codex_parallel_session`
**Role**: `direct_write`
**Date**: `2026-03-09`
**Objective**: write the durable office-harness binding law
**Priority**: `highest`
**Target**: `orchestration/state/impl/OFFICE-HARNESS-BINDING-CONTRACT-v1.md`
**Origin lane**: `communications/prompts`
**Expected response**: `communications/responses/RESPONSE-CODEX-CAMPAIGN-04-LANE-03-OFFICE-HARNESS-BINDING-CONTRACT-DIRECT-WRITE.md`

## Required Output

1. create `orchestration/state/impl/OFFICE-HARNESS-BINDING-CONTRACT-v1.md`
2. define stable office identity, mutable harness binding, precedence, rebinding law, and ratification-pointer obligations
3. ensure the contract is compatible with the repo / exocortex / ontology sovereignty split
4. keep the file focused on law, not on validator implementation detail beyond minimum obligations
5. run `git diff --check`
6. report `complete / partial / blocked`
