# September 13, 2026 Edition — Status

_Updated: 2026-09-12 (check-emails run)_

**Sept 12 check-emails run:** Sig sent the full "Sweet Memories and Cookies" article text (msg `1a095cd5be91bf39`, to Judy and John), superseding the Sept 8 one-paragraph "Blast." Built into `editions/2026-09-13/chef/index.html` verbatim (two concurrent sessions built this independently with the same result), title updated from working "Chef" to "Sweet Memories and Cookies," homepage card/nav updated to match. Several likely typos carried verbatim, not corrected: "residenece" (residence), "Unanticipately", "hamantachen" (hamantaschen), "cinnamon candle" (probably "cinnamon candy"), "grinded" (ground) — flagging per house rule, not silently fixing. Sig's email says "I'll follow with additional emails that have images and credits" — no such follow-up had arrived as of this check, so the one photo already on disk (`IMG_7976.JPEG`, from the Sept 8 Blast, captioned "NYB Baking Workshop, Chicago, August 9, 2026, Photo: Leo Bommarito") is used as the hero figure, since every article requires one and this photo already carries an explicit credit for exactly this kind of use. John separately replied to Sig confirming receipt and promising to lay it out "as soon as I get home" (msg `1a095d54db5812b7`) — this fulfills that. **6 of 7 articles now Ready** — only The Village remains, still awaiting Annie/Laurel Baer's draft (promised "by noon" Sept 12, not yet received as of this check).

**Local session Sept 12 — laid out all articles with available content.** Using local Gmail credentials (not available to the hourly cloud routine), extracted every pending photo attachment and built out every article that had full text: Puget Sound (22 photos + COVER), Griffin Museum (5 photos), Judith Guest (6 candidate photos, all extracted — hero choice still unresolved, see Blockers), and **Chitchat** (previously just a stub — full 7-page text extracted from Jill Lowe's PDF and built, with all 7 photos placed in the exact order they appear in the source PDF, one photo per page/paragraph, per John's explicit instruction to match the PDF's own layout; visually matched each embedded PDF image to its corresponding downloaded file since filenames didn't hash-match — see photo-to-file mapping in Notes). Also generated real 200&times;200 `navthumb.jpg` thumbnails for all 5 newly-Ready articles (futuresports, puget-sound, chitchat, judith-guest, griffin-museum, plus chef using its one available photo) and rewired every nav-thumb `<img>` in the chain to use them instead of the shared placeholder — `verify_edition.py` now reports zero structural issues. **5 of 7 articles now fully Ready** (up from 1; Judy's confirmed Sept 9 lineup is 7 articles — Pokemon was dropped and is not counted). Chef and The Village remain blocked on content that has not arrived from their contributors — nothing to lay out there without guessing.

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

- **Chitchat** (Jill Lowe) — ✅ **RESOLVED Sept 12.** PDF text extracted (7 pages, "Phatic Communication, or Small Talk — Our Social Lubricant," her "Facts and Froth" column) and built in full. All 7 photos extracted from msg `1a07b81e5713587c` and placed one-per-paragraph in PDF page order (visually matched via embedded-image comparison, since the PDF's re-encoded images don't hash-match the emailed originals). No captions were given for any photo — none invented, per house rule.
- **Puget Sound** (Libbet Richter) — ✅ **RESOLVED Sept 12.** All 22 photos + COVER extracted from msg `1a08bc49f7b39acb` and confirmed matching the already-built HTML's filenames exactly. `verify_edition.py` shows READY.
- **Chef** (Sigalit Zetouni) — ✅ **RESOLVED Sept 12.** Full text received 8:27 AM ET (msg `1a095cd5be91bf39`, "Full text") — "Sweet Memories and Cookies," on the Marcel Proust exhibitions in Paris and the madeleine's evolution into Chicago's Not Your Bubbe's Hamantaschen. Built verbatim (several likely source typos kept as-is, not corrected: "residenece," "Unanticipately," "hamantachen," "cinnamon candle," "grinded"). Sig said she'd follow with "additional emails that have images and credits" — none had arrived as of this check, so the article uses only the one photo already on hand (`IMG_7976.JPEG`, the Aug 8 blast photo) as hero, with its verbatim credit — add more if/when they arrive. John already replied to Sig same morning promising to lay it out "as soon as I get home" (msg `1a095d54db5812b7`) — this fulfills that.
- **The Griffin Museum** (Sydney Armstrong) — ✅ **RESOLVED Sept 12.** All 5 photos extracted from msg `1a093f6b41acc4b2` and confirmed matching the already-built HTML. `verify_edition.py` shows READY. Still open: whether Emma's `cover photo.jpeg` duplicates Judy's `images-1.jpeg` (currently used for the homepage card) — not resolved, low priority since the card already works.
- **Nostalgia and the Village** (Laurel Baer) — via Annie. Not received. (Note: Judy's final list spells it "Laurel Baer", not "Baar" — update if confirmed.) Annie's Sept 12 5:54 AM ET promise of drafts "by noon" checked again in the Sept 12 third-pass `/check-emails` run (EMAIL_LOG.md #89) — still not sent as of that check; only Judy's one-line "Thanks, Annie" courtesy reply had come in. Re-check on the next pass.
- **Judith Guest photos** — ✅ **RESOLVED Sept 12.** All 6 candidate photos extracted. Hero decided: `images-3.jpeg` (a vintage black-and-white author portrait, previously unused) replaces `Unknown.jpeg` as the hero image. Rationale: the book cover (`image2.jpeg`/`9780143139461.jpeg`) and movie poster (`image1 2.jpeg`/`images-4.jpeg`) are already placed inline in the Q&A body next to the relevant questions about the novel and film — promoting either to hero would duplicate it (house rule #30). The vintage portrait was unused, is more dignified than the casual "sweatshirt" snapshot Judy flagged, and fits the "Author Judith Guest" caption. navthumb.jpg regenerated to match.
- **Laurel Baer bio** — needed for about.html; her byline link is dead until it exists.

## Blockers

- ~~Judith Guest hero photo~~ — **RESOLVED Sept 12**, see Pending Deliveries. `images-3.jpeg` (vintage author portrait) now used as hero.
- **Field Museum vs. Griffin Museum** — resolved: Judy's final list says Griffin Museum. No Field Museum article.
- **"Libbet Richter" assumed to be Elizabeth Dunlop Richter** — confirmed pattern; byline points at existing anchor.
- **Laurel Baer bio** — needed for about.html before publish (byline link is dead).
- **October Astrochart not yet requested** from Victoria (`vconst@aol.com`). Current page covers through Sept 30 — needed before Sept 27 edition.
- **Editorial for next week** — Judy asked what John had in mind; reply owed.

## Articles

| Slug | Title | Author | HTML | Photos | Notes |
|------|-------|--------|------|--------|-------|
| futuresports | Chicago-Based FutureSports Brings Novel Concept to Markets | David A. F. Sweet | ✅ Full text built | ✅ 2/2 photos placed with captions | READY. Lead/hero article (Judy's suggestion). Real navthumb.jpg added Sept 12. |
| puget-sound | When Your Lawn Ornament Is an Airplane… | Elizabeth Dunlop Richter | ✅ Full text built | ✅ 22/22 photos + COVER extracted and placed | READY as of Sept 12. Full article arrived Sept 10 (msg `1a08bc49f7b39acb` via Ana). |
| chitchat | Phatic Communication, or Small Talk — Our Social Lubricant | Jill Lowe | ✅ Full text built Sept 12 | ✅ 7/7 photos placed, one per paragraph in PDF page order | READY as of Sept 12. PDF (msg `1a078281b3a3a56d`) + photos (msg `1a07b81e5713587c`) extracted and built same session. "Facts and Froth" column. No captions given for any photo (none invented). Two likely typos carried verbatim from source, not corrected: "Mucho" (probably "Much") and "commmunion" (one instance, elsewhere spelled correctly). |
| judith-guest | Judith Guest on Ordinary People | Scott Holleran | ✅ Full text built | ✅ 6/6 candidate photos extracted | TEXT+PHOTOS READY but **hero choice still open** — see Blockers. Hyperlinks to prior Ordinary People articles already embedded in text. |
| chef | Sweet Memories and Cookies | Sigalit Zetouni | ✅ Full text built Sept 12 | ✅ 1/1 photo (hero, verbatim credit) | READY as of Sept 12. Full text arrived Sept 12 (msg `1a095cd5be91bf39`), superseding the Sept 8 blast. More photos/credits promised by Sig but not yet received; add if they arrive. Slug kept as `chef`. |
| griffin-museum | The Griffin Museum | Sydney Armstrong | ✅ Full text built | ✅ 5/5 photos + card image extracted and placed | READY as of Sept 12. Homepage card uses Judy's Sept 7 cover shot (`images-1.jpeg`). Photos 1-3 captioned and placed inline; `photo 4.jpeg` placed as hero (uncaptioned, positional guess — confirm with Emma/Sydney before publish). |
| the-village | Nostalgia and the Village | Laurel Baer | Placeholder | — | Annie building; promised drafts "by noon" Sept 12, not yet confirmed received. **No `laurel-baer` anchor in about.html** — byline link dead until bio added. |
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
  - ~~Judith Guest hero/cover photo choice~~ — **RESOLVED Sept 12** by John's editorial call: `images-3.jpeg` (vintage author portrait, previously unused) is now the hero, avoiding duplication with the book cover and movie poster already placed inline in the Q&A body.
  - **Judith Guest photo extraction** — files must be manually downloaded from Gmail. Two source messages now: `1a082daaf4739c9d` (original 3: Unknown.jpeg, image2.jpeg, "image1 2.jpeg") and `1a087fd2c8446918` (adds images-3.jpeg, 9780143139461.jpeg, images-4.jpeg). All 6 still need manual extraction and placement in `editions/2026-09-13/judith-guest/`.
  - ~~Sigalit/chef full article~~ — **RESOLVED Sept 12**, see Pending Deliveries. Built as "Sweet Memories and Cookies." Additional photos/credits Sig promised may still arrive; add them if so.
  - **Laurel Baer bio** — needed for about.html before publish, or the byline link 404s. (Note spelling: Judy's final list says "Baer", earlier drafts had "Baar".)
  - **Judy's own article** — "I may be writing an article but will let you know." No folder created.
  - **Editorial for next week** — Judy asked "John, I think you had an idea about an Editorial for next week?" Reply owed; Editor's Page content, not a nav-chain article.
  - **October Astrochart** — not yet requested from Victoria (`vconst@aol.com`).
  - **Griffin Museum `photo 4.jpeg` role** — placed as the uncaptioned hero on positional grounds only (it's the one photo in Emma's Sept 12 email with no caption, sitting right before the lead paragraph). Confirm with Emma/Sydney that this is correct before publishing.
  - **Griffin Museum `cover photo.jpeg` vs. `images-1.jpeg`** — Emma's Sept 12 package includes its own `cover photo.jpeg`; the homepage card is currently wired to Judy's earlier `images-1.jpeg` (Sept 7). Not confirmed whether these are the same image or Emma's should replace it once extracted.
  - **Griffin Museum text artifact** — "which can brought to the school's location" carried verbatim from Emma's email; likely missing "be" but not corrected (flagging per house rule against silent spelling/grammar fixes).
