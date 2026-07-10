# July 12, 2026 Edition — Status

_Updated: 2026-07-07_

## Lineup (Judy, Jul 7, msg 19f3bdbfb7e3e937 — "Photos for The Odyssey")

Order updated from original Jul 6 schedule. Golden Triangle replaced by John Makowski Odyssey Q&A. Judy moved Odyssey to #3 (msg 19f3bdbfb7e3e937).

| # | Slug | Title | Author | Coordinator | HTML | Photos | Notes |
|---|------|-------|--------|-------------|------|--------|-------|
| 1 | making-history-awards | Making History Awards | Judy Carmack Bross | Ana | ⚠ stub | ✅ 1 cover | Cover: Buddy Guy with Ronnie Baker Brooks (`Buddy Guy 22.jpg`, on disk); Judy re-sent cover Jul 6 (msg 19f36d6d20b74ddd); article text promised "today" (Jul 6); Eric Miller captions unconfirmed — Judy checking with Ana; nav chain fixed Jul 7 |
| 2 | biba-roesch | Biba Roesch's Favorite People | Biba Roesch | Emma | ❌ | ✅ 1 cover | Cover photo (Biba with Steve Zick, `steven-zick-01 copy.jpeg`) on disk (msg 19f373efb4caa832); article text not yet received |
| 3 | odyssey | What You Need to Know Before Seeing "The Odyssey" | John Makowski (Q&A) | Annie | ✅ | ✅ 1 photo | Built Jul 7 from email body (msg 19f3bd677202980a) — 8 Q&A questions verbatim; photo `63cebaf7-a253-4d5a-a62f-a1c72794e7a3.jpeg` on disk, caption: "Melinda Sue Gordon/Universal Pictures/Everett Collection" (msg 19f3be100e8c529a); nav: biba-roesch ← odyssey → kintsugi (rocky-mountaineer to be inserted when built) |
| 4 | rocky-mountaineer | Rocky Mountaineer Train Trip | Judy Carmack Bross | Ana | ❌ | ❌ | Text + photos promised by Judy "by Wednesday" (Jul 8, msg 19f3bbdc2f0a09d4); folder not yet created |
| 5 | kintsugi | Kintsugi (Jill Lowe's feature) | Jill Lowe | Emma | ❌ | ✅ 15 files | `64) Kintsugi.pdf` + lead photo `shutterstock_2308896621.jpeg` (msg 19f376918ce0cf05) and 13 more files (msg 19f3769fe0b412b8) all on disk, incl. `Screenshot 2026-07-04 at 08.44.00.png` (book cover "Use the Good Dishes" by Dr. Elaine Dembe); no captions in email — check PDF; PDF article → build text first, get placement before placing photos (mistake #29); PDF not downloadable without Gmail credentials |
| 6 | kiddieland | Kiddieland's Closing (Adrian Naves Illinois feature) | Adrian Naves | Annie | ❌ | ✅ 1 cover | Topic confirmed: Kiddieland closing soon (msg 19f3bbdc2f0a09d4); cover `IMG_1537.png` on disk (msg 19f3bdce53653692); article text to Annie by Friday Jul 11 |
| 7 | letter-from-paris | Letter from Paris | Russell Kelley | Judy → John | ❌ | ❌ | `Letter from Paris #39 040726.pdf` on disk (msg 19f3920d09f9d6c6); **author is Russell Kelley** (lineup originally said "Russell Lewis" — verify byline from PDF); long piece, Judy asks John to decide how to divide into 2–3 issues; PDF not downloadable without Gmail credentials |
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

## Philip Vidal Questions (msg 19f397dad3bb3044, via Judy)

Philip asked three things that need a reply from John:
1. ✅ **Past editions not accessible** — fixed by creating edition index pages for all 4 past editions
2. **Glessner House article link** — it's at `editions/2026-06-21/glessner-house/` on the live site; John should send Philip the direct URL
3. **Where do "Leave a Comment" submissions go?** — they go to `editor@classicchicagomagazine.com` via the FormSubmit endpoint; John should reply to Philip with this info

## Notes

- Nav chain: making-history-awards → biba-roesch → odyssey → kintsugi → kiddieland → letter-from-paris
- Rocky-mountaineer to be inserted between odyssey and kintsugi once built; update odyssey's next link and kintsugi's prev link at that time
- Jill Lowe (`jill.lowe@mac.com`) is a guest contributor; bio added to about.html
- John Makowski bio added to about.html (`id="john-makowski"`)
- Making History Awards article date needs updating to July 12 when article text arrives
