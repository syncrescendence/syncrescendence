# Root Wrapper Retirement Patchset v1

**Date**: `2026-03-08`  
**Status**: `prepared for post-cutover application`  
**Subject**: `finalize_cowork_relay_job.py`

## 1. Cutover Gate

Apply this patch set only after the live Hazel rule has been verified to:

1. call `/Users/system/syncrescendence/operators/cli-web-gap/finalize_cowork_relay_job.py`
2. stop passing unsupported `--project-ontology`
3. produce at least one successful post-cutover finalization

This lane does **not** delete the wrapper now. It prepares the exact repo-side patch set for immediate use once that evidence exists.

## 2. Required Runtime Or Validator Cleanup

These items are safe immediately after successful Hazel cutover and should land in the same retirement tranche.

### 2.1 Delete the root compatibility wrapper

File:

- [finalize_cowork_relay_job.py](/Users/system/syncrescendence/finalize_cowork_relay_job.py)

Exact patch:

```diff
diff --git a/finalize_cowork_relay_job.py b/finalize_cowork_relay_job.py
deleted file mode 100755
--- a/finalize_cowork_relay_job.py
+++ /dev/null
@@ -1,11 +0,0 @@
-#!/usr/bin/env python3
-"""Compatibility wrapper for Hazel until local rules are repointed."""
-
-from __future__ import annotations
-
-from pathlib import Path
-import runpy
-import sys
-
-TARGET = Path(__file__).resolve().parent / "operators" / "cli-web-gap" / "finalize_cowork_relay_job.py"
-sys.argv[0] = str(TARGET)
-runpy.run_path(str(TARGET), run_name="__main__")
```

### 2.2 Remove the constitutional transitional allowlist entry

File:

- [validate_constitution.py](/Users/system/syncrescendence/operators/validators/validate_constitution.py)

Exact patch:

```diff
diff --git a/operators/validators/validate_constitution.py b/operators/validators/validate_constitution.py
--- a/operators/validators/validate_constitution.py
+++ b/operators/validators/validate_constitution.py
@@
-TRANSITIONAL_ROOT = {
-    "finalize_cowork_relay_job.py",
-}
+TRANSITIONAL_ROOT = set()
```

Expected effect:

- the warning in [CONSTITUTION-VALIDATION-REPORT.md](/Users/system/syncrescendence/orchestration/state/CONSTITUTION-VALIDATION-REPORT.md) drops from `1` to `0`

### 2.3 Remove the artifact-law transitional root allowlist entry

File:

- [artifact_law_inventory.py](/Users/system/syncrescendence/operators/validators/artifact_law_inventory.py)

Exact patch:

```diff
diff --git a/operators/validators/artifact_law_inventory.py b/operators/validators/artifact_law_inventory.py
--- a/operators/validators/artifact_law_inventory.py
+++ b/operators/validators/artifact_law_inventory.py
@@
-TRANSITIONAL_ROOT_OPERATORS = {
-    "finalize_cowork_relay_job.py",
-}
+TRANSITIONAL_ROOT_OPERATORS = set()
```

Expected effect:

- [ARTIFACT-LAW-INVENTORY.md](/Users/system/syncrescendence/orchestration/state/ARTIFACT-LAW-INVENTORY.md) `Root-level operators` drops from `1` to `0`
- the `root_operators` `transitional-root` bucket disappears from the rendered inventory

## 3. Report Regeneration Steps

These are safe immediately after the three required cleanup edits above.

1. Run `make validate-constitution`.
2. Run `make check-artifact-law`.

Files expected to refresh:

- [CONSTITUTION-VALIDATION-REPORT.json](/Users/system/syncrescendence/orchestration/state/CONSTITUTION-VALIDATION-REPORT.json)
- [CONSTITUTION-VALIDATION-REPORT.md](/Users/system/syncrescendence/orchestration/state/CONSTITUTION-VALIDATION-REPORT.md)
- [ARTIFACT-LAW-INVENTORY.json](/Users/system/syncrescendence/orchestration/state/ARTIFACT-LAW-INVENTORY.json)
- [ARTIFACT-LAW-INVENTORY.md](/Users/system/syncrescendence/orchestration/state/ARTIFACT-LAW-INVENTORY.md)

Expected post-regeneration state:

- constitution validation still has `0` errors and now `0` warnings
- artifact-law inventory still has `0` unknown top-level entries and now `0` root-level operators

## 4. Documentation-Only Follow-On Cleanup

These items can wait until after the runtime retirement patch lands. They do not block wrapper deletion.

### 4.1 Active guidance worth updating

- [validated-patterns/cli-web-gap/HAZEL-RULES.md](/Users/system/syncrescendence/validated-patterns/cli-web-gap/HAZEL-RULES.md)
  - remove stale `--project-ontology` so repo guidance matches the operator CLI
- [orchestration/state/impl/TRANSITIONAL-ALLOWLIST-v1.md](/Users/system/syncrescendence/orchestration/state/impl/TRANSITIONAL-ALLOWLIST-v1.md)
  - remove or close out the wrapper's transitional entry if the document is still treated as live doctrine
- [orchestration/state/impl/SCRIPT-OPERATOR-TAXONOMY-v1.md](/Users/system/syncrescendence/orchestration/state/impl/SCRIPT-OPERATOR-TAXONOMY-v1.md)
  - remove the wrapper from current taxonomy if the file is kept current
- [orchestration/state/impl/ROOT-CUTOVER-TRANCHE-01.md](/Users/system/syncrescendence/orchestration/state/impl/ROOT-CUTOVER-TRANCHE-01.md)
  - mark the retirement step complete instead of pending
- [communications/handoffs/HANDOFF-CC92-REPO-MIGRATION-ORACLE-CONVERGENCE.md](/Users/system/syncrescendence/communications/handoffs/HANDOFF-CC92-REPO-MIGRATION-ORACLE-CONVERGENCE.md)
- [communications/handoffs/HANDOFF-20260307-WAVE-4-CC92-UNIFIED-FRONTIER.md](/Users/system/syncrescendence/communications/handoffs/HANDOFF-20260307-WAVE-4-CC92-UNIFIED-FRONTIER.md)
  - update only if those handoffs are still used as active operational guidance
- [orchestration/state/impl/ARTIFACT-LAW-VALIDATOR-SPEC-v1.md](/Users/system/syncrescendence/orchestration/state/impl/ARTIFACT-LAW-VALIDATOR-SPEC-v1.md)
  - adjust examples if the spec is intended to describe the post-retirement steady state

### 4.2 Historical evidence that should usually stay untouched

- [TRANSITIONAL-ROOT-OPERATOR-INTERNALIZATION-PLAN-v1.md](/Users/system/syncrescendence/orchestration/state/TRANSITIONAL-ROOT-OPERATOR-INTERNALIZATION-PLAN-v1.md)
- [ROOT-WRAPPER-EDGE-AUDIT-v1.md](/Users/system/syncrescendence/orchestration/state/ROOT-WRAPPER-EDGE-AUDIT-v1.md)
- prior wave prompt and response artifacts under [communications](/Users/system/syncrescendence/communications)
- pedigree snapshots under [pedigree/archive-manifests](/Users/system/syncrescendence/pedigree/archive-manifests)

These are historical receipts of pre-cutover state. They do not need to be rewritten as part of the retirement patch.

## 5. Minimal Landing Order

Once cutover evidence exists, the fastest safe retirement sequence is:

1. apply the three required cleanup edits in Section 2
2. run the two regeneration commands in Section 3
3. confirm the reports reflect `0` wrapper warnings and `0` root-level operators
4. defer Section 4 until convenient

## 6. Final Classification

- required immediately after cutover:
  - delete [finalize_cowork_relay_job.py](/Users/system/syncrescendence/finalize_cowork_relay_job.py)
  - edit [validate_constitution.py](/Users/system/syncrescendence/operators/validators/validate_constitution.py)
  - edit [artifact_law_inventory.py](/Users/system/syncrescendence/operators/validators/artifact_law_inventory.py)
  - regenerate the four report artifacts
- safe to defer:
  - documentation-only cleanup listed in Section 4
- current posture:
  - prepared, but not yet applied because live Hazel cutover evidence is still required
