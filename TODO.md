# Classic Chicago Magazine — TODO

## TODO — JUNE 28 EDITION

### In progress
- [ ] David Sweet — Daniel Murphy Scholarship Fund article (threads 19ed7c6e67b00757 + 19ed7cd60c666dd8)
- [ ] Judy's Editor's Page — "What Are We Doing for the Fourth of July" (thread 19ee4d2b064b21b0)
- [ ] Soma Roy article — Ana is laying it out; add to editions/2026-06-28/ when ready

### Next up
- [ ] Create editions/2026-06-28/ folder skeleton (articles, datebook, daily-star, editors page)
- [ ] Copy daily-star from June 21 edition into June 28
- [ ] Update homepage + nav for June 28 edition

### Blocked / waiting
- [ ] NMH Summer Soiree article — waiting on: photos from NMH (Judy awaiting their reply)

---

## TODO — EDITORS TOOLS

### Next up
- [ ] Re-apply tools/ga4_report.py changes to dev2 — 4 metrics (engagement time), top 25, avgEngagementFormatted; lost in stash conflict last session
- [ ] Add June 14 votes & comments to reader-comments.html on editors branch — 14 Yes, 0 No; 2 Reunion comments

---

## TODO — ELIZABETH RICHTER SITE

### Next up
- [ ] Email Judy with URL (elizabeth-dunlop-richter-ccm.vercel.app) to share with Elizabeth
- [ ] Spot-check a sample of articles for image quality and body text accuracy

---

## TODO — SITE / ONGOING

### Next up
- [ ] Disable Vercel Deployment Protection — dev preview URLs not publicly accessible (Vercel Dashboard → Settings → Deployment Protection)
- [ ] Susan Aurinko silk-roads article: verify brand spelling "LensFlair Editions" vs "lensflaireditions.com" with Susan or Judy

---

## Done (this session)
- [x] Glessner House — replaced garbled last paragraph with Bill Tyre's two corrected paragraphs; deployed to prod
- [x] Marcy Carmack + 4 others — fixed article popups broken by collapsed `<details>` element; removed duplicate popup IDs
- [x] verify_edition.py — added check_about_popups() to catch popups trapped in collapsed `<details>`
- [x] article-mini placeholder cards — fixed width/height to match img sizing (all 6 instances sitewide)
- [x] Caption fix — "Flore" → "Cafe de Flore" in Marcy's June 21 fashion-trends article; deployed to prod
- [x] Stats page (editors branch) — 23-article table with avg engagement time + engagement rate; color-coded
- [x] Elizabeth Dunlop Richter archive — 103 articles (98 old CCM + 5 current) built and deployed to elizabeth-dunlop-richter-ccm.vercel.app
