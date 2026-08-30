# August 23, 2026 Edition — Status

_Updated: 2026-08-23 (session 4, post-publish)_

**7 of 7 lineup articles Ready.** Susan Aurinko was confirmed by Judy to be held for Aug 30 (not this edition) and has been fully removed — folder deleted, nav chain rewired, homepage card removed. Michael Anderson's photo resolution issue is mostly resolved (7 of 11 upgraded to full-res via Libbet; 4 remain small — she genuinely doesn't have better originals for those).

## Judy's lineup (`1a00a96d0b7338ae`, received 2026-08-16)

1. Michael Anderson, new History Museum Head, by Libbet Richter — via Annie
2. Biba Roesch — via Emma
3. Sig's piece — The Arts Club Garden Project
4. ~~Susan Aurinko~~ — confirmed held for Aug 30, see Notes
5. Landmark Preservation's Bonnie McDonald — turned out to be **by Ronald Clewer**, via Emma
6. Mike Traynor's Lincoln Park — via Annie
7. Murray Bay by Judy — via Ana (Part 2 confirmed for Aug 30, possible Part 3 later)
8. Unsung Gems (Croatia) by David Sweet — added Aug 18

Nav chain order (hero → last):
1. `michael-anderson` — Michael Anderson: The New Voice at the Chicago History Museum by Elizabeth Dunlop Richter
2. `biba-favorites-aug23` — Biba's Favorite Things: Mia Cohen by Biba Roesch
3. `sig-arts-club-garden` — Past Present and Future Steps (The Arts Club Garden Project) by Sigalit Zetouni
4. `bonnie-mcdonald-landmarks` — Bonnie McDonald: Changing What—and Who—Preservation Is For by Ronald Clewer
5. `lincoln-park-stroll` — A Stroll Through a Park by Michael Traynor
6. `murray-bay` — Only in Murray Bay: Part 1 by Judy Carmack Bross
7. `unsung-gems` — The Pleasures of Discovering a New Country by David A. F. Sweet

## Articles

| Slug | Title | Author | HTML | Photos | Notes |
|------|-------|--------|------|--------|-------|
| michael-anderson | Michael Anderson: The New Voice at the Chicago History Museum | Elizabeth Dunlop Richter | ✅ Full text built | ✅ 7/11 upgraded to full-res, 4/11 still small | **READY, photo quality mostly resolved.** Libbet's PDF attempt (Aug 22 afternoon) didn't help, but her follow-up batch of 11 individual photo emails ("Sent as many as I can find") mostly did. Replaced 7 of 11 with genuine full-resolution originals (headshot, examining-the-book, podium, both dancer photos, Alaska mountain, Anderson-and-Caruso) — 3 needed EXIF rotation baked in, all converted PNG→JPG. Libbet explicitly couldn't find originals for 4: Anderson speaking on stage, Lincoln honor roll book, Cafaro handshake, and the bicycle photo — these remain at their original small size (she confirmed "I didn't take any of them myself" and sent duplicates of what she had). Note: the "Alaska trip" photo caption was softened from "...in Alaska" to just "Michael Anderson with Andrew Caruso" since the replacement photo is clearly not set in Alaska (garden setting) — Libbet offered it as a fallback for a store photo she couldn't locate, not a confirmed match. |
| biba-favorites-aug23 | Biba's Favorite Things: Mia Cohen | Biba Roesch | ✅ Full text built | ✅ 5/5 placed | **READY.** Photo 4 is explicitly the cover per Emma's own text ("Photo 4- cover photo") — correctly hero-only, not duplicated inline. Photo 5 (`IMG_2724.JPG`) had its EXIF rotation baked in (was sideways). |
| sig-arts-club-garden | Past Present and Future Steps | Sigalit Zetouni | ✅ Full text built | ✅ 5/5 placed | **READY.** Real title used (subtitle: "The Arts Club Garden Project"). One photo arrived as `.TIFF` — converted to `.jpg`. |
| bonnie-mcdonald-landmarks | Bonnie McDonald: Changing What—and Who—Preservation Is For | Ronald Clewer | ✅ Full text built | ✅ 9/9 placed | **READY.** Byline is Ronald Clewer, not Emma (she was only forwarding). |
| lincoln-park-stroll | A Stroll Through a Park | Michael Traynor | ✅ Full text built | ✅ 16/16 placed | **READY.** Photo essay, no individual captions (source said "any order"). |
| murray-bay | Only in Murray Bay: Part 1 | Judy Carmack Bross | ✅ Full text built | ✅ 12/12 placed | **READY.** Part 2 confirmed by Judy for Aug 30; possible Part 3 after that, not yet committed. |
| unsung-gems | The Pleasures of Discovering a New Country | David A. F. Sweet | ✅ Full text built | ✅ 3/3 placed | **READY.** |
| datebook | DateBook | Annie Delfosse | Copied forward, dated Aug 23 | — | Still no content received from Annie despite her Aug 17 confirmation that she'd update it this week. |
| daily-star-august | Astrochart | Victoria Martin | Copied forward, unchanged | — | Still within August; coverage confirmed through Aug 31 |

## Held for August 30

- **Susan Aurinko — "My Silk Roads."** Article and photos were sent to Emma on Aug 22, but Judy confirmed the same day (`1a02ac5af008253d`) this runs next week instead of Aug 23, since this edition already has another travel piece. Content exists and is in Emma's hands — not built into this edition. Logged in `future-articles.html`.
- **Murray Bay, Part 2.** Confirmed by Judy Aug 22 (`1a02ad1e4421e789`): "Murray Bay will have part 2 next week. I may do a part 3 but for now, just two."

## Open items requiring your input

1. **DateBook** — Annie confirmed Aug 17 she'd update it "this week" but nothing has arrived as of Aug 22, one day before publish.

## Notes

- Nav chain order (hero → last): michael-anderson → biba-favorites-aug23 → sig-arts-club-garden → bonnie-mcdonald-landmarks → lincoln-park-stroll → murray-bay → unsung-gems
- Real bios for Michael Traynor and Ronald Clewer received from Judy Aug 22 (`1a02ad1e4421e789`) and added to `about.html`, replacing the earlier bare-minimum placeholders.
- Multiple EXIF-rotation fixes applied this session (Biba's, Sig's photos) — baked in via `ImageOps.exif_transpose()` rather than relying on browser EXIF support, consistent with this site's documented history of EXIF rotation not reliably working in production even when previews look correct.
- Multiple oversized-source-photo compressions applied this session (Bonnie's photo 1: 14.7MB→265KB; Sig's TIFF: 15.7MB→840KB; Sig's "leticia install": 8.7MB→1.3MB) — none were ever close to the 25MB Cloudflare limit, but compressed proactively for page-weight reasons.
- **Post-publish audit fix (2026-08-23):** prev/next nav thumbnails across this edition (and Aug 9 and Aug 16, also already live) were all showing a generic shared `thumb-placeholder.jpg` instead of the linked article's actual photo — a regression from the correct per-article `navthumb.jpg` convention used through Aug 2. `verify_edition.py` had been flagging this the whole time as a "duplicate image" structural warning; it was misread in an earlier session as an intentional shared-icon pattern rather than the bug it was. Generated real 70×70 `navthumb.jpg` crops for all 21 affected articles across the 3 editions and rewired every prev/next thumbnail to point to the correct neighbor. Fixed and pushed to dev2, dev, and master (already live at chicagoclassicmag.com). `verify_edition.py` now reports zero structural issues on all 3 editions.
