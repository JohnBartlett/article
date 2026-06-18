# TODO — Classic Chicago Magazine

## June 21 Edition — In Progress

1. [x] Lay out Jean Colonomos poems article — built June 16
2. [ ] Add Jean Colonomos bio to `about.html` (awaiting Judy's reply; poet, playwright, former Martha Graham dancer)
3. [x] Lay out Francesco Bianchini / Ciorba de Perisoare — text + 4 photos complete June 16
4. [ ] Lay out Glessner House Gala — cover photo downloaded (`2 - Tom and Barbi Donnelley with Bill Tyre.jpeg`); article text pending from Annie
5. [ ] Lay out Rush Hospital Luncheon — cover photo downloaded (`Ela Lewis, Gale Gottlieb, Mary Pearlman.jpeg`); article text pending from Emma
6. [ ] Lay out Today in Chicago History — cover photo downloaded (`IMG_4034.JPG`); article text pending from Ana / Scott Holleran
7. [ ] Lay out Bob Glaze column (pending from Emma)
8. [ ] Lay out Marcy Carmack Fashion Trends article (Judy chasing her for photo + Blast sentence)
9. [ ] Update DateBook for June 21 (new events from Annie — pending)
10. [x] Add Philip Vidal to `about.html` — Events Editor card added to More Contributors using Judy's bio text
11. [x] Add Jean Colonomos intro to `editorial.html` — posted June 21 (Judy-approved)
12. [ ] Run `/edition-checks` before staging
13. [ ] Stage and publish June 21 edition

## People / Editorial

1. [x] Add Philip Vidal to `about.html` as contributor (About the Town column) — done
2. [x] Send Philip Vidal intro/title email to Judy — sent + corrected June 18 (role: About the Town)
3. [ ] Await Sig Zetouni reply re: articles for coming weeks (email sent June 16)
4. [x] Compile Elizabeth Richter article list for Judy — sent June 18

## High Priority (Site)

1. [ ] Disable Vercel Deployment Protection so dev preview URLs are publicly accessible (Vercel Dashboard → Settings → Deployment Protection → turn off)
2. [x] Confirm Formsubmit activation for `editor@2ccmag.com` — activation link opened June 18
3. [x] Re-enable Subscribe form on `subscribe.html` — done June 18
4. [x] Re-enable Advertise form on `advertise.html` — done June 18
5. [x] Swap Heritage Auctions ad to June image (`Classic Chicago June 2026.png`) — already done on homepage
6. [ ] Susan Aurinko silk-roads article (`editions/2026-04-26/silk-roads/`): confirm correct brand spelling — article uses "LensFlair Editions" (capital F); domain is `lensflaireditions.com` (lowercase). Verify with Susan or Judy before changing.

## Content / Editorial (Recurring)

These are handled by skills each edition — tracked here as a reminder:

1. [ ] Update `about.html` "Our Writers This Week" section with each new edition (handled by `/edition-checks`)
2. [ ] Update homepage `index.html` hero + card grid for each new edition (handled by `/new-edition`)
3. [ ] Update keyboard navigation order in all articles to match homepage order (handled by `/layout`)

## Completed

1. [x] Set up Gmail API for email/attachment extraction (`tools/gmail_api.py`, `~/.gmail-mcp/credentials.json`)
2. [x] Set up GA4 reporting (`tools/ga4_report.py`, `tools/credentials.json`, property ID `523654462`)
3. [x] Scheduled deploy to production: Saturday Feb 14 at 11:30pm CST (GitHub Actions workflow)
4. [x] Remove experimental homepage variants (`index-b.html`, `index-b1.html`, `index-c.html`)
5. [x] Remove edition test page (`editions/2026-02-15/index.html`)
6. [x] Fix all broken links across Feb 08 and Feb 15 editions (30+ fixes)
7. [x] Clean orphaned files (~6.5MB, 20 files removed)
8. [x] Create `/ads/` folder and consolidate ad assets
9. [x] Add Heritage Auctions ad to homepage and edition page
10. [x] Reorder keyboard navigation to match homepage article order
11. [x] Add PgUp/PgDn to keyboard shortcuts help popup
12. [x] Fix "Back to Sunday Edition" links across all articles
13. [x] Fix Silk Roads image splicing (zebra-gaze.jpg / poesie-affiches.jpg)
14. [x] Disable forms with "coming soon" placeholder (no emails exposed)
15. [x] Remove email addresses from subscribe and advertise pages
