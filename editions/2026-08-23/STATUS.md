# August 23, 2026 Edition — Status

_Updated: 2026-08-22 (session 2)_

7 of 9 lineup articles Ready (Michael Anderson, Biba's Favorite Things, Sig's Arts Club piece, Bonnie McDonald, Lincoln Park Stroll, Murray Bay, Unsung Gems). Only Susan Aurinko is still Placeholder — nothing received. DateBook/Astrochart unchanged.

## Judy's lineup (`1a00a96d0b7338ae`, received 2026-08-16)

1. Michael Anderson, new History Museum Head, by Libbet Richter — via Annie
2. Biba Roesch — via Emma
3. Sig's piece — The Arts Club Garden Project
4. Susan Aurinko — Emma
5. Landmark Preservation's Bonnie McDonald — turned out to be **by Ronald Clewer**, via Emma
6. Mike Traynor's Lincoln Park — via Annie
7. Murray Bay by Judy — via Ana
8. Unsung Gems (Croatia) by David Sweet — added Aug 18

Nav chain order (hero → last):
1. `michael-anderson` — Michael Anderson: The New Voice at the Chicago History Museum by Elizabeth Dunlop Richter
2. `biba-favorites-aug23` — Biba's Favorite Things: Mia Cohen by Biba Roesch
3. `sig-arts-club-garden` — Past Present and Future Steps (The Arts Club Garden Project) by Sigalit Zetouni
4. `susan-aurinko-aug23` — My Silk Roads by Susan Aurinko
5. `bonnie-mcdonald-landmarks` — Bonnie McDonald: Changing What—and Who—Preservation Is For by Ronald Clewer
6. `lincoln-park-stroll` — A Stroll Through a Park by Michael Traynor
7. `murray-bay` — Only in Murray Bay: Part 1 by Judy Carmack Bross
8. `unsung-gems` — The Pleasures of Discovering a New Country by David A. F. Sweet

## Articles

| Slug | Title | Author | HTML | Photos | Notes |
|------|-------|--------|------|--------|-------|
| michael-anderson | Michael Anderson: The New Voice at the Chicago History Museum | Elizabeth Dunlop Richter | ✅ Full text built | ✅ 11/11 placed | **READY.** Built from Annie's Aug 22 email (`1a028c4ae9ebffc0`). All 11 PNGs placed. |
| biba-favorites-aug23 | Biba's Favorite Things: Mia Cohen | Biba Roesch | ✅ Full text built | ✅ 5/5 placed | **READY.** Photo 4 is explicitly the cover per Emma's own text ("Photo 4- cover photo") — correctly hero-only, not duplicated inline. Photo 5 (`IMG_2724.JPG`) had its EXIF rotation baked in (was sideways). Emma's Aug 21 resend duplicated the same 2 photos under new filenames (`photo 4.JPEG`/`photo 5.JPG`) — confirmed byte-identical to the originals from Biba's daughter, kept the true original filenames (`IMG_2719.JPEG`/`IMG_2724.JPG`) and deleted the duplicates. |
| sig-arts-club-garden | Past Present and Future Steps | Sigalit Zetouni | ✅ Full text built | ✅ 5/5 placed | **READY.** Real title used (subtitle: "The Arts Club Garden Project"). Applied her self-reported spelling fix ("functionsl" → "functional"). One photo arrived as `.TIFF` (browsers can't render it) — converted to `.jpg`, same base filename, original deleted. Two large files (7-8MB) compressed to ~1MB. Photo 5 of 5 was byte-identical to the already-placed hero photo — not duplicated. |
| susan-aurinko-aug23 | My Silk Roads | Susan Aurinko | Placeholder | — | Not yet received |
| bonnie-mcdonald-landmarks | Bonnie McDonald: Changing What—and Who—Preservation Is For | Ronald Clewer | ✅ Full text built | ✅ 9/9 placed | **READY.** Full text arrived from Emma (`1a027d248b7e5d60`) — **byline is Ronald Clewer, not Emma** (she was only forwarding, confirmed by "By Ronald Clewer" in the piece itself). Retitled and re-attributed accordingly. Cover photo 4 confirmed to be a higher-res version of the earlier ad-hoc "Frank Butterfield Photo #1.jpeg" — replaced with the official one, duplicate deleted. `photo 1.JPG` was 14.7MB — compressed to ~265KB. |
| lincoln-park-stroll | A Stroll Through a Park | Michael Traynor | ✅ Full text built | ✅ 16/16 placed | **READY.** Photo essay piece — text explicitly describes photos as a slideshow with "any order," so no individual captions were fabricated. Placed all 14 remaining images (image7.jpeg was already the hero) as a plain sequential gallery, matching the site's established photo-essay convention (e.g. Nick Wilder's Summer Photo Essay). |
| murray-bay | Only in Murray Bay: Part 1 | Judy Carmack Bross | ✅ Full text built | ✅ 12/12 placed | **READY** (completed prior session). **Open: "Part 1" is genuine (Ana's own subject line) but no explicit Part 2/3 scheduling agreement was found in the emails — confirm timing with Judy before assuming a specific future edition, per the multi-part rule.** |
| unsung-gems | The Pleasures of Discovering a New Country | David A. F. Sweet | ✅ Full text built | ✅ 3/3 placed | **READY** (completed prior session). |
| datebook | DateBook | Annie Delfosse | Copied forward, dated Aug 23 | — | Still no content received from Annie despite her Aug 17 confirmation that she'd update it this week. |
| daily-star-august | Astrochart | Victoria Martin | Copied forward, unchanged | — | Still within August; coverage confirmed through Aug 31 |

## Open items requiring your input

1. ~~Two missing `about.html` bio anchors~~ — resolved Aug 22: added minimal cards for both. Michael Traynor's is a bare name + generic "Contributing Writer" role (no other info available — nothing to source it from). Ronald Clewer's role ("Board Chair, Landmarks Illinois") was sourced directly from his own bylined article.
2. **Murray Bay "Part 1"** — genuine per Ana's subject line, but no confirmed Part 2/3 schedule found. Worth a quick confirmation with Judy so a future edition doesn't get built without it, or so this one doesn't imply a promise that isn't kept.
3. **DateBook** — Annie confirmed Aug 17 she'd update it "this week" but nothing has arrived as of Aug 22, one day before publish.
4. **Susan Aurinko** — the only remaining fully-blank slot. No text, no photos, no contact from her or Emma about it yet.

## Notes

- Nav chain order (hero → last): michael-anderson → biba-favorites-aug23 → sig-arts-club-garden → susan-aurinko-aug23 → bonnie-mcdonald-landmarks → lincoln-park-stroll → murray-bay → unsung-gems
- Nav thumbnails use the shared `thumb-placeholder.jpg` at the edition root.
- Multiple EXIF-rotation fixes applied this session (Biba's, Sig's photos) — baked in via `ImageOps.exif_transpose()` rather than relying on browser EXIF support, consistent with this site's documented history of EXIF rotation not reliably working in production even when previews look correct.
- Multiple oversized-source-photo compressions applied this session (Bonnie's photo 1: 14.7MB→265KB; Sig's TIFF: 15.7MB→840KB; Sig's "leticia install": 8.7MB→1.3MB) — none were ever close to the 25MB Cloudflare limit, but compressed proactively for page-weight reasons.
