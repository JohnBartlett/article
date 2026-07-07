# July 12, 2026 Edition — Status

_Updated: 2026-07-06_

## Lineup (Judy, Jul 6, msg 19f36d4ca49d3ce6 — "Tentative schedule for July 12")

Order below is Judy's suggested Sunday order.

| # | Slug | Title | Author | Coordinator | HTML | Photos | Notes |
|---|------|-------|--------|-------------|------|--------|-------|
| 1 | making-history-awards | Making History Awards | Judy Carmack Bross | Ana | ❌ | ✅ 1 cover | Cover: Buddy Guy with Ronnie Baker Brooks (Buddy Guy 22.jpg, on disk); Judy re-sent cover Jul 6 (msg 19f36d6d20b74ddd); article text promised "today" (Jul 6); Eric Miller captions status unconfirmed — Judy checking with Ana |
| 2 | biba-roesch | Biba Roesch's Favorite People | Biba Roesch (?) | Emma | ❌ | ✅ 1 cover | Cover photo (Biba with Steve Zick, `steven-zick-01 copy.jpeg`) on disk (msg 19f373efb4caa832); article text not yet received |
| 3 | rocky-mountaineer | Rocky Mountaineer Train Trip | Judy Carmack Bross | Ana | ❌ | ❌ | Judy sending story + photos to Ana by Wednesday Jul 8 (msg 19f3bbdc2f0a09d4) |
| 4 | kintsugi | Kintsugi (Jill Lowe's feature) | Jill Lowe | Emma | ❌ | ✅ 15 files | `64) Kintsugi.pdf` + lead photo `shutterstock_2308896621.jpeg` (msg 19f376918ce0cf05) and 13 more files (msg 19f3769fe0b412b8) all on disk, incl. `Screenshot 2026-07-04 at 08.44.00.png` (book cover "Use the Good Dishes" by Dr. Elaine Dembe); no captions in email — check PDF for captions/placement; PDF article → build text first, get placement before placing photos (mistake #29) |
| 5 | letter-from-paris | Letter from Paris | Russell Kelley | Judy → John | ❌ | ❌ | `Letter from Paris #39 040726.pdf` on disk (msg 19f3920d09f9d6c6); **author is Russell Kelley** (lineup originally said "Russell Lewis" — verify byline from PDF); long piece, Judy asks John to decide how to divide into 2–3 issues |
| 6 | kiddieland | Kiddieland's Closing (Adrian Naves Illinois feature) | Adrian Naves | Annie | ❌ | ✅ 1 cover | Topic confirmed: Kiddieland, long-time tradition closing soon (msg 19f3bbdc2f0a09d4); cover placeholder `IMG_1537.png` on disk (msg 19f3bdce53653692); article text to Annie by Friday Jul 10 |
| 7 | odyssey | What You Need to Know Before Seeing "The Odyssey" | John Makowski (Q&A) | Annie | ❌ | ✅ 1 photo | **Replaces Golden Triangle** (delayed to Jul 19, msg 19f3bbdc2f0a09d4); full Q&A text arrived in email body (msg 19f3bd677202980a) — **8 CCM questions, verify count in HTML (mistake #6)**; photo `63cebaf7-a253-4d5a-a62f-a1c72794e7a3.jpeg` on disk with caption credit from subject line: "Melinda Sue Gordon/Universal Pictures/Everett Collection" (msg 19f3be100e8c529a); Judy later suggested it could run as #3 (msg 19f3bdbfb7e3e937) — confirm position before homepage build |
| — | datebook | DateBook | Annie Delfosse | — | ✅* | — | Copied from July 5; new events pending from Annie |
| — | daily-star-july | Astrochart | Victoria Martin | — | ✅* | — | Copied from July 5; coverage already extends through July 31 |

Slugs for articles 3, 5–7 are provisional — folders not yet created (`/prep-edition` to run). biba-roesch/ and kintsugi/ folders exist (photos only, no index.html yet).

## Pending Deliveries

- **Judy** — Making History Awards article text (promised Jul 6); Rocky Mountaineer text + photos (to Ana by Wed Jul 8); more Odyssey photos (she's looking)
- **Biba Roesch / Emma** — Biba's Favorite People article text (Judy says Emma has it)
- **Adrian / Annie** — Kiddieland article text (Friday Jul 10)
- **Annie** — updated DateBook events for July 12
- **Eric Miller** — Making History Awards photo captions (Judy checking with Ana)
- **John** — decide how to divide the Russell Kelley Letter from Paris (2–3 parts); reply to Judy's readership-growth question (msg 19f38b3174c9aa65); reply to Philip Vidal's questions via Judy (msg 19f397dad3bb3044)

## Deferred to July 19

- Golden Triangle sale (Judy) — delayed from this edition (msg 19f3bbdc2f0a09d4)
- Sig's next article (text/photos/credits promised by Wed Jul 15, msg 19f2539e60725e54)
- Adrian's next cover feature ("I will send one to start for July 19", msg 19f3bd677202980a subject line)

## Blockers

- ~~No Gmail API credentials on this machine~~ **Resolved Jul 6**: new Desktop OAuth client "CCM Gmail CLI (John's Mac)" created in GCP project `classic-chicago-article-mgmt`; token saved to `~/.gmail-mcp/`; all pending attachments downloaded. (GA4 stats credentials `tools/credentials.json` still missing — separate issue.)

## Notes

- `/prep-edition` should now run with the full 7-article lineup (stubs, nav chain, homepage shell)
- Nav chain: Making History Awards prev/next both point to homepage (sole article) — will rewire once more articles are added
- Making History Awards was previously a placeholder stub sitting unwired in editions/2026-07-05/ (never linked from homepage or nav chain); moved here since it wasn't part of the July 5 lineup
- Jill Lowe (`jill.lowe@mac.com`) is a new/outside contributor caught by tier-2 search — not in tier-1 addresses
