# AGI Definition and Measurement

## Definition

Artificial General Intelligence (AGI) remains the most contested concept in AI. The term is used to mean everything from "human-level performance on benchmarks" to "autonomous scientific discovery" to "the last invention humanity will need to make." The ARC-AGI benchmark, created by Francois Chollet, represents the most rigorous attempt to operationalize AGI measurement through the lens of sample efficiency and novel problem-solving rather than accumulated knowledge. The core argument: LLMs are not AGI because they are 4-5 orders of magnitude less sample-efficient than human learning. They memorize; they do not generalize.

This debate is not academic. AGI timelines drive billions in capital allocation, shape regulatory policy, and determine whether AI labs are building tools or building minds.

---

## Core Principles

### 1. Chollet's Sample Efficiency Argument

The foundational claim of the ARC-AGI research program is that intelligence should be measured by the efficiency of skill acquisition, not by the breadth of skills already acquired. A human child can learn a new visual pattern from 2-3 examples. An LLM requires millions of training examples to acquire comparable capability — gradient descent is 4-5 orders of magnitude less sample-efficient than human learning.

By this definition, current LLMs are not intelligent — they are extraordinarily well-memorized. They have encoded vast numbers of programs via gradient descent, but they have not acquired the ability to rapidly learn new programs from minimal data. This is the difference between a library and a mind: the library contains more information, but the mind can learn new things the library never contained.

### 2. LLMs as Memory, Not General Intelligence

Chollet's framework positions LLMs as a potential component of AGI — specifically, the memory and knowledge representation layer — but not AGI itself. An AGI system would need an efficient skill acquisition mechanism (something other than gradient descent) that could leverage LLM-stored knowledge as a foundation. The LLM is the knowledge base; the missing piece is the learning algorithm that can use that knowledge base to rapidly master novel domains.

This is a structurally different claim from "LLMs are useless" or "LLMs are AGI." It is the nuanced middle position: LLMs are a necessary but insufficient component, and the field's obsession with scaling LLMs is optimizing the wrong variable.

### 3. ARC-AGI Benchmark Evolution

The ARC-AGI benchmark has evolved through three versions:
- **v1**: Pattern completion tasks requiring novel spatial reasoning. Models must infer transformation rules from 2-3 examples.
- **v2**: Harder variants with more complex rules and less obvious patterns. Both accuracy and inference cost are tracked — the evaluation surface expands beyond raw accuracy alone.
- **v3**: Adds goal discovery, temporal planning, and interactive learning. The model must not only solve puzzles but figure out what the puzzle IS and adapt its strategy over time.

Each version raises the bar on what counts as "general" by adding cognitive capabilities that pure memorization cannot fake. v3 in particular targets the learning-to-learn capability that Chollet argues is the essence of intelligence.

### 4. The Self-Improving Model Complication

OpenAI's announcement that GPT-5.3-Codex was "instrumental in creating itself" — and the broader trend of models contributing to their own development — complicates Chollet's framework (source: `corpus/ai-models/00157.md`). If a model can debug its own training, diagnose evaluation failures, and accelerate its own development, is it "merely memorizing"? The ARC-AGI definition says yes — the model is applying memorized programming knowledge, not learning a fundamentally new skill. But the practical impact of self-improving models may render the theoretical distinction moot if capability growth accelerates regardless of mechanism.

---

## Key Insights

### The Benchmark Paradox

Every AGI benchmark eventually gets solved by systems that are not AGI by anyone's definition. ARC-AGI v1 scores have climbed from single digits to high levels with frontier models at high effort (source: `corpus/ai-models/00157.md`). This does not mean those models are AGI — it means the benchmark has been partially reduced to a compute-scaling problem. v2 and v3 attempt to stay ahead of this curve, but the arms race between benchmark designers and model trainers has no natural endpoint.

The paradox: if a benchmark can be solved, it was not measuring AGI. If it cannot be solved, it is not useful as a benchmark. Chollet's response is that the cost-performance frontier (accuracy per dollar) is the real metric, not raw accuracy alone.

### Timeline Compression

AGI timeline estimates have compressed dramatically. Mark Chen (OpenAI CRO) discusses "automating research within 2 years." Jerry Tworek (ex-OpenAI researcher) views current timelines more skeptically, noting "the sad homogeneity of current AI labs" — all converging on the same ideas, which means the same blind spots. Tworek's bet is on new architectures and continual learning as the path beyond current scaling limits.

The compression is driven by the self-improvement feedback loop: better models build better models faster. Whether this constitutes AGI or merely rapid capability improvement depends entirely on which definition you adopt.

### Gradient Descent as the Wrong Algorithm

Chollet's most provocative claim is that "gradient descent is the wrong algorithm for intelligence." Intelligence requires rapid adaptation from minimal data. Gradient descent requires massive data and compute to learn anything. No amount of scaling gradient descent will produce the sample efficiency that characterizes human intelligence.

This claim is testable: if future systems achieve human-level sample efficiency while still relying on gradient descent (perhaps through better architectures, meta-learning, or in-context learning improvements), Chollet's thesis is falsified. If they achieve it only through fundamentally different learning algorithms, his thesis is vindicated.

### The Operational Irrelevance of the Definition

For practitioners, the AGI definition debate may be operationally irrelevant. Whether Opus 4.6 is "truly intelligent" or "merely memorizing very well" does not change its utility for coding, analysis, orchestration, and creative work. The capability is real regardless of the philosophical classification. The AGI debate matters for research direction (where to invest), regulation (what to control), and existential risk assessment (what to fear) — but not for the daily work of deploying AI systems. [synthesis beyond cited sources — the "operationally irrelevant" framing and incentive-driven-timelines interpretation are the entry's synthesis, not stated explicitly in the source set]

---

## Anti-Patterns

### Declaring AGI Based on Benchmark Scores
Achieving high scores on any benchmark, including ARC-AGI, does not constitute AGI. Benchmarks measure specific capabilities; AGI is a claim about generality. Conflating the two is the most common error in AI discourse.

### Dismissing LLMs Because They Are "Not AGI"
The fact that LLMs may not be AGI by Chollet's definition does not diminish their practical utility. Dismissing useful capabilities because they do not meet a theoretical threshold is intellectual vanity with operational consequences.

### Treating AGI as Binary
AGI is not a threshold to be crossed but a spectrum to be explored. Models become more general incrementally. The question "is this AGI?" is less useful than "how general is this system, and for what tasks?"

### Ignoring the Economic Incentives
AGI timeline claims are made by people and organizations with financial interests in those claims. OpenAI saying "AGI in 2 years" raises funding. Chollet saying "LLMs are not AGI" funds ARC-AGI research. Neither is disinterested. Evaluate claims against evidence, not authority.

---

## Implications

The AGI definition debate will not be resolved by argument — it will be resolved by capability. As models become more capable, the definition of AGI will either stretch to include them (rendering the term meaningless) or narrow to exclude them (rendering the term perpetually aspirational). Either way, the practical work of deploying AI systems continues regardless.

The architectural takeaway from Chollet's framework is that multi-model orchestration systems — where an outer coordination layer provides learning, adaptation, and strategic continuity across context windows — may point toward how AGI-level capability could emerge from composition of specialized components, rather than from any single model. Whether such compositions constitute a meaningful step toward AGI depends entirely on which definition of AGI one adopts. [synthesis beyond cited sources]

---

## Source Provenance

| Source | File | Content |
|--------|------|---------|
| ARC-AGI v3 discussion — Chollet + Knoop | `corpus/ai-models/01191.md` | Sample efficiency argument, LLMs as memory, gradient descent critique, v3 benchmark design |
| Mark Chen (OpenAI CRO) — Core Memory podcast | `corpus/ai-models/09558.md` | AGI timelines, research prioritization, self-improving models, compute allocation |
| Jerry Tworek (ex-OpenAI) — Core Memory podcast | `corpus/ai-models/10201.md` | Lab homogeneity critique, new architectures, continual learning, skeptical timeline |
| GPT-5.3 Codex and Opus 4.6 release analysis | `corpus/ai-models/00157.md` | Self-improving model claims; ARC-AGI v1 high-effort frontier scores |

---

*Compendium entry 13 of 21 -- ai-models*
*Crystallized: 2026-03-02*
