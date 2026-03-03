# The Agent-Native Economy: Selling to Agents, Coase's Boundary, and Machine Commerce

> AI agents can discover, check prices, and call a service in a single HTTP roundtrip, eliminating traditional transaction costs. The attention economy does not apply to agents.

## Sources

04144.jsonl, 04146.md, 04306.jsonl, 11056.md, 03259.jsonl, 03904.jsonl

## Coase's Boundary Collapses

Ronald Coase's 1937 Nobel Prize-winning question: if markets are so efficient, why do firms exist? His answer: transaction costs — finding specialists, evaluating work, negotiating prices, enforcing agreements (04146.md).

AI agents change this calculation. They can discover, check prices, and call a service in a single HTTP roundtrip, eliminating search and evaluation costs that historically justified building in-house. While integration, compliance, and security review remain expensive, the search and evaluation costs for services approach zero (04146.md).

**The default decision shifts**: When search costs collapse, the default moves from "build it in-house" to "buy it on the open market," with software agents as the primary buyers (04146.md). This is the fundamental restructuring of Coase's make/buy boundary.

## Selling to Agents: A New Commerce Model

Agents optimize for outcomes, not attention. They lack brand loyalty, impulse purchasing, or status signaling. Their decision function: problem-solving capability, speed, cost, reliability (04146.md).

**What does not work for agent buyers** (04146.md):
- Marketing sites and pricing pages are irrelevant
- Brand recognition, social media metrics carry no weight
- The attention economy (billboards, ads, emails) does not apply
- Beautiful UI is meaningless to a buyer that never sees it

**What works** (04146.md):
- Machine-readable capability registries providing structured data on functionality, cost, payment methods via URL
- Liveness, proven reliability, confidence in results
- Verifiable accuracy: services that prove output accuracy outperform cheaper alternatives lacking proof
- Reliability is the entire product, not a feature

**If a service cannot be discovered by a machine, it does not exist to AI agents** (04146.md).

## The Human-Agent Marketing Surface

Humans still determine which tools an agent is allowed to use, creating a marketing surface for getting onto an "allowlist." But runtime purchasing decisions are pure optimization (04146.md). Enterprise agents operate within policy constraints: spending limits, vendor allowlists, data residency, approved-provider lists.

The adversarial environment for agents is real — some endpoints return garbage, exfiltrate data, or lie about capabilities (04146.md).

## Compliance as Structured Data

Compliance itself can become machine-readable: terms of service as structured data, data retention policies in API headers, licensing as metadata (04146.md). This creates a new infrastructure layer where legal and compliance documents are API-queryable.

## Skills Stores as the New App Stores

Skills as new apps; skills stores as new App Stores; desktop control equals distribution control (04306.jsonl). The platform that controls which skills an agent can access controls the distribution layer of the agent economy — paralleling how iOS/Android app stores control mobile distribution.

## API-First as Maximum Defensibility

API-first companies are the most defensible position in the agent-native economy. Off-the-shelf software is worst-common-denominator — designed for human users who are no longer the primary buyer (03904.jsonl).

## Platform Data Asymmetry Breaking

AI is breaking the data asymmetry that platforms like LinkedIn maintained over users (03259.jsonl). When agents can aggregate and synthesize data from multiple sources, platform lock-in through data hoarding weakens.

## The Web Forks

The web is forking into human-facing and agent-facing layers (11056.md). Coinbase launched agent wallets (13,000 agents registered Ethereum wallets within 24 hours). Stripe had to retrain its entire fraud detection system because agent traffic does not move a mouse. Cloudflare ships Markdown conversion and X402 monetization support for agent access.

The mobile web analogy breaks down: the new client is not a smaller screen — it is no screen at all. The gap between infrastructure being built and trust people are willing to extend is the central tension of the next few years (11056.md).

## Antipatterns & Lessons

- **Optimizing for human attention when the buyer is an agent**: The entire marketing, sales, and distribution stack built for human psychology is irrelevant to machine buyers (04146.md).
- **Assuming brand loyalty transfers to agents**: Agents switch providers based on cost/reliability/speed with zero switching cost if MCP is implemented (04146.md).
- **Ignoring adversarial agent environments**: Agents operating in the open internet encounter hostile endpoints. Trust and verification infrastructure is a prerequisite (04146.md).
- **Building closed platforms in an open-discovery world**: If agents cannot discover your service programmatically, you are invisible to the fastest-growing buyer segment (04146.md).

## Obsolescence & Supersession

**The human-first internet assumption (now obsolete)**: Every internet infrastructure layer — DNS, HTTP headers, HTML, SEO, ad tracking, analytics — was built assuming the client is a human. Search engines ranked by human engagement signals. Pricing pages assumed human comparison-shopping. Email marketing assumed human attention. These assumptions were so foundational that the question "what if the client has no attention span?" was never asked. It did not need to be asked.

The agent-native web is the first phase where that assumption fails in practice, not just in theory. Coinbase launching agent wallets (13,000 registrations in 24 hours), Stripe retraining fraud detection because agent traffic moves no mouse, Cloudflare shipping agent-specific infrastructure — these are infrastructure providers discovering mid-deployment that their entire request-analysis stack was tuned to a client that no longer represents the dominant traffic type (11056.md).

**v1 → v2: from human-facing SEO to machine-readable capability registries**: The v1 pattern for getting discovered was search engine optimization — content structured for human attention and search engine indexing heuristics. The v2 pattern for getting discovered by agents is machine-readable capability registries: structured data at a URL describing functionality, cost, payment methods, and uptime. These are not adjacent strategies; they are competing standards optimized for incompatible clients. The companies that built v1 distribution moats (brand recognition, Google ranking, email lists) find those moats irrelevant to the fastest-growing buyer segment (04146.md).

**What the supersession chain reveals**: The Coase boundary itself has a version history. v1 (1937): transaction costs are high, so firms internalize functions they could otherwise outsource. v2 (2010s SaaS era): cloud infrastructure reduced search costs, so make-vs-buy moved toward buy for software. v3 (agent era): AI agents reduce search and evaluation costs to near zero for any API-accessible service, completing the Coase reversal for the entire services market. Each version assumed the prior version's transaction cost floor was fixed. Each time, the floor dropped further than the prior model predicted.

## Cross-References

- [Interface Moat Collapse](interface-moat-collapse.md) — why human interfaces lose value
- [Software Survival Framework](software-survival-framework.md) — what architectural properties serve agents
- [AI Market Structure](ai-market-structure.md) — the competitive dynamics of the agent economy
- [Platform Power Distribution](platform-power-distribution.md) — who captures value in agent-mediated markets
