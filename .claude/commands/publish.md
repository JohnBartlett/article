# /publish

Push the staged dev edition to production (master → Cloudflare). Run this after Judy has approved the Vercel preview, either manually or on a scheduled basis.

## Step 1 — Switch to master and merge dev

```
git checkout master
git merge -X theirs dev
```

The GA4 state always differs between dev (disabled) and master (enabled), so use `-X theirs` to take dev's content for all conflicts — GA4 will be re-enabled in the next step.

## Step 1b — Verify AstroChart points to current month

Before merging, check that the Astrochart link in `index.html` points to the current month's daily-star folder, not a past month's.

```bash
grep "daily-star" /home/john/article/index.html
```

The href should match the current edition month (e.g. `editions/2026-04-05/daily-star-april/` for April). If it points to a previous month (e.g. `daily-star-march`), fix it on dev2 first, then re-stage before publishing.

**Do not proceed to master if the Astrochart link is stale.**

## Step 2 — Re-enable GA4 on master

GA4 was disabled on dev to prevent skewing stats. It must be re-enabled on master before pushing to production. Run this Python script:

```python
import os, re

GA4_DISABLED_PATTERN = re.compile(
    r'[ \t]*<!-- GA4-disabled\s*(.*?)\s*-->',
    re.DOTALL
)
RESTORE = lambda m: m.group(1)

root = '/home/john/article'
changed = []
for dirpath, _, files in os.walk(root):
    for fname in files:
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(dirpath, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        if '<!-- GA4-disabled' not in content:
            continue
        new_content = GA4_DISABLED_PATTERN.sub(RESTORE, content)
        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            changed.append(fpath)

print(f"Re-enabled GA4 in {len(changed)} files")
```

Verify the count matches the number of HTML files in the repo.

## Step 3 — Commit and push to master

```
git add -u
git commit -m "Publish <edition date> edition to production

Re-enables GA4 for production deployment.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"

git push origin master
```

Cloudflare will detect the push and deploy automatically to `chicagoclassicmag.com`.

## Step 4 — Send publication notification emails

Send an email to Judy confirming the edition is live. Use the Python Gmail API (same OAuth credentials as `/check-emails`):

```python
import os, json, base64, requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
msg = MIMEMultipart()
msg['To'] = 'judycbross@aol.com'
msg['Cc'] = 'john.bartlett@gmail.com'
msg['Subject'] = 'Classic Chicago Magazine — <Edition Date> Edition Is Live'
msg.attach(MIMEText("""Dear Judy,

The <Month Day> edition of Classic Chicago Magazine is now live at:

https://chicagoclassicmag.com

Cheers, John""", 'plain'))
raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
requests.post('https://gmail.googleapis.com/gmail/v1/users/me/messages/send',
    headers={'Authorization': f'Bearer {token}'}, json={'raw': raw}).raise_for_status()
```

Adjust the edition date in Subject and body appropriately.

## Step 5 — Switch back to dev2

```
git checkout dev2
```

## Step 6 — Confirm deployment

Return the production URL to the user:

**https://chicagoclassicmag.com**

Note that Cloudflare may take 1–2 minutes to propagate after the push.

## Notes

- Never push to master without GA4 re-enabled — production must always have analytics active
- Never push to master without Judy having reviewed and approved the Vercel preview first
- If the merge is not a fast-forward (unexpected), investigate before proceeding — do not force-merge
- After publishing, dev and master will have diverged slightly (GA4 state). This is expected and handled automatically on the next `/stage` run
