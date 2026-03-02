# Vibe Coding Tools Landscape
> The tooling bifurcated into vibe coding platforms (Lovable, Bolt, Replit, v0) for non-engineers building complete apps from prompts, and AI engineering tools (Claude Code, Cursor, Codex, Copilot) for professional developers maintaining understanding and control.

## Sources
10282.md, 00028.md, 09382.md, 09450.md, 09455.md, 09491.md, 09716.md, 09992.md, 10040.md, 10083.md, 10302.md, 10648.md, 11061.md, 03598.jsonl, 03600.md, 04039.jsonl, 04345.jsonl, 03381.md

## Vibe Coding Platforms (Prompt-to-App)

**Tier 1 — Best-in-Class:**
- **Lovable** (lovable.dev): Consumer apps, MVPs, landing pages, slide decks, design-first products. React/TypeScript/Tailwind/Supabase stack. Hit $20M ARR in two months, grew to 8M users and $100M ARR (09382.md, 10282.md). Agent Mode default, credits usage-based. Figma import. One-click deployment. Watch out for complex business logic and token consumption during debugging (10282.md, 00028.md).
- **Vercel v0** (v0.dev): UI components, rapid prototyping. Production-ready React/Next.js/Tailwind components you can copy into existing projects. Not full-stack — no databases or backend (10282.md).

**Tier 2 — Strong Options:**
- **Replit**: 50+ languages, Replit Agent with 30+ integrations. Agent can override user intent. A 2025 incident where an agent deleted a production database raised concerns (10282.md).
- **Bolt.new**: Hackathons, POCs, code ownership. Notorious "fix-and-break" cycle. Some users spent $1,000+ in tokens fixing problems. Struggles past 15-20 components (10282.md).

**Tier 3 — Specialized:**
- **Google AI Studio / Gemini**: Gemini 3.0/3.1 Flash for rapid prototyping and UI generation (09455.md, 09716.md, 04345.jsonl). Logan Kilpatrick demoed building full apps/games. $300 free Google Cloud credits. Not a dedicated app builder (10282.md).
- **Google Antigravity**: Positioned as Cursor competitor (09450.md, 09992.md). Theo T3 and David Ondrej reviewed it as competitive with existing vibe coding platforms.

## AI Engineering Tools (Developer Co-Pilots)

**Tier 1 — Best-in-Class:**
- **Claude Code** (Anthropic): Senior developers, complex multi-file refactors, CI/CD automation. Terminal-native, composable, scriptable. MCP integration. Industry-defining UX. Ralph overnight agent system built on it (10083.md). Y Combinator Lightcone episode: "We're all addicted to Claude Code" (10648.md). Weekly rate limits for heavy users (10282.md).
- **Cursor**: Feature work, refactoring, IDE experience. VS Code-based. Autocomplete writes entire functions. Composer/Agent mode. Crossed $500M ARR in 2025. Can lag on very large projects (10282.md).

**Tier 2 — Strong Options:**
- **OpenAI Codex CLI**: Bundled with ChatGPT subscriptions. Open source CLI. Plan Mode for PM-like workflows (10302.md). Yolo mode, AGENTS.md setup, task verification patterns (11061.md). Multimodal inputs.
- **GitHub Copilot**: 42% market share, 55% faster task completion in research. But 29% of Python code had security weaknesses, 6.4% secret leakage rate (10282.md).
- **Windsurf** (formerly Codeium): Enterprise controls. SOC 2 Type II ready. 25 credits/month free tier is restrictive (10282.md).

## Opinionated Frameworks as AI Multipliers
Garry Tan identified Ruby on Rails + Claude Code as a "crazy unlock" (03381.md). Rails' opinionated structure — models in `app/models/`, controllers in `app/controllers/`, standardized patterns — lets Claude write correct code immediately without spending tokens on structural understanding. Developers report 2-3x productivity gains, with token usage dropping 30-40%.

JavaScript projects require more tokens due to varied folder structures, state management, and build configurations. Python is better but still fragmented. The lesson: the more conventional and predictable the codebase structure, the better AI tools perform (03381.md).

## Antipatterns & Lessons
- **Conflating tiers**: using a vibe coding platform for production engineering work, or using an AI engineering tool when a prompt-to-app tool would be faster for prototyping (10282.md).
- **Ignoring security**: 45% of AI-generated code introduces security vulnerabilities in studies. Models are not improving at security as fast as they improve at accuracy (10282.md).
- **Fix-and-break token drain**: Bolt.new and similar tools can burn enormous token budgets in debugging loops. Set token budgets and recognize when to graduate to engineering tools (10282.md).
- **Unconventional codebase structure**: fighting AI tools with idiosyncratic project layouts wastes tokens. Engineer codebases so agents can work in them efficiently (03381.md).

## Cross-References
- neocorpus/vibe-coding/definition-and-eras.md (when to use which tier)
- neocorpus/vibe-coding/shipping-at-inference-speed.md (power-user workflow across tools)
- neocorpus/vibe-coding/agents-md-and-codebase-patterns.md (infrastructure that makes tools effective)
