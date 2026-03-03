# OpenClaw — Threat Model & Attack Surface

## Provenance

| Source File | Title | Signal |
|---|---|---|
| `corpus/openclaw/00045.md` | "Hacking ClawdBot and Eating Lobster Souls" | Shodan reconnaissance, real-world exploitation, reverse proxy bypass, root access case study |
| `corpus/openclaw/00059.md` | "10 ways to hack into a vibecoder's clawdbot" | Canonical 10-vector taxonomy, attack timelines, credential extraction walkthroughs |
| `corpus/openclaw/00044.md` | "Clawdbot is amazing — and, I don't think consumers should use it" | Consumer gap analysis, security implications for non-technical users |

All three pieces were published within two days of each other in late January 2026, during the initial wave of OpenClaw (then ClawdBot) viral adoption. The attack surface they describe is not theoretical — the Shodan scans happened, the root shell happened, the credential dumps happened.

---

## Why OpenClaw Is Uniquely Exposed

Most server software either has high capability or wide deployment surface — rarely both. OpenClaw has both, by design.

**Always-on, network-reachable.** OpenClaw runs persistently as a daemon. It is not a desktop app you open and close. It listens on the network so messaging platforms can reach it. This means its attack surface is live 24 hours a day, and it announces its presence to Shodan scanners the moment it starts serving HTTP.

**Full tool access.** Useful OpenClaw deployments have command execution, browser control, and filesystem access enabled. These are not optional extras — they are what make the agent capable of doing anything. An attacker who reaches the control interface inherits the same tool set.

**Credential concentration.** To connect to Telegram, Slack, Discord, Signal, Gmail, and GitHub simultaneously, OpenClaw must hold all of those credentials simultaneously. The config store is a single file (or small set of files) containing every key, token, and OAuth secret the operator has ever authorized. This is not a vulnerability unique to OpenClaw — it is the functional requirement of an integration gateway. But it means the blast radius of a single compromise includes every connected service.

**Consumer deployment by non-security-experts.** OpenClaw went viral on X (formerly Twitter) as a DIY Jarvis. Hundreds of people set it up on $5 VPS instances over a single weekend, following tutorial threads and YouTube walkthroughs. Most of them had never managed a server before. They did not read the security hardening guide because they did not know there was one. The 2am deployment that solved someone's problem and got forgotten about — that is the default, not the exception.

---

## Discovery and Reconnaissance

The IPv4 internet is continuously scanned. Shodan, Censys, and similar services maintain searchable indexes of every responding host, updated within hours of deployment. Any service with a unique HTTP fingerprint can be queried globally in seconds.

OpenClaw's fingerprint is stable across versions: the Control UI serves a distinctive HTML title tag. Searching "Clawdbot Control" on Shodan returns hundreds of results. The query takes seconds. The list includes IP address, port, and enough response metadata to immediately classify each instance.

What attackers find in those results:

- **Exposed gateways with no authentication** — WebSocket handshake accepted, immediate access granted.
- **Exposed gateways with broken authentication** — auth is configured but the reverse proxy bypass (see section 5) renders it ineffective.
- **Gateways behind authentication that still expose attack surface** — command execution, credential stores, and months of conversation history are present even when the Control UI is locked. A second vulnerability would be sufficient.
- **Default configurations** — default port (18789), default SSH password, no firewall, no fail2ban, root login permitted.

A handful of exposed instances are test deployments with no real data. The rest range from misconfigured to completely open. Two instances found in the January 2026 scan were fully unauthenticated with command execution enabled, running as root.

---

## The 10 Attack Vectors

These are the canonical attack vectors identified from systematic analysis of real-world deployments. They are ordered roughly from lowest to highest sophistication, though in practice they combine and cascade.

### Vector 1: SSH Brute Force on Fresh VPS

The victim provisions a VPS and enables password authentication with a weak or default password (common defaults: "TempPassword123", "Root123", "password"). They SSH in once to confirm it works and consider setup complete.

Automated bots discover new SSH-enabled hosts within two minutes of them going live. Password lists tuned to common VPS defaults crack root access in five minutes.

**Timeline**: T+0 VPS live, T+2 min detected by scanner, T+5 min password cracked, T+6 min root shell and full credential extraction.

**What is harvested immediately**: `~/.clawdbot/config.json` (all tokens), `.env` files (API keys), `~/.aws/credentials`, `~/.ssh/id_rsa`. Within ten minutes: conversation history, production server SSH keys, GitHub deploy keys, customer databases.

**Prevention cost**: zero. Disable password authentication, use SSH keys, enable a firewall.

### Vector 2: Exposed Control Gateway (No Auth)

The Control UI is bound to `0.0.0.0` instead of `127.0.0.1`, or the operator forwarded port 18789 through their router for convenience. No authentication is configured.

A Shodan query surfaces the instance in seconds. An automated exploit connects to the gateway and receives a full config dump: every API key, bot token, OAuth credential, database URL, and a flag indicating whether command execution is enabled.

**What is harvested**: every credential the agent holds, plus the capability to execute commands on the host if enabled.

**Time to compromise**: 30 seconds (automated).

### Vector 3: Discord/Telegram Allowlist Bypass

The operator has connected OpenClaw to a Discord server or Telegram bot but has not configured a user ID allowlist. The bot responds to any user who can reach it — any member of the Discord server, or anyone who knows the Telegram bot username.

An attacker joins the server (or discovers the bot username) and converses with the bot directly. Because the bot has command execution and file access, social engineering its own system prompt yields full credential extraction in four messages: ask for the `.env` file, ask for the AWS credentials file, ask for the SSH config, ask for the key file itself.

**What is harvested**: all credentials the agent can reach via the filesystem, up to and including production SSH private keys.

**Time to compromise**: two minutes.

### Vector 4: Browser Session Hijacking (Gmail → Everything)

Operators using OpenClaw's browser agent commonly configure it to use their default Chrome profile — the one that is already authenticated to Gmail, GitHub, AWS Console, Stripe, and their bank. This makes the agent more capable immediately, and the operator sees no reason to change it.

An attacker who reaches the bot (via any of the other vectors, or via a compromised messaging channel) can instruct it to navigate to Gmail and retrieve password reset codes or verification tokens for any linked account. The attacker initiates password resets on Apple ID and Google Account, uses the bot to read the verification emails, and disables 2FA before the victim notices anything has happened.

**Cascade**: Apple ID exposes iCloud backups, photos, Keychain passwords, and Find My location. Google Account exposes Gmail history, Drive documents, Chrome sync (all saved passwords), Android backups, and Google Pay.

**Time to compromise**: 15 minutes. Recovery time: six to twelve months if possible.

### Vector 5: 1Password / Password Manager Full Extraction

If the victim has authenticated the 1Password CLI on the same machine running OpenClaw and the bot has command execution, an attacker instructs the bot to enumerate all 1Password items and export them to a JSON file.

A realistic vault contains 347 items: banking logins, email passwords, crypto exchange credentials, GitHub tokens, Stripe keys, VPN credentials, SSH private keys, credit card numbers with CVV, and secure notes containing SSN and passport details.

**What is harvested**: the victim's entire digital life in a single file.

**Time to extract**: five minutes.

### Vector 6: Slack Workspace Takeover

The Slack bot token stored in the OpenClaw config grants access to all channels the bot is a member of, including private channels. An attacker who extracts that token does not need ongoing bot access — they use the token directly against the Slack API.

The attack sequence: enumerate accessible channels (including executive, finance, legal, HR); bulk-download message history and files across all channels; mine downloaded text for credentials, financials, and strategy using keyword search; use the same token to post phishing messages from the bot account to the engineering channel.

**What is harvested**: years of internal communications, shared documents, credentials posted in chat, internal phishing capability.

**Detection probability**: low. Bot API activity looks like normal automation.

### Vector 7: Privilege Escalation via Uncontained Docker

Many OpenClaw deployments run the agent in a Docker container configured with `--privileged` mode, the host filesystem mounted at `/host`, and the Docker socket exposed. The container runs as root.

An attacker who reaches the bot can enumerate SSH private keys across all users on the host (`/host/home/*/\.ssh/id_*`), add their own SSH key to `/host/root/.ssh/authorized_keys`, and install a rootkit that survives reboots. The container escape grants kernel-level access to the host.

**What is harvested**: complete, persistent host system ownership. All containers. All data.

**Recovery**: weeks, requiring full rebuild from scratch. Detection probability: very low once a rootkit is installed.

### Vector 8: Prompt Injection via Email, Web, and Documents

This vector exploits the agent's fundamental architecture: it reads content from the environment and acts on instructions it finds there. Hidden instructions in that content are indistinguishable from legitimate user instructions unless the agent has explicit defenses.

**8A — Email injection**: A malicious email contains hidden text (white-on-white, tiny font, after hundreds of line breaks) formatted as a system instruction. When the victim asks the bot to summarize their inbox, the bot reads the email, interprets the hidden payload as a legitimate command, exfiltrates credentials to an attacker-controlled endpoint, and reports the email as a routine invoice. The victim sees a helpful summary. The attacker receives AWS credentials, SSH keys, and all `.env` files via HTTP POST.

**8B — Web search poisoning**: A SEO-optimized attacker page ranks in the top results for a common developer query. The page contains hidden instructions in a one-pixel white div. When the bot fetches the page during a web search, it executes the embedded commands.

**8C — Document/PDF injection**: A malicious PDF contains hidden text in a page footer with white-on-white formatting, formatted as a SOC2 compliance audit directive. When the victim asks the bot to summarize the benefits handbook, the bot runs the embedded commands before delivering the summary.

**8D/8E — Slack and code injection**: Hidden instructions embedded in a linked article posted to Slack, or in a Python docstring submitted for code review.

In all variants: the victim sees a normal output. The attacker receives credentials silently.

### Vector 9: Clawdhub Skill Backdooring

Third-party skills installable from the Clawdhub skill marketplace can contain backdoored code. A malicious skill author publishes a popular utility skill. The skill is installed by many operators and executes in the context of their agent with full tool access. The supply chain attack grants persistent access to every operator who installs the skill, without requiring any direct compromise of their deployment.

### Vector 10: The Perfect Storm

All of the above mistakes combined into a single deployment. This is not a theoretical worst case — it is a description of the default configuration used by many first-time deployers who follow a tutorial without reading the hardening guide.

**Configuration**: SSH password auth enabled with default password; OpenClaw gateway bound to `0.0.0.0` with no authentication; bot DM policy open with empty allowlist; Chrome default profile (authenticated to everything) in use; Docker running privileged as root with host filesystem mounted; `.env` files world-readable; no firewall; no fail2ban; auto-updates disabled.

**Timeline of complete destruction**:

- T+0: VPS goes live
- T+2 min: Shodan scanner detects SSH on port 22 and HTTP on port 18789
- T+5 min: SSH password cracked
- T+6 min: Automated exploitation begins — config.json, AWS credentials, SSH keys, `.env` files extracted; Control UI accessed with no auth; container escape via privileged Docker; SSH backdoor installed; rootkit deployed; everything exfiltrated
- T+10 min: All platform tokens used to access Anthropic API, Telegram, Discord, Slack, Signal, GitHub, AWS simultaneously
- T+15 min: Browser agent opens Chrome; Gmail, GitHub, AWS Console, Stripe, and bank sessions active; password resets initiated
- T+20 min: Production database accessed via stolen SSH keys
- T+30 min: Full 1Password vault exported (347 items)
- T+45 min: AWS IAM backdoor admin user created; all S3 buckets downloaded; all RDS databases snapshotted
- T+60 min: Slack workspace downloaded — all channels, all DMs, two years of history
- T+90 min: All 15 production servers, 3 database servers, and complete internal network mapped from extracted SSH configs
- T+2 hours: Ransomware deployed across all 25 servers; backups deleted; ransom note dropped
- T+4 hours: Dark web listings posted — 2.4M customer records, 840K credit cards, source code, complete Slack history, 1Password vault

---

## Real-World Exploitation: The Root Access Case Study

The following is a reconstructed account of the January 2026 Shodan reconnaissance described in 00045.md. The researcher followed standard responsible disclosure practices and did not persist access.

**Step 1 — Fingerprinting**: Shodan query for "Clawdbot Control" in the title tag. Returned hundreds of results within seconds.

**Step 2 — Classification**: Most instances had some form of authentication. A handful were test deployments. A subset were misconfigured to completely open.

**Step 3 — Reverse proxy bypass**: For instances that appeared protected, the researcher identified a structural misconfiguration. OpenClaw's authentication uses a challenge-response protocol for device identity — solid cryptographic engineering. However, when deployed behind nginx or Caddy (the standard deployment pattern), all connections arrive at the application from `127.0.0.1`. OpenClaw's default behavior auto-approves localhost connections without requiring authentication, because localhost implies local development. The `gateway.trustedProxies` option that would correct this defaults to empty, and when empty, the gateway ignores `X-Forwarded-For` headers entirely. It trusts the socket address — which is always loopback behind a reverse proxy. Every internet request becomes an auto-approved local request.

This is a classic proxy misconfiguration pattern, not a novel vulnerability. It has appeared in dozens of web frameworks. The novelty is the stakes: in a typical web application, a misconfigured proxy might bypass rate limiting. In OpenClaw, it bypasses the only authentication layer protecting a full credential store and command execution interface.

**Step 4 — Control UI access**: On two instances, the WebSocket handshake completed immediately with no challenge. Full admin access granted.

**Step 5 — Configuration dump**: From the Control UI, the researcher extracted configuration containing Anthropic API keys, Telegram bot tokens, Slack OAuth credentials and signing secrets, and complete conversation histories going back months.

**Step 6 — Command execution**: On one instance with command execution enabled, the researcher sent three commands to the chat interface:

1. `cat Soul.md` — retrieved the full agent personality and behavioral configuration (the system prompt).
2. `env` — retrieved all environment variables, including API keys in plaintext.
3. `whoami` — returned `root`.

The container was running as root with no privilege separation. Full system access. No authentication required. Exposed to the entire internet.

**Step 7 — Signal device pairing artifact**: On another instance, a Signal integration setup script had left a device linking URI in a world-readable temp file. The URI is a `sgnl://` deep link — tap it on any phone with Signal installed and you are paired to the account with full read access. The cryptographic protections Signal provides for message content in transit terminate at the agent. The pairing credential sitting in a temp file renders all of that irrelevant.

---

## Consequences

**Credential theft**: A single OpenClaw config dump yields credentials for every platform the operator connected: Anthropic API (billable usage, model access), Telegram bot token (send messages as the bot, access conversation history), Slack OAuth credentials (workspace enumeration, message history, impersonation), Discord tokens, Signal pairing URIs, GitHub tokens (repository access, deploy keys), AWS access keys (cloud infrastructure, storage, databases), Stripe keys (payment processing, customer data). Each credential is independently exploitable and typically grants access to downstream systems.

**Impersonation via agent capabilities**: An attacker who controls the OpenClaw gateway inherits all of the agent's messaging capabilities. They can send messages as the operator across Telegram, Slack, Discord, Signal, and WhatsApp. Because the messages originate from the operator's bot account and arrive through the operator's configured channels, they are indistinguishable from legitimate communications to recipients. This enables targeted social engineering of the operator's contacts — colleagues, clients, family — with high credibility.

**Data exfiltration through legitimate channels**: Exfiltration through an agent's existing integrations looks like normal traffic. The Slack API does not distinguish between the operator's automation and an attacker using their token. The exfiltration channel has no anomaly signature to detect.

**Perception manipulation**: The most subtle consequence. An attacker who controls the agent's mediation layer controls what the operator perceives. They can filter out specific messages before they reach the operator. They can modify the agent's responses to omit or alter information. They can inject false information into the operator's information stream. The operator believes they are having a normal interaction with their agent while an attacker sits in the middle reading everything and altering whatever serves their purposes. There are currently no defensive frameworks for verifying that an agent-mediated communication stream reflects reality.

**Persistent access**: Agents run indefinitely. An attacker who installs a backdoor or continues to hold valid credentials maintains access for as long as those credentials remain valid — which may be until the operator manually rotates every key and token across every connected platform, an action that requires knowing a compromise occurred in the first place.

---

## The Consumer Gap

The consumer perspective in 00044.md makes the threat model concrete by describing who is actually deploying OpenClaw.

The typical viral-adoption deployer saw OpenClaw on their timeline, thought it was cool, and wanted their own Jarvis. They set up a $5 VPS, followed a tutorial, ran the install script, and connected their accounts. They authorized everything the setup flow asked for without fully understanding what they were authorizing. They did not think about security because nothing in the onboarding flow prompted them to, and the agent worked immediately after setup.

This user has no mental model for what it means to run a persistent internet-facing service. They do not know that their VPS is being scanned within minutes of going live. They do not know that the agent's default configuration is optimized for developer convenience, not production security. They do not have the background to distinguish between "secure by default" and "secure if you read the hardening guide."

The technical user has safeguards: they know to check what ports are exposed, they understand what `bind 0.0.0.0` means, they recognize when command execution is a risk. For the technical user, OpenClaw is a powerful tool deployed with deliberate choices.

For the non-technical user, OpenClaw is a powerful tool deployed with the defaults. The defaults are not safe. The consumer gap is the distance between "I set it up and it works" and "I understand what I have handed to the internet."

This gap is not a criticism of OpenClaw's engineering. It is a consequence of deploying any complex, privileged, always-on gateway software to a population with no prior exposure to server administration. The security implications are real, the setup is technically demanding for novices, and the consequence of a mistake is not a broken feature — it is months of private communications and every credential the operator has handed to their agent, available to whoever stumbles across it on Shodan.

---

## Mitigation References

This entry is focused on offense — what can go wrong, how attackers think, what the attack surface looks like from the outside.

Defense is covered in the companion entry: **`openclaw-security-hardening.md`**.

That entry covers: authentication configuration, reverse proxy setup (the `gateway.trustedProxies` fix), network binding, Docker containment, user ID allowlists, credential isolation, conversation history protection, and monitoring for perception attacks.

If you are running OpenClaw in any configuration, read that entry before continuing.

---

**Phase 3-4 audit (CC78a)**: Source material (00045, 00059, 00044) was published within a two-day window in late January 2026 — contemporaneous documentation of the initial exploitation wave. The sources do not contain version chains or "we used to think X" patterns about the threat model itself; they are the first written record of this attack surface at the moment it became visible. The temporal signal is in the companion entry (`openclaw-security-hardening.md`): SHIELD v0 version chain and default-insecure obsolescence. This entry is redundancy-complete for offense; temporal evolution belongs to the defense entry.
