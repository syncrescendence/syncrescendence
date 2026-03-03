# Script and Operator Taxonomy v1

**Date**: 2026-03-02  
**Status**: operator-law design  
**Purpose**: classify current scripts and automation-facing tools into a legal operator taxonomy, define what class of work they perform, and specify how they should live in the next shell

---

## 0. Why This Exists

Scripts currently prove the system works, but they do not yet live under a clear operator law.

At repo root and nearby lanes, operators are mixed together:

- staging
- validation
- runtime sync
- event reconciliation
- bridge emitters
- migration utilities
- deployment helpers
- collectors

This works tactically but scales badly:

- root becomes a script graveyard
- ownership is unclear
- classes of operators blur
- compaction paths are absent

The system needs operator taxonomy the same way it needed artifact law.

---

## 1. Core Doctrine

Scripts are not miscellaneous utilities.

They are **operators** in the execution fabric.

Each operator should answer:

- what kind of operation it performs
- what authority it has
- what classes of files or state it may touch
- whether it stages, validates, reconciles, promotes, observes, enforces, or migrates

---

## 2. Primary Operator Classes

## 2.1 Stage

**Purpose**
- prepare work for another surface or downstream operator

**Examples**
- packet staging
- queue item creation
- workspace deployment preparation

**Typical behavior**
- writes new work artifacts
- does not finalize system truth by itself

## 2.2 Validate

**Purpose**
- check coherence, contract compliance, or structure

**Examples**
- config validation
- schema verification
- future artifact-law validation

**Typical behavior**
- read-heavy
- should fail fast
- should not silently mutate truth

## 2.3 Reconcile

**Purpose**
- transform operational returns into normalized repo truth

**Examples**
- event reconciliation
- runtime snapshot normalization
- finalizing Cowork returns

**Typical behavior**
- high-authority transformation
- writes durable truth surfaces

## 2.4 Promote

**Purpose**
- move material from one authority tier to a higher tier

**Examples**
- future research -> neocorpus promotion
- neocorpus -> canon promotion
- lineage -> playbook primitive promotion

**Typical behavior**
- most governance-sensitive operator class
- should usually require strong validation and review

## 2.5 Observe

**Purpose**
- collect runtime or environment facts without changing the world materially

**Examples**
- surface status collectors
- mini constellation status
- local runtime snapshot collectors

## 2.6 Enforce

**Purpose**
- block illegal state, sanitize, quarantine, or maintain invariant boundaries

**Examples**
- sanitizers
- future artifact-law validator
- future deprecation guardrails

## 2.7 Bridge

**Purpose**
- mediate between repo truth and external execution surfaces

**Examples**
- Manus, GitHub, YouTube, xAI, Google model, Cloudflare, channel bridges

**Typical behavior**
- surface-aware ingress/egress
- should respect exocortex capture policy

## 2.8 Bootstrap / Provision

**Purpose**
- bring execution substrate online

**Examples**
- machine bootstrap
- launchagent installation
- tmux/constellation stage scripts

## 2.9 Migration / Salvage

**Purpose**
- reshape shells, restore lineage, move old state into new structure

**Examples**
- nucleosynthesis undo tools
- future shell migration tools

---

## 3. Current Operator Inventory

## 3.1 Stage operators

- [render-configs.py](/Users/system/syncrescendence/render-configs.py)
- packet staging scripts under [CLI-WEB-GAP/scripts](/Users/system/syncrescendence/CLI-WEB-GAP/scripts)

## 3.2 Validate operators

- [validate-configs.py](/Users/system/syncrescendence/validate-configs.py)

## 3.3 Reconcile operators

- [reconcile-ajna-events.py](/Users/system/syncrescendence/reconcile-ajna-events.py)
- [finalize_cowork_relay_job.py](/Users/system/syncrescendence/finalize_cowork_relay_job.py)
- [sync-openclaw.py](/Users/system/syncrescendence/sync-openclaw.py)

## 3.4 Observe operators

- [collect-tooling-surface-status.py](/Users/system/syncrescendence/collect-tooling-surface-status.py)
- [collect-mini-constellation-status.py](/Users/system/syncrescendence/collect-mini-constellation-status.py)

## 3.5 Enforce / sanitize operators

- [sanitize-openclaw-events.py](/Users/system/syncrescendence/sanitize-openclaw-events.py)
- [normalize_event_ledger.py](/Users/system/syncrescendence/normalize_event_ledger.py)

## 3.6 Bridge operators

- [exocortex_event_bridge.py](/Users/system/syncrescendence/exocortex_event_bridge.py)
- [channel_surface_bridge.py](/Users/system/syncrescendence/channel_surface_bridge.py)
- [cloudflare_domain_bridge.py](/Users/system/syncrescendence/cloudflare_domain_bridge.py)
- [github_issue_bridge.py](/Users/system/syncrescendence/github_issue_bridge.py)
- [google_model_bridge.py](/Users/system/syncrescendence/google_model_bridge.py)
- [manus_checkpoint_bridge.py](/Users/system/syncrescendence/manus_checkpoint_bridge.py)
- [obsidian_repo_bridge.py](/Users/system/syncrescendence/obsidian_repo_bridge.py)
- [xai_model_bridge.py](/Users/system/syncrescendence/xai_model_bridge.py)
- [youtube_feed_bridge.py](/Users/system/syncrescendence/youtube_feed_bridge.py)

## 3.7 Bootstrap / provision operators

- [bootstrap-mac-mini.sh](/Users/system/syncrescendence/bootstrap-mac-mini.sh)
- [constellation-mini-stage1.sh](/Users/system/syncrescendence/constellation-mini-stage1.sh)
- [install-mini-constellation-launchagent.sh](/Users/system/syncrescendence/install-mini-constellation-launchagent.sh)
- [hydrate-openclaw-channels.py](/Users/system/syncrescendence/hydrate-openclaw-channels.py)

## 3.8 Migration / salvage operators

- [UNDO-NUCLEOSYNTHESIS.sh](/Users/system/syncrescendence/corpus/UNDO-NUCLEOSYNTHESIS.sh)
- [classifier.py](/Users/system/syncrescendence/corpus/classifier.py)
- [adjudicator_classifier.py](/Users/system/syncrescendence/corpus/adjudicator_classifier.py)
- [strip_filenames.py](/Users/system/syncrescendence/corpus/strip_filenames.py)

---

## 4. Placement Law

## 4.1 Root-shell rule

Only a narrow subset of operators should remain root-facing:

- build entrypoints
- core constitutional compilers/validators
- exceptionally central reconcilers or wrappers needed by existing integrations

Everything else should move into a dedicated operator lane in the next shell.

## 4.2 Target placement by class

### `operators/stage/`
- queue staging
- packet staging
- renderers

### `operators/validate/`
- structural validation
- policy validation
- schema checks

### `operators/reconcile/`
- finalizers
- runtime sync
- event normalization

### `operators/bridge/`
- surface-specific exocortex bridges

### `operators/observe/`
- status collectors
- runtime probes

### `operators/enforce/`
- sanitizers
- future quarantine/deprecation/artifact-law guards

### `operators/bootstrap/`
- machine provisioning
- launchagent installers
- constellation/bootstrap scripts

### `operators/migrate/`
- shell migration
- salvage
- CRUSH/nucleosynthesis helpers

---

## 5. Operator Metadata

Every mature operator should eventually declare:

- `operator_class`
- `authority_scope`
- `writes_to`
- `reads_from`
- `idempotency`
- `side_effect_level`
- `invocation_surface`

At minimum:

- whether it is safe to run repeatedly
- whether it mutates durable truth
- whether it touches external surfaces

---

## 6. Pain Points and Edge Cases

## 6.1 Wrapper vs real operator

A thin compatibility wrapper is not the real operator.
Example:
- a root wrapper preserved for Hazel compatibility may remain, but the real logic belongs in the operator lane.

## 6.2 Bridge vs reconcile

Bridges speak to external surfaces.
Reconcilers turn returns into truth.
These are not the same thing and should remain separate when possible.

## 6.3 Observe vs enforce

Collectors should not silently sanitize or mutate unless explicitly designated to do so.

## 6.4 Migration tools

Migration operators are dangerous by nature and should be visibly classified as such.

## 6.5 Script compaction

Repeated manual operational sequences should eventually compact into operators.
Repeated operator sequences should eventually compact into playbook recipes, hooks, or automations.

---

## 7. Alignment with Harness Research

The harness/context-engineering research implies:

- systems become reliable when the scaffolding is explicit
- prompt engineering alone is not enough
- operational behavior must compile down into repeatable mechanisms

Operators are part of that compiled scaffolding.

They are the concrete mechanisms by which:

- constitutional rules become executable
- runtime state becomes durable
- exocortex returns become normalized
- compaction becomes mechanized

---

## 8. Net Rule

The next shell should make it obvious, for every operator:

- what class it is,
- where it belongs,
- what truth surfaces it can mutate,
- and whether it stages, validates, reconciles, bridges, observes, enforces, bootstraps, or migrates.

If a script is merely "some python file at repo root," the shell is still underdesigned.
