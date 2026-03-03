# OpenClaw Patterns

## High-Value Patterns

### 1. Repo-to-runtime deployment loop

Render from constitutional source, then deploy conservatively into the workspace.

Why it works:
- reduces workspace drift
- keeps runtime aligned with repo law
- preserves a clear source/generated distinction

### 2. Runtime snapshotting

Capture gateway, channels, skills, identity, and model/provider state into repo-safe state artifacts.

Why it works:
- makes runtime legible
- catches drift early
- turns “it feels broken” into inspectable state

### 3. Explicit persona splits

Keep Ajna and Psyche on deliberately different provider/account surfaces when that serves the architecture.

Why it works:
- prevents accidental identity collapse
- preserves role differentiation
- turns auth into explicit design rather than accidental residue

### 4. Pointer-only secret discipline

Keep credentials in runtime config and Keychain; keep repo artifacts pointer-only.

Why it works:
- reduces secret sprawl
- preserves repo safety
- supports reconciliation without leakage

### 5. Event emission on durable change

Have the runtime write structured events whenever a meaningful state transition occurs.

Why it works:
- bridges runtime back into repo memory
- enables ontology projection
- preserves lineage across volatile sessions

### 6. Browser as specialist, not universal substrate

Use browser capability for UI-only steps, not as a reason to blur every execution surface together.

Why it works:
- respects the strengths of the runtime
- reduces over-automation fantasies
- keeps browser work bounded and legible

### 7. LaunchAgent / daemon hygiene

Treat background services as part of the harness and verify them with live turns, not only process state.

Why it works:
- catches “loaded but dead” failures
- makes persistence real
- preserves operational confidence

### 8. Workspace memory as always-on tier

Keep workspace memory compact and explicitly operational.

Why it works:
- preserves useful continuity
- avoids always-on context bloat
- keeps the workspace from becoming a second canon
