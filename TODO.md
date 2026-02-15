# TODO — Classic Chicago Magazine

## High Priority

- [ ] Disable Vercel Deployment Protection so preview/production URLs are publicly accessible (Vercel Dashboard → Settings → Deployment Protection → turn off)
- [ ] Confirm Formsubmit activation emails for `subscribe@2ccmag.com` and `advertise@2ccmag.com` (check inbox, click confirmation link)
- [ ] Re-enable Subscribe form on `subscribe.html` after Formsubmit activation confirmed
- [ ] Re-enable Advertise form on `advertise.html` after Formsubmit activation confirmed

## Post-Deploy Cleanup

- [ ] Remove `.github/workflows/scheduled-deploy.yml` after production deploy completes (was set for Feb 14 11:30pm CST)
- [ ] Verify production site is live and all pages/images load correctly

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
