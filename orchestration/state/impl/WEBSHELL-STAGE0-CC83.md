# Webshell Stage0 — CC83

**Date**: 2026-03-04  
**Status**: active  
**Class**: operational thin-shell

## Purpose

Stand up a minimal website surface for development that connects:

1. repo truth
2. exocortex migration state
3. ontology health
4. callback ingress into office workflow

without expanding into product-site scope.

## Implemented Surface

Operator:

- [syncrescendence_dev_shell.py](/Users/system/syncrescendence/operators/webshell/syncrescendence_dev_shell.py)

Runbook:

- [operators/webshell/README.md](/Users/system/syncrescendence/operators/webshell/README.md)

Make targets:

- `make webshell-dev`
- `make webshell-smoke PORT=8890`
- `make webshell-callback-smoke PORT=8890 CALLBACK_TOKEN=...`

## Route Contract

1. `GET /health`: service heartbeat
2. `GET /status`: reads tracker + ledger + local-surface snapshot
3. `GET /docs`: webshell route index
4. `GET /ontology`: local snapshot + live health probe to ontology domain
5. `GET /artifacts/<path>`: read-only artifact serving from allowed repo prefixes
6. `POST /callbacks/<surface>`: callback capture and office task issuance

## Callback Ingress Contract

A callback POST writes:

1. raw payload artifact:
   - `runtime/webshell/callbacks/inbox/CALLBACK-...json`
2. commander task envelope:
   - `offices/commander/inbox/pending/TASK-callback-...md`

This keeps web ingress aligned with office law and wake-on-inbox.

## Security Boundary

1. Default bind is loopback (`127.0.0.1`).
2. Callback POST ingestion is disabled unless `--callback-token` is configured.
3. When configured, callback POST requires `X-Sync-Token`.
4. Artifact serving is prefix-restricted and repo-root constrained.
5. Secrets remain local; no keychain export or remote broad-secret handoff.

## What Stage0 Is Not

1. Not a public product site.
2. Not an auth system.
3. Not a general webhook platform exposed to the open internet.
4. Not a replacement for exocortex bridge operators.

## Next Natural Move

When ready for controlled external callbacks:

1. keep webshell local-only
2. terminate at Cloudflare/Caddy with explicit path routing (`/ops/*`)
3. enforce token/signature verification per provider
4. map each callback to a dedicated bridge operator before auto-promotion
