# dmux Thread Archive
## Original Post
**We're open sourcing dmux.**
Our internal tool for running Codex and Claude Code swarms.
- tmux + worktrees + claude/codex/opencode
- hooks for worktree automation
- a/b claude vs codex
- manage worktrees
- multi-project per session
...more.
🔗 [dmux.ai](https://t.co/ImLyLY82pL)
(Description: Video thumbnail showing large orange text "dmux" with subtitle "Parallel agents with tmux and worktrees")
**7:33 AM · Feb 19, 2026** · 305.6K Views
---
## Thread Posts by Justin Schroeder
### Post 1: Coordinator Feature
**Feb 19, 2026**
One of my favorite features is to create a "coordinator". Just create a parent directory/repo that has lots of related projects under it. They are all excluded via .gitignore from the parent and each have their own git repo. These are not git submodules (🤮) Just simple directories, I generally have a root AGENTS/CLAUDE file to describe the structure.
Dmux will detect these sub-repositories and when you create a worktree in the root, will also create worktrees of all those sub-directories in the parent directory worktree. When you merge it will let you merge each of the children's worktrees.
For OSS maintainers like myself, with many related projects, this is a real game changer.
---
### Post 2: Something Exciting Coming
**Feb 19, 2026**
Something even more exciting is coming very soon...if you want early access for that bombshell join the waitlist here:
(Description: Screenshot showing "Standard AgentBuilder" interface with dark theme, displaying multiple panels with code, configuration options, and hierarchical navigation structure)
---
### Post 3: Inter-Agent Communication
**Feb 19, 2026**
This doesn't add any extra layers to the existing coding agents because each already has their own capacity for inter-agent and sub-agent communication.
---
### Post 4: Tmux Details
**Feb 19, 2026**
Tmux is perfect for all this stuff because it runs in a server and allows a full programming layer on top of it. We even have an experimental "autopilot" mode that can read the tmux stream and have an LLM help steer the AI. Also if your terminal crashes, no problem, just open a new one, go back to the directory, and run dmux and all your sessions will still be running.
---
### Post 5: Codex Preference
**Feb 19, 2026**
Codex on everything except ui
---
### Post 6: Branch Handling
**Feb 19, 2026**
If you're in a branch it creates the worktree as a branch off that
---
### Post 7: Dev-Centric Approach
**Feb 19, 2026**
More dev-centric. I'm personally a fan of TUI interfaces for most dev stuff, tmux is a boss too, if your terminal crashes for example, your agent sessions just keep running.
And as TUI you can just use CC/Codex however you normally would
---
### Post 8: Conflict Resolution
**Feb 20, 2026**
It'll ask you if you want to spin up another agent pane to resolve the conflicts
---
### Post 9: Tmux Configuration
**Feb 20, 2026**
Depends how you setup tmux. If you used our config you can click on it, or use ctrl-option and an arrow to navigate between panes. If you didn't use our tmux config, lookup pane switching in tmux
---
### Post 10: AI Naming
**Feb 20, 2026**
That's why ai names ours automatically
---
### Post 11: JavaScript CLIs
**Feb 20, 2026**
we cannot
---
### Post 12: Real Codebase Question
**Feb 19, 2026**
what's a "real" codebase, and why would one not work on your own machine?
Also, its just tmux, you can run it on any server if thats your cup o tea
---
### Post 13: Error Recovery
**Feb 19, 2026**
Try unplugging your computer and then plug it back in and restart.
---
### Post 14: Agent Pair
**Feb 19, 2026**
I've got a pair of agents
---
### Post 15: Claude Subscription
**9 hours ago**
I mean it just uses your Claude code so yes. Only thing it needs other than that is an openrouter key and it will last for months on $10
---
### Post 16: Botany Work
**12 hours ago**
This botany work that way
---
### Post 17: Team Behind dmux
**7 hours ago**
Team from FormKit.com, tempo, auto-animate, drag-and-drop... and our new thing which you can get on the waitlist for at standardagentbuilder.com
(Description: Card showing FormKit framework information - "The Open-Source Form Framework" with FormKit logo and description: "FormKit equips developers to build their forms 10x faster by simplifying form structure, generation, validation, theming, submission, error handling, and more.")
---
### Post 18: Simple Response
**21 hours ago**
Ok
---