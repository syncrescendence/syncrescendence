# Response

## Overall verdict

Campaign 03 should proceed as a law-first, validator-second, registry-last program.

The lanes agree that the shell is not missing macro doctrine. It is missing the typed middle layer that turns existing doctrine into lawful config sources, office-to-harness bindings, and generalized ledger contracts without copying vendor text downward or mutating live authority surfaces too early.

## What should be ratified immediately

1. `knowledge/sigma/CONFIG-SOURCE-OF-TRUTH-ARCHITECTURE-v1.md`
2. `knowledge/sigma/CONFIG-BEHAVIOR-ATOMS-AND-SURFACE-PROFILES-v1.md`
3. `orchestration/state/impl/OFFICE-HARNESS-BINDING-CONTRACT-v1.md`
4. `orchestration/state/impl/LIVE-LEDGER-FAMILY-CONTRACT-v1.md`
5. `orchestration/state/impl/RATIFICATION-POINTER-ROLLOUT-v1.md`

These five artifacts resolve the common drift points across all lanes:

- one constitutional config kernel
- one durable atom and surface-profile layer
- one office-binding law
- one generic ledger family law
- one non-breaking ratification-pointer transition order

## What should remain design-only

- `CLI-CONFIG-DISTILLATION-LAW-v1.md` and `CONFIG-PROJECTION-MATRIX-v1.md` as separate first-pass artifacts. Their substance should be folded into the two Sigma docs before any additional doctrine family is created.
- `orchestration/state/registry/config-surface-schema-v1.md`, `config-surface-registry.csv`, and `config-projection-ledger.jsonl` until the config kernel is ratified.
- `orchestration/state/registry/office-harness-bindings.effective.json` and `office-harness-binding-ledger.jsonl` until per-office metadata exists and the office validator is running.
- `LIVE-LEDGER-FRESHNESS-AND-DECAY-CONTRACT-v1.md`, `LIVE-LEDGER-ROLLOUT-GATES-v1.md`, `LIVE-LEDGER-VALIDATOR-SPEC-v1.md`, `live-ledger-family-schema-v1.md`, `live-ledger-domain-register.csv`, and `SEVEN-LEDGER-MANIFEST-v1.md` until the family contract is landed and one additional ledger family is selected.
- Any tributary `v2` header change or inline ratification-pointer column expansion until schema-law transition and dual-mode validator support are in place.
- Dashboard, ontology, and broad renderer expansion until report-only validator proofs are clean.

## Exact next direct-write batch

1. `knowledge/sigma/CONFIG-SOURCE-OF-TRUTH-ARCHITECTURE-v1.md`
2. `knowledge/sigma/CONFIG-BEHAVIOR-ATOMS-AND-SURFACE-PROFILES-v1.md`
3. `orchestration/state/impl/OFFICE-HARNESS-BINDING-CONTRACT-v1.md`
4. `orchestration/state/impl/LIVE-LEDGER-FAMILY-CONTRACT-v1.md`
5. `orchestration/state/impl/RATIFICATION-POINTER-ROLLOUT-v1.md`
6. `offices/commander/platform/contracts/OFFICE-HARNESS-METADATA.v1.yaml`

This is the smallest direct-write batch that creates actual law plus one typed specimen.

`commander` should be the first specimen because its binding to `claude_code` is the least ambiguous current office-harness pair and gives the cleanest validator fixture before the OpenClaw-specific runtime facts are introduced.

## Smallest safe sequencing that preserves momentum without reintroducing drift

1. Land the five law artifacts above and the single `commander` metadata specimen.
2. Add `operators/validators/validate_office_harness_coherence.py` in report-only mode, then write `ajna`, `psyche`, `adjudicator`, and `cartographer` metadata files.
3. Amend `orchestration/state/registry/tributary-disposition-schema-v1.md` to ratify the temporary `v1` compatibility rule, then update `operators/validators/validate_tributary_disposition.py` so rows are classified as `authority_bound` or `informative_only`. Do not change the live CSV header yet.
4. After both validators produce clean report-only proofs, write `orchestration/state/registry/office-harness-bindings.effective.json`, `office-harness-binding-ledger.jsonl`, the coherence reports, and the config-surface schema/registry/ledger trio.
5. Only then widen renderer scope, ledger-family adjunct contracts, shared domain registers, dashboards, ontology projections, and any tributary `v2` inline-pointer migration.

This order preserves momentum because it ratifies the missing middle layer first, proves one concrete office contract immediately, and keeps live control-plane surfaces compatibility-safe until validators are ready to carry the change.
