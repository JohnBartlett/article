# Project: Classic Chicago Magazine

A weekly digital magazine about Chicago culture, dining, arts, and society. Static HTML site — no build step, no framework.

## Publication Info

- **Name:** Classic Chicago Magazine
- **Tagline:** "The Sunday Edition"
- **Publishes:** Every Sunday
- **Contact:** editor@classicchicagomagazine.com
- **Google Analytics:** G-5J2HWKC0B1

## Team

- **Judy Carmack Bross** — Editor-in-Chief & Founder
- **Megan McKinney** — Publisher & Founder

### Writers (update "Our Writers This Week" on about.html each edition)
- Bob Glaze — Culinary & Cultural Guide
- Katherine Harvey — Travel Writer
- Susan Aurinko — Arts & Photography
- Jen Huang — Magazine Intern (UIC student)

## Branching Strategy

Three-branch workflow:

- **`master`** — Production (live site, Cloudflare). NEVER commit directly.
- **`dev`** — Staging / review (Vercel preview). Merges to `master` when ready.
- **`dev2`** — Spitballing / experimentation. All exploratory work starts here.

Workflow: `dev2` → `dev` → `master`

## Hosting

### Production: Cloudflare
- **URL:** `chicagoclassicmag.com`
- **Deploys from:** `master` branch

### Dev Preview: Vercel
- **Dev URL:** `https://article-git-dev-johns-projects-e5fce345.vercel.app`
- **Deploys from:** `dev` branch (this is intentional — Vercel is the dev preview site, not production)
- **Vercel Project ID:** `prj_hzNhpgPW5e0hcF8GtyzmkkJZnMzY`
- **Vercel Team ID:** `team_8vNXZ20pDprMAIxBJgnZdEeM`

### GitHub repo
- **Repo:** `JohnBartlett/article`

## Git Push

Pushes require a personal access token:
```
git push origin dev
```

## Site Structure

```
/
├── index.html              Homepage — "The Sunday Edition" hero + card grid
├── about.html              About — team bios + "Our Writers This Week"
├── subscribe.html          Subscribe — form disabled, "coming soon" placeholder
├── advertise.html          Advertise — form disabled, "coming soon" placeholder
├── logo.jpg                Shared masthead logo
├── favicon.ico             Favicon
├── ads/                    All advertisement assets (NOT in edition folders)
│   ├── ha-ad.html          Heritage Auctions ad click-through page
│   ├── ha-ad.jpg           Heritage Auctions ad image
│   └── image006.png        Heritage Auctions banner image
├── .github/workflows/
│   └── scheduled-deploy.yml  Cron: merge dev→master (remove after deploy)
├── editions/
│   ├── 2026-02-08/           Edition 1 — February 8, 2026
│   │   ├── index.html        Edition landing page
│   │   ├── about-the-town-february/
│   │   ├── iron-lung/
│   │   ├── lincoln-park/
│   │   ├── linda-heister/
│   │   ├── mimosa/
│   │   └── sam-hiller/
│   └── 2026-02-15/           Edition 2 — February 15, 2026
│       ├── thumb-*.jpg       Thumbnails for homepage/edition page
│       ├── winter-in-antibes/
│       ├── best-restaurants-halsted-street/
│       ├── my-silk-roads/
│       ├── boba-tea-chinatown/
│       ├── alicia-ziegler/
│       └── childrens-research-fund/
```

## Current Homepage Article Order (Feb 15 edition)

This order is used for keyboard navigation (N/P keys cycle through):

1. **Winter in Antibes and Environs** — Katherine Harvey (hero)
2. **Best Restaurants on Halsted Street** — Bob Glaze
3. **My Silk Roads** — Susan Aurinko
4. **Boba Tea in Chinatown** — Jen Huang
5. **Alicia Ziegler** — profile
6. **Children's Research Fund Children's Ball** — Judy Carmack Bross

Heritage Auctions ad card appears in the grid next to the Children's Ball card.

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
- Google Analytics on all pages

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

### Updating the homepage for a new edition
Edit `index.html` (root):
1. **Date line** — change `March 8, 2026` → `March 15, 2026` (etc.)
2. **Hero section** — update path, image, label, title, byline, and teaser for first article
3. **Card grid** — replace all cards with the new edition's articles (title, byline, image, teaser)
4. **Past Editions** — move the previous current edition to the top of Past Editions; drop the oldest one if the grid gets too long (keep ~4 past editions)
5. Image paths from root: `editions/YYYY-MM-DD/<slug>/<image-file>`

### Recurring email workflow

Run `/check-emails` to execute this workflow. Do it at the start of a session or when Judy may have sent instructions.

**Sources:**
- Judy Carmack Bross (`judycbross@aol.com`) — editorial instructions, bio updates, photo requests, text corrections
- FormSubmit (`submissions@formsubmit.co` → `editor@2ccmag.com`) — reader comments and Quick Votes

**What to expect from FormSubmit:**
- "Classic Chicago Reader Comment" — check the `comment` field; empty submissions are common (reader opened form, didn't type)
- "Classic Chicago Quick Vote" — vote=Yes means reader liked the article; `Environment: dev2` = test, ignore
- Real comments (non-empty, non-dev2) go in `reader-comments.html`

**Common bio locations in `about.html`:**
- Judy and Megan: Our Team section
- Writers and curators: Our Writers This Week section
- Annie Delfosse: `id="annie-delfosse"` (linked from DateBook page)

### Editors menu (Internal nav — dev2 only)
The `.internal-nav` bar sits below the main nav in the `<header>`. On dev2 it is **uncommented and visible**; it must be commented out before promoting to `dev` or `master`.

To update it for a new edition, edit the `<!-- dev2-only -->` block in `index.html`:
- Keep standing links: `reader-comments.html`, `future-articles.html`, `march-events-planning.html`, `comments.html`
- Add/remove edition-specific links (e.g. editorial critique, datebook drafts) as needed
- Remove any stale edition-specific links from the prior edition

The comment marker convention:
- **Active (dev2):** `<!-- dev2-only -->` followed immediately by the `<div class="internal-nav">` block (no closing `-->`)
- **Hidden (dev/master):** wrap entire block in `<!-- dev2-only ... -->`
