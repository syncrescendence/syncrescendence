# Model Capability Benchmarks

AI model capability benchmarks are standardized evaluation protocols that measure the performance of frontier models against defined tasks, scoring rubrics, and cost metrics. The major benchmarks — ARC-AGI, SWE-Bench, Arena Hard, LM Arena, MMLU — each capture a different facet of model capability, from abstract reasoning to real-world software engineering to open-ended conversational quality. But benchmarks are not neutral instruments. They encode assumptions about what intelligence is, they create optimization targets that distort development priorities, and they are increasingly gamed by labs that train specifically for benchmark performance. The cost-per-task axis, introduced by ARC-AGI-2, reframes evaluation from "what can the model do?" to "what can the model do per dollar?" — a question with direct engineering consequences. The "Move 37 moment" framing, borrowed from AlphaGo, captures the aspiration that AI will produce solutions so novel they redefine human understanding of the problem space.

---

## The Major Benchmarks

### ARC-AGI (Abstraction and Reasoning Corpus)

Created by Francois Chollet, ARC-AGI is designed to test genuine abstraction — the ability to discover novel patterns from minimal examples, rather than interpolating from massive training data. The benchmark has evolved through three versions:

- **ARC-AGI-1**: Passive pattern completion tasks. Models must identify transformation rules from a few input-output pairs and apply them to new inputs. Early LLMs struggled; by late 2025, frontier models achieved 80-90%+ with sufficient compute.
- **ARC-AGI-2**: Introduced the **cost-per-task axis**. Performance is plotted against the dollar cost of inference, creating a cost-performance frontier. Claude Opus 4.6 achieved state-of-the-art at 69.17% on ARC-AGI-2 at high effort, establishing a new cost/performance frontier. The innovation is forcing the evaluation to include economic efficiency, not just raw capability.
- **ARC-AGI-3** (announced): Adds goal discovery, temporal planning, and interactive learning. Moves beyond passive model-fitting toward evaluating whether a system can determine what the task IS, not just solve a presented task.

ARC-AGI's design philosophy is explicitly adversarial to scale-dependent approaches. Chollet's thesis: if a benchmark can be solved by memorizing more data, it does not test intelligence. ARC tasks are specifically designed to be outside any plausible training distribution.

### SWE-Bench

SWE-Bench evaluates models on real-world software engineering tasks: given a GitHub issue and a codebase, produce a patch that resolves the issue and passes the test suite. SWE-Bench Pro is the harder variant with more complex, multi-file changes.

- GPT-5.3 Codex demonstrated superior performance curves on SWE-Bench Pro, reaching approximately 60% accuracy while showing dramatically better token efficiency than GPT-5.2
- SWE-Bench is unusual among benchmarks in that its tasks are drawn from real open-source projects, providing ecological validity that synthetic benchmarks lack
- The benchmark directly measures agentic coding capability — the model must understand the codebase, diagnose the issue, and produce working code

### LM Arena (Chatbot Arena)

LM Arena uses pairwise human preference judgments: two models answer the same prompt, human evaluators choose which response they prefer, and an Elo rating system ranks models. This is the closest benchmark to "what do users actually prefer?"

- Gemini 3.0 Pro held the top LM Arena position in late 2025, triggering OpenAI's "Code Red" response
- LM Arena measures conversational quality, helpfulness, and overall response preference — different from task-specific benchmarks
- The Elo system creates a single ranking that is easy to communicate but collapses multi-dimensional performance into one number

### MMLU (Massive Multitask Language Understanding)

MMLU tests knowledge and reasoning across 57 academic subjects. It was the canonical benchmark for early frontier model comparisons but has been increasingly criticized as models approach high performance levels and as its multiple-choice format may fail to distinguish genuine understanding from pattern matching. [MMLU saturation characterization and methodological critique are synthesis beyond cited sources]

### Arena Hard

Arena Hard is a derivative of LM Arena that uses a fixed set of challenging prompts evaluated by a strong model judge rather than human evaluators. It provides faster, cheaper evaluation at the cost of being one step removed from actual human preferences. [Arena Hard methodology detail is synthesis beyond cited sources]

---

## The Cost-Per-Task Revolution

ARC-AGI-2's introduction of the cost-per-task axis represents a fundamental shift in benchmark design. Prior benchmarks asked: "What score does the model achieve?" Cost-aware benchmarks ask: "What score does the model achieve for what price?"

This reframing has immediate engineering consequences:

- A model that achieves 60% accuracy at $0.50 per task may be more valuable than one achieving 70% accuracy at $50 per task, depending on the deployment context
- Token efficiency becomes a first-class metric — GPT-5.3 Codex's improved token efficiency means better benchmark performance at lower cost, which Noam Brown identified as "the biggest story" of the release
- The cost-performance frontier creates a Pareto surface where different models are optimal for different budget constraints

The scatter plot format used in ARC-AGI-2 reporting — score on the y-axis, cost-per-task on the x-axis, multiple effort levels per model — provides a richer picture than a single leaderboard number.

---

## The "Move 37 Moment" Framing

In competitive coding and mathematics, AI models have begun producing solutions that surprise human experts — not just correct answers but novel approaches that redefine understanding of the problem. Mark Chen's reference to the "Move 37 moment" invokes AlphaGo's game 2 against Lee Sedol, where move 37 was so unexpected that commentators initially thought it was a mistake, only to realize it reflected a deeper understanding of the position.

The aspiration embedded in this framing: that AI models will not merely match human performance on defined tasks but will produce insights that expand the frontier of human knowledge. Chen's description of GPT-5 Pro making "scientific discoveries" reflects this aspiration, though the distinction between genuine discovery and sophisticated interpolation from training data remains contested.

---

## Key Insights

### Benchmark Saturation and Successor Design

As frontier models approach ceiling performance on existing benchmarks, the benchmark community must design harder tasks. ARC-AGI-1 became tractable, yielding ARC-AGI-2 and the planned ARC-AGI-3. Each successor benchmark must resist the specific strategies that cracked its predecessor while remaining valid as a measure of the capability it claims to test. The broader pattern — where saturation on one benchmark drives successor design (e.g., MMLU yielding MMLU-Pro) — is a widely observed dynamic, though specific successor examples beyond the ARC series are synthesis beyond cited sources. [synthesis beyond cited sources]

### The Sample Efficiency Critique

Chollet's persistent critique: gradient descent is 4-5 orders of magnitude less sample-efficient than human learning. An LLM that requires millions of examples to learn a pattern that a human learns from three examples has not achieved intelligence — it has achieved memorization at scale. This critique does not deny that LLMs are useful, but it challenges the inference from "high benchmark scores" to "general intelligence."

LLMs may function as a component of AGI — serving as the memory and knowledge representation layer — while lacking the efficient skill acquisition that characterizes general intelligence. The benchmark implications: tasks that can be solved via massive memorization do not test what we think they test.

### Every Lab Can Lead on Something

The proliferation of benchmarks means competitive advantage is always qualified. Opus 4.6 leads on ARC-AGI-2. GPT-5.3 leads on SWE-Bench Pro token efficiency. Gemini 3.0 leads on LM Arena Elo. Each lab selects the benchmarks that favor its model for marketing materials. Sophisticated evaluation requires examining the full benchmark profile, not any single number.

---

## Anti-Patterns

- **Benchmark monoculture**: Optimizing for a single benchmark distorts development priorities. Models trained to maximize MMLU may sacrifice the open-ended reasoning that LM Arena captures, and vice versa.
- **Confusing benchmark scores with deployment value**: A model's benchmark profile predicts its utility for specific tasks, but deployment value depends on latency, cost, context length, tool integration, and reliability — none of which most benchmarks measure.
- **Ignoring cost**: Reporting accuracy without cost is incomplete. The same accuracy at 10x lower cost is a fundamentally different product.
- **Treating saturated benchmarks as discriminating**: When multiple models score 90%+ on MMLU, the remaining 10% may reflect noise, training data overlap, or prompt formatting sensitivity rather than genuine capability differences.
- **Anthropomorphizing benchmark performance**: High scores on reasoning benchmarks do not imply the model "reasons" in the way humans do. The mechanism may be entirely different while producing the same outputs.

---

## Implications

Benchmark design is a form of intelligence theory. Choosing what to measure is choosing what to value. ARC-AGI's emphasis on abstraction from minimal examples reflects Chollet's theory that intelligence is the ability to handle novelty efficiently. SWE-Bench's emphasis on real codebases reflects the theory that intelligence manifests in practical problem-solving. LM Arena's emphasis on human preference reflects the theory that intelligence is whatever humans find useful. These are not compatible definitions, and the benchmark a practitioner prioritizes reveals their implicit theory of what AI should do.

The cost-per-task axis may be the most consequential innovation in recent benchmark design. It aligns evaluation with deployment economics and forces the field to take efficiency seriously as a dimension of capability, not merely a deployment constraint.

---

## Source Provenance

| Source | Corpus ID | Content |
|--------|-----------|---------|
| "GPT-5.3 Codex and Opus 4.6: An Unexpected Breakthrough" | `corpus/ai-models/00157.md` | ARC-AGI-2 scatter plots; cost-per-task frontier; Opus 4.6 SOTA; SWE-Bench Pro curves; Noam Brown token efficiency quote |
| Extraction: GPT-5.1 improvements | `corpus/ai-models/01332.md` | GPT-5.1 benchmark improvements in task accuracy, strategic decision-making, planning |
| Gemini 3 Pro overview | `corpus/ai-models/09456.md` | LM Arena positioning; Gemini 3 Pro benchmarks |
| ARC-AGI v3 interview (Chollet & Knoop) | `corpus/ai-models/01191.md` | ARC-AGI v3 design; gradient descent sample inefficiency; LLMs as memory component; goal discovery and temporal planning |
| Mark Chen interview (Core Memory) | `corpus/ai-models/09558.md` | "Move 37 moment" framing; competitive coding AI; scientific discoveries; is scaling dead debate |
