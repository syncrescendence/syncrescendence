# OpenClaw Phone & Voice Integration

## Provenance

| # | Source File | Corpus Path | Content |
|---|-------------|-------------|---------|
| 1 | `00111.md` | `corpus/openclaw/00111.md` | Inbound calls via ElevenLabs Agents + Twilio + ngrok tunneling |
| 2 | `00197.md` | `corpus/openclaw/00197.md` | Outbound calls via skill installation, autonomous cron-triggered calling |

---

## Architecture

OpenClaw phone/voice integration is a two-layer system where each layer owns a distinct responsibility:

```
Twilio (phone network)
        ↕  [SIP/PSTN]
ElevenLabs Agents (voice orchestration)
  - Turn-taking
  - Speech synthesis (TTS)
  - Speech recognition (STT)
  - Phone number integration
        ↕  [OpenAI /chat/completions protocol]
OpenClaw (intelligence layer)
  - Tools
  - Memory
  - Skills
```

**The seam**: ElevenLabs connects to OpenClaw via the standard OpenAI `/chat/completions` endpoint. ElevenLabs sends the full message history on every turn, providing complete conversation context to OpenClaw without any special state management. OpenClaw never handles audio — ElevenLabs owns everything voice.

This architecture is **bidirectional**: the same protocol stack (Twilio + ElevenLabs + `/chat/completions` + OpenClaw) handles both inbound calls (human calls the bot) and outbound calls (bot calls the human).

---

## Inbound Setup

Inbound calls route: **Phone call → Twilio number → ElevenLabs Agent → ngrok tunnel → OpenClaw `/v1/chat/completions`**

### 1. Enable the chat completions endpoint in OpenClaw

In `~/.openclaw/openclaw.json`:

```json
{
  "gateway": {
    "http": {
      "endpoints": {
        "chatCompletions": {
          "enabled": true
        }
      }
    }
  }
}
```

This exposes `/v1/chat/completions` on the gateway port (default: `18789`).

### 2. Expose OpenClaw via ngrok

```bash
ngrok http 18789
```

ngrok returns a public HTTPS URL, e.g. `https://your-unique-url.ngrok-free.app`. Keep the terminal open — the URL changes on restart.

### 3. Configure ElevenLabs Agent

**Option A — Manual (ElevenLabs dashboard)**:
1. Create a new ElevenLabs Agent
2. Under LLM settings, select **Custom LLM**
3. Set the URL to: `https://your-unique-url.ngrok-free.app/v1/chat/completions`
4. Add your OpenClaw gateway token as the authentication header (from `~/.openclaw/openclaw.json` under `gateway.auth.token`)

**Option B — Programmatic (coding agent executes)**:

Step 1 — Store the gateway token as a secret in ElevenLabs:
```bash
curl -X POST https://api.elevenlabs.io/v1/convai/secrets \
  -H "xi-api-key: YOUR_ELEVENLABS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "new",
    "name": "openclaw_gateway_token",
    "value": "YOUR_OPENCLAW_GATEWAY_TOKEN"
  }'
```

Response:
```json
{"type": "stored", "secret_id": "abc123...", "name": "openclaw_gateway_token"}
```

Step 2 — Create the agent, referencing the secret by ID:
```bash
curl -X POST https://api.elevenlabs.io/v1/convai/agents/create \
  -H "xi-api-key: YOUR_ELEVENLABS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_config": {
      "agent": {
        "language": "en",
        "prompt": {
          "llm": "custom-llm",
          "prompt": "You are a helpful assistant.",
          "custom_llm": {
            "url": "https://YOUR_NGROK_URL.ngrok-free.app/v1/chat/completions",
            "api_key": {"secret_id": "RETURNED_SECRET_ID"}
          }
        }
      }
    }
  }'
```

Substitutions:
- `YOUR_ELEVENLABS_API_KEY` — ElevenLabs API key
- `YOUR_OPENCLAW_GATEWAY_TOKEN` — from `~/.openclaw/openclaw.json` at `gateway.auth.token`
- `YOUR_NGROK_URL` — ngrok subdomain
- `RETURNED_SECRET_ID` — `secret_id` from step 1

### 4. Attach a Twilio phone number

1. Purchase a phone number in Twilio
2. In the ElevenLabs agent settings, go to the **Phone** section
3. Click **Manage credentials** and enter Twilio Account SID and Auth Token
4. Connect the Twilio number to the agent

At this point, calling the Twilio number reaches OpenClaw via ElevenLabs voice orchestration.

---

## Outbound Setup

Outbound calls require the ElevenLabs inbound integration to already be configured (same Twilio + ElevenLabs Agent stack). The outbound capability is then layered on top via an OpenClaw skill.

### 1. Install the ElevenLabs skill

Tell OpenClaw:
```
Install these skills globally: npx skills add elevenlabs/skills
```

### 2. Configure the API key

```bash
openclaw dashboard
```

Navigate to the Skills tab, find the **agents** entry, and enter the ElevenLabs API key.

Security note: create a dedicated ElevenLabs API key scoped to `agents-write` only, with a spend limit.

### 3. Initiate a call

Tell OpenClaw:
```
Call <your phone number> using agents skill
```

OpenClaw will prompt for two IDs on the first call:
- **Agent ID** — found on the ElevenLabs Agent page (top of the interface)
- **Outbound Phone ID** — found in the ElevenLabs Phone Numbers tab

After the first successful call, persist these IDs:
```
Put these IDs in your memory
```

On subsequent calls, OpenClaw retrieves the IDs from memory and calls autonomously.

---

## Session Continuity

By default, each call spins up a fresh OpenClaw agent instance. The only shared state is OpenClaw's persistent memory layer.

To make all calls share a single agent instance (preserving full in-session context across calls), add the `x-openclaw-session-key` header to the Custom LLM configuration in ElevenLabs:

| Header | Value |
|--------|-------|
| `x-openclaw-session-key` | A stable, consistent key identifying the shared session |

This is configured in the **Request Headers** section of the Custom LLM settings in the ElevenLabs Agent. With this header present, ElevenLabs routes all calls through the same OpenClaw agent instance rather than creating a new one per call.

---

## Autonomous Calling

OpenClaw can initiate outbound calls without human prompting via cron scheduling.

Two setup paths:

**Path 1 — OpenClaw UI**: Add a cron job in the OpenClaw dashboard interface.

**Path 2 — Natural language**: Tell OpenClaw:
```
Set up a cron job to call me at 7am every morning with a daily briefing
```

OpenClaw will configure the cron schedule and use the persisted Agent ID and Outbound Phone ID from memory to execute the call autonomously.

Use cases:
- Morning briefing (daily digest of events, tasks)
- Failure alerts (coding agent failed, trigger on error condition)
- Progress check-ins (gym tracking, habit monitoring)
- Any event-driven or time-driven notification that benefits from voice

---

## The Unified Architecture

Both inbound and outbound calls operate on the same protocol stack:

```
Direction    Phone Network    Voice Layer          Intelligence Layer
---------    -------------    -----------          ------------------
Inbound      Twilio number    ElevenLabs Agent  →  OpenClaw /v1/chat/completions
Outbound     Twilio number    ElevenLabs Agent  ←  OpenClaw (via agents skill)
```

The ElevenLabs Agent is the constant: it owns voice (TTS, STT, turn-taking, telephony) in both directions. OpenClaw owns intelligence in both directions. The `/chat/completions` protocol is the seam in both directions.

Session continuity (`x-openclaw-session-key`) applies to both directions — any call, regardless of who initiated it, can share a single agent instance if the header is present in the Custom LLM config.

The only asymmetry is initiation: inbound calls are initiated by the human dialing Twilio; outbound calls are initiated by OpenClaw via the `elevenlabs/skills` skill, triggered manually or by cron.

---

**Phase 3-4 audit (CC78a)**: Source material (00111, 00197) documents the phone/voice integration architecture as a complete two-layer system. Sources do not contain version chains or deprecated approaches — they describe the current integration pattern (ElevenLabs + Twilio + `/chat/completions`) without documenting prior approaches it replaced. The one temporal signal present (BlueBubbles documented as an alternative to iMessage CLI, with the longer-term default unsettled) is covered in the companion entry `openclaw-communication-channels.md`. Entry is redundancy-complete.
