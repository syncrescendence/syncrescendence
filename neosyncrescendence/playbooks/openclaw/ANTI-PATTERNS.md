# OpenClaw Anti-Patterns

## Core Failures

### 1. Workspace sovereignty drift

Letting OpenClaw workspace files become the de facto truth because they are easier to edit in the moment.

Failure mode:
- repo/runtime split
- stale law
- hidden divergence

### 2. Auth ambiguity

Treating setup tokens, OAuth, API-style credentials, and saved profiles as interchangeable.

Failure mode:
- broken agents
- phantom working state
- accidental account collapse

### 3. Secret-bearing artifacts

Allowing runtime failures or event files to capture raw tokens, cookies, or other sensitive material.

Failure mode:
- credential exposure
- cleanup debt
- trust erosion

### 4. Browser triumphalism

Assuming “browser enabled” means robust autonomous web execution is solved.

Failure mode:
- brittle flows
- unstable operator experience
- overclaiming capability

### 5. Gateway complacency

Treating the gateway as healthy because config looks right or the process exists.

Failure mode:
- silent runtime death
- broken extension relay
- false confidence

### 6. Session-store negligence

Ignoring malformed or stale session files because the harness appears mostly functional.

Failure mode:
- control-plane bugs
- broken list/status behavior
- hard-to-diagnose runtime weirdness

### 7. Channel as memory

Using Slack or Discord conversations as the durable record of what happened.

Failure mode:
- hidden state
- no lawful lineage
- poor compaction and review

### 8. Monolithic OpenClaw identity

Treating all OpenClaw agents as one generic runtime.

Failure mode:
- no role clarity
- broken account strategy
- accidental overwrites of live runtime assumptions
