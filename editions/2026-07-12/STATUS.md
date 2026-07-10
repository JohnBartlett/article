# July 12, 2026 Edition — Status

_Updated: 2026-07-07_

## Lineup (Judy, Jul 7, msg 19f3bdbfb7e3e937 — "Photos for The Odyssey")

Order updated from original Jul 6 schedule. Golden Triangle replaced by John Makowski Odyssey Q&A. Judy moved Odyssey to #3 (msg 19f3bdbfb7e3e937).

| # | Slug | Title | Author | Coordinator | HTML | Photos | Notes |
|---|------|-------|--------|-------------|------|--------|-------|
| 1 | making-history-awards | Making History Awards | Judy Carmack Bross | Ana | ⚠ stub | ✅ 1 cover | Cover: Buddy Guy with Ronnie Baker Brooks (`Buddy Guy 22.jpg`, on disk); Judy re-sent cover Jul 6 (msg 19f36d6d20b74ddd); article text promised "today" (Jul 6); Eric Miller captions unconfirmed — Judy checking with Ana; nav chain fixed Jul 7 |
| 2 | biba-roesch | Biba Roesch's Favorite People | Biba Roesch | Emma | ⚠ stub | ✅ 1 cover | Cover photo (Biba with Steve Zick, `steven-zick-01 copy.jpeg`) on disk (msg 19f373efb4caa832); article text not yet received; stub built Jul 10 (prep), nav wired making-history-awards ↔ biba-roesch ↔ odyssey |
| 3 | odyssey | What You Need to Know Before Seeing "The Odyssey" | John Makowski (Q&A) | Annie | ✅ | ✅ 1 photo | Built Jul 7 from email body (msg 19f3bd677202980a) — 8 Q&A questions verbatim; photo `63cebaf7-a253-4d5a-a62f-a1c72794e7a3.jpeg` on disk, caption: "Melinda Sue Gordon/Universal Pictures/Everett Collection" (msg 19f3be100e8c529a); nav updated Jul 10: biba-roesch ← odyssey → rocky-mountaineer |
| 4 | rocky-mountaineer | Canada's Rocky Mountaineer: Spectacular Scenery and Superb Service | Judy Carmack Bross and George York | Ana | ✅ | ✅ 17 photos | Built Jul 10 from Ana's email (msg `19f4c4d35fa69657`) — full text + cover + 16 numbered photos, all explicitly placed inline via `[PHOTO n - filename - caption]` markers in the email body (cleanest placement instructions of the edition, no guessing needed); Judy replied approving (msg `19f4c543a9b03d1e`): "This looks extraordinary"; co-author George York has no about.html bio yet — byline left unlinked for him, flag to Judy if one should be added; homepage card + odyssey/kintsugi nav thumbs updated to real cover photo |
| 5 | kintsugi | Use the Good Dishes&hellip; But If They Break, Is Kintsugi an Option? | Jill Lowe | Emma | ✅ | ✅ 14 photos | Built Jul 10 from PDF (`64) Kintsugi.pdf`) — rendered all 11 PDF pages to images to extract Jill's own photo placement order (no placement instructions in email, so used the PDF's own layout per mistake #29); matched all 14 photo files to their exact page positions by visual comparison; real hero is `IMG_9045.jpeg` (gilded porcelain plate, page 1) — not `shutterstock_2308896621.jpeg` as earlier assumed, that one is actually mid-article (page 5) with a real caption "Beautiful seams of gold glint in the conspicuous cracks of ceramic wares."; real personal photos are `IMG_9045.jpeg` (plate) and `IMG_8883.jpeg` (restored mercury pendulum clock, "Presented to Michael B. Lowe"), rest are stock/graphic images from the PDF; category "Facts and Froth" (Jill's column name); homepage card + nav thumbs updated to correct hero |
| 6 | kiddieland | Kiddieland's Closing (Adrian Naves Illinois feature) | Adrian Naves | Annie | ⚠ stub | ✅ 1 cover | Topic confirmed: Kiddieland closing soon (msg 19f3bbdc2f0a09d4); cover `IMG_1537.png` on disk (msg 19f3bdce53653692); article text to Annie by Friday Jul 11; stub built Jul 10 (prep) |
| 7 | letter-from-paris | Letter from Paris | Russell Kelley | Judy → John | ⚠ stub | ❌ | `Letter from Paris #39 040726.pdf` on disk (msg 19f3920d09f9d6c6); **author is Russell Kelley** (lineup originally said "Russell Lewis" — verify byline from PDF); long piece, Judy asks John to decide how to divide into 2–3 issues; PDF not downloadable without Gmail credentials; stub built Jul 10 (prep) as last article in nav chain, no photo yet |
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

## Philip Vidal Questions (msg 19f397dad3bb3044, via Judy)

Philip asked three things — all answered by John via Judy (msg 19f3cc702a89554e, Jul 7):
1. ✅ **Past editions not accessible** — fixed by creating edition index pages for all 4 past editions
2. ✅ **Glessner House article link** — sent `editions/2026-06-21/glessner-house/` direct URL
3. ✅ **Where do "Leave a Comment" submissions go?** — explained FormSubmit → editor inbox flow

## Notes

- Nav chain (final, wired Jul 10): making-history-awards → biba-roesch → odyssey → rocky-mountaineer → kintsugi → kiddieland → letter-from-paris
- Jill Lowe (`jill.lowe@mac.com`) is a guest contributor; bio added to about.html
- All 7 article stubs exist; still need real text for biba-roesch, rocky-mountaineer, kintsugi, kiddieland, letter-from-paris (only making-history-awards and odyssey have real photos/text beyond placeholders)
- John Makowski bio added to about.html (`id="john-makowski"`)
- Making History Awards article date needs updating to July 12 when article text arrives
