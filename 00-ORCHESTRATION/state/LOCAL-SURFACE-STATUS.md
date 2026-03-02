# Local Surface Status

**Captured**: 2026-03-02T04:49:24Z

## Auth Surfaces

- `gcloud` authenticated: `True`
- `gcloud` active account: `icloud.truongphillipthanh@gmail.com`
- `gcloud` keychain pointer present: `True`
- `wrangler` authenticated: `True`
- `wrangler` email: `icloud.truongphillipthanh@gmail.com`
- `wrangler` account id: `b76f644c19db95eb0dfc2b6db1e7186d`
- Cloudflare account-id keychain pointer present: `True`
- Manus keychain pointer present: `True`
- Manus API reachable: `True`

## Ontology Domain Readiness

- Local API reachable: `True`
- Local proxy reachable: `True`
- macOS resolver sees domain: `False`
- `dig` sees public records: `True`
- Direct public edge health reachable: `True`
- Default local domain health reachable: `False`

## Tunnel

- `cloudflared` installed: `True`
- Cloudflare tunnel cert present: `True`
- Local tunnel config present: `True`
- Named tunnel present: `True`
- Tunnel LaunchAgent loaded: `True`
- Tunnel LaunchAgent state: `active`

## Reading

- Local auth and serving surfaces can be checked without exposing secrets in repo artifacts.
- If `dig` and direct edge health are green while default local curl still fails, the public cutover is live and only the local resolver is stale.
- CLI and Keychain status should remain pointer-only; credentials stay local.
