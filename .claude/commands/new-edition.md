# /new-edition

Set up a new edition of Classic Chicago Magazine. Searches Judy's emails for article content and photos, downloads everything, builds article HTML pages, and commits to dev2.

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
- `<head>`: GA4 script (enabled, not commented out), fonts, CSS
- `<header>`: logo, nav (Home, DateBook, Astrochart, hamburger → About/Subscribe/Advertise)
- Article wrapper: category label, h1 title, meta (By Author · Date), hero figure
- `<p class="article-intro">`: first paragraph in larger font
- `<div class="article-body">`: remaining paragraphs with inline `<figure>` elements
- Feedback widget (thumbs up/down + comment form, with dynamic environment detection)
- "About the Author" link (if author is in `about.html`)
- Edition nav: `← Previous` and `Next →` links
- `<footer>`: social icons + copyright
- Scripts: hamburger toggle, keyboard nav (N/P/Space/PgDn/PgUp)

**Photo placement:** Insert `<figure>` elements after the paragraph that references each photo. Put unreferenced photos at the end of the article body. Match captions from the docx photo notes.

**Navigation order:** Article 1 ← Article 2 ← Article 3. Article 1's "Previous" links to the last article of the prior edition. Article 3's "Next" links to `../../../index.html`.

**GA4:** Always enabled (uncommented) on new articles.

**No popups:** Do not add author popup, location popup, or any overlay systems.

## Step 7 — Add articles to the dev2 internal nav

The dev2 homepage (`index.html`) has a `<!-- dev2-only -->` internal nav bar below the main nav. Add links to all new articles under a new edition label:

```html
<span class="internal-nav-label" style="margin-left:12px;">Mar 22</span>
<a href="editions/2026-03-22/chicago-chamber-music-society/">Chamber Music</a>
<a href="editions/2026-03-22/jessie-mueller/">Jessie Mueller</a>
<a href="editions/2026-03-22/two-sisters-and-a-piano/">Two Sisters</a>
```

Find the existing internal nav block in `index.html` (look for `<!-- dev2-only -->`) and append the new links inside the `.internal-nav-inner` div, after the standing links.

Remove any stale edition-specific links from the prior edition at the same time.

## Step 8 — Commit

```bash
git add editions/YYYY-MM-DD/ index.html
git commit -m "Add [Month Day] edition: [Article 1], [Article 2], [Article 3]; update dev2 internal nav"
```

Do NOT push — user controls push timing.

## Notes

- Always work on `dev2`
- Judy's email: `judycbross@aol.com`
- Use `mcp__gmail__read_email` (not `mcp__claude_ai_Gmail__gmail_read_message`) to get attachment IDs
- Photo emails often have descriptive subject lines; use those for captions
- "Cover photo" emails designate the hero image for an article
- Articles marked "DRAFT" in the docx may still need Judy's editorial review — note this in your summary
- A 5th or final photo mentioned in the docx but not received should be noted as missing
- The homepage (`index.html`) and edition landing page are built separately — do not create them here
- After committing, report: articles built, photos placed, any missing photos or draft flags, and what still needs to be done (homepage, article order confirmation, etc.)
