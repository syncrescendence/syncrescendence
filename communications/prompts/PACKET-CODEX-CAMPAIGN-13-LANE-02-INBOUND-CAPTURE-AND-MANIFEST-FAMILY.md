# Packet — Codex Campaign 13 Lane 02 — Inbound Capture And Manifest Family

**Reasoning level**: `extra high`

Direct-write the repo-local law for feed capture before mutation.

Write or patch:

1. `/Users/system/syncrescendence/orchestration/state/impl/ACUMEN-INBOUND-FEED-CAPTURE-AND-IMPORT-CONTRACT-v1.md`
2. `/Users/system/syncrescendence/runtime/acumen/inbound-feed-manifests/README.md`
3. `/Users/system/syncrescendence/runtime/acumen/README.md` and `/Users/system/syncrescendence/operators/acumen/README.md` only if necessary

Requirements:

1. Preserve the chain: `browser/session recon -> raw capture witness -> normalized manifest -> validation -> inbound portfolio -> registry-ready seed`.
2. Stop on identity ambiguity.
3. Preserve raw captures through existing feedstock witness lanes rather than inventing a new authority surface.
4. Keep non-YouTube captures portfolio-visible but registry-deferred until matching workers exist.
5. Keep outbound follow/subscription mutation out of scope.

Write your receipt:

- `/Users/system/syncrescendence/communications/responses/RESPONSE-CODEX-CAMPAIGN-13-LANE-02-INBOUND-CAPTURE-AND-MANIFEST-FAMILY.md`

Run `git diff --check`.
