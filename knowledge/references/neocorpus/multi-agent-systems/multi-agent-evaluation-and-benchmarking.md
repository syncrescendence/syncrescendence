# Multi-Agent Evaluation and Benchmarking

**Nucleosynthesis Date**: 2026-03-02
**Synthesized By**: Commander (Claude Opus 4.6)
**Protocol**: CRUSH — lossless compression of corpus wisdom

---

## Sources

| ID | File | Content |
|----|------|---------|
| 00176 | `corpus/multi-agent-systems/00176.md` | Agentic reasoning survey — 41-86.7% MAS failure rates, 1,642 execution traces, 14 failure modes |
| 11041 | `corpus/multi-agent-systems/11041.md` | AdaptOrch — orchestration topology as optimization target, 12-23% improvement over static baselines |
| 00413 | `corpus/multi-agent-systems/00413.md` | Ontology Annealment v2.0 — entity taxonomy, metric types, quality tier systems |

---

## Definitive Treatment

### The Evaluation Gap

Multi-agent systems fail at rates between 41% and 86.7% in production deployment. This finding — from Berkeley researchers analyzing 1,642 execution traces across seven state-of-the-art frameworks — represents the single most important number in the field that almost nobody cites. A 29-author, 74-page survey from Meta, Amazon, and DeepMind on "agentic reasoning" organized the taxonomy beautifully and did not mention it.

The gap between benchmark performance and production reliability is not a measurement error. It is a category error. Single-agent benchmarks (MMLU, HumanEval, SWE-bench) measure whether a model can produce a correct output given a well-formed input. Multi-agent evaluation must measure whether a *system* of models can coordinate to produce a correct output given ambiguous, distributed, temporally extended inputs — while managing failures, retries, cost, and latency across the coordination surface.

These are fundamentally different evaluation problems. Treating them as the same — extrapolating from single-agent scores to multi-agent capability — is the field's dominant methodological error.

---

### What Standard Benchmarks Miss

#### Coordination Overhead

Every inter-agent message consumes tokens, adds latency, and introduces a failure point. A hierarchical system where a planner dispatches to three specialists incurs coordination costs that a monolithic agent does not. Benchmarks that measure only final output quality ignore the overhead that makes the output possible — or impossible.

The AdaptOrch framework (11041) quantifies this directly: orchestration topology selection yields 12-23% improvement over static baselines *using identical underlying models*. The models did not change. The coordination architecture changed. This means evaluation frameworks that hold architecture fixed and vary models are measuring the wrong variable.

#### Consistency vs. Accuracy

An agent achieving 60% pass@1 may exhibit only 25% consistency across multiple trials. This distinction — between getting the right answer sometimes and getting the right answer reliably — disappears in standard benchmarks that report single-trial accuracy.

For multi-agent systems, inconsistency compounds. If Agent A produces correct output 60% of the time and Agent B depends on A's output, the system's theoretical ceiling (assuming perfect downstream processing) is already 60%. In practice, it is lower, because B's reasoning over A's incorrect output does not merely fail — it fails in ways that appear plausible and resist detection.

#### Failure Mode Taxonomy

The Berkeley trace analysis identified 14 unique failure modes. Most were system design and coordination issues, not individual model failures. The following failure-mode labels synthesize from the survey's reported categories; the specific terminology used here is the entry author's characterization:

1. **Cascading misinterpretation**: Agent B misreads Agent A's output, producing confidently wrong downstream reasoning
2. **Coordination deadlock**: Agents wait on each other or duplicate work without detection
3. **Role confusion**: Agents in role-based systems drift from their assigned functions
4. **Partial completion**: The system produces some correct outputs and silently drops others
5. **Cost explosion**: Retry loops and verbose inter-agent communication exhaust budgets before task completion

None of these modes are captured by pass/fail benchmarks on individual tasks. They emerge from interaction patterns that only exist when multiple agents coordinate.

---

### Dimensions of Multi-Agent Evaluation

A rigorous MAS evaluation framework must measure along dimensions that single-agent benchmarks ignore entirely:

#### Task Completion Latency

Wall-clock time from task dispatch to verified completion. This includes:
- Agent initialization and context loading
- Inter-agent communication round-trips
- Retry cycles after failures
- Human-in-the-loop relay delays (if applicable)
- Verification and quality-check overhead

Latency varies by topology. Parallel architectures reduce latency at the cost of coordination complexity. Sequential architectures simplify coordination at the cost of serial bottlenecks. Hierarchical architectures introduce planner overhead but enable adaptive task decomposition. The AdaptOrch finding — that topology selection itself is a first-class optimization target — means latency benchmarks must be topology-aware.

#### Cost Per Success

Total resource expenditure (tokens consumed, API calls made, compute time) divided by the number of successfully completed tasks. This is the production-relevant metric that vanity benchmarks avoid.

Cost per success exposes hidden failure modes. A system with 90% accuracy but 50% retry rate on failures has a dramatically different cost profile than a system with 85% accuracy and 5% retry rate. The first system may cost 3x more per success despite appearing superior on accuracy alone.

#### Failure Rate and Failure Distribution

Not just "how often does it fail" but "how does it fail, and who detects it?" Silent failures — tasks the system reports as complete but that contain errors — are categorically worse than loud failures that trigger retry or escalation.

The 41-86.7% failure range across frameworks suggests that failure rate is highly sensitive to framework design choices. This sensitivity is itself a finding: the evaluation must decompose failure rate by failure mode to be actionable. A framework with 50% failure rate concentrated in coordination deadlocks has a different improvement path than one with 50% failure rate concentrated in cascading misinterpretation.

#### Execution Trace Analysis

The most information-dense evaluation artifact is the execution trace: the complete record of what each agent did, in what order, with what inputs and outputs. Trace analysis reveals:

- **Bottleneck identification**: Which agent or communication link is the throughput constraint
- **Waste detection**: Redundant computation, circular communication, abandoned work
- **Failure causation**: The causal chain from initial trigger to eventual failure
- **Topology efficiency**: Whether the actual execution pattern matches the intended topology

Production systems generate traces as operational artifacts. The Syncrescendence constellation's task dispatch system (TASK/CONFIRM/RESULT directives with exit codes, lease IDs, and execution logs) is an execution trace infrastructure — every agent interaction produces a reviewable record with status, timing, and failure classification.

---

### The Topology Evaluation Problem

The AdaptOrch framework formalizes what production experience teaches informally: the choice of orchestration topology (parallel, sequential, hierarchical, hybrid) is a first-class variable that affects performance as much as model selection.

This creates an evaluation challenge. Comparing two MAS requires controlling for topology, but the optimal topology varies by task. A benchmark that fixes topology measures model performance within that topology, not system performance across the task distribution. A benchmark that allows topology variation measures system design skill, not model capability.

The resolution is **task-adaptive evaluation**: benchmark suites that include tasks with different dependency structures, measure performance across topology choices, and report both best-case (optimal topology selected) and average-case (uniform topology distribution) scores. The 12-23% improvement that AdaptOrch achieves over static baselines is the measured cost of topology mismatch — the performance left on the table by systems that do not adapt their coordination architecture to the task.

---

### Quality Tiers and Metric Types

Evaluation metrics must themselves be typed. The Ontology Annealment framework (00413) distinguishes metric types relevant to MAS evaluation:

- **Integration Coherence**: Do the outputs of multiple agents form a coherent whole, or do they contain internal contradictions?
- **Omni-Quality Dimensions**: Breadth metrics that assess coverage across the full task space, not just cherry-picked examples
- **Quality Tier classification**: Stratifying outputs into tiers (correct, partially correct, plausibly wrong, obviously wrong) rather than binary pass/fail

Binary evaluation (correct/incorrect) is maximally lossy. Tiered evaluation preserves the distribution shape that tells you whether the system is close to correct (and improvable with minor tuning) or fundamentally misarchitected.

---

### Obsolescence and Supersession

#### Single-Agent Benchmarks Applied to Multi-Agent Systems

The first-generation approach to evaluating multi-agent systems was to benchmark the individual agents within them using standard single-agent metrics: MMLU, HumanEval, SWE-bench, GPQA. The implicit assumption: if the components are good, the system will be good. The system-level evaluation was treated as an afterthought — "the parts work, so the whole should work."

The Berkeley 1,642-trace analysis supersedes this with a direct refutation: 41-86.7% of multi-agent systems fail in production regardless of the component models' benchmark scores. The failure modes identified — cascading context loss, coordination breakdown, tool auth failure, rate limit saturation, sandbox collision — are not measurable by any single-agent benchmark. They emerge from coordination, and they require coordination-level evaluation to detect.

The supersession is clear: single-agent benchmarks are necessary but not sufficient for multi-agent evaluation. They tell you the floor of system performance (a low-scoring component will degrade the system); they tell you nothing about the ceiling (a high-scoring component may still fail catastrophically in the coordination layer).

#### Pass@1 as the Evaluation Standard

A specific supersession: the field's reliance on pass@1 as the canonical evaluation metric. Pass@1 measures whether the system ever produces a correct answer on a given task. It dominated early agent evaluation because it was easy to measure and correlated with useful properties in single-agent systems.

The consistency gap — 60% pass@1 / 25% consistency across trials — reveals that pass@1 measures something orthogonal to reliability. A system that produces a correct answer 60% of the time but an incorrect answer 75% of the time is not reliable; it is unpredictable. For production deployments where users depend on consistent behavior, consistency is more important than peak accuracy.

The multi-agent evaluation framework prescribed here — measuring consistency distributions, cost per success, failure mode distribution, and execution trace quality — represents the successor standard to pass@1-dominated evaluation.

---

### Anti-Patterns

**Extrapolating from single-agent benchmarks.** A model that scores 90% on SWE-bench solo tells you nothing about its performance as one node in a five-agent pipeline. Coordination overhead, message formatting sensitivity, and role adherence are invisible to single-agent evaluation.

**Reporting accuracy without cost.** A system that achieves 95% accuracy at $50 per task and one that achieves 90% at $2 per task serve different use cases. Reporting accuracy alone is misleading for production evaluation.

**Ignoring silent failures.** Systems that report success while delivering incorrect results are worse than systems that fail loudly. Evaluation must include verification passes that check output correctness independently of the system's self-report.

**Benchmarking on single topologies.** Static benchmarks that fix the coordination architecture measure a narrow slice of system capability. Topology-adaptive evaluation reveals the system's actual performance envelope.

**Averaging over failure modes.** A 50% failure rate tells you nothing actionable. A 50% failure rate decomposed into 30% coordination deadlock, 15% cascading misinterpretation, and 5% cost explosion tells you exactly what to fix.

**Trusting single-trial results.** Consistency across trials is as important as peak performance. Report distributions, not point estimates.

---

### Implications

The evaluation gap has practical consequences for every team building multi-agent systems:

1. **Internal benchmarks are mandatory.** Public benchmarks do not measure what matters for your system. Build task suites that reflect your actual workload and measure the dimensions that affect your production outcomes.

2. **Execution traces are the primary evaluation artifact.** Not accuracy numbers — traces. Every deployment should produce reviewable traces that enable failure mode decomposition.

3. **Cost accounting must be first-class.** Token consumption, API calls, retry counts, and wall-clock time are not operational details — they are evaluation metrics on par with accuracy.

4. **Topology is a variable, not a constant.** If your evaluation holds coordination architecture fixed, you are measuring the wrong thing. The AdaptOrch finding (12-23% improvement from topology selection alone) means architecture choice is a larger lever than most model upgrades.

5. **The 41-86.7% failure rate is the baseline to beat.** Any MAS deployment that does not measure and report its failure rate is operating blind. The Berkeley finding is not a warning about multi-agent systems — it is the current state of the art. Improvement requires measurement, and measurement requires evaluation frameworks designed for coordination, not individual performance.

---

## Syncrescendence Operational Context

The following claims derive from the constellation's operational history and constitutional documents (AGENTS.md, CLAUDE.md, memory/), not from external corpus sources:
- TASK/CONFIRM/RESULT traces as execution trace infrastructure with exit codes, lease IDs, and execution logs
- The Syncrescendence constellation's task dispatch system as an instance of execution trace architecture

---

## Provenance

This entry synthesizes the agentic reasoning survey critique (00176, citing Berkeley's 1,642-trace analysis), the AdaptOrch topology optimization framework (11041), and the Ontology Annealment metric taxonomy (00413). The 41-86.7% failure rate statistic originates from the Berkeley multi-agent failure analysis paper cited in 00176. The coordination topology findings originate from AdaptOrch (arxiv.org/abs/2602.16873). Operational trace experience draws from Syncrescendence constellation dispatch records (TASK/CONFIRM/RESULT artifacts in corpus/multi-agent-systems/).
