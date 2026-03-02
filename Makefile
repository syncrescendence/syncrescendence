# Syncrescendence Makefile
# Standard targets for repository operations

.PHONY: configs validate reconcile deploy-ajna sync-openclaw hydrate-openclaw-channels tooling-surface-status cloudflared-version ontology-domain-health-edge reconcile-ajna-events reconcile-ajna-events-project reconcile-ajna-events-project-domain sanitize-openclaw-events normalize-event-ledger ontology-init ontology-project ontology-run ontology-smoke ontology-domain-health obsidian-bridge-help exocortex-bridge-help manus-checkpoint-help cloudflare-domain-bridge-help github-issue-bridge-help channel-surface-bridge-help oracle-packet-help perplexity-packet-help notebooklm-packet-help claude-cowork-packet-help oracle-response-bridge-help perplexity-response-bridge-help notebooklm-response-bridge-help claude-cowork-response-bridge-help youtube-feed-bridge-help xai-model-bridge-help google-model-bridge-help cowork-relay-stage-help cowork-relay-finalize-help bootstrap-mini revive-mini-constellation constellation-mini-status mini-constellation-snapshot install-mini-constellation-launchagent sync clean sync-checkpoint tree help

PYTHON ?= python3
HOSTNAME := $(shell hostname -s)
ONTOLOGY_LOCAL_URL ?= http://127.0.0.1:8787/ingest/event
ONTOLOGY_DOMAIN_URL ?= https://syncrescendence.com/ingest/event
ONTOLOGY_DOMAIN_HEALTH_URL ?= https://syncrescendence.com/health

# ──────────────────────────────────────────────────────────────
# Config Generation — Rendered + validated from AGENTS.md master
# ──────────────────────────────────────────────────────────────
# AGENTS.md is the single source of truth for all operational law.
# Harness manifests define the thin platform extensions.
# Machine manifests define where generated configs can safely land.

validate:
	@$(PYTHON) validate-configs.py --source AGENTS.md --harness-dir harness --machine-dir machine

configs: validate
	@$(PYTHON) render-configs.py --source AGENTS.md --harness-dir harness --machine-dir machine --output-dir configs --machine "$(HOSTNAME)"
	@echo "✓ Rendered config tree in configs/"

reconcile: validate
	@$(PYTHON) render-configs.py --source AGENTS.md --harness-dir harness --machine-dir machine --output-dir configs --machine "$(HOSTNAME)" --sync-root
	@echo "✓ Root harness files reconciled for $(HOSTNAME)"
	@echo "i OpenClaw workspace deployment remains manual until repo↔runtime sync lands"

deploy-ajna: configs
	@$(PYTHON) sync-openclaw.py --agent ajna --deploy
	@echo "✓ Ajna workspace refreshed from generated config"

sync-openclaw:
	@$(PYTHON) sync-openclaw.py --agent ajna --snapshot --synthesize-memory
	@echo "✓ OpenClaw runtime snapshot and memory synthesis refreshed"

hydrate-openclaw-channels:
	@$(PYTHON) hydrate-openclaw-channels.py
	@echo "✓ OpenClaw channel credentials hydrated from Keychain"

tooling-surface-status:
	@$(PYTHON) collect-tooling-surface-status.py
	@echo "✓ Local tooling/auth/domain status report refreshed"

cloudflared-version:
	@cloudflared --version

reconcile-ajna-events:
	@$(PYTHON) reconcile-ajna-events.py
	@echo "✓ Ajna event landing zone reconciled into repo memory/state"

reconcile-ajna-events-project:
	@$(PYTHON) reconcile-ajna-events.py --project-ontology --ontology-url "$(ONTOLOGY_LOCAL_URL)"
	@echo "✓ Ajna event landing zone reconciled and projected to ontology"

reconcile-ajna-events-project-domain:
	@$(PYTHON) reconcile-ajna-events.py --project-ontology --ontology-url "$(ONTOLOGY_DOMAIN_URL)"
	@echo "✓ Ajna event landing zone reconciled and projected to ontology domain"

sanitize-openclaw-events:
	@$(PYTHON) sanitize-openclaw-events.py --apply
	@echo "✓ OpenClaw runtime event files sanitized and report refreshed"

normalize-event-ledger:
	@$(PYTHON) normalize_event_ledger.py
	@echo "✓ Legacy event ledger normalized"

ontology-init:
	@$(PYTHON) ontology_v1.py init
	@echo "✓ Ontology v1 schema initialized"

ontology-project:
	@$(PYTHON) ontology_v1.py project-repo
	@echo "✓ Repo state projected into ontology v1"

ontology-run:
	@$(PYTHON) ontology_v1.py serve --host 127.0.0.1 --port 8787

ontology-smoke:
	@$(PYTHON) ontology_v1.py smoke
	@echo "✓ Ontology v1 smoke test passed"

ontology-domain-health:
	@curl --fail --show-error --silent "$(ONTOLOGY_DOMAIN_HEALTH_URL)"
	@echo ""
	@echo "✓ Ontology domain health endpoint is reachable"

ontology-domain-health-edge:
	@$(PYTHON) collect-tooling-surface-status.py
	@$(PYTHON) -c 'import json, pathlib; report=json.loads(pathlib.Path("00-ORCHESTRATION/state/LOCAL-SURFACE-STATUS.json").read_text()); edge=report["ontology"].get("domain_health_edge") or {}; assert edge.get("reachable"), "Direct edge health is not reachable"; print("✓ Ontology edge health reachable via {} with status {}".format(edge.get("address"), edge.get("status_code")))'

obsidian-bridge-help:
	@$(PYTHON) obsidian_repo_bridge.py --help

exocortex-bridge-help:
	@$(PYTHON) exocortex_event_bridge.py --help

manus-checkpoint-help:
	@$(PYTHON) manus_checkpoint_bridge.py --help

cloudflare-domain-bridge-help:
	@$(PYTHON) cloudflare_domain_bridge.py --help

github-issue-bridge-help:
	@$(PYTHON) github_issue_bridge.py --help

channel-surface-bridge-help:
	@$(PYTHON) channel_surface_bridge.py --help

oracle-packet-help:
	@$(PYTHON) stage_oracle_packet.py --help

perplexity-packet-help:
	@$(PYTHON) stage_perplexity_packet.py --help

notebooklm-packet-help:
	@$(PYTHON) stage_notebooklm_packet.py --help

claude-cowork-packet-help:
	@$(PYTHON) stage_claude_cowork_packet.py --help

oracle-response-bridge-help:
	@$(PYTHON) oracle_response_bridge.py --help

perplexity-response-bridge-help:
	@$(PYTHON) perplexity_response_bridge.py --help

notebooklm-response-bridge-help:
	@$(PYTHON) notebooklm_response_bridge.py --help

claude-cowork-response-bridge-help:
	@$(PYTHON) claude_cowork_response_bridge.py --help

youtube-feed-bridge-help:
	@$(PYTHON) youtube_feed_bridge.py --help

xai-model-bridge-help:
	@$(PYTHON) xai_model_bridge.py --help

google-model-bridge-help:
	@$(PYTHON) google_model_bridge.py --help

cowork-relay-stage-help:
	@$(PYTHON) stage_cowork_relay_job.py --help

cowork-relay-finalize-help:
	@$(PYTHON) finalize_cowork_relay_job.py --help

bootstrap-mini:
	@bash bootstrap-mac-mini.sh all
	@echo "✓ Mac mini repo/bootstrap state refreshed"

revive-mini-constellation:
	@ssh mini 'bash /Users/home/syncrescendence/constellation-mini-stage1.sh'
	@echo "✓ Mac mini constellation tmux stage-1 session refreshed"

constellation-mini-status:
	@bash bootstrap-mac-mini.sh status
	@ssh mini 'PATH=/opt/homebrew/bin:$$PATH; tmux has-session -t constellation 2>/dev/null && tmux list-windows -t constellation || true'

mini-constellation-snapshot:
	@$(PYTHON) collect-mini-constellation-status.py
	@echo "✓ Mac mini constellation status snapshot refreshed"

install-mini-constellation-launchagent:
	@bash install-mini-constellation-launchagent.sh
	@echo "✓ Mac mini constellation LaunchAgent installed and kickstarted"

# Default target
help:
	@echo "Syncrescendence Repository Commands"
	@echo ""
	@echo "  make validate         - Validate config sources, manifests, and referenced paths"
	@echo "  make configs          - Render configs/ from AGENTS.md + harness manifests"
	@echo "  make reconcile        - Render configs/ and sync root harness files"
	@echo "  make deploy-ajna      - Deploy generated Ajna config to the live OpenClaw workspace"
	@echo "  make sync-openclaw    - Snapshot live OpenClaw runtime back into repo state"
	@echo "  make hydrate-openclaw-channels - Hydrate local OpenClaw Slack/Discord tokens from Keychain"
	@echo "  make tooling-surface-status - Write repo-safe local auth/domain readiness status"
	@echo "  make cloudflared-version - Verify local Cloudflare Tunnel client is installed"
	@echo "  make reconcile-ajna-events - Ingest Ajna event files from OpenClaw workspace"
	@echo "  make reconcile-ajna-events-project - Reconcile Ajna events and POST them to local ontology"
	@echo "  make reconcile-ajna-events-project-domain - Reconcile Ajna events and POST them to ontology domain"
	@echo "  make sanitize-openclaw-events - Redact secrets from OpenClaw runtime event files"
	@echo "  make normalize-event-ledger - Normalize legacy event ledger records to the current contract"
	@echo "  make ontology-init    - Initialize the local ontology v1 SQLite schema"
	@echo "  make ontology-project - Project repo-normalized state into ontology v1"
	@echo "  make ontology-run     - Run the ontology v1 FastAPI service on 127.0.0.1:8787"
	@echo "  make ontology-smoke   - Verify ontology v1 projection and API wiring"
	@echo "  make ontology-domain-health - Check https://syncrescendence.com/health"
	@echo "  make ontology-domain-health-edge - Check edge health even if the local resolver is stale"
	@echo "  make obsidian-bridge-help - Show repo-backed Obsidian bridge usage"
	@echo "  make exocortex-bridge-help - Show generic exocortex event bridge usage"
	@echo "  make manus-checkpoint-help - Show Manus checkpoint bridge usage"
	@echo "  make cloudflare-domain-bridge-help - Show Cloudflare domain checkpoint bridge usage"
	@echo "  make github-issue-bridge-help - Show GitHub issue/PR checkpoint bridge usage"
	@echo "  make channel-surface-bridge-help - Show Slack/Discord runtime checkpoint bridge usage"
	@echo "  make oracle-packet-help - Show Oracle web dispatch packet generator usage"
	@echo "  make perplexity-packet-help - Show Perplexity verification packet generator usage"
	@echo "  make notebooklm-packet-help - Show NotebookLM synthesis packet generator usage"
	@echo "  make claude-cowork-packet-help - Show Claude Cowork collaboration packet generator usage"
	@echo "  make oracle-response-bridge-help - Show Oracle response landing bridge usage"
	@echo "  make perplexity-response-bridge-help - Show Perplexity response landing bridge usage"
	@echo "  make notebooklm-response-bridge-help - Show NotebookLM response landing bridge usage"
	@echo "  make claude-cowork-response-bridge-help - Show Claude Cowork response landing bridge usage"
	@echo "  make youtube-feed-bridge-help - Show YouTube feed/media checkpoint bridge usage"
	@echo "  make xai-model-bridge-help - Show xAI model checkpoint bridge usage"
	@echo "  make google-model-bridge-help - Show Google model checkpoint bridge usage"
	@echo "  make cowork-relay-stage-help - Show Cowork relay job staging usage"
	@echo "  make cowork-relay-finalize-help - Show Cowork relay finalization usage"
	@echo "  make bootstrap-mini  - Render mini configs, rsync repo to the Mac mini, and deploy Psyche surface"
	@echo "  make revive-mini-constellation - Create the stage-1 tmux constellation session on the Mac mini"
	@echo "  make constellation-mini-status - Report Mac mini repo/tmux constellation status"
	@echo "  make mini-constellation-snapshot - Write repo-safe Mac mini constellation status artifacts"
	@echo "  make install-mini-constellation-launchagent - Install the stage-1 mini LaunchAgent that recreates the tmux session"
	@echo "  make sync             - Pull, rebase, push"
	@echo "  make sync-checkpoint  - Quick sync checkpoint (git state)"
	@echo "  make tree             - Generate current directory tree"
	@echo "  make clean            - Remove temporary files"

# Git sync with rebase
sync:
	@echo "Pulling latest..."
	git pull --rebase
	@echo "Pushing changes..."
	git push
	@echo "Sync complete."

# Generate directory tree (stdout)
tree:
	@if command -v tree >/dev/null 2>&1; then \
		tree -L 2 -I 'node_modules|.git|__pycache__|*.pyc'; \
	else \
		echo "tree not installed (brew install tree). Falling back to find:"; \
		find . -maxdepth 2 -not -path './.git/*' -not -name '.DS_Store' | sort; \
	fi

# Clean temporary files
clean:
	@echo "Cleaning temporary files..."
	@find . -name "*.tmp" -not -path './.git/*' -delete 2>/dev/null; true
	@find . -name "*.bak.*" -mtime +7 -not -path './.git/*' -delete 2>/dev/null; true
	@find . -name ".DS_Store" -not -path './.git/*' -delete 2>/dev/null; true
	@echo "Clean complete."

# Quick sync checkpoint (no file generation, just output)
sync-checkpoint:
	@echo "SYNC-CHECKPOINT: $$(date -u +"%Y-%m-%dT%H:%M:%SZ")" && \
	echo "COMMIT: $$(git rev-parse --short HEAD)" && \
	echo "BRANCH: $$(git rev-parse --abbrev-ref HEAD)"
