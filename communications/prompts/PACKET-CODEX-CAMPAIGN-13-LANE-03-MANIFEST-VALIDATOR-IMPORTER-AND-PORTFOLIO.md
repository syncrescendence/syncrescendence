# Packet — Codex Campaign 13 Lane 03 — Manifest Validator, Importer, And Portfolio

**Reasoning level**: `extra high`

Direct-write the first executable inbound manifest spine.

Write or patch:

1. `/Users/system/syncrescendence/operators/validators/validate_inbound_feed_manifest.py`
2. `/Users/system/syncrescendence/operators/acumen/import_inbound_feed_manifests.py`
3. `/Users/system/syncrescendence/orchestration/state/ACUMEN-INBOUND-FEED-PORTFOLIO.json`
4. `/Users/system/syncrescendence/orchestration/state/ACUMEN-INBOUND-FEED-PORTFOLIO.md`
5. `/Users/system/syncrescendence/runtime/acumen/inbound-feed-import-seed.json`
6. add any minimal `Makefile` targets needed

Requirements:

1. Validation must fail on identity ambiguity, broken raw-capture lineage, duplicate entries within a manifest, and missing stable identifiers where required.
2. Importer must emit:
   - full inbound portfolio preview
   - match-state categories such as `registry_ready`, `portfolio_only`, `blocked_identity`, `ambiguous_target`, `unresolved_platform_id`
   - registry-ready seed rows only for current-registry-compatible entries
3. Do not create a second intake authority.
4. Reuse current Acumen registry merge/validation logic rather than replacing it.

Write your receipt:

- `/Users/system/syncrescendence/communications/responses/RESPONSE-CODEX-CAMPAIGN-13-LANE-03-MANIFEST-VALIDATOR-IMPORTER-AND-PORTFOLIO.md`

Run `git diff --check`.
