# LOG-CC83 dev webshell stage0

## Objective

Stand up a minimal development website surface that connects repo state, exocortex migration state, ontology health, and callback ingress without expanding into product scope.

## Landed artifacts

- webshell operator:
  - [syncrescendence_dev_shell.py](/Users/system/syncrescendence/operators/webshell/syncrescendence_dev_shell.py)
- webshell runbook:
  - [operators/webshell/README.md](/Users/system/syncrescendence/operators/webshell/README.md)
- stage0 doctrine:
  - [WEBSHELL-STAGE0-CC83.md](/Users/system/syncrescendence/orchestration/state/impl/WEBSHELL-STAGE0-CC83.md)
- caddy gateway example:
  - [dev-webshell.Caddyfile.example](/Users/system/syncrescendence/orchestration/state/impl/dev-webshell.Caddyfile.example)
- runtime lane for callback intake:
  - [runtime/webshell/README.md](/Users/system/syncrescendence/runtime/webshell/README.md)
  - [runtime/webshell/callbacks/inbox/README.md](/Users/system/syncrescendence/runtime/webshell/callbacks/inbox/README.md)
  - [runtime/webshell/callbacks/inbox/.gitignore](/Users/system/syncrescendence/runtime/webshell/callbacks/inbox/.gitignore)
- make targets:
  - [Makefile](/Users/system/syncrescendence/Makefile)
    - `webshell-dev`
    - `webshell-smoke`

## Implemented route contract

1. `GET /health`
2. `GET /status`
3. `GET /docs`
4. `GET /ontology`
5. `GET /artifacts/<path>` (allowlisted read-only)
6. `POST /callbacks/<surface>` where surface is one of:
   - `github`
   - `slack`
   - `discord`
   - `cloudflare`
   - `generic`

## Callback ingestion behavior

Every callback POST writes:

1. raw callback artifact to:
   - `runtime/webshell/callbacks/inbox/`
2. commander wake task to:
   - `offices/commander/inbox/pending/`

This preserves office-law routing and wake-on-inbox semantics.

## Verification

1. `python3 -m py_compile operators/webshell/syncrescendence_dev_shell.py`
2. launched webshell on `127.0.0.1:8892`
3. `make webshell-smoke PORT=8892` passed
4. callback POST smoke verified task + raw payload creation, then smoke artifacts were removed

## Security boundary

1. local loopback bind by default
2. optional callback token gate via `--callback-token` + `X-Sync-Token`
3. no keychain export, no broad secret delegation
4. artifact serving constrained to allowlisted repo prefixes

## Manus follow-up dispatch

- prompt:
  - [PACKET-MANUS-cc83-account-topology-and-cutover.md](/Users/system/syncrescendence/communications/prompts/PACKET-MANUS-cc83-account-topology-and-cutover.md)
- task id:
  - `kD8SxUjH6FyVv7hYFNQVT4`
- task url:
  - [manus task](https://manus.im/app/kD8SxUjH6FyVv7hYFNQVT4)
- response target:
  - [RESPONSE-MANUS-cc83-account-topology-and-cutover.md](/Users/system/syncrescendence/communications/responses/RESPONSE-MANUS-cc83-account-topology-and-cutover.md)
- task status:
  - `completed`
- landed raw artifact:
  - [RESPONSE-MANUS-cc83-account-topology-and-cutover-raw.md](/Users/system/syncrescendence/communications/responses/RESPONSE-MANUS-cc83-account-topology-and-cutover-raw.md)

## Account topology decision landing

- [ACCOUNT-TOPOLOGY-DECISION-CC83.md](/Users/system/syncrescendence/orchestration/state/impl/ACCOUNT-TOPOLOGY-DECISION-CC83.md)
