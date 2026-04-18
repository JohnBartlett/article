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

GA4 was disabled on dev to prevent skewing stats. Re-enable it before pushing to production:

```bash
python3 tools/enable_ga4.py
```

Verify the file count printed looks right (should match all HTML files in the repo).

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
