# Local Surface Status

**Captured**: 2026-03-02T05:40:41Z

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

## OpenClaw Channels

- `slack` running: `True`
- `slack` probe ok: `True`
- `slack` last inbound observed: `None`
- `slack` last outbound observed: `None`
- `slack` workspace: `Syncrescendence` (`T0AB6TCRZGF`)
- `discord` running: `True`
- `discord` probe ok: `True`
- `discord` last inbound observed: `None`
- `discord` last outbound observed: `None`
- `discord` bot: `Ajna` (`1469043297174421618`)

## Ontology Domain Readiness

- Local API reachable: `True`
- Local proxy reachable: `True`
- macOS resolver sees domain: `True`
- `dig` sees public records: `True`
- Direct public edge health reachable: `True`
- Default local domain health reachable: `True`

## Tunnel

- `cloudflared` installed: `True`
- Cloudflare tunnel cert present: `True`
- Local tunnel config present: `True`
- Named tunnel present: `True`
- Tunnel LaunchAgent loaded: `True`
- Tunnel LaunchAgent state: `active`

## Reading

- Local auth and serving surfaces can be checked without exposing secrets in repo artifacts.
- Slack and Discord may be healthy and authenticated before any real inbound/outbound traffic is observed.
- If `dig` and direct edge health are green while default local curl still fails, the public cutover is live and only the local resolver is stale.
- CLI and Keychain status should remain pointer-only; credentials stay local.
