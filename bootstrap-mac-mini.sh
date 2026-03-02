#!/usr/bin/env bash
set -euo pipefail

REMOTE_HOST="${REMOTE_HOST:-mini}"
REMOTE_USER="${REMOTE_USER:-home}"
REMOTE_ROOT="${REMOTE_ROOT:-/Users/home}"
REMOTE_REPO="${REMOTE_REPO:-$REMOTE_ROOT/syncrescendence}"
REMOTE_OPENCLAW_WORKSPACE="${REMOTE_OPENCLAW_WORKSPACE:-$REMOTE_ROOT/.openclaw/workspace/AGENTS.md}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$SCRIPT_DIR"
PYTHON_BIN="${PYTHON_BIN:-python3}"
RENDER_DIR=""

cleanup() {
  if [ -n "$RENDER_DIR" ] && [ -d "$RENDER_DIR" ]; then
    rm -rf "$RENDER_DIR"
  fi
}

trap cleanup EXIT

render_mac_mini_configs() {
  RENDER_DIR="$(mktemp -d "${TMPDIR:-/tmp}/syncrescendence-mini-render.XXXXXX")"
  "$PYTHON_BIN" "$REPO_ROOT/render-configs.py" \
    --source "$REPO_ROOT/AGENTS.md" \
    --harness-dir "$REPO_ROOT/harness" \
    --machine-dir "$REPO_ROOT/machine" \
    --output-dir "$RENDER_DIR" \
    --machine "mac-mini"
}

sync_repo_to_mini() {
  rsync -az --delete \
    --exclude ".git/" \
    --exclude ".DS_Store" \
    --exclude "__pycache__/" \
    --exclude "*.pyc" \
    --exclude "00-ORCHESTRATION/state/*.lock" \
    "$REPO_ROOT/" \
    "${REMOTE_HOST}:${REMOTE_REPO}/"
}

deploy_psyche_surface() {
  if [ -z "$RENDER_DIR" ]; then
    echo "render step has not been run" >&2
    exit 1
  fi
  scp "$RENDER_DIR/psyche/AGENTS.md" "${REMOTE_HOST}:${REMOTE_OPENCLAW_WORKSPACE}"
}

remote_status() {
  ssh "$REMOTE_HOST" "PATH=/opt/homebrew/bin:\$PATH; \
    echo 'host='\"\$(hostname)\"; \
    echo 'repo='\"$REMOTE_REPO\"; \
    [ -d \"$REMOTE_REPO\" ] && echo repo_present=true || echo repo_present=false; \
    [ -f \"$REMOTE_OPENCLAW_WORKSPACE\" ] && echo psyche_workspace_present=true || echo psyche_workspace_present=false; \
    command -v tmux >/dev/null 2>&1 && echo tmux_path=\"\$(command -v tmux)\" || echo tmux_path=missing; \
    tmux has-session -t constellation 2>/dev/null && echo constellation_session=present || echo constellation_session=absent"
}

usage() {
  cat <<'EOF'
Usage: bootstrap-mac-mini.sh [render|sync|deploy-psyche|status|all]

  render         Render configs for the mac-mini manifest
  sync           Rsync the repo to /Users/home/syncrescendence on the mini
  deploy-psyche  Copy the generated Psyche AGENTS.md into the mini OpenClaw workspace
  status         Print remote bootstrap status
  all            Render, sync, deploy Psyche, then print status
EOF
}

cmd="${1:-all}"
case "$cmd" in
  render)
    render_mac_mini_configs
    ;;
  sync)
    sync_repo_to_mini
    ;;
  deploy-psyche)
    deploy_psyche_surface
    ;;
  status)
    remote_status
    ;;
  all)
    render_mac_mini_configs
    sync_repo_to_mini
    deploy_psyche_surface
    remote_status
    ;;
  *)
    usage
    exit 1
    ;;
esac
