# /publish

Push the staged dev edition to production (master → Cloudflare). Run this after Judy has
approved the Vercel staging preview, either manually or on a scheduled basis.

## Step 1 — Switch to master and merge dev

```bash
git checkout master
git merge -X theirs dev
```

The GA4 state always differs between dev (disabled) and master (enabled), so `-X theirs`
takes dev's content — GA4 will be re-enabled in Step 2.

## Step 0 — Pre-flight checks

**No oversized images (Cloudflare 25 MB limit):**
```bash
find editions/ -name "*.jpg" -o -name "*.jpeg" -o -name "*.JPG" -o -name "*.png" | while read f; do [ $(stat -c%s "$f") -gt 26214400 ] && echo "$f"; done
```
Compress any hits before proceeding.

**No dangling git submodules:**
```bash
git ls-files --stage | grep "^160000"
```
No output = clean.

## Step 1b — Verify DateBook and AstroChart point to current edition

```bash
grep -E "datebook|daily-star" index.html
```

Both hrefs must match the current edition date. Fix on dev2, re-stage, then publish if either is stale.

**Do not proceed if either link is stale.**

## Step 2 — Re-enable GA4 on master

```bash
python3 tools/enable_ga4.py
```

Verify the file count is non-zero and plausible (should match total HTML files in the repo).
If it prints 0, check that the merge brought in files with a GA4 comment — it may mean
`-X theirs` resolved files in favor of master's already-enabled form (safe to proceed).

## Step 3 — Commit and push to master

```bash
git add -u
git commit -m "Publish <edition date> edition to production

Re-enables GA4 for production deployment.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"

git push origin master
```

Cloudflare detects the push and deploys automatically to `chicagoclassicmag.com`.

## Step 4 — Send publication notification

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

## Step 5 — Switch back to dev2 and update editors pages

```bash
git checkout dev2
```

**`editors/index.html`:**
- Edition tag: "Published"
- Add production URL (`https://chicagoclassicmag.com`) to Quick Links
- Decisions Needed: add "Published [date] at [time]"
- Archive current reader votes as a dated paragraph (so tallies are preserved before next edition resets)

Commit and push to dev2.

## Step 6 — Confirm deployment

Return the production URL to the user:

**https://chicagoclassicmag.com**

Note: Cloudflare may take 1–2 minutes to propagate after the push. To confirm deployment:

```bash
curl -s -o /dev/null -w "%{http_code}" https://chicagoclassicmag.com
```

200 = live. If not yet up, wait 60 seconds and retry.

## Notes

- Never push to master without GA4 re-enabled — production must always have analytics active
- Never push to master without Judy having reviewed and approved the staging preview
- After publishing, dev and master will have diverged slightly (GA4 state) — this is expected and handled automatically on the next `/stage` run
- If the merge is not a fast-forward, investigate before proceeding — do not force-merge
