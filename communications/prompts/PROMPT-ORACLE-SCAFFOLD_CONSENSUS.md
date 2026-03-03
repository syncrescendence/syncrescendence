# PROMPT-ORACLE-SCAFFOLD_CONSENSUS.md
## Oracle Recon Directive: How Should a Multi-Agent AI Repo Be Organized?
**Priority**: P1 — scaffold tightening prerequisite
**Target Platform**: Grok (Oracle)
**Reply-To**: Commander | **CC**: Ajna
**Date**: 2026-02-22

---

## Directive

Oracle, RECON mission. We need to tighten our repository scaffold — it grew organically and has accumulated cruft. Before we restructure, we need to know: **what does consensus say the BEST way to organize a multi-agent AI knowledge repo looks like?**

### Our Current Structure (simplified)
```
orchestration/    (~250 files: state/, scripts/, archive/)
canon/            (81 verified knowledge files, protected)
engine/           (135 operational files: REF-, FUNC-, PROMPT-, MODEL-, DYN-)
sources/          (~1788 raw/processed sources)
praxis/            (31 distilled operational wisdom files)
agents/              (5 agent offices with inbox/outbox/memory)
```

State directory (orchestration/state/) is the main culprit — ~80 files including:
- ARCH-* (architecture decisions, ~20 files)
- DYN-* (dynamic state, ~15 files)
- REF-* (reference specs, ~10 files)
- impl/ subdirectories (clarescence, kinetic, sensing, tooling)

### What We Need to Know
1. **How do the best multi-agent repos organize operational state?** — single file vs many files, flat vs nested, naming conventions
2. **Is our ARCH/DYN/REF prefix taxonomy good?** — or is there a better way to categorize operational docs?
3. **How do production AI teams manage configuration drift?** — our AGENTS.md → Makefile → platform-specific files is novel; is anyone else doing this?
4. **The Obsidian/git pattern** — we're moving toward Obsidian co-location. What patterns exist for Obsidian vaults that also serve as AI agent repos?
5. **ADR (Architecture Decision Records)** — should our ARCH-* files follow ADR conventions? What's the consensus on ADR in AI agent repos?
6. **State management at scale** — with 5 agents, our state directory is manageable. At 10 agents? 20? What patterns scale?

### Search Vectors
- GitHub: repos with "multi-agent" + "orchestration" >500 stars — look at their directory structures
- X: "CLAUDE.md" OR "AI agent repo" OR "multi-agent organization" (last 30 days)
- ADR: "adr" + "ai" + "architecture decision record" (best practices 2025-2026)
- Obsidian: "obsidian vault" + "ai agent" OR "claude" (integration patterns)

### Output Format
For each pattern found:
```
### [REPO-NNN] Pattern Name
**Source**: [repo URL or reference]
**Scale**: [how many agents/files it handles]
**Key Insight**: [1-2 sentences]
**Applicable to Us**: [YES/NO + why]
```

Then provide your RECOMMENDATION for how we should tighten orchestration/state/.
