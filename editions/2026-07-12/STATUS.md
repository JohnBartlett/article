# July 12, 2026 Edition — Status

_Updated: 2026-07-06_

## Lineup (Judy, Jul 6, msg 19f36d4ca49d3ce6 — "Tentative schedule for July 12")

Order below is Judy's suggested Sunday order.

| # | Slug | Title | Author | Coordinator | HTML | Photos | Notes |
|---|------|-------|--------|-------------|------|--------|-------|
| 1 | making-history-awards | Making History Awards | Judy Carmack Bross | Ana | ❌ | ✅ 1 cover | Cover: Buddy Guy with Ronnie Baker Brooks (Buddy Guy 22.jpg, on disk); Judy re-sent cover Jul 6 (msg 19f36d6d20b74ddd); article text promised "today" (Jul 6); Eric Miller captions status unconfirmed — Judy checking with Ana |
| 2 | biba-roesch | Biba Roesch's Favorite People | Biba Roesch (?) | Emma | ❌ | ⏳ cover sent | Cover photo (Biba with Steve Zick, `steven-zick-01 copy.jpeg`) sent Jul 6 (msg 19f373efb4caa832) — **needs manual download**; article text not yet received |
| 3 | rocky-mountaineer | Rocky Mountaineer Train Trip | Judy Carmack Bross | Ana | ❌ | ❌ | Not yet received |
| 4 | kintsugi | Kintsugi (Jill Lowe's feature) | Jill Lowe | Emma | ❌ | ⏳ 14 files sent | Article PDF `64) Kintsugi.pdf` + lead photo `shutterstock_2308896621.jpeg` (msg 19f376918ce0cf05, to Judy CC John); 13 photos + 1 screenshot sent direct to John (msg 19f3769fe0b412b8) — **all need manual download**; PDF article → build text first, get placement before placing photos (mistake #29) |
| 5 | letter-from-paris | Letter from Paris | Russell Lewis | Judy | ❌ | ❌ | To be divided into several parts; Judy will send to John to look at |
| 6 | adrian-illinois | Adrian Naves Illinois feature | Adrian Naves | Annie | ❌ | ❌ | Not yet received |
| 7 | golden-triangle | Golden Triangle sale | Judy Carmack Bross | Annie | ❌ | ❌ | Not yet received |
| — | datebook | DateBook | Annie Delfosse | — | ✅* | — | Copied from July 5; new events pending from Annie |
| — | daily-star-july | Astrochart | Victoria Martin | — | ✅* | — | Copied from July 5; coverage already extends through July 31 |

Slugs for articles 2–7 are provisional — folders not yet created (`/prep-edition` to run).

## Pending Deliveries

- **Judy** — Making History Awards article text (promised Jul 6); Rocky Mountaineer text + photos; Golden Triangle text + photos; Russell Lewis Letter from Paris parts
- **Biba Roesch / Emma** — Biba's Favorite People article text
- **Adrian / Annie** — Illinois feature
- **Annie** — updated DateBook events for July 12
- **Eric Miller** — Making History Awards photo captions (Judy checking with Ana)

## Blockers

- **No Gmail API credentials on this machine** (`~/.gmail-mcp/` missing) — attachments cannot be auto-downloaded. Needs John to either run `python3 tools/get_gmail_token.py` (requires client_secret JSON in ~/Downloads) or download manually:
  - `steven-zick-01 copy.jpeg` (Biba cover, msg 19f373efb4caa832) → `editions/2026-07-12/biba-roesch/`
  - `64) Kintsugi.pdf` + `shutterstock_2308896621.jpeg` (msg 19f376918ce0cf05) → `editions/2026-07-12/kintsugi/`
  - 14 Kintsugi photo files (msg 19f3769fe0b412b8) → `editions/2026-07-12/kintsugi/`

## Notes

- `/prep-edition` should now run with the full 7-article lineup (stubs, nav chain, homepage shell)
- Nav chain: Making History Awards prev/next both point to homepage (sole article) — will rewire once more articles are added
- Making History Awards was previously a placeholder stub sitting unwired in editions/2026-07-05/ (never linked from homepage or nav chain); moved here since it wasn't part of the July 5 lineup
- Jill Lowe (`jill.lowe@mac.com`) is a new/outside contributor caught by tier-2 search — not in tier-1 addresses
