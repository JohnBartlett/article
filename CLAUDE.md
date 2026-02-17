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
│   ├── 2026-02-15/           Edition 2 — February 15, 2026
│   │   ├── thumb-*.jpg       Thumbnails for homepage/edition page
│   │   ├── winter-in-antibes/
│   │   ├── best-restaurants-halsted-street/
│   │   ├── my-silk-roads/
│   │   ├── boba-tea-chinatown/
│   │   ├── alicia-ziegler/
│   │   └── childrens-research-fund/
│   └── 2026-02-22/           Edition 3 — February 22, 2026 (placeholders)
│       ├── article-1/        Placeholder — awaiting content
│       ├── article-2/        Placeholder — awaiting content
│       ├── article-3/        Placeholder — awaiting content
│       ├── article-4/        Placeholder — awaiting content
│       ├── article-5/        Placeholder — awaiting content
│       └── article-6/        Placeholder — awaiting content
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
4. Update `index.html` homepage with new hero + card grid
5. Update `about.html` "Our Writers This Week" section
6. Update keyboard nav links across all new articles (order must match homepage)
7. Add `../../../` paths for root assets, `../<slug>/` for sibling links
