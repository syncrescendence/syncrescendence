# Transitional Allowlist v1

**Date**: 2026-03-02  
**Status**: tranche-01 control artifact  
**Purpose**: explicitly record the temporary exceptions allowed during shell redesign so drift is visible rather than silently normalized

---

## 0. Why This Exists

The redesign cannot harden if "temporary exceptions" live only in memory.

This allowlist exists so that:

- compatibility exceptions are explicit
- root-level spill is measured rather than hand-waved
- temporary paths can later be retired deliberately

This is a transitional control artifact, not a permanent constitutional destination.

---

## 1. Root-Level Operator Allowlist

These root-level operators are currently tolerated as transitional:

- [artifact_law_inventory.py](/Users/system/syncrescendence/artifact_law_inventory.py)
- [bootstrap-mac-mini.sh](/Users/system/syncrescendence/bootstrap-mac-mini.sh)
- [channel_surface_bridge.py](/Users/system/syncrescendence/channel_surface_bridge.py)
- [cloudflare_domain_bridge.py](/Users/system/syncrescendence/cloudflare_domain_bridge.py)
- [collect-mini-constellation-status.py](/Users/system/syncrescendence/collect-mini-constellation-status.py)
- [collect-tooling-surface-status.py](/Users/system/syncrescendence/collect-tooling-surface-status.py)
- [constellation-mini-stage1.sh](/Users/system/syncrescendence/constellation-mini-stage1.sh)
- [exocortex_event_bridge.py](/Users/system/syncrescendence/exocortex_event_bridge.py)
- [finalize_cowork_relay_job.py](/Users/system/syncrescendence/finalize_cowork_relay_job.py)
- [github_issue_bridge.py](/Users/system/syncrescendence/github_issue_bridge.py)
- [google_model_bridge.py](/Users/system/syncrescendence/google_model_bridge.py)
- [hydrate-openclaw-channels.py](/Users/system/syncrescendence/hydrate-openclaw-channels.py)
- [install-mini-constellation-launchagent.sh](/Users/system/syncrescendence/install-mini-constellation-launchagent.sh)
- [manus_checkpoint_bridge.py](/Users/system/syncrescendence/manus_checkpoint_bridge.py)
- [normalize_event_ledger.py](/Users/system/syncrescendence/normalize_event_ledger.py)
- [obsidian_repo_bridge.py](/Users/system/syncrescendence/obsidian_repo_bridge.py)
- [ontology_v1.py](/Users/system/syncrescendence/ontology_v1.py)
- [reconcile-ajna-events.py](/Users/system/syncrescendence/reconcile-ajna-events.py)
- [render-configs.py](/Users/system/syncrescendence/render-configs.py)
- [sanitize-openclaw-events.py](/Users/system/syncrescendence/sanitize-openclaw-events.py)
- [sync-openclaw.py](/Users/system/syncrescendence/sync-openclaw.py)
- [validate-configs.py](/Users/system/syncrescendence/validate-configs.py)
- [xai_model_bridge.py](/Users/system/syncrescendence/xai_model_bridge.py)
- [youtube_feed_bridge.py](/Users/system/syncrescendence/youtube_feed_bridge.py)

These are tolerated because:

- they are active,
- they underpin live runtime/tooling behavior,
- and a safe operator lane has not yet physically replaced them.

---

## 2. Root-Level Non-Operator Transitional Files

These root-level files remain transitional exceptions and should be accounted for in future shell work:

- [ontology_v1_schema.sql](/Users/system/syncrescendence/ontology_v1_schema.sql)
- [requirements-ontology.txt](/Users/system/syncrescendence/requirements-ontology.txt)

They are not illegal in the short term, but they are evidence that the target shell has not yet fully absorbed registry-related materials.

---

## 3. Legacy Lane Allowlist

These lanes are allowed to remain active temporarily:

- [engine](/Users/system/syncrescendence/engine)
- [-INBOX](/Users/system/syncrescendence/-INBOX)
- [00-ORCHESTRATION/state](/Users/system/syncrescendence/00-ORCHESTRATION/state)
- [00-ORCHESTRATION/state/impl](/Users/system/syncrescendence/00-ORCHESTRATION/state/impl)
- [CLI-WEB-GAP](/Users/system/syncrescendence/CLI-WEB-GAP)

Allowed does not mean final.
It means migration has not yet safely replaced them.

---

## 4. Misfiled Historical Exceptions

The inventory already shows some classes that are currently tolerated only as historical debt:

- prompts and responses in [ascertescence](/Users/system/syncrescendence/ascertescence)
- legacy handoffs in [memory](/Users/system/syncrescendence/memory)

These are not sanctioned live patterns.
They are transitional debt to be handled by later migration tranches.

---

## 5. Retirement Rule

An item leaves this allowlist only when:

1. a successor lane or mechanism exists,
2. the live behavior has moved,
3. validators can flag new use safely,
4. historical provenance is preserved.

---

## 6. Net Rule

If an exception matters enough to preserve, it matters enough to name.

Unnamed exceptions are just ungoverned drift.
