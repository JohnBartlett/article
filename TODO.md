# Classic Chicago Magazine — TODO

## TODO — JULY 26 EDITION (next)

### Articles / editor's page
- [ ] **Obama Presidential Center article** — being worked shortly. Two related pieces:
  - [ ] Sigalit — art in the Sky Room (8th floor), Obama Presidential Center; article + photos + credits promised by Tue Jul 21 (msg `19f6bb631c2c4945`, 3 preview photos attached)
  - [ ] John — write the Obama Library/Center piece Judy asked for (her Jul 20 text) and mention it in the **July 26 editor's page** (editorial.html); this is the piece deferred from Jul 19 when "On Mentoring" ran instead
- [ ] Get Judy's July 26 lineup email (source of truth) and reconcile against future-articles.html + this list

### Carryover to answer Judy
- [ ] **LIVE FIX — Guild caption**: photo of blonde woman + woman with purple hair reads "Michael Anderson"; should be **Lisa Malkin and Virginia Cudecki** (Judy, Jul 20 AM; Darcy Evon email). Fix on live site, then confirm back to Judy
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
