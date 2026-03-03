# Claude Code Anti-Patterns

## Core Failures

### 1. Kitchen sink context

Loading every file, note, and doctrine artifact at session start.

Failure mode:
- immediate context bloat
- degraded attention
- lower quality before work begins

### 2. Search-by-default

Making the agent rediscover obvious locations that the operator already knows.

Failure mode:
- wasted time
- higher token burn
- more variable edits

### 3. Thread as memory

Leaving key state only in conversation.

Failure mode:
- deletion destroys continuity
- compaction erases nuance
- provenance becomes impossible

### 4. Reactive compaction tolerance

Letting the session drift until quality degrades, then trusting the summary.

Failure mode:
- invisible loss of rationale
- contradictions after long runs
- poor handoffs

### 5. Over-delegation

Forking sub-agents for tiny or highly context-dependent work.

Failure mode:
- coordination overhead
- vague child tasks
- no real gain

### 6. Under-delegation

Keeping all search, analysis, and implementation in the main thread.

Failure mode:
- main-thread exhaustion
- context pressure
- preventable degradation

### 7. Monolithic constitution

Stuffing every harness-specific rule into one universal constitutional file.

Failure mode:
- bloated law
- conflicting instructions
- poor progressive loading

### 8. Skill shelfware

Creating skills that are never invoked, never wired, and never reviewed.

Failure mode:
- maintenance burden
- false sense of capability
- clutter in the skill surface

### 9. Prompt cargo culting

Reusing prompts mechanically across harnesses without respecting native grain.

Failure mode:
- brittle results
- poor leverage
- hidden mismatch between surface and doctrine

### 10. Filing improvisation

Choosing output locations ad hoc because the shell is ambiguous.

Failure mode:
- orphan artifacts
- duplicates and near-duplicates
- no enforceable lineage
