# Claude Code Patterns

## High-Value Patterns

### 1. Constitutional source + generated surfaces

Keep shared law compact and render harness-specific outputs from source.

Why it works:
- one place to edit shared law
- harness-specific surfaces stay consistent
- stale divergence becomes measurable

### 2. Pointer-rich context injection

Supply exact files, paths, and anchors instead of forcing search.

Why it works:
- reduces variance
- lowers search overhead
- improves edit accuracy at scale

### 3. Progressive disclosure

Load only the doctrine required for the task:
- constitution first
- supporting files second
- skills on demand

Why it works:
- preserves context fidelity
- prevents kitchen-sink startup
- keeps sessions legible

### 4. Fresh-session discipline

Bias toward handoff and restart before degradation, rather than trusting compaction.

Why it works:
- preserves nuance
- keeps execution quality stable
- reduces summary-of-summary decay

### 5. Sub-agent reconnaissance

Use child contexts for bounded exploration and summary return.

Why it works:
- preserves main-thread context
- parallelizes discovery
- lets the parent remain strategic

### 6. Repo as memory

Persist durable state in files, not chat.

Why it works:
- deletion-safe
- inspectable
- compactable into future law and operators

### 7. Graduated trust

Use permissions and hooks to encode actual safety boundaries instead of all-or-nothing autonomy.

Why it works:
- reduces friction where confidence is earned
- preserves review on novel or risky actions

### 8. Artifact-class separation

Prompts, responses, handoffs, playbooks, outputs, and state artifacts should have distinct lanes and metadata.

Why it works:
- lowers filing entropy
- makes validators possible
- prevents the repo from becoming another undifferentiated memory swamp

### 9. Plan before wide edits

When the change spans many files or many domains, spend the first pass on mapping and sequencing.

Why it works:
- prevents blind edits
- improves ordering
- turns exploration into a reusable artifact

### 10. Compact repeated wins

Repeated prompts and repeated successful behaviors should not stay trapped in threads.

Compact them into:
- playbooks
- operators
- skills
- quality rules

Why it works:
- converts repeated effort into institutional capability
- keeps the shell antifragile under capability shifts
