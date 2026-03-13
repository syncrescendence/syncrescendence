# DISPATCH-AJNA-cc94-feed-recon-migration

**Surface**: `ajna_openclaw_browser_runtime`  
**Packet type**: `feed_recon_migration_dispatch`  
**Purpose**: execute X + YouTube follow/subscription reconnaissance and migration across Accounts 1, 2, and 3 without prematurely destroying the current source feed.

## Live Browser Context

- Designated browser surface is `Vivaldi`.
- Required OpenClaw browser profile is `vivaldi`.
- The human has already logged into the relevant accounts in that browser.
- `X` has three logged-in accounts available through the profile/account switcher.
- `YouTube` has two logged-in accounts available through the profile/account switcher.
- Do not assume separate browser profiles exist for each account during this run.
- Because account switching is taking place inside the same live browser surface, explicit identity verification is mandatory before every capture or mutation step.
- No OpenClaw node is paired for this machine. Do not attempt to use `nodes`; execute directly through the local browser/runtime surface.

## Canonical Protocol

Execute exactly:

- `/Users/system/Desktop/canon/CANON-25230-FEED_RECON_MIGRATION-satellite-CONSTELLATION_ARCH-lattice.md`

Use supporting context as needed:

- `/Users/system/Desktop/canon/CANON-25220-ACCOUNT_FEED_ARCH-satellite-CONSTELLATION_ARCH-lattice.md`
- `/Users/system/Desktop/canon/CANON-31142-PLATFORM_GRAMMAR-satellite-IIC-lunar-ACUMEN-planetary-INFORMATION.md`
- `/Users/system/Desktop/canon/CANON-31143-FEED_CURATION-satellite-IIC-lunar-ACUMEN-planetary-INFORMATION.md`

## Scope

- **Account 1**: X current follows capture only
- **Account 2**: capture current X follows + current YouTube subscriptions before mutation
- **Account 3**: treat X follows + YouTube subscriptions as source-of-truth graph
- **Transfer**: clone the missing Account 3 X and YouTube graph into Account 2
- **Stop condition**: do not begin Account 3 cleanup or pivot after parity; return results only

## Output Artifacts

1. Human-readable result:
   - `/Users/system/syncrescendence/communications/responses/RESPONSE-AJNA-cc94-feed-recon-migration.md`
2. Working manifests directory:
   - `/Users/system/Desktop/canon/feed-recon/2026-03-13-account-migration/`

## Required Summary Verdict

Return one of:

- `READY FOR ACCOUNT 3 PIVOT PLANNING`
- `NOT READY FOR ACCOUNT 3 PIVOT`

## Constraints

1. No Account 3 pruning or unsubscribing in this run.
2. No Account 2 unfollows in this run.
3. Before each capture or transfer step, verify the active account from visible UI identity markers after switching via the account/profile icon.
4. If session ambiguity or missing login blocks execution, document exact blockage and stop safely.
5. Preserve evidence of counts, deltas, and unresolved failures.
