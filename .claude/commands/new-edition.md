# /new-edition

Set up a new edition of Classic Chicago Magazine. Searches Judy's emails for article content and photos, downloads everything, builds article HTML pages, updates the homepage, and commits to dev2.

## Step 1 — Search for edition emails

Search Gmail for recent emails from Judy that contain article content:
- `from:judycbross@aol.com newer_than:14d` (max 20)

Read all results. Identify emails that contain:
- Article docx attachments ("here is our first/second/third article for [date]")
- Photo attachments for articles (subject lines often name the article and describe the photo)
- A cover photo designation ("Cover photo for...")
- Photo captions in the subject line

## Step 2 — Identify the articles

From the emails, determine:
- Edition date (e.g. March 22, 2026 → folder `editions/2026-03-22/`)
- Article titles, authors, and order (Judy often numbers them: "second article", "third article")
- Which photos belong to which article, and which is the cover/hero photo
- Any notes Judy has added (e.g. "DRAFT", "needs editing", missing photos)

## Step 3 — Download article content

For each article docx attachment:
1. Use `mcp__gmail__read_email` (not `mcp__claude_ai_Gmail__gmail_read_message`) to get the attachment ID
2. Use `mcp__gmail__download_attachment` to save the docx to `/tmp/`
3. Extract the text with Python:
```python
import zipfile, re
with zipfile.ZipFile('/tmp/article.docx') as z:
    xml = z.read('word/document.xml').decode('utf-8')
text = re.sub(r'<[^>]+>', ' ', xml)
text = re.sub(r'\s+', ' ', text).strip()
```

Note any photo placement instructions in parentheses within the docx text (e.g. "(Photo of X, caption: Y)") — these tell you where to insert figures in the article body.

**OCR artifacts:** Docx files from Judy occasionally contain OCR artifacts — words split by spaces (e.g. "T he", "thriving office s", "Band W ith"). Clean these up when building the article HTML.

## Step 4 — Create folder structure

```
editions/YYYY-MM-DD/
  article-slug/
    index.html
    photo1.jpg
    photo2.jpg
  article-slug-2/
    index.html
    ...
```

Slugs are lowercase, hyphenated versions of the article title.

```bash
mkdir -p editions/YYYY-MM-DD/article-slug editions/YYYY-MM-DD/article-slug-2 ...
```

## Step 5 — Download photos

For each photo email:
1. Use `mcp__gmail__read_email` to get the attachment ID
2. Use `mcp__gmail__download_attachment` to save directly into the article folder with a clean filename

**If photos were sent via Hightail** (a file-sharing service) and can't be downloaded directly: ask the user to save the files to Google Drive. Then use `mcp__google-workspace__search_drive_files` to find the zip/folder, `mcp__google-workspace__get_drive_file_download_url` to get the URL, and `curl` to download it. Extract with Python `zipfile`.

For articles whose docx has embedded images (large file size, e.g. >500KB), extract them:
```python
import zipfile, os
with zipfile.ZipFile('/tmp/article.docx') as z:
    for name in z.namelist():
        if name.startswith('word/media/'):
            data = z.read(name)
            with open(f'editions/YYYY-MM-DD/slug/{os.path.basename(name)}', 'wb') as f:
                f.write(data)
```

## Step 6 — Build article HTML pages

Use a Python script to generate all article `index.html` files at once. Follow the site template exactly:

**Template structure** (see any existing article for reference, e.g. `editions/2026-03-15/little-village/index.html`):
- `<head>`: GA4 script **disabled** (use `<!-- GA4-disabled ... -->` wrapper, matching `_template/article.html`), fonts, CSS
- `<header>`: logo, nav (Home, DateBook, Astrochart, hamburger → About/Subscribe/Advertise)
- Article wrapper: category label, h1 title, meta (By Author · Date), hero figure
- `<p class="article-intro">`: first paragraph in larger font
- `<div class="article-body">`: remaining paragraphs with inline `<figure>` elements
- Attribution line (if author has one — see Writer Bios below)
- Feedback widget (thumbs up/down + comment form, with dynamic environment detection)
- "About the Author" link (if author is in `about.html` — see Writer Bios below)
- Edition nav: `← Previous` and `Next →` links
- `<footer>`: social icons + copyright
- Scripts: hamburger toggle, keyboard nav (N/P/Space/PgDn/PgUp)

**Photo placement:** Insert `<figure>` elements after the paragraph that references each photo. Put unreferenced photos at the end of the article body. Match captions from the docx photo notes.

**Navigation order:** Article 1 ← Article 2 ← Article 3. Article 1's "Previous" links to `../../../index.html` (Home). Article 3's "Next" also links to `../../../index.html` (Home).

**GA4:** Always **disabled** on new articles (dev2 never runs analytics). The `/publish` skill re-enables GA4 across all files when pushing to master.

**No popups:** Do not add author popup, location popup, or any overlay systems.

**Writer Bios:** For each article author, read `_bios/<author-slug>.md` before finalizing the HTML:
1. If the file exists and the attribution line is not `(none — byline only)`, add it as the last `<p>` in `.article-body`:
   ```html
   <p style="font-size: 15px; color: #888; font-style: italic;">Attribution line here.</p>
   ```
2. Do **not** add an "About the Author" link in the article — author links belong on `about.html`, not in articles.
3. If no bio file exists for an author, note it in your summary and create the file using `/writer-bios` conventions.

## Step 7 — Update the homepage

Edit `index.html` (root) to make this the current edition:

1. **Date line** — update to the new edition date (e.g. `March 22, 2026`)
2. **Hero section** — wrap the entire hero (image + overlay) in a single `<a>` tag so both image and text are clickable. The hero article does NOT also appear as a card.
```html
<div class="hero">
  <a href="editions/YYYY-MM-DD/article-slug/">
    <img class="hero-image" src="..." style="object-position: center 20%;">
    <div class="hero-overlay">
      <div class="label">Category</div>
      <h2>Title</h2>
      <div class="meta">By Author · Date</div>
      <p>Teaser...</p>
    </div>
  </a>
</div>
```
Required CSS (add if not already present):
```css
.hero > a { display: block; text-decoration: none; }
.hero > a:hover .hero-overlay h2 { text-decoration: underline; }
```
3. **Card grid** — replace with Articles 2, 3, etc. (title, byline, image, teaser).
4. **Past Editions** — move the previous current edition to the top; drop the oldest if count exceeds 4.

Image paths from root: `editions/YYYY-MM-DD/<slug>/<image-file>`

**object-position for portrait photos:** Portrait images in the hero often need `center 15%`–`center 25%` rather than `center top`. With `center top`, a tall portrait scaled to fill the wide hero may place the subject's face in the overlay zone. Adjust based on where the face sits in the photo.

## Step 8 — Update future-articles.html

If any article in this edition was previously listed in `future-articles.html` as a held article, remove it. If no articles remain, replace the list with a "No articles currently held" placeholder.

## Step 8b — Update "Our Writers This Week" in about.html

The "Our Writers This Week" section in `about.html` should reflect only the writers who have articles in the **current edition**. Update it to show only this edition's authors (remove writers from prior editions who aren't in this one).

## Step 9 — Update the dev2 internal nav

The dev2 homepage (`index.html`) has a `<!-- dev2-only -->` internal nav bar. Since the new articles are now on the main homepage, **do not add edition-specific links** for this edition. Instead:

- Remove any stale edition-specific links from the prior edition
- Keep only the standing links: `reader-comments.html`, `future-articles.html`, `march-events-planning.html`

## Step 10 — Commit and push

```bash
git add editions/YYYY-MM-DD/ index.html
git commit -m "Add [Month Day] edition: [Article 1], [Article 2], [Article 3]; update homepage"
git push origin dev2
```

## Email style (when drafting follow-up emails to Judy)

- Salutation: `Dear Judy,`
- Sign-off: `Cheers, John`
- Write in first person — use "I/me", not "we/us"

## Notes

- Always work on `dev2`
- Judy's email: `judycbross@aol.com`
- Use `mcp__gmail__read_email` (not `mcp__claude_ai_Gmail__gmail_read_message`) to get attachment IDs
- Photo emails often have descriptive subject lines; use those for captions
- "Cover photo" emails designate the hero image for an article
- Articles marked "DRAFT" in the docx may still need Judy's editorial review — note this in your summary
- A photo mentioned in the docx but not received should be noted as missing
- The edition landing page (`editions/YYYY-MM-DD/index.html`) is built separately — do not create it here
- After committing, report: articles built, photos placed, any missing photos or draft flags
