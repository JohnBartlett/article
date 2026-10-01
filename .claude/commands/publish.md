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

## Step 1a — No internal-only files on master

```bash
git ls-files | grep -E '^[^/]+\.md$|^(tools|\.claude|_template|_attachment-staging|_bios|docs|dashboard|editors|john-article-ideas)/|/STATUS\.md$'
```

```bash
git grep -l 'name="ccm-retrospective" content="dev2-only"' -- writers/ \
  && echo "STOP: a dev2-only writer retrospective is on this branch" || echo "no dev2-only retrospectives"
```

No output from the first command and "no dev2-only retrospectives" from the second = clean. Any other output means `/stage` didn't strip dev (Step 4b there) — these files
would be publicly served by Cloudflare (this exposed `EMAIL_LOG.md` and `CLAUDE.md` until
Sept 26, 2026). **Do not push.** Fix dev with `/stage` Step 4b, then re-run the merge.

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

Verify the file count printed looks right (should match all HTML files in the repo).

## Step 3 — Commit and push to master

```bash
git add -u
git commit -m "Publish <edition date> edition to production

Re-enables GA4 for production deployment.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"

git push origin master
```

Cloudflare detects the push and deploys automatically to `chicagoclassicmag.com`.

## Step 4 — Send publication notification

**Ask the user "Should I send this or save it as a draft?" before sending — do not send automatically just because this step exists in the skill.** This mirrors the standing rule in CLAUDE.md (mistake #15). Draft the notification below, show it, and wait for confirmation. **Recipients (John's standing practice, confirmed Sept 26, 2026):** To Judy and Sig, Cc Emma, Annie and Ana. Send with `~/.claude/scripts/gmail_api.py` so the link isn't rewritten.

```python
import sys; sys.path.insert(0, 'tools')
from gmail_api import get_access_token, send_email

token = get_access_token()
send_email(token,
    to='judycbross@aol.com, sigalina@aol.com',
    subject='Classic Chicago Magazine: <Month Day> Edition Is Live',
    body='Dear Judy and Sig,\n\nThe <Month Day> edition of Classic Chicago Magazine is now live at:\n\nhttps://chicagoclassicmag.com\n\nThank you all for your work on this issue.\n\nCheers,\nJohn',
    cc='muhlemane2@gmail.com, aedelfosse1@gmail.com, anabaca8@gmail.com')
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

- **Run the merge in a temporary worktree** so the dev2 checkout is never switched:
  `git worktree add /tmp/pub-wt origin/master -B pub-wt`, work there, push `pub-wt:master`, then
  `git worktree remove --force /tmp/pub-wt && git branch -D pub-wt`. `tools/` is not on dev or master, so run
  `comment_internal_nav.py` / `disable_ga4.py` / `enable_ga4.py` / `strip_internal_files.sh` from the dev2
  checkout's `tools/` while inside the worktree — they all operate on the current directory.
- **Push the merge commit as is (CLAUDE.md mistake #69):** give the message with `git merge -m` (a clean
  merge commits itself — a follow-up `git commit` fails and, in an `&&` chain, silently skips the push);
  never `git pull --rebase` it; confirm `origin/master` still equals `HEAD^1`, then push. Rename-detection
  conflicts (a deleted internal file "renamed" into an article, `.DS_Store`) resolve to dev's content.

- Never push to master without GA4 re-enabled — production must always have analytics active
- Never push to master without Judy having reviewed and approved the staging preview
- After publishing, dev and master will have diverged slightly (GA4 state) — this is expected and handled automatically on the next `/stage` run
- If the merge is not a fast-forward, investigate before proceeding — do not force-merge
