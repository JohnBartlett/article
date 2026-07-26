# Classic Chicago Magazine — TODO

## TODO — JULY 26 EDITION (next)

### Articles / editor's page
- [ ] **Obama Presidential Center article** — two related pieces approved for July 26:
  - [ ] Sigalit — art in the Sky Room (8th floor), Obama Presidential Center. **Blast text + 1 photo arriving today (Jul 21 PM); full article + photos + credits arriving tomorrow morning (Jul 22 AM).** Create `editions/2026-07-26/sigalit-sky-room/` (or similar slug) when content arrives. (msgs `19f6bb631c2c4945`, `19f849b59501292d`)
  - [ ] John — write the Obama Library/Center piece Judy asked for and mention it in the **July 26 editor's page** (editorial.html); deferred from Jul 19
- [x] Get Judy's July 26 lineup email (source of truth) — **received Jul 20** (msg `19f7f085498aee25`). Confirmed order: 1. Boys & Girls Club (Judy/Emma) · 2. Susan Aurinko Vienna (Emma) · 3. Heritage Lincoln Office (Judy/Ana) · 4. Vienna by Susan Aurinko (Emma — likely dup of #2, asked Judy) · 5. Adrian's Adventures (Annie) · 6. Sydney Garfield Park (Annie) · 7. Russell Kelley Part III (John). Sigalit's Sky Room not yet in lineup (Judy approved separately).

### Carryover to answer Judy
- [x] **LIVE FIX — Guild caption**: ✅ Fixed Jul 20. Duplicate `photo 5.jpg` (mislabeled "Michael Anderson and Connie Barkley") removed; `IMG_4184.jpeg` caption confirmed "Lisa Malkin and Virginia Cudecki"; "Andersen"→"Anderson" in quote. Published to master; Judy confirmed (msg `19f816ab692ea243`).
- [ ] Reply to Judy's Jul 20 8:58 text (Obama Library + editor's-page mention)
- [ ] Scott Holleran comments question — John explained policy; Judy relaying to Scott. Decide whether to print the reader comment on Scott's TWA article

### Recurring setup for the edition
- [ ] Copy DateBook forward (`cp -r editions/2026-07-19/datebook editions/2026-07-26/datebook`); Annie's updated events; strip stale months
- [ ] Copy Astrochart forward; daily-star-july covers through Jul 31 (Jul 26 OK). Chase Victoria for **August** forecast
- [ ] Update "Our Writers This Week" in about.html for Jul 26 writers

## TODO — JUNE 28 EDITION

### Article order (per Judy)
1. Philip Vidal
2. Daniel Murphy
3. Sigalit (Edgar Calel)
4. CHM / Lincoln Park statue
5. Versailles (Kristin Smith)
6. Susan Aurinko
7. Soma Roy
8. Linda Miller

### Article status

- Philip Vidal — content OK, photos OK — Built
- Daniel Murphy (DMSF) — content OK, photos OK — Built; needs real URL from David Sweet
- Sigalit (Edgar Calel) — content OK, photos OK — Built
- CHM / Lincoln Park — content OK, photos OK — Built
- Versailles — content OK, photos OK — Built (32 photos)
- Susan Aurinko — content OK, photos OK — Built
- Soma Roy — content OK, photos OK — Built; nav temporarily unlinked for writer preview
- Linda Miller — content OK, photos PARTIAL — Text built; not all photos extracted

### Still to do [Jun 28]
- [ ] Restore Soma Roy nav links once she confirms preview [Jun 28]
- [ ] Linda Miller — confirm all photos are in place; extract missing ones if needed [Jun 28]
- [ ] July astrochart — replace daily-star-june with July content; Victoria's full text needed (Word doc unreadable) [Jun 28]
- [ ] DMSF article: replace "contact the author" with real URL once received from David Sweet or Judy [Jun 28]
- [ ] `about.html` "Our Writers This Week" — update for June 28 writers [Jun 28]
- [ ] Run verify_edition.py and fix any issues before staging [Jun 28]
- [ ] Deploy to Vercel + update editors pages [Jun 28]

---

## TODO — PENDING REPLIES / ACTIONS

- [ ] Reply to Judy with Soma Roy direct preview URL to forward to Soma [Jun 28]
- [ ] Chase Victoria for July astrochart full text (ask her to paste into email) [Jun 28]
- [ ] DMSF article: replace "contact the author" with real URL once received from David Sweet or Judy [Jun 28]
- [ ] Reply to Marcy re: ad placement and Instagram question [General]

---

## TODO — EDITORS TOOLS

- [ ] Re-apply tools/ga4_report.py changes to dev2 (engagement time, top 25, avgEngagementFormatted; lost in stash conflict) [General]
- [ ] Add June 14 votes & comments to reader-comments.html on editors branch — 14 Yes, 0 No; 2 Reunion comments [General]

---

## TODO — SITE / ONGOING

- [ ] GitHub token expired — update token to re-enable git push to remote [General]
- [ ] Susan Aurinko silk-roads article: verify brand spelling "LensFlair Editions" vs "lensflaireditions.com" [General]

---

## Done — June 28 Edition
- [x] Philip Vidal article built with 7 photos
- [x] Daniel Murphy (DMSF) article built
- [x] Sigalit (Edgar Calel) article built with 8 photos
- [x] CHM / Lincoln Park article built
- [x] Versailles article built with 32 photos (Kristin Smith)
- [x] Susan Aurinko "Dispatch from Paris" built with 7 photos
- [x] Soma Roy article built; nav unlinked for writer preview
- [x] Linda Miller article built (partial photos)
- [x] Nav chain wired across all 8 articles
- [x] Homepage updated with all June 28 cards
- [x] Reader Comments and Future Articles removed from internal nav (all articles + template)
- [x] Stray rush-hospital and trains-chicago folders deleted
- [x] Soma Roy nav unlinked and deployed for writer preview

## Done — General
- [x] Elizabeth Dunlop Richter archive — 103 articles built, deployed, emailed Judy
- [x] Writer preview policy: never share dev2 homepage; send direct unlinked article URL only
- [x] No-emoji rule added to CLAUDE.md and memory
