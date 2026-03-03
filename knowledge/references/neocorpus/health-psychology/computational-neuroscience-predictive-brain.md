# Computational Neuroscience — The Predictive Brain

## Sources

- `corpus/health-psychology/01122.md` — Extraction: Five New Paradigms of Intelligence (BrainMind)
- `corpus/health-psychology/01131.md` — Extraction: A Fundamental Unit of Intelligence (Artem Kirsanov)
- `corpus/health-psychology/09266.md` — A Universal Theory of Brain Function (Artem Kirsanov)
- `corpus/health-psychology/09270.md` — Collective Brain / Cultural Evolution (Joseph Henrich / Dwarkesh Patel)
- `corpus/health-psychology/09293.md` — A Fundamental Unit of Intelligence (Artem Kirsanov, source)
- `corpus/health-psychology/09838.md` — Your Brain Doesn't Command Your Body. It Predicts It (Max Bennett / MLST)
- `corpus/health-psychology/09863.md` — AutoGrad Changed Everything (Dr. Jeff Beck / MLST)
- `corpus/health-psychology/10123.md` — Why Every Brain Metaphor in History Has Been Wrong (MLST Special)
- `corpus/health-psychology/10274.md` — If You Can't See Inside, How Do You Know It's Thinking? (Dr. Jeff Beck / MLST)
- `corpus/health-psychology/09785.md` — You See Better Than AI: Vision Secrets Only Biology Knows (AI Neuro Insight)
- `corpus/health-psychology/02232.md` — Extraction: Predictive Brain / Max Bennett (MLST)

## Core Thesis

The brain is not a passive receiver of sensory data but an active prediction machine — a generative system that constructs models of the world, issues top-down predictions, and uses sensory signals only to compute and correct errors. This view, grounded in the Free Energy Principle (Karl Friston) and related Bayesian frameworks, holds that perception is fundamentally inference: you do not see the world, your brain builds a simulation of what it thinks is out there and uses the eyes to check whether it was right. Optical illusions are not bugs in this system — they are features, demonstrations that the brain's prior model is stronger than the incoming signal. Every act of cognition, from seeing a boundary to feeling a hunger pang, is the brain minimizing the gap between prediction and reality.

What makes the brain's predictive architecture remarkable is its physical substrate: a 3mm-thick sheet of cells, the neocortex, organized into cortical columns that each function as a complete sensorimotor system. Jeff Hawkins' Thousand Brains Theory proposes that every column builds its own model of the world through sensation, movement, and consensus voting across all six neuronal layers — there are thousands of such models operating in parallel, voting on the brain's best hypothesis. This architecture may be the fundamental unit of mammalian intelligence. Intelligence, in this account, is not a single faculty but a distributed, predictive, model-building process that evolution discovered and the neocortex instantiated.

The evolutionary and cultural dimensions of this thesis are equally consequential. The brain that predicts is also a brain shaped by — and dependent on — the collective. Joseph Henrich's evidence that individual brain size has declined 10% in 10,000 years while human capability has accelerated reveals a counterintuitive truth: the brain outsources cognition to culture. Prediction, at civilizational scale, is collective.

## Key Frameworks

### 1. Predictive Processing (Bayesian Brain / Helmholtz Tradition)

- The brain is "essentially running the scientific method on autopilot" — combining priors with sensory evidence to form posteriors through optimal Bayesian inference (09863.md, Dr. Jeff Beck)
- Perception is not direct observation but a "simulation built by the brain, which is then checked against sensory input" (02232.md, Max Bennett)
- Optical illusions demonstrate that the brain's prior model can overpower incoming sensory signal (09266.md, Artem Kirsanov)
- The brain generates predictions top-down and uses bottom-up signals to update models — the inversion that makes predictive processing canonical

### 2. Free Energy Principle (Karl Friston)

- Free Energy is a trade-off between accuracy and complexity in model-building (09266.md)
- The generative model issues predictions; the recognition model performs approximate (variational) inference to match predicted with observed (09266.md)
- Active Inference extends this to action: organisms act to bring the world into conformity with predictions, minimizing free energy through both perception and behavior (09863.md, 10274.md)
- Karl Friston cited across multiple sources as central figure (09863.md, 10274.md)

### 3. Thousand Brains Theory (Jeff Hawkins)

- Every cortical column is a complete sensorimotor system, not a simple feature detector (01131.md, 09293.md)
- Six neuronal layers work together through constant loops of sensation, movement, and consensus voting (09293.md)
- Grid cells in the neocortex serve as the mechanism for location-tagged model building (09293.md)
- Key references: Hawkins et al. (2019, 2021, 2025), Clay et al. (2024), Harris & Shepherd (2015)

### 4. Computational Neuroscience Foundations

- Hodgkin-Huxley equations demonstrate "that all processes in the brain are amenable to mathematical modeling" (01122.md)
- Church-Turing thesis implies brain computations are substrate-independent (01122.md)
- Wiener's 1943 cybernetics: a teleological system is "fundamentally a predictor, and higher-order prediction correlates with greater intelligence" (01122.md)
- AutoGrad (automatic differentiation), not transformers, was the real inflection point converting AI from math to engineering — but it obscured what makes biological intelligence work (09863.md, Jeff Beck)

### 5. Bayesian Object Models and the Grounding Problem

- Jeff Beck: the brain works not like a giant prediction engine over pixels/tokens but like a scientist working with objects that interact through forces (09863.md)
- Current LLMs cannot form hypotheses, test them, and update beliefs based on experiments (02232.md)
- Beck's proposed architecture: thousands of small modular object models that can be combined, swapped, updated — "like a video game engine" (09863.md)
- Grounding AI in language is "fundamentally misguided" because self-report is the least reliable data in psychology (09863.md)
- JEPA (LeCun) cited as step toward learning in latent space rather than predicting every pixel (10274.md)

### 6. Biological Vision

- Biological vision constructs boundaries, selects angles, and identifies corners using mechanisms with "no direct analogue in current AI" (09785.md)
- Timing constraints in the visual pipeline that current ML architectures do not respect (09785.md)
- Claim: these bio-plausible mechanisms "will lead to huge increases in AI efficiency" (09785.md)

### 7. Evolutionary Neuroscience of Intelligence

- Intelligence explosions via feedback loops among intelligent beings — the Social Intelligence Hypothesis (01122.md)
- Consciousness proposed as "the mind modeling itself, building upon the mind's capacity to model other minds" (01122.md)
- Max Bennett: brain evolved over 600M years in layers, each adding new predictive capacity (09838.md)
- Rats exhibit regret — they "imagine eating the food they passed up" and change decisions (02232.md, David Redish's Restaurant Row)
- Chimpanzees engage in deception and counter-deception (Rock and Belle experiment), demonstrating theory of mind (02232.md)
- Language as the human "singularity that already happened" — enables sharing internal mental simulations across individuals (02232.md)

### 8. Collective Brain and Cultural Evolution (Henrich)

- Collective brain = population size × interconnection × transmission fidelity — determines technological capability more than individual cognition (09270.md)
- Human brain size declined ~10% in 10,000 years while capability accelerated; hypothesis: cognitive outsourcing to culture (09270.md)
- Neanderthals had larger brains but lost because of smaller, less connected groups (09270.md)
- Cassava processing: a 10-step detoxification process that cannot be invented through individual insight — "thousands of people over thousands of years making small adjustments" (09270.md)
- Catholic Church's medieval marriage prohibitions inadvertently broke kinship networks, creating preconditions for capitalism (09270.md)

### 9. The Metaphor Problem

- Every historical brain metaphor — hydraulic pump, telegraph, switchboard, computer — "felt obviously true at the time" (10123.md)
- Chirimuuta: the mechanistic assumptions behind AGI may be a "cultural historical illusion" (10123.md)
- Joscha Bach: "software is literally spirit, not metaphorically" (10123.md)
- John Jumper (Nobel, AlphaFold): "AI can predict and control, but understanding requires a human in the loop" (10123.md)
- The predictive brain framework itself is subject to this critique

## Synthesis

**The convergence:** Prediction is the unifying operation across 180 years of science. Wiener's 1943 cybernetics established that purposive systems are predictors. Friston's Free Energy Principle formalizes this as variational inference. Hawkins' Thousand Brains instantiates it in cortical columns. Helmholtz's "perception as unconscious inference" is the 19th-century ancestor. The answer keeps being: prediction.

**The individual-collective tension:** The sources converge on prediction as the mechanism of individual intelligence, then reveal that individual intelligence is not where the action is. Henrich shows the individual brain has been shrinking as collective intelligence grows. Bennett shows that language enables sharing of mental simulations across individuals. The predictive brain is powerful because it predicts other minds and is embedded in a social fabric that vastly exceeds any single brain's capacity. Active Inference at scale becomes culture: a collective prediction machine evolving faster than any genome.

**The LLM challenge:** Multiple sources grapple with whether LLMs are genuine predictors in the relevant sense. The Wiener frame says LLMs validate cybernetic theory because they are prediction machines. But Beck and Bennett insist LLMs lack world models in the biological sense — they cannot form hypotheses, run experiments, or update beliefs. This is an active fault line, not a settled question.

**The metaphor warning:** The most sobering thread: every generation believed its brain metaphor was final. The predictive brain, Free Energy Principle, cortical column architecture — these are the current best models, not established truths.

**The bio-plausible gap:** Biological visual processing uses timing constraints, boundary detection, and angle/corner processing with no ML equivalent. The predictive brain is not just abstractly different from current AI — it is mechanically different in ways that may matter enormously for capability and efficiency.

## Open Questions

1. **Friston and Hawkins: complementary or competing?** Both arrive at prediction-error minimization but through different routes. No source resolves whether these are the same thing at different levels of description or genuinely different theories.

2. **What is a world model, precisely?** Beck requires hypothesis formation, testing, and belief updating. Bennett requires the ability to reject known-false information. Whether these are the same criterion is unresolved.

3. **Consciousness as self-modeling: testable or definitional?** Presented with novelty=0.70, epistemic_stability=0.40. No empirical test is provided that would distinguish this from alternative theories.

4. **The individual brain decline: outsourcing or something else?** Henrich proposes cognitive outsourcing to culture. Alternative explanations (metabolic efficiency, dietary changes) are not engaged.

5. **When does the metaphor break?** What specific predictions would, if falsified, cause abandonment of the predictive brain framework? Failure conditions are not specified.

6. **LLMs as prediction machines:** Are they evidence for or counterexamples to the prediction theory of intelligence? The sources do not resolve this tension.

7. **Cultural evolution and cognitive architecture: causal direction?** Culture drives brain size down (Henrich) but brain architecture enables cultural learning. Whether there is a feedback loop is unaddressed.
