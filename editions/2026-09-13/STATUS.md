# September 13, 2026 Edition — Status

_Updated: 2026-09-12_

**Sept 12 email check (cutoff after Sept 11, per item #85):** Emma sent Sydney Armstrong's full Griffin Museum article text, 12:53 AM ET (msg `1a093f6b41acc4b2`, to John cc Judy). Full text built into `editions/2026-09-13/griffin-museum/index.html`. Five photo attachments: `cover photo.jpeg`, `Photo 1.jpeg`, `Photo 2.jpeg`, `Photo 3.jpeg`, `photo 4.jpeg` (exact filenames/case as sent — do not rename). Photos 1-3 have explicit verbatim captions in the email text and are placed inline at their indicated paragraphs. Homepage card wired to Judy's already-extracted Sept 7 cover shot (`images-1.jpeg`, msg `1a07c5bcbb70d346`), which was sitting unused in the folder. **Two open ambiguities, not decided here:** (1) `photo 4.jpeg` appears with no caption immediately before the lead paragraph — the position every other article uses for its hero figure, so it's been placed as the (uncaptioned) hero `<figure>` on that positional basis only, but confirm with Emma/Sydney this is correct, since it's the one photo without any caption or instruction. (2) Emma's `cover photo.jpeg` may duplicate or be meant to replace Judy's `images-1.jpeg` now used as the card image — not resolved. None of the 5 new photo files have been extracted from Gmail (no local Gmail credentials in this sandbox); all show as broken images in `verify_edition.py` until manually downloaded. One verbatim text artifact carried over from Emma's email, not corrected: "which can brought to the school's location" (likely missing "be" — flagged, not silently fixed). Homepage teaser card updated with real copy (was "Coming in the September 13 edition."). 3 of 8 slots now text-built pending photos (Puget Sound, Judith Guest, Griffin Museum); Chitchat, Chef, and The Village remain stubs.

**Final lineup received from Judy (Sept 9, msg `1a085c9a5a289b3e`).** Nav chain updated. Judith Guest article built (text + 3 photos referenced; photo files pending extraction from Gmail). Pokemon dropped from lineup. 2 of 8 slots Ready (FutureSports); 1 text-built pending photos (Puget Sound, Judith Guest); 4 are stubs; chef/sig has blast text only.

**Sept 10 email check:** Chitchat PDF arrived Sept 6 (msg `1a078281b3a3a56d`, attached to original email); photos arrived Sept 7 (msg `1a07b81e5713587c`, 7 attachments: shutterstock_2039784620.jpeg, shutterstock_2779946955.jpeg, shutterstock_2660425777.jpeg, Screenshot 2026-09-05 at 16.51.53.png, Screenshot 2026-09-04 at 13.40.54.png, shutterstock_2537796621.jpeg, shutterstock_2758830333.jpeg). Cannot auto-extract (no local Gmail credentials); needs manual download. Two cover photo candidates for The Village sent by Judy to Annie+John: `TVC 7.jpeg` (msg `1a08b051c167e9e1`) and `collage for 2026 Benefit.png` (msg `1a08b042b7348975`). Sigalit/chef: blast text only, no full article yet.

**Sept 11 email check:** Puget Sound full article + 22 photos arrived from Ana (msg `1a08bc49f7b39acb`, sent Sept 10). HTML built with all 22 inline photos and captions per Ana's placement markers. Photo files need downloading from Gmail (22 attachments + COVER). Title: "When Your Lawn Ornament Is an Airplane…". One minor text artifact: "o]er" in "his uncle's 2001 o]er to sell him" — rendered as "offer" (clear PDF/encoding corruption, not contributor's spelling). Judy asked about name correction in Jafra article (Hanan→Hamed, Sept 10 msg `1a08b3cf024db009`) — already fixed in prior session (commit 91c624f). Cover photo candidates for The Village: `TVC 7.jpeg` confirmed from Judy (msg `1a08b051c167e9e1`); article text still not received from Annie/Laurel Baer.

**check-emails run, Sept 11 (cutoff after Sept 9):** New tier1 mail: Ana's Puget Sound package (`1a08bc49f7b39acb`, already covered above); a Judy/Jill exchange reconfirming Chitchat's photos were sent to John (`1a0880ad7df9e1d7`, `1a08846c39c82f7d` — no new attachments, same PDF re-sent); a courtesy Editors Dashboard feedback thread from Judy (`1a08b60d7b996f9b`, `1a08ff59a92331f2`) restating the open "Editorial Comment for this week?" question and confirming she resent Judith Guest's photos; and — the one substantive new item — **Judy's Sept 9 9:04pm follow-up on the Judith Guest article** (`1a087fd2c8446918`) with 3 new candidate photos (`images-3.jpeg`, `9780143139461.jpeg` — the Penguin 50th-anniversary book cover, `images-4.jpeg` — a movie-poster frame) on top of the original 3 already referenced in the built HTML. Judy raises an unresolved editorial question there: is the current hero photo (`Unknown.jpeg`, the "sweatshirt" photo) good enough, should the book-cover shot replace it, and should the movie-poster-frame photos be dropped — she asks "Should I look for other photos?" rather than deciding. **Not acted on** — this is an open photo-selection call for John, and none of the 6 Judith Guest photo files (original 3 or new 3) have been extracted from Gmail yet in any session. See EMAIL_LOG.md items 76-83 for full detail.

**check-emails run, Sept 11 (second pass, same day):** Re-swept tier1/tier2 with cutoff after the last processed message (Sept 10). One new message: Judy's 11:34 PM `1a092d305c2689f5`, worried the Editors Dashboard isn't reflecting incoming material (cites Jill Lowe's Chitchat materials and her own Judith Guest photo resend) — no new content, both items already tracked above and in EMAIL_LOG.md item #85; this is dashboard-tool feedback, not an edition request. Targeted search for Jill Lowe/Emma/Scott Holleran/Sydney Armstrong/Laurel Baer/Griffin Museum/Village confirmed nothing new has arrived — Chitchat, Griffin Museum, chef, and The Village remain exactly as above. No dev2 changes this pass.

## Judy's final lineup (Sept 9, msg `1a085c9a5a289b3e`)

Nav chain order (hero → last):
1. `futuresports` — Chicago-Based FutureSports Brings Novel Concept to Markets, by David A. F. Sweet (lead/hero, Judy's suggestion)
2. `puget-sound` — Puget Sound, by Elizabeth Dunlop Richter
3. `chitchat` — Chitchat, by Jill Lowe
4. `judith-guest` — Judith Guest on Ordinary People, by Scott Holleran (NEW — article + 3 photos arrived Sept 8)
5. `chef` — Chef/NYB Hamantaschen, by Sigalit Zetouni
6. `griffin-museum` — The Griffin Museum, by Sydney Armstrong
7. `the-village` — Nostalgia and the Village, by Laurel Baer
`pokemon` — DROPPED from lineup (Jackson LeJeune not in Judy's final list)

DateBook (Annie) is copied forward and linked from the nav bar, not part of the article chain — same as every prior edition.

What the Sept 7 changes email moved: Pokemon from Annie to Emma; David Sweet's story from Emma to John (already delivered and built); Griffin Museum added to Emma with "we should go ahead and do this week"; The Village (Laurel Baar) added to Annie alongside DateBook.

## Lineup

| Order | Slug | Title | Author | Coordinator |
|---|---|---|---|---|
| 1 | futuresports | Chicago-Based FutureSports Brings Novel Concept to Markets | David A. F. Sweet | Judy to John |
| 2 | puget-sound | Puget Sound | Elizabeth Dunlop Richter | Ana |
| 3 | chitchat | Chitchat | Jill Lowe | Judy to John |
| 4 | judith-guest | Judith Guest on Ordinary People | Scott Holleran | Judy to John |
| 5 | chef | NYB Hamantaschen (working title) | Sigalit Zetouni | Sig to John |
| 6 | griffin-museum | The Griffin Museum | Sydney Armstrong | Emma |
| 7 | the-village | Nostalgia and the Village | Laurel Baer | Annie |
| — | pokemon | (dropped) | Jackson LeJeune | — |

## Pending Deliveries

- **Chitchat** (Jill Lowe) — PDF article arrived Sept 6 (msg `1a078281b3a3a56d`); 7 photos arrived Sept 7 (msg `1a07b81e5713587c`). Needs manual extraction from Gmail (no local credentials in remote session). Manually download PDF + photos → build article.
- **Puget Sound** (Libbet Richter) — ✅ Full article received Sept 10 (msg `1a08bc49f7b39acb`). HTML built. **Photo files still need manual extraction** from Gmail (22 attachments + COVER; message id `1a08bc49f7b39acb`, from anabaca8@gmail.com).
- **Chef** (Sigalit Zetouni) — Blast text received Sept 8 (msg `1a08369f62e68b76`): one paragraph about NYB hamantaschen/Jacob Shaw. Full article not yet received; placeholder still in place.
- **The Griffin Museum** (Sydney Armstrong) — ✅ Full article received Sept 12 (msg `1a093f6b41acc4b2` via Emma). HTML built. Homepage card now uses Judy's already-extracted cover shot (`images-1.jpeg`, from msg `1a07c5bcbb70d346`, Sept 7) — a museum exterior photo, no caption, so per house rule #27 it's card-only and not duplicated in the article body. **5 more photo files from Emma's Sept 12 email still need manual extraction** from Gmail (`cover photo.jpeg`, `Photo 1.jpeg`, `Photo 2.jpeg`, `Photo 3.jpeg`, `photo 4.jpeg`; message id `1a093f6b41acc4b2`, from muhlemane2@gmail.com). Unclear whether Emma's `cover photo.jpeg` duplicates or replaces Judy's `images-1.jpeg` — not resolved here.
- **Nostalgia and the Village** (Laurel Baer) — via Annie. Not received. (Note: Judy's final list spells it "Laurel Baer", not "Baar" — update if confirmed.)
- **Judith Guest photos** — 3 photo attachments in msg `1a082daaf4739c9d` (Unknown.jpeg, image2.jpeg, image1 2.jpeg). HTML references them correctly but files not yet extracted from Gmail (no local Gmail credentials). Needs manual extraction. Placement of image2.jpeg and "image1 2.jpeg" estimated (no explicit placement instructions given).
- **Laurel Baer bio** — needed for about.html; her byline link is dead until it exists.

## Blockers

- **Judith Guest photo files missing** — Need manual extraction from Gmail msg `1a082daaf4739c9d` (attachments: Unknown.jpeg, image2.jpeg, "image1 2.jpeg"). Article HTML is built and correct but will show broken images until files are downloaded.
- **Field Museum vs. Griffin Museum** — resolved: Judy's final list says Griffin Museum. No Field Museum article.
- **"Libbet Richter" assumed to be Elizabeth Dunlop Richter** — confirmed pattern; byline points at existing anchor.
- **Laurel Baer bio** — needed for about.html before publish (byline link is dead).
- **October Astrochart not yet requested** from Victoria (`vconst@aol.com`). Current page covers through Sept 30 — needed before Sept 27 edition.
- **Editorial for next week** — Judy asked what John had in mind; reply owed.

## Articles

| Slug | Title | Author | HTML | Photos | Notes |
|------|-------|--------|------|--------|-------|
| futuresports | Chicago-Based FutureSports Brings Novel Concept to Markets | David A. F. Sweet | ✅ Full text built | ✅ 2/2 photos placed with captions | READY. Lead/hero article (Judy's suggestion). |
| puget-sound | When Your Lawn Ornament Is an Airplane… | Elizabeth Dunlop Richter | ✅ Full text built | ⚠ 22 photos referenced but files not extracted | Full article arrived Sept 10 (msg `1a08bc49f7b39acb` via Ana). 22 inline figures + COVER card image. Photo files need manual Gmail extraction. |
| chitchat | Chitchat | Jill Lowe | Placeholder | — | PDF arrived msg `1a078281b3a3a56d`; 7 photos arrived msg `1a07b81e5713587c`. Needs manual extraction. |
| judith-guest | Judith Guest on Ordinary People | Scott Holleran | ✅ Full text built | ⚠ 3 photos referenced but files not extracted | Article arrived Sept 8 (msg `1a082daaf4739c9d`). Text is complete. Photos: Unknown.jpeg (hero, "Author Judith Guest"), image2.jpeg, image1 2.jpeg — files need manual Gmail extraction. Hyperlinks to prior Ordinary People articles already embedded in text. |
| chef | NYB Hamantaschen / Chef | Sigalit Zetouni | Placeholder (blast text only) | — | Sig sent 1-paragraph blast Sept 8 (msg `1a08369f62e68b76`). Full article not received. Slug may change once real title arrives. |
| griffin-museum | The Griffin Museum | Sydney Armstrong | ✅ Full text built | ⚠ Card image live (`images-1.jpeg`); 5 body/hero photos referenced but files not extracted | Full article arrived Sept 12 (msg `1a093f6b41acc4b2` via Emma). Homepage card now uses Judy's Sept 7 cover shot. Photos 1-3 captioned and placed inline; `photo 4.jpeg` placed as hero (uncaptioned, positional guess — confirm); Emma's `cover photo.jpeg` not used (unclear if duplicate of `images-1.jpeg`). 5 files still need manual Gmail extraction. |
| the-village | Nostalgia and the Village | Laurel Baer | Placeholder | — | Annie building. **No `laurel-baer` anchor in about.html** — byline link dead until bio added. |
| pokemon | (dropped) | Jackson LeJeune | Placeholder | — | Removed from Judy's final Sept 9 lineup. Folder retained but not linked in nav chain. |
| datebook | DateBook | Annie Delfosse | Copied forward from Sept 6; title and kicker updated to Sept 13 | — | — |
| daily-star-september | Astrochart | Victoria Martin | Copied forward; Sept 1–12 stripped | — | Covers Sept 13–30. October content needed before Sept 27 edition. |

## Notes

- Nav chain (hero → last): **futuresports** → puget-sound → chitchat → judith-guest → chef → griffin-museum → **the-village**. First article's Previous and last article's Next both point at the root homepage. Pokemon is disconnected from chain.
- Nav thumbnails across the edition use the shared `thumb-placeholder.jpg` at the edition root — replace with real navthumbs as covers arrive. `verify_edition.py` flags the resulting "duplicate image used 2×" on futuresports; that's the known harmless placeholder pattern, same as Sept 6.
- Homepage hero is `chitchat` with a placeholder card image and a neutral teaser. Every stub card carries "Coming in the September 13 edition." rather than invented copy — replace each teaser as real content lands.
- Categories on the stubs (Society, Travel, Dining, Arts, Community, Culture) are provisional guesses from the working titles, not Judy's assignments.

- **Open questions / decisions needed:**
  - **Judith Guest photo placement** — image2.jpeg and image1 2.jpeg placed by editorial judgment (after intro para and mid-Q&A). Confirm with Judy or Scott if specific placement required.
  - **Judith Guest hero/cover photo choice (new, Sept 9 msg `1a087fd2c8446918`)** — Judy isn't sure the current hero photo (`Unknown.jpeg`, the "sweatshirt" photo) is good, suggests the Penguin 50th-anniversary book cover (`9780143139461.jpeg`) might work better as the lead image, and questions whether the movie-poster-frame photo (`images-4.jpeg`) should be used at all. She asked John to decide / look for more photos rather than deciding herself. **Do not change the hero image until John decides.**
  - **Judith Guest photo extraction** — files must be manually downloaded from Gmail. Two source messages now: `1a082daaf4739c9d` (original 3: Unknown.jpeg, image2.jpeg, "image1 2.jpeg") and `1a087fd2c8446918` (adds images-3.jpeg, 9780143139461.jpeg, images-4.jpeg). All 6 still need manual extraction and placement in `editions/2026-09-13/judith-guest/`.
  - **Sigalit/chef full article** — only blast text (1 paragraph) received. Full article still needed. Slug may change once title is confirmed.
  - **Laurel Baer bio** — needed for about.html before publish, or the byline link 404s. (Note spelling: Judy's final list says "Baer", earlier drafts had "Baar".)
  - **Judy's own article** — "I may be writing an article but will let you know." No folder created.
  - **Editorial for next week** — Judy asked "John, I think you had an idea about an Editorial for next week?" Reply owed; Editor's Page content, not a nav-chain article.
  - **October Astrochart** — not yet requested from Victoria (`vconst@aol.com`).
  - **Griffin Museum `photo 4.jpeg` role** — placed as the uncaptioned hero on positional grounds only (it's the one photo in Emma's Sept 12 email with no caption, sitting right before the lead paragraph). Confirm with Emma/Sydney that this is correct before publishing.
  - **Griffin Museum `cover photo.jpeg` vs. `images-1.jpeg`** — Emma's Sept 12 package includes its own `cover photo.jpeg`; the homepage card is currently wired to Judy's earlier `images-1.jpeg` (Sept 7). Not confirmed whether these are the same image or Emma's should replace it once extracted.
  - **Griffin Museum text artifact** — "which can brought to the school's location" carried verbatim from Emma's email; likely missing "be" but not corrected (flagging per house rule against silent spelling/grammar fixes).
