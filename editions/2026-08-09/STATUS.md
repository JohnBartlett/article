# August 9, 2026 Edition — Status

_Updated: 2026-08-06_

**3 of 7 articles have full text placed (2 fully ready with photos, 1 with unconfirmed captions). 4 are stubs awaiting content.**

## Judy's official lineup (`19fd59ca7cdb169d`, received 2026-08-06)

Nav chain order (hero → last):
1. `nick-wilder-summer` — Nick Wilder's photo essays, Lemonade Stand cover
2. `sig-august` — "Spanish Loop" by Sigalit Zetouni (Miró/Picasso sculptures)
3. `this-date-in-history` — This Date in History by Scott Holleran
4. `josee-nadeau` — Josee Nadeau, Monet's Anniversary
5. `jill-lowe-hands` — Jill Lowe's feature on hands
6. `dance-for-life` — Dance for Life
7. `jean-poems` — Two poems by Jean Colonomos

Plus John's editorial on `editorial.html` (Editor's Page) — not part of this edition's nav chain.

**Note on session history:** this edition was prepped twice in parallel. An earlier pass by this session built a rough-lineup version using slugs that didn't match Judy's later official lineup email; that version was discarded (`git reset --hard`) once the official lineup and newer content arrived. A second, concurrent session built `this-date-in-history` first with real content. This STATUS.md reflects the reconciled, final state.

## Articles

| Slug | Title | Author | HTML | Photos | Notes |
|------|-------|--------|------|--------|-------|
| nick-wilder-summer | Nick Wilder's Summer Photo Essay | Nick Wilder | Placeholder — cover only | Cover photo placed as hero: `IMG_0312.jpeg` (msg `19fd343a2081cc95`) | Essay text and remaining photos not sent yet. **Nick has no `about.html` bio/anchor** — byline link 404s until one is added. |
| sig-august | Spanish Loop | Sigalit Zetouni | ✅ Full text built | ✅ 3/3 placed with credits: `IMG_7123.JPG` (hero, "The Picasso"), `IMG_3078.JPG` (climbing photo), `043_20160204_STOCK_MIRO.JPG` (Miró's Chicago — compressed from 18.6MB to ~700KB) | Full article ("Spanish Loop") + captions + a closing credit note — republished/expanded from Sig's Spring 2025 Chicago Life piece, per her own note in the text (kept verbatim). |
| this-date-in-history | This Date in History | Scott Holleran | ✅ Full text built (by the parallel session) | 3/3 placed — hero `images-1.jpeg` ("Charles Wacker"), plus `IMG_4085.jpg` and `IMG_4084.JPG` at the bottom | **Captions for the 2 bottom photos are not specified anywhere in Judy's email** ("Photos at the Bottom") — verify with her before publishing, don't guess. |
| josee-nadeau | Josee Nadeau: Monet's Anniversary | Judy Carmack Bross | Placeholder — cover only | Cover photo placed as hero: `IMG_20180726_055631_230.jpg` (msg `19fd5818aab34ff3`) | Article text not sent yet. |
| jill-lowe-hands | Jill Lowe's Feature on Hands | Jill Lowe | Placeholder | — | No content yet. |
| dance-for-life | Dance for Life | Judy Carmack Bross | Placeholder | — | No content yet; via Emma. |
| jean-poems | New Poems by Jean Colonomos ("Grief" & "Revery") | Jean Colonomos | ✅ Full text built | Candidate photo placed as hero, **not fully confirmed** — `Martha_Graham-Cave_of_the_Heart.jpg` (msg `19fd206307617732`, Judy: "Still thinking...") | Both poems + Judy's intro paragraph, in full. |
| datebook | DateBook | Annie Delfosse | Copied forward, title/date updated to Aug 9 | — | Already includes Annie's new event batch (~20 events, added to the Aug 2 copy in a separate commit before this edition branched off it) — no further action needed here. |
| daily-star-august | Astrochart | Victoria Martin | Copied forward unchanged | — | Still within August — no rename/edit needed. |

## Notes

- Nav chain order (hero → last): nick-wilder-summer → sig-august → this-date-in-history → josee-nadeau → jill-lowe-hands → dance-for-life → jean-poems
- Homepage hero uses Nick Wilder's real cover photo; cards for sig-august/this-date-in-history/josee-nadeau/jean-poems use their real photos; jill-lowe-hands/dance-for-life still use `card-placeholder.jpg`.
- Nav thumbnails across all 7 articles use a shared `thumb-placeholder.jpg` at the edition root — replace with real navthumbs as content/covers arrive. This causes a harmless "duplicate image used 2×" soft warning in `verify_edition.py` (same placeholder used for both prev and next on some pages) — expected until real navthumbs replace it.
- **Nick Wilder needs an `about.html` bio** before this edition can publish — new contributor, no anchor exists yet.
- **Open item:** confirm captions for the 2 bottom photos in `this-date-in-history` with Judy before publishing.
- **Open item:** confirm the Martha Graham photo choice for `jean-poems` with Judy before publishing — she hedged ("still thinking") rather than firmly deciding.
