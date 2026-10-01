# /writer-retrospective

Build (or update) a standalone retrospective of one writer's Classic Chicago articles under
`writers/<slug>/`, from the old-site archive in Google Drive plus anything already on the
current site. Run it when Judy or John asks for "a file", "a folder" or "a retrospective" of a
writer's past pieces.

Usage: `/writer-retrospective <writer name>` (for example `/writer-retrospective Rob Murphy`)

## What a retrospective is (defined by John, Oct 1, 2026)

1. **The magazine's look and feel.** Logo header, Playfair Display / Lato, the red
   `article-category` label, centered `article-title` and `article-meta`, magazine figure and
   caption styling, dark footer. The index page is a two-column card grid like the homepage.
2. **Not linked to the magazine, in either direction.** No header, footer or body link points
   at the main site (the logo and "All Articles" go to the retrospective's own index; there are
   no social links, no About/Subscribe menu, no scripts, analytics or forms). Nothing on the
   main site (homepage, about.html, article pages, internal nav) links to the retrospective.
   Each page carries `<meta name="robots" content="noindex">`.
3. **Pagination between the article pages.** Every article ends with Previous / Next links
   with 70px thumbnails and an "n of N" counter; the first and last link back to All Articles.
   Order is newest first, the same as the index page.
4. **Verbatim text, original photo filenames.** Only layout markup changes. The author's old
   headshot, the repeated column kicker and the byline line are lifted out of the body and
   shown in the page header instead. Photos the archive does not have are marked
   "[Photo not recovered from the archive]" with their captions kept.
5. **Hosted on dev2.** The page to share is the retrospective's own URL,
   `https://article-dev2.vercel.app/writers/<slug>/`, and only that URL: because the
   retrospective has no links into the magazine, a reader cannot wander from it into the dev
   site (this is the one case where a dev2 URL may go to someone outside the team; see
   CLAUDE.md mistake #33). Never share the dev2 homepage.

Earlier retrospectives (`writers/lucia-adams/`, `writers/francesco-bianchini/`) predate this
definition and use other shells. Don't restyle them unless asked.

## Step 1 — Config

One JSON file per writer: `tools/retrospectives/<slug>.json`. Copy
`tools/retrospectives/robert-murphy.json` and change:

| Key | Meaning |
|---|---|
| `slug` | folder name under `writers/` |
| `author` | display name for headers and page titles |
| `column` | the column name; shown as the red category label and the index title |
| `byline_pattern` | regex matching the byline line in the old article body (e.g. `^By\s+Lucia Adams$`) |
| `kicker_pattern` | optional regex for a repeated column kicker to lift out of the body |
| `search_phrases` | exact phrases to full-text search in the archive (name variants) |
| `intro`, `note` | index page text; `{missing}` in `note` becomes the count of unrecovered photos |
| `archive_articles` | `{old_slug, slug}` pairs: the old site's folder name and the short slug to publish under |
| `current_articles` | `{edition, slug, byline?}` for pieces already on the current site (`edition_slug` if the folder name differs) |

## Step 2 — Find the writer's articles

```bash
source .venv/bin/activate
python3 tools/build_writer_retrospective.py tools/retrospectives/<slug>.json --find
```

This full-text searches the Drive archive for `search_phrases`, downloads every page that
mentions the writer, and lists only those whose **article body** carries the byline. The
search alone over-matches badly (the old site's sidebars name many writers: 204 pages
mentioned "Rob Murphy", 8 were his), so trust the byline list, not the hit count. Add each
`(NEW)` line to `archive_articles` with a short slug.

Also check the current site: `grep -rl "<writer name>" editions/*/*/index.html about.html`,
and add those to `current_articles`.

Tell the user how many were found against how many were expected. An article under another
byline, or with no byline in the body, will not be found this way.

## Step 3 — Build and verify

```bash
python3 tools/build_writer_retrospective.py tools/retrospectives/<slug>.json
python3 tools/content_audit.py YYYY-MM-DD      # "Writer retrospective nav check" must be clean
```

The build downloads missing pages and photos into `.retrospective-cache/<slug>/`
(gitignored), writes `writers/<slug>/`, and then checks, for every article:

- body text identical to the source, character for character (whitespace aside)
- every local image and link resolves
- no link into the magazine, and no magazine page linking to the retrospective

It exits non-zero if any check fails. Don't commit a build that fails.

Then look at it: screenshot the index, one article top and one pagination bar (headless
Chrome against the `file://` pages is enough) and read them before calling it done.

## Step 4 — Commit, deploy, share

```bash
git add writers/<slug> tools/retrospectives/<slug>.json
git commit -m "Add <Writer> retrospective: N articles"
git pull --rebase origin dev2 && git push origin dev2
PREVIEW_URL=$(vercel deploy --yes 2>&1 | grep -oE 'https://article-[a-z0-9]+-johns-projects-e5fce345\.vercel\.app' | head -1)
vercel alias set ${PREVIEW_URL} article-dev2.vercel.app
```

Verify on the deployed URL (cache-busted) that the index, an article and a photo return 200.
Log it in `EMAIL_LOG.md`. If the request came from Judy, draft the note to her with the
retrospective URL and **ask before sending** (links go out via `gmail_api.py`, not a Gmail
MCP draft).

## Rules

- **Stay inside the archive.** The Drive token can read all of John's Drive. Every query must
  be scoped to the CCM archive folders (the tool does this). Never search the whole Drive by
  filename for a missing photo: on Oct 1, 2026 a `name contains 'IMG_0698'` query listed
  filenames from personal photo folders. If a photo is not under the archive's
  `wp-content/uploads/YYYY/MM/`, it is not recovered; say so and move on.
- **Never rename photos.** Files keep the names they had on the old site.
- **Don't add links back to the magazine**, "for convenience" or otherwise, and don't link the
  retrospective from about.html popups or the internal nav.
- `writers/` is a reader-facing folder, so `/stage` and `/publish` will carry a retrospective
  to production (still unlinked). If it must stay off production, say so before staging.
- The old-site archive stops at its February 8, 2026 snapshot; anything later comes from
  `editions/`.
