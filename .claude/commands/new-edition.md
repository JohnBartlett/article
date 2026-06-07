# /new-edition

Fill in article content and photos for the current edition as contributor emails arrive.
Runs repeatedly — once per batch of content — until all articles are Ready.

**Prerequisite:** `/prep-edition` has already run. Folder structure, stubs, and nav chain
already exist. This skill fills them in, not creates them.

## Step 1 — Check emails

Search `john.bartlett@gmail.com` for contributor emails since the last build pass:

```python
import sys; sys.path.insert(0, 'tools')
from gmail_api import get_access_token, search_messages, get_metadata, get_body, list_attachments, download_attachment

token = get_access_token()
messages = search_messages(token,
    "from:(judycbross@aol.com OR aedelfosse1@gmail.com OR anabaca8@gmail.com OR emuhl2@uic.edu OR muhlemane2@gmail.com OR marcycarmack@icloud.com OR sigalina@aol.com OR niceguyfatz@gmail.com) newer_than:7d")
```

Fetch metadata first (From, Subject, Date, Snippet), then full body for actionable messages.

## Step 2 — Identify content per article

For each email, determine:
- Which article it belongs to (match contributor + working title)
- What it contains: article text (docx/PDF/inline), photos (attachments), or both
- Any photo placement instructions in the text (e.g. "(Photo of X, caption: Y)")
- Whether Judy has marked any article as held, replaced, or deferred

## Step 3 — Download and place photos

For each photo attachment:

```python
attachments = list_attachments(token, msg_id)
for att in attachments:
    download_attachment(token, msg_id, att['id'],
        f'editions/YYYY-MM-DD/slug/photo-{n:02d}.jpeg')
```

Normalize filenames to `photo-01.jpeg`, `photo-02.jpeg`, etc.

If photos arrived via Hightail or Google Drive shortcut (downloads as HTML, not image):
ask the user to save files to `editions/YYYY-MM-DD/slug/` manually, then continue.

**Before placing any `<figure>` HTML, build an explicit photo map:**

| Filename | Caption (verbatim from email) | Placement (after which sentence/paragraph) |
|---|---|---|
| photo-01.jpeg | "..." | after byline, as hero |
| photo-02.jpeg | "..." | after paragraph beginning "..." |

If any field is unknown, stop and find it from the email before writing HTML. Never infer captions or placement positions.

**COVER photos:** Any file with "COVER" in the filename is the homepage card image. Do NOT include it in the article body unless the contributor explicitly says to AND it has a caption.

**PDF-sourced photos:** PDFs have no embedded layout. Build article text first (no photos), then ask for or find explicit placement instructions before inserting any figures.

**After placing all photos:**
- Count `<figure>` elements vs. photos on disk — they must match (excluding COVER-only files)
- For articles with 6+ photos, do a sequential read-through: confirm each `<figure>` appears immediately after its specified anchor sentence
- Check no photo filename appears more than once in the HTML (duplicate = hero + inline conflict)

## Step 4 — Extract article text

**From docx attachment:**
```python
import zipfile, re
with zipfile.ZipFile('/tmp/article.docx') as z:
    xml = z.read('word/document.xml').decode('utf-8')
text = re.sub(r'<[^>]+>', ' ', xml)
text = re.sub(r'\s+', ' ', text).strip()
```

**From PDF attachment:**
```python
source .venv/bin/activate  # if not already active
import PyPDF2
reader = PyPDF2.PdfReader('/tmp/article.pdf')
text = '\n'.join(page.extract_text() for page in reader.pages)
```

**OCR artifacts:** Clean up split words (e.g. "T he" → "The", "Band W ith" → "Bandwidth").

**From docx with embedded images:**
```python
with zipfile.ZipFile('/tmp/article.docx') as z:
    for name in z.namelist():
        if name.startswith('word/media/'):
            data = z.read(name)
            with open(f'editions/YYYY-MM-DD/slug/{os.path.basename(name)}', 'wb') as f:
                f.write(data)
```

## Step 5 — Build article HTML

Fill in the existing stub at `editions/YYYY-MM-DD/slug/index.html`. Do not recreate from
scratch — the nav chain, GA4 state, and internal nav block are already correct.

**Article structure (required order):**
1. Category label, `<h1>` title, meta (By Author · Date)
2. Hero `<figure>` — `photo-01.jpeg` placed right after byline (not in carousel)
3. `<p class="article-intro">` — first paragraph in larger font
4. `<div class="article-body">` — body paragraphs with inline `<figure>` elements for remaining photos
5. About the Author link — last element inside `.article-body`:
   ```html
   <p style="margin-top: 32px;"><a href="../../../about.html#author-id" style="font-family: 'Lato', sans-serif; font-size: 14px; font-weight: 700; color: #b51c20; text-decoration: none; text-transform: uppercase; letter-spacing: 0.08em;">About the Author: Author Name &rarr;</a></p>
   ```
6. Feedback widget (thumbs up/down + comment form, with dynamic environment detection)
7. Edition nav (← Previous / Next →) with nav-thumb images

**Image sizing:** `width: 100%; height: auto;` — never fixed pixel dimensions.

**No author bio in article body** — name links to about.html only.

**No carousels** — all photos are inline `<figure>` elements.

## Step 6 — Update homepage card

Replace the placeholder card in root `index.html` for this article with the real cover image
and teaser text. If this is the hero (article #1), update the hero section.

## Step 7 — Handle held or pulled articles

**Article newly held (Judy says "hold this for later"):**
- If folder already exists: remove it
- Rewire nav chain: update predecessor's "next" link and successor's "prev" link
- Remove card from edition homepage and root `index.html`
- Log in `future-articles.html` as Held with reason

**Held article cleared (Judy says "include it after all"):**
- Create folder, add stub with correct nav position
- Rewire nav chain for predecessor and successor
- Add card to edition homepage and root `index.html`
- Update `future-articles.html` status: Held → Active

## Step 8 — DateBook (always last)

When Annie's DateBook content arrives, build `editions/YYYY-MM-DD/datebook/index.html`:

1. Parse Annie's prose-block input into JSON internally:
   ```json
   { "date": "May 3, 2026", "title": "...", "venue": "...", "time": "7:30 PM",
     "description": "...", "url": "https://...", "price": "$35" }
   ```
2. Generate HTML from the structured data — consistent fields for every event
3. Past events: use JS auto-detection (not hardcoded HTML classes)

## Step 9 — Verify

```bash
python3 tools/verify_edition.py YYYY-MM-DD
```

Confirm actual state — content + photos — before claiming any article is Ready.
Never mark an article Ready without running this.

## Step 10 — Update editors pages

After each build pass:

**`editors/edition.html`:**
- Update badge for each newly completed article: Pending → Text Only → Ready
- Update article subtitle with photo count (e.g. "content built; 6 photos")
- Append new reader votes to Reader Quick Votes section (from `/check-emails` if run)
- Update Dev2 Preview button URL

**`editors/index.html`:**
- Update progress count and bar: "N of M articles ready", bar width = N/M × 100%
- Update Decisions Needed: note any held articles or blocked content
- Update Dev Preview quick link URL

## Step 11 — Commit and push

Always include `index.html` in the same commit as article folders:

```bash
git add editions/YYYY-MM-DD/ index.html future-articles.html editors/
git commit -m "YYYY-MM-DD edition: add [article], [article]; N of M articles ready"
git push origin dev2
```

## Step 12 — Deploy Vercel preview

```bash
PREVIEW_URL=$(vercel deploy --yes 2>&1 | grep "^Preview:" | head -1 | awk '{print $2}')
```

Update both editors pages with the new URL, commit, push, return URL to user.

## Notes

- Always work on dev2 — never commit to dev or master
- GA4 is already disabled in stubs — do not change it
- Relative paths from articles: `../../../` root assets, `../<sibling>/` siblings, `../../../ads/` ads
- Run `/check-emails` first if Judy may have sent instructions since the last session
- Repeat this skill as many times as needed — once per content batch — until all articles are Ready
- Report at end: articles completed, photos placed, articles still pending, any held changes
