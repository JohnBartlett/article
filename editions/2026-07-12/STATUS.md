# July 12, 2026 Edition — Status

_Updated: 2026-07-07_

## Lineup (Judy, Jul 7, msg 19f3bdbfb7e3e937 — "Photos for The Odyssey")

Order updated from original Jul 6 schedule. Golden Triangle replaced by John Makowski Odyssey Q&A. Judy moved Odyssey to #3 (msg 19f3bdbfb7e3e937).

| # | Slug | Title | Author | Coordinator | HTML | Photos | Notes |
|---|------|-------|--------|-------------|------|--------|-------|
| 1 | making-history-awards | Making History Awards: Chicago's Version of the Oscars | Judy Carmack Bross | Ana | ✅ | ✅ 11 photos | Built Jul 11 from Ana's email (msg `19f4c932702ae452`) — full text with explicit `[PHOTO n - filename - caption]` markers, 158-award history, Ali Velshi/Buddy Guy/Linda Johnson Rice/Debra Cafaro/Fred Eychaner/John McCarter Jr coverage; cover re-sent as `COVER Buddy Guy.jpg` (same photo as old `Buddy Guy 22.jpg`, now with caption) — old file removed, all references updated; photo credit Kyle Flubacker Photography; Photo 5 (Buddy Guy/Ronnie Baker Brooks) was silently dropped during the initial build, caught by a user audit Jul 12 and restored; Photo 4 caption corrected Jul 12 to add Leo Melamed's name per Judy's request (msg `19f52babc7e89e9e`) — filename already identified him (`4 Michael Anderson Leo Melamed.jpg`) but the caption text only had Michael Anderson |
| 2 | biba-roesch | Biba's Favorite Things &ndash; Steven Zick | Biba Roesch | Emma | ✅ | ✅ 4 photos | Emma sent a Mia Cohen piece first then retracted it ("saved for a future week"), then sent the correct Steven Zick piece (msg `19f4f1ab6d329848`) matching the existing cover photo (Biba with Steve Zick); built Jul 11, full text + 3 inline photos (Christie's, Giotto & Toots). Judy flagged the Giotto/Toots photo (`photo 3.png`) as sideways (msg `19f52bc434b128c3`) — investigated Jul 12: the file carries an EXIF orientation=6 tag that some viewers (e.g. Mail.app) apply and others (Chrome, and this site's `<img>` rendering) ignore; verified in-browser that the live site already displays it upright correctly, so no file change was needed — do not "fix" this file by baking in the EXIF rotation, that makes it display sideways |
| 3 | odyssey | What You Need to Know Before Seeing "The Odyssey" | John Makowski (Q&A) | Annie | ✅ | ✅ 1 photo | Built Jul 7 from email body (msg 19f3bd677202980a) — 8 Q&A questions verbatim; photo `63cebaf7-a253-4d5a-a62f-a1c72794e7a3.jpeg` on disk, caption: "Melinda Sue Gordon/Universal Pictures/Everett Collection" (msg 19f3be100e8c529a); nav updated Jul 10: biba-roesch ← odyssey → rocky-mountaineer |
| 4 | rocky-mountaineer | Canada's Rocky Mountaineer: Spectacular Scenery and Superb Service | Judy Carmack Bross and George York | Ana | ✅ | ✅ 17 photos | Built Jul 10 from Ana's email (msg `19f4c4d35fa69657`) — full text + cover + 16 numbered photos, all explicitly placed inline via `[PHOTO n - filename - caption]` markers in the email body (cleanest placement instructions of the edition, no guessing needed); Judy replied approving (msg `19f4c543a9b03d1e`): "This looks extraordinary"; co-author George York has no about.html bio yet — byline left unlinked for him, flag to Judy if one should be added; homepage card + odyssey/kintsugi nav thumbs updated to real cover photo |
| 5 | kintsugi | Use the Good Dishes&hellip; But If They Break, Is Kintsugi an Option? | Jill Lowe | Emma | ✅ | ✅ 14 photos | Built Jul 10 from PDF (`64) Kintsugi.pdf`) — rendered all 11 PDF pages to images to extract Jill's own photo placement order (no placement instructions in email, so used the PDF's own layout per mistake #29); matched all 14 photo files to their exact page positions by visual comparison; real hero is `IMG_9045.jpeg` (gilded porcelain plate, page 1) — not `shutterstock_2308896621.jpeg` as earlier assumed, that one is actually mid-article (page 5) with a real caption "Beautiful seams of gold glint in the conspicuous cracks of ceramic wares."; real personal photos are `IMG_9045.jpeg` (plate) and `IMG_8883.jpeg` (restored mercury pendulum clock, "Presented to Michael B. Lowe"), rest are stock/graphic images from the PDF; category "Facts and Froth" (Jill's column name); homepage card + nav thumbs updated to correct hero |
| 6 | kiddieland | The History of Kiddieland | Adrian Naves | Annie | ✅ | ✅ 6 photos | Text actually arrived from Annie at 14:24 Jul 11 (msg `19f52a3c25973009`, 5 numbered photos + captions matching filenames) — but this was missed in an earlier email-check pass and the article was pulled from the edition and reported to Judy as missing. Judy replied (msg `19f52b57f83f2fd3`) pointing out the text had arrived and asking for it to be put back in; restored Jul 12 to its original lineup position (#6, between Kintsugi and Letter from Paris) with full text + 5 numbered photos (`1-Kids on Rollercoaster.jpeg` through `5-Train with passengers.png`) + existing cover (`IMG_1537.png`); category "Chicago History" (matches train-history precedent) |
| 7 | letter-from-paris | Letter from Paris: France's Record Heatwave (Part 1 of 3) | Russell Kelley | Judy → John | ✅ | ✅ 3 photos | Built Jul 10 from PDF (`Letter from Paris #39 040726.pdf`) — split into 3 parts, **one per edition across three consecutive weeks**, per John's Jul 7 proposal ("run across three consecutive issues") and Judy's agreement (msg `19f3df740c07880c`); rendered all 17 PDF pages to images to extract embedded photos (no separate attachments — images live inside the PDF) and confirm placement; Part 1 covers "Dear Friends" intro + "La Canicule" (heatwave) through "Cela change la donne"; 3 images (flyover, heatwave satellite map, Loire river map); **last article in the July 12 edition, links back to homepage** |
| — | letter-from-paris-2 | Letter from Paris: Retirement Politics and the Poetry of French (Part 2 of 3) | Russell Kelley | Judy → John | **not in this edition** | — 0 photos | Built Jul 10, ready — but incorrectly linked into the July 12 nav chain/homepage in that session; corrected Jul 12 (see below) since it's meant to run July 19, one edition per the "three consecutive issues" plan. Covers "La Reforme de la Retraite" (retirement age history) + Samuel Fitoussi's satirical Figaro column + "La poésie de la langue de Molière"; genuinely no images in the source PDF for this section — not an omission |
| — | letter-from-paris-3 | Letter from Paris: Paris's Great Museums and Summer Spectacles (Part 3 of 3) | Russell Kelley | Judy → John | **not in this edition** | ✅ 8 photos | Built Jul 10, ready — same nav-chain correction as Part 2; meant to run July 26. Covers "Les Grands Musées Parisiens" + "Les Expositions" (Matisse exhibition + Russell's 1970 term paper) + "Les Spectacles" + "Avant et Après" (Atget then/now photos) + "Le Bac Philo" + "La Baignade" |
| — | datebook | DateBook | Annie Delfosse | — | ✅ | — | Copied from July 5; updated title/kicker to July 12; new events pending from Annie |
| — | daily-star-july | Astrochart | Victoria Martin | — | ✅ | — | Copied from July 5; coverage extends through July 31 |

## Pending Deliveries

- **Judy** — Making History Awards article text (promised Jul 6); Rocky Mountaineer text + photos (to Ana by Wed Jul 8); more Odyssey photos (she's looking)
- **Biba Roesch / Emma** — Biba's Favorite People article text (Judy says Emma has it)
- **Adrian / Annie** — Kiddieland article text (Friday Jul 11)
- **Annie** — updated DateBook events for July 12
- **Eric Miller** — Making History Awards photo captions (Judy checking with Ana)
- **John** — decide how to divide the Russell Kelley Letter from Paris (2–3 parts)

## Deferred to July 19

- Golden Triangle sale (Judy) — delayed from this edition (msg 19f3bbdc2f0a09d4)
- Sig's next article (text/photos/credits promised by Wed Jul 15, msg 19f2539e60725e54)
- Adrian's next cover feature ("I will send one to start for July 19", msg 19f3bd677202980a subject line)
- Letter from Paris, Part 2 of 3 (already built, just needs re-linking into that edition's nav/homepage)

## Deferred to July 26

- Letter from Paris, Part 3 of 3 (already built, just needs re-linking into that edition's nav/homepage)

## Blockers

- **Gmail API credentials not available in remote session** — PDF attachments (Kintsugi, Letter from Paris) require Gmail API credentials at `~/.gmail-mcp/` which are absent in this cloud environment. These need to be downloaded in a local session before those articles can be built.

## Work Done This Session (Jul 7)

- ✅ Built `odyssey/index.html` — full Q&A text (8 questions, verbatim); photo added (63cebaf7...jpeg with caption credit)
- ✅ Fixed `making-history-awards/index.html` nav — removed dead July 5 links, now points to biba-roesch as next; fixed article date to July 12
- ✅ Copied datebook + daily-star-july from July 5; updated datebook title/kicker to July 12
- ✅ Created `editions/2026-06-{28,21,14,07}/index.html` — fixes Philip Vidal's "past editions not accessible" report
- ✅ Added John Makowski bio to `about.html` (More Contributors section, `id="john-makowski"`)

## Work Done This Session (Jul 10 — prep-edition)

- ✅ Built stub `index.html` for `biba-roesch`, `kintsugi`, `kiddieland`, `letter-from-paris` (placeholder body, hero photo where one exists on disk)
- ✅ Created `rocky-mountaineer/` folder + stub `index.html` (no photo yet — `thumb-placeholder.jpg` used for nav thumbs)
- ✅ Wired full nav chain: making-history-awards ↔ biba-roesch ↔ odyssey ↔ rocky-mountaineer ↔ kintsugi ↔ kiddieland ↔ letter-from-paris ↔ homepage; updated odyssey's next link (was pointing directly to kintsugi, now points to rocky-mountaineer)
- ✅ Copied `thumb-placeholder.jpg` into `editions/2026-07-12/`
- ✅ Filled homepage card grid with all 6 non-hero articles (placeholder teasers except odyssey, which has real content)
- ✅ Rebuilt `future-articles.html` pending table to match current 7-article lineup (was stale — wrong order, wrong slugs, missing odyssey/kiddieland, "Russell Lewis" typo)
- ✅ Built `kintsugi/index.html` from PDF — 14 photos placed per Jill's own layout (rendered PDF pages to images to extract placement); real hero is `IMG_9045.jpeg`, not `shutterstock_2308896621.jpeg` as earlier assumed
- ✅ Added Judy's Editor's Page post "How Classic Chicago Magazine Began" (corrected version, via docx attachment)
- ✅ Built `rocky-mountaineer/index.html` — full text + 17 photos from Ana's email, all explicitly placed
- ✅ Split `letter-from-paris` into 3 parts (letter-from-paris, letter-from-paris-2, letter-from-paris-3) — extracted all 11 embedded PDF images, placed per source layout; nav chain extended kiddieland → part 1 → part 2 → part 3 → homepage; homepage grid grew from 7 to 9 article cards

## Philip Vidal Questions (msg 19f397dad3bb3044, via Judy)

Philip asked three things — all answered by John via Judy (msg 19f3cc702a89554e, Jul 7):
1. ✅ **Past editions not accessible** — fixed by creating edition index pages for all 4 past editions
2. ✅ **Glessner House article link** — sent `editions/2026-06-21/glessner-house/` direct URL
3. ✅ **Where do "Leave a Comment" submissions go?** — explained FormSubmit → editor inbox flow

## Notes

- Nav chain (final, wired Jul 12 for publish): making-history-awards → biba-roesch → odyssey → rocky-mountaineer → kintsugi → kiddieland → letter-from-paris (part 1 of 3)
- Jill Lowe (`jill.lowe@mac.com`) is a guest contributor; bio added to about.html
- Edition published with 7 articles (kiddieland restored Jul 12; letter-from-paris runs Part 1 only, Parts 2/3 the following two weeks). All 7 Ready: making-history-awards, biba-roesch, odyssey, rocky-mountaineer, kintsugi, kiddieland, letter-from-paris (part 1)
- John Makowski bio added to about.html (`id="john-makowski"`)
- Making History Awards article date needs updating to July 12 when article text arrives

## Work Done This Session (Jul 12 — Kiddieland restored)

- ✅ Kiddieland's text had actually arrived from Annie on Jul 11 (msg `19f52a3c25973009`) but was missed during an earlier email-check pass; the article was incorrectly pulled and reported to Judy as missing. Judy caught this in her reply (msg `19f52b57f83f2fd3`) and asked for it to be restored
- ✅ Downloaded 5 numbered photos from Annie's email, built full `kiddieland/index.html` (category "Chicago History", title "The History of Kiddieland"), re-wired nav chain kintsugi ↔ kiddieland ↔ letter-from-paris, added homepage card and about.html popup entry, added Adrian Naves back to "Our Writers This Week"
- ✅ Fixed Making History Awards Photo 4 caption to add Leo Melamed's name per Judy's request (msg `19f52babc7e89e9e`)
- ✅ Investigated Judy's report that the Giotto/Toots photo in Biba's article was sideways (msg `19f52bc434b128c3`) — confirmed via browser that the live site already renders it correctly; the file's EXIF orientation tag is what some mail clients show as sideways, but browsers ignore it for this PNG. No file change made — attempted baking in the EXIF rotation once and it broke the display, reverted via git

## Work Done This Session (Jul 12 — publish day)

- ✅ Pulled `kiddieland` from the nav chain: kintsugi's next link and letter-from-paris's prev link now point directly to each other; stub + cover photo left on disk, unlinked from nav/homepage
- ✅ Removed kiddieland card from homepage grid (`index.html`)
- ✅ Updated `future-articles.html` — removed kiddieland row from July 12 lineup table, added "Pulled from July 12" note, renumbered letter-from-paris-2/3 rows (7b/7c → 6b/6c), shifted Kiddieland Parts 1/2/3 to July 19/July 26/Aug 2
