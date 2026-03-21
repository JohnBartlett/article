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

## Step 3 — Disable GA4 on dev

Google Analytics must not fire on dev or dev2 — it skews production stats. After the merge, run this Python script to comment out all GA4 blocks across every HTML file:

```python
import os, re

GA4_PATTERN = re.compile(
    r'(\s*<!-- Google tag \(gtag\.js\) -->.*?</script>)',
    re.DOTALL
)
DISABLED_WRAP = lambda m: f'\n  <!-- GA4-disabled{m.group(1)}\n  -->'

root = '/home/john/article'
changed = []
for dirpath, _, files in os.walk(root):
    for fname in files:
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(dirpath, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        if '<!-- Google tag (gtag.js) -->' not in content:
            continue
        if '<!-- GA4-disabled' in content:
            continue  # already disabled
        new_content = GA4_PATTERN.sub(DISABLED_WRAP, content)
        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            changed.append(fpath)

print(f"Disabled GA4 in {len(changed)} files")
```

Run it, verify the count looks right (should match all HTML files in the repo), then stage the changes:

```
git add -u
```

## Step 4 — Verify internal-only pages are not surfaced

The following pages exist on dev2 for internal use only. They should **not** be linked from any public-facing page on dev or master (the internal-nav is the only place they appear, and it's now commented out):

- `reader-comments.html` — internal reader vote/comment log
- `future-articles.html` — unpublished article planning
- `march-events-planning.html` (or equivalent month) — editorial calendar
- `comments.html` — internal editorial notes

These files may exist in the repo and be pushed to dev — that's fine. They just must not be linked from any public nav or page.

## Step 5 — Commit and push

```
git add index.html
git add -u
git commit -m "Stage <edition date> edition for dev preview

Merges dev2 into dev: <brief list of what's new>
Removes dev2-only experimental files; comments out internal-nav; disables GA4.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"

git push origin dev
```

## Step 6 — Ask about production push time

Ask the user: **"What time should this go to production?"**

If they give a time, use `CronCreate` to schedule the `/publish` skill at that time. The cron should run:
```
/publish
```
Confirm the scheduled time back to the user.

If they say "now" or "manually", skip scheduling and proceed to push immediately (or leave it for them to run `/publish` when ready).

## Step 7 — Return preview URL and switch back to dev2

The Vercel preview URL is:

**https://article-git-dev-johns-projects-e5fce345.vercel.app**

Return this URL as the final output — it should be the last thing produced so it's easy to copy and send to Judy.

Then switch back to dev2:
```
git checkout dev2
```

Always return to dev2 after staging — all ongoing work stays on dev2.

## Notes

- Never commit directly to `master` — dev → master happens only when Judy approves the preview
- The `<!-- dev2-only -->` block in `index.html` must always be commented out before any push to dev or master
- GA4 must be disabled on dev and dev2; it is re-enabled by the `/publish` skill when pushing to master
- If the merge produces unexpected conflicts (content conflicts, not just modify/delete), read the conflicting files and resolve manually, preferring dev2's version for all edition content
