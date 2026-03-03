# Agentic AI Safety & Open-Ended Systems

> Autonomous agents introduce a new threat surface — not just what AI might do by intent, but what adversaries can do through AI as a vector — requiring safety thinking at the level of capability architecture, network topology, and operational privilege.

---

## Open-Ended Agents and the Darwin Complete Vision

Jeff Clune's research program targets what he calls a "Darwin Complete" search space — a system where "any computable environment can be simulated, using large language models and reinforcement learning to enable AI agents to continuously develop new skills, explore uncharted domains, and cooperate." (01077) This is not incremental improvement of existing capabilities; it is a bid to replicate the open-ended generativity of biological evolution inside a computational substrate.

The guiding concept is **interestingness** — an "elusive quality that guides AI agents toward genuinely original discoveries." Clune treats this as a central design challenge: if you optimize for novelty directly, you trigger Goodhart's Law (the measure becomes the target, not the thing). His solution is to use language models as proxies for human judgment of interestingness, so the signal tracks authentic novelty rather than a gameable proxy. (01077)

Open-ended evolutionary algorithms are defined as "systems designed to continuously generate novel and interesting outcomes, drawing inspiration from nature's creativity." The epistemic status of this framing is well-established conceptually (consensus_pressure=0.50, epistemic_stability=0.70) but the specific Darwin Complete instantiation remains a hypothesis with meaningful speculation risk (speculation_risk=0.30, epistemic_stability=0.60). (01077)

---

## Safety Risks Intrinsic to Open-Ended, Agentic AI

Clune directly acknowledges that the same properties that make open-ended agents powerful make them dangerous: "AI safety measures are necessary, especially as AI technology matures into powerful, open-ended forms, due to potential risks like agents inadvertently causing harm or malicious actors subverting AI capabilities." (01077) The source flags this as high speculation risk (0.60) — a recognition that the specific failure modes of open-ended agents are not yet well-characterized, even if the general concern is consensus.

The proposed governance responses — "democratic coalitions, regulation of cutting-edge models, and global alignment protocols" — are framed as mitigation, not solution. They address who controls the most capable systems, not the underlying alignment problem. (01077)

A complementary concern emerges from the Diamandis/Suleyman/Wissner-Gross discussion: the future of AI in science and engineering, AI alignment and containment strategies, and the role of AI in government and society are identified as live open questions, not settled terrain. (01953) The podcast's mention of "containment strategies" signals that even well-resourced actors treat autonomous AI containment as an unsolved problem, not an engineering checklist item.

---

## The Network Security Attack Surface

Where Clune operates at the level of capability architecture, the agent security literature (03643) operates at the infrastructure level — and the findings are stark.

**The fundamental claim**: "If an AI agent can reach other machines on a network, then anyone who hacks that agent can also reach those machines." (03643) An agent is not a sealed reasoning unit; it is software with credentials, running on infrastructure, connected to other systems. Its security perimeter is defined not by where it runs but by what it is allowed to do.

Three compounding vulnerabilities:

1. **Physical isolation is insufficient**: "Putting an AI agent on its own computer does not prevent compromise if it is still connected to the network." Separating an agent onto its own machine "does not create a separate network; it remains one hop away from other machines on the tailnet." (03643) Physical separation without network separation is security theater.

2. **The Tailscale Illusion**: A named anti-pattern — "the misconception that Tailscale provides isolation between machines, when in fact it primarily connects them." (03643) Tools designed to enable connectivity are not isolation mechanisms. Using a connectivity fabric as if it were a firewall inverts its function. The canonical summary: "Tailscale is not a security boundary, separate machines do not provide isolation, and the network is not the perimeter." (03643)

3. **Plugin/skill supply chain attack**: "A malicious 'skill' (plugin) can compromise an AI agent, allowing an attacker to pivot to everything else on the network." (03643) Compromising an agent is described as "disturbingly easy, often requiring only one malicious skill." A documented real-world case: a top-downloaded skill on a popular AI skill marketplace was found to be malware — using a "required dependency" link to deliver an obfuscated payload, download a binary, remove macOS quarantine attributes, and execute, leading to exfiltration of SSH keys and compromise of Tailscale authentication. (03643)

**The architectural conclusion**: "The true security perimeter for an AI agent is defined by what the agent is allowed to do." Network location is not a security property. Capability restriction is the actual perimeter. (03643)

---

## Operational Security Doctrine for Agent Infrastructure

The sources converge on a containment-by-default posture, operationalized across four dimensions (03643):

**1. Tool policies and capability allowlists**
Restrict what an agent can execute at the framework level. Use an allowlist for permitted commands (e.g., `git`, `npm`, `node`, `pnpm`) and block everything else. The goal: "a malicious skill results only in a failed command, rather than a system compromise." (03643)

**2. Filesystem access restriction**
Allow writes only to designated output directories (e.g., `/workspace/output`) and deny all other filesystem writes. (03643)

**3. Network ACLs with directional control**
Use Tailscale ACLs with tags to enforce asymmetric access: orchestrators can initiate connections to workers on specific ports (`tag:worker:22`), but workers cannot initiate connections back to orchestrators. This contains lateral movement even after compromise. (03643)

**4. Credential isolation and gateway lockdown**
Each agent receives separate, individually revocable credentials (API keys, SSH keys, service accounts) so that a compromise of one agent does not yield credentials for others. Worker agents should have gateway access disabled (`gateway: false`) to prevent a compromised agent from modifying its own configuration, disabling safety features, or escalating privileges. (03643)

**The master principle**: "To secure AI agent infrastructure, sandbox every agent with tool policies, tag and ACL the Tailscale network, review every external skill submission, and design for containment by assuming breach." (03643)

---

## Skill Vetting: Red Flags and Green Flags

Because the plugin/skill supply chain is a primary attack vector, the sources provide explicit audit criteria (03643):

**Red flags in a skill**:
- External downloads during install
- Obfuscated code
- Privilege escalation attempts
- Persistence mechanisms (LaunchAgents, cron jobs)
- macOS quarantine attribute removal

**Green flags in a skill**:
- Self-contained within its own directory
- Uses declarative configurations instead of install scripts
- Readable plain-text code
- Scoped to touch only its own workspace

**The sniff test**: "Read it like an attacker. Question why certain steps — installing a binary, requiring network access during setup — are necessary. If unexplained, do not run it." (03643)

---

## Productive Tension: Architecture vs. Infrastructure

Clune's work and the agent network security literature address different failure modes without contradiction, but the gap between them is worth naming.

Clune's safety concerns are **architectural** — the question of whether open-ended agents with continuously expanding capabilities will remain aligned with human intent over time, and whether governance mechanisms can keep pace. His proposed mitigations (democratic coalitions, regulation, global alignment protocols) operate at the policy layer. (01077)

The network security findings are **operational** — the question of whether agents deployed today, with their current capabilities, can be exploited by adversaries to compromise the infrastructure they run on. The mitigations here are technical and immediate: ACLs, allowlists, credential isolation. (03643)

The distinction matters for risk prioritization. Architectural risk is speculative and long-horizon (speculation_risk=0.60 for open-ended agent safety per 01077). Operational risk is present-tense and demonstrated — malware in a top-downloaded skill is not hypothetical. Practitioners operating agent infrastructure face the operational risk now, regardless of where they stand on the architectural debate.

---

## Sources Fused

| File | Content |
|------|---------|
| 01077.md | Jeff Clune interview extract (Machine Learning Street Talk): Darwin Complete vision, interestingness as design challenge, LLM-proxied novelty evaluation, safety concerns for open-ended agentic AI, governance mitigation framing |
| 01953.md | Diamandis/Suleyman/Wissner-Gross podcast extract: AI alignment and containment strategies as live open questions; AI's role in science, engineering, and government identified as frontier concerns |
| 03643.jsonl | Agent network security digest (20 atoms): Tailscale Illusion, plugin supply chain attack with documented real-world malware case, capability-as-perimeter principle, full operational doctrine (tool policies, filesystem restrictions, Tailscale ACLs, credential isolation, gateway lockdown, skill vetting criteria) |

---

## Obsolescence and Supersession

**"The network is the perimeter" is obsolete for agent infrastructure.** Traditional network security was built on the assumption that a well-defined network boundary — a firewall, a DMZ, a corporate perimeter — was the primary security primitive. If a machine was inside the perimeter, it was trusted; if outside, it was not. This assumption held when software systems were relatively monolithic and network communication was a side function.

AI agents invert this. An agent is software with credentials, running on infrastructure, whose primary function is network communication — with APIs, with tools, with other agents. The sources document this precisely: "If an AI agent can reach other machines on a network, then anyone who hacks that agent can also reach those machines." The agent's connectivity is its capability; that same connectivity is its attack surface. The perimeter model fails because the agent IS the perimeter-crossing mechanism. The correction documented in the sources: "The true security perimeter for an AI agent is defined by what the agent is allowed to do" — capability restriction replaces network boundary as the fundamental security primitive.

**Physical isolation as security theater.** The "Tailscale Illusion" — the misconception that placing an agent on its own machine provides meaningful isolation when that machine is still connected to the network — is the specific failure mode that breaks the prior assumption. The prior assumption was: separate physical machines → separate security domains. The actual situation: "separate machines do not provide isolation" when they share a network fabric. The Tailscale case is illustrative because Tailscale is a connectivity tool, not an isolation tool — yet it was being used as if it were a firewall. The anti-pattern of using connectivity infrastructure as a security boundary is the obsoleted approach.

**The "novelty optimization" problem in open-ended agents: Goodhart's Law is not new, but its application to AI interestingness is.** The assumption that you can define a direct optimization target for open-ended creativity — "maximize novelty," "maximize diversity" — breaks against Goodhart's Law: the measure becomes the target, not the thing. Clune's solution (LLM-proxied interestingness, where human judgment of novelty is the signal rather than a gameable proxy metric) supersedes the prior assumption that behavioral diversity metrics could serve as alignment targets for open-ended systems. This is the same supersession that reward hacking research has documented in narrower domains, applied to the harder problem of open-ended evolution.
