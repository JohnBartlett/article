# September 27, 2026 Edition — Status

_Updated: 2026-09-26_

Skeleton prepped Sept 24 against Judy's finalized lineup. All 9 stubs exist (7 original + 2 added Sept 25) and the nav chain is wired. Two articles are received but not yet built (Amouze Mousse, Deerpath), one is already built (Jean Colonomos), and four are still with coordinators. Stories are due to John by Friday night, Sept 25.

## Judy's official lineup (`1a0bea8adf366799`, received 2026-09-20; finalized `1a0d2ee0111aa0a8`, 2026-09-24)

Nav chain order (hero → last):
1. `amouze-mousse` — Margaret Unetich and Matt Ziol Create Amouze Mousse by Judy Carmack Bross
2. `this-day-in-history` — This Day in History by Scott Holleran
3. `silk-roads-scarves` — My Silk Roads by Susan Aurinko
4. `dusty-sang` — American Echoes: A New Book by Dusty Sang by Judy Carmack Bross
5. `deerpath-golf` — No Matter How You Slice It, Deerpath Golf Course Remains a Lake Forest Treasure at 100 by David A. F. Sweet
6. `jean-colonomos-poems` — Two Poems by Jean Colonomos
7. `dumpling-fest` — Dumpling Fest by Elizabeth Dunlop Richter
8. `lejeune-film-review` — Film Review by Jackson LeJeune (added Sept 25, `1a0d89a6f719d921`)
9. `ravinia-school-lawndale` — The Ravinia School in Lawndale by Drake Boehm (added Sept 25, `1a0d89a6f719d921`)

Judy also asked that the October Heritage Auctions ad "run in this issue and all month" — already on dev2's homepage.

## Lineup

| Order | Slug | Title | Author | Coordinator |
|---|---|---|---|---|
| 1 | amouze-mousse | Margaret Unetich and Matt Ziol Create Amouze Mousse | Judy Carmack Bross | Ana Baca |
| 2 | this-day-in-history | This Day in History | Scott Holleran | Annie Delfosse |
| 3 | silk-roads-scarves | My Silk Roads | Susan Aurinko | Emma Muhleman |
| 4 | dusty-sang | American Echoes: A New Book by Dusty Sang | Judy Carmack Bross | Annie Delfosse |
| 5 | deerpath-golf | No Matter How You Slice It, Deerpath Golf Course Remains a Lake Forest Treasure at 100 | David A. F. Sweet | Judy to John |
| 6 | jean-colonomos-poems | Two Poems | Jean Colonomos | Judy to John |
| 7 | dumpling-fest | Dumpling Fest | Elizabeth Dunlop Richter | Emma Muhleman |
| 8 | lejeune-film-review | Film Review | Jackson LeJeune | Judy to John |
| 9 | ravinia-school-lawndale | The Ravinia School in Lawndale | Drake Boehm | Judy to John |

## Pending Deliveries

- **Dumpling Fest photos 16-21** (Elizabeth Dunlop Richter) — corrupted in Emma's copy; Judy is asking Libbet to resend (`1a0dda74a609e3e3`). Text and photos 1-15 are in hand.

## Blockers

- **Six articles received but not yet built:** This Date in History, Dusty Sang, My Silk Roads, Dumpling Fest (text only; photos 16-21 missing), Jack's Vampires review, Drake's Ravinia piece. Source messages are in EMAIL_LOG.md items #246-#252.
- **Titles to change when building** (mistake #61): `this-day-in-history` → "This Date in History"; `dusty-sang` → "Dusty Sang: Echoes from America's Past"; `lejeune-film-review` → "The Vampires of New Orleans – An Indie Editing Accomplishment".
- **Dumpling Fest text must come from Libbet's PDF, not Emma's email** — Emma's copy has PDF ligature damage ("oLering", "organiza(ons", etc.).
- **This Date in History photos are low-resolution** (two ~210x320 px, two ~474 px wide) and photos 4-5 have no real captions.
- **Drake Boehm's bio says "Classics Chicago"** — placed verbatim; flag to Judy.
- **Heritage October ad + Erika Dufour credit** — both on dev2; reach production with this edition's `/stage` + `/publish`, or a hotfix.

## Articles

| Slug | Title | Author | HTML | Photos | Notes |
|------|-------|--------|------|--------|-------|
| amouze-mousse | Margaret Unetich and Matt Ziol Create Amouze Mousse | Judy Carmack Bross | Ready | 14/14 + cover | Source `1a0d486111ef2168` (Ana, Sept 24). Files in `_attachment-staging/1a0d486111ef2168/`. Photos 9+10 and 13+14 are side-by-side pairs with shared captions; photo 8 has no caption; COVER is homepage-card only. |
| this-day-in-history | This Day in History | Scott Holleran | Placeholder | — | Awaiting text from Annie. Covers: `1a0d2ea6532b35c9`, `1a0d2eb7fba723f8`. |
| silk-roads-scarves | My Silk Roads | Susan Aurinko | Placeholder | — | Awaiting Emma. Slug/title are working names; the column's real headline comes with the text. |
| dusty-sang | American Echoes: A New Book by Dusty Sang | Judy Carmack Bross | Placeholder | cover only | Cover `1a0c60b2f6517021` / resent `1a0d2ef3b97a908d`; Judy: "Also use at top of page" (cover + hero). |
| deerpath-golf | No Matter How You Slice It, Deerpath Golf Course Remains a Lake Forest Treasure at 100 | David A. F. Sweet | Ready | 2/2 | Source `1a0c3a5f9e688f14` (Judy fwd, Sept 21). Third cover candidate `1a0d2f06c1b52abd`. |
| jean-colonomos-poems | Two Poems | Jean Colonomos | Ready | 2/2 | Moved from `editions/2026-09-20/` (held there Sept 18). Byline date and nav updated. |
| dumpling-fest | Dumpling Fest | Elizabeth Dunlop Richter | Placeholder | cover only | Source PDF `1a0c46e603a9b2c3`; cover `1a0c615cd806fce8`. Working title. |
| lejeune-film-review | Film Review | Jackson LeJeune | Placeholder | cover staged | Added Sept 25 at Judy's request (`1a0d89a6f719d921`), approved by John. Working title until Jack's text arrives. |
| ravinia-school-lawndale | The Ravinia School in Lawndale | Drake Boehm | Placeholder | — | Added Sept 25 at Judy's request, approved by John. New author, no bio yet. |
| datebook | DateBook | Annie Delfosse | Copied | — | From Sept 20; title/kicker updated. |
| daily-star-september | Astrochart | Victoria Martin | Copied | — | Sept 20–26 removed; runs Sept 27–30 only. |

## Notes

- Nav chain order (hero → last): amouze-mousse → this-day-in-history → silk-roads-scarves → dusty-sang → deerpath-golf → jean-colonomos-poems → dumpling-fest → lejeune-film-review → ravinia-school-lawndale.
- Categories are working choices, following each author's earlier pieces where there are any: Aurinko "My Silk Roads", Holleran "Chicago History", Sweet "The Sporting Life".
- Found and fixed during prep: the Astrochart nav link in 6 Sept 20 articles, Jean Colonomos's page, and Sept 13's `pokemon` pointed at the unfilled template placeholder `../daily-star-MONTH/` (live on production as a soft 404 that loads the homepage). Fixed on dev2; reaches production with this edition's publish unless hotfixed sooner.
- Automation (hourly email routine, attachment fetcher, dashboard refresh) was paused Sept 24 for this manual build; the editors dashboard will not show this file until the refresh workflow is re-enabled.
- Held for Oct 4: Francesco Bianchini / Drake Boehm (Emma), Sig's Ann Dunham Water Terrace piece.
