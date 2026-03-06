# Dispatch Packet

**Packet ID**: `PKT-20260306-codex-swarm-wave-2-lane-01-knowledge-compatibility`  
**Surface**: `codex_parallel_session`  
**Role**: `drafting`  
**Date**: `2026-03-06`  
**Objective**: draft the minimal live-facing doc updates required so the repo stops treating bare `knowledge/references/` as the sovereign secondary lane  
**Origin lane**: `communications/prompts`  
**Expected response**: `communications/responses/RESPONSE-CODEX-SWARM-WAVE-2-LANE-01-KNOWLEDGE-COMPATIBILITY.md`

## Decision Envelope

- **Trigger**: Sigma ratification is landed, but several live-facing docs still describe bare `knowledge/references/` as if it were the enduring lane identity
- **Selected approach**: identify only the smallest necessary readmes and law surfaces to update now
- **Alternatives considered**:
  - mass path rewrite — rejected because compatibility semantics remain intentional for now
- **Assumptions**:
  - `knowledge/sigma/` is binding
- **Inherited constraints**:
  - write only to your assigned response file
  - do not edit shared files

## Anchors

- [KNOWLEDGE-LANE-LAW-v1.md](/Users/system/syncrescendence/orchestration/state/impl/KNOWLEDGE-LANE-LAW-v1.md)
- [knowledge/README.md](/Users/system/syncrescendence/knowledge/README.md)
- [knowledge/feedstock/README.md](/Users/system/syncrescendence/knowledge/feedstock/README.md)
- [README.md](/Users/system/syncrescendence/README.md)

## Required Output

1. list of exact docs that must change now
2. patch-ready replacement text or diff blocks for each
3. compatibility wording that preserves current readability without diluting Sigma
4. top failure modes if this cleanup is skipped
5. complete / partial / blocked status
