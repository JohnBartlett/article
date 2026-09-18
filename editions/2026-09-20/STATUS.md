# September 20, 2026 Edition — Status

_Updated: 2026-09-18 (local session — lineup swap executed: Jean's poems out, Coyote vs Acme in)_

**✅ Lineup swap executed.** Per Judy's request (`1a0ab55918f267c8`, "Like the idea of just having 7
stories"), `jean-colonomos-poems` has been removed from this edition's nav chain and homepage —
the article stays fully built on disk (both poems + Nick Wilder's photo) but is unlinked from
everywhere, held for a future thin week per Judy's own suggestion. `coyote-vs-acme` (Jackson
LeJeune's review) now occupies that slot instead: full text built verbatim from the PDF
(`pdftotext -layout`, not PyPDF2 — see CLAUDE.md mistake #43), and all 4 photos placed at their
exact positions in the source PDF's own layout (confirmed by rendering pages as images and
visually matching each photo to its page). None of the 4 photos had captions in the source, so
none were invented. The embedded New Yorker hyperlink in the PDF (a real clickable link, found
via annotation extraction, not visible in the plain text) was preserved. Byline is Jackson
LeJeune, who already has an about.html bio from a previously-dropped article — his articles-popup
was updated automatically by `edition_checks.py`.

`baseball-ulysses` remains **Text Only** — full article text built verbatim (msg
`1a0ab428d33b38b8`); no photos placed yet, see Blockers below. `block-museum` is **Ready** —
article text built verbatim (msg `1a0ac8315f198ed8`) and its image (`1a0ac872b0343f4e`) placed as
the hero figure with the full credit line from Sig's email as the figcaption; also the homepage
card image. `basak-notz` is **Ready** — 5 real Gmail-attachment photos placed (COVER as
homepage/hero card only, per house rule #27 — no explicit "also use in body" instruction); the
other 17 of 22 photo positions remain Google Drive-link-only and cannot be auto-staged — still
open. `hawthorne-works` remains a placeholder stub (Annie still has Adrian's article text) but its
cover photo is placed as the homepage card. `bob-glaze` remains a placeholder stub — topic not
yet known. Dominic Pacyga still needs an about.html bio.

## Judy's official lineup (`1a0a1ed94574209a`, received 2026-09-14; date corrected to Sept 20 via `1a0a574a949ffeba`, 2026-09-15; swapped per `1a0ab55918f267c8`, 2026-09-16)

Nav chain order (hero → last):
1. `basak-notz` — Basak Notz, Illustrator and Artist by Judy Carmack Bross
2. `bob-glaze` — Bob Glaze (topic TBD)
3. `baseball-ulysses` — Baseball and Ulysses by David A. F. Sweet
4. `block-museum` — The Block Museum by Sigalit Zetouni
5. `newberry-chicago-machine` — The Newberry Library: A Book on the Chicago Machine, by Dominic Pacyga
6. `hawthorne-works` — The Hawthorne Works Project by Adrian Naves
7. `coyote-vs-acme` — Coyote vs. Acme Review: A Well-Done Romp in Spite of All Odds by Jackson LeJeune

**Held for a future thin week (not in this edition's nav/homepage):** `jean-colonomos-poems` — Two Poems by Jean Colonomos, fully built, do not delete.

## Lineup

| Order | Slug | Title | Author | Coordinator |
|---|---|---|---|---|
| 1 | basak-notz | Basak Notz, Illustrator and Artist | Judy Carmack Bross | Ana Baca |
| 2 | bob-glaze | Bob Glaze | Bob Glaze | Emma Muhleman |
| 3 | baseball-ulysses | Baseball and Ulysses | David A. F. Sweet | Judy to John |
| 4 | block-museum | The Block Museum | Sigalit Zetouni | Sig to John |
| 5 | newberry-chicago-machine | The Newberry Library: A Book on the Chicago Machine | Dominic Pacyga | Annie Delfosse |
| 6 | hawthorne-works | The Hawthorne Works Project | Adrian Naves | Emma Muhleman |
| 7 | coyote-vs-acme | Coyote vs. Acme Review: A Well-Done Romp in Spite of All Odds | Jackson LeJeune | Judy to John |

## Pending Deliveries

- ~~**Basak Notz, Illustrator and Artist** (Judy Carmack Bross)~~ — done, article **Ready**. The 5 real Gmail-attachment photos are placed: `2 - Cartier Drawings.jpg`, `3 - Diamond Bracelet.jpg`, `4 - Basak Desk.jpg` inline with no caption (none given in source); `16 - Blue Heeler.jpg` inline with its verbatim caption; `COVER - Basak Colectivo Billboard.jpeg` set as the homepage/hero card image only. The other 17 of 22 photo positions remain Google Drive `view`-link-only in the source email — `fetch-email-attachments.yml` cannot stage these; still needs John to download manually or ask Ana/Judy to resend as real attachments.
- **Bob Glaze** (Bob Glaze) — topic not yet known; owed by Emma.
- ~~**The Block Museum** (Sigalit Zetouni)~~ — done, article **Ready**.
- **The Newberry Library: A Book on the Chicago Machine** (Dominic Pacyga) — article text not yet received; cover headshot in hand and set as the homepage card image. **New author's bio** — needed for about.html; the byline link is dead until it exists.
- **The Hawthorne Works Project** (Adrian Naves) — cover photo placed as homepage card; article text still not received directly — Annie has it from Adrian, still needs to forward.
- ~~**Baseball and Ulysses** (David A. F. Sweet)~~ — article text received and built verbatim. Three captioned photos staged, placement still blocked — see Blockers below.
- ~~**Coyote vs. Acme Review** (Jackson LeJeune)~~ — done, article **Ready**. Full text + all 4 photos placed at their exact PDF-source positions.

## Blockers

- **Baseball and Ulysses photo placement is an open question.** Judy's subject line for `1a0ab428d33b38b8` literally asks "Use book cover for main photo?" — unanswered. Three attachments (`Baseball 1 2.jpeg`, `Baseball 2.jpeg`, `Baseball 3.jpeg`, staged in `_attachment-staging/1a0ab428d33b38b8/`) came with explicit captions "in the order they should appear," but it's unclear whether any of the three IS the book cover Judy is asking about. Needs John's/Judy's decision on (1) which image is the main/hero photo and (2) confirmation the 3 captioned images should run inline in that order.
- **Basak Notz and Dominic Pacyga have no about.html bios yet.** Basak Notz's byline points to `#judy-carmack-bross` (she's the credited author, already has a bio) so this risk applies to Dominic Pacyga only.
- **Basak Notz photos — 17 of 22 are Google Drive links, not Gmail attachments, and cannot be staged automatically.** Needs John's decision: download manually, or ask Ana/Judy to resend as real attachments.
- **Basak Notz COVER photo placement is ambiguous** (hero-in-body vs. homepage-card-only) — file is in hand and set as homepage card image; whether it should *also* run inline as the hero/opening image is still unconfirmed (no caption, no explicit instruction).
- **Annie's DateBook question is still open** — she asked (Sept 13, msg `1a09c1176fa6497d`) whether she can add more events later; needs John's yes/no.

## Articles

| Slug | Title | Author | HTML | Photos | Notes |
|------|-------|--------|------|--------|-------|
| basak-notz | Basak Notz, Illustrator and Artist | Judy Carmack Bross | **Ready** | 5/22 placed (COVER as homepage card only; 2/3/4/16 inline, 16 captioned); 17/22 Drive-link only, unreachable by fetch workflow | COVER in-body placement still unconfirmed |
| bob-glaze | Bob Glaze | Bob Glaze | Placeholder | — | Topic TBD |
| baseball-ulysses | Baseball and Ulysses | David A. F. Sweet | **Text Only** | Pending — 3 captioned photos now staged, main-photo/placement question open | Hero photo choice unresolved |
| block-museum | The Block Museum | Sigalit Zetouni | **Ready** | Hero + homepage card (`9-ModernMetropolis-Yuichi Idaka - Untitled El.JPEG`, credited to Yuichi Idaka) | Full credit line placed verbatim |
| newberry-chicago-machine | The Newberry Library: A Book on the Chicago Machine | Dominic Pacyga | Placeholder | In article folder, set as homepage card (`DominicHeadshot.jpeg`) | New author, needs bio |
| hawthorne-works | The Hawthorne Works Project | Adrian Naves | Placeholder | Cover photo placed as homepage card (`COVER - Water tower sideview.jpeg`) | Article text still with Annie |
| coyote-vs-acme | Coyote vs. Acme Review: A Well-Done Romp in Spite of All Odds | Jackson LeJeune | **Ready** | Hero (poster) + 3 inline, all at exact PDF-source positions | No captions given in source; none invented |

**Held, not in nav/homepage:** `jean-colonomos-poems` (Jean Colonomos) — **Ready**, fully built, kept on disk for a future thin week.

## Notes

- Nav chain order (hero → last): basak-notz → bob-glaze → baseball-ulysses → block-museum → newberry-chicago-machine → hawthorne-works → coyote-vs-acme
- DateBook and Astrochart (daily-star-september) copied forward from Sept 13; stale Sept 13-19 Astrochart entries removed, coverage now runs Sept 20-30.
- FutureSports quote correction (David Sweet's PR-requested fix) was applied to the *previous* edition (Sept 13, already published) in an earlier session pass — unrelated to this edition's build.
