# September 13, 2026 Edition — Status

_Updated: 2026-09-08_

**Skeleton prepped Sept 8 against a DRAFT lineup.** Judy's Sept 7 "Assignment changes" email says the final September 13 lineup is still coming ("I will send the final line up of the articles for September 13 by tomorrow"), so slugs, order, and even which articles run should be expected to move. 1 of 7 articles (FutureSports) is already Ready; the other 6 are placeholder stubs with the nav chain wired end to end. DateBook and Astrochart copied forward from Sept 6.

## Judy's lineup (draft `1a0769af43807d60`, received 2026-09-06; changes `1a07bb63d85bb921`, 2026-09-07)

Nav chain order (hero → last) — **provisional, pending Judy's final list**:
1. `chitchat` — Chitchat, by Jill Lowe
2. `puget-sound` — Puget Sound, by Elizabeth "Libbet" Dunlop Richter
3. `chef` — Chef, by Sigalit Zetouni
4. `futuresports` — Chicago-Based FutureSports Brings Novel Concept to Markets, by David A. F. Sweet
5. `griffin-museum` — The Griffin Museum, by Sydney Armstrong
6. `the-village` — The Village, by Laurel Baar
7. `pokemon` — Pokemon, by Jackson LeJeune

DateBook (Annie) is copied forward and linked from the nav bar, not part of the article chain — same as every prior edition.

What the Sept 7 changes email moved: Pokemon from Annie to Emma; David Sweet's story from Emma to John (already delivered and built); Griffin Museum added to Emma with "we should go ahead and do this week"; The Village (Laurel Baar) added to Annie alongside DateBook.

## Articles

| Slug | Title | Author | HTML | Photos | Notes |
|------|-------|--------|------|--------|-------|
| chitchat | Chitchat | Jill Lowe | Placeholder | — | Judy sends directly to John. Working title from her list. |
| puget-sound | Puget Sound | Elizabeth Dunlop Richter | Placeholder | — | Ana coordinating. Judy's list says "Libbet Richter" — byline points at the existing `elizabeth-dunlop-richter` anchor on the assumption it's the same writer; confirm. |
| chef | Chef | Sigalit Zetouni | Placeholder | — | The piece delayed from Sept 6 (Sig, Sept 2, msg `1a0647a40f159cf9`). Slug will change once the real title arrives. |
| futuresports | Chicago-Based FutureSports Brings Novel Concept to Markets | David A. F. Sweet | ✅ Full text built | ✅ 2/2 photos placed with captions | Received from Judy Sept 7 (msg `1a07bab4b14a0595`) with captions in placement order. Verifies READY. |
| griffin-museum | The Griffin Museum | Sydney Armstrong | Placeholder | — | Emma building; Judy sent the cover shot to Emma Sept 7 (msg `1a07c5bcbb70d346`). See the Field/Griffin ambiguity below. |
| the-village | The Village | Laurel Baar | Placeholder | — | Annie building. **New author — no `laurel-baar` anchor in about.html**, so the byline link is dead until a bio is added. |
| pokemon | Pokemon | Jackson LeJeune | Placeholder | — | Emma building (reassigned from Annie Sept 7). Judy's list says only "Jackson"; matched to the existing `jackson-lejeune` anchor. |
| datebook | DateBook | Annie Delfosse | Copied forward from Sept 6; title and kicker updated to Sept 13 | — | Internal Astrochart link already points at `../daily-star-september/`, correct for this edition. |
| daily-star-september | Astrochart | Victoria Martin | Copied forward from Sept 6; Sept 1–12 sections and dropdown options stripped per mistake #21 | — | Now covers Sept 13–30. **October content will be needed before the Sept 27 edition** — Victoria (`vconst@aol.com`) has not been asked yet. |

## Notes

- Nav chain (hero → last): **chitchat** → puget-sound → chef → futuresports → griffin-museum → the-village → **pokemon**. First article's Previous and last article's Next both point at the root homepage.
- Nav thumbnails across the edition use the shared `thumb-placeholder.jpg` at the edition root — replace with real navthumbs as covers arrive. `verify_edition.py` flags the resulting "duplicate image used 2×" on futuresports; that's the known harmless placeholder pattern, same as Sept 6.
- Homepage hero is `chitchat` with a placeholder card image and a neutral teaser. Every stub card carries "Coming in the September 13 edition." rather than invented copy — replace each teaser as real content lands.
- Categories on the stubs (Society, Travel, Dining, Arts, Community, Culture) are provisional guesses from the working titles, not Judy's assignments.

- **Open questions / decisions needed:**
  - **Final lineup.** Judy promised it Sept 8. Everything here is built against the Sept 6 draft plus the Sept 7 changes.
  - **Field Museum vs. Griffin Museum.** The draft list says "Field Museum by Sydney"; the changes email and the cover-shot email both say Griffin Museum. Treated as one article (Griffin) — confirm Field Museum isn't a separate piece that also needs a slot. This was already flagged as unresolved in the Sept 6 prep notes.
  - **Laurel Baar bio** — needed for about.html before publish, or the byline link 404s.
  - **"Libbet Richter" = Elizabeth Dunlop Richter?** — assumed, not confirmed.
  - **Judy's own article** — "I may be writing an article but will let you know." No folder created.
  - **Editorial for next week** — Judy asked "John, I think you had an idea about an Editorial for next week?" Reply owed; Editor's Page content, not a nav-chain article.
  - **October Astrochart** — not yet requested from Victoria.
