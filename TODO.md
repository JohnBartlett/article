# TODO — Classic Chicago Magazine

## URGENT — Fix Vercel Production Branch (dev is deploying to production)

### What happened
On Feb 14, we discovered that every push to `dev` was going live on production
(`chicagoclassicmag.com`) immediately. The Vercel project's **Production Branch**
is almost certainly set to `dev` instead of `master`. This means there was NO
separation between development and production — all in-progress work was visible
to the public as soon as it was pushed.

### What was affected
- All dev work from Feb 9 onward deployed live automatically (Feb 15 edition,
  test pages that were later deleted, form experiments, etc.)
- The site currently looks correct because we cleaned everything up before
  discovering this, but it could have exposed unfinished/broken work.

### What to do (Vercel Dashboard — manual step required)
1. Go to **vercel.com** → select the **article** project
2. Go to **Settings** → **Git** → **Production Branch**
3. Check what branch is listed. It is likely `dev`.
4. **Change it to `master`**
5. This will make `master` the branch that deploys to `chicagoclassicmag.com`
6. `dev` will still get preview deployments at the dev URL

### After fixing the production branch
- Push dev → master once to sync them: `git checkout master && git merge dev && git push origin master`
- Then future dev pushes will only update the preview URL, not production
- The scheduled-deploy.yml workflow can handle automated dev→master merges on a schedule if desired

### Timeline of what deployed to production
- **Feb 8** — Last intentional push to master (Google Analytics commit)
- **Feb 9 onward** — All dev pushes auto-deployed to production via Vercel
- **Feb 14 9:10pm** — Most recent push (CLAUDE.md/TODO.md updates)

## High Priority

- [ ] **FIX: Change Vercel Production Branch from `dev` to `master`** (see above)
- [ ] Disable Vercel Deployment Protection so preview/production URLs are publicly accessible (Vercel Dashboard → Settings → Deployment Protection → turn off)
- [ ] Confirm Formsubmit activation emails for `subscribe@2ccmag.com` and `advertise@2ccmag.com` (check inbox, click confirmation link)
- [ ] Re-enable Subscribe form on `subscribe.html` after Formsubmit activation confirmed
- [ ] Re-enable Advertise form on `advertise.html` after Formsubmit activation confirmed

## Post-Deploy Cleanup

- [ ] Remove `.github/workflows/scheduled-deploy.yml` after production branch is fixed (no longer needed if using Vercel's branch-based deploys)
- [ ] Sync master with dev: `git checkout master && git merge dev && git push origin master`

## Content / Editorial (Recurring)

- [ ] Update `about.html` "Our Writers This Week" section with each new edition
- [ ] Add new articles and editions as they come in
- [ ] Update homepage `index.html` hero + card grid for each new edition
- [ ] Update keyboard navigation order in all articles to match new homepage order

## Completed

- [x] Scheduled deploy to production: Saturday Feb 14 at 11:30pm CST (GitHub Actions workflow)
- [x] Remove experimental homepage variants (`index-b.html`, `index-b1.html`, `index-c.html`)
- [x] Remove edition test page (`editions/2026-02-15/index.html`)
- [x] Fix all broken links across Feb 08 and Feb 15 editions (30+ fixes)
- [x] Clean orphaned files (~6.5MB, 20 files removed)
- [x] Create `/ads/` folder and consolidate ad assets
- [x] Add Heritage Auctions ad to homepage and edition page
- [x] Reorder keyboard navigation to match homepage article order
- [x] Add PgUp/PgDn to keyboard shortcuts help popup
- [x] Fix "Back to Sunday Edition" links across all articles
- [x] Fix Silk Roads image splicing (zebra-gaze.jpg / poesie-affiches.jpg)
- [x] Disable forms with "coming soon" placeholder (no emails exposed)
- [x] Remove email addresses from subscribe and advertise pages
