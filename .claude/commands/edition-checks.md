# /edition-checks

Run after all articles are Ready — before staging. Applies structural fixes, updates
about.html, and verifies nav integrity. This is the quality gate between Build and Stage.

## Step 1 — Pre-flight checks (run before anything else)

**Run verify_edition.py and fix all issues before proceeding:**
```bash
python3 tools/verify_edition.py YYYY-MM-DD
```
Fix every structural issue reported — broken images, missing nav thumbnails, doubled menus, oversized images, missing feedback widget, etc. Do not proceed to Step 2 until verify_edition.py is clean.

**DateBook + Astrochart links point to current edition:**
```bash
grep -E "datebook|daily-star" index.html
```
Both hrefs must match the current edition date. Fix if stale.

**Homepage hero meta is author-only:**
```bash
grep "hero-meta" index.html
```
Must read `By [Author Name]` — no date.

**No dangling git submodules:**
```bash
git ls-files --stage | grep "^160000"
```
No output = clean. If any: `git rm --cached <folder>` and commit.

## Step 2 — Run automated fixes

```bash
python3 tools/edition_checks.py
```

Read `tools/edition_checks_report.json` after running:

```python
import json
report = json.load(open('tools/edition_checks_report.json'))
```

The script handles:
- Adds `dark-mode.js` to any article missing it
- Adds nav-thumb CSS (70×70px, `object-fit:cover`) to any article missing it
- Appends new articles to existing author popups in `about.html`
- Flags any DateBook month-header sections dated before the current edition's own month (`stale_datebook_months` in the report) — these are past events left over from copying the previous week's DateBook (see mistake #20). If flagged, remove that month's entire `<!-- ═ MONTH ═ -->` block (comment, `month-header` div, and its `event-list` div) from `editions/YYYY-MM-DD/datebook/index.html` before staging. Do not touch months that are the current or a future month.

## Step 3 — Handle new authors

For each author in `report['new_authors_needing_bios']`, add a `<div class="team-member">` entry
to the **Our Writers** section in `about.html` (just before the closing `</div>` of that
section's `<div class="team-grid">`) — this is the only writers grid; see the note in Step 4.

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

## Step 4 — Update "Our Writers" author popups

**Note (2026-08-29):** `about.html` has a single "Our Writers" heading (renamed from
"Our Writers This Week") with one flat, permanent `team-grid` containing every
contributor ever published — there is no separate rotating/"this week only" section
and no separate permanent "More Contributors" section; they were the same section
all along. **Never replace or prune this grid** — doing so deletes other
contributors' bio cards. `edition_checks.py`'s `popup_articles_added` step already
handles the actual per-edition work: appending this edition's articles into each
author's existing `articles-popup` grid. There is nothing else to do here — this
step is a no-op beyond what the automated script already did in Step 2.

## Step 5 — Verify nav chain

Check end-to-end nav integrity for the new edition:
- First article's "Previous" → `../../../index.html` (root homepage)
- Last article's "Next" → `../../../index.html` (root homepage)
- Every middle article's prev/next slugs match actual folder names

```bash
EDITION=2026-06-07
# Extract all prev/next hrefs across the edition
grep -rh 'class="prev"\|class="next"' editions/$EDITION/ --include="index.html" -A1 | grep href
```

Confirm the first href is `../../../index.html`, the last href is `../../../index.html`, and all middle hrefs are `../slug/` paths that exist on disk.

## Step 6 — Verify homepage card order

Confirm root `index.html` card order matches the nav chain order (hero = article #1,
cards = articles #2 onward in nav order).

## Step 7 — Commit and push

`editors/edition.html` and `editors/index.html` no longer exist (removed Jun 22, 2026) —
do not recreate them or reference them here. Nothing on dev2 needs updating for the
`editors` branch dashboard; it reads `STATUS.md` and `verify_edition.py` directly.

```bash
git add about.html editions/ index.html
git commit -m "Edition YYYY-MM-DD checks: dark-mode, nav-thumb, about.html — ready for staging"
git push origin dev2
```

## Step 8 — Deploy Vercel preview

```bash
PREVIEW_URL=$(vercel deploy --yes 2>&1 | grep "^Preview:" | head -1 | awk '{print $2}')
```

Return the Vercel preview URL to the user.

## Checklist

- [ ] `python3 tools/edition_checks.py` ran clean
- [ ] `python3 tools/verify_edition.py YYYY-MM-DD` — no structural issues, no oversized images
- [ ] DateBook link in `index.html` points to current edition
- [ ] DateBook has no stale past-month sections (checked by `edition_checks.py`, `stale_datebook_months`)
- [ ] DateBook Astrochart nav link inside `datebook/index.html` itself points to the current month's `daily-star-MONTH` folder, not a stale one
- [ ] Astrochart link in `index.html` points to current edition
- [ ] Homepage hero meta is `By [Author Name]` only — no date
- [ ] No dangling git submodules (`git ls-files --stage | grep "^160000"` returns nothing)
- [ ] New author bios added to Our Writers (if any)
- [ ] "Our Writers" author popups updated for this edition (handled by edition_checks.py)
- [ ] Nav chain verified end-to-end
- [ ] Homepage card order matches nav chain
- [ ] Changes committed and pushed to dev2
- [ ] Vercel preview deployed and URL returned
