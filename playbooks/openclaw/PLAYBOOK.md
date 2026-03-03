# OpenClaw Playbook

**Status**: live-v1  
**Class**: harness playbook  
**Authority chain**: constitution -> executive intention -> program -> playbook -> runtime surface / events / operators  
**Primary sources**:
- [AGENTS.md](/Users/system/syncrescendence/AGENTS.md)
- [TOOL-STACK-LIVE-STATE.md](/Users/system/syncrescendence/00-ORCHESTRATION/state/TOOL-STACK-LIVE-STATE.md)
- [OPENCLAW-RUNTIME-SNAPSHOT.md](/Users/system/syncrescendence/00-ORCHESTRATION/state/OPENCLAW-RUNTIME-SNAPSHOT.md)
- [AGENT-RUNTIME-IDENTITIES-CC75.md](/Users/system/syncrescendence/00-ORCHESTRATION/state/impl/AGENT-RUNTIME-IDENTITIES-CC75.md)
- [OPENCLAW-ROLE.md](/Users/system/syncrescendence/agents/ajna/OPENCLAW-ROLE.md)
- [openclaw-memory-architecture.md](/Users/system/syncrescendence/neocorpus/openclaw/openclaw-memory-architecture.md)
- [openclaw-setup-and-operations.md](/Users/system/syncrescendence/neocorpus/openclaw/openclaw-setup-and-operations.md)
- [openclaw-model-configuration.md](/Users/system/syncrescendence/neocorpus/openclaw/openclaw-model-configuration.md)
- [openclaw-communication-channels.md](/Users/system/syncrescendence/neocorpus/openclaw/openclaw-communication-channels.md)
- [syncrescendence-openclaw-infrastructure.md](/Users/system/syncrescendence/neocorpus/openclaw/syncrescendence-openclaw-infrastructure.md)

## 0. What This Surface Is For

OpenClaw is the persistent agent-runtime harness for Syncrescendence.

Its proper role is:
- host live agents on local machines
- bridge models, tools, channels, browser, and workspace memory
- emit durable state changes back toward repo truth
- provide a controlled runtime substrate for agents that are more persistent and more UI-/channel-capable than terminal harnesses

OpenClaw is not the constitutional source, not the long-term memory authority, and not the place where secrets should leak into durable artifacts.

## 1. Native Grain

OpenClaw’s native grain is defined by seven properties:

1. **Persistent runtime**
   It is meant to stay alive between tasks and across sessions.

2. **Workspace-centered memory**
   `SOUL.md`, `MEMORY.md`, and related workspace files form an always-on memory tier.

3. **Channel and browser surfaces**
   It can inhabit Discord, Slack, browser flows, and other UI-mediated execution paths that terminal harnesses handle poorly.

4. **Model/provider plasticity**
   Auth and provider strategy are part of the harness itself, not just session configuration.

5. **Gateway and daemon reality**
   Health of the harness depends on actual local runtime components: gateway, session store, launchd state, browser relay, channel tokens.

6. **Event-driven reconciliation**
   Runtime changes should flow outward through event emission and synchronization, not remain trapped inside local state.

7. **Persona/runtime split**
   Ajna and Psyche are not just names; they are distinct live runtime bindings with different auth surfaces and responsibilities.

## 2. What OpenClaw Is Bad At

OpenClaw is weak or structurally risky when:
- it is allowed to become a second canon with stale workspace truth diverging from the repo
- raw channel credentials or secrets are allowed to surface in durable artifacts
- operators confuse browser capability with reliable end-to-end browser worker fabric
- auth profiles are swapped casually, collapsing distinct agent identities
- local runtime repair history remains implicit instead of being distilled into doctrine

## 3. Runtime Identity Doctrine

Current live split:

- **Ajna**
  - machine: MacBook Air
  - provider: `anthropic`
  - model: `claude-sonnet-4-5`
  - auth mode: Claude setup-token / token-mode profile
  - role: browser-capable strategist and operational agent

- **Psyche**
  - machine: Mac mini
  - provider: `openai-codex`
  - model: `gpt-5.3-codex`
  - auth mode: OAuth profile
  - account: `truongphillipthanh@icloud.com`
  - role: tmux constellation substrate and ChatGPT Plus-backed agent surface

Do not collapse these accidentally. Runtime identity is part of the shell, not a disposable convenience setting.

## 4. Memory Doctrine

OpenClaw’s workspace memory is real, but it is not sovereign.

Use the workspace for:
- current runtime orientation
- compact local identity and state
- persistent live-session continuity

Do not use the workspace as:
- the final authority on architecture
- the durable repository of shell law
- the place where rich provenance should remain permanently

The correct rule is:
- workspace memory for live operation
- repo memory and state artifacts for durable institutional truth
- event reconciliation to bridge the two

## 5. Auth and Provider Doctrine

Auth mode is a first-class operational concern in OpenClaw.

Rules:
- use the provider/auth mode that matches the intended agent identity
- never assume OAuth and API-style auth are interchangeable
- keep account binding explicit in repo state artifacts
- treat auth rewiring as a runtime identity change, not a small implementation detail

The actual lesson from repairs is simple:
- auth must be verified on the provider’s terms
- session-store shape and daemon health matter as much as credentials
- a “working account” claim without a live turn is not enough

## 6. Browser and Channel Doctrine

### Browser

OpenClaw browser capability is valuable, but should be treated as a specialized runtime surface:
- useful for OAuth, dashboards, token regeneration, DOM work, and UI-only operations
- weaker than a dedicated worker fabric for large-scale automation
- best when paired with repo-grounded event emission and explicit surface law

### Channels

Slack and Discord are execution surfaces, not durable memory stores.

Use them to:
- route tasks
- run lightweight control flows
- surface agent output
- maintain operator-facing interaction

Do not use them to:
- store canonical state
- preserve secrets in transcripts
- replace repo-based lineage and logging

## 7. Runtime Health Doctrine

OpenClaw should be treated like infrastructure, not just a chat surface.

That means:
- gateway health matters
- daemon persistence matters
- session-store integrity matters
- relay attachment matters
- token/keychain presence matters
- runtime snapshotting matters

The harness is healthy only when it can execute live turns cleanly, not merely when configuration files look plausible.

## 8. Output and Event Doctrine

OpenClaw should externalize durable state changes through events.

Rules:
- one event per meaningful state change
- explicit `surface` and `artifact_class`
- pointer-first durable capture
- no raw tokens, cookies, or secrets
- repo-path references where durable effects occurred

This is how OpenClaw stops being an isolated runtime and becomes part of the governed shell.

## 9. Relationship to Other Surfaces

OpenClaw is not the terminal coder harness and not the final browser-worker architecture.

Use:
- Claude Code for repo-native implementation and constitutional editing
- OpenClaw for persistent live agents, browser- and channel-mediated operations, and subscription-runtime personas
- Cowork for interactive browser subscription workflows
- Manus for bounded autonomous external execution

OpenClaw’s role is persistent runtime orchestration, not universal replacement.

## 10. Compaction Targets

Repeated OpenClaw wins should compact into:
- runtime repair doctrine
- auth/provider rules
- event schemas
- safer bridge operators
- harness-specific playbook patterns

Repeated OpenClaw failures should compact into:
- anti-patterns
- sanitization rules
- quarantine rules
- stricter runtime sync and validator checks

## 11. Net Rule

Use OpenClaw as the persistent runtime shell:
- identity-explicit,
- provider-conscious,
- browser/channel-capable,
- event-emitting,
- and always subordinated to repo truth through reconciliation.
