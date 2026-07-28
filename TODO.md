# Classic Chicago Magazine — TODO

## TODO — AUGUST 2 EDITION (next)

### Incoming lineup (Judy's email Jul 26, 2026)
- [x] **David Sweet book interview** — Built: `editions/2026-08-02/hindenburg-disaster/` (TEXT ONLY — photos pending extraction)
- [ ] **Dinner Party on the Bluff** — Emma. Slug TBD. (Lurie Garden dinner; cover photo `group photo (1).jpeg` in msg `19fa89fde1c12b57` — no article text yet)
- [ ] **Philip Vidal: About the Town in August** — Ana Baca. Slug TBD.
- [ ] **Katherine Harvey on Antibes** — Annie Delfosse. Cover photo received: `IMG_1882.jpeg` (msg `19f9e74c0584af79`) — extract when building stub. Slug TBD.
- [ ] **Sydney on Garfield Park** — Annie Delfosse. Cover photo `20260710_132414.jpeg` in Judy email Jul 26 (msg `19f9add5cefd7f06`). Slug: `sydney-garfield-park`. No article text yet.
- [ ] **Adrian's Adventures** — Emma (Adrian delivering by Thursday; Judy will substitute if he can't). Slug TBD.
- [x] **Scott Holleran's short story** — Built: `editions/2026-08-02/beauty-and-the-beast/` (TEXT ONLY — cover photo `image0.jpeg` pending extraction from msg `19fa83463f9e4654`)
- [ ] **DateBook** — Annie updating.
- [ ] Possible additional article TBD.

### Photos pending (require Gmail credentials / new session)
- [ ] Extract `image0.jpeg` → `editions/2026-08-02/beauty-and-the-beast/` (msg `19fa83463f9e4654`)
- [ ] Extract `Catherine Grace Katz 1 (Photo by Steve Dondero).jpeg`, `Catherine Grace Katz 2.jpeg`, `Catherine Grace Katz 3 Zeppelin Museum in Freidrichshafen.jpeg` → `editions/2026-08-02/hindenburg-disaster/` (msg with David Sweet article)
- [ ] Extract `group photo (1).jpeg` → Lurie Dinner article folder (msg `19fa89fde1c12b57`)
- [ ] Extract `20260710_132414.jpeg` → Sydney Garfield Park article folder (msg `19f9add5cefd7f06`)
- [ ] Download `Classic Chicago August 2026.png` → `ads/` (Heritage Auctions ad, link: `ha.com/43249`)
- [ ] Update `index.html`: HA ad image `Classic Chicago June 2026.png` → `Classic Chicago August 2026.png`; link → `ha.com/43249`
- [ ] Create navthumb.jpg for hindenburg-disaster and beauty-and-the-beast (after photos extracted)

### Setup tasks (do when Judy confirms lineup is final)
- [x] Copy DateBook forward: `cp -r editions/2026-07-26/datebook editions/2026-08-02/datebook` ✅
- [x] Copy Astrochart forward: `cp -r editions/2026-07-26/daily-star-july editions/2026-08-02/daily-star-july` ✅ (July forecast; swap for August when Victoria sends text)
- [ ] Run `/prep-edition 2026-08-02` for remaining stubs when full lineup confirmed
- [ ] Update "Our Writers This Week" in about.html for Aug 2 writers
- [ ] Wire final nav chain once all articles built
- [ ] Update index.html homepage with Aug 2 hero + cards

## DONE — JULY 26 EDITION (published Jul 26, 2026)

### Carryover to answer Judy
- [x] **LIVE FIX — Guild caption**: ✅ Fixed Jul 20. Duplicate `photo 5.jpg` (mislabeled "Michael Anderson and Connie Barkley") removed; `IMG_4184.jpeg` caption confirmed "Lisa Malkin and Virginia Cudecki"; "Andersen"→"Anderson" in quote. Published to master; Judy confirmed (msg `19f816ab692ea243`).
- [x] Reply to Judy's Jul 20 8:58 text (Obama Library + editor's-page mention) — covered in Jul 26 publish thread
- [x] Scott Holleran comments question — policy explained; no action needed

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
