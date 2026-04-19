 set -e
  read -p "Client ID: " CLIENT_ID
  read -p "Client Secret: " CLIENT_SECRET
  if [[ -z "$CLIENT_ID" || -z "$CLIENT_SECRET" ]]; then echo "Error: credentials required."; exit 1; fi
  echo "Installing @aaronsb/google-workspace-mcp..."
  npm install -g @aaronsb/google-workspace-mcp
  echo "Updating ~/.claude/settings.json..."
  python3 -c "
  import json, os
  path = os.path.expanduser('~/.claude/settings.json')
  s = json.load(open(path))
  s.setdefault('mcpServers', {})['google-workspace'] = {'command': 'npx', 'args': ['-y',
  '@aaronsb/google-workspace-mcp'], 'env': {'GOOGLE_CLIENT_ID': os.environ['CLIENT_ID'],
  'GOOGLE_CLIENT_SECRET': os.environ['CLIENT_SECRET']}}
  json.dump(s, open(path, 'w'), indent=2)
  "
  echo "Done! Restart Claude Code, then run /mcp to verify."
