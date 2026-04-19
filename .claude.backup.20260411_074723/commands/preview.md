# /preview

Usage: `/preview <article description> email from <sender name>`

Example: `/preview CCMS article email from Lee`

Build a layout review page from the article content in a sender's most recent email, commit and push to dev2, deploy to Vercel, and return the preview URL.

## Step 1 — Find the email

Search Gmail for the most recent email from the named sender that contains the article. The article may be:
- A Word doc (.docx) attachment
- A PDF attachment
- Plain text in the email body
- An inline HTML attachment

## Step 2 — Extract the article content

Depending on format:

**Word doc (.docx):** Download to `/tmp/article.docx`. Parse the XML (`word/document.xml`) to extract paragraph text and images in document order. Map images via `word/_rels/document.xml.rels`. Extract all images from `word/media/` into `review-images/` in the article folder.

**PDF:** Download to `/tmp/article.pdf`. Read the PDF content for text. Extract any embedded images if possible.

**Plain text / email body:** Use the email body text directly. No images to extract unless attached separately.

In all cases, identify:
- Article title, byline, date
- Intro paragraph
- Body paragraphs in order
- Images and their captions, in document order
- Caption text that follows each image or image group

## Step 3 — Identify the article folder and author bio

Find the matching article folder under `editions/` (e.g. `editions/2026-03-22/chicago-chamber-music-society/`).

Also check `_bios/<author-slug>.md` for the author's attribution line and `about_url` — useful context for building the review page and for noting if the author is missing from the bio library.

## Step 4 — Build the review page

Create `<sender-first-name>-review.html` in the article folder using the site's standard article HTML structure (Google Fonts, Lato/Playfair Display, standard color palette `#b51c20`). No site header/nav/footer — keep it clean for review.

Include:
- Yellow "Review Copy" banner at top: `● Review Copy — <Sender> Final Draft (<date>) — Not Published ●`
- Article category, title (`h1.article-title`), byline/date (`.article-meta`)
- Intro paragraph (`.article-intro`)
- Body paragraphs (`.article-body p`)
- **Single images**: full-width `<figure>` with caption
- **Portrait grids** (individual people): CSS grid, `object-fit: cover; object-position: top center`, height ~220px so faces are framed correctly
- **Ensemble/group photo grids**: CSS grid, `object-fit: cover; object-position: center`, height ~200px
- Use `review-images/` subfolder for image `src` paths

Grid column counts by image group size:
- 4 images → `repeat(4, 1fr)`
- 3 images → `repeat(3, 1fr)`
- 2 images → `repeat(2, 1fr)`

Mobile (max-width 600px): collapse 3- and 4-col grids to 2 columns.

## Step 5 — Commit and push to dev2

```
git add editions/.../<sender>-review.html editions/.../review-images/
git commit -m "Add <sender> review page for <article title>"
git push origin dev2
```

## Step 6 — Deploy to Vercel

Run `vercel deploy --yes` from the project root. Capture the Preview URL from the output line starting with `Preview:`.

## Step 7 — Update editors/edition.html preview URL

After capturing the Preview URL, update the Dev2 Preview button in `editors/edition.html` and commit:

```bash
sed -i "s|href=\"https://article-[^/]*/editions/[^\"]*\"|href=\"${PREVIEW_URL}/editions/2026-03-29/driehaus-museum/\"|" editors/edition.html
sed -i "s|href=\"https://article-[^/]*/index\.html\"|href=\"${PREVIEW_URL}/index.html\"|" editors/index.html
git add editors/edition.html editors/index.html && git commit -m "Update dev2 preview URL" && git push origin dev2
```

## Step 8 — Return the URL

Return the full direct URL to the review page:
`<preview-url>/editions/YYYY-MM-DD/<slug>/<sender>-review.html`
