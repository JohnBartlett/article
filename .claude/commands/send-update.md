# /send-update

Draft and send a weekly update email to Judy summarizing recent site activity and reader engagement stats. If nothing has changed since the last update, say so and skip the email.

## Step 1 — Check if anything has changed

Find the last update email sent to Judy using the Python Gmail API:

```python
import os, json, base64, email as emaillib, requests

GMAIL_MCP_CREDS = os.path.expanduser("~/.gmail-mcp/credentials.json")
GMAIL_MCP_KEYS  = os.path.expanduser("~/.gmail-mcp/gcp-oauth.keys.json")

def get_access_token():
    with open(GMAIL_MCP_CREDS) as f: creds = json.load(f)
    with open(GMAIL_MCP_KEYS)  as f: keys  = json.load(f)
    web = keys.get("web") or keys.get("installed") or {}
    resp = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": web["client_id"], "client_secret": web["client_secret"],
        "refresh_token": creds["refresh_token"], "grant_type": "refresh_token",
    })
    resp.raise_for_status()
    return resp.json()["access_token"]

token = get_access_token()
# Search for last update email sent by John to Judy
r = requests.get("https://gmail.googleapis.com/gmail/v1/users/me/messages",
    headers={"Authorization": f"Bearer {token}"},
    params={"q": "from:john.bartlett@gmail.com to:judycbross@aol.com subject:\"Site Update\"", "maxResults": 1})
r.raise_for_status()
messages = r.json().get("messages", [])
```

Then check git for commits since that date:
```bash
git log --oneline --after="YYYY-MM-DD"
```

**If there are no new commits and no new votes or emails since the last update:** tell the user "Nothing has changed since the last update — no email needed." and stop.

## Step 2 — Gather activity

Summarize commits since the last update email — bios added, articles published, corrections made, photos added, etc.

## Step 3 — Pull reader stats

Read `reader-comments.html` to get the current vote tallies for the most recent edition (Yes/No counts, per-article breakdown).

Compare against what was reported in the last update email (if readable) to identify any new votes since then.

## Step 4 — Draft the email

Write the email in this format:

**To:** judycbross@aol.com
**Subject:** Classic Chicago — Site Update

**Body structure:**
1. Brief summary of what was worked on since the last update (bios added, articles published, corrections made, etc.)
2. Reader engagement stats — total votes, Yes/No breakdown, per-article tally
3. Dev2 preview URL — read the current URL from the Dev2 Preview button in `editors/edition.html` (the `href` attribute of `class="btn-stage"`)
4. Any items still pending (articles not yet received, photos needed, etc.)

**Email style:**
- Salutation: `Dear Judy,`
- Sign-off: `Cheers, John`
- First person — use "I/me", not "we/us"
- Keep it warm but concise

## Step 5 — Confirm before sending

Show the draft to the user and ask: **"Send this?"**

If yes, send using the Python Gmail API:

```python
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

msg = MIMEMultipart()
msg['To'] = 'judycbross@aol.com'
msg['Subject'] = 'Classic Chicago — Site Update'
msg.attach(MIMEText(body_text, 'plain'))
raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
requests.post('https://gmail.googleapis.com/gmail/v1/users/me/messages/send',
    headers={'Authorization': f'Bearer {token}'}, json={'raw': raw}).raise_for_status()
```

## Notes

- Judy's email: `judycbross@aol.com`
- Dev2 preview URL changes with each `vercel deploy` — always read from `editors/edition.html`, never hardcode
- Only send after user confirms
