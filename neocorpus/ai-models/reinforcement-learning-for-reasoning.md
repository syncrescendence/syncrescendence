# Reinforcement Learning for Reasoning

Reinforcement learning from human feedback (RLHF) and its successors are the post-training techniques that transformed large language models from fluent text generators into reasoning systems. The shift is architectural in significance: pre-training gives a model knowledge; reinforcement learning gives it the ability to use that knowledge to solve problems step-by-step. The reasoning models — OpenAI's o-series, Anthropic's extended thinking, and their descendants — represent a regime where the primary capability improvement comes from RL post-training, not from scaling pre-training. This inverts the development paradigm that dominated 2020-2024, where pre-training scale was the primary lever. The fundamental tension: gradient descent, the optimizer underlying both pre-training and RL fine-tuning, is 4-5 orders of magnitude less sample-efficient than human learning. RL makes models reason, but the mechanism by which they reason bears little resemblance to human cognition.

---

## The RLHF Pipeline and Its Evolution

### Classical RLHF

The original RLHF pipeline (Christiano et al., 2017; refined by OpenAI for InstructGPT):

1. **Pre-train** a base model on internet text (unsupervised)
2. **Supervised fine-tuning** (SFT) on human-demonstrated responses
3. **Train a reward model** from human preference comparisons (which response is better?)
4. **Optimize the model** via reinforcement learning (PPO) to maximize the reward model's score

This pipeline converted base models that completed text into assistants that followed instructions. The reward model encodes human preferences; RL optimizes the model to produce outputs that score highly against those preferences.

### Beyond RLHF: Direct Preference Optimization and Variants

DPO (Direct Preference Optimization) eliminated the separate reward model and RL optimization step, instead directly optimizing the policy from preference pairs. RLHF's successors (DPO, IPO, KTO, ORPO) share the core insight — human preferences are the training signal — but differ in how they convert preferences into gradient updates.

The trend: simpler pipelines that achieve comparable or better results. The reward model and PPO loop introduced instability, hyperparameter sensitivity, and training complexity. Direct methods reduce engineering overhead while preserving the capability gains.

### RL for Reasoning: The New Frontier

The reasoning models (o1, o3, and their successors) represent a qualitative expansion of what RL post-training achieves. Instead of merely aligning the model's outputs with human preferences for helpfulness and safety, RL now trains the model to:

- Decompose problems into steps
- Evaluate intermediate results
- Backtrack when a reasoning path fails
- Allocate more "thinking" to harder problems
- Produce chain-of-thought traces that demonstrate step-by-step reasoning

This is RL applied not to output quality but to cognitive strategy. The reward signal shifts from "did the human prefer this response?" to "did this reasoning process arrive at the correct answer?" Process reward models (PRMs) evaluate each step of the reasoning chain, not just the final output.

---

## The Shift from Pre-Training-Primary to RL-Primary Capability

### The Historical Arc

- **2020-2023**: Pre-training scale is the primary lever. Bigger models, more data, more compute yield better performance. RL post-training (RLHF) is a refinement step that improves alignment and instruction-following.
- **2024**: The reasoning models reveal that RL can add capabilities that pre-training alone does not provide. Chain-of-thought reasoning, multi-step problem solving, and self-correction emerge primarily from RL training, not from scale.
- **2025-2026**: Labs converge on a dual-scaling paradigm — pre-training for knowledge, RL for reasoning. Jerry Tworek (formerly OpenAI) describes the need for "new scaling methods" beyond pre-training, and the "shift toward reasoning-driven models" as one of OpenAI's most important breakthroughs.

### Why RL Adds What Pre-Training Cannot

Pre-training optimizes next-token prediction. A model trained only to predict the next token learns to produce plausible text, including text that looks like reasoning. But it does not optimize for reasoning correctness — it optimizes for the statistical distribution of tokens that appear after reasoning-like prefixes.

RL optimizes for a different objective: did the reasoning process produce a correct outcome? This distinction is subtle but crucial. A pre-trained model may produce fluent, plausible-looking reasoning that arrives at an incorrect answer. An RL-trained model has been explicitly optimized to produce reasoning that arrives at correct answers, with incorrect reasoning paths penalized during training.

The result: RL-trained reasoning models show qualitatively different behavior on hard problems. They allocate more tokens to harder sub-problems, they backtrack and try alternative approaches, and they achieve higher accuracy on tasks that require multi-step deduction — not because they are larger, but because they have been trained to reason rather than to predict.

---

## The Sample Efficiency Gap

### Gradient Descent vs. Human Learning

Francois Chollet's persistent critique provides essential context: gradient descent, the optimizer underlying both pre-training and RL fine-tuning, is 4-5 orders of magnitude less sample-efficient than human learning. A human learns a new reasoning pattern from a handful of examples. An RL training run requires millions of trajectory samples to achieve comparable improvement.

This means that RL-trained reasoning is not reasoning in the way humans reason. The model does not learn abstract reasoning principles and apply them flexibly; it learns statistical patterns over millions of reasoning trajectories and interpolates between them. The outputs may look like reasoning — step-by-step, self-correcting, internally consistent — but the mechanism is statistical pattern matching at enormous scale, not the flexible abstraction that characterizes human cognition.

### The Implications

This gap does not make RL-trained reasoning useless — it makes it useful in a specific way. RL-trained models excel at problems that are well-represented in their training distribution. They can apply learned reasoning patterns reliably and quickly. But they struggle with genuinely novel problems that require reasoning patterns not present in training — the exact capability that ARC-AGI is designed to test and that Chollet argues is the essence of intelligence.

---

## Key Insights

### RL as the Second Scaling Axis

The discovery that RL post-training provides a scaling axis independent of pre-training is the most important architectural insight of the 2024-2026 period. Labs now optimize across both axes: pre-training compute for knowledge breadth, RL compute for reasoning depth. The optimal allocation between these two axes is an active research question and a competitive differentiator.

### Inference-Time Compute as the Third Axis

Reasoning models introduced a third scaling dimension: inference-time compute. By "thinking" for more tokens, the model can solve harder problems. This creates a cost-accuracy tradeoff at inference time — spend more tokens (and more money) for better answers. This is economically significant because inference costs are ongoing while training costs are one-time.

### The Convergence of Labs

Tworek's observation about the "sad homogeneity of current AI labs" applies directly to RL for reasoning. All major labs have converged on variants of the same approach: pre-train a large model, then RL-train it for reasoning. The architectures differ in details but share the fundamental structure. This convergence may indicate that the approach is correct, or it may indicate that the field is stuck in a local optimum. The mavericks working on alternative architectures (Sutskever's SSI, LeCun's JEPA) represent the hedge against this convergence being premature.

### Process vs. Outcome Rewards

A crucial design decision in RL for reasoning: reward each step of the reasoning process (process reward) or reward only the final answer (outcome reward)? Process rewards provide denser training signal and better credit assignment but require evaluating intermediate reasoning steps, which is harder to automate. Outcome rewards are simpler but can reward models that arrive at correct answers via flawed reasoning (lucky guessing). The field is trending toward process rewards as the superior approach, but the evaluation infrastructure for step-level assessment remains immature.

---

## Anti-Patterns

- **Assuming RL reasoning = human reasoning**: The mechanism is fundamentally different. Treating model reasoning as equivalent to human reasoning leads to misplaced trust in novel situations where the model's training distribution does not apply.
- **Ignoring the sample efficiency gap**: Celebrating reasoning benchmark improvements without acknowledging that achieving them required orders of magnitude more training signal than a human would need. The capability is real; the mechanism is profligate.
- **Treating thinking tokens as free**: Inference-time reasoning costs money proportional to the number of thinking tokens. For high-volume applications, the cost of RL-trained reasoning models can be substantially higher than pre-training-only models that answer immediately.
- **Conflating alignment RLHF with reasoning RL**: RLHF for helpfulness/safety and RL for reasoning are different applications of similar techniques with different objectives, failure modes, and evaluation criteria. Expertise in one does not transfer cleanly to the other.

---

## Implications

Reinforcement learning has permanently expanded the frontier of what language models can do. The reasoning capability it provides is real, measurable, and valuable. But it is important to hold two facts simultaneously: RL-trained models reason better than pre-training-only models, and the mechanism by which they reason is fundamentally different from human reasoning. This dual awareness — capability without anthropomorphism — is essential for deploying reasoning models appropriately.

The RL-primary paradigm is likely to intensify. As pre-training scaling approaches data and compute constraints, RL post-training provides a way to continue improving capability without proportional increases in pre-training cost. The next generation of frontier models will likely be distinguished more by their RL training recipes than by their pre-training scale.

---

## Source Provenance

| Source | Corpus ID | Content |
|--------|-----------|---------|
| ARC-AGI v3 interview (Chollet & Knoop) | `corpus/ai-models/01191.md` | Gradient descent 4-5 orders of magnitude less efficient than human learning; LLMs as memory component; efficient skill acquisition gap |
| Mark Chen interview (Core Memory) | `corpus/ai-models/09558.md` | Reasoning model breakthroughs; renewed pre-training focus; compute allocation across paradigms; AGI timeline speculation |
| Jerry Tworek interview (Core Memory) | `corpus/ai-models/10201.md` | Shift toward reasoning-driven models; beyond pre-training; homogeneity of labs; new architectures needed; RL as primary capability source |
