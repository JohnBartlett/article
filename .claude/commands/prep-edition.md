# /prep-edition

Run when Judy sends the article list for a new edition. Creates the full folder skeleton,
article stubs, nav chain, and homepage shell before any content arrives. This is always
the first step — before `/new-edition`, before any emails are processed.

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

**Held articles:** Log in `future-articles.html` only — do NOT create a folder or stub.

## Step 2 — Create edition folder and article stubs

```bash
EDITION=2026-05-03
mkdir -p editions/$EDITION
```

For each active article, copy the template and fill in the stub:

```bash
mkdir -p editions/$EDITION/bill-kurtis
cp _template/article.html editions/$EDITION/bill-kurtis/index.html
```

Fill in each stub:
- `<title>` and `<h1>` — working title
- Byline — author name linked to `../../../about.html#author-id`
- Prev/next nav — correct slugs in order (first article prev → `../index.html`; last article next → `../index.html`)
- Hero image — omit `src` or use `../thumb-placeholder.jpg`
- Body — `<p style="color:#999; font-style:italic;">[Article text coming soon]</p>`
- GA4 disabled (already in template — do not change)
- `<!-- dev2-only -->` internal nav block

## Step 3 — Create edition homepage

```bash
cp _template/article.html editions/$EDITION/index.html
```

Fill in:
- Edition date in header and title
- Article list in correct order with placeholder images
- Links to each article subfolder (`./slug/`)
- Prev/next not applicable on edition homepage — link back to `../../index.html`

## Step 4 — Update root index.html

- Change date line to new edition date
- Replace hero with article #1 (placeholder image OK)
- Replace card grid with all active articles (placeholder images OK)
- Move previous current edition to Past Editions footer (keep ~4 past editions)

## Step 5 — Log articles in future-articles.html

Update the pending table with every article — active and held:

| Article | Author | Status | Source | Notes |
|---|---|---|---|---|
| Bill Kurtis | David Sweet | Pending | Email | |
| Origami | Jen Huang | Pending | Email via Annie | |
| DateBook | Annie Delfosse | Pending | Email | Arrives last |
| [Held article] | Author | Held | — | Reason if known |

## Step 6 — Update editors/edition.html

- Change edition date in page header and edition-tag
- Populate article inventory table: one row per active article, all badged `Pending`
- Clear reader votes section (will be populated during Build)
- Update Dev2 Preview button URL after first deploy (Step 8)

Columns: Article title + sub (order, category), Writer, Status badge, Dev2 link

## Step 7 — Update editors/index.html

- Change edition date and edition-tag to "In Progress — Prep"
- Reset progress block: "0 of N articles ready", bar at 0%
- Clear Decisions Needed — add one item: "Edition prepped — awaiting content from contributors"
- Replace next-edition planning section with current edition's article list and expected contributors

## Step 8 — Commit and push

```bash
git add editions/$EDITION/ index.html future-articles.html editors/
git commit -m "Prep YYYY-MM-DD edition: skeleton + stubs for N articles"
git push origin dev2
```

## Step 9 — Deploy Vercel preview and update editors pages

```bash
PREVIEW_URL=$(vercel deploy --yes 2>&1 | grep "^Preview:" | head -1 | awk '{print $2}')
```

Update `editors/edition.html` Dev2 Preview button to point to the new edition's first article.
Update `editors/index.html` Dev Preview quick link to point to homepage.

```bash
git add editors/edition.html editors/index.html
git commit -m "Update dev2 preview URL for YYYY-MM-DD prep"
git push origin dev2
```

Return the preview URL to the user.

## Step 10 — Email Judy

Draft and send a confirmation email:

**To:** judycbross@aol.com  
**Subject:** Classic Chicago — [Month Day] Edition Structure Ready

Body: confirm edition is prepped, list each article with its author and expected source,
note any held articles, include preview URL. Style: `Dear Judy,` / `Cheers, John` / first person.

## Notes

- Never wait for content before running prep — the skeleton enables parallel work
- Nav chain must be wired correctly from the start; don't leave it for Build
- If Judy's list changes after prep (article added, held, or slug renamed): update stubs,
  rewire nav chain for affected articles, update edition homepage and root index.html
- If an article is held after its folder was created: remove the folder, rewire nav chain,
  move to future-articles.html as Held
