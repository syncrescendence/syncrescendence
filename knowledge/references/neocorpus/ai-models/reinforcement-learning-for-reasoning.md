# Reinforcement Learning for Reasoning

Reinforcement learning post-training represents one of the most consequential shifts in recent AI development. The reasoning models — OpenAI's o-series and their successors — emerged from a period when labs began moving beyond pre-training as the sole scaling lever. This shift is documented from three sources: a Chollet/Knoop interview on ARC-AGI and the limits of gradient descent, a Mark Chen (OpenAI CRO) interview reflecting on reasoning model breakthroughs, and a Jerry Tworek exit interview discussing lab convergence and the need for new scaling directions.

---

## The Reasoning Paradigm Shift

### Evidence from Benchmarks

Before 2024, large language models with only pre-training performed poorly on ARC: GPT-4's base model achieved 4–5%. Performance jumped significantly — to approximately 21% — with the introduction of reasoning paradigms, as seen with o1 and o1 preview. Chollet and Knoop cite this jump as evidence that the reasoning paradigm was transformational, and note that major labs including OpenAI and xAI subsequently adopted ARC-AGI as part of their model release evaluations.

### Industry Testimony

Mark Chen, OpenAI's Chief Research Officer, describes the breakthrough in reasoning models as one of OpenAI's most significant milestones, alongside a renewed focus on pre-training. He frames the compute allocation question — how to balance pre-training investment against other paradigms — as an active concern. The episode description references "the shift toward reasoning-driven models" and "what's next" as central themes, but no transcript is available, so specific technical claims about RL mechanisms cannot be attributed to this source.

Jerry Tworek, in his exit interview after nearly seven years at OpenAI, identifies the shift toward reasoning-driven models as one of the breakthroughs he worked on. The episode describes him discussing "the need for new scaling methods" beyond pre-training and the convergence of major labs on similar approaches. Again, no transcript is available; only chapter-level descriptions can be cited.

---

## The Sample Efficiency Gap

Francois Chollet's critique provides the clearest technical grounding. Gradient descent — the optimizer underlying pre-training and RL fine-tuning — is 4–5 orders of magnitude less sample-efficient than human learning. Chollet frames this as the core reason LLMs are not AGI: they encode programs acquired via gradient descent, which is far less efficient at skill acquisition than human intelligence. LLMs could serve as a memory or knowledge-representation component of AGI, but they lack the efficient skill acquisition that characterizes general intelligence.

Chollet further argues that relying on RL environments for AI progress is a "whack-a-mole" problem: it is impossible to create RL environments for every future problem, and solving novel problems without environment-specific training is core to AGI. This is distinct from claiming RL reasoning is without value — rather, it identifies a structural ceiling on what environment-specific RL training can achieve.

---

## The Homogeneity of Current Labs

Tworek's interview is described as addressing "the sad homogeneity of current AI labs" — the observation that nearly every major lab has converged on the same ideas. He names mavericks working on alternative approaches: Carmack, Ilya Sutskever, and LeCun. The episode also references "two big bets: new architectures and continual learning" as directions Tworek considers promising. The specific connection between this lab homogeneity and RL reasoning recipes is suggested by context but cannot be quoted directly without a transcript.

---

## The 2025–2026 Dual-Scaling Period

The combination of sources supports the claim that 2025–2026 marks a period where labs pursue capability improvement through multiple scaling axes — pre-training and post-training RL — rather than pre-training alone. Mark Chen's interview references a "renewed focus on pre-training" alongside reasoning model breakthroughs, suggesting both are active levers rather than a clean handoff from one paradigm to the other.

---

## Anti-Patterns

- **Anthropomorphizing RL reasoning**: Chollet explicitly distinguishes gradient descent-based skill acquisition from human learning. RL-trained reasoning outputs may resemble step-by-step human reasoning in appearance while differing fundamentally in mechanism.
- **Assuming RL environments generalize**: Chollet's critique applies — RL trained on specific environments does not automatically transfer to novel problems outside the training distribution. This is what ARC-AGI is designed to expose.
- **Treating benchmark jumps as mechanism proof**: The ARC performance jump with o1 demonstrates that the reasoning paradigm changed model behavior on this benchmark. It does not by itself explain which specific RL techniques drove the change.

---

## Source Provenance

| Source | Corpus ID | What It Actually Contains |
|--------|-----------|--------------------------|
| ARC-AGI v3 interview (Chollet & Knoop) | `corpus/ai-models/01191.md` | Transcript-derived atoms: gradient descent 4–5 orders of magnitude less efficient than human learning; LLMs as memory component; ARC benchmark jump from ~5% to 21% with reasoning paradigms; RL environment "whack-a-mole" critique |
| Mark Chen interview (Core Memory EP 46) | `corpus/ai-models/09558.md` | Episode description only (no transcript): reasoning model breakthrough; renewed pre-training focus; compute allocation across paradigms; AGI timeline speculation |
| Jerry Tworek interview (Core Memory EP 53) | `corpus/ai-models/10201.md` | Episode description only (no transcript): shift toward reasoning-driven models; need for new scaling methods beyond pre-training; homogeneity of AI labs; mavericks on alternative architectures |
