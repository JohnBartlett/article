#!/usr/bin/env python3
"""
One-time Gmail OAuth token setup using google-auth-oauthlib.
Saves credentials to ~/.gmail-mcp/ so gmail_api.py can use them.

Usage:
    python3 tools/get_gmail_token.py
"""

import json, os, sys, glob
from pathlib import Path

# ── Find newest client_secret JSON ──────────────────────────────────────────
candidates = sorted(
    glob.glob(os.path.expanduser("~/Downloads/client_secret_*.json")),
    key=os.path.getmtime, reverse=True
)
installed = [c for c in candidates if "installed" in open(c).read()]
if not installed:
    print("❌  No installed-app client_secret_*.json found in ~/Downloads/")
    print("   Create one at: https://console.cloud.google.com/apis/credentials")
    sys.exit(1)

CLIENT_SECRETS_FILE = installed[0]
print(f"Using credential: {os.path.basename(CLIENT_SECRETS_FILE)}")

# ── Output paths ─────────────────────────────────────────────────────────────
GMAIL_MCP_DIR = Path.home() / ".gmail-mcp"
CREDS_FILE    = GMAIL_MCP_DIR / "credentials.json"
KEYS_FILE     = GMAIL_MCP_DIR / "gcp-oauth.keys.json"

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/analytics.readonly",
]

# ── Run OAuth flow ────────────────────────────────────────────────────────────
from google_auth_oauthlib.flow import InstalledAppFlow

print("\n📧  Starting Gmail OAuth flow…")
print("Your browser will open. Authorize, then return here.\n")

flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
# run_local_server starts its own HTTP server and opens the browser
creds = flow.run_local_server(
    port=8765,
    open_browser=True,
    success_message="Authorization complete — you can close this tab.",
)

if not creds or not creds.refresh_token:
    print("❌  No refresh_token returned. Try revoking app access first:")
    print("   https://myaccount.google.com/permissions")
    sys.exit(1)

# ── Save credentials ──────────────────────────────────────────────────────────
GMAIL_MCP_DIR.mkdir(parents=True, exist_ok=True)

# credentials.json — refresh_token for gmail_api.py
with open(CREDS_FILE, "w") as f:
    json.dump({
        "access_token":  creds.token,
        "refresh_token": creds.refresh_token,
        "token_type":    "Bearer",
        "scope":         " ".join(SCOPES),
    }, f, indent=2)

# Load client id/secret from the secrets file for gcp-oauth.keys.json
with open(CLIENT_SECRETS_FILE) as f:
    secrets = json.load(f)
key = list(secrets.keys())[0]
with open(KEYS_FILE, "w") as f:
    json.dump({"installed": {
        "client_id":     secrets[key]["client_id"],
        "client_secret": secrets[key]["client_secret"],
    }}, f, indent=2)

print(f"\n✅  Saved!")
print(f"   {CREDS_FILE}")
print(f"   {KEYS_FILE}")
print("\nVerifying…")

# Quick test
import sys
sys.path.insert(0, str(Path(__file__).parent))
from gmail_api import get_access_token
token = get_access_token()
print(f"✅  Token works: {token[:20]}…")
