# Why you should use opencode(oc) over claude code(cc)
(Description: A stylized versus graphic with "opencode" in gray pixelated text on the left, a gold diagonal slash in the center, and "CLAUDE CODE" in orange/red pixelated text on the right against a dark background)
## Somewhat in order of importance:
> **model agnostic** - try new ones as soon as they come out (you even get free usage for the leading OSS ones kimi2.5, glm 5, mm 2.5...). This is becoming more and more important with every other lab releasing better and cheaper models by the minute.
> **it's OSS** so you can make a fix if you encounter something - hell use oc to make the fix (check though, don't submit slop)
> **really cool team** that actively engage with the community in discord, twitter, twitch streams... on the other hand, I don't know a single cc employee apart from the guy who's only been using cc to code cc. lol
> **oc built for a faster, keyboard oriented workflow.** This is the main reason of using a tui agent and being in the terminal - you're close to your code and env to work fasterrr. oc has every bind as configurable with support for stuff like <leader> key. You can interact with the dialog box while the agent runs instead of waiting for it to end or for you prompt box to be empty. LAUGHABLE that they don't support this, really.
> **cc is UX HELL!** If it wasn't immediately obvious to you, they really don't put much thought into it - unlike oc, where the opposite is true. Too much to show here; so check the video below.
> **The UI is night and day.** If you are blessed to have eyes, you'll know this at a glance. If you're gonna be spending hours on something - atleast let it be appealing to look at.
> **/share feature** so you can share your sessions with other's or just save and inspect them later yourself.
> **rewind and sessions** are so broken in cc, I don't understand how anyone puts up with it. It works flawlessly in oc. again, this should be another main reason for you to be using a tui agent - i.e, running parallel sessions and navigating them seemlessly. Ik this is fixable, but why don't they care to make it better already?!?
## The obvious stuff: performance and agentic ability
Performance and agentic ability is on par -- if not better -- in oc. It's effectively the same thing underneath, though with some nuance: cc edges out with newer additions to the agentic harness (stuff like plan mode for instance). They just have a bigger team that dogfoods these features before releasing to the public, while oc plays catch up. While I haven't benchmarked performance - oc uses a naive, yet promising tui library `opentui` that they develop in-house, with a rendering engine built with zig while cc uses `ink` which is an objectively worse primitive. Also, they don't own it + forking and changing the core of something so mature isn't really that easy or sustainable.
## Workflow comparison: UX demonstration
Showing oc vs. cc workflow to display UX by going over a task: Write a plan > check the current cost > change your mind and open up a new session > copy the output.
(Description: Embedded video showing split-screen workflow comparison with terminal interfaces, displaying Claude Code on the left with interface elements and an opencode interface on the right. Video timestamp shows 2:32)
### In cc:
- couldn't run commands while agent executing, cancelled but they didn't execute, so had to re-run.
- In new session, it trims the commands it runs for some reason.
- doesn't let you expand output with mouse - expanding with keybaord just opens up a new layout where you can't see the running agent and have to escape it seperately.
- copying the output has weird spacing
### In oc:
- can run commands while agent runs with customizable bindings. cost already displayed at the top and updates dynamically.
- everything the agent does is neatly presented to you - not in idiosyncratic toolcall syntax Bash('yaba gooba')
- ofcourse, you can copy outputs just fine.
---
this is just one scenario lol, I didn't even get into sessions and rewind.