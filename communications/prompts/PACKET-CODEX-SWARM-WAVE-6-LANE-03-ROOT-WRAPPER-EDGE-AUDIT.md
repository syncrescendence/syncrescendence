# Dispatch Packet

**Packet ID**: `PKT-20260308-codex-swarm-wave-6-lane-03-root-wrapper-edge-audit`  
**Surface**: `codex_parallel_session`  
**Role**: `assessment`  
**Date**: `2026-03-08`  
**Objective**: audit local edge callers for the transitional root wrapper path and produce runtime evidence for or against future retirement  
**Priority**: `high`  
**Target**: `external caller truth for finalize_cowork_relay_job.py`  
**Origin lane**: `communications/prompts`  
**Expected response**: `communications/responses/RESPONSE-CODEX-SWARM-WAVE-6-LANE-03-ROOT-WRAPPER-EDGE-AUDIT.md`

## Decision Envelope

- **Trigger**: Wave 5 reduced the root-wrapper problem to one unresolved question: whether live edge automation still invokes the root path outside the repo
- **Selected approach**: perform a bounded local search for likely caller surfaces and write a repo-native audit artifact
- **Alternatives considered**:
  - deleting the wrapper now — rejected because runtime-edge evidence is still missing
  - deferring all audit work indefinitely — rejected because the remaining constitutional warning is now almost entirely an external-caller question
- **Assumptions**:
  - likely caller surfaces include Hazel configuration, LaunchAgents, shell aliases, helper scripts, and adjacent local automation files
- **Inherited constraints**:
  - do not modify external machine configuration in this lane
  - clearly separate confirmed callers from plausible-but-unverified risks
  - keep the search bounded to reasonable local roots under `/Users/system`

## Assigned Live Files

- [orchestration/state/ROOT-WRAPPER-EDGE-AUDIT-v1.md](/Users/system/syncrescendence/orchestration/state/ROOT-WRAPPER-EDGE-AUDIT-v1.md)

## Anchors

- [TRANSITIONAL-ROOT-OPERATOR-INTERNALIZATION-PLAN-v1.md](/Users/system/syncrescendence/orchestration/state/TRANSITIONAL-ROOT-OPERATOR-INTERNALIZATION-PLAN-v1.md)
- [finalize_cowork_relay_job.py](/Users/system/syncrescendence/finalize_cowork_relay_job.py)
- [operators/cli-web-gap/finalize_cowork_relay_job.py](/Users/system/syncrescendence/operators/cli-web-gap/finalize_cowork_relay_job.py)

## Required Output

1. search likely local roots for references to `/Users/system/syncrescendence/finalize_cowork_relay_job.py`
2. distinguish:
   - confirmed active caller candidates
   - stale historical references
   - no-hit search areas
3. recommend whether wrapper retirement is safe next wave or still blocked
4. keep the repo-native audit artifact concrete and evidence-based
5. write a short response artifact summarizing findings and search roots
6. run `git diff --check`
7. report `complete / partial / blocked`
