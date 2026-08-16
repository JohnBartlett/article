# August 16, 2026 Edition — Status

_Updated: 2026-08-15_

**All 7 lineup articles are built. 6 of 7 fully READY (text + all photos); Cheryl's is at 13/14 photos, one still owed by Annie. Edition is publish-ready pending that last photo.**

## Judy's updated lineup (`1a0025d6b16583a5`, received 2026-08-14)

> "I am thinking that this is a potential line up of articles. Let me know what you are missing."

1. Vanja Malloy
2. Bob Glaze on Chicago Theaters
3. Sig's piece on the man at MCA (Mike Cloud)
4. David Sweet on Venice
5. Cheryl Anderson on the Garden at Menton
6. Elizabeth Richter on the Pacific Northwest
7. Adrian Naves on [Lincoln-Douglas] Debates — "I will make sure Adrian has sent it in"

**Supersedes** her Aug 9 tentative list (`19fe6291d9a8a9cf`). Changes: Mike Traynor dropped (was never resolved who was writing it — correctly held out of the earlier build); Bonnie McDonald/Landmarks Preservation dropped entirely; Elizabeth Richter on the Pacific Northwest added as new; Vanja Malloy moved to hero (was #4); order otherwise reshuffled.

Nav chain order (hero → last):
1. `vanja-malloy` — Vanja Malloy: The Unexpected at the Smart by Judy Carmack Bross
2. `bob-glaze-chicago-theaters` — My Top Recent Theater Experiences in Chicago by Bob Glaze
3. `sig-mca-mike-cloud` — Mike Cloud at the MCA by Sigalit Zetouni
4. `unsung-gems-venice` — Venice Energizes Family That Was Left Holding the Bag by David A. F. Sweet
5. `cheryl-menton-garden` — Jardin Botanique Val Rameh by Cheryl Anderson
6. `elizabeth-richter-pacific-northwest` — The Pacific Northwest by Elizabeth Dunlop Richter
7. `adrian-debates` — The Lincoln and Douglas Debates by Adrian Naves

## Articles

| Slug | Title | Author | HTML | Photos | Notes |
|------|-------|--------|------|--------|-------|
| vanja-malloy | Vanja Malloy: The Unexpected at the Smart | Judy Carmack Bross | ✅ Full text built | ✅ 4/4 placed | Q&A profile of the Smart Museum's director, via Ana Baca. Judy approved as-is ("It just looks great!", `19ff7cc9436c0389`). Cover photo deduped from 3 identical copies sent under different filenames. |
| bob-glaze-chicago-theaters | My Top Recent Theater Experiences in Chicago | Bob Glaze | ✅ Full text built (Aug 14) | ✅ 12/12 placed | Tour of Chicago theater companies/venues (PrideArts, American Blues Theater, Black Ensemble Theater, Porchlight, Apollo Theater, Greenhouse Theater Center, Chicago Shakespeare, TimeLine Theatre, Broadway Playhouse). Explicit inline "Photo N — Venue, Show" map from the source email; Photos 11 and 10 appear in that reversed order in the text (venue shot before the specific production shot) — kept verbatim, not renumbered. |
| sig-mca-mike-cloud | Expressions in 3-D | Sigalit Zetouni | ✅ Full text built (Aug 15) | ✅ 7/7 placed | Arrived Aug 15 (text + 7 photo emails + a self-caught spelling fix). Opens with a Frank Stella biographical section, then reviews Mike Cloud's "Wordless Obstruction" at the MCA. Real title used ("Expressions in 3-D," from her own text) instead of the earlier placeholder "Mike Cloud at the MCA." |
| unsung-gems-venice | Venice Energizes Family That Was Left Holding the Bag | David A. F. Sweet | ✅ Full text built | ✅ 3/3 placed | Extracted from `Unsung Gems Venice.docx`. Captions and cover (Venice 1, Grand Canal) confirmed by David in his Aug 11 reply to Judy. |
| cheryl-menton-garden | Jardin Botanique Val Rameh | Cheryl Anderson | ✅ Full text built (Aug 15) | ⚠️ 13/14 placed (Aug 15) | Full article received via Annie (thread `1a005710fbbe464f`), approved by Judy. Photo 7 (Olive tree) had a Drive link but the download call failed 6 times across two sessions (metadata fetch always worked) — John downloaded it himself from Drive and dropped it in, now placed. **Photo 11 (Pond 2) is still missing** — no Drive link was ever supplied in the source email at all; likely a contributor omission, not fabricated or guessed. Asked Annie for it Aug 15 (`1a007aaf8537f514`), no reply yet. The `<figure>` for Photo 11 was removed entirely (not left as a broken-image placeholder) — add it back once the real photo arrives, using Photo 10's caption verbatim ("Victoria du Parana – Victoria cruziana"), tracked in `TODO.md`. Contributor title is "Jardin Botanique Val Rameh" (email subject uses "Val Rameh" but body text uses "Val Rahmeh" with extra h — not corrected, flagged here). |
| elizabeth-richter-pacific-northwest | The Olympic Peninsula: Where are the Vampires? | Elizabeth Dunlop Richter | ✅ Full text built (Aug 15) | ✅ 38/38 placed | Turned out she'd sent it to Annie as a PDF on **Aug 10** — before this even became a lineup item — but Annie never forwarded it. Judy tracked it down and sent it directly Aug 15, along with 5 corrections Libbet had also sent Annie on Aug 10 that were likewise never applied. PDF text and all 38 embedded photos extracted (via `pdfimages`/poppler) in source page order with original captions; all 5 corrections applied (see EMAIL_LOG.md for the list). Real title used ("The Olympic Peninsula: Where are the Vampires?") instead of the earlier placeholder "The Pacific Northwest." |
| adrian-debates | The Lincoln and Douglas Debates | Adrian Naves | ✅ Full text built (Aug 15) | ✅ 4/4 placed (Aug 15) | Full article received via Annie (thread `1a005623dd420550`), approved by Judy. Photos extracted directly from the Gmail message. Verified READY via `verify_edition.py`. |
| datebook | DateBook | Annie Delfosse | Copied forward, dated Aug 16 | — | Already correctly dated. |
| daily-star-august | Astrochart | Victoria Martin | Copied forward, unchanged | — | Still within August — no rename needed. |

## Resolved — Michael Traynor held for August 23

**Michael Traynor — "A Stroll Through a Park"** (thread `1a0055c04cbdd9b1`): Article submitted via Annie with photo attachments, real text about walking Lincoln Park. Judy confirmed Aug 15 (`1a005c75f44e7276`): **"I think we will save this for next when, August 23, when we have fewer stories."** Do NOT build into this edition's nav chain or homepage — log in `future-articles.html` as Held for Aug 23 instead. Content stays on disk, saved for that week.

## Notes

- Nav chain order (hero → last): vanja-malloy → bob-glaze-chicago-theaters → sig-mca-mike-cloud → unsung-gems-venice → cheryl-menton-garden → elizabeth-richter-pacific-northwest → adrian-debates
- Nav thumbnails use the shared `thumb-placeholder.jpg` at the edition root, matching established convention.
- Homepage hero (Vanja Malloy) uses her real cover photo with `object-position: center top` to keep her face in frame. Placeholder cards (Sig, Cheryl, Elizabeth Richter, Adrian) use `card-placeholder.jpg`.
- **Open item:** Cheryl's Photo 11 (Pond 2) — asked Annie for it Aug 15 (`1a007aaf8537f514`), reply owed. Otherwise the edition is publish-ready.
