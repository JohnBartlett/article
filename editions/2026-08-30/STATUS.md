# August 30, 2026 Edition — Status

_Updated: 2026-08-29_

Nav chain, homepage, and folder skeleton wired for the full 8-article lineup. Chicago Innovation and Susan Aurinko's health retreat piece both arrived with full text and are now fully built — 5 of 8 articles are Ready; 3 remain placeholder stubs awaiting content.

## Judy's official lineup (`1a02e630509ec117`, received 2026-08-23)

1. Chicago Innovation — Emma
2. Murray Bay, Part 2 — Ana (photos), Judy (author)
3. Soma Roy Feature — Annie
4. David Sweet — Judy sending directly to John
5. Susan Aurinko Health retreat story — Emma
6. Young dancer's perspective, Judy — Annie
7. Sydney Armstrong's Griffin Museum — Ana — **delayed to Sept 6** (Judy, Aug 25, `1a03867ed50ac1c4`), removed from this lineup
8. Sig's article: Garfield Park Conservatory — Sig sends to John

**Not in Judy's numbered lineup:** Philip Vidal's "About the Town" (via Ana, `1a03315f72b0a964`) — slotted in at the traditional end-of-month position, last in the nav chain.

Nav chain order (hero → last):
1. `chicago-innovation` — Rallying Chicago's Next Innovators by Judy Carmack Bross
2. `murray-bay-part-2` — Only in Murray Bay: Part II by Judy Carmack Bross
3. `soma-roy` — Soma Roy Feature by Annie Delfosse (byline tentative — see Notes)
4. `sporting-life` — Birthplace of the Olympics Reveals Naked Truth by David A. F. Sweet
5. `silk-roads-health-retreat` — Health in the Austrian Alps: Dispatch from MAYRLIFE by Susan Aurinko
6. `young-dancers-perspective` — A Young Dancer's Perspective by Judy Carmack Bross
7. `garfield-park-pigments` — Pigments! at Garfield Park Conservatory by Sigalit Zetouni
8. `about-the-town` — About the Town in September by Philip Vidal

## Articles

| Slug | Title | Author | HTML | Photos | Notes |
|------|-------|--------|------|--------|-------|
| chicago-innovation | Rallying Chicago's Next Innovators | Judy Carmack Bross | ✅ Full text built | ✅ 11/11 placed | **READY.** Received from Emma Aug 28 (`1a04b5981d924552`) — full text + 11 Gmail attachments. Byline is Judy Carmack Bross, not Emma (she was only forwarding) — confirms the tentative-byline guess was wrong. Also resolves the Huertas name discrepancy: article's own caption reads "Monica Huertas," confirming the filename was correct and Judy's earlier email ("Maria") was the error. |
| murray-bay-part-2 | Only in Murray Bay: Part II | Judy Carmack Bross | ✅ Full text built | ✅ 29/29 placed | **READY.** Cover (`IMG_1776.jpg`) and team photo (`IMG_1149.jpg`) resolved via Judy's Aug 28 cover-photo thread. Name discrepancy in team-photo caption ("Roland" vs. article body's "Raymond" Bouchard) still needs Judy's confirmation before publish. |
| soma-roy | Soma Roy Feature | Annie Delfosse (tentative) | Placeholder | — | Content not yet received. |
| sporting-life | Birthplace of the Olympics Reveals Naked Truth | David A. F. Sweet | ✅ Full text built | ✅ 4/4 placed | **READY.** Forwarded by Judy from David Sweet, Olympia column. |
| silk-roads-health-retreat | Health in the Austrian Alps: Dispatch from MAYRLIFE | Susan Aurinko | ✅ Full text built | ✅ 11/11 placed | **READY.** Received from Emma Aug 28 (`1a04b2da5e5e6b2c`) — full text. Photos arrived as Google Drive links (not Gmail attachments); 10 of 11 downloaded via the Drive connector, the 11th (`photo 9.JPG`, "A Walk Around the Lake") failed repeatedly with a connector session-expired error specific to that one file — John downloaded it manually from the Drive link and it was placed from `~/Downloads`. |
| young-dancers-perspective | A Young Dancer's Perspective | Judy Carmack Bross (tentative) | Placeholder | — | Content not yet received. |
| garfield-park-pigments | Pigments! at Garfield Park Conservatory | Sigalit Zetouni | Placeholder | — | Only a promotional "blast" teaser text + 1 credited image received so far (`IMG_7887.jpeg`); full article text not yet confirmed. |
| about-the-town | About the Town in September | Philip Vidal | ✅ Full text built | ✅ 10/10 placed | **READY.** Via Ana Baca. |
| datebook | DateBook | Annie Delfosse | Copied forward from Aug 23 | — | Text-only (no photos expected). |
| daily-star-august | Astrochart | Victoria Martin | Copied forward from Aug 23 | — | Text-only (no photos expected); verify coverage still extends through end of August. |

## Open items requiring your input

1. **Soma Roy Feature byline is still tentative** (Annie Delfosse) — Judy's lineup lists only "Annie" for this slot, same pattern that turned out wrong for Chicago Innovation (listed as "Emma," actual byline was Judy). Confirm the real byline once content arrives — don't assume Annie is the author just because she's the coordinator.
2. **Roland vs. Raymond Bouchard** — Murray Bay Part 2 team-photo caption discrepancy, carried over from Aug 28 log entry, still unresolved.
3. **Garfield Park Conservatory** — confirm with Sig whether full article text is still coming, separate from the promotional blast already received.
4. **About the Town's slot** — placed last per its traditional end-of-month position since it wasn't in Judy's numbered lineup; flag if she intended a different placement.

## Notes

- Nav chain order (hero → last): chicago-innovation → murray-bay-part-2 → soma-roy → sporting-life → silk-roads-health-retreat → young-dancers-perspective → garfield-park-pigments → about-the-town
- Remaining not-yet-received articles (Soma Roy, Young Dancer's Perspective, Garfield Park/Pigments) have real placeholder stubs (header/nav/byline wired, body text "[Article text coming soon]") so the nav chain and homepage didn't have to wait on content — per prep-edition convention.
- Stub articles use a generic `card-placeholder.jpg`-derived `navthumb.jpg` until real content/photos arrive; swap in a real 70×70 crop of each article's hero photo once built.
- Homepage hero and card teasers for the 3 remaining stub articles read "[Teaser coming]" — replace with real copy once article text is in hand.
- `about.html`'s "Our Writers This Week" section was intentionally left untouched — that's owned by `/edition-checks`, not this prep pass.
