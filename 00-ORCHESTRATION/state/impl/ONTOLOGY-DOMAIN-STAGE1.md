# Ontology Domain Stage 1

**Date**: 2026-03-02  
**Purpose**: First domain-facing deployment shape for `syncrescendence.com`

## Current Status

As of **March 2, 2026**, the Stage 1 domain path is effectively live at Cloudflare edge, but this macOS host still has a stale default resolver path.

Current state:

- local ontology API is healthy on `127.0.0.1:8787`
- local reverse proxy is healthy on `http://localhost:8080/health`
- `dig` resolves `syncrescendence.com` to Cloudflare edge IPs
- direct edge health checks succeed for `https://syncrescendence.com/health`
- default `curl https://syncrescendence.com/health` on this machine may still fail until the local resolver catches up
- repo-safe readiness checks are written by `make tooling-surface-status`

## Role

Stage 1 keeps the domain narrow:

- `syncrescendence.com` serves the ontology API first
- the API is a thin reverse proxy to local FastAPI on `127.0.0.1:8787`
- dashboards or docs are downstream and should not become a second truth surface yet
- `cloudflared` is the preferred cutover path if direct inbound edge routing is not yet in place

## Shape

- local service: `ontology_v1.py serve --host 127.0.0.1 --port 8787`
- reverse proxy: Caddy or equivalent
- public contract:
  - `GET /health`
  - `GET /entities`
  - `GET /entities/{id}`
  - `GET /events`
  - `POST /ingest/event`
  - `POST /project/repo`

## Why This Stage

This preserves the ratified boundary contract:

- repo remains authority
- ontology remains projection
- domain remains typed query surface only

It avoids premature UI drift while still making the ontology reachable.

## Deployment Sequence

1. Start ontology locally with:

```bash
/Users/system/.venvs/syncrescendence-ontology/bin/python /Users/system/syncrescendence/ontology_v1.py serve --host 127.0.0.1 --port 8787
```

2. Put a reverse proxy in front of it using the example Caddyfile in this folder.

Alternative edge path:

- use `cloudflared` with `CLOUDFLARED-ONTOLOGY-STAGE1.md`
- route `syncrescendence.com` and `www.syncrescendence.com` to the local Caddy proxy on `127.0.0.1:8080`

3. Refresh the local readiness artifact:

```bash
make tooling-surface-status
```

4. Confirm:

```bash
make ontology-domain-health-edge
```

If the machine resolver has caught up, this should also pass:

```bash
make ontology-domain-health
```

5. Only after stable edge health:
   - point selected automation/event projectors at the domain URL instead of localhost
   - use `make reconcile-ajna-events-project-domain`

## Non-Goals For Stage 1

- no dashboard
- no docs site
- no write path outside the existing ingestion contract
- no direct SaaS webhooks bypassing repo/event reconciliation
