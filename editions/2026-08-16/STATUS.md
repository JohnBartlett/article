# August 16, 2026 Edition — Status

_Updated: 2026-08-14_

**Skeleton built, nav chain and homepage wired. 2 of 7 lineup slots fully built (Vanja Malloy, David Sweet's Venice piece). 4 slots are placeholders awaiting contributor content. 1 slot (Mike Traynor) held out of the folder structure — author unclear, needs clarification from Judy before it can be built.**

## Judy's tentative lineup (`19fe6291d9a8a9cf`, received 2026-08-09)

> "Here is a tentative list of pieces for August 16, there might be a slight change"

1. Bob Glaze Weekend Update — via Emma
2. David Sweet piece — Judy to get to John
3. Mike Traynor — via Annie
4. Vanja Malloy feature by Judy — via Ana
5. Sig on Art — via John
6. Cheryl on Gardens — via Annie
7. Landmarks Preservation's Bonnie McDonald by Judy — via Emma

Nav chain order (hero → last), Mike Traynor excluded until resolved:
1. `bob-glaze-weekend-update` — Bob Glaze Weekend Update by Bob Glaze
2. `unsung-gems-venice` — Venice Energizes Family That Was Left Holding the Bag by David A. F. Sweet
3. `vanja-malloy` — Vanja Malloy: The Unexpected at the Smart by Judy Carmack Bross
4. `sig-mca-mike-cloud` — Mike Cloud at the MCA by Sigalit Zetouni
5. `cheryl-gardens` — Cheryl on Gardens by Cheryl Anderson
6. `bonnie-mcdonald-landmarks` — Bonnie McDonald and Landmarks Preservation by Judy Carmack Bross

## Articles

| Slug | Title | Author | HTML | Photos | Notes |
|------|-------|--------|------|--------|-------|
| bob-glaze-weekend-update | Bob Glaze Weekend Update | Bob Glaze | Placeholder | — | No content received yet. Hero slot. |
| unsung-gems-venice | Venice Energizes Family That Was Left Holding the Bag | David A. F. Sweet | ✅ Full text built (Aug 14) | ✅ 3/3 placed | Extracted from `Unsung Gems Venice.docx`. Captions confirmed in order (Venice 1: Grand Canal / hero; Venice 2: Hotel Flora courtyard; Venice 3: Woman in a Sailor Shirt, Peggy Guggenheim). David confirmed Venice 1 as cover in his Aug 11 reply to Judy (`19ff127400161e07`). |
| mike-traynor | *(held — not built)* | *(unclear)* | — | — | Judy's lineup doesn't say who's writing this piece, only that Annie is coordinating. Held out of the folder structure per `/prep-edition` guidance rather than guessing a slug/author — **needs clarification from Judy before this can be built.** |
| vanja-malloy | Vanja Malloy: The Unexpected at the Smart | Judy Carmack Bross | ✅ Full text built (by an earlier parallel session) | ✅ 4/4 placed | Q&A profile of the Smart Museum's director, via Ana Baca. Judy approved as-is ("It just looks great!", `19ff7cc9436c0389`). 3 identical copies of the cover photo arrived under different filenames (`COVER - Vanja Malloy.jpg` from Ana, `1 Vanja.jpg` also from Ana, `Vanja-Malloy.jpg` sent separately by Judy) — confirmed byte-identical via md5, kept `COVER - Vanja Malloy.jpg` as canonical, removed the Judy duplicate. |
| sig-mca-mike-cloud | Mike Cloud at the MCA | Sigalit Zetouni | Placeholder | Blast image + credit in hand (`image0.jpeg`, Aug 13) | Full article text/photos due "tomorrow" per Sig's Aug 13 blast-text email — matches her agreed Fri Aug 14 deadline from the Aug 11 schedule Judy approved. Not yet arrived as of this update. |
| cheryl-gardens | Cheryl on Gardens | Cheryl Anderson | Placeholder | — | No content received yet. |
| bonnie-mcdonald-landmarks | Bonnie McDonald and Landmarks Preservation | Judy Carmack Bross | Placeholder | — | No content received yet. |
| datebook | DateBook | Annie Delfosse | Copied forward from Aug 9 (by earlier parallel session), title/date already updated | — | Already correctly dated "August 16, 2026" in kicker and `<title>`. Internal Astrochart nav link confirmed pointing to `daily-star-august` (not stale). |
| daily-star-august | Astrochart | Victoria Martin | Copied forward from Aug 9 (by earlier parallel session), unchanged | — | Still within August — no rename needed. |

## Notes

- Nav chain order (hero → last): bob-glaze-weekend-update → unsung-gems-venice → vanja-malloy → sig-mca-mike-cloud → cheryl-gardens → bonnie-mcdonald-landmarks
- Nav thumbnails across all built/stub articles use the shared `thumb-placeholder.jpg` at the edition root — matches the established Aug 9 convention (full-res cover images are too large per `verify_edition.py`'s nav-thumb size check; real small navthumbs still need to be generated once photos are final). Causes the same harmless "duplicate image used 2×" soft warning seen on prior editions.
- Homepage hero (Bob Glaze) and 3 of 5 remaining cards (Sig, Cheryl, Bonnie McDonald) use `card-placeholder.jpg` until real cover photos arrive.
- **Open decision:** Mike Traynor's authorship needs clarification from Judy — hold before building.
- Verified via `python3 tools/verify_edition.py 2026-08-16`: 2 Ready, 2 Text Only (datebook/daily-star, expected), 4 Placeholder.
