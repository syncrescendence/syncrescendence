# Prompt Optimization & Production Rigor

> A prompt is not text — it is a lifecycle: from intent formation through adversarial testing, Goldilocks calibration, and caching economics, prompts earn production status only when they survive systematic scrutiny and are maintained as first-class engineering artifacts.

## Source Provenance

| File | Contribution |
|------|-------------|
| `00084.md` | `think-critically` adversarial analysis skill; self-referential convergence testing; scorecard-stabilized iteration |
| `00087.md` | `cache_control: ephemeral` implementation; 90% cost reduction / 85% latency reduction; per-model minimum token thresholds |
| `01288.jsonl` | Goldilocks principle (over-specification vs. under-prompting); prompt slugs over instruction dumps; balanced control without suppressing model judgment |
| `01513.jsonl` | Multi-stage prompt lifecycle; intent formation as an overlooked first stage; LLM-assisted versioning and testing; tinkering vs. production-grade evaluation distinction; agent deployment necessitating rigorous tooling |
| `02101.jsonl` | 7 praxis hooks: clarity, contextual why, examples, positive framing (TO DO not NOT TO DO), directness, high-quality research injection, comprehensive documentation |

---

## The Lifecycle Frame

Prompting is not drafting text — it is operating within a lifecycle. Sources converge on the same structural claim: most practitioners skip stages, then wonder why prompts degrade in production. The lifecycle runs:

**1. Intent Formation** (01513.jsonl) — the most skipped stage. Before any tokens are written, the operator must crystallize what the prompt is FOR. Intent is not the same as task description. Intent encodes the success criterion, the failure mode, and the user's actual goal behind the stated request. A prompt written without a locked intent will drift during iteration toward locally pleasing outputs that miss the original need.

**2. Drafting with Goldilocks Balance** (01288.jsonl) — over-specification consumes context and suppresses model judgment; under-prompting forces the model to guess. The optimal zone provides just enough scaffold for the model to exercise its own competence. The practical form: short, reusable prompt slugs rather than exhaustive instruction dumps. A slug names the behavior and trusts the model; a dump names every step and produces mechanical execution with no inference.

**3. Adversarial Analysis via `think-critically`** (00084.md) — once a draft exists, run it through adversarial critique before deployment. The `think-critically` skill accepts a prompt and an expected output, then analyzes whether the prompt will reliably produce that output. The critical insight from self-referential testing: adversarial critics have a bias toward finding problems, so unchecked iteration diverges rather than converges. The fix is a running scorecard of mitigated issues. Each pass closes issues against the scorecard; convergence is reached when the scorecard shows no net new findings across successive runs. This is not perfection-seeking — it is stability detection.

**4. Production Evaluation vs. Tinkering** (01513.jsonl) — there is a categorical difference between exploratory tinkering and production-grade evaluation. Tinkering is informal, impression-based, and brittle. Production evaluation is systematic: versioned prompts, defined test cases, measurable output criteria, regression detection when the prompt changes. AI agent deployments and automated pipelines require the latter. The cost of treating production prompts like exploratory drafts is silent degradation — outputs drift, edge cases accumulate, and no one knows when the regression occurred.

**5. Cache Economics** (00087.md) — prompts with stable prefixes (system prompts, large context blocks, reference documents) should carry `"cache_control": {"type": "ephemeral"}` on the cacheable prefix. This yields up to 90% cost reduction on cached reads and 85% latency improvement. The operational constraint: minimum cacheable lengths are model-specific (4096 tokens for Opus 4.5 / Haiku 4.5; 1024 tokens for Sonnet 4.5, Sonnet 4, Opus 4.1, Opus 4). Prompts shorter than the threshold receive no benefit. Caching is not an optimization — at scale, it is a budget prerequisite.

**6. Lifecycle Maintenance** (01513.jsonl) — LLMs can assist in shaping, versioning, and testing high-leverage prompts. Prompt documentation (02101.jsonl) is not optional for production systems: it is what makes prompts transferable, auditable, and improvable by anyone other than the original author.

---

## The 7 Praxis Hooks

Sourced from 02101.jsonl — these are the tactical execution layer beneath the lifecycle:

1. **Clarity** — Ambiguous instructions produce ambiguous outputs. State the task with no interpretive slack.
2. **Contextual why** — Explain the purpose behind the request. The model's inference about intent shapes how it resolves ambiguities; a stated why locks that inference to the correct vector.
3. **Examples** — Exemplars are the highest-signal input. One concrete example outperforms three paragraphs of abstract description.
4. **Positive framing** — Frame as what TO DO, not what NOT TO DO. Negations require the model to compute the complement set; positive mandates are direct.
5. **Directness** — Concise prompts outperform verbose ones when the information density is equivalent. Padding is not clarification.
6. **Research injection** — For knowledge-intensive tasks, bring the information into the prompt rather than relying on the model's parametric knowledge. High-quality injected research consistently outperforms retrieval from weights.
7. **Documentation** — Comprehensive prompt documentation (purpose, version, test cases, known failure modes) enables consistency across runs and operators.

---

## Synthesis: The Three Axes

These five sources jointly describe prompt optimization along three axes:

| Axis | Failure Mode | Remedy |
|------|-------------|--------|
| **Calibration** | Over-specification or under-prompting | Goldilocks balance; slugs over dumps |
| **Validation** | No adversarial scrutiny before deployment | `think-critically` + scorecard convergence |
| **Economics** | Treating prompts as stateless ephemera | Cache prefixes; lifecycle maintenance; documentation |

The axes are interdependent. A perfectly calibrated prompt that was never adversarially tested will break on edge cases. A rigorously tested prompt without caching bleeds budget in high-volume deployment. A cached, tested prompt without documentation becomes a black box that no subsequent operator can safely modify.

---

## Antipatterns

- **Skipping intent formation**: Beginning with drafting before locking what success looks like. Produces locally coherent prompts that miss the actual goal.
- **Instruction dumps**: Long, exhaustive specification replacing Goldilocks calibration. Consumes context, suppresses model inference, and produces mechanical output.
- **Unchecked adversarial iteration**: Running `think-critically` (or equivalent) without a scorecard. The adversarial bias ensures the prompt never converges — each pass surfaces new issues against a moving target.
- **Tinkering as production evaluation**: Impression-based "it seems to work" substituting for versioned, measurable, regression-tracked evaluation. Silent degradation is the inevitable result.
- **Ignoring cache thresholds**: Applying `cache_control` to prompts below the model's minimum cacheable length. No benefit is realized; the cache marker is noise.
- **Undocumented production prompts**: Prompts without versioning, test cases, or failure mode documentation cannot be safely maintained by anyone other than the original author, and often not even by them after sufficient time.
- **Negative framing**: "Do not do X" instructions force complement-set inference and produce higher failure rates than equivalent positive mandates.

---

## The Lesson

A prompt that works once in exploration is not a production asset. Production status requires passing through the full lifecycle: intent locked before drafting, detail calibrated to the Goldilocks zone, adversarial analysis with scorecard-stabilized convergence, systematic evaluation distinct from tinkering, cache economics applied where token thresholds permit, and documentation sufficient for any operator to maintain and extend. These are not optional quality improvements — they are the difference between a prompt that works and a prompt that remains working.

---

## Obsolescence and Supersession

**"Prompting is just instructions" is the obsoleted view.** The pre-lifecycle framing of prompt engineering treated a prompt as a natural language instruction — you write what you want, the model produces it. This was adequate during the era of narrow task completion (GPT-3 era completions, BERT-era text classification), where prompts were short, tasks were narrow, and deployment was not agentic. The assumption embedded in this view: prompts are ephemeral, task-specific text strings, not engineering artifacts requiring versioning, testing, or lifecycle management.

The sources document what broke this assumption: agent deployments and production pipelines. When prompts drive autonomous systems that run unsupervised, the "write and hope" approach produces silent degradation — edge cases accumulate, the model's behavior drifts from intent, and no one knows when the regression occurred because no one defined "correct behavior" precisely enough to detect its absence. The lifecycle frame (01513.jsonl) explicitly identifies the moment of supersession: "AI agent deployments and automated pipelines" necessitate production-grade evaluation. The tool became high-stakes, and the casual approach became a liability.

**The "NOT TO DO" prompting assumption.** The sources establish (02101.jsonl) that negative framing — "do not do X" — produces higher failure rates than equivalent positive mandates. This supersedes the intuitive assumption that prohibition is a clean way to constrain model behavior. The failure mode: negations require the model to compute the complement set of the forbidden behavior, introducing inference steps that create edge cases the prohibition didn't anticipate. Positive framing ("do Y") bypasses this by specifying the target directly. The prior assumption (write prohibitions as natural language negations) is obsoleted by the empirical observation that positive mandates are more reliable.

**Cache economics as a recently emerged engineering constraint.** The `cache_control: ephemeral` mechanism with model-specific minimum token thresholds (4096 tokens for Opus 4.5/Haiku 4.5, 1024 for Sonnet 4.5/Sonnet 4/Opus 4.1/Opus 4) (00087.md) represents a newly emergent engineering concern that did not exist in earlier prompt engineering practice. When models were accessed primarily through chat interfaces with low request volumes, prompt caching was irrelevant. At production scale with stable system prompts, ignoring cache economics means paying full price on every request for tokens that haven't changed. The assumption that prompt cost is fixed per token is obsoleted by the infrastructure economics of high-volume agentic deployment.

**Audit note:** These sources are current (late 2025 / early 2026) and document the field's current state more than its history. The supersession chains above are constructed from what the sources identify as failure modes and corrections; the specific prior assumptions they supersede are inferred from context rather than explicitly historicized in the source material. This entry accurately represents what its sources contain.
