# Response

**Response ID**: `RSP-20260313-codex-campaign-12-lane-04-feed-recon-capture-and-import-path`  
**Surface**: `codex_parallel_session`  
**Date received**: `2026-03-13`  
**Dispatch packet**: `communications/prompts/PACKET-CODEX-CAMPAIGN-12-LANE-04-FEED-RECON-CAPTURE-AND-IMPORT-PATH.md`  
**Result state**: `complete`  
**Receipt artifact**: `communications/responses/RESPONSE-CODEX-CAMPAIGN-12-LANE-04-FEED-RECON-CAPTURE-AND-IMPORT-PATH.md`

## Returned Content

The lawful path is:

`browser/session recon -> raw source capture preserved -> normalized manifest pair -> ambiguity/parity gate -> inbound portfolio import -> registry merge only for registry-ready rows -> normal Acumen poll/triage`

That keeps the feed-recon canon intact in repo terms:

1. capture happens before mutation
2. account ambiguity blocks the run
3. source-of-truth manifests stay preserved as their own witnesses
4. Acumen remains the only active intake plane
5. outbound subscription mutation is out of scope for this path

One important repo-truth constraint changes the implementation shape:

- the current active Acumen intake registry at `runtime/acumen/registry.json` is YouTube-channel-oriented
- therefore not every captured subscription manifest can go straight into the live registry
- all captured manifests should first land in an Acumen-facing inbound portfolio surface
- only rows that resolve lawfully to current registry requirements should merge into `runtime/acumen/registry.json`

That means YouTube captures can become live registry rows when they resolve to stable channel identity.
X or other platform captures remain portfolio-visible but registry-deferred until a matching intake worker and contract exist.

## 1. The Direct-Write Set

1. Create `orchestration/state/impl/ACUMEN-INBOUND-FEED-CAPTURE-AND-IMPORT-CONTRACT-v1.md`
   This should ratify the repo-side doctrine for:
   `capture-before-mutation`, `stop-on-identity-ambiguity`, `preserve-source-manifests`, `portfolio-before-registry`, and `no-outbound-mutation-in-this-path`.
   It should also state explicitly that chain-account browser capture is upstream reconnaissance, not a replacement for the current canonical Acumen runtime identity bound to `syncrescendence@gmail.com`.

2. Reuse the existing raw-source preservation lane instead of inventing a new one.
   Original browser exports, copied page data, or operator-produced CSV/JSON/HTML captures should be staged through:
   - `knowledge/feedstock/inbox/`
   - `knowledge/feedstock/receipts/`
   That gives the source-of-truth capture a preserved witness before any normalization or merge.

3. Create `runtime/acumen/inbound-feed-manifests/README.md` and the normalized manifest family under that directory.
   Use one preserved manifest pair per account/platform/capture run:
   - `YYYYMMDD-<account>-<platform>-subscriptions-source.json`
   - `YYYYMMDD-<account>-<platform>-subscriptions-source.md`
   Minimum JSON fields should include:
   - `manifest_id`
   - `capture_account`
   - `claimed_chain`
   - `platform`
   - `capture_started_at`
   - `capture_completed_at`
   - `identity_status`
   - `identity_evidence`
   - `ambiguity_status`
   - `entry_count`
   - `entries`
   - `raw_capture_refs`
   - `notes`
   The markdown companion should summarize counts, capture method, caveats, unresolved ambiguity, and import eligibility.

4. Create `operators/validators/validate_inbound_feed_manifest.py`
   This validator should fail when:
   - `identity_status` is not confirmed
   - `ambiguity_status` is not none
   - stable identifiers are missing where required
   - duplicate entries survive dedupe rules inside one manifest
   - referenced raw capture artifacts or receipts are missing

5. Create `operators/acumen/import_inbound_feed_manifests.py`
   This should consume validated source manifests and emit three derivative outputs:
   - `orchestration/state/ACUMEN-INBOUND-FEED-PORTFOLIO.json`
   - `orchestration/state/ACUMEN-INBOUND-FEED-PORTFOLIO.md`
   - `runtime/acumen/inbound-feed-import-seed.json`
   The portfolio surfaces are for all captured feeds across platforms.
   The seed JSON is only for rows that are registry-admissible under the current Acumen contract.

6. Reuse the existing Acumen registry builder and validator rather than inventing a second registry authority.
   The import operator should prepare seed rows compatible with:
   - `operators/acumen/init_registry.py`
   - `operators/acumen/validate_registry.py`
   Then merge by:
   - `python3 operators/acumen/init_registry.py --seed runtime/acumen/inbound-feed-import-seed.json --output runtime/acumen/registry.json --merge`
   followed by strict validation.

7. Patch `runtime/acumen/README.md` and `operators/acumen/README.md`
   Document the new inbound capture family, the import preview/portfolio outputs, and the rule that only registry-ready YouTube rows can currently become live Acumen intake entries.

## 2. The Capture / Import Chain

1. Verify browser/session identity before any list capture.
   Use one dedicated browser profile or session container per account/platform pair where possible.
   If the active account cannot be confirmed, stop immediately and mark the manifest run blocked.

2. Preserve the raw source-of-truth capture before normalization.
   Save the original export, copied table, page dump, or browser-produced artifact into `knowledge/feedstock/inbox/` and write the staging receipt into `knowledge/feedstock/receipts/`.
   This is the pre-mutation witness.

3. Normalize the capture into one manifest pair in `runtime/acumen/inbound-feed-manifests/`.
   Keep the original per-account/per-platform boundary intact.
   Do not merge multiple accounts or multiple platforms into one source manifest.

4. Validate the manifest and stop on ambiguity.
   Identity ambiguity, missing stable identifiers, or broken raw-capture lineage should fail here.
   This is the repo translation of the canon rule: recon is lawful only when the active account is known.

5. Import validated manifests into the Acumen inbound portfolio surface.
   `operators/acumen/import_inbound_feed_manifests.py` should build:
   - a full portfolio view of captured feeds
   - parity and duplicate checks against prior imports
   - match-state categories such as `registry_ready`, `portfolio_only`, `blocked_identity`, `ambiguous_target`, or `unresolved_platform_id`

6. Emit registry seed rows only for current-registry-compatible entries.
   Under the current repo truth, that mainly means YouTube subscriptions that can be resolved to stable `channel_id` plus a lawful `name`.
   The importer can let `registry_contract.default_channel()` fill the current default fields after the identity-bearing minimums are present.

7. Merge seed rows into `runtime/acumen/registry.json` only after the preview is clean.
   Use the existing merge path in `init_registry.py`, then run `validate_registry.py --strict`.
   If strict validation fails, the import is not complete and the portfolio surface remains the authoritative import preview.

8. Only after registry validation passes should normal Acumen intake consume the new rows.
   The downstream path remains unchanged:
   `registry -> poll_youtube_registry.py -> run_triage.py -> product / verification / assessment`

9. Do not perform outbound follow/subscribe mutation from this path.
   This lane is inbound repo capture and import only.
   It is not the canon's earlier transfer or parity-mutation procedure rewritten under a new name.

## 3. What Still Remains Manual Or Browser-Bound

1. Logged-in capture of subscription/following surfaces.
   The repo can validate and import manifests, but it does not itself hold the browser sessions for the five chain accounts.

2. Identity confirmation on the live platform surface.
   Shared-session confusion, silent account switching, and multi-login ambiguity still require browser-visible verification before capture.

3. Full-list extraction from lazy-loaded subscription pages.
   Infinite scroll, partial management views, rate limits, and anti-bot friction remain browser-work problems even if later normalized automatically.

4. Resolution of missing or ambiguous stable identifiers.
   If a captured row has only a display name and no trustworthy channel URL, handle, or platform ID, it should stay blocked or portfolio-only until resolved.

5. Human adjudication of chain fit when the platform subscription itself is not enough.
   A subscription can be real and still be a poor active Acumen intake candidate.
   Lane 05 policy should govern widening, but the first import path still needs a human review step for edge cases.

6. Any future outbound synchronization back to platform accounts.
   Subscribe/unsubscribe parity work, cleanup, and migration actions are outside this inbound path and should remain separately governed.

## 4. Bottom Line

The lawful repo translation of the feed-recon canon is not:

`browser capture -> direct registry mutation`

It is:

`browser capture -> preserved source manifest -> validated normalized manifest -> inbound portfolio preview -> registry merge only for resolved, registry-ready rows`

That is the right shape for the current shell because it preserves the original captures, blocks on identity ambiguity, respects the existing Acumen YouTube intake contract, and avoids creating a hidden second intake authority while broader curated-feed policy is still being formalized.

## 5. Status

`complete`
