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
- Emma Muhleman (`emuhl2@uic.edu`) — Magazine Intern (UIC student)
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
2. Update two links in the editors pages:
   - `editors/edition.html` — Dev2 Preview button (points to current hero article)
   - `editors/index.html` — Dev Preview quick link (points to homepage)
3. Commit both files and push to dev2

```bash
PREVIEW_URL=$(vercel deploy --yes 2>&1 | grep "^Preview:" | head -1 | awk '{print $2}')
sed -i "s|href=\"https://article-[^/]*/editions/[^\"]*\"|href=\"${PREVIEW_URL}/editions/2026-03-29/driehaus-museum/\"|" editors/edition.html
sed -i "s|href=\"https://article-[^/]*/index\.html\"|href=\"${PREVIEW_URL}/index.html\"|" editors/index.html
git add editors/edition.html editors/index.html && git commit -m "Update dev2 preview URL" && git push origin dev2
```

### GitHub repo
- **Repo:** `JohnBartlett/article`

## Skills

| Skill | Purpose |
|---|---|
| `/check-emails` | Check Judy's emails and FormSubmit votes; apply changes; commit to dev2 |
| `/update-editors` | Refresh all four editors pages, pull fresh GA4/HA stats, deploy new Vercel preview |
| `/layout` | Audit and fix homepage order, article nav links, attribution lines, about.html popups |
| `/new-edition` | Build a new edition from Judy's emails; create article HTML; update homepage |
| `/preview` | Build a layout review page from an article email; deploy to Vercel; return URL |
| `/stage` | Promote dev2 → dev: disable GA4, comment out internal-nav, push, schedule production push |
| `/publish` | Promote dev → master: re-enable GA4, push to Cloudflare, email Judy and John |
| `/send-update` | Draft and send a weekly site activity + reader stats update to Judy |

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
export GA4_PROPERTY_ID="your-numeric-id"
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your-key.json"
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
├── reader-comments.html    Internal — reader votes/comments log (dev2 only)
├── future-articles.html    Internal — unpublished article planning (dev2 only)
├── comments.html           Internal — editorial notes (dev2 only)
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
│   ├── 2026-02-08/         Edition 1 — February 8, 2026
│   ├── 2026-02-15/         Edition 2 — February 15, 2026
│   ├── 2026-02-22/         Edition 3 — February 22, 2026
│   ├── 2026-03-01/         Edition 4 — March 1, 2026
│   ├── 2026-03-08/         Edition 5 — March 8, 2026
│   ├── 2026-03-15/         Edition 6 — March 15, 2026
│   ├── 2026-03-22/         Edition 7 — March 22, 2026
│   │   ├── jessie-mueller/
│   │   ├── chicago-chamber-music-society/
│   │   ├── unsung-gems-lfhs/
│   │   ├── two-sisters-and-a-piano/
│   │   ├── pokemon-fossil-museum/
│   │   ├── kanuga/
│   │   └── building-blocks/
│   └── 2026-03-29/         Edition 8 — March 29, 2026 (current, in progress)
│       ├── unsung-gems-backgammon/
│       ├── an-island-idyll/
│       ├── marwen/
│       ├── landmarks-preservation-forward/
│       ├── american-writers-museum/
│       └── biba-palm-springs/          (photos only; article pending)
```

## Current Homepage Article Order (March 29 edition — staged, publishing 10pm March 28)

This order is used for keyboard navigation (N/P keys cycle through):

1. **The Dice Keep Rolling at Trudie's Winnetka Backgammon Club** — David A. F. Sweet (hero)
2. **An Island Idyll** — Susan Aurinko
3. **Marwen: Fostering Creativity for the Next Generation** — Jen Huang
4. **Landmarks Illinois Delivers at The Old Post Office** — Judy Carmack Bross
5. **Tiffany at the Driehaus Museum: Chicago Can't Get Enough** — Judy Carmack Bross
6. **A Literary Adventure at the American Writers Museum** — Sydney Armstrong
7. **The Shape of Spring** — Marcy Carmack
8. **Biba's Favorite Things: Palm Springs** — Biba Roesch

Past editions in footer: March 22, March 15, March 8, March 1.

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

### Updating the homepage for a new edition
Edit `index.html` (root):
1. **Date line** — change `March 22, 2026` → next edition date
2. **Hero section** — update path, image, label, title, byline, and teaser for first article
3. **Card grid** — replace all cards with the new edition's articles (title, byline, image, teaser)
4. **Past Editions** — move the previous current edition to the top of Past Editions; drop the oldest one if the grid gets too long (keep ~4 past editions)
5. Image paths from root: `editions/YYYY-MM-DD/<slug>/<image-file>`

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
- Real comments (non-empty, non-dev2) go in `reader-comments.html`
- If a comment raises an editorial concern (criticism of a feature, content question), also add it to `comments.html` under a "Reader Comments" section

**Common bio locations in `about.html`:**
- Judy and Megan: Our Team section
- Writers and curators: Our Writers This Week section
- Annie Delfosse: `id="annie-delfosse"` (linked from DateBook page)

### Editors menu (Internal nav — dev2 only)
The `.internal-nav` bar sits below the main nav in the `<header>`. On dev2 it is **uncommented and visible**; it must be commented out before promoting to `dev` or `master` (handled automatically by `/stage`).

To update it for a new edition, edit the `<!-- dev2-only -->` block in `index.html`:
- Keep standing links: `reader-comments.html`, `future-articles.html`, `march-events-planning.html`
- Add/remove edition-specific links (e.g. editorial critique, datebook drafts) as needed
- Remove any stale edition-specific links from the prior edition

The comment marker convention:
- **Active (dev2):** `<!-- dev2-only -->` followed immediately by the `<div class="internal-nav">` block (no closing `-->`)
- **Hidden (dev/master):** wrap entire block in `<!-- dev2-only ... -->`

### Email style (Judy and notifications)
- **To Judy:** Salutation `Dear Judy,` / Sign-off `Cheers, John` / first person (I/me, not we/us)
- **Publication notification:** To `judycbross@aol.com`, CC `john.bartlett@gmail.com`
