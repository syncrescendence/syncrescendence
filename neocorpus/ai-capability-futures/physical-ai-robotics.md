# Physical AI & Robotics

> Physical AI — agentic intelligence embodied in the physical world — represents the transition from the $2-5 trillion IT industry to the $100 trillion "world of atoms," but the messy physical world demands fundamentally different data, simulation, and evaluation strategies than digital agents.

## Sources
- 00912.md — Jensen Huang's Physical AI framework: perception-generative-agentic-physical wave progression, NVIDIA Cosmos/Omniverse, AR/VR as "half a robot," digital twins
- 01146.md — Dwarkesh Patel interview: foundation models for physical intelligence, modular perception/control architecture, robot capability progression analogous to LLM coding assistants (194 atoms)
- 01227_from_infrastructure.md — Extropic/Trevor McCourt: probabilistic circuits for physical AI, thermodynamic computing as alternative to digital inference (158 atoms)
- 01374.md — Dylan Curious "Embodied General Intelligence" atoms: SIMA 2 in 3D environments, Tesla robot AI, delivery robot comfort zones, focus on useful AI over AGI fantasy
- 02619.md — Dylan Curious/Boston Dynamics atoms: AI learning human skills autonomously, AGI disruption prevention
- 02916.md — Zipline drone delivery: 2M deliveries, 125M autonomous miles zero incidents, vertical integration, 1:30 human-to-aircraft ratio
- 02914.jsonl — Zipline atoms (duplicate of 02916.md content)
- 01372.jsonl — Embodied general intelligence atoms (duplicate of 01374.md content)
- 03201.md — Lisa LaBelle: Figure robots running in formation, SkildAI breakthrough, robot brains
- 03939.md — Rivian CEO: autonomous vehicles transitioning from human-coded rules to neural networks, software-defined vehicle architecture
- 09436.md — Dylan Curious "Embodied General Intelligence" video description
- 09642.md — Google DeepMind robotics lab tour: robots that think, plan, and do; generalization testing
- 09766.md — NVIDIA Developer: introduction to physical AI & robotics ecosystem
- 09910.md — NVIDIA CES 2026: Jensen Huang on physical AI, Cosmos, Isaac Sim, industrial automation
- 10049.md — Dylan Curious/Boston Dynamics: Google-Boston Dynamics reunion on next-gen Atlas
- 10372.md — Lisa LaBelle robotics episode description

## The Four Waves of AI

Jensen Huang's framework defines a clear progression (00912):
1. **Perception AI**: Understanding images, words, sounds.
2. **Generative AI**: Creating images, text, sounds.
3. **Agentic AI**: Perceiving, reasoning, planning, acting — in digital environments.
4. **Physical AI**: The same perceive-reason-plan-act loop, embodied in the physical world.

Physical AI is agentic AI that must deal with the "messy physical world" rather than constrained digital APIs. The recursive loop — map the world, perceive contents, plan actions, execute, repeat — is the same, but the state space is vastly larger and less structured (00912).

## The Data Bottleneck

The critical asymmetry: LLMs converge because they all train on the same data (the public internet). Physical AI diverges because real-world data is expensive to capture, curate, and label (00912). Companies with massive sensor fleets — Tesla (vehicle fleet), Google (Maps, 98% global population coverage) — hold structural advantages.

Three facets of world models (00912):
1. **Photorealistic**: Human-readable (Google Maps Immersive View, Google Earth)
2. **Abstracted**: Buildings, road networks, points of interest
3. **Machine-readable 3D**: Semantic classes (sidewalks, trees, poles) that machines can parse

NVIDIA's answer for companies without Google/Tesla-scale data: **Cosmos** (world foundation models) + **Omniverse** (physics-based simulation engine). The pipeline: build physically-accurate scenarios in Omniverse, output renders into Cosmos to generate photoreal synthetic training data. This combines procedural 3D modeling's physical accuracy with generative AI's variation capacity. 3D simulations enforce traffic rules; Cosmos makes renders look like real camera noise (00912).

## Simulation as Accelerant

Simulations can run 432,000 times faster than real-time (00912). Robots can learn in an evening what would take thousands of years in the physical world. Digital twins — built by fusing LiDAR, imagery, and real-time IoT data — enable what-if scenarios (city evacuations, traffic modeling, weather forecasting).

NVIDIA is applying this to weather forecasting in Taiwan: diffusion models achieve super-resolution from 25km to 2km; 3D simulation models achieve centimeter-level wind accuracy (00912). The same physical AI techniques that train robots also discover the past — a PhD student used LiDAR to reveal a lost Mayan city of 6,000+ buildings (00912).

## Robot Capability Trajectories

The progression of robot capabilities mirrors LLM coding assistants: starting with narrow tasks (coffee making), gradually increasing in scope and agency as common sense develops (01146). Initial productivity gains come from augmenting experts, not immediately replacing workers. The modular architecture separating perception from control mirrors biological sensory/motor separation (01146).

Key milestones:
- **Figure**: Robots running in formation (03201)
- **Boston Dynamics**: Next-gen Atlas reunited with Google (10049)
- **SkildAI**: Breakthroughs in robot learning (03201)
- **SIMA 2** (DeepMind): Plays, reasons, and learns in 3D environments; transfers concepts across games; self-improves through trial-and-error without human intervention (01374, 01284)
- **Zipline**: 2 million autonomous deliveries, 125 million miles with zero safety incidents, FAA-approved 1:30 human-to-aircraft ratio, site ramp from 110 days to 2 days (02916)

## Autonomous Vehicles as Physical AI

Rivian's trajectory illustrates the industry shift: abandoned original technology platform to build a vertically integrated data stack. The automotive industry is moving from human-coded rules to neural networks and custom chips. Software-defined vehicle architecture enables monthly feature updates, replacing function-based architecture (03939).

## AR/VR: "Half a Robot"

XR devices are "half a robot" — they contain perception (sensors, intelligence) but feed decisions into the human brain, which then acts on the world (00912). This positions AR glasses as human-robot hybrids. Google's Project Astra demonstrates this: AR glasses running Gemini that answer questions about the physical world, provide navigation overlays, and offer "circle to search" for physical objects. Enterprise applications include hands-free maintenance with real-time 3D annotations from remote experts (00912).

## Alternative Computing Substrates

Extropic's probabilistic circuits represent a radically different approach to physical AI computation (01227_from_infrastructure). The thesis: digital computers generating pseudo-randomness for probabilistic inference is thermodynamically equivalent to "running an electric heater inside a freezer." Purpose-built probabilistic hardware that natively samples from desired distributions could be orders of magnitude more efficient for the inference operations physical AI requires. Quantum computing is dismissed for this purpose — "using a finicky rocket to ship something across town" (01227_from_infrastructure).

## The $100 Trillion Opportunity

NVIDIA frames physical AI as the transition from the $2-5 trillion IT industry to the $100 trillion physical world (00912). The market encompasses spatial intelligence, robotic systems, AR/VR, construction, weather forecasting, and autonomous logistics. Elon Musk's "full spectrum dominance" — satellite grid, self-driving fleet, AI development — exemplifies the physical AI play at civilizational scale (00912).

## Human-Robot Interaction

A measurable human "comfort zone" dictates appropriate proximity for delivery robots (01374). This signals that physical AI deployment requires social and psychological research, not just engineering. The spectrum from pure human to pure robot intelligence, with AR-augmented humans in between, demands evaluation frameworks that account for human factors (00912).

## Antipatterns & Lessons
- **Treating physical AI as "just agentic AI with a body"**: The data bottleneck, physics constraints, and state space explosion make physical AI a qualitatively different problem (00912).
- **Ignoring simulation**: Real-world data collection is too slow and expensive. Simulation-to-real transfer (with careful domain randomization) is the viable path (00912).
- **Pursuing AGI fantasy over useful AI**: Building useful robots that solve real problems now (like Zipline's 2M deliveries) teaches more than chasing embodied general intelligence as an abstract goal (01374).
- **Brute-force approaches**: ARC v3 explicitly prevents brute-force solutions. Future robot evaluation will measure efficiency, not just completion (09332 cross-ref).
- **Assuming linear scaling**: Zipline's ramp from 110 days to 2 days per site shows exponential operational learning curves in physical AI deployment (02916).

## Cross-References
- neocorpus/ai-capability-futures/agent-evals-capability-benchmarks (SIMA 2, ARC v3 interactive evaluation)
- neocorpus/ai-capability-futures/scaling-laws-trajectories (simulation scaling, data requirements)
- neocorpus/ai-capability-futures/ai-economic-impact-labor (robot labor substitution patterns)
- neocorpus/ai-capability-futures/agi-timelines-predictions (embodied AGI timelines)
