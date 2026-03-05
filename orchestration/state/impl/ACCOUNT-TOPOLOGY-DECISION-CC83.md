# Account Topology Decision — CC83

**Date**: 2026-03-04  
**Status**: active  
**Class**: decision note

## Decision

Use a split-control model instead of forcing all paid subscriptions into `syncrescendence@gmail.com` immediately.

## Canonical roles

1. `syncrescendence@gmail.com`
   - organization control-plane owner
   - platform ownership target for GitHub/Slack/Discord/Cloudflare/exocortex workspaces
2. `icloud.truongphillipthanh@gmail.com` (Account 2)
   - paid-subscription and billing anchor for non-transferable or benefit-constrained plans
   - keep Google AI Pro student-linked benefits here until natural expiration or eligibility change
3. `truongphillipthanh@icloud.com` (Account 1)
   - temporary break-glass only
   - reduce to minimal emergency privilege after cutover stabilization
4. `truongphillipthanh@gmail.com` (Account 3)
   - optional personal secondary user account; not a control-plane owner

## Why this model

1. Preserves current paid-benefit constraints on Account 2.
2. Avoids forced subscription churn while critical ownership migration is in flight.
3. Keeps operational authority clear by moving platform ownership to `syncrescendence@gmail.com`.
4. Maintains recoverability with Account 1 until all waves are verified.

## Conflict note (Manus CC83)

The returned Manus CC83 raw runbook suggests broader subscription migration toward `syncrescendence@gmail.com`.
That is useful as a long-term direction but should be gated by current paid-plan constraints.

Reference:

- [RESPONSE-MANUS-cc83-account-topology-and-cutover-raw.md](/Users/system/syncrescendence/communications/responses/RESPONSE-MANUS-cc83-account-topology-and-cutover-raw.md)

## Execution rule

In the current cutover window:

1. migrate ownership and admin control first
2. keep constrained paid subscriptions where benefits currently exist
3. schedule subscription unification only after control-plane stabilization and cost/benefit validation
