# Dispatch Packet

**Packet ID**: `PKT-20260308-codex-swarm-wave-6-lane-01-strict-ready-metadata-normalization`  
**Surface**: `codex_parallel_session`  
**Role**: `direct_write`  
**Date**: `2026-03-08`  
**Objective**: normalize the `6` strict-ready communications files so they satisfy the naming validator’s metadata expectations without moving lineage  
**Priority**: `high`  
**Target**: `strict-ready communications metadata subset`  
**Origin lane**: `communications/prompts`  
**Expected response**: `communications/responses/RESPONSE-CODEX-SWARM-WAVE-6-LANE-01-STRICT-READY-METADATA-NORMALIZATION.md`

## Decision Envelope

- **Trigger**: Wave 5 classified the communications naming warnings and isolated a small strict-ready metadata subset
- **Selected approach**: add the minimum expected lane markers to the identified files without renaming them or rewriting their substantive content
- **Alternatives considered**:
  - renaming warned files now — rejected because rename-required debt is a separate non-strict-ready bucket
  - normalizing the entire warning set — rejected because only `6` files are safe and high-yield in this wave
- **Assumptions**:
  - adding the validator’s expected metadata markers is sufficient to retire these warnings
- **Inherited constraints**:
  - edit only the assigned files plus your response artifact
  - do not rename any files
  - do not alter doctrinal meaning or raw response substance beyond metadata framing

## Assigned Live Files

- [communications/prompts/PACKET-MANUS-cc86-owner-cutover-execution-kits.md](/Users/system/syncrescendence/communications/prompts/PACKET-MANUS-cc86-owner-cutover-execution-kits.md)
- [communications/prompts/PACKET-MANUS-cc86b-owner-cutover-kits-inline.md](/Users/system/syncrescendence/communications/prompts/PACKET-MANUS-cc86b-owner-cutover-kits-inline.md)
- [communications/responses/RESPONSE-ORACLE-CONFIG-CONSENSUS-ARCHITECTURE-CC92.md](/Users/system/syncrescendence/communications/responses/RESPONSE-ORACLE-CONFIG-CONSENSUS-ARCHITECTURE-CC92.md)
- [communications/responses/RESPONSE-ORACLE-MEMORY-ARCHITECTURE-SENSING-CC92.md](/Users/system/syncrescendence/communications/responses/RESPONSE-ORACLE-MEMORY-ARCHITECTURE-SENSING-CC92.md)
- [communications/responses/RESPONSE-ORACLE-SCAFFOLD-CONSENSUS-CC92.md](/Users/system/syncrescendence/communications/responses/RESPONSE-ORACLE-SCAFFOLD-CONSENSUS-CC92.md)
- [communications/responses/RESPONSE-ORACLE-SYNTHESIS-RECONCILIATION-CC92.md](/Users/system/syncrescendence/communications/responses/RESPONSE-ORACLE-SYNTHESIS-RECONCILIATION-CC92.md)

## Anchors

- [COMMUNICATIONS-NAMING-TRIAGE-v1.md](/Users/system/syncrescendence/orchestration/state/COMMUNICATIONS-NAMING-TRIAGE-v1.md)
- [COMMUNICATIONS-NAMING-REPORT.md](/Users/system/syncrescendence/orchestration/state/COMMUNICATIONS-NAMING-REPORT.md)
- [validate_metadata_naming.py](/Users/system/syncrescendence/operators/validators/validate_metadata_naming.py)

## Required Output

1. add the minimum expected lane metadata markers to the assigned `6` files
2. preserve filenames, substantive body text, and lineage framing
3. avoid introducing duplicated headers or malformed front matter
4. write a short response artifact listing which markers were added where
5. run `git diff --check`
6. report `complete / partial / blocked`
