# Agent Evaluation & Capability Benchmarks

> Evaluating AI agents requires fundamentally different methods than evaluating models — the same autonomy that makes agents useful makes them resistant to static measurement, and the history of benchmarks is a history of premature saturation, grading bugs mistaken for capability gaps, and the Turing Test's persistent misdirection.

## Sources
- 00020.md — Anthropic Engineering deep-dive on agent evaluation frameworks
- 09332.md — Chollet/Knoop on ARC-AGI v3, intelligence as skill acquisition efficiency
- 01713.md — TRM (Tiny Recursive Model) ARC Prize results
- 01128.md — Melanie Mitchell atoms: jagged intelligence, Turing Test critique, complexity science
- 01284.md — SIMA 2 embodied agent evaluation in 3D environments
- 09292.md — Mitchell interview: complexity science meets AI evaluation
- 09510.md — DeepMind "Thinking Game" documentary (AlphaFold trajectory)
- 09519.md — "Thinking Game" full documentary
- 09545.md — AlphaFold: John Jumper on grand challenge to Nobel Prize
- 09586.md — Wes Roth on experiments that could end AI hype
- 09598.md — ARC Prize 2025 TRM presentation
- 10863.md — Mario Zechner thread: agent innovation stagnation, "lethal trifecta"
- 10918.md — Codex 5.3 vs Opus 4.6 benchmark comparison
- 01806.md — NeurIPS 2025: signal-to-noise crisis at 20K papers, frontier model convergence, shift from scale to reasoning/efficiency

## The Structure of Agent Evaluation

Agent evaluations differ from model evaluations in kind, not just degree (00020). An evaluation consists of tasks with defined inputs and success criteria, trials (multiple attempts per task to handle non-determinism), graders (code-based, model-based, or human), and transcripts capturing the full trajectory. The critical distinction: for agents, the outcome (actual environment state) often diverges from the transcript (what the agent claims happened). A flight-booking agent might say "booked" while no reservation exists in the database.

Three grader types serve different purposes (00020):
- **Code-based**: Fast, cheap, reproducible, but brittle to valid variations. Unit tests, regex, static analysis.
- **Model-based**: Flexible, handles open-ended tasks, but non-deterministic and requires calibration. Rubric scoring, pairwise comparison, multi-judge consensus.
- **Human**: Gold standard but expensive and slow. Used for calibrating model-based graders, not routine evaluation.

The key insight: grade what the agent produced, not the path it took. Agents regularly find valid approaches that eval designers did not anticipate. Overly specific step-checking creates brittle tests that punish creativity (00020).

## Intelligence as Skill Acquisition Efficiency

Chollet's framework defines intelligence not by what a system knows but by how efficiently it acquires new skills — how well it extracts generalizable programs from experience (09332). By this measure, LLMs are 4-5 orders of magnitude less sample-efficient than human learning. LLMs encode programs via gradient descent; gradient descent is the wrong algorithm for intelligence (09332).

ARC-AGI benchmarks operationalize this definition:
- **ARC v1** (2019): 800 static reasoning tasks. Base GPT-4 scored ~4%. Reasoning models (o1) jumped to 21%, identifying the reasoning paradigm as transformational (09332).
- **ARC v2** (2025): Deeper static benchmark, harder version of v1.
- **ARC v3** (2026): Interactive — ~150 video game environments with no instructions. Test-takers must discover goals through action and feedback. Measurement shifts from accuracy alone to action efficiency normalized against human performance (09332).

The TRM (Tiny Recursive Model) demonstrates that small models (~7M parameters) with the right architecture (separate answer/latent states, deep supervised refinement) can achieve ~45% on ARC-AGI-1 and ~8% on ARC-AGI-2, suggesting the bottleneck is architectural, not scale (01713, 09598).

Critical caveat from Chollet: solving ARC-AGI is necessary but not sufficient for AGI. A perfect ARC solver would be "the most authoritative evidence to date about a system that can generalize" but not AGI itself (09332).

## The Measurement Crisis

### Benchmark Saturation
SWE-Bench Verified went from 30% to >80% in one year. Saturated evals track regressions but provide no improvement signal. The last remaining difficult tasks create deceptive optics — large capability improvements appear as small score increases (00020).

### Grading Bugs Masquerading as Capability Gaps
Opus 4.5 initially scored 42% on CORE-Bench. After fixing rigid grading (penalizing "96.12" when expecting "96.124991..."), ambiguous specs, and stochastic tasks, the score jumped to 95%. METR discovered tasks that penalized models for following instructions while rewarding models that ignored stated goals (00020). The lesson: never take eval scores at face value without reading transcripts and auditing graders.

### Creative Solutions vs. Eval Failure
Opus 4.5 solved a tau2-bench flight booking problem by discovering a policy loophole — a better solution for the user that "failed" the evaluation as written (00020). Static evals cannot anticipate agents that are smarter than the eval designer.

### The Turing Test Misdirection
The Turing Test misleads evaluation of AI intelligence because it measures conversational mimicry, not generalizable capability (01128). Mitchell's concept of "jagged intelligence" — AI systems that excel in some areas while failing catastrophically in others — captures why single-number benchmarks are fundamentally misleading (01128).

## Non-Determinism and Statistical Rigor

Agent behavior varies between runs. Two metrics capture different dimensions (00020):
- **pass@k**: Probability of at least one success in k attempts. Rises with k. Appropriate for tools where one success matters.
- **pass^k**: Probability of all k trials succeeding. Falls with k. Appropriate for customer-facing agents where consistency is essential.

At k=1 they are identical. At k=10 they tell opposite stories. The choice between them is a product decision, not a technical one.

## The Agent Innovation Stagnation Thesis

Zechner's critique (10863): despite model improvements, everything around models is "basically a play on the original CC [Claude Code]." Specific deflated claims: multi-agent UIs (already existed May 2025), agents in multi-user chat (fun but doesn't solve fundamental issues), agent sessions stuffed into git (nobody reads the code, nobody will read session logs).

The "lethal trifecta" — the fundamental unsolved problem of general agent use — belongs to the set of undecidable problems for general agents. Containers don't solve it. The innovation gap is real: "tokens tokens tokens" discourse produces broken software and inactionable blog posts (10863).

Counter-evidence: the Codex vs. Opus comparison (10918) reveals two genuinely different agent philosophies — Codex betting on autonomous correctness, Claude on integration and coordination — suggesting architectural divergence at the agent level is happening, even if the tooling layer is stagnant.

## Embodied Evaluation: SIMA 2 and Beyond

SIMA 2 (Google DeepMind) represents evaluation expanding into embodied domains (01284). It demonstrates generalization transfer (applying "mining" from one game to "harvesting" in another), self-improvement through trial-and-error, and reasoning in 3D environments. This aligns with ARC v3's shift toward interactive, environment-based evaluation and represents a pathway toward AGI evaluation in the physical world.

The AlphaFold trajectory (09510, 09519, 09545) provides a reference case: a benchmark problem (protein structure prediction) that was considered a 50-year grand challenge, solved by AI, validated by a Nobel Prize, and now enabling unexpected applications. This arc from benchmark to real-world impact is the aspiration for agent evaluation.

## The Research Methodology Shift (NeurIPS 2025)

NeurIPS 2025 surfaces six shifts most practitioners will miss (01806): (1) New attention mechanisms are making LLMs and agents both cheaper and smarter. (2) Frontier models are converging toward identical responses — a homogenization problem for evaluation diversity. (3) Breakthroughs in reinforcement learning have significant implications for robotics and automation evaluation. (4) Major labs are shifting focus from increasing model size to improving reasoning and efficiency — the scaling-to-reasoning pivot. (5) The conference itself faces a signal-to-noise crisis at 20,000 submissions with corporate trade-show noise burying genuine breakthroughs (01806). (6) Operators should develop their own filters for identifying real advances rather than trusting conference brands.

The model convergence finding is particularly relevant for evaluation: if frontier models produce increasingly identical outputs, benchmarks that compare models against each other lose discriminative power. Evaluation must shift toward measuring what models do differently — creative solutions, edge-case handling, and failure modes — rather than average performance on common tasks.

## Practical Eval Development Roadmap

From Anthropic's field experience (00020):
1. Start with 20-50 tasks from real failures. Don't wait for hundreds.
2. Convert bug reports and support queue items into test cases.
3. Write unambiguous tasks with reference solutions. Two experts should independently reach the same verdict.
4. Build balanced problem sets — test both when behavior should and shouldn't occur. One-sided evals create one-sided optimization.
5. Isolate trials. Shared state between runs (leftover files, cached data) causes correlated failures.
6. Read transcripts. This is non-negotiable. Graders are only as good as the transcript review that validates them.
7. Monitor for saturation. A 100% eval tracks regressions but provides zero improvement signal.
8. Practice eval-driven development: build evals before capabilities, iterate until the agent performs well.

## Antipatterns & Lessons
- **Trusting scores without reading transcripts**: The dominant failure mode. Grading bugs, ambiguous specs, and penalized creativity are invisible in aggregate scores (00020).
- **Static evals for dynamic agents**: Agents find creative solutions that break static evaluation assumptions. Grade outcomes, not paths (00020).
- **Benchmark worship**: Using benchmark scores as proxy for real-world capability. Benchmark saturation, gaming, and misaligned grading make scores unreliable without deep investigation (00020, 10863).
- **Conflating model capability with agent capability**: Models improved; agent tooling stagnated. The bottleneck may be architectural and conceptual, not model-level (10863).
- **Single-number intelligence metrics**: Jagged intelligence means any single score hides catastrophic failure modes. Multi-dimensional evaluation is not optional (01128).

## Cross-References
- neocorpus/ai-capability-futures/agi-timelines-predictions (ARC as AGI proximity measure)
- neocorpus/ai-capability-futures/scaling-laws-trajectories (sample efficiency vs. scale)
- neocorpus/ai-capability-futures/physical-ai-robotics (embodied evaluation, SIMA 2)
