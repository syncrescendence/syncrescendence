# Dispatch Packet

**Packet ID**: `PKT-20260308-codex-swarm-wave-6-lane-02-naming-tolerance-codification`  
**Surface**: `codex_parallel_session`  
**Role**: `direct_write`  
**Date**: `2026-03-08`  
**Objective**: codify the `11` intentional naming tolerances or false positives so report-first enforcement distinguishes permanent lineage residue from real remediation debt  
**Priority**: `high`  
**Target**: `explicit communications naming tolerances`  
**Origin lane**: `communications/prompts`  
**Expected response**: `communications/responses/RESPONSE-CODEX-SWARM-WAVE-6-LANE-02-NAMING-TOLERANCE-CODIFICATION.md`

## Decision Envelope

- **Trigger**: Wave 5 classified a stable bucket of intentional exceptions and false positives that should stop surfacing as generic debt
- **Selected approach**: encode the tolerance set explicitly in report-first validator logic and document the tolerated paths
- **Alternatives considered**:
  - leaving the warnings in generic output indefinitely — rejected because it obscures which debt is real
  - suppressing all legacy warnings broadly — rejected because acceptable debt and rename-required items must stay visible
- **Assumptions**:
  - tolerated paths should remain inspectable and bounded, not hidden in opaque ad hoc conditions
- **Inherited constraints**:
  - edit only the assigned files plus your response artifact
  - do not suppress the `acceptable legacy debt` or `rename required` buckets
  - do not change lane naming taxonomy itself

## Assigned Live Files

- [operators/validators/validate_metadata_naming.py](/Users/system/syncrescendence/operators/validators/validate_metadata_naming.py)
- [orchestration/state/COMMUNICATIONS-NAMING-TOLERANCES-v1.md](/Users/system/syncrescendence/orchestration/state/COMMUNICATIONS-NAMING-TOLERANCES-v1.md)

## Anchors

- [COMMUNICATIONS-NAMING-TRIAGE-v1.md](/Users/system/syncrescendence/orchestration/state/COMMUNICATIONS-NAMING-TRIAGE-v1.md)
- [COMMUNICATIONS-NAMING-REPORT.md](/Users/system/syncrescendence/orchestration/state/COMMUNICATIONS-NAMING-REPORT.md)

## Required Output

1. codify the `11` intentional tolerances or false positives in a bounded, inspectable way
2. preserve visibility for:
   - `6` strict-ready metadata items
   - `4` rename-required items
   - `3` acceptable legacy-debt items
3. document the tolerance set in a repo-native state artifact
4. keep the validator report-first and non-blocking
5. write a short response artifact listing the tolerance mechanism chosen and the tolerated paths
6. run `git diff --check`
7. report `complete / partial / blocked`
