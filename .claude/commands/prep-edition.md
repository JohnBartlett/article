# /prep-edition

Run when Judy sends the article list for a new edition. Creates the full folder skeleton,
article stubs, nav chain, homepage shell, and STATUS.md before any content arrives. This is
always the first step — before `/new-edition`, before any emails are processed.

## Input

Judy's article list — titles, authors, and publication order. Usually arrives as a plain-text
email. Example:

    May 3 edition:
    1. Bill Kurtis — David Sweet
    2. Origami exhibition — Jen Huang
    3. St. James Episcopal — Judy
    4. Facets — Sydney Armstrong
    5. Philip Vidal About the Town
    6. DateBook — Annie

## Step 1 — Parse the list

Convert Judy's list into a structured table:

| Order | Slug | Working Title | Author ID | Status |
|---|---|---|---|---|
| 1 | bill-kurtis | Bill Kurtis | david-sweet | Active |
| 2 | origami | Origami Exhibition | jen-huang | Active |
| 3 | st-james | St. James Episcopal | judycbross | Active |
| 4 | facets | Facets Children's Programs | sydney-armstrong | Active |
| 5 | about-the-town | About the Town | philip-vidal | Active |
| 6 | datebook | DateBook | annie-delfosse | Active |

Rules:
- Slug = lowercase, hyphenated, 3–4 words max
- Author ID = matches existing `about.html#` anchor
- Order = keyboard nav order; hero = 1
- DateBook always gets slug `datebook`
- Articles Judy marks as "hold", "TBD", or "not yet" = Status: Held
- If an author/subject in the list is ambiguous (e.g. unclear who's actually writing a piece
  about a named person), don't guess — hold that slot as Status: Pending Clarification and
  flag it in STATUS.md rather than assigning a folder/slug you might have to rename later

**Held articles:** Log in `future-articles.html` only — do NOT create a folder or stub.

**Check new authors:** For any author not previously published, verify their `about.html#anchor`
exists: `grep -n "id=\"author-id\"" about.html`. If missing, flag it — the byline link will be
broken until it's added.

## Step 2 — Create edition folder, copy DateBook and Astrochart

```bash
EDITION=2026-05-03
PREV=2026-04-26
mkdir -p editions/$EDITION
```

Copy the DateBook and Astrochart folders from the previous edition — both are persistent and must exist in every edition:

```bash
cp -r editions/$PREV/datebook editions/$EDITION/datebook
cp -r editions/$PREV/daily-star-MONTH editions/$EDITION/daily-star-MONTH
```

Update the title/date in both `index.html` files. If the Astrochart folder name changes (e.g. `daily-star-may` → `daily-star-june`), rename accordingly.

**Do not skip this step.** A missing datebook or daily-star folder causes a live 404 on nav links in every article.

For each active article, copy the template and fill in the stub:

```bash
mkdir -p editions/$EDITION/bill-kurtis
cp _template/article.html editions/$EDITION/bill-kurtis/index.html
```

Fill in each stub:
- `<title>` and `<h1>` — working title
- Byline — author name linked to `../../../about.html#author-id`
- Prev/next nav — correct slugs in order:
  - First article: prev → `../../../index.html` (root homepage), next → `../second-slug/`
  - Middle articles: prev → `../prev-slug/`, next → `../next-slug/`
  - Last article: prev → `../prev-slug/`, next → `../../../index.html` (root homepage)
- Nav thumbnails — include `<img src="../thumb-placeholder.jpg">` in each prev/next link so verify_edition.py doesn't flag them as missing
- Hero image — omit `src` or use a placeholder
- Body — `<p style="color:#999; font-style:italic;">[Article text coming soon]</p>`
- GA4 disabled (already in template — do not change)
- `<!-- dev2-only -->` internal nav block

## Step 3 — Update root index.html

- Change date line to new edition date
- Replace hero with article #1 (placeholder image OK); hero meta = `By [Author Name]` only — no date
- Replace card grid with all active articles (placeholder images OK)
- Move previous current edition to Past Editions footer (keep ~4 past editions)
- Update DateBook nav link: `editions/YYYY-MM-DD/datebook/`
- Update Astrochart nav link: `editions/YYYY-MM-DD/daily-star-MONTH/`

Verify both links point to the new edition: `grep -E "datebook|daily-star" index.html`

## Step 4 — Log articles in future-articles.html

Update the pending table with every article — active and held:

| Article | Author | Status | Source | Notes |
|---|---|---|---|---|
| Bill Kurtis | David Sweet | Pending | Email | |
| Origami | Jen Huang | Pending | Email via Annie | |
| DateBook | Annie Delfosse | Pending | Email | Arrives last |
| [Held article] | Author | Held | — | Reason if known |

## Step 5 — Create editions/YYYY-MM-DD/STATUS.md

This is the live source of truth for the edition's build progress — replaces the old
`editors/edition.html`/`editors/index.html` pages (removed Jun 22, 2026; do not recreate them
on dev2). It's read directly by `editors/dashboard.html` on the `editors` branch and by anyone
picking up the edition mid-build. Follow the pattern of a recent edition's STATUS.md (e.g.
`editions/2026-08-09/STATUS.md`) — structure:

```markdown
# [Month Day, Year] Edition — Status

_Updated: YYYY-MM-DD_

[One-line summary of where the edition stands.]

## Judy's official lineup (`msg-id`, received YYYY-MM-DD)

Nav chain order (hero → last):
1. `slug` — Title by Author
2. ...

## Articles

| Slug | Title | Author | HTML | Photos | Notes |
|------|-------|--------|------|--------|-------|
| slug | Title | Author | Placeholder | — | Awaiting content from X |

## Notes

- Nav chain order (hero → last): ...
- Any pending clarifications (e.g. ambiguous authorship), decisions needed, held articles
```

At prep time, every article row starts as `Placeholder` / `—`. Update this file every time
content arrives during `/new-edition` — this is how progress gets tracked now, not a separate
editors page.

## Step 6 — Commit and push

```bash
git add editions/$EDITION/ index.html future-articles.html
git commit -m "Prep YYYY-MM-DD edition: skeleton + stubs for N articles"
git push origin dev2
```

## Step 7 — Deploy Vercel preview

```bash
PREVIEW_URL=$(vercel deploy --yes 2>&1 | grep "^Preview:" | head -1 | awk '{print $2}')
vercel alias set ${PREVIEW_URL} article-dev2.vercel.app
```

The stable alias `https://article-dev2.vercel.app` always points to the latest dev2 deploy —
no per-article or per-edition preview links to update anywhere else.

## Step 8 — Email Judy

Draft a confirmation email and **show it to the user before sending**:

**To:** judycbross@aol.com
**Subject:** Classic Chicago — [Month Day] Edition Structure Ready

Body: confirm edition is prepped, list each article with its author and expected source,
note any held or pending-clarification articles, include the dev2 preview URL. Style:
`Dear Judy,` / `Cheers, John` / first person.

Ask: "Should I send this?" — do not send until confirmed.

## Notes

- Never wait for content before running prep — the skeleton enables parallel work
- Nav chain must be wired correctly from the start; don't leave it for Build
- If Judy's list changes after prep (article added, held, or slug renamed): update stubs,
  rewire nav chain for affected articles, update edition homepage, root index.html, and STATUS.md
- If an article is held after its folder was created: remove the folder, rewire nav chain,
  move to future-articles.html as Held, remove its row from STATUS.md
- `editors/edition.html` and `editors/index.html` no longer exist — do not recreate them on
  dev2. The `editors` branch's `editors/dashboard.html` reads STATUS.md and `verify_edition.py`
  directly; nothing on dev2 needs to be updated to keep it current.
