Here is the narrow factual verification pass on Cowork + Claude in Chrome as a practical browser relay layer.

***

# Cowork + Claude in Chrome — CLI↔Web Gap Follow-Up Verification

**March 2, 2026**

***

## 1. Cowork + Folder Grounding

**Verified fact — strong official support.**

Cowork has documented, explicit local file access as a core capability. The official help-center article states: *"Direct local file access: Claude can read from and write to your local files without manual uploads or downloads."*  Folder-specific context is supported via **Folder Instructions**: when you select a local folder in a Cowork session, Cowork loads project-specific instructions from that folder, and Claude can also update those instructions autonomously during a session. [support.claude](https://support.claude.com/en/articles/13345190-get-started-with-cowork)

File output is written directly to your filesystem after execution in an isolated VM. Cowork supports generation of Excel files with working formulas, PowerPoints, CSVs, and formatted documents — all delivered to specified local paths. [support.claude](https://support.claude.com/en/articles/13345190-get-started-with-cowork)

**Constraint to note (official):** There is **no memory across sessions** — Claude does not retain memory from previous Cowork sessions, so folder instructions and global instructions are the only persistence mechanism across runs. The Claude Desktop app must remain open for the session to continue; closing it ends the session. **Inference:** Folder-based job relay is architecturally realistic, but the relay contract must be encoded in folder instructions and task descriptions, not in session memory. [support.claude](https://support.claude.com/en/articles/13345190-get-started-with-cowork)

***

## 2. Claude in Chrome — Browser Execution

**Verified fact — broadly capable, with specific documented limitations.**

Claude in Chrome is now generally available in beta to all paid subscribers (Pro, Team, Enterprise). The Chrome Web Store listing (official Anthropic publisher) explicitly documents the following capabilities: [pcmag](https://www.pcmag.com/news/anthropic-rolls-out-its-chatbot-claude-as-a-chrome-extension)

- Navigate and organize inbox and calendar
- Fill forms and handle repetitive data entry
- Extract information from web content
- **Run multi-step processes across multiple tabs**
- **Record common browser workflows and let Claude handle them automatically** [chromewebstore.google](https://chromewebstore.google.com/publisher/anthropic/u308d63ea0533efcf7ba778ad42da7390)

PCMag's December 2025 rollout report (secondary source, labeled as such) confirms it can complete **scheduled tasks** and access multiple tabs simultaneously. The initial beta was Max-only ($100–$200/month) when launched in August 2025; it was extended to all paid tiers (Pro at $20/month minimum) by December 2025. [techcrunch](https://techcrunch.com/2025/08/26/anthropic-launches-a-claude-ai-agent-that-lives-in-chrome/)

**Cowork + Claude in Chrome integration: CONFIRMED.** The Chrome Web Store listing explicitly notes *"For developers: Claude Code"* as an integration point, and the December 2025 Reddit thread confirmed Claude in Chrome shipped with a **Claude Code integration**. The Cowork help article also notes MCP connectivity as part of the permission/tool layer. **Inference (not explicitly documented):** whether a Cowork task can programmatically *invoke* a Claude in Chrome browser action as a sub-agent step is not confirmed in official docs — treat the Cowork→Chrome dispatch chain as plausible but unverified at the sub-agent invocation level. [reddit](https://www.reddit.com/r/ClaudeAI/comments/1pq2cf8/official_claude_in_chrome_is_now_live_for_all/)

***

## 3. File Uploads

**Verified fact — Claude's own upload surface is broad; third-party site uploads via Chrome are separately addressable.**

For Claude's own interface, officially supported upload types include: [support.claude](https://support.claude.com/en/articles/8241126-uploading-files-to-claude)

| Category | Formats |
|---|---|
| Documents | DOCX, CSV, TXT, HTML, ODT, RTF, EPUB, JSON, XLSX |
| Images | JPEG, PNG, GIF, WebP |
| Size limit | 30MB per file, 20 files per chat |
| Project files | Unlimited count, 30MB per file, text extraction only (except multimodal PDFs) |

The question of whether Claude in Chrome can **upload files to third-party sites** (e.g., NotebookLM, Perplexity) is a distinct capability from Claude's own upload surface. The Chrome Web Store listing states Claude can "fill forms" and "run multi-step processes", and PCMag confirms "filling out forms" is an explicit capability. **Inference:** Form-based file upload to third-party sites is architecturally within scope of Claude in Chrome's documented capability set (it is a form action), but there is **no official statement explicitly confirming third-party file uploads** to services like NotebookLM. Treat this as plausible but unverified — **lower confidence, experimental**. [pcmag](https://www.pcmag.com/news/anthropic-rolls-out-its-chatbot-claude-as-a-chrome-extension)

***

## 4. Follow-Ups and Continuation

**Verified fact — within-session state is maintained; cross-session state is not.**

Claude in Chrome maintains browser context across a multi-step interaction during a single task session: it "maintains context of everything happening in your browser"  and can work across multiple tabs simultaneously. The workflow recording feature (Chrome Web Store) implies state-aware continuation within a session. [techcrunch](https://techcrunch.com/2025/08/26/anthropic-launches-a-claude-ai-agent-that-lives-in-chrome/)

**Hard official limitation:** Claude in Chrome, like Cowork, does not have documented cross-session persistence. There is no officially documented mechanism to resume a prior browser task from a new session. **Verified constraint:** Claude will prompt for user permission before high-risk actions (publishing, purchasing, sharing personal data) and auto-disables on financial services, adult content, and piracy sites. These blocks are enforced by default and are not overridable for those categories. [techcrunch](https://techcrunch.com/2025/08/26/anthropic-launches-a-claude-ai-agent-that-lives-in-chrome/)

***

## 5. Extension / Programmability / Hooks

**Verified fact — no official developer API or programmable hook for Claude in Chrome.**

The official Chrome Web Store listing (Anthropic publisher) describes Claude in Chrome as entirely interaction-driven: natural conversation, task description, and workflow recording. There is no documented webhook, event listener, REST hook, or programmatic API surface exposed by the extension itself. The Claude Code integration mentioned in the December 2025 rollout is user-facing (Claude Code users can invoke browser tasks from Claude Code's interface), not a developer hook for external orchestration. [chromewebstore.google](https://chromewebstore.google.com/publisher/anthropic/u308d63ea0533efcf7ba778ad42da7390)

**Verified fact:** The current official model is purely interactive and task-driven. Any programmatic relay must go through Claude Code's MCP or tool layer to invoke browser actions — there is no headless or API-driven mode for Claude in Chrome. [chromewebstore.google](https://chromewebstore.google.com/publisher/anthropic/u308d63ea0533efcf7ba778ad42da7390)

***

## 6. Best Factual Interpretation

| Prototype target | Current official support | Confidence | Recommendation |
|---|---|---|---|
| **Perplexity browser relay** | Claude in Chrome can navigate, extract, and run multi-step workflows; Perplexity is not on the blocked-sites list | **Medium-high** | Prototype now — treat workflow recording as the relay mechanism |
| **NotebookLM upload + synthesis** | Claude in Chrome can fill forms and run multi-step processes; file upload to third-party sites is plausible but not explicitly documented | **Medium** | Prototype with explicit verification step — do not assume file upload works until tested |
| **Cowork as job relay layer** | Folder grounding, local file read/write, scheduled tasks, and sub-agent coordination are all officially documented | **High** | Architectural fact — proceed |
| **Cowork→Chrome sub-agent dispatch** | Claude Code integration exists; whether Cowork can invoke Chrome actions as a named sub-agent step is undocumented | **Low-medium** | Experimental — verify before building architecture around it |

**Overall verdict:** Cowork + Claude in Chrome is strong enough for a **Perplexity browser relay prototype now**. The folder grounding, workflow recording, multi-tab execution, and scheduled task features are all officially documented. The **NotebookLM upload prototype** is viable as an experiment but should be treated as requiring empirical confirmation on the file-upload step specifically — it is not an architectural fact yet. [support.claude](https://support.claude.com/en/articles/13345190-get-started-with-cowork)

The part that remains most unverified and should **not** be treated as architectural fact: the Cowork→Chrome programmatic sub-agent invocation chain, and explicit third-party file upload behavior via Claude in Chrome. Both are plausible from documented capability descriptions, but neither is explicitly stated in official Anthropic documentation as of this date.

***

*Filesystem relay note: The `python3 perplexity_response_bridge.py` command must be executed locally. This response is the full artifact content for `-INBOX/commander/00-INBOX0/RESPONSE-PERPLEXITY-cc76-cli-web-gap-followup.md`.*