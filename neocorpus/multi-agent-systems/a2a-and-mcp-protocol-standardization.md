# A2A and MCP Protocol Standardization

The Model Context Protocol (MCP) and the Agent-to-Agent Protocol (A2A) represent the two foundational standards emerging for the agentic era: MCP standardizes how agents connect to tools and data sources, while A2A standardizes how agents communicate with each other. MCP has been described as "USB-C for AI" — a universal connector that allows any tool implementing the protocol to be immediately accessible to any agent that speaks it. A2A, developed by Google, complements MCP by providing the inter-agent communication layer that MCP deliberately omits. Together they define the plumbing of multi-agent systems. But protocols are political artifacts as much as technical ones: Anthropic donating MCP to the Linux Foundation under the Agentic AI Foundation (with OpenAI as co-steward) signals that protocol governance — who controls the standard, who can extend it, who can fragment it — matters as much as protocol design.

---

## Core Principles

### 1. MCP Architecture: Server, Client, Protocol

MCP separates three concerns that were previously entangled:

- **Server**: Exposes capabilities via the protocol. A server can expose resources (data the agent can read), tools (actions the agent can take), and prompts (templates for common operations). Any system — a database, a file system, a SaaS API, an IDE — can become an MCP server by implementing the protocol.
- **Client**: Discovers and invokes server capabilities. Claude Code, Cursor, Windsurf, and other agent harnesses are MCP clients. The client queries what tools are available, presents them to the model, and routes tool calls to the appropriate server.
- **Protocol**: JSON-RPC over stdio or HTTP. The transport is deliberately simple — no custom binary format, no complex handshake beyond standard auth. This simplicity is the source of adoption velocity: any developer who can write a JSON-RPC handler can write an MCP server.

The architectural insight is that MCP externalizes capability from the model. A model does not need to "know" how to query a database — it needs to know that a database tool exists, what arguments it takes, and what it returns. The MCP server handles the actual database query. This separation means that tool capabilities can be updated, replaced, or extended without retraining the model.

### 2. The Context Tax Problem

Every MCP server connected to an agent consumes context window tokens with its tool schema definitions. The agent must "know" what tools are available, and that knowledge is encoded as token-consuming schema in the context. The measurement is stark: seven typical MCP servers consume approximately 100,000 tokens — 50% of a 200K context window — before a single conversational message is processed.

This is the fundamental scaling problem of MCP: the protocol's openness (any server can expose any tools) collides with the context window's finiteness. Solutions include:

- **Tool search**: Rather than loading all tool schemas at session start, the agent searches for relevant tools on demand. Only the schemas for tools actually needed enter the context.
- **CLI wrappers**: Instead of exposing fine-grained tools (one per API endpoint), expose coarse-grained CLI commands that bundle multiple operations. Fewer tools, less schema, less context consumed.
- **MCP Launchpad / proxy patterns**: An intermediary that aggregates multiple servers and presents a curated subset of tools based on the current task context.

The context tax is not a bug in MCP — it is an inherent cost of the tool-schema-as-context-injection architecture. Every tool the agent knows about is a tool it might hallucinate using. The tax is both computational (tokens consumed) and behavioral (irrelevant tools create noise that degrades tool selection accuracy).

### 3. A2A: The Inter-Agent Layer

While MCP connects agents to tools, A2A connects agents to each other. Google's Agent-to-Agent Protocol provides:

09928 describes ADK/A2A agents communicating over web standards; the discovery and delegation details extrapolate from this framing:

- **Agent discovery**: Agents can find other agents and query their capabilities. This enables dynamic team formation — an orchestrator can discover specialist agents at runtime rather than hardcoding their existence.
- **Task delegation**: A standardized format for one agent to request work from another, including task description, expected output format, and completion criteria.
- **Communication over web standards**: A2A uses HTTP, JSON, and standard web authentication. No proprietary transport. Any agent that speaks HTTP can participate.

The distinction between MCP and A2A is the distinction between tool use and collaboration. An agent using MCP is operating on its environment. An agent using A2A is coordinating with peers. Both are necessary; neither is sufficient alone.

### 4. Protocol Governance as Strategic Asset

Anthropic's decision to donate MCP to the Linux Foundation under the Agentic AI Foundation — with OpenAI joining as co-steward — transforms MCP from a corporate project into a governed standard. This matters for several reasons:

- **Fragmentation prevention**: Without neutral governance, competing implementations (Google's A2A, OpenAI's tool-calling format, Anthropic's MCP) could fracture the ecosystem into incompatible islands. A single foundation with multi-stakeholder governance reduces this risk.
- **Trust for third-party adoption**: Developers building MCP servers need confidence that Anthropic will not unilaterally change the protocol in ways that break their implementations. Foundation governance provides that stability guarantee.
- **Extension management**: As the protocol evolves, governance determines which extensions become standard and which remain vendor-specific. This is the HTML standards story: without governance, every browser (agent) implements its own extensions, and interoperability collapses.

The parallel to USB-C is precise: USB-C succeeded not because it was the best connector design but because it was governed by a standards body that enforced compliance. MCP's success depends on similar governance discipline.

---

## Key Insights

### The IDE as First Mover

The fastest adoption of MCP has been in developer tools. Apple shipping an MCP server with Xcode 26.3, Cursor and Windsurf building on MCP natively, and Claude Code using MCP as its primary tool extension mechanism all demonstrate that the developer tooling ecosystem has converged on MCP as the standard integration layer. This is not surprising — developers are both the builders and the first users of agent tools, creating a tight feedback loop between protocol design and adoption.

However, the IDE adoption pattern also reveals MCP's current limitations. Apple's Xcode MCP server requires the IDE to be running — it extends the IDE rather than replacing it. This means the agent is tethered to a GUI application, negating the headless execution model that agent automation requires. The community response (XcodeBuildMCP, which operates headlessly against the command-line tools) illustrates the tension between vendor MCP implementations (which expose existing product surfaces) and community MCP implementations (which expose the capabilities agents actually need).

### The Authentication Gap

MCP's transport layer (JSON-RPC over stdio or HTTP) is simple by design, but authentication remains a significant friction point. The Syncrescendence constellation experienced this directly: MCP clients for Notion and Linear failed to start because OAuth token handshakes failed. The error cascade — `AuthRequired` -> `Transport channel closed` -> `MCP client failed to start` — reveals that MCP's simplicity stops at the auth boundary.

The protocol specifies a `Bearer` auth mechanism, but the lifecycle of tokens (issuance, refresh, rotation, revocation) is outside the protocol's scope. This means every MCP server implements its own auth flow, and every auth failure produces a different error surface. Standardizing the auth lifecycle — not just the auth header — is the next frontier for MCP governance.

### Tool Schema as Contract

An MCP tool schema is a contract between the server and the agent: "if you call this function with these arguments, I will return this type of result." The quality of the schema determines the quality of the agent's tool use. A schema with vague argument descriptions produces hallucinated arguments. A schema with overly complex nested objects produces parsing errors. A schema with no error type specification produces agents that cannot handle failures gracefully.

The best MCP servers treat their tool schemas with the same rigor as public API documentation — because that is exactly what they are. The schema is not metadata; it is the primary interface through which an AI system understands and uses the tool.

---

## Anti-Patterns

### The Tool Explosion

Exposing every possible operation as a separate MCP tool. A database server that exposes `select`, `insert`, `update`, `delete`, `create_table`, `drop_table`, `alter_table`, `create_index`, `drop_index` as nine separate tools when a single `execute_sql` tool would suffice. Each additional tool consumes context tokens and increases the probability of the agent selecting the wrong tool.

### Protocol as Product Lock-In

Building an MCP server that technically implements the protocol but functionally requires a specific vendor's agent to use it (through undocumented extensions, proprietary auth flows, or capabilities that only one client implements). This defeats the interoperability purpose of the protocol.

### Ignoring the Context Budget

Connecting an agent to every available MCP server because "more tools means more capability." The context tax means more tools often means less capability — the agent's reasoning quality degrades as irrelevant tool schemas consume context that should be available for the actual task.

### Auth as Afterthought

Building the MCP server, shipping it, and then discovering that OAuth token refresh does not work when the server is invoked by an agent at 3 AM with no human available to re-authenticate. Auth lifecycle must be designed as a first-class concern, not bolted on after the happy path works.

### Protocol Without Governance

Adopting MCP or A2A without participating in or monitoring the governance process. Protocols evolve. Breaking changes happen. Extensions that become de facto standards can strand implementations that do not adopt them. If your system depends on a protocol, you must track its governance — or accept the risk of silent incompatibility.

---

## The Protocol Stack in Practice

A concrete multi-agent system in 2026 uses protocols at multiple layers:

| Layer | Protocol | Function |
|-------|----------|----------|
| **Tool access** | MCP (JSON-RPC / stdio or HTTP) | Agent discovers and invokes tools exposed by servers |
| **Agent discovery** | A2A (HTTP / JSON) | Agents find other agents and query capabilities |
| **Task delegation** | A2A or custom (HTTP / JSON) | One agent requests work from another |
| **State coordination** | Git / filesystem / database | Shared state between agents (repo as coordination surface) |
| **Human escalation** | Custom (CLI prompts, Slack, etc.) | Agent routes decisions to human principal |

The Syncrescendence constellation uses MCP for tool access (Playwright, filesystem, Notion, Linear), git for state coordination, and a custom dispatch system (TASK/CONFIRM/RESULT messages in the repo) for task delegation. A2A is not yet adopted but would replace the custom dispatch system if the constellation scaled beyond its current five-agent architecture.

The protocol stack reveals a gap: there is no standard for state coordination between agents. MCP handles tools; A2A handles communication; but the shared understanding of "what has been done, what remains, and what the current state is" relies on ad hoc solutions (shared filesystems, databases, git repos). This gap is where most coordination failures occur.

---

## Design Implications

### For MCP Server Developers

Design your tool surface for agents, not humans. An agent does not need a tool for every GUI button — it needs a minimal set of high-leverage tools with clear schemas, predictable error types, and authentication that works unattended. Measure your server's context tax (total tokens consumed by all tool schemas) and minimize it.

### For Agent Framework Developers

Implement tool search or lazy loading for MCP tool schemas. Do not load all connected servers' schemas at session start. Provide clear error messages when MCP servers fail to connect, distinguishing between "server not found," "auth failed," and "server started but tool invocation failed."

### For Protocol Governance

Prioritize the authentication lifecycle specification. The transport layer works; the auth layer is where adoption friction lives. Define standard flows for token refresh, credential rotation, and unattended re-authentication so that MCP servers can be used by agents operating without human supervision.

### For Multi-Agent System Operators

Map your current integration points to the protocol stack. Every custom integration (shell scripts, file-based dispatch, ad hoc HTTP calls) is a candidate for replacement with an MCP server or A2A endpoint. The migration is not urgent — custom integrations that work are better than standard integrations that do not — but the trajectory is clear. As the protocol ecosystem matures, custom integrations become technical debt.

### For the Ecosystem

The convergence of MCP and A2A under foundation governance creates the possibility of a unified agent communication stack: agents discover tools via MCP, discover each other via A2A, and both protocols are governed by the same foundation. This is the TCP/IP moment for AI agents — the point where the plumbing becomes invisible and the focus shifts to what you build on top of it. But only if governance prevents fragmentation. The history of technology standards teaches that the window for convergence is narrow: once incompatible implementations reach critical mass, the cost of convergence exceeds the benefit, and the ecosystem fragments permanently. MCP and A2A are in the convergence window now. The decisions made by the Agentic AI Foundation in its first two years will determine whether the agent ecosystem unifies or balkanizes.

---

## Syncrescendence Operational Context

The following claims derive from the constellation's operational history and constitutional documents (AGENTS.md, CLAUDE.md, memory/), not from external corpus sources:
- MCP clients for Notion and Linear failing to start due to OAuth token handshake failures
- The specific error cascade (`AuthRequired` -> `Transport channel closed` -> `MCP client failed to start`)
- The Syncrescendence constellation's use of MCP for tool access, git for state coordination, and custom dispatch for task delegation

---

## Source Provenance

| Source | Corpus Path | Contribution |
|--------|-------------|--------------|
| MCP server patterns (MECH entry) | `corpus/multi-agent-systems/04587.md` | MCP architecture (server/client/protocol); context tax measurement (7 servers = 100K tokens); JSON-RPC transport; tool schema as contract |
| Apple Xcode MCP server discussion | `corpus/multi-agent-systems/00130.md` | IDE-first MCP adoption; Xcode MCP limitations (requires running IDE); community vs vendor implementations; XcodeBuildMCP as headless alternative |
| Anthropic donates MCP to Linux Foundation | `corpus/multi-agent-systems/09659.md` | Protocol governance; Agentic AI Foundation; OpenAI as co-steward; fragmentation prevention; USB-C parallel |
| Google ADK / A2A architecture | `corpus/multi-agent-systems/09928.md` | A2A protocol; agent discovery; loop/sequential/judge agents; web standards transport |
