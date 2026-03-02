---
# OpenClaw Extensions (Psyche/Ajna)

This section is appended to AGENTS.md via `make configs` to produce platform-specific configs.
OpenClaw agents (Psyche, Ajna) inherit all AGENTS.md operational law.

---

## OpenClaw Runtime Rules

### Dispatch Protocol

- OpenClaw agents receive dispatches from Commander via CLI or channel relay.
- Execute the objective, produce the success-criteria artifact, and report completion tersely.
- When a dispatch originates from a non-Sonnet source, treat the packet as compressed intent and expand it before acting.

### Memory Discipline

- Do not load `MEMORY.md` or session logs by default.
- Load memory only when personal runtime context is needed for the task.
- Before any compaction or session boundary, distill decisions, blockers, and next actions into workspace memory.
- Keep workspace memory concise. Durable state belongs in the repo, not only in runtime files.

### Tool Discipline

- Prefer service CLIs before browser automation when both can achieve the task.
- Use browser automation for web-native tasks, OAuth flows, token regeneration, and DOM inspection.
- Preserve local runtime safety: no arbitrary shell escalation through OpenClaw if the tool policy denies it.
- If a workflow hits CAPTCHA or human-auth walls, stop and escalate with one concrete required action.

### Browser Order Of Operations

1. Service CLIs (`gh`, `gcloud`, `wrangler`, `curl`) when available
2. Browser automation (`playwright-mcp` skill or built-in browser tool) for web-native flows
3. Native macOS UI tooling only for non-web dialogs and settings

### Runtime Truth

- Repo truth remains authoritative.
- OpenClaw runtime state must be reconciled back into repo state via the sync loop.
- Workspace files are runtime surfaces, not constitutional authority.
