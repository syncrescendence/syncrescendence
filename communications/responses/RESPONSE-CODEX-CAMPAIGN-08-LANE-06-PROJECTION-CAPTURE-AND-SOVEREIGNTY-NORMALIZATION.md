# Response

**Response ID**: `RSP-20260310-codex-campaign-08-lane-06-projection-capture-and-sovereignty-normalization`
**Surface**: `codex_parallel_session`
**Date received**: `2026-03-10`
**Dispatch packet**: `communications/prompts/PACKET-CODEX-CAMPAIGN-08-LANE-06-PROJECTION-CAPTURE-AND-SOVEREIGNTY-NORMALIZATION.md`
**Result state**: `complete`
**Receipt artifacts**:
  - `orchestration/state/impl/PROJECTION-FAMILY-SOVEREIGNTY-NORMALIZATION-v1.md`
  - `orchestration/state/impl/OFFICE-HARNESS-EXOCORTEX-PROJECTION-CONTRACT-v1.md`
  - `operators/exocortex/office_harness_projection_bridge.py`
  - `operators/validators/validate_config_surface_state.py`
  - `orchestration/state/registry/CHAT-CI-PROVIDER-PROFILES-v1.json`
  - `orchestration/state/registry/CHAT-CI-PROJECTION-PACK-v1.json`
  - `orchestration/state/impl/CONFIG-SURFACE-CHAT-CI-WIDENING-CONTRACT-v1.md`
  - `orchestration/state/impl/CHAT-CI-MANUAL-EXPORT-READINESS-CONTRACT-v1.md`
  - `operators/validators/validate_chat_ci_manual_export_readiness.py`
  - `orchestration/state/registry/CHAT-CI-MANUAL-EXPORT-READINESS-v1.json`

## Returned Content

Normalized derivative projection sovereignty around one shared rule:

- repo ratifies
- exocortex coordinates only where a family contract permits it
- projection artifacts derive and remain replaceable

That shared rule now lives at:

- `orchestration/state/impl/PROJECTION-FAMILY-SOVEREIGNTY-NORMALIZATION-v1.md`

What changed:

- added a common `projection_governance` envelope with explicit `capture_policy`, `reliance_ceiling`, and hidden-second-control-plane prohibition
- bound the office-harness exocortex projection contract, builder, emitted artifact, and report checks to that envelope
- normalized the repo-native `chat_ci` provider-profile and projection-pack surfaces to the same sovereignty rule with `manual_export_only` capture posture
- extended the existing config-surface validator so the landed `chat_ci` derivative artifacts must keep that governance envelope and manual-export-only behavior
- normalized the adjacent `chat_ci` widening and manual-export-readiness family surfaces already present in the worktree so they inherit the same contract rather than opening a second dialect

Net effect:

- projection families now declare one coherent capture posture instead of relying on scattered authority statements
- office-harness keeps row-scoped operative reliance under contract-bound repo joins
- `chat_ci` widening remains informative-only until receipted export, manual-only, and explicitly non-automated
- repo ratification, exocortex coordination, and projection artifacts stay distinct

## Verification

- ran `python3 operators/exocortex/office_harness_projection_bridge.py`
- ran `python3 operators/validators/validate_config_surface_state.py`
- ran `python3 operators/validators/validate_chat_ci_manual_export_readiness.py`
- ran `git diff --check`
- result: clean

## Status

`complete`
