# Syncrescendence Makefile
# Standard targets for repository operations

.PHONY: configs validate reconcile deploy-ajna sync-openclaw reconcile-ajna-events sync clean sync-checkpoint tree help

PYTHON ?= python3
HOSTNAME := $(shell hostname -s)

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

reconcile-ajna-events:
	@$(PYTHON) reconcile-ajna-events.py
	@echo "✓ Ajna event landing zone reconciled into repo memory/state"

# Default target
help:
	@echo "Syncrescendence Repository Commands"
	@echo ""
	@echo "  make validate         - Validate config sources, manifests, and referenced paths"
	@echo "  make configs          - Render configs/ from AGENTS.md + harness manifests"
	@echo "  make reconcile        - Render configs/ and sync root harness files"
	@echo "  make deploy-ajna      - Deploy generated Ajna config to the live OpenClaw workspace"
	@echo "  make sync-openclaw    - Snapshot live OpenClaw runtime back into repo state"
	@echo "  make reconcile-ajna-events - Ingest Ajna event files from OpenClaw workspace"
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
