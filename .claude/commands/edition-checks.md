# /edition-checks

Run after every new edition is built. Applies all structural fixes, updates about.html
author popups, and walks through any manual steps that need human content.

## What it does

1. **Automated fixes** (via `tools/edition_checks.py`):
   - Adds `dark-mode.js` to any edition homepage or article missing it
   - Adds nav-thumb CSS (64×48px flex layout) to any article missing it
   - Appends new articles to existing author popups in `about.html`

2. **Manual steps** (guided by this skill):
   - Writes bio entries for any new authors referenced in article bylines
   - Updates "Our Writers This Week" for the new edition
   - Commits all changes and deploys a Vercel preview

---

## Execution

### Step 1 — Run automated fixes

```bash
cd /home/john/article
python3 tools/edition_checks.py
```

Read `tools/edition_checks_report.json` after running to see what changed and what needs manual attention.

### Step 2 — Handle new authors

For each author in `new_authors_needing_bios`, add a `<div class="team-member" id="AUTHOR-ID">` entry to the **More Contributors** section in `about.html` (just before the closing `</div>` of that section's `<div class="team-grid">`).

Use this template:

```html
        <div class="team-member" id="AUTHOR-ID">
          <h3>Display Name</h3>
          <div class="role">Role / Column</div>
          <p>One or two sentence bio.</p>
      <button class="articles-trigger" data-popup="articles-AUTHOR-ID">Name&rsquo;s Articles &rarr;</button>
      <div id="articles-AUTHOR-ID" class="articles-popup">
        <button class="articles-popup-close">&times;</button>
        <div class="articles-popup-heading">Name&rsquo;s Articles</div>
        <div class="articles-grid">
        <!-- articles go here -->
        </div>
      </div>
        </div>
```

Article entries use this format (path is relative to site root):

```html
        <a href="editions/YYYY-MM-DD/slug/" class="article-mini">
          <img src="editions/YYYY-MM-DD/slug/cover-image.jpg" alt="Article Title">
          <span class="article-mini-info">
            <span class="article-mini-title">Article Title</span>
            <span class="article-mini-date">Month D, YYYY</span>
          </span>
        </a>
```

The author's role and bio text should come from:
- CLAUDE.md (Writers section) if the author is listed there
- The article itself (byline or author note) otherwise
- Ask Judy if unknown

### Step 3 — Update "Our Writers This Week"

The "Our Writers This Week" section in `about.html` should list only the **current edition's** writers.

1. Find the new edition's articles and their `about.html#` author IDs (grep the new edition folder)
2. Replace the `<div class="team-grid">` inside "Our Writers This Week" so it contains only those authors
3. Each author card should already exist (with bio + popup) — just reference their existing `id`
4. Keep the trigger button pointing to their existing popup (e.g., `data-popup="articles-biba-roesch"`)

Quick grep to find current edition authors:
```bash
EDITION=2026-05-03  # change to new edition
grep -rh 'about\.html#' editions/$EDITION/ --include="index.html" | grep -oP 'about\.html#\K[\w-]+'  | sort -u
```

### Step 4 — Commit and deploy

```bash
git add about.html editions/
git commit -m "Edition YYYY-MM-DD checks: dark-mode, nav-thumb, about.html updates"
git push origin dev2
vercel deploy --yes 2>&1 | grep "^Preview:"
```

Then update both editors pages with the new preview URL per CLAUDE.md instructions.

---

## Checklist

- [ ] `python3 tools/edition_checks.py` ran with no errors
- [ ] New author bios added to "More Contributors" (if any)
- [ ] "Our Writers This Week" updated for new edition
- [ ] All new authors have articles popups
- [ ] Changes committed and pushed to dev2
- [ ] Vercel preview deployed and editors pages updated
