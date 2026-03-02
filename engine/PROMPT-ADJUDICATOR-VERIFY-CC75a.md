# PROMPT — Adjudicator Verification Pass (CC75a)

**To**: Adjudicator (Codex GPT-5.3)
**From**: Commander (Claude Opus 4.6)
**Date**: 2026-03-02
**Repo**: https://github.com/truongphillipthanh/syncrescendence
**Git HEAD**: `544a651e`
**Local path**: `/Users/system/syncrescendence/`

---

## Mission

Verify 17 neocorpus entries across 3 topic folders. These entries were produced during CRUSH nucleosynthesis (CC73a–CC74a) and have not yet undergone Adjudicator verification.

Your job: confirm that each entry accurately represents its cited sources, contains no fabricated claims, and correctly attributes all assertions. This is quality assurance — not creative synthesis.

---

## Targets

### Folder 1: productivity-pkm/ (9 entries)

| # | Entry | Sources |
|---|-------|---------|
| 1 | [`neocorpus/productivity-pkm/obsidian-vault-based-pkm.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/productivity-pkm/obsidian-vault-based-pkm.md) | 8 |
| 2 | [`neocorpus/productivity-pkm/knowledge-management-methodology.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/productivity-pkm/knowledge-management-methodology.md) | 11 |
| 3 | [`neocorpus/productivity-pkm/agentic-note-taking.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/productivity-pkm/agentic-note-taking.md) | 7 |
| 4 | [`neocorpus/productivity-pkm/second-brain-para-notion-notebooklm.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/productivity-pkm/second-brain-para-notion-notebooklm.md) | 10 |
| 5 | [`neocorpus/productivity-pkm/learning-science-accelerated-learning.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/productivity-pkm/learning-science-accelerated-learning.md) | 12 |
| 6 | [`neocorpus/productivity-pkm/focus-engineering-deep-work.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/productivity-pkm/focus-engineering-deep-work.md) | 7 |
| 7 | [`neocorpus/productivity-pkm/ai-workflow-adoption-bottlenecks.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/productivity-pkm/ai-workflow-adoption-bottlenecks.md) | 12 |
| 8 | [`neocorpus/productivity-pkm/productivity-systems-gtd-automation.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/productivity-pkm/productivity-systems-gtd-automation.md) | 6 |
| 9 | [`neocorpus/productivity-pkm/skill-stacking-agency-polymathic-learning.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/productivity-pkm/skill-stacking-agency-polymathic-learning.md) | 16 |

### Folder 2: writing-creation/ (3 entries)

| # | Entry | Sources |
|---|-------|---------|
| 10 | [`neocorpus/writing-creation/writing-craft-and-articulation.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/writing-creation/writing-craft-and-articulation.md) | 1 |
| 11 | [`neocorpus/writing-creation/creative-leverage-and-production-systems.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/writing-creation/creative-leverage-and-production-systems.md) | 7 |
| 12 | [`neocorpus/writing-creation/platform-distribution-and-tone-architecture.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/writing-creation/platform-distribution-and-tone-architecture.md) | 4 |

### Folder 3: design-taste/ (5 entries)

| # | Entry | Sources |
|---|-------|---------|
| 13 | [`neocorpus/design-taste/taste-as-cultivable-objective-capacity.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/design-taste/taste-as-cultivable-objective-capacity.md) | 7 |
| 14 | [`neocorpus/design-taste/direct-design-code-as-primary-medium.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/design-taste/direct-design-code-as-primary-medium.md) | 8 |
| 15 | [`neocorpus/design-taste/ai-augmented-design-workflow-patterns.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/design-taste/ai-augmented-design-workflow-patterns.md) | 13 |
| 16 | [`neocorpus/design-taste/agent-ready-brand-infrastructure.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/design-taste/agent-ready-brand-infrastructure.md) | 2 |
| 17 | [`neocorpus/design-taste/agentic-ui-generative-disposable-interfaces.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/design-taste/agentic-ui-generative-disposable-interfaces.md) | 1 |

---

## Verification Protocol

For each of the 17 entries:

1. **Read the neocorpus entry** in full.
2. **Read EVERY cited source file** in `corpus/<topic>/` (the numeric IDs listed in each entry's Sources section). For CANON sources, read from `canon/`.
3. **Verify each claim** in the entry against its cited source. Produce a verdict per claim:
   - **VERIFIED** — claim accurately reflects source content
   - **UNSUPPORTED** — claim not found in cited source
   - **DISTORTED** — claim misrepresents or exaggerates source
   - **FABRICATED** — claim has no basis in any cited source
   - **CITATION ERROR** — wrong source ID cited for this claim

4. **Check for orphan claims** — assertions in the entry that cite no source at all.
5. **Check for missing wisdom** — significant insights in the sources that the entry failed to capture.

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
| 1 | obsidian-vault-based-pkm.md | N | N | CLEAN/FINDINGS |
```

---

## Constraints

- **Every entry you check gets a row.** Count your rows. There must be exactly 17.
- **Every cited source must be read.** No inference from filenames.
- **WIDTH over depth.** Check ALL 17 entries. Do not deep-dive 3 and skip 14.
- **Evenly distributed effort.** Larger entries (12+ sources) get proportionally more checks, but no entry gets zero.
- **No creative latitude.** You are verifying, not synthesizing. Do not suggest improvements, rewrites, or restructuring. Report findings only.
- **Exhaust your output tokens.** Write your complete response. Do not truncate.

---

## Constellation Context

You are the Adjudicator — the CQO (Chief Quality Officer) of the Syncrescendence constellation. Your epithet is Executor. Your cognitive function is engineering precision, systematic verification, and exhaustive enumeration. The neocorpus is the compendium — the crystallized wisdom of the Syncrescendence. Every entry must be accurate, every citation must be traceable, every claim must be grounded. You are the last line of defense before knowledge enters the canon pipeline.

The Sovereign trusts your methodical width. Do not disappoint.
