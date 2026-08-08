# August 9, 2026 Edition — Status

_Updated: 2026-08-08_

**5 of 7 articles have full text placed (4 fully ready with photos, 1 with unconfirmed captions). 2 are stubs awaiting content (1 has full text in hand, unbuilt).**

## Judy's official lineup (`19fd59ca7cdb169d`, received 2026-08-06)

Nav chain order (hero → last):
1. `nick-wilder-summer` — Nick Wilder's photo essays, Lemonade Stand cover
2. `sig-august` — "Spanish Loop" by Sigalit Zetouni (Miró/Picasso sculptures)
3. `this-date-in-history` — This Date in History by Scott Holleran
4. `josee-nadeau` — "Painting Giverny" by Josée Nadeau
5. `jill-lowe-hands` — Jill Lowe's feature on hands
6. `dance-for-life` — Dance for Life
7. `jean-poems` — Two poems by Jean Colonomos

Plus John's editorial on `editorial.html` (Editor's Page) — not part of this edition's nav chain.

**Note on session history:** this edition was prepped twice in parallel. An earlier pass by this session built a rough-lineup version using slugs that didn't match Judy's later official lineup email; that version was discarded (`git reset --hard`) once the official lineup and newer content arrived. A second, concurrent session built `this-date-in-history` first with real content. This STATUS.md reflects the reconciled, final state.

## Articles

| Slug | Title | Author | HTML | Photos | Notes |
|------|-------|--------|------|--------|-------|
| nick-wilder-summer | Nick Wilder's Summer Photo Essay | Nick Wilder | Placeholder — cover only | Cover photo placed as hero: `IMG_0312.jpeg` (msg `19fd343a2081cc95`) | **Full essay text arrived Aug 8** (msg `19fdfb50d13e1a5b`) with 23 numbered Drive-linked photos — text has explicit "Photo N" placement map (Chicago section then Door County section). Not yet built — awaiting the 23 photos to be downloaded locally (Drive files too large to pull individually through the Drive MCP tool). |
| sig-august | Spanish Loop | Sigalit Zetouni | ✅ Full text built | ✅ 3/3 placed with credits: `IMG_7123.JPG` (hero, "The Picasso"), `IMG_3078.JPG` (climbing photo), `043_20160204_STOCK_MIRO.JPG` (Miró's Chicago — compressed from 18.6MB to ~700KB) | Full article ("Spanish Loop") + captions + a closing credit note — republished/expanded from Sig's Spring 2025 Chicago Life piece, per her own note in the text (kept verbatim). |
| this-date-in-history | This Date in History | Scott Holleran | ✅ Full text built (by the parallel session) | 3/3 placed — hero `images-1.jpeg` ("Charles Wacker"), plus `IMG_4085.jpg` and `IMG_4084.JPG` at the bottom | **Captions for the 2 bottom photos are not specified anywhere in Judy's email** ("Photos at the Bottom") — verify with her before publishing, don't guess. |
| josee-nadeau | Painting Giverny | Josée Nadeau | ✅ Full text built (Aug 7) | ✅ 10/10 placed (cover + 9 numbered, all with placement/captions from Ana's explicit map) | First-person piece written by Josée Nadeau herself — arrived via Ana Baca, not a Judy-authored profile as the lineup email implied. Covers her decade painting at Giverny under Gérald Van der Kemp's invitation, for Monet's centenary. Added a new `about.html` bio for Josée (first-time contributor). Old placeholder cover file (`IMG_20180726_055631_230.jpg`, sent standalone Aug 6) confirmed byte-identical to the article's own `COVER - Josee Nadeau.jpg` and removed. |
| jill-lowe-hands | Jill Lowe's Feature on Hands | Jill Lowe | Placeholder | — | No content yet. Jill's Aug 8 email ("A helping hand...") asks John to send *her* a draft to review — backwards from her being the piece's author. **Needs a clarifying reply before building anything**, not a guess. |
| dance-for-life | Dance for Life ("Jubilation Anticipation") | Judy Carmack Bross | ✅ Full text built (Aug 8) | ✅ 10/10 placed with credits | Chicago Dance Health Fund's 35th anniversary; interview with co-chairs Gary Metzner and Scott Johnson. Photo 2 (Hubbard Street Dance Chicago) had a mixup — Emma's Drive folder had a "photo 2.jpg" that turned out to be a different, unrelated shot; Judy caught it and sent the correct photo directly, matching the article's own caption exactly — used that instead, removed the mismatched Drive file. One photo (an unlabeled shot of co-chairs Scott Johnson and Gary Metzner, referenced in the text between Photo 2 and Photo 4) was never sent by anyone — omitted rather than guessed at; still an open gap. |
| jean-poems | New Poems by Jean Colonomos ("Grief" & "Revery") | Jean Colonomos | ✅ Full text built | Candidate photo placed as hero, **not fully confirmed** — `Martha_Graham-Cave_of_the_Heart.jpg` (msg `19fd206307617732`, Judy: "Still thinking...") | Both poems + Judy's intro paragraph, in full. |
| datebook | DateBook | Annie Delfosse | Copied forward, title/date updated to Aug 9 | — | Already includes Annie's new event batch (~20 events, added to the Aug 2 copy in a separate commit before this edition branched off it) — no further action needed here. |
| daily-star-august | Astrochart | Victoria Martin | Copied forward unchanged | — | Still within August — no rename/edit needed. |

## Notes

- Nav chain order (hero → last): nick-wilder-summer → sig-august → this-date-in-history → josee-nadeau → jill-lowe-hands → dance-for-life → jean-poems
- Homepage hero uses Nick Wilder's real cover photo; cards for sig-august/this-date-in-history/josee-nadeau/jean-poems use their real photos; jill-lowe-hands/dance-for-life still use `card-placeholder.jpg`.
- Nav thumbnails across all 7 articles use a shared `thumb-placeholder.jpg` at the edition root — replace with real navthumbs as content/covers arrive. This causes a harmless "duplicate image used 2×" soft warning in `verify_edition.py` (same placeholder used for both prev and next on some pages) — expected until real navthumbs replace it.
- **Open item:** confirm captions for the 2 bottom photos in `this-date-in-history` with Judy before publishing.
- **Open item:** confirm the Martha Graham photo choice for `jean-poems` with Judy before publishing — she hedged ("still thinking") rather than firmly deciding.
- Francesco Bianchini confirmed **not** in this edition — moved to August 16 per Judy (msg `19fdc80b690541f6`).
