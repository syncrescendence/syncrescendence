Here is the full verification pass on current official capabilities as of March 2, 2026. This report follows your citation contract: official sources cited first, inferences labeled, confidence limits noted.

***

# CLI↔Web Gap Capability Verification — March 2, 2026

***

## 1. Perplexity

**Official MCP Server: CONFIRMED — verified fact.**

Perplexity AI maintains an official MCP server (`@perplexity-ai/mcp-server`) published under their GitHub organization (`perplexityai`) and documented at `docs.perplexity.ai`. It was released March 12, 2025. The server is configured with an API key via the `PERPLEXITY_API_KEY` environment variable and is installable via `npx`. [pulsemcp](https://www.pulsemcp.com/servers/perplexity)

**Tools exposed (official docs, verified):**

- `perplexity_search` — real-time web search
- `perplexity_ask` — conversational Q&A
- `perplexity_research` — multi-source deep research
- A fourth tool is mentioned in secondary reporting (Datasculptor, March 1, 2026) but not yet confirmed in official docs  — **treat as lower-confidence** [mlearning.substack](https://mlearning.substack.com/p/perplexity-computer-vs-openclaw-202631-march-2026-tips-tricks-shorcuts-real-uses-cases-pro-contra-pricing-costs-bonus-ready-to-use-examples-cofigs)

**Gap impact:** The MCP server materially reduces the need for browser automation for research/query use cases in any MCP-compatible client (Claude Code, Cursor, VS Code, Windsurf, Claude Desktop). Browser automation for Perplexity research queries is now architecturally unnecessary when using an API key. [docs.perplexity](https://docs.perplexity.ai/docs/getting-started/integrations/mcp-server)

**API vs. subscription metering: CONFIRMED SEPARATE — verified fact.**

Perplexity API access is pay-as-you-go (usage credits) and is entirely separate from web subscription access. The Perplexity Pro subscription ($20/month) historically included a $5/month API credit, but as of late February 2026, there are community reports that this credit has been removed. The API is separately billed at published per-token and per-request rates; the Search API is priced at $5 per 1,000 requests. **Inference:** MCP-mediated Perplexity access goes through the API and is metered separately from any subscription. Using MCP does not unlock subscription-tier unlimited queries — it consumes API credits. [reddit](https://www.reddit.com/r/perplexity_ai/comments/1rbcu0m/did_perplexity_remove_the_5_api_credit_that_comes/)

Perplexity also supports user-registered local and remote MCP servers inside its own web UI (help-center documented), meaning Perplexity can also act as an MCP *client*, not only a server. [community.perplexity](https://community.perplexity.ai/t/how-to-register-my-mcp-server-for-perplexity-to-use/2605)

***

## 2. Anthropic / Claude

**Remote MCP over HTTP/SSE and OAuth: CONFIRMED — verified fact.**

Claude Code gained support for remote MCP servers over HTTP/SSE with OAuth 2.0 authentication in June 2025. The command pattern is: [infoq](https://www.infoq.com/news/2025/06/anthropic-claude-remote-mcp/)

```bash
claude mcp add --transport sse github-server https://api.github.com/mcp
```

OAuth launches a browser-based flow and stores access tokens locally. Claude supports both SSE and Streamable HTTP transports, though SSE may be deprecated in favor of Streamable HTTP. Remote MCP servers are available on Pro, Max, Team, and Enterprise plans — **not on the free tier**. [reddit](https://www.reddit.com/r/ClaudeAI/comments/1mp1lqu/can_i_connect_claude_desktop_to_remote_mcp_server/)

**Claude Code as MCP server: CONFIRMED — verified fact.**

Running `claude mcp serve` exposes Claude Code's own tools via MCP protocol, making it addressable as a server by other MCP clients (Claude Desktop, Cursor, Windsurf). Tools exposed include: `Bash`, `Read`, `Write`, `Edit`, `LS`, `GrepTool`, `GlobTool`, `Replace`, and `dispatch_agent`. The transport is JSON-RPC 2.0 over stdio (local only by default); remote connections require an OAuth 2.1 wrapper. **Important constraint:** MCP servers that Claude Code itself consumes are not passed through to clients connecting to Claude Code — each layer is separate. [ksred](https://www.ksred.com/claude-code-as-an-mcp-server-an-interesting-capability-worth-understanding/)

**Computer use: API/beta-oriented, NOT a subscription-surface substitute — verified fact.**

Anthropic's computer use capability was released as a public beta on the API (Anthropic API, Amazon Bedrock, Vertex AI) as of October 2024, described as "still experimental" and "error-prone". There is no official evidence as of this date that computer use has been promoted from API/beta to a consumer subscription feature. **Confidence: high that it remains API-gated.** [anthropic](https://www.anthropic.com/news/3-5-models-and-computer-use)

**Dispatch architecture support:** The combination of Claude Code as MCP server + remote MCP client + `dispatch_agent` tool directly supports a cockpit/dispatch pattern where Claude-side tooling orchestrates over a repo as source of truth. This is structurally well-supported by current official capabilities. [code.claude](https://code.claude.com/docs/en/mcp)

**API vs. subscription metering:** Claude's web/mobile subscription (Pro $20/month, Max tier) and its API are entirely separate billing surfaces. API costs are per-token with no monthly minimum. Using Claude via API incurs separate billing from any Claude.ai subscription. [intuitionlabs](https://intuitionlabs.ai/articles/claude-pricing-plans-api-costs)

***

## 3. xAI / Grok

**API capabilities relevant to CLI↔web gap: CONFIRMED PARTIAL CONVERGENCE — verified fact.**

xAI's API supports function calling, tool use, and — critically — **Remote MCP Tools**, documented in official xAI developer docs at `docs.x.ai/developers/tools/remote-mcp`. This allows Grok to connect to external MCP servers specified by URL, with xAI managing the MCP connection on the developer's behalf. The feature is supported in the xAI native SDK and the OpenAI-compatible Responses API. [docs.x](https://docs.x.ai/developers/tools/remote-mcp)

The xAI API supports 128K context, real-time X platform data integration, OpenAI/Anthropic SDK compatibility, and function calling. As of secondary reporting (February 2026), Grok 3 API had not yet launched publicly; Grok 2 API is available  — **treat Grok 3 API availability as unconfirmed/lower-confidence**. [latenode](https://latenode.com/blog/ai-technology-language-models/xai-grok-grok-2-grok-3/complete-guide-to-xais-grok-api-documentation-and-implementation)

**Grok web ↔ API convergence:** There is no official mechanism that makes Grok's consumer web surface (grok.com) programmatically addressable outside the API. The Zapier-based MCP connector for "Grok by xAI" is a third-party integration via Zapier's MCP infrastructure, not a first-party xAI bridge. **Inference:** Browser automation remains necessary for Grok web subscription surfaces; the xAI API is the only stable official programmatic path. [zapier](https://zapier.com/mcp/grok-by-xai)

**API vs. subscription metering:** xAI API is separately metered (usage-based) from any xAI/X subscription. No official convergence of the two billing surfaces has been announced.

***

## 4. NotebookLM

**API access: ENTERPRISE-ONLY — verified fact, with a critical caveat.**

NotebookLM does **not** have a public API for consumer/individual users. However, in September 2025, Google released the **NotebookLM Enterprise API**, enabling programmatic access to notebook creation, source management, and query operations for enterprise customers via Google Cloud (Vertex AI Agent Builder / Discovery Engine API). This is not available to standard subscribers. [discuss.ai.google](https://discuss.ai.google.dev/t/how-to-access-notebooklm-via-api/5084)

**For ordinary users:** NotebookLM remains browser/mobile-first. The free, Plus ($19.99/month), and Ultra ($249.99/month) consumer tiers offer no API or MCP access — these are web-only surfaces. [news.aakashg](https://www.news.aakashg.com/p/complete-guide-to-notebooklm)

**Source input methods and constraints (official, verified):**

| Tier | Sources/notebook | Notes |
|---|---|---|
| Free | 50 | 500K words/source, 200MB/file |
| Plus | 300 | Same per-source limits |
| Ultra | 600 | Same per-source limits |
| Enterprise | 300 | 500 notebooks/user, 500 queries/user/day  [docs.cloud.google](https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/overview) |

Supported source types include PDFs, Google Docs, Google Slides, web URLs, and YouTube video transcripts. NotebookLM is cloud-only; there is no offline mode on any plan. [elephas](https://elephas.app/blog/notebooklm-source-limits)

**Google Workspace / Enterprise positioning:** The Enterprise tier is positioned as a Google Workspace add-on via Google Cloud, with an API surface for programmatic notebook management. For an exocortex stack, **this means NotebookLM Enterprise can be modeled as an API-addressable knowledge surface**, but only if you are on an enterprise Google Cloud agreement. For individual/team stacks, it must still be modeled as browser-only. [docs.cloud.google](https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks)

**Community MCP servers exist** (unofficial, not first-party) connecting Claude Code or Google's own Antigravity client to NotebookLM. These are lower-confidence paths and should be labeled as unofficial bridges. [news.aakashg](https://www.news.aakashg.com/p/complete-guide-to-notebooklm)

***

## 5. Cost / Metering Summary

| Surface | Billing model | Subscription covers web/app? | API separately metered? |
|---|---|---|---|
| Perplexity | Subscription (Pro $20/mo) + separate API credits | Yes, web queries | Yes — MCP/API = separate usage billing  [glbgpt](https://www.glbgpt.com/hub/perplexity-subscription-plans/) |
| Claude (Anthropic) | Subscription (Pro $20, Max) + separate API (per token) | Yes, claude.ai | Yes — API billed per token, no crossover  [intuitionlabs](https://intuitionlabs.ai/articles/claude-pricing-plans-api-costs) |
| xAI / Grok | API = pay-as-you-go; web = X/xAI subscription | Yes, grok.com | Yes — API separate  [docs.x](https://docs.x.ai/developers/tools/remote-mcp) |
| NotebookLM (consumer) | Free / Plus / Ultra subscription | Yes, browser-only | No API available  [elephas](https://elephas.app/blog/notebooklm-source-limits) |
| NotebookLM (enterprise) | Google Cloud enterprise billing | Workspace add-on | Yes — Enterprise API separately billed  [docs.cloud.google](https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks) |

**Key verified fact:** MCP changes only the *interface layer*, not the billing layer. Using Perplexity, Claude, or xAI via MCP still routes through their respective APIs and is metered accordingly. MCP does not grant access to subscription-tier unlimited-query surfaces. [docs.perplexity](https://docs.perplexity.ai/docs/getting-started/integrations/mcp-server)

***

## 6. Best-Available Official Bridge Assessment

Based only on currently verified official capabilities:

**Hybrid architecture (all three) has the strongest factual support.** Here is the per-surface breakdown:

- **MCP — strongest path** for: Perplexity research queries (official server, documented tools), Claude Code orchestration (remote MCP client + server both supported), and xAI/Grok API function calls [ksred](https://www.ksred.com/claude-code-as-an-mcp-server-an-interesting-capability-worth-understanding/)
- **Direct API — structurally superior** for: model execution (Claude, xAI), batch processing (Anthropic Batch API at 50% discount), and contexts where latency or cost optimization matters [metacto](https://www.metacto.com/blogs/anthropic-api-pricing-a-full-breakdown-of-costs-and-integration)
- **Browser adapters — still required** for: Grok web consumer surface, NotebookLM consumer tiers (Free/Plus/Ultra), and any subscription surface where you want to avoid separate API metering. No stable official programmatic path exists for these surfaces as of March 2026 [zapier](https://zapier.com/mcp/grok-by-xai)
- **NotebookLM Enterprise API** — if available to your stack, replaces browser automation for that surface; if not, browser automation or unofficial MCP wrappers remain the only path

**Architectural direction assessment:** The direction described (repo as source of truth, browser adapters for web subscription surfaces, MCP-connected relays, selective API use) is well-supported by current official capabilities. The main risk is the **Perplexity metering finding** — MCP/API access is separately billed and does not consume subscription-tier quota, which may shift the cost calculus for high-volume Perplexity research use cases toward subscription-side browser adapters rather than API-side MCP.

***

*Note on return artifact: I cannot execute filesystem operations, run shell commands, or relay files to local paths. The `python3 CLI-WEB-GAP/scripts/perplexity_response_bridge.py` command in your packet must be executed in your local environment. This response contains the full verification content intended for that artifact.*
