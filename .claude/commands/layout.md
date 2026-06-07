# /layout

Audit and manage the layout of the homepage and article pages for the current edition. Use this skill to check or fix article order, navigation links, attribution lines, and other structural elements.

Usage examples:
- `/layout audit` — check all pages and report issues
- `/layout fix` — audit and apply all fixes
- `/layout homepage` — update homepage order/hero
- `/layout nav` — fix article-to-article navigation order

---

## What this skill manages

### Homepage (`index.html`)
- **Hero** — the first article in the edition order, full-width at top
- **Card grid** — remaining articles in a 2-column grid below the hero
- **Article order** — must match the order used for keyboard navigation
- **Date line** — current edition date
- **Past Editions** — previous edition links in the footer area (keep ~4)

### Article pages (`editions/YYYY-MM-DD/<slug>/index.html`)
- **Navigation links** — `← Previous` / `Next →` at bottom; `prevUrl` / `nextUrl` JS vars for keyboard nav (N/P keys)
- **About the Author link** — last element inside `.article-body`, before `</div><!-- end article-body -->`; links to `about.html#slug`
- **Feedback widget** — thumbs up/down + comment form (should be present in all articles)
- **GA4** — must be disabled on dev2 (wrapped in `<!-- GA4-disabled ... -->`)
- **HA ad** — should not appear in articles (was removed March 2026)

---

## Article order (current edition)

The homepage and keyboard nav order must match. The first article is the hero; the rest are cards.

To find the current order, read `index.html` and note the hero slug and card slugs in sequence.

When the user specifies a new order, update:
1. The hero section in `index.html` (first article)
2. The card grid in `index.html` (remaining articles, in order)
3. The `prevUrl` / `nextUrl` JS variables and `← Previous` / `Next →` link labels in **every** article

Navigation rules:
- Article 1 (hero): `prevUrl = '../../../index.html'` (Home), `nextUrl = '../<article-2-slug>/'`
- Article N (last): `prevUrl = '../<article-n-minus-1-slug>/'`, `nextUrl = '../../../index.html'` (Home)
- All others: prev and next point to adjacent articles in order

---

## About the Author link pattern

Every article must end with an "About the Author" link as the last element inside `.article-body`, immediately before `</div><!-- end article-body -->`. The feedback widget comes after.

Format — no inline bio text, no external links (those belong only in the author's `about.html` bio):
```html
<p style="margin-top: 32px;"><a href="../../../about.html#slug" style="font-family: 'Lato', sans-serif; font-size: 14px; font-weight: 700; color: #b51c20; text-decoration: none; text-transform: uppercase; letter-spacing: 0.08em;">About the Author: Author Name &rarr;</a></p>
```

If an author has no `about.html` entry yet, note it — do not add an external link in the article. External websites, email addresses, and organizational affiliations belong in the author's bio in `about.html`, never in the article itself.

---

## About the Author popups (about.html)

Each writer in `about.html` should have an "Articles →" popup button listing all their published articles across all editions. When a new article is published:
1. Check if the author has a popup in `about.html`
2. If yes, add the new article to their popup
3. If no popup exists yet, add both the trigger button and the popup div following the pattern of existing writers (David Sweet, Susan Aurinko, Jen Huang, etc.)

Popup entry pattern:
```html
<a href="editions/YYYY-MM-DD/<slug>/" class="article-mini">
  <img src="editions/YYYY-MM-DD/<slug>/<hero-image>" alt="<title>">
  <span class="article-mini-info">
    <span class="article-mini-title"><title></span>
    <span class="article-mini-date"><Month DD, YYYY></span>
  </span>
</a>
```

---

## Audit checklist

When auditing, check every article in the current edition for:

| Check | Pass condition |
|---|---|
| Navigation — prev link | Points to correct preceding article (or Home if first) |
| Navigation — next link | Points to correct following article (or Home if last) |
| Navigation — JS vars | `prevUrl` and `nextUrl` match the link hrefs |
| Nav thumbnails | Every article-to-article link has a 70×70px `<img>` with `object-fit:cover`; only homepage links are exempt |
| About the Author link | Last element in `.article-body`; "About the Author: Name →" linked to `about.html#slug`; no inline bio text or external links |
| GA4 | Disabled (`<!-- GA4-disabled ... -->` wrapper) |
| HA ad | Not present in article body |
| Feedback widget | Present |
| Nav pattern | `nav-inner` contains Home/DateBook/Astrochart/hamburger-btn ONLY; About/Subscribe/Advertise in hamburger ONLY |

Also check the homepage:
| Check | Pass condition |
|---|---|
| Hero | First article in edition order |
| Card count | All non-hero articles appear as cards |
| Card order | Matches edition order (top-to-bottom, left-to-right) |
| Hero meta | `By [Author Name]` only — no date |
| DateBook link | `href` points to current edition datebook |
| Astrochart link | `href` points to current edition daily-star folder |
| about.html popups | All authors have article popups with all their articles listed |

---

## Applying fixes

When fixing:
1. Read each article file before editing
2. Apply all corrections in a single pass per file where possible
3. Commit all changed files together with a descriptive message
4. Push to dev2

```bash
git add <files>
git commit -m "Fix layout: <summary of changes>"
git push origin dev2
```
