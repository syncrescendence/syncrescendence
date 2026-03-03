# Scaling Laws & Capability Trajectories

> The AI field is transitioning from the "age of scaling" (more compute = better models) to the "age of research" (novel architectures, RL, and efficiency breakthroughs) — where the clean reward signal thesis explains why code/math work and open-ended tasks don't, and inference compute emerges as the true bottleneck.

## Sources
- 08442.md — Sholto Douglas & Trenton Bricken "Is RL + LLMs Enough for AGI?": two axes of capability, clean reward signal thesis, neuralese, THAT/WHY gap, inference bottleneck, LLMs as "baby AGI"
- 01539.md — Ilya Sutskever: transition from age of scaling to age of research
- 02091.md — Dwarkesh Patel "What Are We Scaling?": RL scaling misguided if near human-like learners, models lack on-the-job learning, economic impact lags capability benchmarks, AGI goalposts shifting
- 01377.md — AI costs plummeting 40x: Anthropic vs OpenAI comparisons, cost collapse dynamics
- 01506.md — Post-transformer architecture: Continuous Thought Machines, success capture phenomenon
- 01752.md — Pedro Domingos: Tensor Logic unifies AI paradigms, trillions wasted on brute-force compute, Predicate Invention
- 01806.md — NeurIPS 2025: 6 shifts most people will miss
- 01887.md — Yi Ma: mathematical foundations of intelligence, parsimony + self-consistency, transformers derivable from compression, blessing of dimensionality
- 02205.md — State of RL Reasoning: IMO/IOI gold, o3, GPT-5 trajectory, IOI Gold paradox, continual learning with infinite memory
- 02211.md — Terry Tao: "LLMs are simpler than you think"
- 02181.md — In-context learning mechanism explained, ICL as Rank-1 weight update
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
- 09700.md — Trump AI executive order, Nvidia H200 exports, GPT-5.2 benchmark rankings
- 00257.md — "Something Big Is Happening": social proof narrative, METR task-length doubling, recursive self-improvement (GPT-5.3 Codex), workforce impact timeline
- 01200.md — Nvidia next phase: three scaling laws, Hopper→Blackwell→Vera Rubin roadmap, data center token economics
- 01215.md — a16z State of AI Runtime: $200B+ capex, AI as biggest platform shift, US-China innovation lag, intelligence vs leadership
- 01509.md — Benedict Evans "AI Eats the World": platform cycle framing, LLMs as commoditized inputs, path-dependent adoption
- 01524.md — Google Willow quantum chip: verifiable quantum advantage, quantum-AI interplay
- 01608.md — OpenAI at 800M users: single model→specialized portfolio, prompt engineering→context design
- 01779.md — a16z "Chip That Could Unlock AGI": analog computing thesis, brain 20W vs 4% US grid, digital computing limitations
- 01968.md — AI vibe check: plateau perception myopic, infinite capital constraining innovation, RL Goldilocks zone
- 02313.md — DeepSeek topological transformer: mHC (Manifold-Constrained Hyper-Connections)
- 02460.md — AI phase transitions: Logical Phase Transitions as universal LLM breaking points, FOL skeleton + neural soft tissue

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

Post-transformer architectures are emerging: Continuous Thought Machines (01506), Tensor Logic unifying AI paradigms (01752), probabilistic circuits for energy efficiency (09361), DeepSeek's topological transformer mHC (Manifold-Constrained Hyper-Connections) (02313). The mathematical foundations of intelligence are being formalized (01887, 04117, 04197). Yi Ma demonstrates that transformer architectures can be mathematically derived from compression principles, and that natural optimization landscapes are "surprisingly smooth" — a "blessing of dimensionality" explaining why gradient descent works at scale (01887).

The transition is not uniform. The perception that models are "plateauing" is myopic — focused too narrowly on LLM text benchmarks while breakthroughs occur in other modalities (01968). Paradoxically, infinite capital at frontier labs may actually constrain innovation by locking resources into proven approaches rather than exploratory research (01968). RL operates within a narrow "Goldilocks zone" where it is effective, and the 2017-2022 RL research era largely failed because the community overfitted to benchmarks and rewarded complex ideas over simpler, more generalizable ones (02205, 01968).

### Success Capture

The transformer co-inventor warns of "success capture" — the phenomenon where an industry focuses on making small tweaks to a successful architecture rather than seeking fundamental new advancements (01506). Current AI models may be "faking understanding" — drawing tiny straight lines that mimic a spiral rather than grasping the concept of spiraling itself. CTMs address this by enabling step-by-step "pondering" through problems, allowing self-correction and backtracking that current LLMs cannot genuinely perform (01506).

## Neuralese and the Interpretability Gap

Models may develop their own internal language ("neuralese") optimized for how they compute, not for how humans read (08442). Implication: human-language interpretability may fundamentally miss model cognition — like transcribing whale clicks into English.

The THAT/WHY gap (08442):
- We can identify THAT the model is computing something
- We can trace information flow
- We CANNOT explain WHY it chose that particular computation over alternatives

This is not a temporary engineering limitation — it may be structural. If models think in neuralese, full interpretability through human-language probes may be impossible in principle.

## The Three Scaling Laws

Nvidia identifies three distinct scaling laws, all demanding more compute (01200):
1. **Pre-training scaling**: More data and parameters improve base capability
2. **Post-training scaling**: RL, RLHF, and fine-tuning improve alignment and task performance
3. **Test-time scaling**: More inference compute (chain-of-thought, search, verification) improves output quality

The hardware roadmap tracking these laws progresses from Hopper to Blackwell to Vera Rubin architectures, with unprecedented annual "X-factor" improvements enabled by extreme co-design from transistor to data center level (01200). Blackwell is twice as efficient as Hopper in token generation. A CPU-only data center generates $1-2B/year in revenue; a Hopper data center generates $10-20B; a Blackwell data center generates $40-45B — with revenue now measured in tokens generated (01200).

## The Inference Bottleneck

"Inference compute is much harder to scale than training compute" (08442). Training: throw more compute, get better models. Inference: real-time, can't batch the same way, requires different infrastructure. This may bottleneck AGI deployment more than capability development — models could be AGI-capable in training but undeployable at scale due to inference costs.

## Cost Collapse Dynamics

AI costs are plummeting ~40x (01377, 09439). This democratizes capability rapidly — what required frontier lab resources becomes available to startups and individuals within months. The cost curve explains why open-source models catch up so quickly (cross-ref democratization entry) and why the SaaSpocalypse hits enterprise software.

"Apple took years to catch up; Kilo Code took 6 weeks" (03012) — AI development speed is compressing traditional technology timelines by orders of magnitude.

The hardware energy gap is stark: the human brain operates on 20 watts while AI data centers consume 4% of the US energy grid (01779). This has prompted exploration of analog computing as a fundamentally different substrate — Unconventional AI argues that 80 years of digital computing may be an unsuitable foundation for intelligence, and that analog systems are better suited (01779). The physics of causality and analog processing may offer alternative paths to AGI that sidestep the energy crisis entirely.

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

OpenAI has transitioned from a single general-purpose model to a portfolio of specialized systems with custom fine-tuning, node-based agent workflows, and deterministic (not free-roaming) agent builders (01608). The interaction paradigm itself is evolving from "prompt engineering" to "context design" (01608). The US leads in conceptual AI breakthroughs while China excels at implementation and commoditization with a 3-6 month lag (01215).

### Recursive Self-Improvement

GPT-5.3 Codex is the first model "instrumental in creating itself" — used to debug its own training, manage deployment, and diagnose evaluations (00257). Anthropic's CEO reports AI writes "much of the code" at the company, with the feedback loop between current and next-generation AI "gathering steam month by month." The estimate: 1-2 years from a point where the current generation autonomously builds the next (00257). This is the intelligence explosion thesis moving from prediction to observation.

### METR Task-Length Doubling

METR tracks the length of real-world tasks (measured by expert human completion time) that models can complete end-to-end without help. The progression: ~10 minutes (early 2025) → 1 hour → several hours → nearly 5 hours (Claude Opus 4.5, November 2025). This metric doubles approximately every 7 months, with recent data suggesting acceleration to every 4 months. Extrapolating: AI working independently for days within a year, weeks within two, month-long projects within three (00257).

### The IOI Gold Paradox

Achieving IOI Gold — a major competitive programming benchmark — did not produce the expected societal shift or sense that AI was "solved" (02205). The goalposts moved. This is a recurring pattern: milestones that seemed definitional of AGI are reclassified as baseline once achieved (02091, 02205).

### Continual Learning with Infinite Memory

The next paradigm shift may be "continual learning with infinite memory" — models that learn from an experience once (a bug, a user mistake) and store it permanently in their weights, leveraging capacity from trillions of pretraining tokens (02205). Cursor's approach embodies this: policy updates every two hours, co-designing products so the entire software engineering workflow is in-distribution for RL (02205).

## Biological Intelligence Parallels

Multiple sources explore biological intelligence as blueprint for AI capability:
- Michael Levin: multi-scale cognition, biological intelligence operating at cellular/tissue/organism levels simultaneously (01626, 02007)
- "Life Emerges from Code": intelligence as superset of which life is a subset; DNA stability as dynamical system (01194)
- Brain metaphor history: every generation uses its most advanced technology as metaphor for the brain, and every metaphor has been wrong (02751)
- "What if Intelligence Was There From the Start?": panpsychism-adjacent theory where intelligence is a mathematical property, not an emergent one (04197)

## Quantum Computing as Scaling Accelerant

Google's Willow chip achieved the first verifiable quantum advantage — solving a physics problem 13,000 times faster than a supercomputer (01524). The quantum-AI interplay creates a potential acceleration loop: quantum computing advances drug discovery, materials science, and protein structure analysis, while AI advances quantum algorithm design. Industry applications are projected to be "just a few years away" (01524). Nvidia positions quantum computing as particularly suited for physics problems — chemistry, materials science, drug discovery — complementing rather than replacing classical AI compute (01200).

## AI Phase Transitions and Logical Breaking Points

Logical Phase Transitions (LPTs) describe the universal breaking point of all LLMs in their reasoning capabilities (02460). It is possible to determine the exact point at which a model's reasoning collapses. A proposed architecture: First Order Logic (FOL) forms the "skeleton" of reasoning while the neural network constitutes the "soft tissue" (02460). This framework predicts capability discontinuities — sudden jumps or failures at specific complexity thresholds rather than smooth degradation.

## Platform Shift Dynamics

AI is the biggest platform shift in computing history because it changes what computers CAN DO, not just who uses them or how they are distributed (01215). Previous shifts (mainframe→PC, web, mobile) changed interfaces and distribution; AI enables computers to perform tasks requiring human intelligence. This is backed by $200B+ in hyperscaler capex, projected to exceed $300B (01200, 01215).

Benedict Evans frames AI adoption as following familiar platform cycles, but with a critical difference: LLMs are becoming commoditized inputs while frontier labs maintain differentiation (01509). Path-dependent adoption means that teams treating AI as optional tooling will lose ground to those redesigning workflows, org charts, and vendor strategy around AI's inevitability (01509). AlphaFold's trajectory — from grand challenge to Nobel Prize in Chemistry (2024) — demonstrates AI's capacity to solve problems previously considered intractable, with AlphaFold 3 incorporating diffusion models for a more comprehensive approach (01602).

## In-Context Learning Mechanisms

In-context learning may be a form of implicit fine-tuning — specifically a Rank-1 update function in the weight tensor space (02181). The transformer architecture may possess "open degrees of freedom" that enable ICL, only now being discovered (02181). This mechanistic understanding suggests that the learning algorithms within transformer layers that activate ICL are not yet fully characterized — the architecture may be more capable than its designers intended.

## Antipatterns & Lessons
- **Confusing benchmark capability with economic impact**: Models achieve gold on competitions but lack on-the-job learning. Economic deployment requires sustained time-horizon capability, not just complexity peaks (08442, 02091).
- **Scaling maximalism**: "More compute = better" was the age of scaling. The age of research requires architectural and algorithmic innovation (01539).
- **Ignoring inference economics**: Training a model is one cost; deploying it at scale is a different, often harder, cost (08442).
- **Human-language interpretability hubris**: If models compute in neuralese, our interpretability tools may be fundamentally limited (08442).
- **Every brain metaphor is wrong**: Using current technology (LLMs, neural networks) as metaphor for biological intelligence repeats the historical error of every prior generation (02751).
- **AGI goalpost shifting**: Standards for AGI shift as capabilities arrive. What seemed sufficient in 2020 is now considered baseline (02091). IOI Gold didn't feel like "solving AI" once it happened (02205).
- **Success capture**: Incremental improvement to transformers may trap the field in a local maximum, preventing discovery of fundamentally better architectures (01506).
- **Intelligence supremacism**: Assuming raw IQ equals power. High-IQ experts often work for mid-IQ generalists. Leadership requires emotional intelligence, theory of mind, courage, and the ability to navigate human psychology — properties AI cannot easily acquire through scaling alone (01215).
- **Infinite capital as constraint**: Counterintuitively, unlimited funding at frontier labs may lock resources into proven approaches rather than exploratory research, constraining the innovation that the "age of research" demands (01968).

## Cross-References
- neocorpus/ai-capability-futures/agi-timelines-predictions (when scaling produces AGI)
- neocorpus/ai-capability-futures/agent-evals-capability-benchmarks (measuring what scaling produces)
- neocorpus/ai-capability-futures/ai-market-investment-dynamics (compute economics)
- neocorpus/ai-capability-futures/physical-ai-robotics (inference at the edge)
