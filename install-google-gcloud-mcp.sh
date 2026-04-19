#!/usr/bin/env bash
set -euo pipefail

SERVER_NAME="gcloud"
PACKAGE="@google-cloud/gcloud-mcp"

CONFIG_CANDIDATES=(
  "$PWD/.claude/settings.local.json"
  "$HOME/.claude/settings.local.json"
  "$HOME/.claude/settings.json"
  "$HOME/.claude.json"
)

log() {
  printf "\n==> %s\n" "$1"
}

need_cmd() {
  command -v "$1" >/dev/null 2>&1
}

choose_config() {
  for f in "${CONFIG_CANDIDATES[@]}"; do
    if [[ -f "$f" ]]; then
      echo "$f"
      return 0
    fi
  done

  mkdir -p "$HOME/.claude"
  echo "$HOME/.claude/settings.json"
}

ensure_node() {
  if need_cmd node && need_cmd npx; then
    log "Node detected: $(node -v)"
    return 0
  fi

  echo "Node.js 20+ is required but was not found."
  echo "Install it first, then rerun this script."
  echo "macOS: brew install node"
  echo "Ubuntu/Debian: sudo apt-get update && sudo apt-get install -y nodejs npm"
  exit 1
}

ensure_gcloud() {
  if need_cmd gcloud; then
    log "gcloud detected: $(gcloud version | head -n 1)"
    return 0
  fi

  echo "Google Cloud CLI (gcloud) is required but was not found."
  echo "Install it first: https://cloud.google.com/sdk/docs/install"
  exit 1
}

ensure_jq() {
  if need_cmd jq; then
    return 0
  fi

  echo "jq is required but was not found."
  echo "macOS: brew install jq"
  echo "Ubuntu/Debian: sudo apt-get update && sudo apt-get install -y jq"
  exit 1
}

auth_gcloud() {
  if gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    log "An active gcloud account is already configured."
    return 0
  fi

  log "No active gcloud account found. Starting login..."
  gcloud auth login
}

update_config() {
  local config_file="$1"
  local tmp_file
  tmp_file="$(mktemp)"

  mkdir -p "$(dirname "$config_file")"

  if [[ ! -f "$config_file" || ! -s "$config_file" ]]; then
    echo '{}' > "$config_file"
  fi

  jq --arg name "$SERVER_NAME" --arg pkg "$PACKAGE" '
    .mcpServers = (.mcpServers // {}) |
    .mcpServers[$name] = {
      "command": "npx",
      "args": ["-y", $pkg]
    }
  ' "$config_file" > "$tmp_file"

  mv "$tmp_file" "$config_file"
  log "Updated MCP config: $config_file"
}

show_next_steps() {
  local config_file="$1"

  cat <<EOF

Done.

Configured server:
  $SERVER_NAME -> npx -y $PACKAGE

Config file:
  $config_file

Suggested checks:
  claude mcp list
  claude mcp get $SERVER_NAME

If Claude is already running, restart it so it reloads MCP configuration.
EOF
}

main() {
  log "Checking prerequisites"
  ensure_node
  ensure_gcloud
  ensure_jq

  log "Authenticating gcloud"
  auth_gcloud

  log "Selecting Claude config file"
  CONFIG_FILE="$(choose_config)"
  echo "Using: $CONFIG_FILE"

  log "Writing MCP server config"
  update_config "$CONFIG_FILE"

  show_next_steps "$CONFIG_FILE"
}

main "$@"
