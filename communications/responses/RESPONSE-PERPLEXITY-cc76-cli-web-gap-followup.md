# Perplexity Verification Response — CLI/Web Gap Follow-Up

- Slug: `cc76-cli-web-gap-followup`
- Source: Perplexity (Claude Sonnet 4.6 model)
- Retrieved: 2026-03-02
- Perplexity URL: https://www.perplexity.ai/search/we-need-a-narrow-factual-verif-oHkp9bwpRuSFJjNh5Tx5oA

---

Here is a rigorous, question-by-question factual verification based on official Anthropic sources and closely adjacent documentation. Each item is labeled as **Verified Fact**, **Plausible / Unverified**, or **Explicitly Unsupported**.

---

## 1. Cowork + Folder Grounding

**Verified Fact.** Cowork requires you to designate a specific local folder as its working context. Within that folder, it can read existing files, modify them, and create new files. Anthropic stated directly on X: *"In Cowork, you grant access to a folder on your computer. [Claude] can then read, modify, or create files within that folder."* Tasks are executed inside an isolated virtual machine sandboxed to that folder — Cowork cannot roam your entire filesystem. [1][2]

**Constraint worth noting:** The sandbox is the point of confinement. Folder-based job relay is realistic and explicitly supported, but multi-folder or cross-drive access requires explicitly granting additional folder mounts. Cowork cannot self-expand its own file access scope. [2]

---

## 2. Claude in Chrome: Browser Execution

**Verified Fact.** Claude in Chrome is an official Anthropic Chrome extension (currently beta, available to all paid subscribers at Pro tier and above). It can navigate pages, click buttons, fill forms, run multi-step processes across multiple tabs, and complete scheduled workflows. The official claude.com/chrome page explicitly states it supports "scheduled workflows" set to run daily or weekly without manual triggers. [3][4]

**Verified Fact — Cowork integration.** The official Anthropic page at claude.com/chrome explicitly documents the Cowork handoff: *"Chrome navigates and gathers information, Cowork produces Excel models, comparison decks, and reports without having to copy and paste."* Context flows automatically from Chrome to Cowork without manual copy-paste. This confirms that a Cowork task can invoke Claude in Chrome as part of its execution path — this is officially documented, not inferred. [5]

---

## 3. File Uploads in Claude in Chrome

**Plausible / Partially Verified.** The official Chrome Web Store listing and claude.com/chrome page describe Claude in Chrome's capabilities in terms of browser-native interaction: navigating sites, clicking, filling forms, and extracting information from web content. There is **no explicit official statement** from Anthropic confirming that Claude in Chrome supports direct file uploads to third-party sites like NotebookLM or Perplexity as a documented capability. [6]

**Plausible inference:** Because Claude in Chrome can click buttons and fill forms, it could in principle trigger a file input element on a third-party site. However, operating a native OS file picker (which is what file upload buttons open) is a known hard constraint for browser automation agents — it typically requires OS-level access, not just browser DOM control. Whether Cowork's local file access bridges this gap is not officially documented. **Treat this as experimental.**

---

## 4. State, Continuation, and Long-Running Workflows

**Verified Fact.** Claude in Chrome maintains context across tabs during a session — the official description notes it *"maintains context of everything happening in their browser"*. The claude.com/chrome page confirms background task completion and scheduled recurrence. [4][7]

**Partially Verified.** Claude in Chrome can record workflows for reuse: *"Record common browser workflows and let Claude handle them automatically"*. This constitutes a form of workflow continuation. [6]

**Plausible / Unverified — long-running chained complexity.** There is no official documentation specifying a session state limit, a maximum number of chained steps, or a timeout ceiling. Third-party hands-on guides note that well-defined tasks of 7–10 steps complete reliably, but complex or indefinitely long chained actions are not officially characterized as supported or unsupported. **Treat multi-dozen-step chains as experimental.** [8]

---

## 5. Programmability, Developer Hooks, and Automation Surface

**Partially Verified.** The official claude.com/chrome FAQ notes: *"Developers can use Claude Code to build and test directly in Chrome. This integration enables faster iteration on browser-based projects."* Claude in Chrome and Claude Code communicate via MCP (Model Context Protocol), which keeps context synced across terminal and browser sessions. [9]

**Explicitly Unsupported (as of current official documentation).** There is no official Anthropic API, webhook, or programmatic trigger surface for Claude in Chrome itself — no documented way to invoke it headlessly, script it externally, or embed it as a callable service. The current model is purely interactive and task-driven, initiated by a user prompt or a pre-recorded workflow. **This is a hard architectural boundary to note: you cannot, from code, call "Claude in Chrome, go do X" the way you would call an API.**

---

## 6. Factual Verdict

| Prototype | Strength of Current Official Capability | Experimental Risk |
|---|---|---|
| **Perplexity browser relay** | Moderate — Chrome can navigate and extract from Perplexity; Cowork can receive that data and produce outputs [5][10] | The relay depends on Chrome→Cowork context handoff working reliably end-to-end; no official SLA on handoff fidelity |
| **NotebookLM upload + synthesis** | Low-to-moderate — Chrome can navigate NotebookLM; file upload via native OS picker is unverified officially | File upload capability to third-party sites is the single largest unverified assumption; treat as experimental, not architectural fact |

### What is verified and safe to architect around:

- Cowork folder read/write with explicit folder grant [10]
- Chrome multi-step browser interaction + scheduled/recorded workflows [5]
- Native Chrome→Cowork handoff with automatic context transfer [5]

### What must be treated as experimental:

- File upload to third-party sites (OS file picker access from Chrome agent) — not officially documented
- Complex chained workflows beyond ~10 steps — no official characterization of limits
- Any programmatic invocation of Claude in Chrome from external code — explicitly absent from official documentation; no developer hook exists [5]

**The Cowork + Claude in Chrome stack is strong enough to be a first execution layer for research-gather → local-synthesis workflows (e.g., competitor research → PowerPoint). It is not yet verified as a reliable execution layer for upload-dependent workflows like NotebookLM ingestion until the file-picker question is empirically tested or officially clarified.**

---

## Sources

1. letsdatascience — https://letsdatascience.com/blog/anthropic-launches-claude-cowork-the-agent-that-lives-on-your-...
2. letsdatascience (same article, folder constraints)
3. pcmag — https://www.pcmag.com/news/anthropic-rolls-out-its-chatbot-claude-as-a-chrome-extension
4. techcrunch (Claude in Chrome capabilities)
5. claude.com/chrome — https://claude.com/chrome (official Anthropic page)
6. chromewebstore.google — Chrome Web Store listing for Claude in Chrome
7. techcrunch (context maintenance across tabs)
8. datacamp — hands-on guide to Claude in Chrome step limits
9. aimaker.substack — MCP integration between Claude Code and Chrome
10. venturebeat — https://venturebeat.com/technology/anthropic-launches-cowork-a-claude-desktop-agent...

---

*Prepared using Perplexity with Claude Sonnet 4.6 — 25 citations referenced in original response.*
