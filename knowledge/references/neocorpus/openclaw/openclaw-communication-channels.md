# OpenClaw: Multi-Platform Communication Channels

## Provenance

| Source File | Content |
|-------------|---------|
| `corpus/openclaw/10802.md` | Slack integration: daily automations, business operations, revenue impact |
| `corpus/openclaw/10833.md` | Discord server structure: per-agent channels, threads, model selection |
| `corpus/openclaw/10907.md` | iMessage CLI v0.5.0: typing indicators, reactions, events |

---

## The Pattern

Agents communicate through the platforms humans already use. OpenClaw does not impose a new interface — it meets operators in Slack, Discord, or iMessage. The platform choice reflects the use case: business operations run through Slack, multi-agent orchestration through Discord, personal/mobile interaction through iMessage.

---

## Slack — Business Operations

Slack is the recommended entry point for operators running a business. Four hours of setup yields a functioning chief of staff inside the existing workspace.

Documented automations (10 days post-setup, resulted in doubled MRR):

- Daily report generation
- Pre-call research preparation
- Overdue project chasing
- Daily team check-ins
- Client message drafting (in operator's voice)
- Urgent email flagging
- Live revenue and margin tracking
- Script-to-editor-ready brief conversion
- Tool building during off-hours
- Follow-up on unanswered items
- Proposal generation
- Client detail retention
- 9 background automations running daily
- 24/7 team accountability

The Slack integration positions the agent as a chief of staff embedded in the operator's existing communication layer, not a separate tool requiring context-switching.

---

## Discord — Multi-Agent Channel Architecture

Discord structures multi-agent deployments through dedicated channels per agent and per functional area.

Example structure from a live deployment:

**General** (agent-scoped channels):
- `#ecco` — agent workspace (Testing Codex Spark)
- `#gordon` — agent workspace (Remarketing Plan, Multi-Language Expansion, Landing Page Testing System, Keyword Maintenance System, RSA Cluster Intel + Improvement)
- `#zero` — agent workspace (test/placeholder)
- `#group-chat` — multi-agent coordination

**Areas** (functional channels):
- `#personal-assistant`, `#content-marketing`, `#health-and-fitness`, `#openclaw`, `#meal-planning`

**Projects** (task-scoped channels):
- `#fitness-dashboard`, `#loop-dashboard`

Channels and threads are created and closed liberally. Threads serve as context containers — ongoing work in a thread preserves conversational history for the agent without polluting the channel. Model selection is configured per channel, enabling different agents to run different models in their dedicated workspaces.

Agent separation is for hyper-focus, not architectural necessity. Two agents (Ecco and Gordon) handled the documented workload; the third was a test.

---

## iMessage — Native Apple Integration

iMessage CLI (imsg, v0.5.0) brings OpenClaw agents into the native Apple messaging layer.

Capabilities added in v0.5.0:
- Typing indicators (via `typing indicator` command + RPC methods with stricter validation)
- Reactions support (`--reactions` flag on the `watch` command)
- Events support

BlueBubbles is documented as an alternative plugin. The longer-term default between imsg and BlueBubbles was unsettled at time of writing.

iMessage integration targets personal and mobile use cases where Slack and Discord are not the primary interface.

---

## Channel Architecture Principles

**Threads as context containers.** A thread preserves the conversational history an agent needs to continue a task without polluting the broader channel. Create and close liberally — they are cheap and reversible.

**Channels as agent scoping.** A dedicated channel per agent concentrates that agent's work and allows model selection to be configured at the channel level. Functional area channels (health, content, projects) organize work by domain, not by agent.

**Platform choice based on use case.**

| Platform | Primary Use Case |
|----------|-----------------|
| Slack | Business operations, team coordination, operator is running a company |
| Discord | Multi-agent orchestration, developer/power-user workflows, model-per-channel routing |
| iMessage | Personal assistant, mobile, native Apple ecosystem |

The unifying principle: the agent adapts to the human's communication context. The human does not migrate to a new tool.

---

## Temporal Dimensions

### Supersession: iMessage CLI Version Chain

Source `10907.md` documents iMessage CLI at **v0.5.0** with a specific capability set added in that version: typing indicators (via `typing indicator` command and RPC methods with stricter validation), reactions support (`--reactions` flag on the `watch` command), and events support. The version number and the feature-level description of what v0.5.0 added implies a prior version without those capabilities — a version chain where v0.4.x or earlier had the core watch/send primitives but lacked real-time presence signals.

The lesson this encodes: native messaging integration began as pure request-response (send message, receive reply) and grew presence semantics — typing indicators, reactions — as operators demanded more natural conversational feel. The direction of travel is toward indistinguishability from a human messaging contact.

### Obsolescence: The Unsettled Default

Source `10907.md` explicitly notes the longer-term default between imsg and BlueBubbles was unsettled at time of writing. This is an obsolescence signal about a design decision: the iMessage CLI integration was the current solution, but it was not declared final. The assumption was that one integration would emerge as canonical; which one was unknown. Any downstream documentation treating either as the definitive iMessage path may have been superseded by subsequent resolution of this choice.

**Phase 3-4 audit (CC78a)**: iMessage CLI version chain (v0.5.0 capability additions) and unsettled-default obsolescence signal both present in source 10907. Slack and Discord sources (10802, 10833) do not contain version chains or temporal evolution signals.
