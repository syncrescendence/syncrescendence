# Ajna Runtime Synthesis

**Captured**: 2026-03-02T05:39:56Z

## Stable Facts

- Ajna primary model: `anthropic/claude-sonnet-4-5`
- OpenClaw workspace: `/Users/system/.openclaw/workspace`
- Browser enabled: `True`
- Installed skills: `playwright-mcp`

## Current Constraints

- Denied tools: `exec, process, apply_patch`
- Channel `slack` enabled: `True`
- Channel `discord` enabled: `True`
- Slack runtime token presence: bot=`True` app=`True`
- Slack keychain presence: bot=`True` app=`True`
- Slack provider health: running=`True` probeOk=`True` inbound=`None` outbound=`None`
- Discord runtime token presence: bot=`True`
- Discord keychain presence: bot=`True`
- Discord provider health: running=`True` probeOk=`True` inbound=`None` outbound=`None`

## Operational Reading

- Ajna is browser-capable and repo-grounded.
- Runtime remains conservative: browser is available, shell mutation remains denied in OpenClaw.
- Slack and Discord are now live in runtime, but their durable description must remain pointer-only and repo-safe.
- Durable decisions should be promoted from workspace memory into repo artifacts rather than living only in runtime files.

## Next Actions

- Use `make deploy-ajna` after repo-side OpenClaw instruction updates.
- Run `make sync-openclaw` after meaningful runtime changes or browser/OAuth milestones.
- Keep ontology/exocortex design separate until the boundary contract is settled.
