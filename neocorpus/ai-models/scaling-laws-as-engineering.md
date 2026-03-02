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

## Source Provenance

| Source | Corpus ID | Content |
|--------|-----------|---------|
| Mark Chen interview (Core Memory Podcast, EP 46) | `corpus/ai-models/09558.md` | Compute allocation; ranking ~300 research projects; "Is Scaling Dead? Supercharging Pre-training"; insatiable demand for compute |
| Jerry Tworek interview (Core Memory Podcast, EP 53) | `corpus/ai-models/10201.md` | Beyond pre-training; new scaling methods needed; "sad homogeneity" of AI labs; mavericks (Carmack, Ilya, LeCun); new architectures and continual learning |
| Extraction: ARK Invest AI bubble analysis | `corpus/ai-models/01248.md` | AI investment not a bubble; CapEx justified; pricing power; productivity gains compounding |
