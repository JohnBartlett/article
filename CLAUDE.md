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
- **Sigalit Zetouni** — Arts Editor (`sigalina@aol.com`; email prefix "sigalina" is not her display name — always byline as "Sigalit Zetouni"); also writes her own pieces (Blast teasers, features)
- **John Bartlett** — Managing Editor & Technology Editor (`john.bartlett@gmail.com`)

### Writers (update "Our Writers This Week" on about.html each edition)
- Bob Glaze — Culinary & Cultural Guide
- Katherine Harvey — Travel Writer
- Susan Aurinko — Arts & Photography (My Silk Roads column)
- Jen Huang — Magazine Intern (UIC student)
- Emma Muhleman (`emuhl2@uic.edu`, `muhlemane2@gmail.com`) — Magazine Intern (UIC student). Also acts as a production assistant for other writers (e.g. Bob Glaze): she receives their finished article/photos and packages it up to send to John, but is not herself the author unless she's explicitly the byline — don't infer authorship from her being the sender.
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
  - Auto-refreshed by `.github/workflows/refresh-editors-dashboard.yml`, which checks out `dev2` (for the build scripts, GA4/Gmail credentials, and the `editions/`/`STATUS.md` files it reads from) and `editors` (the publish target) side by side, builds from the `dev2` checkout, then commits/pushes the output to `editors` only. **The cron itself is hourly** (`37 * * * *`), but GitHub's best-effort scheduling for this repo actually lands it every 2-7 hours in practice (confirmed via `gh run list` 2026-09-14) — "every 6 hours" describes observed real-world cadence, not the workflow's own trigger; don't read the YAML expecting an hourly guarantee. Each run also takes 12-16 minutes, consistent with a full re-scan rather than an incremental fetch — not yet investigated for a fix.
  - Two different "current edition" concepts feed the page: the **prep edition** (latest edition folder with an active `STATUS.md` — may be a future, not-yet-published date) drives Article Status/Decisions Needed; the **GA4 edition** (latest *published* edition, `date <= today`) drives all the reader-stats sections, since GA4 can't report on traffic for a page that isn't live yet.
  - Do not add `editors/dashboard.html` (or the old `editors/stats.html`) back to `dev2` — `editors/stats.html` is gitignored there to prevent drift.
  - **The GitHub default branch is `actions`, not `dev2` or `master`** — scheduled cron runs read workflow YAML from the default branch, so `.github/workflows/refresh-editors-dashboard.yml` must be kept in sync on both `dev2` and `actions` (e.g. via a temporary `git worktree add /tmp/actions-worktree actions`). The `actions` branch is otherwise just a stale full-repo mirror; nothing else on it is used at runtime.
  - **To force an immediate rebuild** (don't wait for the 6-hour cron): `gh workflow run "Refresh Editors Dashboard" --ref actions`, then poll `gh run view <run_id> --json status,conclusion` until `completed`. Verify the live result with a cache-busted `curl -H "Cache-Control: no-cache" ".../dashboard?cb=$(date +%s)"` — don't trust a stale browser/CDN cache.
  - **GA4 credentials (`tools/credentials.json`) do not exist on this machine** — they're gitignored and only materialize inside the GitHub Actions run (written at runtime from the `GA4_CREDENTIALS_JSON`/`GMAIL_OAUTH_KEYS`/`GMAIL_CREDENTIALS` secrets, which are write-only — not readable by anyone, including the repo owner, once set). Don't waste a session hunting for the key locally; either read the dashboard's live output, or trigger the workflow above and read its logs (`gh run view <id> --log`).
  - **`fetch_gmail_votes_comments()`'s Gmail search must fully subject-anchor every OR'd term.** A query like `subject:("Classic Chicago") (vote OR comment OR "Form Submission")` only scopes the *first* clause to the subject — the OR'd terms search the whole message, so an unrelated forwarded article whose subject happens to contain "Classic Chicago" and whose long body happens to contain the word "comment" gets swept in, parses to an all-blank record, and produces a bogus leaderboard row (this happened Jul 29, from a forwarded short-story email). Correct form: `(subject:"Classic Chicago Quick Vote" OR subject:"Classic Chicago Reader Comment" OR subject:"Classic Chicago Form Submission")` — every branch subject-anchored. Also keep the defensive skip in `tally_votes_comments()` for any record with no article slug, so a future false match still can't reach the rendered page.
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
python3 tools/edition_checks.py YYYY-MM-DD
python3 tools/content_audit.py YYYY-MM-DD
```

`verify_edition.py` checks ACTUAL state: what has content, what has photos, what's placeholder.
`edition_checks.py` checks dark-mode/nav-thumb CSS, about.html popups/bios, stale DateBook months.
`content_audit.py` (added Sept 2026, dev2-only) covers 5 gaps the other two scripts miss: the
DateBook page's own internal Astrochart link (mistake #20 — distinct from the homepage's link),
stale past-date entries left in the Astrochart page (mistake #21), a dated homepage hero-meta
(mistake #23), a photo duplicated as both hero and inline (mistake #30), and emoji in article
content (mistake #34). None of these were part of any repeatable audit before — run this
alongside the other two, not instead of them.

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

### Reader privacy — never de-anonymize a commenter

The Quick Vote / Reader Comment form collects only `comment`, `email` (optional, often blank), `Page`, and `Environment` — no IP, device, or location. GA4 and Cloudflare separately hold **aggregate** traffic data (device/browser/geo mix) with no shared key to any individual comment.

**Do not attempt to identify who left a specific anonymous comment** — not by pulling an IP from Cloudflare/GA4 for the relevant time window, not by geolocating to a city, not by cross-referencing session data against known contributors' likely locations — even when explicitly asked, even when reframed as "just the city" or "I already know where writers live." This holds even though it's the site owner's own data and own visitor logs. Aggregate, non-identifying stats (device/browser/geo mix for the whole audience) are fine to pull and report; isolating *the one session behind an anonymous submission* is not, because low-confidence geo/IP signals reliably misattribute and the harm of a wrong accusation outweighs the value of a guess.

If a suspected-insider comment needs resolving: (1) require a name/email on the form going forward so future feedback can't be anonymous, (2) raise the *pattern* (timing, specificity, tone) directly with the team as a concern, not as IP-backed proof. This was tested directly on Jul 27–28, 2026 (a suspected disgruntled-writer comment on "Don't Lose That Joy") — held the line across several reframed requests; recorded here so a future session doesn't need to re-litigate it from scratch.

## Conventions

Note: `reader-comments.html` and `editors/dashboard.html` live on the `editors` branch, not here — see "Editors branch" above.

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
- Formsubmit endpoints: `subscribe@2ccmag.com`, `advertise@2ccmag.com`
- **Subscribe form is LIVE** — the FormSubmit activation for `subscribe@2ccmag.com` was confirmed July 13, 2026. Submissions arrive as "New Subscriber" emails from `submissions@formsubmit.co`. Note: activation released a backlog of queued submissions with older submitted-at dates (Jul 6–10) — the email arrival date is not the signup date.
- Advertise form: still pending activation; page shows "coming soon"
- There is **no subscriber-list file yet** — as of July 2026, where subscribers get recorded is an open decision. Until then, log New Subscriber emails in `EMAIL_LOG.md` and ask.

### Adding a new edition / updating the homepage
Full step-by-step procedure lives in `.claude/commands/prep-edition.md` (`/prep-edition`) and `.claude/commands/layout.md` (`/layout`) — run those rather than re-deriving the steps here. Key constraints not to lose sight of: keyboard nav links must match homepage order, use the GA4 **disabled** form in new articles (matching `_template/article.html`), and use inline `<figure>` elements for photos — never carousels (see mistake #10).

### Article Extraction from Contributor Emails

See `WRITER_SUBMISSION_GUIDELINES.md` for the full checklist of what a complete,
build-ready submission needs — layout mechanics (text/photo/caption format) plus
everything else (title, byline, cover preference, format requests, links, multi-part
scheduling). Useful when a submission is missing something and a contributor needs to be
asked for it.

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
- `sigalina@aol.com` — Sigalit Zetouni, Arts Editor (sends articles directly to John; email address uses "sigalina" but her byline name is Sigalit)

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
20. **DateBook is persistent — copy it each week** — The DateBook never comes down; its events auto-dim via JS as they pass. Each new edition must copy the previous week's datebook folder: `cp -r editions/PREV-DATE/datebook editions/NEW-DATE/datebook`, then update the title/kicker date. Never remove DateBook nav links from articles. **Entire past months must be edited out, not just individually-dimmed past events** — copying forward means whole month sections (e.g. a June `<!-- ═ MONTH ═ -->` block) can linger for editions that are now in July or later. `tools/edition_checks.py` checks for this automatically (`stale_datebook_months` in the report) — remove any flagged month's full block (comment, `month-header` div, and `event-list` div) before staging. Also check the DateBook page's own internal Astrochart nav link (`daily-star-MONTH`) — it can go stale the same way and won't be caught by the homepage's DateBook/Astrochart link check.
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

39. **Always `git pull --rebase` before pushing any branch — remotes advance mid-session.** Parallel Claude sessions push to `dev2`, and the GitHub Actions dashboard refresh (every 6 hours) pushes to `editors`, so a branch that was current at session start is often behind by push time. Both pushes in the Jul 14 session were rejected as non-fast-forward on the first try. Pattern: commit → `git pull --rebase origin <branch>` → push. Never force-push to resolve it.

40. **A fix isn't done until the person who reported the problem is answered.** Judy's Jul 12 "photo is still on its side" follow-up was fixed in-repo the same day (EXIF strip + cache-bust rename), but no one told her — the fix sat invisible to her for two days. When closing out a reported problem, draft the confirmation reply to the reporter as part of the fix (send only after asking, per mistake #15), and mark "reply owed" in `EMAIL_LOG.md` if it can't go out yet.

41. **Judy's edition lineup email is the source of truth for what runs — reconcile it against prior plans.** Her "The July 19th Issue" lineup omitted Kiddieland Part 2 even though a 3-part schedule had been agreed days earlier. When a lineup arrives, diff it against STATUS.md / future-articles.html / prior multi-part agreements and flag every discrepancy to her rather than silently following either version.

42. **Link-heavy contributor articles (Philip Vidal's About the Town, and any similar roundup piece) need a link-count check against the source email before marking Ready.** The Sept. 2026 "About the Town" article was built with all 39 of Philip's inline links to event/venue pages silently dropped — the article read coherently with plain text where links should have been, so it passed every other check and was almost published without them. Before marking such an article Ready, count the `<a href="http...">` links in the source email and confirm the same count (matched to the same anchor text/venue names) appears in the built HTML — this is the same failure mode as mistake #6's Q&A count check: a dropped link, like a dropped question, leaves no visible gap.
43. **PDF text extraction loses paragraph breaks and all italics/bold — verify against rendered pages, not just extracted text, before marking a PDF-sourced article Ready.** Jill Lowe's Sept 13, 2026 "Chitchat" article was built from PyPDF2's `page.extract_text()`, which returns one flat character stream per page with no blank-line breaks and no font-style information at all. The result: her distinct paragraphs were silently merged into run-on blocks, a mid-document heading landed in the wrong position, four italicized book/essay titles came out in quotation marks instead, two italicized terms lost their emphasis, and a dropped parenthetical ("...Phatic Communion **(or Communication)**") went unnoticed — none of it visible from reading the extracted text alone, since it still read as grammatically coherent English. This was only caught after Jill complained and a full page-by-page comparison was done: `pdftotext -layout` (preserves paragraph breaks, same one-command cost as PyPDF2) plus `pdftoppm -png` to render every page as an image for a visual read alongside the build. **For any PDF-sourced article: use `pdftotext -layout` instead of PyPDF2 for extraction, and render the source pages as images once while placing photos/headings** — this costs no more time than the current process, it just uses a tool that doesn't discard information. See also mistake #29 (never place photos without explicit placement instructions) and mistake #6 (Q&A count checks) — this is the same "silent, undetectable loss" failure family, now extended to structure/formatting, not just content.
44. **A missing `.article-meta a` CSS rule makes the byline link render as a default blue/underlined link instead of the site's brand-red/no-underline convention — and this recurs because the earlier fix was a one-time manual patch, not a standing check.** First found and manually fixed across 7 templates in an August 2026 session; recurred in Sept 13's Chitchat because nothing was added at the time to catch it in future articles. `tools/edition_checks.py` now checks for and auto-adds this rule (see the `article_meta_a_added` check) — run `edition_checks.py` on every edition and trust its report, don't rely on remembering this by eye.
45. **A manual prose/grammar audit pass must be exhaustive, not sampled — a clear word-substitution typo can sit next to ones that were caught and still get missed.** The Sept 12, 2026 manual audit of Chitchat caught a lowercase "iphone," a doubled "is," and a missing "as," but missed "Mucho of phatic communion is strictly rhetorical" (should be "Much") in the very next section — a substitution at least as obvious as the ones it did catch. When running a prose audit, confirm every paragraph was actually read, not just the ones that happened to surface issues on a first pass.
46. **Bundled-document sources (a single PDF or Word doc with embedded photos) carry more placement/identity risk than individually-captioned email attachments, and need a different verification depth.** Compare Sig Zetouni's Chef photos (9 separate emails, one photo + one caption each — no ambiguity possible about which caption belongs to which file) against Jill Lowe's Chitchat PDF (7 photos embedded in one document, generically-named screenshot files, no separate caption list) — the PDF format is exactly what let two of Jill's photos get swapped (matched by eye, once, no second check, wrong). For any article built from a bundled document rather than individually captioned attachments: (a) do a page-by-page visual comparison per mistake #43 before marking Ready, and (b) when photo filenames don't hash-match their embedded PDF counterparts, treat that manual visual match as a single point of failure — do it once, then verify it a second time before placing, since there is no automated backstop for a wrong match.
47. **CCM's tools-driven build process, house style, and editorial authority are not things to apologize for or second-guess in isolation.** (1) Building from tooling (PyPDF2/pdftotext extraction, automated checks) instead of manually re-typesetting every contributor's source is a real production necessity — most editions have about one day (Saturday) to lay out; the fix for a tooling gap is a better tool or an added check, not "stop using tools." (2) CCM's grammar/punctuation reference is the Chicago Manual of Style (CMOS), but visual layout (pull-quotes, heading treatment, photo placement) follows CCM's own established site conventions, not necessarily whatever a contributor's source document did visually — CMOS answers "is this correct," not "how should this look." (3) CCM does not routinely share laid-out articles with contributors before publishing, including editor-contributors with their own site access (e.g. Sigalit Zetouni sent two corrections on her own Chef article, Sept 12, 2026, without having seen the built page) — this is a timing/production-squeeze reality, not a reflection of care. (4) A contributor's source layout and captions are *signal* for understanding intent, not a binding instruction CCM must replicate exactly — CCM is the final arbiter of photo placement and layout format. When fixing a build against a contributor's source, the goal is correcting actual transcription errors (lost breaks, swapped photos, dropped formatting), not treating every visual choice in the source as a mandate. See the Sept 13, 2026 Chitchat session: restoring Jill's paragraph breaks and fixing swapped photos were genuine error corrections; keeping the closing Fitzgerald/Tolstoy pull-quotes grouped together instead of splitting them with a photo (as her PDF did) was a deliberate CCM layout call, owned as such.

48. **Every `editions/YYYY-MM-DD/` folder linked from the homepage's Past Editions section needs its own `index.html`, or Cloudflare's fallback silently serves the root homepage's HTML at that URL — and because the homepage's own links are relative (no leading slash), every link on that mis-served page compounds into a doubled, broken path.** This is the third confirmed occurrence of the same bug class (first Aug 16/23, fixed manually; then Sept 13, caught and fixed mid-session; then Sept 6, which reached Judy as a live "I think something has popped out again, not able to see photos or get back issues" report before it was root-caused). `verify_edition.py` now checks this automatically (`PAST-EDITION LANDING PAGE ISSUES`) — every `editions/DATE/` folder the homepage links to via `href="editions/DATE/"` is checked for a real `index.html`. Run it after every homepage edit, not just after `/prep-edition`, since moving an edition into Past Editions is exactly the moment this bug activates.
49. **A recurring "harmless-looking" automation bug is still worth fixing once confirmed, not just re-logged.** `fetch-email-attachments.yml`'s re-staging bug recurred 9 times across the Sept 20 edition build alone (`EMAIL_LOG.md` items #158 onward) before being fixed 2026-09-18 — its idempotency check was based on whether a message's `_attachment-staging/<id>/` folder currently existed, but the normal consumption workflow *deletes* that folder once its files are placed, so every consumed message looked "never staged" again on the very next hourly run and got silently re-downloaded, forever. Nine cloud passes each independently re-discovered and re-cleaned the same duplicates rather than anyone fixing the root cause, because each pass treated it as a one-off nuisance rather than tallying the recurrence count. Fixed by adding a permanent ledger (`_attachment-staging/.staged_log.json`) checked *before* folder existence, which survives the folder's deletion. Lesson: when the same automated-workflow bug is logged 3+ times with the same signature, stop re-logging it and fix the actual code — "it happened again" is itself the signal that a targeted fix, not another cleanup pass, is due.
50. **Audit scripts must be re-run and their new checks trusted, not just written.** Both fixes above (#48, #49) were found by directly investigating a user-reported symptom, not by an existing audit catching them first — `verify_edition.py`/`edition_checks.py`/`content_audit.py` had no coverage for either failure mode until this session added it. When a real bug is found this way, the fix isn't complete until an automated check exists that would have caught it, per the standing philosophy that audits should convert "found this once by hand" into "will never silently recur."
51. **A GitHub Actions cron tied to a specific historical date, left in the repo after its one-time use, is a live landmine, not dead code.** `scheduled-deploy.yml` was a one-time deploy cron for a single February 2026 date that remained armed to fire again automatically the following year, auto-merging `dev` into `master` with none of `/publish`'s safety checks (no GA4 re-enable, no oversized-image/submodule/DateBook-freshness checks). Found and deleted 2026-09-14 during a routine process-efficiency review, not because anything had gone wrong yet. Periodically audit `.github/workflows/*.yml` for `schedule:` triggers using a fixed calendar date (not a repeating pattern like `* * * *`) — those are one-time crons that need deleting after use, not left dormant.
52. **The Vercel `dev2` preview alias does not update itself — it must be manually redeployed after every commit batch, and a stale preview looks indistinguishable from broken code.** Mid-session, a redeployed homepage with real photos placed by the automated cloud routine still showed all-placeholder images on `article-dev2.vercel.app`, prompting a report of "I don't see any articles at all" — the code was correct throughout; only the deployed preview was several commits behind. Redeploy (`vercel deploy --yes` + `vercel alias set`) proactively after committing a meaningful batch of dev2 changes, rather than waiting to be asked or assuming the alias auto-tracks the branch — the same applies to the `dev` branch's Vercel alias (see mistake list generally; that one has a known-broken git integration on top of the same non-auto-update behavior).
53. **A contributor's PDF/document can contain real embedded hyperlinks invisible to any plain-text extraction — check for them with a dedicated annotation-extraction step, not just `pdftotext`.** Jackson LeJeune's Coyote vs. Acme review PDF cited "the 1990 New Yorker article of the same name" as a real clickable link to `newyorker.com`, visible only via PDF annotation extraction (`PyPDF2`'s `/Annots` → `/A` → `/URI`), not in `pdftotext -layout`'s plain text or even in a rendered-page screenshot read casually. Silently dropping it would have been the same failure class as mistake #42 (dropped links leave no visible gap) but originating from a PDF instead of an email body. For any PDF-sourced article, check for embedded link annotations as a standard step alongside the page-image visual-placement check from mistake #43.
54. **An email that "looks" attachment-free from its rendered body may still carry a real attachment — check the full MIME part list before concluding text hasn't arrived.** Adrian Naves's "My article" email (forwarded by Judy, Sept 19, 2026) was read once via a body-only fetch and logged as "no article text at all, only Drive-linked photos" — a reasonable-looking but wrong conclusion, because the email actually carried a real `.docx` attachment (`History of The Hawthorne Works Complex.docx`) that a body-only read simply doesn't surface. This nearly caused a second, unnecessary round of chasing Annie/Adrian for text that had already arrived. **Before declaring any email "text missing" or "photos only,"** fetch the message with `format=full` (or equivalent) and check the actual MIME part list/filenames, not just the rendered plain-text/HTML body — an attachment can be present with zero mention of it in the visible text.
55. **For any recurring columnist, check their own previously published articles for established category/style conventions before defaulting to a generic one on a new piece.** Bob Glaze's "My Favorite Fall Destinations in Chicago" was initially left under the template's default article-category ("Culinary & Cultural Guide") until a check of his prior bylines (`editions/2026-04-19/bob-glaze/`, `2026-06-21/bob-glaze/`, etc.) showed "Weekend Road Trips" is his established column name — confirmed further by his own about.html bio text. Before publishing a new piece by an author who already has prior CCM articles, grep their other bylines for the category convention they've actually been running under, rather than leaving a template default in place.
56. **A production assistant/coordinator sending an article on a writer's behalf is not the author — check the team roster before inferring authorship from the sender, and confirm explicitly rather than guessing either way.** Emma Muhleman (`muhlemane2@gmail.com`) sent Bob Glaze's "Fall Destinations" column in her own name with no byline stated anywhere in the email; her role in CLAUDE.md's roster is "production assistant" for other writers (she packages a contributor's finished piece to forward to John), not an author herself unless explicitly credited. The correct handling — confirmed twice independently (once by Judy's own forward, once by John directly asking Emma) — was to keep the byline as the actual writer (Bob Glaze), not the sender. This generalizes mistake #4 (email address ≠ display name) to production/coordinator roles specifically: always check whether a sender is a known coordinator for someone else before treating "who sent it" as "who wrote it."
57. **Google Drive photo links that exceed the Drive MCP connector's ~10MB per-file cap need a Chrome fallback — and the direct export URL is far more reliable than the viewer page's download button.** Both Hawthorne Works' remaining photos and all 17 of Basak Notz's Drive-linked photos (full-resolution contributor photos routinely run 20–37MB) failed the Drive MCP connector identically ("file too large"). Clicking the download icon on `drive.google.com/file/d/<id>/view` works but is flaky — it often silently fails and needs 2–9 retries with no visible error (the button lives in Drive's native viewer chrome, not a standard webpage element). **Navigating Chrome directly to `https://drive.google.com/uc?export=download&id=<fileId>` downloads the file straight to `~/Downloads/` reliably on the first attempt** — prefer this over the click-through UI once the Drive MCP has failed on size.
58. **Before sending any consolidated status/ask email that bundles multiple open items, cross-check the current edition's full Blockers list in STATUS.md item-by-item — don't assemble the ask list from memory.** A combined email to Emma and Annie (Sept 19, 2026) covering the two live blockers (Bob Glaze's photo map, Newberry's missing text) omitted a third open item — Dominic Pacyga's missing about.html bio — even though it was already documented in STATUS.md's Blockers section at the time of sending. Caught only because John asked directly after the fact, requiring a separate follow-up email. Read the Blockers list fresh immediately before drafting any multi-item status email, rather than relying on what's been discussed recently in conversation.
59. **Documentation describing a script's intended behavior is not proof the script actually does it — verify against the code, not the prose.** CLAUDE.md's "Our Writers" section stated that `/edition-checks` "added to" the Our Writers grid each week, but `tools/edition_checks.py`'s `check_new_authors()` only ever flagged a missing bio in its printed report — it never wrote a stub card into `about.html`. This went unnoticed because the flagged output looked like the intended behavior working ("here's what needs a bio"), and no one checked the actual insertion logic. Caught only because John asked "does the audit not do X?" directly. When CLAUDE.md or a skill file asserts that a script performs an action, confirm it by reading the script's actual code path, not just by trusting the doc or the script's own printed summary.

60. **A `/prep-edition` placeholder teaser ("Coming in the [date] edition.") on a homepage hero/card is not self-correcting once the article is actually built — nothing in the pipeline ever goes back to write a real teaser.** The Sept 20 homepage still showed this exact placeholder for both the hero (Basak Notz) and the Hawthorne Works card long after both articles were fully built, photographed, and marked Ready — caught only when John looked at the live homepage directly and reacted with alarm ("the first article is coming soon"). Every other homepage card had a real one-sentence teaser; these two were simply never revisited after the initial `/prep-edition` scaffold. `tools/content_audit.py` now checks for this (`check_homepage_stale_teasers`, mistake #60) — run it after every edition build, not just before staging, since the bug is live on the homepage the whole time an article is "Ready" but its teaser hasn't been rewritten.

### Recurring email workflow

Run `/check-emails` to execute this workflow. Do it at the start of a session or when Judy may have sent instructions.

**Tooling, updated 2026-09-19:** prefer the native Gmail MCP (`mcp__claude_ai_Gmail__*` — `search_threads`, `get_thread`, `get_message`, `create_draft`/`get_draft`/`update_draft`, `reply`, `forward`, `send_message`) over `~/.claude/scripts/gmail_api.py` and Chrome for every Gmail operation in this project. `gmail_api.py`/`tools/extract_article_photos.py` remain necessary only for downloading attachment bytes, since the Gmail MCP connector cannot fetch attachment content. When checking `get_message`/`get_thread`, use a full-content format and check the actual MIME parts — a body-only fetch will miss real attachments (see mistake #54). Before sending any consolidated status/ask email, always show the drafted email in full (via `get_draft`) and cross-check it against STATUS.md's current Blockers list (see mistake #58) before the user approves sending.

**Sources:**
- Judy Carmack Bross (`judycbross@aol.com`) — editorial instructions, bio updates, photo requests, text corrections
- Annie Delfosse (`aedelfosse1@gmail.com`) — DateBook updates, article content (e.g. Katherine Harvey's articles)
- Ana Baca (`anabaca8@gmail.com`) — photos and article content for Philip Vidal's About the Town column
- Emma Muhleman (`emuhl2@uic.edu`, `muhlemane2@gmail.com`) — her own article content/photos as a contributor, AND acts as production assistant for other writers (e.g. Bob Glaze) — when she sends a piece, check whether she's the named byline or just packaging someone else's finished work before assuming authorship (see mistake #56)
- FormSubmit (`submissions@formsubmit.co` → `editor@2ccmag.com`) — reader comments and Quick Votes

**What to expect from FormSubmit:**
- "Classic Chicago Reader Comment" — check the `comment` field; empty submissions are common (reader opened form, didn't type)
- "Classic Chicago Quick Vote" — vote=Yes means reader liked the article; `Environment: dev2` = test, ignore
- "New Subscriber" (to `subscribe@2ccmag.com`) — subscriber signups from the live subscribe form (active since Jul 13, 2026); log in `EMAIL_LOG.md` (no subscriber-list file exists yet)
- **Tallying votes/comments:** search `subject:"Classic Chicago Quick Vote" OR subject:"Classic Chicago Reader Comment" after:YYYY/MM/DD` and paginate — one page is rarely all of them. Gmail snippets truncate at "comment:", so a snippet ending there does NOT mean the comment is empty — fetch the full message for every Reader Comment before classifying it. Commenter identity is in the `email:` field (sometimes with a signed name in the comment body, e.g. Linda Landis Andrews).
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
