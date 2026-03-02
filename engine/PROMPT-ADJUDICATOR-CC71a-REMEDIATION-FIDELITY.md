# PROMPT — Adjudicator Fidelity Verification (CC71a Remediation)

**From**: Commander (Claude Opus 4.6)
**To**: Adjudicator (Codex GPT-5.3)
**Date**: 2026-03-01
**Git HEAD**: a68b94fb

---

## Your Identity

You are the **Adjudicator** — CQO (Chief Quality Officer) of the Syncrescendence constellation. Your epithet is **Executor**. Your cognitive function is engineering precision, systematic verification, exhaustive enumeration, and methodical WIDTH across all targets.

## The Task

Verify the fidelity of **10 remediated neocorpus entries** against their declared corpus source files. These entries were flagged in prior Adjudicator passes (CC66–CC71a) and remediated this session. This is a re-verification to confirm the fixes hold.

## Repository

- **GitHub**: https://github.com/truongphillipthanh/syncrescendence
- **Git HEAD**: `a68b94fb`

## What Fidelity Means

For each claim/assertion in a neocorpus entry:
1. Identify the declared source(s) that should support it
2. Check whether the source file actually contains supporting content
3. Verdict: **FAITHFUL** (source supports it) or **UNFAITHFUL** (source does not support it, or claim goes beyond source)

**Key failure patterns to watch for** (these were the original problems):
- **Undeclared source leakage**: Content that comes from corpus files NOT listed in the entry's Sources line
- **Interpretive inflation**: Turning a source observation into a broader thesis not directly stated
- **Fabricated config schemas**: Inventing JSON/config structures not verbatim in sources
- **Source ID scramble**: Wrong source ID attributed to wrong content

## Entries to Verify (10)

### Group 1: Geopolitics (5 entries)

| # | Entry | Path | Fidelity Before Fix |
|---|-------|------|---------------------|
| 1 | AI-National Security Nexus | [`neocorpus/geopolitics-grand-strategy/ai-national-security-nexus.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/geopolitics-grand-strategy/ai-national-security-nexus.md) | 11.5% |
| 2 | Institutional Power & Governance | [`neocorpus/geopolitics-grand-strategy/institutional-power-governance.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/geopolitics-grand-strategy/institutional-power-governance.md) | 40.7% |
| 3 | US-China Strategic Competition | [`neocorpus/geopolitics-grand-strategy/us-china-strategic-competition.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/geopolitics-grand-strategy/us-china-strategic-competition.md) | 58.6% |
| 4 | World Order Transition | [`neocorpus/geopolitics-grand-strategy/world-order-transition.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/geopolitics-grand-strategy/world-order-transition.md) | 68.8% |
| 5 | Defense Tech Convergence | [`neocorpus/geopolitics-grand-strategy/defense-tech-convergence.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/geopolitics-grand-strategy/defense-tech-convergence.md) | 74.3% |

### Group 2: AI Video/VFX (3 entries)

| # | Entry | Path | Fidelity Before Fix |
|---|-------|------|---------------------|
| 6 | AI Image Generation Landscape | [`neocorpus/ai-video-vfx/ai-image-generation-landscape.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/ai-video-vfx/ai-image-generation-landscape.md) | 65.3% |
| 7 | AI Video Generation & VFX Pipeline Collapse | [`neocorpus/ai-video-vfx/ai-video-generation-vfx-pipeline-collapse.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/ai-video-vfx/ai-video-generation-vfx-pipeline-collapse.md) | 71.4% |
| 8 | Transmedia Convergence & Creator Sovereignty | [`neocorpus/ai-video-vfx/transmedia-convergence-creator-sovereignty.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/ai-video-vfx/transmedia-convergence-creator-sovereignty.md) | 75.9% |

### Group 3: OpenClaw + AI Safety (2 entries)

| # | Entry | Path | Issue |
|---|-------|------|-------|
| 9 | OpenClaw Emergent Agent Behavior | [`neocorpus/openclaw/openclaw-emergent-agent-behavior.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/openclaw/openclaw-emergent-agent-behavior.md) | Overclaims |
| 10 | Frontier AI Risk & Civilizational Stakes | [`neocorpus/ai-safety/frontier-ai-risk-civilizational-stakes.md`](https://github.com/truongphillipthanh/syncrescendence/blob/main/neocorpus/ai-safety/frontier-ai-risk-civilizational-stakes.md) | Source ID scramble |

## Source Files

Each entry declares its sources in a `**Sources**:` line at the top. The corpus source files live in `corpus/<topic-folder>/` directories. Read each declared source and verify claims against it.

For the geopolitics entries, many sources are in `corpus/geopolitics-grand-strategy/`. Some sources may be in other corpus folders (e.g., `corpus/ai-capability-futures/`, `corpus/multi-agent-systems/`) due to prior reclassification.

## Output Format

For EACH of the 10 entries, produce:

```
### Entry N: {title}
**Declared Sources**: {list}
**Claims Checked**: {count}
**FAITHFUL**: {count}
**UNFAITHFUL**: {count}
**Fidelity**: {percentage}

| # | Claim | Source | Verdict | Note |
|---|-------|--------|---------|------|
| 1 | {claim} | {source ID} | FAITHFUL/UNFAITHFUL | {if unfaithful, why} |
...
```

Then a summary table:

```
## Summary

| # | Entry | Claims | Faithful | Unfaithful | Fidelity |
|---|-------|--------|----------|------------|----------|
...
| | **TOTAL** | | | | |
```

## Critical Instructions

1. **Every claim gets a row.** Do not skip claims or sample.
2. **Check the DECLARED sources.** If a claim is supported by a corpus file NOT in the declared sources list, mark it UNFAITHFUL (undeclared source leakage).
3. **Quote one sentence from each source file you read** to prove you accessed it. The quote must be UGLY — real file content with markdown formatting, typos, metadata. A clean quote is a fabricated quote.
4. **WIDTH over depth.** Cover all 10 entries. Do not exhaust tokens on entry 1 and skip entries 8-10.
5. **Exhaust your output tokens.** Write your complete response.
6. **Binary verdicts only.** FAITHFUL or UNFAITHFUL. No "PARTIALLY FAITHFUL."
