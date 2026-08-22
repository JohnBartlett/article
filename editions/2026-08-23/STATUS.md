# August 23, 2026 Edition — Status

_Updated: 2026-08-22 (session 3)_

**7 of 7 lineup articles Ready.** Susan Aurinko was confirmed by Judy to be held for Aug 30 (not this edition) and has been fully removed — folder deleted, nav chain rewired, homepage card removed. One unresolved issue: Michael Anderson's photos are still too low-resolution; a "fix" attempt from Judy did not actually solve it (see below).

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
| michael-anderson | Michael Anderson: The New Voice at the Chicago History Museum | Elizabeth Dunlop Richter | ✅ Full text built | ⚠️ 11/11 placed, but low-res | **Ready but photo quality unresolved.** All 11 original PNGs are tiny (300-600px), causing visible softness at article width. Asked Annie for full-resolution originals (Aug 22); Judy forwarded to Libbet, who sent back a "Michael Anderson Profile.pdf" as "the original" — but its embedded images are 230-475px, essentially the same size or smaller. **This did not solve the problem** — likely the same Word doc just exported to PDF, not fresh camera-roll photos. Still waiting on genuine originals. |
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

1. **Michael Anderson's photos are still low-resolution.** Judy's PDF attempt didn't fix it (see above) — someone (Annie, Libbet, or Michael Anderson's team directly) needs to send the actual full-size originals, not a Word/PDF export of them.
2. **DateBook** — Annie confirmed Aug 17 she'd update it "this week" but nothing has arrived as of Aug 22, one day before publish.

## Notes

- Nav chain order (hero → last): michael-anderson → biba-favorites-aug23 → sig-arts-club-garden → bonnie-mcdonald-landmarks → lincoln-park-stroll → murray-bay → unsung-gems
- Nav thumbnails use the shared `thumb-placeholder.jpg` at the edition root.
- Real bios for Michael Traynor and Ronald Clewer received from Judy Aug 22 (`1a02ad1e4421e789`) and added to `about.html`, replacing the earlier bare-minimum placeholders.
- Multiple EXIF-rotation fixes applied this session (Biba's, Sig's photos) — baked in via `ImageOps.exif_transpose()` rather than relying on browser EXIF support, consistent with this site's documented history of EXIF rotation not reliably working in production even when previews look correct.
- Multiple oversized-source-photo compressions applied this session (Bonnie's photo 1: 14.7MB→265KB; Sig's TIFF: 15.7MB→840KB; Sig's "leticia install": 8.7MB→1.3MB) — none were ever close to the 25MB Cloudflare limit, but compressed proactively for page-weight reasons.
