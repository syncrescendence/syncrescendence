# Ontology Domain Stage 1

**Date**: 2026-03-02  
**Purpose**: First domain-facing deployment shape for `syncrescendence.com`

## Role

Stage 1 keeps the domain narrow:

- `syncrescendence.com` serves the ontology API first
- the API is a thin reverse proxy to local FastAPI on `127.0.0.1:8787`
- dashboards or docs are downstream and should not become a second truth surface yet

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

3. Confirm:

```bash
curl https://syncrescendence.com/health
```

4. Only after stable health:
   - point selected automation/event projectors at the domain URL instead of localhost

## Non-Goals For Stage 1

- no dashboard
- no docs site
- no write path outside the existing ingestion contract
- no direct SaaS webhooks bypassing repo/event reconciliation
