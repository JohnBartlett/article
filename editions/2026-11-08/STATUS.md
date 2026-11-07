# November 8, 2026 Edition — Status

_Updated: 2026-11-06_

Skeleton prepped Nov 5: seven stubs, DateBook and Astrochart copied from Nov 1, homepage pointed at Nov 8. Five pieces are fully in hand (Cultural Stadium, Silent Film, David Sweet, Jill Lowe, Jackson LeJeune); two are waiting on text (Prentice, Gold Coast).

## Judy's official lineup (`1a1a31e81f7e8e1b`, received 2026-11-03, "Just 7 articles")

Supersedes `1a196d8e74bedf93` (Nov 1) and `1a19d68884379d88` (Nov 2). Francesco Bianchini's Argentina piece held to next week.

Nav chain order (hero → last):
1. `friends-of-prentice` — Friends of Prentice Celebrates 40 Years of Women's Healthcare by Judy Carmack Bross
2. `chicago-cultural-stadium` — Chicago Cultural Stadium by Judy Carmack Bross
3. `goddesses-silent-film` — Goddesses in the Machine: Silent Film Fashion by Drew Björkstén
4. `gold-coast-fashion-show` — Gold Coast Fashion Show by Judy Carmack Bross
5. `david-sweet-yd3` — New Business Poised to Guide Student-Athletes to Best Division III Choices by David A. F. Sweet
6. `jill-lowe-ice-cream` — Where to Get It by Jill Lowe
7. `lejeune-wildwood` — Wildwood Review: A Spectacular Visual Feast by Jackson LeJeune

## Lineup

| Order | Slug | Title | Author | Coordinator |
|---|---|---|---|---|
| 1 | friends-of-prentice | Friends of Prentice Celebrates 40 Years of Women's Healthcare | Judy Carmack Bross | Annie |
| 2 | chicago-cultural-stadium | Chicago Cultural Stadium | Judy Carmack Bross | Ana (editing) |
| 3 | goddesses-silent-film | Goddesses in the Machine: Silent Film Fashion | Drew Björkstén | Ana |
| 4 | gold-coast-fashion-show | Gold Coast Fashion Show | Judy Carmack Bross | Emma |
| 5 | david-sweet-yd3 | New Business Poised to Guide Student-Athletes to Best Division III Choices | David A. F. Sweet | Judy to John |
| 6 | jill-lowe-ice-cream | Where to Get It | Jill Lowe | Jill to John |
| 7 | lejeune-wildwood | Wildwood Review: A Spectacular Visual Feast | Jackson LeJeune | Judy to John |

## Build — 2026-11-07

All seven articles built with photos (`fc71e865`); verify_edition 7 Ready, edition_checks clean, content_audit 2 expected flags. Local Gmail token renewed Nov 7 (OAuth consent in Chrome on the Mac, John's OK). Titles taken from the sources (#61): Prentice, Cultural Stadium and Gold Coast changed from working titles.

## Pending Deliveries

- None for the seven articles.

## Blockers

- **Fabrizio's Physical Media Fair piece:** Nov 8 (as an eighth article) or Nov 15? Judy's Nov 6 email and her Nov 3 list of seven disagree. Asked Judy Nov 7 (`1a1b6a1e94108976`, #546), with the typo and small-photo questions.
- **Small photos (#80):** Cultural Stadium `1 Donna Lasinski.jpeg` (387 px) and `2 Koi Pond.jpeg` (241 px); Prentice photos 4, 8 and 10 (416 px, from Annie's layout); Silent Film `5 Gish.jpg` (820 px). Built as sent; ask for larger files if Judy wants them replaced.
- **Jill's photos** come only from her PDF (no originals sent), saved as `peach-000.jpg` … `peach-006.png`.
- **Jackson's "Woods People" image** is on a Drive link not shared with John; the copy in the build comes from his PDF.

## Layout calls to confirm

- David Sweet sent captions but no placement: Jennifer and Caleb at the top, the logo after the yd3.org paragraph, the Jennifer website photo mid-article.
- Prentice category changed from the stub's "Architecture" to "Society"; homepage hero uses Judy's cover `mq-fop40thanniversarypreviews-106.jpeg` (Annie's photo 8 is a smaller copy of it, kept in the body).
- Wildwood homepage card uses the poster (not in Jackson's PDF layout).

## Source text to flag to Judy (left verbatim, #18)

- Silent Film: "Bard GraduateCenter", "Here,“Two Gun Betty”", "which we have implied it its title".
- Sweet: "Kenyon University" (Kenyon College?).
- Gold Coast: "complex fetal condition."
- Wildwood: "only serves to bolsters", and the fragment "Fairy tales, especially the Brothers’ Grimm “original” fairy tale canon."
- Jill: "Delaware Food and Liqor" (the sign in her photo reads LIQUOR).

## Articles

| Slug | Title | Author | HTML | Photos | Notes |
|------|-------|--------|------|--------|-------|
| friends-of-prentice | Friends of Prentice | To confirm | Placeholder | Cover only | Cover `mq-fop40thanniversarypreviews-106.jpeg` (`1a1a335b0abdf363`); caption "Board Member Shannon Flavin, Executive Director Kristen E. Field" (`1a1a2c9202d75b15`) |
| chicago-cultural-stadium | Chicago's Cultural Stadium: Falling in Love With Chicago All Over Again | Judy Carmack Bross | Placeholder | In email | Ana `1a1adb43367db1f9`: text, `COVER Cultural Stadium.jpeg` (same image as Judy's `7+Arttists+7+Streets+4.jpeg`, fingerprint 0) + photos 1-3 with captions |
| goddesses-silent-film | Goddesses in the Machine: Silent Film Fashion | Drew Björkstén | Placeholder | In email | Ana `1a1acbec25d30f9d`: text with links, `COVER Goddess.jpeg` + photos 1-6 with captions. Bio `1a1a1d6558f89c71` (added to about.html) |
| gold-coast-fashion-show | Gold Coast Fashion Show | Judy Carmack Bross | Placeholder | Cover only | Cover `6 - Rachel Pasquini, Kacky Fetzer, Emily Flaherty, Liz Fetzer, and Alona Gornick.jpeg` (`1a196d274334bab3`) |
| david-sweet-yd3 | New Business Poised to Guide Student-Athletes to Best Division III Choices | David A. F. Sweet | Placeholder | In email | `1a19d444dc9a2025`: text, 3 photos with captions |
| jill-lowe-ice-cream | Where to Get It | Jill Lowe | Placeholder | In PDF | `1a187835ee3989b1`: `68) Where to get it - Peach icecream.pdf` (use `pdftotext -layout`, check link annotations, mistakes #43, #53) |
| lejeune-wildwood | Wildwood Review: A Spectacular Visual Feast | Jackson LeJeune | Placeholder | In email | `1a1a851f5991be16` (Judy forward): text, PDF, 4 images (Battle, Hawk, Poster, Title). Judy asks if Jack needs to do anything more |
| datebook | DateBook | Annie Delfosse | Copied from Nov 1 | — | Runs to Dec 12; no past months to remove |
| daily-star-november | Astrochart | Victoria Martin | Copied from Nov 1 | — | Nov 1-7 removed; runs Nov 8 to Dec 5 |

## Notes

- Silent Film cover: Judy (`1a1a1f45c2ec8949`, Nov 3) said use the mannequin (`SF-013_49_175_48_ALT3-Web_JPG_-_732px.jpg,x794.jpeg`) as the cover and `SF-012-49_175_47A-B-1-copy.jpeg` at the top of the article. Ana's Nov 5 layout uses `COVER Goddess.jpeg` (Henri Bendel gown, Lillian Gish). Compared Nov 6: `COVER Goddess.jpeg` is the mannequin and `1 Ivory Dress.jpeg` is `SF-012…`, so Ana's layout already follows Judy.
- Jackson's correction to his Sept 27 review ($50,000 → $150,000, #507) is still open.
- Nov 1 landing page `editions/2026-11-01/index.html` built for Past Editions (mistake #48).
