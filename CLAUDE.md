# Project: Article Website

## Branching Strategy

This project uses a three-branch workflow:

- **`master`** — Production. This branch is live and serves the website. Do NOT make changes directly to `master`.
- **`staging`** — Review-ready code for team review before going to production. Merge `dev` into `staging` when changes are ready for team feedback.
- **`dev`** — Active development. All work happens here first.

### Workflow

1. Work on `dev`
2. When ready for team review, merge `dev` → `staging`
3. When approved, merge `staging` → `master` (production)

### Important

- Never commit directly to `master` — it is the live production site.
- Always start work from the `dev` branch.
- Use `staging` as the team review step before production.

## Hosting: Vercel

This site is hosted on Vercel. Deploys automatically on push.

- **Dev URL:** `https://article-git-dev-johns-projects-e5fce345.vercel.app`
- **Production:** deploys from `master` branch

## Editions Structure

Content is organized into weekly editions under `editions/YYYY-MM-DD/`.

```
/
├── index.html              (homepage — Sunday Edition with hero + card grid)
├── about.html              (About page — team + writers this week)
├── subscribe.html          (Subscribe page)
├── advertise.html          (Advertise page)
├── logo.jpg, favicon.ico   (shared assets in root)
├── ads/                    (all advertisement assets)
│   ├── ha-ad.html          (Heritage Auctions ad page)
│   ├── ha-ad.jpg           (Heritage Auctions ad image)
│   └── image006.png        (Heritage Auctions banner image)
├── editions/
│   ├── 2026-02-08/         (first edition)
│   │   ├── index.html      (edition landing page)
│   │   └── <article-name>/ (article folder)
│   │       ├── index.html  (article page)
│   │       └── *.jpg/jpeg/png (article images)
│   └── 2026-02-15/         (second edition)
│       ├── index.html      (edition landing page)
│       ├── thumb-*.jpg     (article thumbnails for edition/homepage)
│       └── <article-name>/ (article folder)
```

### Conventions

- Each edition folder is named by publication date: `YYYY-MM-DD`
- Each article lives in its own subfolder: `editions/YYYY-MM-DD/<article-name>/index.html`
- Article images live in the same folder as their `index.html`
- Shared assets (`logo.jpg`, `favicon.ico`) stay in root
- Articles reference shared assets via `../../../` (three levels up from article folder)
- Articles reference sibling articles via `../<sibling-name>/`
- Thumbnails (`thumb-*.jpg`) live in the edition root for use by edition and homepage
- **All ad assets go in `/ads/`** — do not store ads in edition folders
- When adding a new edition: create the folder, add article subfolders + images, create thumbnails, then update the homepage
