# Branch Strategy

This repository uses three branches. See CLAUDE.md "Branching Strategy" for the authoritative reference.

## `master` — Production
Live site, deployed to Cloudflare (`chicagoclassicmag.com`). **Never commit directly.** GA4 enabled. Only receives merges from `dev` via `/publish`.

## `dev` — Staging
Vercel preview (`article-git-dev-johns-projects-e5fce345.vercel.app`). Receives merges from `dev2` via `/stage`. GA4 disabled.

## `dev2` — Active Work
All work starts here. Every article, photo, fix, and skill change is made on `dev2`. GA4 disabled.

**What stays on dev2 only:** Skills (`.claude/commands/`), `CLAUDE.md`, `tools/`, `_template/`, memory files. These must never be promoted to `dev` or `master`.

## Workflow

```
dev2 (all work) --> dev (staging/Vercel) --> master (production/Cloudflare)
```

Use `/stage` to promote dev2 → dev, and `/publish` to promote dev → master.
