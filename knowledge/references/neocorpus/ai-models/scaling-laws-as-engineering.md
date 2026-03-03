# Scaling Laws as Engineering

Two senior figures from OpenAI — Mark Chen (Chief Research Officer) and Jerry Tworek (former researcher, nearly seven years) — frame scaling laws not as theoretical curiosities but as operational planning instruments. Chen's account concerns compute allocation inside a large lab. Tworek's account concerns where that approach is heading and what it misses. ARK Invest's Brett Winton provides an external investor perspective on the capital dynamics sustaining the compute build-out.

---

## Compute Allocation as the Core Engineering Problem

Mark Chen described the allocation problem that scaling laws solve: how do you rank approximately 300 internal research projects when everyone believes theirs is the one that matters? Scaling laws provide the basis for that ranking. Given a total compute budget, they allow a lab to predict expected return on each allocation — transforming research prioritization from a political problem into an engineering problem.

Chen also described "supercharging pre-training" as the current direction at OpenAI — not abandoning pre-training scale but treating renewed investment in pre-training as a live priority alongside other advances. The framing is: pre-training remains central, not finished.

The compute demand is, in Chen's characterization, insatiable. Every efficiency gain raises the ceiling of what can be attempted rather than reducing total spend.

---

## The "Is Scaling Dead?" Debate

Chen addressed this directly under the chapter "Is Scaling Dead? Supercharging Pre-training." His position: the question misframes the situation. Pre-training scale remains a live engineering priority.

Tworek's account adds friction. His chapter "Beyond Pre-Training: The Need for New Scaling Methods" signals that he believes pure pre-training scale is insufficient — new methods are needed. This is not a claim that scaling is dead; it is a claim that the current recipe has limits and the field needs to find the next one.

---

## Homogeneity of Current Labs

Tworek observed what he called the "sad homogeneity" of current AI labs — nearly every major lab converging on the same ideas. His concern: if everyone is running the same recipe, the field's ability to discover alternatives atrophies. The next real breakthroughs may require approaches that diverge from the current consensus.

He identified John Carmack, Ilya Sutskever, and Yann LeCun as "mavericks" — figures pursuing different approaches. The chapter "Two Big Bets: New Architectures & Continual Learning" suggests Tworek's own view of where meaningful divergence might lie.

---

## Capital Dynamics

ARK Invest's Brett Winton argued the AI investment build-out is not a bubble. His claims: current revenue projections for AI companies are conservative relative to actual pricing power; massive data center CapEx spending is justified; and productivity gains from AI tools are expected to compound significantly. His framing supports the reading that the compute build-out reflects rational capital allocation, not speculative excess.

---

## Anti-Patterns

- **Declaring scaling dead based on one axis**: Tworek identified limits to pre-training scaling while also noting the field needs new methods — not that all scaling is exhausted.
- **Monoculture as strategy**: If all labs pursue the same recipe, the field's ability to discover alternatives atrophies. Tworek's homogeneity concern is precisely this: convergence on proven approaches may be strategically rational for individual labs while degrading the field's overall research diversity.
- **Treating efficiency gains as cost reduction**: Chen's insatiable demand framing implies efficiency improvements get reinvested into larger attempts rather than reducing total compute spend.

---

## Temporal Framing

### Obsolescence: "Is Scaling Dead?" as a Diagnostic

The question "Is scaling dead?" — which Mark Chen addressed directly in the December 2025 episode — is itself a temporal artifact. The question only becomes askable after a period during which scaling was treated as an unquestioned primary strategy. It arose because several inflection points suggested diminishing returns: GPT-4 to GPT-4.5 showed smaller capability leaps than GPT-3 to GPT-4, and the compute cost of each subsequent generation escalated faster than the capability gain.

Chen's answer ("pre-training scale remains a live engineering priority") and Tworek's answer ("the current recipe has limits; new methods are needed") are not contradictory. They describe two different questions: Chen is answering whether pre-training is still worth doing; Tworek is answering whether pre-training alone is sufficient. Both can be true.

The obsolescence lesson: the assumption that a single scaling recipe — more data, more compute, same architecture — would compound indefinitely was not stated explicitly, but it was acted upon. Investment decisions, team structures, and research roadmaps were built around it. Tworek's "sad homogeneity" observation is the obituary for that assumption: when every lab converges on the same recipe, it signals that the recipe is no longer a differentiator — either because it works for everyone or because everyone has hit the same ceiling.

### Supersession: Scaling Strategies

**v1 (2020-2023)**: Pre-training scale as the primary lever. Chinchilla scaling laws (Hoffmann et al., 2022) provided the governing formula: given a compute budget, allocate between model size and training tokens at a specific ratio. Labs built roadmaps around this. The assumption was that the Chinchilla recipe was approximately optimal and that capability gains would follow predictably from compute investment.

**v2 (2024-2026)**: Pre-training scale as one of several levers. Reinforcement learning for reasoning (RLHF → RLVR → test-time compute) emerged as a complementary scaling axis. GPT-4o, o1, and the GPT-5.x reasoning models demonstrate that scaling inference compute (chain-of-thought, multi-attempt reasoning) produces capability gains on specific task classes that pre-training scale alone does not. Tworek's "new architectures and continual learning" chapter signals that labs are searching for v3 — scaling axes that pre-training and RL-for-reasoning do not cover.

**What broke v1**: The reasoning model breakthrough (o1-class models) demonstrated that test-time compute was a scalable capability axis, not just an architectural trick. This was not predicted by the Chinchilla scaling laws, which measured training-time compute only. The lesson: scaling laws are predictive only within the paradigm they were derived from. Paradigm shifts produce new scaling axes that old laws do not capture.

### Phase 3-4 Audit Note

Both cited sources (09558, 10201) are description-only YouTube videos with no transcripts. The temporal framing above is derived from chapter titles, the episode framing ("Is Scaling Dead?"), and Tworek's "sad homogeneity" comment as represented in the entry. The Chinchilla reference is sourced from external knowledge, not from the cited corpus files. The supersession chain is reasoned inference, not direct citation.

---

## Source Provenance

| Source | Corpus ID | Content |
|--------|-----------|---------|
| Mark Chen interview (Core Memory Podcast, EP 46) | `corpus/ai-models/09558.md` | Compute allocation; ranking ~300 research projects; "Is Scaling Dead? Supercharging Pre-training"; insatiable demand for compute |
| Jerry Tworek interview (Core Memory Podcast, EP 53) | `corpus/ai-models/10201.md` | Beyond pre-training; new scaling methods needed; "sad homogeneity" of AI labs; mavericks (Carmack, Ilya, LeCun); new architectures and continual learning |
| Extraction: ARK Invest AI bubble analysis | `corpus/ai-models/01248.md` | AI investment not a bubble; CapEx justified; pricing power; productivity gains compounding |
