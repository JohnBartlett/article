# August 16, 2026 Edition — Status

_Updated: 2026-08-15_

**5 of 7 articles have full text built. 2 still need photos (Drive downloads) and 2 remain fully pending (Sig's and Elizabeth Richter's).**

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
| sig-mca-mike-cloud | Mike Cloud at the MCA | Sigalit Zetouni | Placeholder | Blast image + credit in hand (`image0.jpeg`, Aug 13) | Full article promised "tomorrow" per her Aug 13 email — matches her Fri Aug 14 deadline from the Aug 11 schedule Judy approved. Not yet arrived. |
| unsung-gems-venice | Venice Energizes Family That Was Left Holding the Bag | David A. F. Sweet | ✅ Full text built | ✅ 3/3 placed | Extracted from `Unsung Gems Venice.docx`. Captions and cover (Venice 1, Grand Canal) confirmed by David in his Aug 11 reply to Judy. |
| cheryl-menton-garden | Jardin Botanique Val Rameh | Cheryl Anderson | ✅ Full text built (Aug 15) | ⚠️ 0/14 photos present — Drive links only | Full article received via Annie (thread `1a005710fbbe464f`). 14 photos linked as Google Drive files in the email — not attachments. HTML built with correct filenames from email. Photos need to be downloaded from Drive manually. Note: Photo 11 (Pond 2) has no Drive link in the email — may be an omission by the contributor. Contributor title is "Jardin Botanique Val Rameh" (email subject uses "Val Rameh" but body text uses "Val Rahmeh" with extra h — not corrected, flagged here). |
| elizabeth-richter-pacific-northwest | The Pacific Northwest | Elizabeth Dunlop Richter | Placeholder | — | New lineup slot, not in the Aug 9 tentative list. No content received yet. |
| adrian-debates | The Lincoln and Douglas Debates | Adrian Naves | ✅ Full text built (Aug 15) | ⚠️ 0/4 photos present — email attachments not yet extracted | Full article received via Annie (thread `1a005623dd420550`). 4 photos attached to the email: `1-Portrait.png`, `2-Audience.png`, `3-Color Painting.jpeg`, `4-Statue.png`. HTML built with correct filenames. Photos need to be extracted from Gmail message `1a005623dd420550` using `python3 tools/extract_article_photos.py 2026-08-16 --contributor annie` (once Gmail credentials are set up locally). |
| datebook | DateBook | Annie Delfosse | Copied forward, dated Aug 16 | — | Already correctly dated. |
| daily-star-august | Astrochart | Victoria Martin | Copied forward, unchanged | — | Still within August — no rename needed. |

## Resolved — Michael Traynor held for August 23

**Michael Traynor — "A Stroll Through a Park"** (thread `1a0055c04cbdd9b1`): Article submitted via Annie with photo attachments, real text about walking Lincoln Park. Judy confirmed Aug 15 (`1a005c75f44e7276`): **"I think we will save this for next when, August 23, when we have fewer stories."** Do NOT build into this edition's nav chain or homepage — log in `future-articles.html` as Held for Aug 23 instead. Content stays on disk, saved for that week.

## Notes

- Nav chain order (hero → last): vanja-malloy → bob-glaze-chicago-theaters → sig-mca-mike-cloud → unsung-gems-venice → cheryl-menton-garden → elizabeth-richter-pacific-northwest → adrian-debates
- Nav thumbnails use the shared `thumb-placeholder.jpg` at the edition root, matching established convention.
- Homepage hero (Vanja Malloy) uses her real cover photo with `object-position: center top` to keep her face in frame. Placeholder cards (Sig, Cheryl, Elizabeth Richter, Adrian) use `card-placeholder.jpg`.
- **Open items:** Sig's Mike Cloud/MCA article promised by 2pm Chicago time Aug 15, not yet arrived. Elizabeth Richter's full article still needed. Photo files for Adrian (email attachments) and Cheryl (Drive links) need to be downloaded.
