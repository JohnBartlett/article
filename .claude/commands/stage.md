# /stage

Promote the current dev2 work to `dev` for Vercel preview. Run this when an edition is
ready for staging review — after `/edition-checks` has passed.

## Step 1 — Switch to dev and merge

```bash
git checkout dev
git merge -X theirs dev2
```

If there are modify/delete conflicts (files deleted in dev but still in dev2), those are
dev2-only files — remove them:

```bash
git rm <conflicted-file>
```

**Known dev2-only files to always remove if they appear:**
- `editions/*/demo*/index.html` — layout demo pages
- `editions/*/datebook2.html`, `datebook3.html`, `datebook4.html` — draft datebook iterations
- `future-articles/*/index.html` — unpublished drafts held in future-articles/

**Always remove the `editors/` folder from dev — it is internal-only:**
```bash
git rm -rf editors/
```
The `editors/` folder contains the internal editors' hub and must never appear on dev or master.

## Step 2 — Comment out the internal-nav block in index.html

The `<!-- dev2-only -->` internal editors menu must **not** appear on dev or master.

**Before (dev2 state — visible):**
```html
<!-- dev2-only -->
<div class="internal-nav">
  ...
</div>
```

**After (dev/master state — hidden):**
```html
<!-- dev2-only
<div class="internal-nav">
  ...
</div>
-->
```

## Step 3 — Disable GA4 on dev

```bash
python3 tools/disable_ga4.py
git add -u
```

Verify the file count looks right (should match all HTML files in the repo).

## Step 4 — Verify internal-only pages are not surfaced

The following pages exist on dev2 for internal use only. They must **not** be linked from
any public-facing page on dev or master:

- `reader-comments.html`
- `future-articles.html`
- `march-events-planning.html` (or equivalent month)
- `comments.html`

These files may exist in the repo — that's fine. They just must not be linked from any public nav.

## Step 5 — Commit and push

```bash
git add index.html
git add -u
git commit -m "Stage <edition date> edition for dev preview

Merges dev2 into dev: <brief list of what's new>
Removes dev2-only experimental files; comments out internal-nav; disables GA4.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"

git push origin dev
```

## Step 6 — Update editors/index.html on dev2

Switch back to dev2 and update the editors page:

```bash
git checkout dev2
```

**`editors/index.html`:**
- Edition tag: "Staged"
- Add staging preview URL to Quick Links (replace or add alongside Dev Preview)
- Decisions Needed: "Staged [date] — awaiting Judy's approval"

Commit and push to dev2.

## Step 7 — Ask about production push time

Ask the user: **"What time should this go to production?"**

If they give a time, use `CronCreate` to schedule the `/publish` skill at that time.
Confirm the scheduled time back to the user.

If they say "now" or "manually", skip scheduling.

## Step 8 — Return preview URL

The Vercel staging preview URL is:

**https://article-git-dev-johns-projects-e5fce345.vercel.app**

Return this URL as the final output — easy to copy and send to Judy.

## Notes

- Never commit directly to `master` — dev → master happens only via `/publish`
- The `<!-- dev2-only -->` block in `index.html` must always be commented out before any push to dev or master
- GA4 must be disabled on dev and dev2; re-enabled only by `/publish` on master
- If the merge produces unexpected content conflicts (not just modify/delete): resolve manually, preferring dev2's version for all edition content
