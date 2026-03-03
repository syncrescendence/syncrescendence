# Claude Code on Desktop Features
**Claude** @claudeai · Feb 20
Claude Code on desktop can now preview your running apps, review your code, and handle CI failures and PRs in the background.
Here's what's new:
(Description: Video preview titled "Previews for Claude Code" showing a checkout form interface with error handling, console logs, and code execution at 0:19 timestamp)
---
**Claude** @claudeai · Feb 20
**Server previews:** Claude can now start dev servers and preview your running app right in the desktop interface.
It reads console logs, catches errors, and keeps iterating.
---
**Claude** @claudeai · Feb 20
**Local code review:** When you're ready to push, hit "Review code" and Claude leaves inline comments on bugs and issues before it goes to a full code review.
(Description: Code review interface showing src/exhibits/index.jsx with highlighted changes:
```jsx
// src/exhibits/index.jsx (+15 lines)
116  116    <ExhibitSlot key={3} exhibits={exhibits} position="southwest" />
117  -       <ExhibitSlot key={4} exhibits={null} position="southeast" />
118  +       <ExhibitSlot key={4} exhibits={exhibits} position="southeast" />
119  119    </div>
```
And src/components/ZooGrid.jsx with import statements:
```jsx
// Zoo Exhibit Registry (+11 lines)
12  12    // Zoo Exhibit Registry
13  13    import { SmallAviary } from './aviary.js';
14  14    import { SafariPark } from './safari.js';
15  15    import { ReptileHouse } from './reptile.js';
16  16    import { PettingZoo } from './petting.js';
```
)
---
**Claude** @claudeai · Feb 20
**PR monitoring:** Open a PR and Claude tracks CI in the background.
With auto-fix, it attempts to resolve failures automatically. With auto-merge, PRs land as soon as checks pass.
Work on your next task while Claude monitors the previous one.
(Description: PR monitoring dashboard showing CI status with metrics:
- In progress: 12
- Passed: 6
- Failed: 0
- Skipped: 4
- Auto fix: enabled (toggle on)
- Auto merge: disabled (toggle off)
- Branch information: main → claude/improve-subagent-rendering-cMd49
- Additional options: +23 -12, CI indicator, View PR link
- Environment: Opus 4.5
- Status: Ready to code)
---
**Claude** @claudeai · Feb 20
**Session mobility:** Sessions move with you now. Run /desktop to bring a CLI session into the desktop app, or push it to the cloud and pick it up from the web or your phone.
Update or download Claude Code on desktop to get started:
[Download Claude | Claude](https://t.co/hwPB3zlRQ4)