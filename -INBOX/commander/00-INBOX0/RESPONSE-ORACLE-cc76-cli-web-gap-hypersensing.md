**Thesis:** The coherent architecture that closes the CLI↔web gap while honoring Syncrescendence's repo-dispatch → surface-execution → artifact-return → reconciliation → ontology-projection contract is a local orchestrator that ingests packets from the repo, enqueues them via filesystem primitives, and fans them out to a subscription-worker fabric composed of persistent browser-profile adapters (Playwright-driven, surfaced as MCP servers) for pure web surfaces, with native MCP or API fallbacks used only where they are verifiably cheaper, faster, or more reliable. Repo, event ledger, and ontology remain the immutable truth plane; no second authority is introduced; already-paid subscriptions are leveraged directly through authenticated browser sessions.

This is not theory. It is the minimal extension of the surface taxonomy and web-surface packet standard already committed in the repo, aligned with the account-identity matrix that already enumerates per-surface auth without duplication.

### 1. Architecture comparison and recommendation
- **Primary:** Local file-queue relay + browser-profile workers (Playwright + MCP wrapper). Packets land in a watched `/jobs/inbox` directory; a daemon dispatches, the worker executes in a logged-in profile, returns artifact to `/artifacts`, daemon reconciles and projects. Matches the boundary contract exactly.
- **Fallback:** Native MCP (Perplexity MCP server, xAI remote MCP tools, Claude Code MCP) or API (xAI Files/Collections, Perplexity Agent/Search where volume justifies) only for surfaces that expose them without incremental metering beyond the subscription already paid.
- **Avoid:** Human relay (breaks automation), website/domain as sole control plane (introduces latency and second source of truth), Cowork as central dispatch cockpit (it is an execution surface, not the orchestrator).

### 2. Subscription-worker fabric
The right primitive is **browser profile + adapter + filesystem queue**, optionally wrapped as an MCP server for standardization.  
- Persistent Playwright contexts with stored cookies/sessions for Grok web, Perplexity web, NotebookLM, Claude web/Cowork.  
- Adapter reads packet (per WEB-SURFACE-PACKET-STANDARD), performs the interaction (navigate, attach files, submit, scrape result), writes artifact.  
- MCP wrapper turns each adapter into a discoverable tool so any MCP client (Claude Desktop, Cursor, local daemon) can call it uniformly.  

This turns already-paid web surfaces into callable workers from one dispatch point. Perplexity's official MCP server and xAI's remote MCP are convenient but API-keyed and therefore metered; browser path bypasses that for the web UI. Anthropic computer-use (updated Nov 2025 with zoom/scroll) is a strong reference implementation but sandboxed and slower—use it as inspiration, not runtime.

### 3. Industry patterns that actually work
Concrete, replicated patterns from 2025–2026 builders (not generic "agentic browsers"):
- Playwright MCP servers with persistent profiles: dominant in Claude Code skill marketplace (microsoft/playwright, vercel-labs/agent-browser, lackeyjb/playwright-skill) and awesome-mcp-servers list. Practitioners keep one Chrome profile per subscription, launch headless or headed on demand, queue tasks as JSON files in a git-ignored but repo-synced directory.
- Filesystem job queues as relay: used in OpenClaw AI, libr-agent, coasty-ai/open-computer-use, and parallel-terminal-grid workflows. Simple, auditable, git-friendly, zero extra infrastructure. Daemon watches dir, processes, moves to done/fail with artifact symlink back to repo.
- MCP as universal abstraction layer: adopted across Anthropic, xAI (remote MCP tools added Nov 2025), Perplexity, and community. Turns heterogeneous surfaces into one protocol without custom glue.
- Hybrid control: repo as truth, local daemon as dispatch, browser as execution, optional web dashboard for human oversight—exactly the shape described in Personal AI Infrastructure write-ups and OpenMetadata-style orchestration.

These patterns minimize metered API exposure while preserving logged-in state that pure APIs cannot replicate for NotebookLM or full Grok web UX.

### 4. Component roles and stack shape
- **Repo/event/ontology:** truth plane (immutable source and sink).  
- **Filesystem job queue + local orchestrator (CLI daemon):** dispatch/control plane.  
- **MCP layer:** tool abstraction (standardizes calling browser workers or native tools).  
- **Browser adapters (Playwright + MCP server per surface):** execution plane for web subscriptions.  
- **Cowork/Claude web:** high-intent interactive execution surface, not dispatch cockpit.  
- **Website/domain:** human monitoring and manual trigger plane, never authoritative control.  

Coherent stack shape:  
Truth (Repo + Ledger + Ontology)  
↑↓  
Dispatch/Control (Local CLI Orchestrator + FS Queue)  
→ Execution (MCP Browser Workers + selective APIs)  
→ Return (Artifacts → Reconciliation → Projection)

### 5. Recent product changes that matter
- xAI (Nov 2025): remote MCP tools, Files API, Collections Search—strengthens API path but does not unify metering with web subscription; Grok 4 remains accessible via both but web retains richer context windows in practice.  
- Anthropic (Claude Code MCP + computer-use updates Nov 2025): dynamic tool refresh, Tool Search, zoom/scroll in computer-use—makes browser control more reliable.  
- Perplexity: MCP server requires API key → metered; web subscription still cheaper for interactive use.  
- NotebookLM: remains web-first (attachments, source uploads, notebook synthesis); enterprise Google Workspace integration exists but no broad public API surfaced in docs—browser adapter is required for consumer tier.  
No shift invalidates the browser-worker approach; all reinforce it for cost-controlled subscription leverage.

### 6. Richer jobs abstraction
One adapter per site that accepts a typed job schema inside the packet (action: query | upload-sources | create-notebook | synthesize | attach-then-query).  
The packet standard already supports extensible fields; extend it with a `job_type` and `payload` map. Filesystem queue carries attachments as sibling files or base64 blobs. This is simpler and more reversible than per-job action schemas in a monolithic queue or one massive adapter. Keeps surface boundary clean.

**Recommended stack diagram (text):**  
Dispatch plane → FS job queue → Execution plane (browser-profile MCP workers for Grok/Perplexity/NotebookLM/Claude + API/MCP fallbacks) → Return plane (artifacts written back) → Event reconciliation → Ontology projection (repo truth).

**Phased recommendation**  
Now (stage 0–1): Deploy FS queue daemon and Playwright adapters for Perplexity web and Grok web using existing account matrix profiles. Wire packet dispatch.  
Next (stage 1–2): Wrap adapters as MCP servers, add NotebookLM browser flow, implement richer job schemas, integrate with Feedcraft/IIC governance.  
Later (stage 2+): Add website monitoring dashboard, optional Cowork packet-generation surface, full hybrid fallback logic, production hardening.

**Explicit answers**  
Browser adapters plus subscription workers are the right primary path—yes.  
Cowork should not be the main dispatch cockpit—no; it is an excellent execution and high-intent planning surface, but dispatch remains the local orchestrator reading repo packets.

This design is parsimonious, falsifiable at every layer, reversible, and directly extends the artifacts already in the repo. Implement the queue daemon first; the rest follows. Save this response to the specified inbox path and run the bridge command to project into ontology. The gap is closed.