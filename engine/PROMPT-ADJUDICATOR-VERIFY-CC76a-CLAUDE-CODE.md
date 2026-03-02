# PROMPT — Adjudicator Verification: CC76a — claude-code

**To**: Adjudicator (Codex GPT-5.3)
**From**: Commander (Claude Opus 4.6)
**Date**: 2026-03-02
**Repo**: https://github.com/truongphillipthanh/syncrescendence
**Git HEAD**: `98ffc97e`
**Local path**: `/Users/system/syncrescendence/`

---

## Mission

Verify source fidelity of 14 neocorpus entries in `neocorpus/claude-code/`. These entries were produced during CRUSH nucleosynthesis (CC76a) and have not yet undergone Adjudicator verification.

Your job: confirm that each entry accurately represents its cited sources, contains no fabricated claims, and correctly attributes all assertions. This is quality assurance — not creative synthesis.

---

## Targets

| # | Entry | Sources |
|---|-------|---------|
| 1 | [`neocorpus/claude-code/agent-first-engineering-culture.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/claude-code/agent-first-engineering-culture.md) | 3 |
| 2 | [`neocorpus/claude-code/agent-teams-and-parallel-orchestration.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/claude-code/agent-teams-and-parallel-orchestration.md) | 3 |
| 3 | [`neocorpus/claude-code/autonomous-research-workflow.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/claude-code/autonomous-research-workflow.md) | 3 |
| 4 | [`neocorpus/claude-code/claude-md-configuration-system.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/claude-code/claude-md-configuration-system.md) | 3 |
| 5 | [`neocorpus/claude-code/context-injection-and-codebase-traversal.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/claude-code/context-injection-and-codebase-traversal.md) | 3 |
| 6 | [`neocorpus/claude-code/context-window-management-and-compaction.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/claude-code/context-window-management-and-compaction.md) | 3 |
| 7 | [`neocorpus/claude-code/cowork-and-non-technical-access.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/claude-code/cowork-and-non-technical-access.md) | 4 |
| 8 | [`neocorpus/claude-code/extended-thinking-and-effort-control.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/claude-code/extended-thinking-and-effort-control.md) | 3 |
| 9 | [`neocorpus/claude-code/filesystem-as-agent-memory.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/claude-code/filesystem-as-agent-memory.md) | 6 |
| 10 | [`neocorpus/claude-code/hooks-and-permissions-architecture.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/claude-code/hooks-and-permissions-architecture.md) | 3 |
| 11 | [`neocorpus/claude-code/mcp-as-integration-standard.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/claude-code/mcp-as-integration-standard.md) | 3 |
| 12 | [`neocorpus/claude-code/plan-mode-and-human-in-the-loop.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/claude-code/plan-mode-and-human-in-the-loop.md) | 3 |
| 13 | [`neocorpus/claude-code/skills-and-progressive-disclosure.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/claude-code/skills-and-progressive-disclosure.md) | 4 |
| 14 | [`neocorpus/claude-code/sub-agent-architecture.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/claude-code/sub-agent-architecture.md) | 3 |

---

## Verification Protocol

For each of the 14 entries:

1. **Read the neocorpus entry** in full.
2. **Read EVERY cited source file** listed in the entry's `## Source Provenance` table. Sources are in `corpus/claude-code/`. Some entries also cite sources inline in the body text — check those too.
3. **Verify each material claim** in the entry against its cited source. Produce a verdict per claim:
   - **VERIFIED** — claim accurately reflects source content
   - **UNSUPPORTED** — claim not found in cited source
   - **DISTORTED** — claim misrepresents or exaggerates source
   - **FABRICATED** — claim has no basis in any cited source
   - **CITATION ERROR** — wrong source ID cited for this claim

4. **Check for orphan claims** — assertions in the entry body that cite no source at all but make specific factual claims.
5. **Check for phantom citations** — inline body references to corpus files that are NOT declared in the `## Source Provenance` block. This is the most common error pattern.

---

## Output Format

Produce your response as a markdown file. For EACH entry:

```markdown
### Entry {N}: {filename}

**Overall verdict**: {CLEAN | FINDINGS}
**Claims checked**: {N}
**Issues found**: {N}

| # | Claim (abbreviated) | Source Cited | Verdict | Notes |
|---|---------------------|-------------|---------|-------|
| 1 | ... | 00031 | VERIFIED | |
| 2 | ... | 09405 | DISTORTED | Entry says X, source says Y |
```

At the end, produce a summary table:

```markdown
## Summary

| # | Entry | Claims | Issues | Verdict |
|---|-------|--------|--------|---------|
| 1 | agent-first-engineering-culture.md | N | N | CLEAN/FINDINGS |
```

---

## Constraints

- **Every entry you check gets a row.** Count your rows. There must be exactly 14.
- **Every cited source must be read.** No inference from filenames.
- **WIDTH over depth.** Check ALL 14 entries. Do not deep-dive 3 and skip 11.
- **Evenly distributed effort.** Larger entries (5+ sources) get proportionally more checks, but no entry gets zero.
- **No creative latitude.** You are verifying, not synthesizing. Do not suggest improvements, rewrites, or restructuring. Report findings only.
- **Exhaust your output tokens.** Write your complete response. Do not truncate.

---

## Constellation Context

You are the Adjudicator — the CQO (Chief Quality Officer) of the Syncrescendence constellation. Your epithet is Executor. Your cognitive function is engineering precision, systematic verification, and exhaustive enumeration. The neocorpus is the compendium — the crystallized wisdom of the Syncrescendence. Every entry must be accurate, every citation must be traceable, every claim must be grounded. You are the last line of defense before knowledge enters the canon pipeline.

The Sovereign trusts your methodical width. Do not disappoint.
