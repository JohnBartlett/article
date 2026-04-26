# Credentials Setup Guide

This guide explains how to set up authentication for Google services (Gmail, Drive, Calendar) used by Classic Chicago Magazine tools.

## Overview

Credentials are stored **locally** (not in git) in standard directories. This keeps secrets secure while allowing tools to function.

## Directory Structure

```
~/.gmail-mcp/
  ├── credentials.json       # Gmail/Drive OAuth token
  └── gcp-oauth.keys.json    # GCP service account (optional)

~/.google/credentials/
  ├── gmail-oauth.json       # Gmail OAuth (alternative location)
  ├── drive-oauth.json       # Drive OAuth
  └── calendar-oauth.json    # Calendar OAuth (optional)
```

## Setup Steps

### 1. Gmail & Drive Authentication

These use OAuth and are obtained through the Claude interface:

```bash
# When you use Claude's Google Drive or Gmail tools:
# 1. You'll be prompted to authenticate
# 2. An OAuth token is saved automatically to:
#    ~/.gmail-mcp/credentials.json  (if using Gmail MCP)
#    ~/.google/credentials/         (if using native integrations)
```

No manual setup needed—just authenticate when prompted.

### 2. Verify Credentials Are In Place

```bash
# Check if credentials exist
ls -la ~/.gmail-mcp/credentials.json
ls -la ~/.google/credentials/

# If missing, re-authenticate via Claude:
# - Use any Gmail or Drive tool
# - Follow the OAuth flow when prompted
# - Token is saved automatically
```

### 3. For Scripts That Need Credentials

Python scripts can load credentials:

```python
from pathlib import Path
import json

def get_gmail_token():
    """Load Gmail OAuth token from local storage."""
    creds_path = Path.home() / ".gmail-mcp" / "credentials.json"
    
    if creds_path.exists():
        with open(creds_path) as f:
            return json.load(f).get('access_token')
    
    raise FileNotFoundError(f"Credentials not found at {creds_path}")
```

## Security Notes

- ✅ Credentials are stored **locally** in your home directory
- ✅ Never committed to git (listed in `.gitignore`)
- ✅ Only accessible to your user account
- ⚠️ Keep backup credentials secure
- ⚠️ If compromised, re-authenticate to generate new tokens

## Troubleshooting

### "Credentials not found" error

1. Check file exists: `ls ~/.gmail-mcp/credentials.json`
2. Re-authenticate:
   - Use any Gmail/Drive tool in Claude
   - Follow the OAuth flow
   - Token is saved automatically

### "401 Unauthorized" errors

Credentials have expired (normal after several weeks):

1. Re-authenticate via Claude interface
2. New token is saved automatically

### OAuth Scopes

If you need new scopes (e.g., "readonly" → "modify"), you'll need to re-authenticate:

1. Clear the old token: `rm ~/.gmail-mcp/credentials.json`
2. Re-authenticate in Claude
3. New token is created with updated scopes

## For Team Members

When you first use Gmail/Drive tools:

1. You'll be prompted to authenticate with Google
2. Follow the OAuth flow in your browser
3. Token is saved to `~/.gmail-mcp/credentials.json`
4. Tools will work locally from then on

**Never share or commit credentials.**

---

*Last updated: April 24, 2026*
