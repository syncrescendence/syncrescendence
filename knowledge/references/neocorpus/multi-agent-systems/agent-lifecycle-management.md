# Agent Lifecycle Management

**Nucleosynthesis Date**: 2026-03-02
**Synthesized By**: Commander (Claude Opus 4.6)
**Protocol**: CRUSH — lossless compression of corpus wisdom

---

## Sources

| ID | File | Content |
|----|------|---------|
| 00302 | `corpus/multi-agent-systems/00302.md` | Task dispatch artifact — usage limit hit, Exit-Code 75, lease-based claiming, retry protocol |
| 00574 | `corpus/multi-agent-systems/00574.md` | Adjudicator execution — auth expiry (OAuth invalid_token), MCP client startup failures, cascading errors |
| 09018 | `corpus/multi-agent-systems/09018.md` | Cartographer initialization — credential caching, extension loading, hook registry, server capability negotiation |

---

## Definitive Treatment

### What Agent Lifecycle Means

An agent is not a function call. It is a process with a lifespan — initialization, execution, degradation, and termination — each phase carrying distinct failure modes that the system must handle or die. Agent lifecycle management is the discipline of anticipating, detecting, and recovering from the inevitable failures that occur when long-running AI processes interact with rate-limited APIs, expiring credentials, saturated quotas, and finite context windows.

The term "lifecycle" is precise. Agents are born (initialized with credentials, context, and identity), live (execute tasks within resource constraints), age (accumulate context, approach limits), and die (exhaust resources, lose authorization, or complete their work). Systems that treat agents as stateless function calls — instantiate, invoke, discard — fail when any lifecycle phase encounters friction. Production systems must manage every phase explicitly.

---

### Initialization

Agent initialization is not instant and not guaranteed. The Cartographer startup sequence (09018) reveals the actual complexity: credential loading from cache, extension loading (code-review, conductor, plan, self-command, and others), MCP server connection with capability negotiation (tool updates, prompt updates), hook registry initialization, and security scanner attachment. Each step can fail independently.

The Adjudicator execution log (00574) demonstrates initialization failure in production: MCP clients for Notion and Linear failed to start because OAuth tokens had expired. The error cascaded — `AuthRequired` errors on the transport layer propagated to `handshaking with MCP server failed`, which propagated to the log suggesting a partial startup sequence, though the session ultimately failed. The agent did not crash cleanly — the log shows it started without tools it was supposed to have, which is worse — a silent capability reduction that the agent may not detect until mid-task.

**Initialization checklist** (derived from operational failures):
1. **Credential validation**: Test every credential before declaring readiness. Cached credentials expire. OAuth tokens rotate. API keys get revoked.
2. **Capability negotiation**: Verify that each MCP server connection actually established and the expected tools are available. Log which capabilities are missing.
3. **Extension loading**: Confirm each extension loaded. Failed extensions should produce loud errors, not silent degradation.
4. **Hook registration**: Verify hooks are active. Hooks that silently fail to register produce systems that appear to work but skip enforcement.
5. **Readiness declaration**: Only after all checks pass should the agent declare itself ready for task dispatch. Partial readiness must be reported as partial, never as full.

---

### Execution Under Constraints

Running agents operate within a cage of constraints: rate limits, token budgets, time limits, and quota ceilings. Hitting any constraint mid-task is not an exception — it is the normal operating condition for production systems.

#### Rate Limits and Backoff

API providers impose rate limits (requests per minute, tokens per minute, daily caps). When an agent hits a rate limit, it must:

1. **Detect the limit signal** (HTTP 429, provider-specific error codes, usage limit messages)
2. **Back off** with exponential delay (not fixed retry intervals, which create thundering herds)
3. **Report status** so the orchestrator knows the agent is alive but throttled
4. **Resume** when the limit window resets

The critical failure mode is not hitting the limit — it is failing to detect it. The task dispatch artifact (00302) shows a real case: `Failure-Reason: You've hit your usage limit`. The system detected the limit, assigned Exit-Code 75 (a specific code for resource exhaustion, distinguishing it from task failure), and incremented the retry counter. This is correct lifecycle management. The alternative — treating a rate limit as a task failure and abandoning the work — wastes everything the agent accomplished before the limit.

#### Lease-Based Claiming

When multiple agents share a task queue, lease-based claiming prevents duplicate work. The dispatch system (00302) demonstrates the pattern:

```
Lease-ID: lease-adjudicator-1771575249-40825
Claimed-By: adjudicator
Claimed-At: 2026-02-20T08:14:09Z
```

A lease is a time-bounded claim on a task. If the agent completes within the lease period, it writes results. If the lease expires (agent crashed, hit limits, timed out), the task returns to the queue for re-dispatch. This prevents both duplication (two agents working the same task) and abandonment (a crashed agent holding a task forever).

Lease design decisions:
- **Duration**: Long enough for legitimate completion, short enough for timely recovery. The `Timeout: 30` value in 00302 (unit unspecified) is aggressive if interpreted as seconds — appropriate for lightweight tasks, insufficient for deep analysis.
- **Renewal**: Should agents extend their own leases mid-task? Yes, for long tasks — but renewal requires liveness checking, adding complexity.
- **Escalation**: When a lease expires without completion, the escalation contact and delay determine how quickly a human or higher-authority agent is notified.

#### Shared Quota Pressure

In the Syncrescendence constellation, Psyche and Adjudicator share ChatGPT Plus capacity. This creates **quota interference**: simultaneous heavy jobs from both agents can saturate the shared ceiling, causing both to degrade. The constitutional rule — "Don't dispatch simultaneous heavy jobs to both under shared quota pressure" — is a lifecycle management policy encoded at the orchestration level.

Quota management strategies:
1. **Sequential dispatch**: Only one agent uses the shared resource at a time (simple but serial)
2. **Budget partitioning**: Allocate fractions of the quota to each agent (wastes slack capacity)
3. **Opportunistic scheduling**: Let agents compete for the shared quota with backoff on saturation (efficient but unpredictable)
4. **Staggered retries**: When Gemini free-tier resets, stagger retry timing to avoid thundering herd on the reset boundary

---

### Degradation and Context Exhaustion

Agents degrade before they fail. Context windows fill, attention quality drops, and the agent's reasoning becomes subtly worse before it becomes obviously wrong. The Syncrescendence context exhaustion protocol codifies the degradation curve:

| Threshold | Action |
|-----------|--------|
| **<30% context remaining** | ALERT the Sovereign. Continue working but flag every response. |
| **<15% context remaining** | Execute Handoff Protocol IMMEDIATELY. Non-negotiable. |

The critical insight: quality degrades at approximately 75% of context window capacity, not at 100%. Waiting for the agent to "run out" of context means operating in a degraded state for the final 25% of the window. The alert at 30% remaining (70% consumed) catches the degradation onset. The mandatory handoff at 15% remaining ensures no context death without state preservation.

Context exhaustion is the most common agent death in long-running sessions. Unlike rate limits (which are temporary) or auth expiry (which is detectable), context degradation is gradual and self-masking — the agent does not know its reasoning is getting worse.

---

### Termination and Exit Codes

How an agent dies determines whether its work survives. Exit codes are the lifecycle's final signal:

| Code | Meaning | Recovery Action |
|------|---------|-----------------|
| 0 | Success | Collect results, close task |
| 1 | General failure | Inspect execution log, re-dispatch or escalate |
| 75 | Resource exhaustion | Wait for quota reset, retry with same state |

Exit-Code 75 (00302) is semantically distinct from Exit-Code 1 (00574). Code 75 means "I could not finish because I ran out of resources, not because the task is impossible." The orchestrator should retry. Code 1 means "something broke" — retry may or may not help, and the execution log must be inspected to determine why.

The Adjudicator's auth failure (00574) terminated with Exit-Code 1, which is correct — the OAuth token expiry is not a resource exhaustion (the resource exists, the credential does not) and cannot be resolved by waiting. It requires human intervention (token refresh) or system reconfiguration.

---

### Human Relay Escalation

When all automated recovery fails — rate limits do not reset, credentials cannot be refreshed, the task exceeds all agents' capabilities — the system must escalate to a human operator. The escalation protocol must be:

1. **Bounded**: Escalation delay (10 minutes in 00302) prevents indefinite waiting
2. **Informative**: The escalation message must contain the task, the failure reason, the attempts made, and the specific human action needed
3. **Minimal**: Present the human with ONE action, not a multi-step procedure. "Paste this token" not "Go to the OAuth dashboard, navigate to credentials, click refresh, copy the new token, paste it here, then restart the agent."
4. **Recoverable**: After human action, the system must be able to resume from the point of failure, not restart from scratch

The Sovereign Interaction Protocol encodes this principle: "Present the Sovereign with a minimal action." Escalation is not delegation — it is a surgical request for the specific human capability (password entry, approval click, 2FA confirmation) that no agent can perform.

---

### Obsolescence and Supersession

#### The Stateless Invocation Model and Its Limits

Early agent frameworks treated agents as stateless functions: instantiate, invoke with a prompt, receive output, discard. This model descends from serverless computing patterns — each invocation is independent, side-effect-free, and short-lived. It works when agents are wrappers around a single API call.

It fails when agents are long-running processes that interact with rate-limited APIs, expire credentials, fill context windows, and claim leases on shared work queues. The lifecycle taxonomy in this entry — initialization, execution under constraints, degradation, termination — represents the design knowledge that accumulates when the stateless invocation model fails in production. The old assumption: "agents are calls." The replacement: "agents are processes with lifespans."

The Syncrescendence dispatch artifacts (exit codes, lease IDs, retry counts, escalation delays) are evidence that the stateless model was already superseded operationally before it was superseded conceptually. The system needed structured exit codes because invocations were failing for reasons that mattered — not just "success" or "failure" but "rate-limited" vs. "auth-expired" vs. "task invalid."

#### OAuth Token Lifecycle: From Ignored to First-Class Concern

Before agents operated unattended, OAuth tokens were managed by humans who re-authenticated when prompted. The token lifecycle (issuance, expiry, refresh, rotation) was a user-interface concern, not an infrastructure concern.

Unattended agent operation supersedes this assumption. An agent that needs to refresh an OAuth token at 3 AM cannot prompt a browser dialog. The cascade failure documented in the Adjudicator execution log (00574) — `AuthRequired` -> transport closure -> MCP client failure — is what happens when token lifecycle is treated as the prior paradigm assumed. The architectural response (dedicated credential management service, agent draws from token store rather than managing lifecycle itself) has not yet been standardized but is the direction the field is moving.

---

### Anti-Patterns

**Treating rate limits as failures.** A rate-limited agent is not a failed agent. It is a throttled agent. The orchestrator must distinguish between "cannot do" (failure) and "cannot do yet" (throttle) to avoid abandoning recoverable work.

**Silent capability degradation.** An agent that starts without some of its tools and does not report the gap will produce subtly wrong results. Failed MCP connections, expired credentials, and missing extensions must be loud failures at initialization, not silent gaps discovered mid-task.

**Fixed retry intervals.** Retrying a rate-limited request every 5 seconds creates thundering herds when multiple agents hit the same limit. Exponential backoff with jitter is the minimum viable retry strategy.

**No lease expiry.** An agent that crashes while holding a task without lease-based timeout creates an orphaned task that no other agent can claim. Every task claim must be time-bounded.

**Context death without handoff.** An agent that exhausts its context window without writing a handoff destroys all session state. The 15% threshold is the last safe moment for state preservation. Waiting longer is gambling with accumulated work.

**Escalating without information.** "Something went wrong" is not an escalation. "OAuth token for Linear expired, need refresh at dashboard.linear.app/settings/tokens, paste new token" is an escalation. The human must know exactly what to do and why.

---

### Implications

Agent lifecycle management is infrastructure, not application logic. Every multi-agent system needs:

1. **Structured exit codes** that distinguish success, failure, and resource exhaustion
2. **Lease-based task claiming** with bounded expiry and re-dispatch
3. **Initialization verification** that confirms all capabilities before declaring readiness
4. **Context monitoring** with degradation alerts before exhaustion
5. **Escalation paths** that present humans with minimal, actionable requests
6. **Quota-aware scheduling** that respects shared ceilings across agents

The systems that treat these as optional — that assume agents will just work, credentials will stay fresh, rate limits will not be hit, and context will not fill — are the systems in the 41-86.7% failure range. Lifecycle management is the difference between a demo and a deployment.

---

## Syncrescendence Operational Context

The following claims derive from the constellation's operational history and constitutional documents (AGENTS.md, CLAUDE.md, memory/), not from external corpus sources:
- Shared quota pressure between Psyche and Adjudicator on ChatGPT Plus capacity
- The constitutional rule against dispatching simultaneous heavy jobs under shared quota pressure
- Gemini free-tier reset hints and staggered retry strategies
- Context exhaustion thresholds (<30% alert, <15% mandatory handoff)
- The Sovereign Interaction Protocol's minimal-action escalation principle

---

## Provenance

This entry synthesizes operational artifacts from the Syncrescendence dispatch system: a task directive showing usage limit handling with Exit-Code 75 and lease-based claiming (00302), an execution log showing OAuth token expiry and cascading MCP client failures (00574), and an initialization log showing credential caching and capability negotiation (09018). The context exhaustion protocol is codified in CLAUDE.md. The shared quota management policy (Psyche + Adjudicator) is documented in AGENTS.md infrastructure section.
