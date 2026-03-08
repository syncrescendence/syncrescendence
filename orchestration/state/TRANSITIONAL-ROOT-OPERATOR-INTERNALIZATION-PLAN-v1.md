# Transitional Root Operator Internalization Plan v1

**Date**: `2026-03-08`  
**Status**: `bounded readiness plan`  
**Subject**: `finalize_cowork_relay_job.py`

## 1. Verified Current State

- The root file [finalize_cowork_relay_job.py](/Users/system/syncrescendence/finalize_cowork_relay_job.py) is a pure compatibility wrapper that immediately dispatches into [operators/cli-web-gap/finalize_cowork_relay_job.py](/Users/system/syncrescendence/operators/cli-web-gap/finalize_cowork_relay_job.py).
- The canonical implementation already lives under [operators/cli-web-gap/finalize_cowork_relay_job.py](/Users/system/syncrescendence/operators/cli-web-gap/finalize_cowork_relay_job.py).
- The current constitutional warning is emitted only because [operators/validators/validate_constitution.py](/Users/system/syncrescendence/operators/validators/validate_constitution.py) still treats the root wrapper as a transitional exception.
- In-repo Hazel guidance already points to the operator path, not the root path:
  - [orchestration/relay/cowork-v1/HAZEL-RULES.md](/Users/system/syncrescendence/orchestration/relay/cowork-v1/HAZEL-RULES.md)
  - [validated-patterns/cli-web-gap/HAZEL-RULES.md](/Users/system/syncrescendence/validated-patterns/cli-web-gap/HAZEL-RULES.md)

## 2. In-Repo Reference Inventory

### 2.1 Runtime or enforcement surfaces

- [finalize_cowork_relay_job.py](/Users/system/syncrescendence/finalize_cowork_relay_job.py): the remaining root compatibility entrypoint.
- [operators/validators/validate_constitution.py](/Users/system/syncrescendence/operators/validators/validate_constitution.py): emits the warning by allowlisting the wrapper as `TRANSITIONAL_ROOT`.
- [operators/validators/artifact_law_inventory.py](/Users/system/syncrescendence/operators/validators/artifact_law_inventory.py): records the wrapper as a `transitional-root` operator for inventory purposes.

### 2.2 Documentation-only references

- [orchestration/state/CONSTITUTION-VALIDATION-REPORT.md](/Users/system/syncrescendence/orchestration/state/CONSTITUTION-VALIDATION-REPORT.md)
- [communications/handoffs/HANDOFF-CC92-REPO-MIGRATION-ORACLE-CONVERGENCE.md](/Users/system/syncrescendence/communications/handoffs/HANDOFF-CC92-REPO-MIGRATION-ORACLE-CONVERGENCE.md)
- [communications/handoffs/HANDOFF-20260307-WAVE-4-CC92-UNIFIED-FRONTIER.md](/Users/system/syncrescendence/communications/handoffs/HANDOFF-20260307-WAVE-4-CC92-UNIFIED-FRONTIER.md)
- [orchestration/state/impl/ROOT-CUTOVER-TRANCHE-01.md](/Users/system/syncrescendence/orchestration/state/impl/ROOT-CUTOVER-TRANCHE-01.md)
- [orchestration/state/impl/TRANSITIONAL-ALLOWLIST-v1.md](/Users/system/syncrescendence/orchestration/state/impl/TRANSITIONAL-ALLOWLIST-v1.md)
- [orchestration/state/impl/SCRIPT-OPERATOR-TAXONOMY-v1.md](/Users/system/syncrescendence/orchestration/state/impl/SCRIPT-OPERATOR-TAXONOMY-v1.md)
- [orchestration/state/impl/ARTIFACT-LAW-VALIDATOR-SPEC-v1.md](/Users/system/syncrescendence/orchestration/state/impl/ARTIFACT-LAW-VALIDATOR-SPEC-v1.md)
- [pedigree/archive-manifests/pre-schematic-design.md](/Users/system/syncrescendence/pedigree/archive-manifests/pre-schematic-design.md)
- [pedigree/archive-manifests/pre-schematic-design.json](/Users/system/syncrescendence/pedigree/archive-manifests/pre-schematic-design.json)

## 3. Classification

### 3.1 Safe in-repo direct-write cutovers

- Hazel documentation is already cut over to the operator path, so no in-repo Hazel command rewrite is still pending.
- The future retirement-critical repo edits are narrow:
  1. delete [finalize_cowork_relay_job.py](/Users/system/syncrescendence/finalize_cowork_relay_job.py)
  2. remove `finalize_cowork_relay_job.py` from `TRANSITIONAL_ROOT` in [operators/validators/validate_constitution.py](/Users/system/syncrescendence/operators/validators/validate_constitution.py)
  3. remove `finalize_cowork_relay_job.py` from `TRANSITIONAL_ROOT_OPERATORS` in [operators/validators/artifact_law_inventory.py](/Users/system/syncrescendence/operators/validators/artifact_law_inventory.py)
  4. regenerate the inventory and constitution reports

### 3.2 Probable out-of-repo dependency risks

- Assumption: a live Hazel rule on the local machine may still call the root path from an older configuration, even though the repo docs now point to the operator path.
- Assumption: other local edge automations may still reference the root path, such as shell aliases, LaunchAgents, Keyboard Maestro, Alfred, or ad hoc scripts outside the repo.
- These risks are plausible but not proven from repo evidence alone.

### 3.3 Documentation-only references

- The remaining mentions outside the validator/inventory surfaces are historical, planning, or report artifacts.
- Those references do not block runtime retirement once the real callsites are repointed.
- They can be cleaned up after retirement without affecting the relay path.

## 4. Minimum Safe Future Direct-Write Set

1. Audit local Hazel and adjacent edge automation for any remaining invocation of `/Users/system/syncrescendence/finalize_cowork_relay_job.py`.
2. Repoint any discovered external caller to `/Users/system/syncrescendence/operators/cli-web-gap/finalize_cowork_relay_job.py`.
3. Delete the root wrapper.
4. Remove the wrapper from the validator and artifact-law transitional sets.
5. Regenerate:
   - `make validate-constitution`
   - `make check-artifact-law`
6. Update documentation and handoff references opportunistically after the runtime cutover is complete.

## 5. Recommendation

- The next wave should **keep the wrapper temporarily tolerated at wave start**, not retire it blindly.
- The reason is not an in-repo blocker; it is the unverified out-of-repo edge dependency surface.
- If the next wave can positively verify or repoint those external callsites, retirement should happen immediately afterward in the same tranche.
- If that verification cannot be completed, the wrapper should remain explicitly tolerated and the validator warning should stay as the visible hold-open signal.
