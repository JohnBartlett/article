# /stage

Promote the current dev2 work to `dev` for Vercel preview. Run this when an edition is ready for staging review before pushing to production.

## Step 1 — Switch to dev and merge

```
git checkout dev
git merge -X theirs dev2
```

If there are modify/delete conflicts (files deleted in dev but still in dev2), those are dev2-only experimental files — remove them:

```
git rm <conflicted-file>
```

**Known dev2-only files to always remove if they appear:**
- `editions/*/demo*/index.html` — layout demo pages
- `editions/*/datebook2.html`, `datebook3.html`, `datebook4.html` — draft datebook iterations
- `future-articles/*/index.html` — unpublished drafts held in future-articles/

## Step 2 — Comment out the internal-nav block in index.html

The `<!-- dev2-only -->` internal editors menu must **not** appear on dev or master. After the merge, open `index.html` and wrap the block in a comment:

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

## Step 3 — Verify internal-only pages are not surfaced

The following pages exist on dev2 for internal use only. They should **not** be linked from any public-facing page on dev or master (the internal-nav is the only place they appear, and it's now commented out):

- `reader-comments.html` — internal reader vote/comment log
- `future-articles.html` — unpublished article planning
- `march-events-planning.html` (or equivalent month) — editorial calendar
- `comments.html` — internal editorial notes

These files may exist in the repo and be pushed to dev — that's fine. They just must not be linked from any public nav or page.

## Step 4 — Stage and commit

```
git add index.html
git add -u  # stage any other resolved files
git commit -m "Stage <edition date> edition for dev preview

Merges dev2 into dev: <brief list of what's new>
Removes dev2-only experimental files; comments out internal-nav.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

## Step 5 — Push and return preview URL

```
git push origin dev
```

The Vercel preview URL is:

**https://article-git-dev-johns-projects-e5fce345.vercel.app**

Return this URL as the final output — it should be the last thing produced so it's easy to copy and send to Judy.

## Step 6 — Switch back to dev2

```
git checkout dev2
```

Always return to dev2 after staging — all ongoing work stays on dev2.

## Notes

- Never commit directly to `master` — dev → master happens only when Judy approves the preview
- The `<!-- dev2-only -->` block in `index.html` must always be commented out before any push to dev or master
- If the merge produces unexpected conflicts (content conflicts, not just modify/delete), read the conflicting files and resolve manually, preferring dev2's version for all edition content
