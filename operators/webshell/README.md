# Dev Webshell

Thin operational website shell for development.

This is intentionally not product UI. It is a control surface for:

1. live status projection from repo artifacts
2. read-only artifact browsing
3. ontology health visibility
4. callback ingestion into commander inbox

## Run

```bash
python3 operators/webshell/syncrescendence_dev_shell.py --repo-root /Users/system/syncrescendence --host 127.0.0.1 --port 8890
```

To enable callback POST intake, you must set a token:

```bash
python3 operators/webshell/syncrescendence_dev_shell.py \
  --repo-root /Users/system/syncrescendence \
  --host 127.0.0.1 \
  --port 8890 \
  --callback-token "set-a-strong-random-token"
```

## Routes

- `GET /health`
- `GET /status`
- `GET /docs`
- `GET /ontology`
- `GET /artifacts/<repo-relative-path>`
- `POST /callbacks/<surface>` where `<surface>` is:
  - `github`
  - `slack`
  - `discord`
  - `cloudflare`
  - `generic`

## Callback behavior

Each callback POST creates:

1. raw callback artifact in:
   - `runtime/webshell/callbacks/inbox/`
2. commander task envelope in:
   - `offices/commander/inbox/pending/`

This keeps web ingress aligned with office law and wake-on-inbox semantics.

## Security notes

1. Default bind is local loopback (`127.0.0.1`).
2. Callback POST ingestion is disabled unless `--callback-token` is set.
3. When token is set, callback POST requires `X-Sync-Token`.
4. Secrets should not be included in callback payloads.
