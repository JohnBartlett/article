# /edition-checks

Run after all articles are Ready — before staging. Applies structural fixes, updates
about.html, and verifies nav integrity. This is the quality gate between Build and Stage.

## Step 1 — Run automated fixes

```bash
python3 tools/edition_checks.py
```

Read `tools/edition_checks_report.json` after running:

```python
import json
report = json.load(open('tools/edition_checks_report.json'))
```

The script handles:
- Adds `dark-mode.js` to any edition homepage or article missing it
- Adds nav-thumb CSS (64×48px flex layout) to any article missing it
- Appends new articles to existing author popups in `about.html`

## Step 2 — Handle new authors

For each author in `report['new_authors_needing_bios']`, add a `<div class="team-member">` entry
to the **More Contributors** section in `about.html` (just before the closing `</div>` of that
section's `<div class="team-grid">`).

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
        </div>
      </div>
        </div>
```

The automated script will have already populated the articles grid — just add the wrapper.

Author bio source (in priority order):
1. CLAUDE.md Writers section — if the author is listed there
2. The article itself — byline or author note
3. Ask Judy if unknown

## Step 3 — Update "Our Writers This Week"

The "Our Writers This Week" section in `about.html` should list **only this edition's writers**.

1. Find this edition's author IDs:
   ```bash
   EDITION=2026-05-03
   grep -rh 'about\.html#' editions/$EDITION/ --include="index.html" | grep -oP 'about\.html#\K[\w-]+' | sort -u
   ```
2. Replace the `<div class="team-grid">` inside "Our Writers This Week" with cards for only those authors
3. Each card references the author's existing `id` — bio and popup already exist in their section
4. Keep trigger buttons pointing to existing popups (e.g. `data-popup="articles-biba-roesch"`)

## Step 4 — Verify nav chain

Check end-to-end nav integrity for the new edition:
- First article's "Previous" → `../index.html` (edition homepage)
- Last article's "Next" → `../index.html` (edition homepage)
- Every article's prev/next slugs match the actual folder names
- Edition homepage links to all articles

```bash
EDITION=2026-05-03
grep -r 'edition-nav\|back-link\|next-link' editions/$EDITION/ --include="index.html" -l
```

## Step 5 — Verify homepage card order

Confirm root `index.html` card order matches the nav chain order (hero = article #1,
cards = articles #2 onward in nav order).

## Step 6 — Update editors pages

**`editors/edition.html`:**
- Mark all articles as Ready (update any remaining Pending badges)
- Add final photo counts to article subtitles

**`editors/index.html`:**
- Progress bar to 100%: "N of N articles ready"
- Edition tag: "Ready for Staging"
- Decisions Needed: remove resolved items; add "All articles ready — awaiting stage approval"

## Step 7 — Commit and push

```bash
git add about.html editions/ editors/ index.html
git commit -m "Edition YYYY-MM-DD checks: dark-mode, nav-thumb, about.html — ready for staging"
git push origin dev2
```

## Step 8 — Deploy Vercel preview

```bash
PREVIEW_URL=$(vercel deploy --yes 2>&1 | grep "^Preview:" | head -1 | awk '{print $2}')
```

Update both editors pages with the final pre-stage preview URL, commit, push, return URL to user.

## Checklist

- [ ] `python3 tools/edition_checks.py` ran clean
- [ ] New author bios added to More Contributors (if any)
- [ ] "Our Writers This Week" updated for this edition
- [ ] Nav chain verified end-to-end
- [ ] Homepage card order matches nav chain
- [ ] `editors/edition.html` — all articles Ready
- [ ] `editors/index.html` — 100% progress, "Ready for Staging"
- [ ] Changes committed and pushed to dev2
- [ ] Vercel preview deployed and URL returned
