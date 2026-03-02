# Scaling Laws & Capability Trajectories

> The AI field is transitioning from the "age of scaling" (more compute = better models) to the "age of research" (novel architectures, RL, and efficiency breakthroughs) — where the clean reward signal thesis explains why code/math work and open-ended tasks don't, and inference compute emerges as the true bottleneck.

## Sources
- 08442.md — Sholto Douglas & Trenton Bricken "Is RL + LLMs Enough for AGI?": two axes of capability, clean reward signal thesis, neuralese, THAT/WHY gap, inference bottleneck, LLMs as "baby AGI"
- 01539.md — Ilya Sutskever: transition from age of scaling to age of research
- 02091.md — Dwarkesh Patel "What Are We Scaling?": RL scaling misguided if near human-like learners, models lack on-the-job learning, economic impact lags capability benchmarks, AGI goalposts shifting
- 01377.md — AI costs plummeting 40x: Anthropic vs OpenAI comparisons, cost collapse dynamics
- 01506.md — Post-transformer architecture: Continuous Thought Machines
- 01752.md — Pedro Domingos: Tensor Logic unifies AI paradigms
- 01806.md — NeurIPS 2025: 6 shifts most people will miss
- 01887.md — Yi Ma: mathematical foundations of intelligence
- 02205.md — State of RL Reasoning: IMO/IOI gold, o3, GPT-5 trajectory
- 02211.md — Terry Tao: "LLMs are simpler than you think"
- 02181.md — In-context learning mechanism explained
- 01194.md — "Life Emerges from Code": 135 atoms on intelligence, abiogenesis, DNA stability
- 01263.md — "Built an AGI Lab in 8 Months": trillion-parameter model timelines
- 01287.md — Gemini 3.0 stealth release performance
- 01485.md — Gemini 3 capability claims
- 01537.jsonl — Sutskever atoms on scaling transition
- 01626.md — Michael Levin: biological intelligence, multi-scale cognition
- 01656.md — Fluid Intelligence: AI for scientific simulation
- 01863.md — GPT-5.2 arrival and market impact
- 01981.jsonl — Luma Ray3 video model atoms
- 02007.md — Michael Levin: life and intelligence relationship
- 02109.md — MiniMax M2.1 open model milestone
- 02550.md — Labs agree on infrastructure priorities
- 02751.md — Brain metaphor history (MLST)
- 03012.md — "Apple Took Years, Kilo Code Took 6 Weeks": AI development speed
- 03273.md — Kimi K2.5 Agent Swarm capability
- 03832.jsonl — AI architecture fundamentals atoms
- 04117.jsonl — Mathematical intelligence atoms
- 04197.md — "What if Intelligence Was There From the Start?"
- 04200.md — "A Guide to Which AI": model capability comparison
- 04251.md — "AI Is Scaling Fast, Should You Be Worried?"
- 09361.md — Probabilistic circuits and AI energy crisis
- 09381.md — Jensen Huang at Cambridge Union: physical AI trajectory
- 09439.md — Cost collapse and capability democratization
- 09526.md — Sutskever interview on scaling paradigm shift
- 09692.md — Why AI advantage compounds
- 09715.md — "OpenAI Is Hiding the Truth": transparency critique
- 10056.md — Technology threat to TSMC/ASML
- 10099.md — Google AI integration depth
- 10153.md — "Craziest Experiment Humans Have Ever Built": frontier training scale
- 10814.md — Gemini 3 Deep Think hands-on
- 10902.md — Karpathy: LLMs as translation engines, rewriting all software

## Two Axes of AI Capability

The capability frontier maps to two independent axes (08442):
1. **Intellectual complexity**: How hard is the task? Current peaks achieved in competitive programming, mathematics.
2. **Time horizon**: How long must the agent sustain coherent effort? Not yet demonstrated for long-running agentic tasks.

Current models are strong on the first axis but weak on the second. This explains the gap between impressive benchmarks and modest real-world economic impact — benchmarks test complexity, the economy tests sustained effort (08442, 02091).

## The Clean Reward Signal Thesis

"If you can give it a good feedback loop for the thing that you want it to do, then it's pretty good at it. If you can't, they struggle" (08442).

This explains:
- **Why code/math work**: Verifiable answers provide clean reward signals
- **Why open-ended tasks struggle**: No clean signal for creative judgment, nuanced reasoning
- **The path forward**: Expanding the domain of tasks with good signals

RL achieves gold at IMO and IOI competitions (02205). But current RL scaling approaches may be "fundamentally misguided if humanity is close to developing human-like learners" (02091). Human workers are valuable precisely because they do NOT require bespoke training loops for every small task. Models currently lack on-the-job learning — which explains why economic impact lags capability benchmarks (02091).

## The Scaling-to-Research Transition

Ilya Sutskever declares the field is transitioning from the "age of scaling" to the "age of research" (01539, 09526). The implications:
- More compute alone no longer guarantees proportional capability gains
- Novel architectures, training methods, and inference strategies become the differentiators
- Research breakthroughs (not capex) will drive the next generation of capability jumps

Post-transformer architectures are emerging: Continuous Thought Machines (01506), Tensor Logic unifying AI paradigms (01752), probabilistic circuits for energy efficiency (09361). The mathematical foundations of intelligence are being formalized (01887, 04117, 04197).

## Neuralese and the Interpretability Gap

Models may develop their own internal language ("neuralese") optimized for how they compute, not for how humans read (08442). Implication: human-language interpretability may fundamentally miss model cognition — like transcribing whale clicks into English.

The THAT/WHY gap (08442):
- We can identify THAT the model is computing something
- We can trace information flow
- We CANNOT explain WHY it chose that particular computation over alternatives

This is not a temporary engineering limitation — it may be structural. If models think in neuralese, full interpretability through human-language probes may be impossible in principle.

## The Inference Bottleneck

"Inference compute is much harder to scale than training compute" (08442). Training: throw more compute, get better models. Inference: real-time, can't batch the same way, requires different infrastructure. This may bottleneck AGI deployment more than capability development — models could be AGI-capable in training but undeployable at scale due to inference costs.

## Cost Collapse Dynamics

AI costs are plummeting ~40x (01377, 09439). This democratizes capability rapidly — what required frontier lab resources becomes available to startups and individuals within months. The cost curve explains why open-source models catch up so quickly (cross-ref democratization entry) and why the SaaSpocalypse hits enterprise software.

"Apple took years to catch up; Kilo Code took 6 weeks" (03012) — AI development speed is compressing traditional technology timelines by orders of magnitude.

## LLMs as "Baby AGI"

"LLMs can do something AlphaZero fundamentally can't: they can reason about things outside their training distribution. AlphaZero is a master within its domain but utterly helpless outside it" (08442). LLMs' generality — even if imperfect — is the property that makes them candidate AGI substrates. Terry Tao observes LLMs are "simpler than you think" (02211), suggesting the gap between current capabilities and human reasoning may be narrower than complex architectural proposals imply.

Karpathy frames LLMs as translation engines that will rewrite all software (10902) — every software interface becomes a natural language interface, fundamentally changing what software IS.

## Frontier Model Trajectory

Key milestones in the corpus:
- Gemini 3.0: stealth release claiming significant capability jumps (01287, 01485), Deep Think mode as "smartest model yet" (10814)
- GPT-5.2: arrival with market impact (01863), benchmarks among top models (09700)
- MiniMax M2.1: open model milestone (02109)
- Kimi K2.5: agent swarm capability (03273)
- Trillion-parameter models: AGI lab built in 8 months (01263)

The frontier model release cadence is accelerating, with competitive benchmarks shifting monthly.

## Biological Intelligence Parallels

Multiple sources explore biological intelligence as blueprint for AI capability:
- Michael Levin: multi-scale cognition, biological intelligence operating at cellular/tissue/organism levels simultaneously (01626, 02007)
- "Life Emerges from Code": intelligence as superset of which life is a subset; DNA stability as dynamical system (01194)
- Brain metaphor history: every generation uses its most advanced technology as metaphor for the brain, and every metaphor has been wrong (02751)
- "What if Intelligence Was There From the Start?": panpsychism-adjacent theory where intelligence is a mathematical property, not an emergent one (04197)

## Antipatterns & Lessons
- **Confusing benchmark capability with economic impact**: Models achieve gold on competitions but lack on-the-job learning. Economic deployment requires sustained time-horizon capability, not just complexity peaks (08442, 02091).
- **Scaling maximalism**: "More compute = better" was the age of scaling. The age of research requires architectural and algorithmic innovation (01539).
- **Ignoring inference economics**: Training a model is one cost; deploying it at scale is a different, often harder, cost (08442).
- **Human-language interpretability hubris**: If models compute in neuralese, our interpretability tools may be fundamentally limited (08442).
- **Every brain metaphor is wrong**: Using current technology (LLMs, neural networks) as metaphor for biological intelligence repeats the historical error of every prior generation (02751).
- **AGI goalpost shifting**: Standards for AGI shift as capabilities arrive. What seemed sufficient in 2020 is now considered baseline (02091).

## Cross-References
- neocorpus/ai-capability-futures/agi-timelines-predictions (when scaling produces AGI)
- neocorpus/ai-capability-futures/agent-evals-capability-benchmarks (measuring what scaling produces)
- neocorpus/ai-capability-futures/ai-market-investment-dynamics (compute economics)
- neocorpus/ai-capability-futures/physical-ai-robotics (inference at the edge)
