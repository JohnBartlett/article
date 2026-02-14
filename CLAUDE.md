# Project: Article Website

## Branching Strategy

This project uses a three-branch workflow:

- **`master`** — Production. This branch is live and serves the website. Do NOT make changes directly to `master`.
- **`staging`** — Review-ready code for team review before going to production. Merge `dev` into `staging` when changes are ready for team feedback.
- **`dev`** — Active development. All work happens here first.
- **`dev2`** — Experimental/spitballing branch. Used for trying out ideas before committing to `dev`.

### Workflow

1. Work on `dev`
2. When ready for team review, merge `dev` → `staging`
3. When approved, merge `staging` → `master` (production)

### Important

- Never commit directly to `master` — it is the live production site.
- Always start work from the `dev` branch.
- Use `staging` as the team review step before production.

## Hosting: Vercel

The `dev` branch deploys to Vercel for development previews. Production (`master`) is deployed separately.

- **Dev URL:** https://article-git-dev-johns-projects-e5fce345.vercel.app

### Guidelines

- Optimize images before adding them.
- Be mindful of file count if bulk-adding assets.

## Editions Structure

Content is organized into weekly editions under `editions/YYYY-MM-DD/`.

```
/
├── index.html              (demo chooser — links to Option B and C)
├── index-b.html            (Option B homepage: latest edition as homepage)
├── index-c.html            (Option C homepage: latest + previous editions)
├── logo.jpg, favicon.ico   (shared assets in root)
├── editions/
│   ├── 2026-02-08/         (first edition)
│   │   ├── index.html      (edition landing page)
│   │   ├── *.html          (article files)
│   │   └── *.jpg/jpeg/png  (article images)
│   └── 2026-02-15/         (next edition placeholder)
│       └── .gitkeep
```

### Conventions

- Each edition folder is named by publication date: `YYYY-MM-DD`
- Article HTML and their images live together in the same edition folder
- Shared assets (`logo.jpg`, `favicon.ico`) stay in root
- Articles reference shared assets via `../../` (two levels up)
- Articles reference images and sibling articles with bare filenames (same directory)
- When adding a new edition: create the folder, add articles + images, then update the homepage files to link to it
