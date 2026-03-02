### Entry 1: agent-first-engineering-culture.md

**Overall verdict**: FINDINGS  
**Claims checked**: 6  
**Issues found**: 3

| # | Claim (abbreviated) | Source Cited | Verdict | Notes |
|---|---------------------|-------------|---------|-------|
| 1 | `10825` supports the "no coding before 10am" playbook, pair prompting, objective-first specs, output-not-code review, and removing old code paths | 10825 | VERIFIED | These points closely track the source text. |
| 2 | `02088` supports the "three worlds" frame: engineers, non-engineers building software, and enterprises moving slowly | 02088 | VERIFIED | This framework appears directly in the extraction. |
| 3 | Software engineers see "3-10x on well-specified tasks" | 02088 | UNSUPPORTED | `02088` says engineers see clear productivity gains, but it does not give a 3-10x range. |
| 4 | Enterprise adoption requires MCP work, data annotation, and internal API surfaces before gains materialize | 02088 | DISTORTED | The source supports connector work, MCP adoption, and data/lineage work; "internal API surfaces" is an uncited expansion. |
| 5 | `10825` supports optimizing for time not tokens and maximizing agent utilization | 10825 | VERIFIED | Both are explicit tenets in the post. |
| 6 | The Syncrescendence paragraph presents external validation of the constellation's founding premise | None | UNSUPPORTED | This is an uncited project-specific synthesis, not sourced evidence about Claude Code. |

### Entry 2: agent-teams-and-parallel-orchestration.md

**Overall verdict**: FINDINGS  
**Claims checked**: 6  
**Issues found**: 3

| # | Claim (abbreviated) | Source Cited | Verdict | Notes |
|---|---------------------|-------------|---------|-------|
| 1 | Agent Teams is enabled by `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` with no extra dependencies | 00212 | VERIFIED | Stated directly in the source. |
| 2 | Teammates have separate context windows, no shared conversation history, auto-load `CLAUDE.md`, and coordinate via messages plus a shared task list | 00212 | VERIFIED | This is the core behavioral description in the source. |
| 3 | Team config lives in `~/.claude/teams/.../config.json`, tasks in `~/.claude/tasks/...`, created by `TeamCreate` and deleted by `TeamDelete` | 00212 | FABRICATED | None of these paths or APIs appear in the cited sources. |
| 4 | File-ownership partitioning is the key anti-collision mechanism and depends on clear module boundaries in `CLAUDE.md` | 00212 | VERIFIED | This matches the three-rules section. |
| 5 | The message protocol has structured lifecycle types like `shutdown_request` and `plan_approval_request` | 00212 | FABRICATED | The source mentions messages and shared tasks, not typed protocol primitives. |
| 6 | Plan mode is evaluated every turn and an agent's mode stays fixed for its lifetime | 00212 | VERIFIED | Explicit in the "Extra: a note on plan mode" section. |

### Entry 3: autonomous-research-workflow.md

**Overall verdict**: FINDINGS  
**Claims checked**: 5  
**Issues found**: 2

| # | Claim (abbreviated) | Source Cited | Verdict | Notes |
|---|---------------------|-------------|---------|-------|
| 1 | A 5-10 minute voice memo is transcribed and turned into a Claude Code prompt that runs the experiment end-to-end | 10857 | VERIFIED | This sequence is described directly. |
| 2 | Claude Code handles SSH, GitHub push/pull, GPU job management, queueing, ETA estimation, and status updates | 10857 | VERIFIED | These operational details are explicit in the post. |
| 3 | The researcher spends only a couple of hours per day checking in, and engineering is no longer the bottleneck | 10857 | VERIFIED | This is stated nearly verbatim. |
| 4 | The workflow widens the research funnel and shifts strategy toward cheap portfolio screening of many hypotheses | 10857 | DISTORTED | The source supports cheaper first-answer generation, but not this fuller portfolio methodology claim. |
| 5 | "Question without hypothesis" and "infrastructure lock-in" are documented failure modes of the workflow | 10857 / 10825 / 00041 | UNSUPPORTED | These warnings are reasonable but not present in the cited sources. |

### Entry 4: claude-md-configuration-system.md

**Overall verdict**: FINDINGS  
**Claims checked**: 6  
**Issues found**: 3

| # | Claim (abbreviated) | Source Cited | Verdict | Notes |
|---|---------------------|-------------|---------|-------|
| 1 | Claude Code uses managed, user, project, rules, local, and subdirectory `CLAUDE.md` scopes | 08764 | VERIFIED | The hierarchy is laid out directly in the synthesis. |
| 2 | Scopes combine additively, with more specific scopes overriding only on conflict | 08764 | VERIFIED | This matches the synthesis language. |
| 3 | Subdirectory files load on file access, and simple directory listing does not trigger loading | 08764 | UNSUPPORTED | The source supports on-demand subtree loading, but not the stronger file-access-vs-listing distinction. |
| 4 | `@path/to/file.md` imports exist and a 5-hop limit is reported but not officially confirmed | 08764 | VERIFIED | This exact uncertainty is documented in the source. |
| 5 | Rules files activate independently and support conditional activation | 08764 | VERIFIED | Supported by the rules-scope description. |
| 6 | Agent teams automatically loading project `CLAUDE.md` is supported by this entry's cited source set | 08764 / 10032 / 00001 | CITATION ERROR | That claim is supported by `00212`, which this entry does not cite. |

### Entry 5: context-injection-and-codebase-traversal.md

**Overall verdict**: FINDINGS  
**Claims checked**: 5  
**Issues found**: 2

| # | Claim (abbreviated) | Source Cited | Verdict | Notes |
|---|---------------------|-------------|---------|-------|
| 1 | The main latency problem is lossy translation from UI intent into code search trajectories | 00116 | VERIFIED | This is the framing of the React Grab article. |
| 2 | File paths and grep-able class names materially speed up location finding | 00116 | VERIFIED | The source gives these exact ad-hoc examples. |
| 3 | React Grab walks the component tree and returns component names plus file path and line numbers | 00116 | VERIFIED | Central mechanism of the tool. |
| 4 | Benchmarking on shadcn/ui with 20 tasks showed roughly 3x faster average edits | 00116 | VERIFIED | Explicit benchmark result. |
| 5 | Claude Code's built-in `@path/to/file` references are part of the cited evidence base here | 08403 / 00375 | UNSUPPORTED | Neither `08403` nor `00375` documents the `@` syntax or this traversal mechanism. |

### Entry 6: context-window-management-and-compaction.md

**Overall verdict**: FINDINGS  
**Claims checked**: 6  
**Issues found**: 4

| # | Claim (abbreviated) | Source Cited | Verdict | Notes |
|---|---------------------|-------------|---------|-------|
| 1 | The nominal context is 200K, but quality degrades well before that because of Lost in the Middle | 08764 | VERIFIED | This is a convergent finding in the synthesis. |
| 2 | Degradation is measurable at about 75%, making the effective window 120K-150K | 08764 | DISTORTED | The source presents ranges and uncertainty, not a settled threshold plus derived effective-window figure. |
| 3 | Auto-compaction is lossy and sources disagree on trigger thresholds | 08764 | VERIFIED | This is one of the synthesis's core conclusions. |
| 4 | Compaction preserves high-level decisions and recent files while losing older tool output and detailed history | 08764 | VERIFIED | Matches the documented preserve/discard lists. |
| 5 | The "<30% alert / <15% emergency handoff" vigilance protocol is established source-backed Claude Code practice | None | UNSUPPORTED | This is an uncited local protocol, not evidenced in the cited corpus. |
| 6 | One session beyond ~100K organic content becomes internally inconsistent, so pre-compaction handoff should happen at 70% | 08764 / 00025 / 10032 | UNSUPPORTED | The sources support fresh-session strategies generally, but not these specific thresholds or inevitability claims. |

### Entry 7: cowork-and-non-technical-access.md

**Overall verdict**: FINDINGS  
**Claims checked**: 6  
**Issues found**: 3

| # | Claim (abbreviated) | Source Cited | Verdict | Notes |
|---|---------------------|-------------|---------|-------|
| 1 | The "three worlds" segmentation of users is supported | 02088 | VERIFIED | Directly present in the extraction. |
| 2 | Outcome-first prompts against a structured filesystem are supported for non-technical users | 00289 | VERIFIED | The examples and framing in the article support this. |
| 3 | Cowork is a desktop GUI layer for Claude Code with the same agentic capabilities and direct local filesystem operation | 02088 / 10313 / 10411 / 00289 | UNSUPPORTED | The cited sources mention Cowork only lightly or not at all; they do not establish this detailed architecture. |
| 4 | Cowork itself was built in ten days using Claude Code | 10313 / 10411 | CITATION ERROR | `10313` mentions software built in ten days, but not Cowork specifically; `10411` is about Slack usage, not Cowork's build history. |
| 5 | Anthropic uses Claude Code in Slack for questions, feedback-to-PR, and prototyping by non-technical teams | 10411 | VERIFIED | This is the core content of the Slack post. |
| 6 | The compounding AI operating system folder structure compounds agent capability over time | 00289 | VERIFIED | Strongly supported by the article's main thesis. |

### Entry 8: extended-thinking-and-effort-control.md

**Overall verdict**: FINDINGS  
**Claims checked**: 6  
**Issues found**: 4

| # | Claim (abbreviated) | Source Cited | Verdict | Notes |
|---|---------------------|-------------|---------|-------|
| 1 | Claude Code has a settled keyword ladder mapping `think` / `think hard` / `ultrathink` to ~4K / ~10K / ~32K budgets | 08764 / CLAUDE.md | DISTORTED | `08764` explicitly presents this as disputed, and local `CLAUDE.md` says the keywords are cosmetic intent signals. |
| 2 | The operational resolution is to treat keywords as behavioral signals, not guaranteed budget switches | 08764 / CLAUDE.md | VERIFIED | This is consistent with both the synthesis and repo config. |
| 3 | Extended thinking is auto-enabled in this repo's Claude Code configuration | CLAUDE.md | VERIFIED | Stated directly in `CLAUDE.md`. |
| 4 | Session-level effort can be controlled with `--thinking-budget`, and prompt/session controls combine by a maximum-wins rule | 08764 / CLAUDE.md | UNSUPPORTED | The cited materials do not establish this CLI flag behavior or combination rule. |
| 5 | Architectural decisions, multi-step processing, and forensic analysis are recommended use cases | CLAUDE.md / 08764 | VERIFIED | The repo config explicitly says this, and the synthesis broadly aligns. |
| 6 | Reading the visible "thinking trace" is an important debugging practice | 08764 / 10857 / 00041 | UNSUPPORTED | None of the cited sources discusses visible thinking traces in this way. |

### Entry 9: filesystem-as-agent-memory.md

**Overall verdict**: FINDINGS  
**Claims checked**: 6  
**Issues found**: 4

| # | Claim (abbreviated) | Source Cited | Verdict | Notes |
|---|---------------------|-------------|---------|-------|
| 1 | Structured files and directories are the agent's persistent memory, and this memory compounds over time | 00289 / 00041 / 08764 | VERIFIED | This synthesis is well grounded across the cited sources. |
| 2 | Filesystem memory is categorically better than vector databases, RAG, or conversation history | 00289 / 00041 / 10857 / 08764 | DISTORTED | The sources argue strongly for file-based systems but do not support this blanket exclusionary ranking. |
| 3 | The CLAUDE.md hierarchy and on-demand subtree loading are part of the filesystem-memory pattern | 08764 | VERIFIED | Directly supported. |
| 4 | Markdown files as nodes, wiki links as edges, and YAML as metadata are supported by the tools-for-thought source | 00041 | VERIFIED | This is one of the source's central claims. |
| 5 | Multi-agent coordination can rely on git-backed files instead of a custom bus or shared database | 00289 / 10857 / 10825 / 00041 / 08764 | UNSUPPORTED | The cited sources imply file-mediated continuity, but not this stronger systems-architecture claim. |
| 6 | The phantom-path failure mode costing 16 sessions is a documented source-backed example for this entry | None | UNSUPPORTED | This is a repo-local anecdote with no citation in the entry's provenance. |

### Entry 10: hooks-and-permissions-architecture.md

**Overall verdict**: FINDINGS  
**Claims checked**: 6  
**Issues found**: 2

| # | Claim (abbreviated) | Source Cited | Verdict | Notes |
|---|---------------------|-------------|---------|-------|
| 1 | Hooks intercept before declarative permission rules, and rule evaluation is deny -> allow -> ask | 08764 | VERIFIED | This ordering is explicit in the synthesis. |
| 2 | Absent explicit config, every action requires approval because the default state is ask | 00001 / 08764 | DISTORTED | `00001` says a small set of safe commands is pre-approved by default, so "every action" is too strong. |
| 3 | Claude Code ships with a conservative set of pre-approved safe commands and exposes `/permissions` for expansion | 00001 | VERIFIED | Directly supported. |
| 4 | Hooks can block, approve, mutate inputs, and serve as organizational policy enforcement | 08764 | VERIFIED | Supported by hook response semantics and policy-gateway framing. |
| 5 | The system also uses prompt-injection detection, static analysis, and sandboxing as layers around permissions | 00001 | VERIFIED | Explicit in the customization thread. |
| 6 | The day-1 / week-1 / month-1 "progressive autonomy" rollout is documented source behavior | None | UNSUPPORTED | This is advisory synthesis, not a cited documented pattern. |

### Entry 11: mcp-as-integration-standard.md

**Overall verdict**: FINDINGS  
**Claims checked**: 6  
**Issues found**: 5

| # | Claim (abbreviated) | Source Cited | Verdict | Notes |
|---|---------------------|-------------|---------|-------|
| 1 | MCP is a standard protocol layer for connecting Claude Code to external tools and services | 08764 | VERIFIED | This is well supported in the synthesis. |
| 2 | MCP only operates over stdio and HTTP transports | 08764 | DISTORTED | `08764` also lists SSE and SDK/in-process transport types. |
| 3 | The Xcode example `claude mcp add --transport stdio xcode -- xcrun mcpbridge` is supported | 10513 | VERIFIED | Directly present. |
| 4 | The scope/paths table (`managed-mcp.json`, `.claude/mcp.json`, `~/.claude/mcp.json`) is accurate | 08764 | DISTORTED | The synthesis gives different locations (`.mcp.json`, `~/.claude.json`) and emphasizes scope complexity. |
| 5 | Desktop Extensions (DXT) are a documented part of the cited MCP evidence base | 08764 / 10513 / 10313 | UNSUPPORTED | None of the cited sources mentions DXT packaging. |
| 6 | MCP has already achieved broad cross-vendor adoption by Apple, Cloudflare, Cursor, Windsurf, and a plugin marketplace ecosystem | 10513 / 10313 / 08764 | UNSUPPORTED | Apple/Xcode is evidenced; the broader adoption-and-marketplace claim is not established by this source set. |

### Entry 12: plan-mode-and-human-in-the-loop.md

**Overall verdict**: FINDINGS  
**Claims checked**: 6  
**Issues found**: 4

| # | Claim (abbreviated) | Source Cited | Verdict | Notes |
|---|---------------------|-------------|---------|-------|
| 1 | Repo `CLAUDE.md` instructs agents to enter Plan Mode for directives touching more than 3 files or spanning multiple domains | CLAUDE.md | VERIFIED | Exact match to the local config. |
| 2 | `10825` supports team alignment before execution as an organizational pattern analogous to planning first | 10825 | VERIFIED | The morning-alignment practice is explicit. |
| 3 | Parallel planning agents can keep the main thread cleaner than doing all planning inline | 00025 | VERIFIED | This is directly supported by the planning-agents examples. |
| 4 | In Plan Mode, write tools are suppressed and the output contract becomes a plan document awaiting approval | 00025 / 10825 / 08764 / CLAUDE.md | UNSUPPORTED | None of the cited sources documents Plan Mode with this level of mechanical detail. |
| 5 | The plan document's required sections (current state, ordered changes, risks, success criteria) are source-backed Claude Code mechanics | 00025 / 08764 | UNSUPPORTED | This structure is plausible but not documented in the cited sources. |
| 6 | Plans are inherently ephemeral and should not be kept as durable artifacts | None | UNSUPPORTED | This is uncited process advice. |

### Entry 13: skills-and-progressive-disclosure.md

**Overall verdict**: FINDINGS  
**Claims checked**: 6  
**Issues found**: 4

| # | Claim (abbreviated) | Source Cited | Verdict | Notes |
|---|---------------------|-------------|---------|-------|
| 1 | Progressive disclosure as a context-management principle for Claude Code is supported | 10032 | VERIFIED | The video description explicitly frames progressive disclosure in these terms. |
| 2 | The anti-shelfware rule, bifurcation schema, wiring requirement, and consolidation logic are supported by the registry | 00419 | VERIFIED | These are all explicit in the registry. |
| 3 | Skills are markdown files in `.claude/skills/` or `~/.claude/skills/`, load only when invoked, and project scope overrides user scope | 10032 / 00419 / 00001 | UNSUPPORTED | Those concrete mechanics are not established by this cited source set. |
| 4 | The 30-skills x 500-tokens example and 10x token-savings calculation are supported evidence | 10032 | UNSUPPORTED | `10032` is only a short video description and does not provide these numbers. |
| 5 | Slack usage shows configuration investment and optional skills can improve non-technical question answering | 10411 | VERIFIED | This is supported, though only at a high level. |
| 6 | The 230-skill audit with 119 flagged and 111 cleared is supported | 00419 | VERIFIED | These exact counts appear in the registry. |

### Entry 14: sub-agent-architecture.md

**Overall verdict**: FINDINGS  
**Claims checked**: 6  
**Issues found**: 3

| # | Claim (abbreviated) | Source Cited | Verdict | Notes |
|---|---------------------|-------------|---------|-------|
| 1 | Sub-agents are separate agent instances with isolated context, not just function calls | 00025 / 00212 | VERIFIED | Both sources support genuine isolation and separate working contexts. |
| 2 | The built-in roster includes Bash, general-purpose, Explore, Planning, and Claude Code Guide, with Explore using Haiku | 00025 | VERIFIED | Directly supported by the walkthrough. |
| 3 | `Ctrl+B` launches background agents and multiple agents can be run in parallel | 00025 | VERIFIED | Explicit in the source. |
| 4 | Sub-agents cannot spawn additional sub-agents and execution is strictly two levels deep | 00025 / 08403 / 00212 | UNSUPPORTED | This is documented in `08764`, but not in this entry's cited sources. |
| 5 | The inline/fork/parallel delegation decision tree is supported | 08403 | VERIFIED | It is the core of that source. |
| 6 | The detailed 95K-vs-15K context-economics example is documented source evidence | 00025 / 08403 / 00212 | UNSUPPORTED | The sources support the general economics, but not this specific numerical scenario. |

## Summary

| # | Entry | Claims | Issues | Verdict |
|---|-------|--------|--------|---------|
| 1 | agent-first-engineering-culture.md | 6 | 3 | FINDINGS |
| 2 | agent-teams-and-parallel-orchestration.md | 6 | 3 | FINDINGS |
| 3 | autonomous-research-workflow.md | 5 | 2 | FINDINGS |
| 4 | claude-md-configuration-system.md | 6 | 3 | FINDINGS |
| 5 | context-injection-and-codebase-traversal.md | 5 | 2 | FINDINGS |
| 6 | context-window-management-and-compaction.md | 6 | 4 | FINDINGS |
| 7 | cowork-and-non-technical-access.md | 6 | 3 | FINDINGS |
| 8 | extended-thinking-and-effort-control.md | 6 | 4 | FINDINGS |
| 9 | filesystem-as-agent-memory.md | 6 | 4 | FINDINGS |
| 10 | hooks-and-permissions-architecture.md | 6 | 2 | FINDINGS |
| 11 | mcp-as-integration-standard.md | 6 | 5 | FINDINGS |
| 12 | plan-mode-and-human-in-the-loop.md | 6 | 4 | FINDINGS |
| 13 | skills-and-progressive-disclosure.md | 6 | 4 | FINDINGS |
| 14 | sub-agent-architecture.md | 6 | 3 | FINDINGS |
