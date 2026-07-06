# July 12, 2026 Edition — Status

_Updated: 2026-07-06_

## Lineup (Judy, Jul 6, msg 19f36d4ca49d3ce6 — "Tentative schedule for July 12")

Order below is Judy's suggested Sunday order.

| # | Slug | Title | Author | Coordinator | HTML | Photos | Notes |
|---|------|-------|--------|-------------|------|--------|-------|
| 1 | making-history-awards | Making History Awards | Judy Carmack Bross | Ana | ❌ | ✅ 1 cover | Cover: Buddy Guy with Ronnie Baker Brooks (Buddy Guy 22.jpg, on disk); Judy re-sent cover Jul 6 (msg 19f36d6d20b74ddd); article text promised "today" (Jul 6); Eric Miller captions status unconfirmed — Judy checking with Ana |
| 2 | biba-roesch | Biba Roesch's Favorite People | Biba Roesch (?) | Emma | ❌ | ✅ 1 cover | Cover photo (Biba with Steve Zick, `steven-zick-01 copy.jpeg`) on disk (msg 19f373efb4caa832); article text not yet received |
| 3 | rocky-mountaineer | Rocky Mountaineer Train Trip | Judy Carmack Bross | Ana | ❌ | ❌ | Not yet received |
| 4 | kintsugi | Kintsugi (Jill Lowe's feature) | Jill Lowe | Emma | ❌ | ✅ 15 files | `64) Kintsugi.pdf` + lead photo `shutterstock_2308896621.jpeg` (msg 19f376918ce0cf05) and 13 more files (msg 19f3769fe0b412b8) all on disk, incl. `Screenshot 2026-07-04 at 08.44.00.png` (book cover "Use the Good Dishes" by Dr. Elaine Dembe); no captions in email — check PDF for captions/placement; PDF article → build text first, get placement before placing photos (mistake #29) |
| 5 | letter-from-paris | Letter from Paris | Russell Lewis | Judy | ❌ | ❌ | To be divided into several parts; Judy will send to John to look at |
| 6 | adrian-illinois | Adrian Naves Illinois feature | Adrian Naves | Annie | ❌ | ❌ | Not yet received |
| 7 | golden-triangle | Golden Triangle sale | Judy Carmack Bross | Annie | ❌ | ❌ | Not yet received |
| — | datebook | DateBook | Annie Delfosse | — | ✅* | — | Copied from July 5; new events pending from Annie |
| — | daily-star-july | Astrochart | Victoria Martin | — | ✅* | — | Copied from July 5; coverage already extends through July 31 |

Slugs for articles 3, 5–7 are provisional — folders not yet created (`/prep-edition` to run). biba-roesch/ and kintsugi/ folders exist (photos only, no index.html yet).

## Pending Deliveries

- **Judy** — Making History Awards article text (promised Jul 6); Rocky Mountaineer text + photos; Golden Triangle text + photos; Russell Lewis Letter from Paris parts
- **Biba Roesch / Emma** — Biba's Favorite People article text
- **Adrian / Annie** — Illinois feature
- **Annie** — updated DateBook events for July 12
- **Eric Miller** — Making History Awards photo captions (Judy checking with Ana)

## Blockers

- ~~No Gmail API credentials on this machine~~ **Resolved Jul 6**: new Desktop OAuth client "CCM Gmail CLI (John's Mac)" created in GCP project `classic-chicago-article-mgmt`; token saved to `~/.gmail-mcp/`; all pending attachments downloaded. (GA4 stats credentials `tools/credentials.json` still missing — separate issue.)

## Notes

- `/prep-edition` should now run with the full 7-article lineup (stubs, nav chain, homepage shell)
- Nav chain: Making History Awards prev/next both point to homepage (sole article) — will rewire once more articles are added
- Making History Awards was previously a placeholder stub sitting unwired in editions/2026-07-05/ (never linked from homepage or nav chain); moved here since it wasn't part of the July 5 lineup
- Jill Lowe (`jill.lowe@mac.com`) is a new/outside contributor caught by tier-2 search — not in tier-1 addresses
