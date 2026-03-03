# AI Cybersecurity Threats

> Source is metadata-only; claims limited to title-level information. The extraction contains only 2 atoms from an IBM Technology video description, providing headline-level predictions without technical depth, attack vectors, or defensive frameworks.

## Sources
- `corpus/ai-capability-futures/02166.md` — 2 atoms: IBM Technology "Cybersecurity Trends in 2026" video description. Headline-level claims only. No transcript, no technical analysis.

## What the Source Contains

Two atoms, both at the description/headline level:

1. **Claim**: "Innovations like AI and quantum computing are redefining security."
2. **Prediction**: "Cybersecurity trends in 2026 will include Shadow AI, polymorphic malware, and post-quantum cryptography."

## The Concepts Named

Despite thin sourcing, the three named trends are substantive concepts worth tracking:

**Shadow AI** — Unauthorized AI tool usage within organizations, analogous to shadow IT. Employees deploying AI assistants, code generators, and data analysis tools without security review or data governance. The threat is not the AI itself but the uncontrolled data exposure: proprietary code fed to external models, confidential documents processed through unvetted services, training data poisoning through compromised AI tools in the supply chain.

**Polymorphic Malware** — AI-generated malware that mutates its own code to evade signature-based detection. Not new as a concept, but AI dramatically lowers the cost and raises the sophistication ceiling. LLMs can generate novel attack payloads, rewrite exploit code to avoid pattern matching, and adapt in real-time to defensive responses.

**Post-Quantum Cryptography** — The migration from current cryptographic standards (RSA, ECC) to quantum-resistant algorithms, driven by the "harvest now, decrypt later" threat: adversaries collecting encrypted data today to decrypt when quantum computers become capable. NIST standardization of post-quantum algorithms (CRYSTALS-Kyber, CRYSTALS-Dilithium) is underway, but enterprise migration is a multi-year infrastructure project.

**Deepfakes** — Named in the video title but not separately extracted. AI-generated synthetic media (video, audio, text) used for social engineering, fraud, and disinformation. The intersection with cybersecurity is direct: voice cloning for vishing attacks, video deepfakes for identity fraud, synthetic text for phishing at scale.

## Limitations

This entry is a stub. The source material contains no technical analysis, no attack vector enumeration, no defensive framework, and no quantitative threat assessment. The IBM imprimatur lends credibility to the trend identification but not to any specific claim about severity, timeline, or mitigation. This entry should be substantially enriched when deeper source material on AI-specific security threats enters the corpus.

## Cross-References
- neocorpus/ai-capability-futures/scaling-laws-trajectories (capability trajectory enabling these threats)
- neocorpus/ai-capability-futures/ai-governance-regulation-safety (regulatory response to AI threats)
