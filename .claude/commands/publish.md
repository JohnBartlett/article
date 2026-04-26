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
grep "daily-star" index.html
```

The href should match the current edition month (e.g. `editions/2026-04-05/daily-star-april/` for April). If it points to a previous month (e.g. `daily-star-march`), fix it on dev2 first, then re-stage before publishing.

**Do not proceed to master if the Astrochart link is stale.**

## Step 2 — Re-enable GA4 on master

GA4 was disabled on dev to prevent skewing stats. Re-enable it before pushing to production.
The script handles both disable comment forms (`<!-- GA4-disabled` and `<!-- GA4 disabled on dev2`):

```bash
python3 tools/enable_ga4.py
```

Verify the file count is non-zero and plausible (should match total HTML files in the repo).
If it prints 0, check that the merge brought in files with a GA4 comment — it may mean
`-X theirs` resolved files in favor of master's already-enabled form (safe to proceed).

## Step 3 — Commit and push to master

Only run `git add -u` and create a separate GA4 commit if `enable_ga4.py` changed files.
If 0 files changed, skip the extra commit — the merge commit already covers the push.

```bash
# Only if enable_ga4.py reported changes:
git add -u
git commit -m "Publish <edition date> edition to production

Re-enables GA4 for production deployment.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"

git push origin master
```

If no GA4 changes were needed, just push:
```bash
git push origin master
```

Cloudflare will detect the push and deploy automatically to `chicagoclassicmag.com`.

## Step 4 — Send publication notification emails

**Option A — Python script** (requires `~/.gmail-mcp/credentials.json`):
```python
import sys; sys.path.insert(0, 'tools')
from gmail_api import get_access_token, send_email

token = get_access_token()
send_email(token,
    to='judycbross@aol.com',
    subject='Classic Chicago Magazine — <Edition Date> Edition Is Live',
    body='Dear Judy,\n\nThe <Month Day> edition of Classic Chicago Magazine is now live at:\n\nhttps://chicagoclassicmag.com\n\nCheers, John',
    cc='john.bartlett@gmail.com')
```

**Option B — Gmail MCP fallback** (if credentials.json is missing):
Use `mcp__claude_ai_Gmail__create_draft` to create the draft, then ask the user to send it from Gmail.

Adjust the edition date in subject and body.

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
