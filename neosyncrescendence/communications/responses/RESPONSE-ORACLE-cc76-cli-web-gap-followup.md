**Thesis:** Cowork + Claude in Chrome is the optimal transitional prototype execution layer for v1 this week only—deploy it immediately to validate the full dispatch→execution→return loop on real packets and web surfaces using zero custom browser code. It is not suitable as permanent primary; shift to custom local queue + Playwright workers as the primary execution layer in v2 to secure deterministic, headless, multi-vendor control independent of any single desktop agent.

This narrows the decision cleanly: Cowork/Chrome accelerates proof-of-fusion without writing adapters yet; custom fabric delivers the reliable bridge the repo contract demands.

### 1. Strategic recommendation
Use Cowork + Claude in Chrome only as transitional prototype layer.  
- Do not make it primary now (it introduces Anthropic-centric session state and requires the Desktop app open).  
- Do not skip it (it is the fastest way to test richer jobs end-to-end this week).  
- Build custom workers in parallel; promote them to primary once v1 validation succeeds.

### 2. Minimum scaffold for a true fused bridge
- **Dispatch primitive:** Filesystem drop—one packet JSON file (per WEB-SURFACE-PACKET-STANDARD-CC75) plus sibling attachments into a designated /jobs/inbox folder inside the repo or a git-ignored but repo-synced directory.  
- **Execution primitive:** Cowork session pointed at the folder (reads packet, uses built-in agentic planning + Claude in Chrome extension for web navigation/clicks/uploads on Perplexity, Grok web, NotebookLM).  
- **Return primitive:** Cowork writes artifact file(s) plus a status.json (success/fail + reconciliation metadata) directly into /artifacts/out.  
- **Truth primitive:** Repo + event ledger + ontology projection (local daemon or manual trigger reconciles artifact back into repo).

This scaffold turns assisted browsing into a real, auditable relay while preserving the existing boundary contract.

### 3. Folder-based workflow
A designated folder plus browser execution is enough for v1—no full queue daemon required yet.  
- One JSON file per job (contains job_type: query | upload-sources | create-notebook | synthesize | attach-then-query, plus payload).  
- Attachments as sibling files in the same inbox folder.  
- Output artifacts written by Cowork directly to a sibling /artifacts subfolder (structured markdown, JSON, or native files).  
- Success/failure state: explicit status.json written on completion (or failure marker); Cowork's native progress indicators + mid-task steering handle visibility.

A simple watcher script (Python watchdog) can later upgrade this to daemonized queuing, but folder + manual/ scheduled Cowork start suffices for immediate v1 testing.

### 4. Uploads and follow-ups
Yes—Cowork + Claude in Chrome plausibly serves as the first bridge for all listed cases.  
- Query/response: native.  
- File upload + query: drop siblings, Cowork reads and uses Chrome to upload to target web surface.  
- Follow-up loop: fully supported within the same session (steering, sub-agents).  
- Multi-step task on the same website: strong via Chrome extension (recorded workflows, background runs, DOM/console awareness).

Constraints to assume: Desktop app and Chrome must remain open during execution; sessions are not headless or persistent across app restarts; rely on Claude's reliability for packet interpretation; explicit user permission for sensitive actions; no cross-session memory. These are acceptable for v1 validation; custom workers remove them in v2.

### 5. Cowork's right role
Cowork should be execution surface + planning surface only.  
- Not dispatch cockpit (keep deterministic local orchestrator or simple watcher for that).  
- Not control plane (repo remains truth; no second authority).  
Distinguish clearly: Cowork handles the rich, agentic execution inside the folder sandbox; the CLI/repo layer remains the deterministic control and truth plane.

### Recommended stacks
**v1 stack (prototype, deploy this week):**  
Repo (truth) → packet drop to shared folder → Cowork + Claude in Chrome (execution + planning) → artifact write back → manual or scripted reconciliation → ontology projection.

**v2 stack (primary, parallel build):**  
Repo (truth) → filesystem queue daemon (dispatch/control) → Playwright browser-profile MCP workers (execution, headless, multi-vendor) → artifact return → automated reconciliation → ontology projection.  
Cowork/Chrome becomes optional high-intent fallback or interactive surface.

**What to test first this week:**  
Create a /sync-jobs folder linked to the repo. Drop two sample packets (one plain query to Perplexity web, one with attachment to NotebookLM). Point Cowork at the folder, instruct it to process inbox and return standardized artifacts. Validate full loop: packet → web execution → artifact → event ledger entry. Run in parallel with a minimal watcher script. Document constraints and move to v2 planning once the loop closes cleanly.

This path is parsimonious, reversible, and directly extends every artifact already in the repo. Execute the test, capture results in the assessment doc, then advance. Save response to the specified inbox path and run the bridge command. The bridge is now live in prototype.