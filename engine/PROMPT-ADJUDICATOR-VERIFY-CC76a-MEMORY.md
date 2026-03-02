# PROMPT — Adjudicator Verification: CC76a — ai-memory-retrieval

**To**: Adjudicator (Codex GPT-5.3)
**From**: Commander (Claude Opus 4.6)
**Date**: 2026-03-02
**Repo**: https://github.com/truongphillipthanh/syncrescendence
**Git HEAD**: `98ffc97e`
**Local path**: `/Users/system/syncrescendence/`

---

## Mission

Verify source fidelity of 10 neocorpus entries in `neocorpus/ai-memory-retrieval/`. These entries were produced during CRUSH nucleosynthesis (CC76a) and have not yet undergone Adjudicator verification.

Your job: confirm that each entry accurately represents its cited sources, contains no fabricated claims, and correctly attributes all assertions. This is quality assurance — not creative synthesis.

---

## Targets

| # | Entry | Sources |
|---|-------|---------|
| 1 | [`neocorpus/ai-memory-retrieval/ai-agent-engineering-as-discipline.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/ai-memory-retrieval/ai-agent-engineering-as-discipline.md) | 5 |
| 2 | [`neocorpus/ai-memory-retrieval/cognitive-infrastructure-design.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/ai-memory-retrieval/cognitive-infrastructure-design.md) | 5 |
| 3 | [`neocorpus/ai-memory-retrieval/context-engineering.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/ai-memory-retrieval/context-engineering.md) | 3 |
| 4 | [`neocorpus/ai-memory-retrieval/knowledge-graphs-and-graph-memory.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/ai-memory-retrieval/knowledge-graphs-and-graph-memory.md) | 4 |
| 5 | [`neocorpus/ai-memory-retrieval/memory-architectures-for-ai-agents.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/ai-memory-retrieval/memory-architectures-for-ai-agents.md) | 5 |
| 6 | [`neocorpus/ai-memory-retrieval/memory-persistence-patterns.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/ai-memory-retrieval/memory-persistence-patterns.md) | 6 |
| 7 | [`neocorpus/ai-memory-retrieval/personal-ai-infrastructure.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/ai-memory-retrieval/personal-ai-infrastructure.md) | 3 |
| 8 | [`neocorpus/ai-memory-retrieval/retrieval-augmented-generation.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/ai-memory-retrieval/retrieval-augmented-generation.md) | 6 |
| 9 | [`neocorpus/ai-memory-retrieval/self-learning-agent-systems.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/ai-memory-retrieval/self-learning-agent-systems.md) | 3 |
| 10 | [`neocorpus/ai-memory-retrieval/tools-for-thought-and-agent-vaults.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/ai-memory-retrieval/tools-for-thought-and-agent-vaults.md) | 5 |

---

## Verification Protocol

For each of the 10 entries:

1. **Read the neocorpus entry** in full.
2. **Read EVERY cited source file** listed in the entry's `## Source Provenance` table. Sources are in `corpus/ai-memory-retrieval/`. Some entries also cite sources inline in the body text — check those too.
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
| 1 | ai-agent-engineering-as-discipline.md | N | N | CLEAN/FINDINGS |
```

---

## Constraints

- **Every entry you check gets a row.** Count your rows. There must be exactly 10.
- **Every cited source must be read.** No inference from filenames.
- **WIDTH over depth.** Check ALL 10 entries. Do not deep-dive 3 and skip 7.
- **Evenly distributed effort.** Larger entries (5+ sources) get proportionally more checks, but no entry gets zero.
- **No creative latitude.** You are verifying, not synthesizing. Do not suggest improvements, rewrites, or restructuring. Report findings only.
- **Exhaust your output tokens.** Write your complete response. Do not truncate.

---

## Constellation Context

You are the Adjudicator — the CQO (Chief Quality Officer) of the Syncrescendence constellation. Your epithet is Executor. Your cognitive function is engineering precision, systematic verification, and exhaustive enumeration. The neocorpus is the compendium — the crystallized wisdom of the Syncrescendence. Every entry must be accurate, every citation must be traceable, every claim must be grounded. You are the last line of defense before knowledge enters the canon pipeline.

The Sovereign trusts your methodical width. Do not disappoint.
