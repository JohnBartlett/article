# Project: Classic Chicago Magazine

A weekly digital magazine about Chicago culture, dining, arts, and society. Static HTML site — no build step, no framework.

## Publication Info

- **Name:** Classic Chicago Magazine
- **Tagline:** "The Sunday Edition"
- **Publishes:** Every Sunday
- **Contact:** editor@classicchicagomagazine.com
- **Google Analytics:** G-5J2HWKC0B1 (disabled on dev/dev2; enabled on master only)

## Team

- **Judy Carmack Bross** — Editor-in-Chief & Founder (`judycbross@aol.com`)
- **Megan McKinney** — Publisher & Founder
- **John Bartlett** — Developer (`john.bartlett@gmail.com`)

### Writers (update "Our Writers This Week" on about.html each edition)
- Bob Glaze — Culinary & Cultural Guide
- Katherine Harvey — Travel Writer
- Susan Aurinko — Arts & Photography (My Silk Roads column)
- Jen Huang — Magazine Intern (UIC student)
- Emma Muhleman (`emuhl2@uic.edu`, `muhlemane2@gmail.com`) — Magazine Intern (UIC student)
- Philip Vidal — About the Town column (comes in end of month; Ana Baca handles photos)
- Elizabeth Dunlop Richter — Travel & Culture
- David A. F. Sweet — Unsung Gems column
- Lee Hamilton — Music
- Sophie Bross — Theatre Review
- Sydney Armstrong — Contributing Writer (new March 2026)
- Marcy Carmack (`marcycarmack@icloud.com`) — Fashion Trends writer (new March 2026)

### Contributors & Support
- **Adrian Naves** (niceguyfatz@gmail.com) — Former intern; layout and writing; works weekends
- **Annie Delfosse** (aedelfosse1@gmail.com) — DateBook curator; bio at `id="annie-delfosse"` in `about.html`
- **Ana Baca** (anabaca8@gmail.com) — Former Saturday publisher (WordPress); handles photos for Philip Vidal's About the Town column

## Branching Strategy

Three-branch workflow:

- **`master`** — Production (live site, Cloudflare). NEVER commit directly. GA4 **enabled**.
- **`dev`** — Staging / review (Vercel preview). Merges to `master` when ready. GA4 **disabled**.
- **`dev2`** — All active work. Everything starts here. GA4 **disabled**.

Workflow: `dev2` → `dev` → `master`

Use `/stage` to promote dev2 → dev, and `/publish` to promote dev → master.

**What goes to dev/master:** Only changes that affect what readers see — article HTML, photos, homepage, CSS, JS.

**What stays on dev2 only:** Skills (`.claude/commands/`), CLAUDE.md, `tools/` scripts, `_template/`, memory files, and any other internal tooling. These have no effect on the live site and must never be promoted to dev or master.

### GA4 per branch
GA4 is disabled on dev and dev2 to prevent skewing production analytics. The `/stage` skill comments it out when merging to dev; the `/publish` skill restores it before pushing to master.

- **Disabled marker:** `<!-- GA4-disabled ... -->`
- **Re-enabled:** original `<!-- Google tag (gtag.js) -->` block, uncommented

All new articles built on dev2 should use the **disabled** form (matching `_template/article.html`).

## Hosting

### Production: Cloudflare
- **URL:** `chicagoclassicmag.com`
- **Deploys from:** `master` branch

### Dev Preview: Vercel
- **Dev URL:** `https://article-git-dev-johns-projects-e5fce345.vercel.app`
- **Deploys from:** `dev` branch (intentional — Vercel is the staging preview, not production)
- **Vercel Project ID:** `prj_hzNhpgPW5e0hcF8GtyzmkkJZnMzY`
- **Vercel Team ID:** `team_8vNXZ20pDprMAIxBJgnZdEeM`

### Dev2 preview deployments
Running `vercel deploy --yes` creates a unique preview URL for the current dev2 state. After every such deploy:
1. Capture the Preview URL from the output line starting with `Preview:`
2. Update the stable alias to point to the new deployment

```bash
PREVIEW_URL=$(vercel deploy --yes 2>&1 | grep "^Preview:" | head -1 | awk '{print $2}')
vercel alias set ${PREVIEW_URL} article-dev2.vercel.app
```

**Stable alias:** `https://article-dev2.vercel.app` — always points to the most recent dev2 deploy.

There is no per-article preview-URL button to update anymore — `editors/edition.html` and `editors/index.html` (the old multi-page dashboard) were deleted Jun 22, 2026 and replaced Jul 10, 2026 by a single consolidated `editors/dashboard.html` (see below). Don't recreate the old multi-page structure.

### Editors branch — internal tooling
A separate orphan branch, `editors`, hosts internal tools that have no place in the article publishing pipeline. It shares no history with `dev2`/`dev`/`master` and has its own Vercel deployment (routes: `/dashboard`, `/comments`, `/future`; `/` and `/stats` both redirect to `/dashboard`).

- **`editors/dashboard.html`** — the internal editors dashboard. One scrolling page (no menu/tabs), with sections in order: **Article Status** (live-computed per-article Ready/Text Only/In Progress/Placeholder/Missing badges, from `verify_edition.py`'s check logic), **Decisions Needed** (pending items + blockers, parsed from the current edition's `STATUS.md`), then reader stats — Current Edition Spotlight, Votes & Comments, Edition History, All-Time Stats, Comment Leaderboard (all reused from the old stats-page logic). Lives on `editors` **only**.
  - Built by `tools/build_editors_dashboard.py`, which imports and reuses `tools/build_stats_page.py`'s GA4/Gmail functions plus `tools/verify_edition.py`'s `check_article_status`.
  - Auto-refreshed every 6 hours by `.github/workflows/refresh-editors-dashboard.yml`, which checks out `dev2` (for the build scripts, GA4/Gmail credentials, and the `editions/`/`STATUS.md` files it reads from) and `editors` (the publish target) side by side, builds from the `dev2` checkout, then commits/pushes the output to `editors` only.
  - Two different "current edition" concepts feed the page: the **prep edition** (latest edition folder with an active `STATUS.md` — may be a future, not-yet-published date) drives Article Status/Decisions Needed; the **GA4 edition** (latest *published* edition, `date <= today`) drives all the reader-stats sections, since GA4 can't report on traffic for a page that isn't live yet.
  - Do not add `editors/dashboard.html` (or the old `editors/stats.html`) back to `dev2` — `editors/stats.html` is gitignored there to prevent drift.
  - **The GitHub default branch is `actions`, not `dev2` or `master`** — scheduled cron runs read workflow YAML from the default branch, so `.github/workflows/refresh-editors-dashboard.yml` must be kept in sync on both `dev2` and `actions` (e.g. via a temporary `git worktree add /tmp/actions-worktree actions`). The `actions` branch is otherwise just a stale full-repo mirror; nothing else on it is used at runtime.
- **`reader-comments.html`** — reader votes/comments log. Lives on `editors` only, maintained by checking out that branch directly; not part of the normal dev2 session workflow.
- **`future-articles.html`** — unpublished article planning. Was moved to `editors` on Jun 22 but drifted back onto `dev2` on Jul 6 (a `/check-emails` session recreated it per the docs at the time) and has been actively maintained there since. It now lives on `dev2`, not `editors` — treat that as the current source of truth. (A stale, frozen-since-Jun-22 copy still sits on `editors` too — ignore it.)

**Never merge `editors` into `dev2`/`dev`/`master`, or vice versa** — it's a deliberately disconnected branch.

### GitHub repo
- **Repo:** `JohnBartlett/article`

## Verification & Deployment

**CRITICAL:** Never claim article status or deployment success without verification.

### Before claiming any status, run:
```bash
python3 tools/verify_edition.py YYYY-MM-DD
```

This checks ACTUAL state: what has content, what has photos, what's placeholder.

### Article Status Definitions
- **Ready** = content + photos both exist
- **Text Only** = content exists, no photos
- **In Progress** = partial (has one but not both)
- **Placeholder** = no real content
- **Missing** = folder doesn't exist or no index.html

See `VERIFICATION.md` for full definitions and workflow.

### Deployment Workflow
After `vercel deploy --yes`:
1. Run verification script to record actual state
2. Check `DEPLOYMENT-CHECKLIST.md` (verify each article loads, nav works, etc.)
3. Update editors pages with new preview URL
4. Include verification output in commit message

See `DEPLOYMENT-CHECKLIST.md` for detailed steps.

## Skills

Skills run in this order each week:

| Phase | Skill | Purpose |
|---|---|---|
| 0 | `/check-emails` | Run at session start: check Judy's emails and FormSubmit votes; apply changes; feeds into whichever phase is active |
| 1 | `/prep-edition` | When Judy sends article list: create folder skeleton, stubs, nav chain, homepage shell, editors pages — before any content arrives |
| 2 | `/new-edition` | Fill in articles and photos as contributor emails arrive; runs repeatedly until all articles are Ready |
| 3 | `/edition-checks` | Quality gate before staging: fix dark-mode, nav-thumbs, about.html popups, "Our Writers This Week", verify nav chain |
| 4 | `/stage` | Promote dev2 → dev: disable GA4, comment out internal-nav, push to Vercel staging preview |
| 5 | `/publish` | Promote dev → master: re-enable GA4, push to Cloudflare, email Judy |
| 6 | `/send-update` | After publish: pull GA4 stats and vote tallies, draft and send weekly update to Judy |

Other skills:

| Skill | Purpose |
|---|---|
| `/update-editors` | Refresh all four editors pages, pull fresh GA4/HA stats, deploy new Vercel preview |
| `/layout` | Audit and fix homepage order, article nav links, attribution lines, about.html popups |
| `/preview` | Build a layout review page from an article email; deploy to Vercel; return URL |
| `/writer-bios` | Look up, add, or update writer bios in `_bios/` and `about.html` |
| `/prompts` | Quick-reference cheat sheet for common request phrasings |
| `/retrospective` | End-of-session: gather lessons, draft updates to CLAUDE.md/skills/memory for review, then apply on approval — nothing written without user sign-off |

## DateBook

The DateBook is a curated weekly events calendar, maintained by Annie Delfosse (`aedelfosse1@gmail.com`). It lives at `editions/YYYY-MM-DD/datebook/`.

### Preferred input format for DateBook events

When receiving event data (from Annie, Judy, or the user), a consistent **prose block** per event is the most realistic format:

```
MARCH 29
Event Title
Venue Name, Address | Time
Description of the event.
Tickets/Info: https://...
Price: $XX (optional)
```

Internally, convert to structured data before generating HTML. JSON is the cleanest intermediate format:

```json
{
  "date": "March 29, 2026",
  "title": "...",
  "venue": "...",
  "time": "7:30 PM",
  "description": "...",
  "url": "https://...",
  "price": "$35–$175"
}
```

**Key rule:** Whatever format events arrive in, every event must have the same fields so HTML generation is consistent.

### Past events — auto-detection required

Past events must be visually dimmed and labeled "Past" using **JavaScript auto-detection** — compare each event's date to `new Date()` at page load and add a `.past` class + "Past" badge. Never hardcode past/future state in HTML classes. This ensures the DateBook stays accurate as time passes without manual edits.

## Analytics Reporting

A script `tools/ga4_report.py` is available to collect performance stats (users, sessions, page views) from Google Analytics 4.

### Setup

1. **Find Numeric Property ID**: In Google Analytics, go to **Admin > Property Settings > Property Details**. The "Property ID" is a numeric value (e.g., `123456789`). This is **not** the `G-XXXX` Measurement ID.
2. **Service Account**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/).
   - Enable the **Google Analytics Data API**.
   - Create a **Service Account** and download a **JSON Key**.
   - Copy the Service Account email (e.g., `my-sa@project.iam.gserviceaccount.com`).
3. **GA4 Permissions**: In Google Analytics, go to **Admin > Property Settings > Property Access Management** and add the service account email with **Viewer** role.

### Running the Report

```bash
pip install google-analytics-data
export GA4_PROPERTY_ID="523654462"
export GOOGLE_APPLICATION_CREDENTIALS="tools/credentials.json"
python3 tools/ga4_report.py
```

The script generates a timestamped JSON file with the last 30 days of data.

## Site Structure

```
/
├── index.html              Homepage — "The Sunday Edition" hero + card grid
├── about.html              About — team bios + "Our Writers This Week"
├── subscribe.html          Subscribe — "coming soon" placeholder
├── advertise.html          Advertise — "coming soon" placeholder
├── future-articles.html    Internal — unpublished article planning (dev2 only)
├── comments.html           Internal — editorial notes (dev2 only)
                            (reader-comments.html and editors/dashboard.html live on the `editors` branch, not here)
├── logo.jpg                Shared masthead logo
├── favicon.ico             Favicon
├── _template/
│   └── article.html        Article template (GA4 disabled)
├── ads/                    All advertisement assets (NOT in edition folders)
│   ├── ha-ad.html          Heritage Auctions ad click-through page
│   ├── ha-ad.jpg           Heritage Auctions ad image
│   └── image006.png        Heritage Auctions banner image
├── tools/                  Analytics and reporting scripts
├── editions/
│   ├── YYYY-MM-DD/         One folder per edition (run `ls editions/` for current list)
│   │   ├── article-slug/   One subfolder per article
│   │   │   └── index.html
│   │   ├── datebook/       Copied from previous edition each week
│   │   ├── daily-star-MONTH/  Copied from previous edition each week
│   │   └── thumb-*.jpg     Homepage card thumbnails
```

## Conventions

### File paths
- Each article: `editions/YYYY-MM-DD/<article-slug>/index.html`
- Article images: same folder as article `index.html`
- Thumbnails: `editions/YYYY-MM-DD/thumb-*.jpg`
- Ads: always in `/ads/` — never in edition folders
- Shared assets (`logo.jpg`, `favicon.ico`): root

### Relative paths from articles
- Root assets (logo, favicon, home link): `../../../` (3 levels up)
- Sibling articles: `../<sibling-slug>/`
- Thumbnails: `../thumb-*.jpg`
- Ads from articles: `../../../ads/`

### Tech stack
- Pure static HTML/CSS — no build step, no JS framework
- Google Fonts: Playfair Display, Lato
- Splide.js for photo carousels (CDN)
- Keyboard shortcuts: N (next article), P (previous), Space/PgDn (page down), PgUp (page up), ? (help)
- Google Analytics G-5J2HWKC0B1 — disabled on dev/dev2, enabled on master

### Forms
- Subscribe and Advertise pages have Formsubmit.co integration (currently commented out/disabled)
- Formsubmit endpoints: `subscribe@2ccmag.com`, `advertise@2ccmag.com`
- Forms show "coming soon" placeholder until Formsubmit activation emails are confirmed

### Adding a new edition
1. Create folder: `editions/YYYY-MM-DD/`
2. Create article subfolders with `index.html` and images
3. Create `thumb-*.jpg` thumbnails in the edition root
4. Update `index.html` homepage with new hero + card grid (see "Updating the homepage" below)
5. Update `about.html` "Our Writers This Week" section
6. Update keyboard nav links across all new articles (order must match homepage)
7. Add `../../../` paths for root assets, `../<slug>/` for sibling links
8. Use GA4 **disabled** form in new articles (matching `_template/article.html`)
9. Use inline `<figure>` elements for photos — never carousels (see mistake #10)

### Updating the homepage for a new edition
Edit `index.html` (root):
1. **Date line** — change `March 22, 2026` → next edition date
2. **Hero section** — update path, image, label, title, byline, and teaser for first article
3. **Card grid** — replace all cards with the new edition's articles (title, byline, image, teaser)
4. **Past Editions** — move the previous current edition to the top of Past Editions; drop the oldest one if the grid gets too long (keep ~4 past editions)
5. Image paths from root: `editions/YYYY-MM-DD/<slug>/<image-file>`

### Article Extraction from Contributor Emails

**CRITICAL:** Articles and photos arrive in contributor emails to `john.bartlett@gmail.com`, not via shared folders or Drive links.

**Workflow:**
1. Check contributor inboxes for emails with article text and photo attachments
2. Identify the Gmail message ID (format: `19db1b467e7a53dd`)
3. Use `tools/extract_article_photos.py` to extract attachments to article folder
4. For PDF articles: setup venv with PyPDF2, manually extract and format text
5. Create article HTML from `_template/article.html` with extracted content
6. Place photos as inline `<figure>` elements — never carousels (see mistake #10)
7. Run `verify_edition.py YYYY-MM-DD` to confirm photos and content
8. Update homepage card with article image
9. Deploy to Vercel and verify preview

**Email Sources by Contributor:**
- `judycbross@aol.com` — Editor-in-Chief (articles, editorial instructions, photo requests)
- `anabaca8@gmail.com` — Photos and articles (Ana Baca - layout editor, photographer)
- `aedelfosse1@gmail.com` — Annie Delfosse (DateBook, article content)
- `muhlemane2@gmail.com` — Emma Muhleman (intern - coordinator for submissions)
- `sigalina@aol.com` — Sigalit Zetouni (sends articles directly to John; email address uses "sigalina" but her byline name is Sigalit)

**Tools:**
- `tools/extract_article_photos.py` — Extract JPEG/PNG attachments from Gmail messages
- `tools/verify_edition.py` — Confirm article content + photo counts
- `.venv/` — Python virtual environment (required for PyPDF2, requests)

**Setup for New Session:**
```bash
# First time only
python3 -m venv .venv
source .venv/bin/activate
pip install PyPDF2 requests

# For future sessions, just activate
source .venv/bin/activate
```

**Critical: Email is the ONLY source of truth.** Articles and photos are sent to john.bartlett@gmail.com by contributors, NOT shared via folders or Drive links. Always check emails first.

**Article Structure (Required for All Articles):**

Every article must have ALL of the following before it is considered complete. Audit immediately after building:

1. **Header** — logo, main nav (Home, About, Subscribe, Advertise, DateBook, Astrochart, hamburger menu), internal-nav (dev2 only, commented out on dev/master)
2. **Article label** — category in red small-caps
3. **H1 title** — matches `<title>` tag
4. **Byline** — `By <a href="../../../about.html#author-id">Author Name</a> • [Date]`
5. **Hero image** — `<figure>` immediately after byline; `width:100%; height:auto`; original filename
6. **Article body** — verbatim contributor text; inline `<figure>` elements with correct captions; `figure img { width:100%; height:auto; display:block; }` in CSS
7. **About the Author link** — centered, before feedback widget: `About the Author: [Name] →` linking to `about.html#anchor`
8. **Feedback widget** — vote buttons + comment form
9. **Article nav** — prev and next links, each with a **70×70px thumbnail** (`object-fit:cover`) and article title. Thumbnail omitted only when linking to the homepage.
10. **Footer** — social links + copyright

**If anything is missing after building:** flag it explicitly ("I found X is missing and want to re-check") before moving on. In auto mode, fix silently and log for post-mortem.

**Photo Extraction Methods:**

**UNIVERSAL RULE — Never rename contributor image files, and never shorten filenames even in conversation.** Referring to `96An Omelette and a Glass of Wine1.jpeg` as "Wine1" in discussion is renaming — it severs the caption-to-photo link just as surely as renaming on disk. The original filename (e.g. `IMG_4824.jpeg`, `DSC_0012.jpg`) is the stable link between a photo and its caption/position in the article. Renaming to `photo-01.jpeg` etc. severs that link and causes git's rename-detection to scramble file contents across commits. This rule applies regardless of source — Gmail, Google Drive, Windows Downloads, or PDF extraction.

1. **From Gmail Attachments (✅ BEST):**
   ```bash
   source .venv/bin/activate
   python3 tools/extract_article_photos.py 2026-04-26 --contributor ana
   ```
   The script preserves original filenames exactly as sent by the contributor.

2. **From Windows Downloads Folder:**
   ```bash
   cp "/mnt/c/Users/johnb/Downloads/article-folder/*.jpeg" editions/2026-04-26/article-slug/
   # Keep original filenames — do NOT rename them.
   ```

3. **From Google Drive:**
   - Download the actual files (not shortcuts — shortcuts download as HTML).
   - Keep original filenames exactly as named in Drive.
   - If Drive has renamed them generically (e.g. `image1.jpg`), ask the contributor for the originals.

4. **From Word Documents (.docx):**
   - Extract text via python-docx or copy-paste from the document.
   - After building the HTML, do a **paragraph-by-paragraph diff** against the original Word doc before publishing. Word-to-HTML conversion silently drops parentheticals, sentence endings, and whole paragraphs with no visual break.
   - Do not trust that the conversion was complete just because the article looks coherent.

5. **From PDF Articles:**
   ```bash
   source .venv/bin/activate
   python3 << 'EOF'
   import PyPDF2
   reader = PyPDF2.PdfReader("article.pdf")
   for page in reader.pages:
       print(page.extract_text())
   EOF
   ```

**Message ID Tracking:**
Every article must have a documented message ID (e.g., `19db1b467e7a53dd`). Create/update `ARTICLE_EMAIL_MAP` in extract script for future reference.

**Common Mistakes to Avoid:**
1. **Renaming contributor image files** — NEVER rename `IMG_4824.jpeg` to `photo-01.jpeg` or any other name, regardless of source. The original filename is the permanent identity of the image. Renaming breaks the caption-to-photo link and causes git's rename-detection to scramble binary content across commits and merges. This rule is absolute for Gmail, Google Drive, Windows Downloads, and PDF extraction.
2. **Writing captions before reading the source emails** — Museum credits, photo credits, and caption text are precise attribution. Never infer or fabricate them. Fetch every caption email before writing a single `<figcaption>`. If a contributor sends captions in separate emails ("Image and Credit 1 of 8"), read all of them first. **Caption-before-image pattern:** when contributors list photos after article text, the label appearing *before* each image in the email body is that image's caption. Build an explicit full-filename → exact-caption-or-none map from the email before writing any `<figure>` HTML. Never correct contributor spelling in captions — use verbatim text and flag typos to the editor.
3. **Editing contributor article text** — Paste the contributor's words verbatim. No paraphrasing, restructuring, or "improvements." The only changes allowed are HTML formatting tags. If the text seems rough, that is not a reason to rewrite it — flag it to Judy instead.
4. **Using the email address prefix as a display name** — `sigalina@aol.com` does not mean the person's name is Sigalina. Always use the name from the email signature or a prior published byline. Email address ≠ person's name.
5. **Word document extraction is silently lossy** — After building HTML from a .docx, always diff the published article paragraph-by-paragraph against the original Word doc. Parentheticals, mid-paragraph sentences, and entire paragraphs can disappear with no obvious gap. Never assume the conversion was complete because the text reads coherently.
6. **Q&A and interview articles require a question count check** — Count the number of questions in the source (email, Word doc, PDF) and verify the exact same count appears in the HTML before publishing. Q&A format is the most dangerous for silent omissions: each dropped Q&A leaves no obvious gap and the article still reads coherently. Also verify photo-to-person matching by name — photos of named individuals cannot be inferred from image content alone; match them explicitly against the source.
7. **Google Drive shortcuts download as HTML, not images** — Don't use shortcuts. Ask for real files or email attachments.
8. **Assume articles are missing BEFORE checking email** — john.bartlett@gmail.com is always the source of truth. Search for contributor names and dates first.
9. **Forget to install PyPDF2 for PDF articles** — Setup venv first: `python3 -m venv .venv && source .venv/bin/activate && pip install PyPDF2`
10. **Use carousels for article photos** — All photos must be inline `<figure>` elements, not carousels. Carousel approach distorts images.
11. **Put author bio in article** — Author name links to About section in byline only. No bio text in article body.
12. **Skip internal nav on dev2** — Add `<!-- dev2-only -->` nav section to all articles (commented for dev/master).
13. ~~Update editors pages~~ — Obsolete. `editors/edition.html` and `editors/index.html` were removed Jun 22, 2026 and no longer exist. After `vercel deploy --yes`, just update the stable alias (see Dev2 preview deployments) — nothing else to update.
14. **Verify AFTER publishing** — Run `python3 tools/verify_edition.py YYYY-MM-DD` before marking edition as complete.
15. **Sending emails without asking** — Always ask "Should I send this or save as a draft?" before sending any email. Never send autonomously unless explicitly told to.
16. **Assuming caption = label before image** — The label appearing before an image in an email body is *sometimes* a caption, but may also be a placement instruction (e.g. "Photo 1", "Cover"). Verify from context; when uncertain, ask before writing `<figcaption>`.
17. **Assuming only Annie specifies photo layout** — Any contributor (Ana, Emma, Judy, the author) may define photo placement order in their article. Always check the source email for placement instructions before building. If the intended order is unclear, ask.
18. **Silently correcting contributor spelling** — Never fix a typo in contributor text without flagging it to the editor first. Use verbatim text and note the suspected error.
19. **Missing nav thumbnails** — Every article-to-article prev/next link must have a thumbnail `<img>` (70×70px, `object-fit:cover`). Only homepage links (`../../../index.html`) are exempt. `verify_edition.py` now checks this — run it before staging.
20. **DateBook is persistent — copy it each week** — The DateBook never comes down; its events auto-dim via JS as they pass. Each new edition must copy the previous week's datebook folder: `cp -r editions/PREV-DATE/datebook editions/NEW-DATE/datebook`, then update the title/kicker date. Never remove DateBook nav links from articles.
21. **Astrochart (daily-star) must also be copied each week** — Like the DateBook, the Astrochart folder (`daily-star-MONTH/`) must be copied from the previous edition: `cp -r editions/PREV-DATE/daily-star-MONTH editions/NEW-DATE/daily-star-MONTH`. If it is missing, the Astrochart link is a 404. Do this at edition setup, same time as DateBook copy. After copying: (a) delete all `<section>` blocks and `<option>` entries with dates before the current edition date, and (b) verify coverage extends through the end of the current month. If data is missing, add to the To Do list: "Email Victoria (`vconst@aol.com`) for [Month] forecast — current data ends [date]." A 1 KB .docx from Victoria is empty/corrupt — always check file size before trusting it.
22. **Update DateBook and Astrochart links on the homepage before publishing** — `index.html` has nav links to both `editions/YYYY-MM-DD/datebook/` and `editions/YYYY-MM-DD/daily-star-MONTH/`. These must point to the current edition, not the previous one. Check both before any push to dev or master: `grep -E "datebook|daily-star" index.html`. Stale links send live readers to old content.
23. **Homepage hero meta: author name only, no date** — The hero article on the homepage shows `<div class="hero-meta">By [Author Name]</div>`. It must not include the edition date. The date appears elsewhere on the page; adding it to the hero byline is redundant and was flagged as incorrect.
24. **Never put internal links in the public nav** — Stats, Reader Comments, Future Articles, and the Staff Dashboard are internal tools. They belong only in the `<!-- dev2-only -->` internal-nav bar, never in the public nav.
25. **Nav pattern: nav-inner contains Home, DateBook, Astrochart, Editors' Page, then the hamburger button. Hamburger contains About, Subscribe, Advertise.** The public Editors' Page (`editorial.html`) was introduced June 14, 2026 and lives in the main nav-inner row (not the hamburger). `verify_edition.py` checks for About/Subscribe/Advertise appearing in nav-inner (a doubled-menu bug) — keep those three in the hamburger only.
26. **Compress photos before pushing to master** — Cloudflare Pages rejects files over 25 MB. Run `verify_edition.py` before staging; it now flags oversized images. To compress: `source .venv/bin/activate && python3 -c "from PIL import Image; img=Image.open('path'); img.thumbnail((3000,3000), Image.LANCZOS); img.save('path','JPEG',quality=75,optimize=True)"`. Run a full-repo scan before major pushes: `find editions/ -name "*.jpg" -o -name "*.jpeg" | while read f; do [ $(stat -c%s "$f") -gt 26214400 ] && echo "$f"; done`. This hit production twice in two consecutive sessions — scan the whole repo, not just the current edition.
27. **COVER photos belong on the homepage card, not in the article body** — Any photo with "COVER" in its filename (e.g. `COVER Mark and Robin Tebbe.JPG`) is the homepage card image. Do not include it in the article body unless the contributor explicitly says to AND it has a caption. If it's already the card image and has no caption, leave it out of the body entirely.
28. **Build a photo map before placing any figures** — Before writing any `<figure>` HTML, create an explicit map: `filename → caption (verbatim from email) → placement (after which paragraph/sentence)`. If any field is unknown, stop and find it. This is especially critical when photos arrive in separate emails, the source is a PDF, or the contributor numbers photos without specifying positions.
29. **PDF articles: never place photos without explicit placement instructions** — PDFs have no embedded photo layout. Build the article text first (no photos), then ask or check the contributor's email for where each photo goes. Don't guess based on content.
30. **Don't place a photo as both the opening hero AND inline in the body** — If a photo appears at the top of the article as a hero figure AND is also placed at its correct inline position in the body, it shows up twice. When building from explicit placement instructions, use those positions only — don't add a separate hero figure unless the contributor explicitly requests one.
31. **Verify photo order after placing in high-count articles** — For articles with more than ~6 photos, do a verification pass after placing all of them: read the HTML top to bottom and confirm each `<figure>` appears immediately after its specified anchor sentence. With 24 photos (as in San Miguel), adjacent photos can be swapped or land one paragraph off. Never trust order is correct just because all photos are present.
33. **Never share the dev2 URL with writers or outside contributors** — The dev2 staging URL (`article-dev2.vercel.app`) is internal only. When a writer asks to preview their article, send them the direct article page URL on dev2 (e.g. `https://article-dev2.vercel.app/editions/YYYY-MM-DD/slug/`) — never the homepage. Only do this once the article is finalized exactly as it will appear in the published edition. **Before sharing the URL, temporarily remove the article from the nav chain** (disconnect its prev/next links so the reader cannot browse to other articles or the homepage card). Restore the nav links after the writer has confirmed.

34. **Never use emojis in article content** — Classic Chicago Magazine articles must never contain emojis. This applies to article body text, headings, captions, bylines, and any user-facing copy. If a contributor's submitted text contains emojis, remove them silently.

32. **Remove dangling git submodule entries** — If a folder was ever added as a git submodule (e.g. `exif-mcp`) but the `.gitmodules` file is gone, git still tracks it in the index and Cloudflare will fail with "No url found for submodule path." Fix with `git rm --cached <folder>` and commit. Run `git ls-files --stage | grep "^160000"` to check for dangling submodules before any major push.

35. **Cloudflare caches aggressively — use the rename trick when changes don't appear** — If a pushed change (image, HTML, CSS) doesn't appear on chicagoclassicmag.com within 2 minutes of a confirmed deploy, Cloudflare is serving a cached version. Fix: rename the file to a new name (e.g. `photo.jpg` → `photo-v2.jpg`), update all HTML references, push, confirm it's live, then rename back to the original and push again. A new URL bypasses the CDN cache entirely. This works for any file type. When grepping to confirm a change is live, use a specific selector (e.g. `grep "soma-roy" | grep "center top"`), not a generic term that may appear elsewhere in the page.

36. **Claude can run git push directly — only ask user when token expires** — `git push origin master/dev/dev2` works fine via the Bash tool. Never use the `!` prefix for git pushes (it silently fails when credentials are needed). The only time user action is needed: if a push silently fails and `origin` doesn't advance, the GitHub token in the remote URL has expired. Ask the user to generate a new token at github.com/settings/tokens and run: `git remote set-url origin https://NEW_TOKEN@github.com/JohnBartlett/article.git`

37. **Check EMAIL_LOG.md before searching for emails — never use a fixed `newer_than:Nd` window** — Read the last entry date in `EMAIL_LOG.md` first, then search `after:YYYY/MM/DD` (Gmail date format) to fetch only emails that arrived after the last processed date. Using a fixed window like `newer_than:3d` re-fetches already-logged emails and wastes time re-processing them.
38. **Multi-part articles always run one part per edition, across consecutive weeks — never bundled in a single edition.** This applies to any article explicitly split into parts (Letter from Paris, Kiddieland's Closing, and any future series). Part 1 goes in the edition it's announced for; Part 2 the following week; Part 3 the week after that, etc. When building a multi-part split, only nav-link and homepage-card the current week's part — the other parts stay built and saved on disk but fully unlinked (no nav entry, no homepage card, no about.html popup entry) until their own week arrives. This was corrected on the July 12, 2026 edition after Letter from Paris was incorrectly built with all 3 parts linked into one edition, despite the source email explicitly agreeing to "run across three consecutive issues" — and after the user had already corrected this exact mistake twice before. Before ever splitting an article into parts, re-read the actual scheduling agreement (don't trust an inherited citation in STATUS.md) and confirm one-part-per-edition explicitly with the user if it isn't unambiguous in the source.

### Recurring email workflow

Run `/check-emails` to execute this workflow. Do it at the start of a session or when Judy may have sent instructions.

**Sources:**
- Judy Carmack Bross (`judycbross@aol.com`) — editorial instructions, bio updates, photo requests, text corrections
- Annie Delfosse (`aedelfosse1@gmail.com`) — DateBook updates, article content (e.g. Katherine Harvey's articles)
- Ana Baca (`anabaca8@gmail.com`) — photos and article content for Philip Vidal's About the Town column
- Emma Muhleman (`emuhl2@uic.edu`) — article content and photos (intern, UIC)
- FormSubmit (`submissions@formsubmit.co` → `editor@2ccmag.com`) — reader comments and Quick Votes

**What to expect from FormSubmit:**
- "Classic Chicago Reader Comment" — check the `comment` field; empty submissions are common (reader opened form, didn't type)
- "Classic Chicago Quick Vote" — vote=Yes means reader liked the article; `Environment: dev2` = test, ignore
- Real comments (non-empty, non-dev2) go in `reader-comments.html` — this file lives on the `editors` branch, not `dev2`. Updating it requires checking out `editors` separately (e.g. `git worktree add /tmp/editors-worktree editors`); it isn't part of the normal dev2 session
- If a comment raises an editorial concern (criticism of a feature, content question), also add it to `comments.html` under a "Reader Comments" section (this one does live on dev2)

**Common bio locations in `about.html`:**
- Judy and Megan: Our Team section
- Writers and curators: More Contributors section (permanent bio cards — persists across editions)
- "Our Writers This Week" section: edition-specific rotation, updated each week by `/edition-checks`
- Annie Delfosse: `id="annie-delfosse"` (linked from DateBook page)

### Editors menu (Internal nav — dev2 only)
The `.internal-nav` bar sits below the main nav in the `<header>`. On dev2 it is **uncommented and visible**; it must be commented out before promoting to `dev` or `master` (handled automatically by `/stage`).

To update it for a new edition, edit the `<!-- dev2-only -->` block in `index.html`:
- Add/remove edition-specific links (e.g. editorial critique, datebook drafts) as needed
- Do NOT include reader-comments.html or future-articles.html in the internal nav — reader-comments.html isn't even on this branch (it's on `editors`), and future-articles.html is a planning doc, not reader-facing
- Remove any stale edition-specific links from the prior edition

The comment marker convention:
- **Active (dev2):** `<!-- dev2-only -->` followed immediately by the `<div class="internal-nav">` block (no closing `-->`)
- **Hidden (dev/master):** wrap entire block in `<!-- dev2-only ... -->`

### Email style (Judy and notifications)
- **To Judy:** Salutation `Dear Judy,` / Sign-off `Cheers, John` / first person (I/me, not we/us)
- **Publication notification:** To `judycbross@aol.com`, CC `john.bartlett@gmail.com`
