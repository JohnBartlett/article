# September 20, 2026 Edition — Status

_Updated: 2026-09-19 (cloud pass — Judy confirmed Emma's "Fall Destinations" piece is Bob Glaze's column; text placed, 25 unplaceable photos still blocked)_

**✅ Bob Glaze authorship resolved — text placed, photos still blocked.** Judy confirmed by email
(`1a0b96e5ce14e81c`, Sept 19 11:29 AM UTC): "This is the Bob Glaze column for tomorrow. I don't see
his name on it." This settles the open question from the prior pass (Emma's Sept 19 "My Favorite
Fall Destinations in Chicago" email, unsigned, sent as Bob Glaze's coordinator). Corroborating
detail: the article's own closing line points readers to globalphile.com, which is literally Bob
Glaze's own site per his about.html bio. Full text placed verbatim in
`editions/2026-09-20/bob-glaze/index.html` (title "My Favorite Fall Destinations in Chicago",
category "Weekend Road Trips" matching his prior columns' style). One verbatim-but-flagged source
issue per house rule #18: the Garfield Park Conservatory paragraph has an unbalanced quotation mark
in the source (opens with a quote, then opens a second nested quote — "landscape art under glass" —
without closing the first) — left as written, not corrected. `bob-glaze` is now **Text Only** (was
Placeholder). **Photos not placed — genuine blocker, not guessed at:** the email's 25 attachments
are all generically named (`photo 1.jpg` through `photo 25.jpg`, now staged in
`_attachment-staging/1a0b85da1188e789/`) with zero placement or caption instructions in the email
body, and no correspondence between filenames and the 10 named locations in the text. Per house
rules #28/#29, this needs an explicit filename→location map from Emma/Judy before any `<figure>` is
built — not guessable from content alone (multiple different-looking Chicago park photos could
belong to any of several locations named in the piece).

**✅ Baseball and Ulysses photo question resolved from the source material itself.** Judy's
subject line asked "Use book cover for main photo?" — unanswered by anyone, but David's own
captions answered it: caption 1 reads "Sales of the book have been helped by the release of the
epic movie The Odyssey," and the actual image (`Baseball 1 2.jpeg`) is literally the cover of
Christian Sheppard's book, *The Ancient Wisdom of Baseball*. Set as hero/homepage card. The other
two (`Baseball 2.jpeg`, Sheppard with daughter Cecilia at a game; `Baseball 3.jpeg`, a Sheppard
portrait) placed inline at the paragraphs matching their given captions verbatim, in the order
David specified. Article is now **Ready**.

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

`baseball-ulysses` is now **Ready** — see above. `block-museum` is **Ready** —
its full article text (msg `1a0b82e61d6002fa`, received Sept 19, subject "Text") replaced the
earlier one-paragraph "Blast" placeholder (msg `1a0ac8315f198ed8`, Sept 16, subject "Blast's
text" — a short blurb, not the full piece) with the complete ~10-paragraph verbatim article on
photographers Yuichi Idaka, Henry Simon, and Vivian Maier at The Block Museum's "Picturing the
Modern Metropolis" exhibition. Its image (`1a0ac872b0343f4e`) remains placed as the hero figure
with the full credit line from Sig's email as the figcaption; also the homepage card image. Sig's
email says 9 more photos with credits will follow in a separate email — not yet received, still
open. Two items flagged, not corrected, per house rule #18: the source has a typo ("potray" for
"portray") and a missing space ("Moholy-Nagy(1895-1946)"). Also open: Sig's own text opens with
the title "Megalopolis," but Judy's official lineup names this article "The Block Museum" — the
published H1/title was left unchanged pending Judy's/John's call on which title to use.
`basak-notz` is **Ready** — 5 real Gmail-attachment photos placed (COVER as
homepage/hero card only, per house rule #27 — no explicit "also use in body" instruction); the
other 17 of 22 photo positions remain Google Drive-link-only and cannot be auto-staged — still
open. `hawthorne-works` remains a placeholder stub — but Adrian's actual article text has now
arrived (docx attachment on `1a0b97097e6da9d9`, Judy forwarding Adrian's own "My article" email to
Annie, cc John, Sept 19 11:32 AM UTC) — not yet staged in `_attachment-staging/` as of this pass
(email arrived after the most recent hourly fetch), so the docx has not been extracted or placed
yet; its cover photo remains placed as the homepage card. `bob-glaze` is now **Text Only** — see
above; the authorship question is resolved. Dominic Pacyga still needs an about.html bio.

**Sig's 9 promised block-museum photos (msg `1a0b82e61d6002fa`'s follow-up) — 7 of 9 now placed.**
Photos 3–7 were staged this pass and placed at the exact anchors mapped in the prior pass (all
unambiguous matches — each credit quotes the same work title/description the article text already
names):
- **1 of 9** (`IMG_8343.JPG`, Moholy-Nagy portrait by Hugo Erfurth, ca. 1930) — placed, after
  paragraph 1 (the Moholy-Nagy biography paragraph).
- **2 of 9** (`9-ModernMetropolis-Yuichi Idaka - Untitled El.JPEG`) — confirmed via MD5 to be a
  byte-identical resend of the photo already placed as the hero (msg `1a0ac872b0343f4e`, item #155).
  Not placed as a separate figure; staging folder deleted as a duplicate, not consumed as new content.
- **3 of 9** (`2-ModernMetropolis-Yuichi Idaka-Untitled Skyline.PNG`, Idaka "Untitled" 1940s) —
  placed, end of paragraph 4.
- **4 of 9** (`5-ModernMetroplis-Henry Simon - State and Monroe Streets.PNG`) — placed, paragraph 6,
  first Simon figure.
- **5 of 9** (`6-ModernMetropolis-Henry Simon - Wacker Drive.PNG`) — placed, paragraph 6, second
  Simon figure.
- **6 of 9** (`IMG_8275.jpeg`, Maier's "At the Balaban and Katz United Artist Theater, 1961") —
  placed, paragraph 7, first Maier figure.
- **7 of 9** (`IMG_8341.jpg`, Maier's "Chicago, IL, 1962" / Snack Shop & Diner) — placed, paragraph
  7, second Maier figure.
- **8 of 9** (`IMG_8273.jpeg`) and **9 of 9** (`IMG_8289.jpeg`) — both captioned identically as
  generic installation views of the exhibition, with no distinguishing detail and no sentence in
  the article text naming a specific installation shot. **Placement genuinely ambiguous — not
  guessed at, still open.** Needs John's/Judy's call on whether/where these two run (e.g. near the
  intro paragraph about the exhibition, or omitted as redundant with each other). Not staged yet
  either as of this pass.

`block-museum` is now **Ready** with 7/9 of Sig's promised photos placed (was 2/9). Only #8/#9's
placement remains an open question.

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
| 2 | bob-glaze | My Favorite Fall Destinations in Chicago | Bob Glaze | Emma Muhleman |
| 3 | baseball-ulysses | Baseball and Ulysses | David A. F. Sweet | Judy to John |
| 4 | block-museum | The Block Museum | Sigalit Zetouni | Sig to John |
| 5 | newberry-chicago-machine | The Newberry Library: A Book on the Chicago Machine | Dominic Pacyga | Annie Delfosse |
| 6 | hawthorne-works | The Hawthorne Works Project | Adrian Naves | Emma Muhleman |
| 7 | coyote-vs-acme | Coyote vs. Acme Review: A Well-Done Romp in Spite of All Odds | Jackson LeJeune | Judy to John |

## Pending Deliveries

- ~~**Basak Notz, Illustrator and Artist** (Judy Carmack Bross)~~ — done, article **Ready**. The 5 real Gmail-attachment photos are placed: `2 - Cartier Drawings.jpg`, `3 - Diamond Bracelet.jpg`, `4 - Basak Desk.jpg` inline with no caption (none given in source); `16 - Blue Heeler.jpg` inline with its verbatim caption; `COVER - Basak Colectivo Billboard.jpeg` set as the homepage/hero card image only. The other 17 of 22 photo positions remain Google Drive `view`-link-only in the source email — `fetch-email-attachments.yml` cannot stage these; still needs John to download manually or ask Ana/Judy to resend as real attachments.
- **My Favorite Fall Destinations in Chicago** (Bob Glaze) — text placed, article **Text Only**. 25 generically-named photos staged but un-placeable without an explicit filename→location map.
- ~~**The Block Museum** (Sigalit Zetouni)~~ — done, article **Ready**.
- **The Newberry Library: A Book on the Chicago Machine** (Dominic Pacyga) — article text not yet received; cover headshot in hand and set as the homepage card image. **New author's bio** — needed for about.html; the byline link is dead until it exists.
- **The Hawthorne Works Project** (Adrian Naves) — cover photo placed as homepage card; article text (docx) has now arrived via Judy's forward (`1a0b97097e6da9d9`) but is not yet staged in `_attachment-staging/` — expected within the hour.
- ~~**Baseball and Ulysses** (David A. F. Sweet)~~ — done, article **Ready**. All 3 photos placed; book cover resolved as hero from the source captions themselves.
- ~~**Coyote vs. Acme Review** (Jackson LeJeune)~~ — done, article **Ready**. Full text + all 4 photos placed at their exact PDF-source positions.

## Blockers

- **Basak Notz and Dominic Pacyga have no about.html bios yet.** Basak Notz's byline points to `#judy-carmack-bross` (she's the credited author, already has a bio) so this risk applies to Dominic Pacyga only.
- **Basak Notz photos — 17 of 22 are Google Drive links, not Gmail attachments, and cannot be staged automatically.** Needs John's decision: download manually, or ask Ana/Judy to resend as real attachments.
- **Basak Notz COVER photo placement is ambiguous** (hero-in-body vs. homepage-card-only) — file is in hand and set as homepage card image; whether it should *also* run inline as the hero/opening image is still unconfirmed (no caption, no explicit instruction).
- **Annie's DateBook question is still open** — she asked (Sept 13, msg `1a09c1176fa6497d`) whether she can add more events later; needs John's yes/no.
- **`block-museum`'s title is ambiguous.** The published H1/title is "The Block Museum" (Judy's official lineup name); Sig's own Sept 19 email headed the full article text "Megalopolis." Left unchanged pending John's/Judy's call on which title to publish under.
- **`block-museum` — 2 of Sig's 9 promised photos (#8/#9) have no textual anchor at all** (both generic, identically-captioned installation views) — needs John's/Judy's decision on placement once staged, not guessable from the source. 7 of 9 are now placed.
- ~~**Authorship of Emma Muhleman's "Fall Destinations" email**~~ — resolved. Judy confirmed by email it's the Bob Glaze column; text placed.
- **NEW — `bob-glaze`'s 25 photos have no placement instructions.** Generic filenames (`photo 1.jpg`–`photo 25.jpg`), no captions or location labels in the email body, no correspondence to the 10 named locations in the text. Needs an explicit filename→location map from Emma or Judy before any figure is built — not guessable from content alone.
- **NEW — `hawthorne-works` article text (docx) received but not yet staged.** Judy forwarded Adrian's original "My article" email (with the docx attachment) to Annie, cc John, Sept 19 11:32 AM UTC (`1a0b97097e6da9d9`). Not yet in `_attachment-staging/` as of this pass — should appear within the hour; a future pass should extract and place the text once it does. Two more Drive-link-only photos also mentioned in Adrian's original email (`IMG_1555.png`, `IMG_1554.png`, `Old fireproof water tower.jpeg`) beyond the already-placed COVER photo — same Drive-link limitation as Basak Notz's remaining photos.

## Articles

| Slug | Title | Author | HTML | Photos | Notes |
|------|-------|--------|------|--------|-------|
| basak-notz | Basak Notz, Illustrator and Artist | Judy Carmack Bross | **Ready** | 5/22 placed (COVER as homepage card only; 2/3/4/16 inline, 16 captioned); 17/22 Drive-link only, unreachable by fetch workflow | COVER in-body placement still unconfirmed |
| bob-glaze | My Favorite Fall Destinations in Chicago | Bob Glaze | **Text Only** | 0/25 placed; staged but no placement map | Authorship confirmed by Judy; photo placement blocked |
| baseball-ulysses | Baseball and Ulysses | David A. F. Sweet | **Ready** | Hero (book cover) + 2 inline, resolved from source captions | Judy's "use book cover?" question answered by caption 1 itself |
| block-museum | The Block Museum | Sigalit Zetouni | **Ready** | Hero + 6 inline (7/9 of Sig's promised photos placed); 2 of 9 (#8/#9) have no anchor (open question) | Full ~10-paragraph text placed verbatim (msg `1a0b82e61d6002fa`) |
| newberry-chicago-machine | The Newberry Library: A Book on the Chicago Machine | Dominic Pacyga | Placeholder | In article folder, set as homepage card (`DominicHeadshot.jpeg`) | New author, needs bio |
| hawthorne-works | The Hawthorne Works Project | Adrian Naves | Placeholder | Cover photo placed as homepage card (`COVER - Water tower sideview.jpeg`) | Article text (docx) received, awaiting staging |
| coyote-vs-acme | Coyote vs. Acme Review: A Well-Done Romp in Spite of All Odds | Jackson LeJeune | **Ready** | Hero (poster) + 3 inline, all at exact PDF-source positions | No captions given in source; none invented |

**Held, not in nav/homepage:** `jean-colonomos-poems` (Jean Colonomos) — **Ready**, fully built, kept on disk for a future thin week.

## Notes

- Nav chain order (hero → last): basak-notz → bob-glaze → baseball-ulysses → block-museum → newberry-chicago-machine → hawthorne-works → coyote-vs-acme
- DateBook and Astrochart (daily-star-september) copied forward from Sept 13; stale Sept 13-19 Astrochart entries removed, coverage now runs Sept 20-30.
- FutureSports quote correction (David Sweet's PR-requested fix) was applied to the *previous* edition (Sept 13, already published) in an earlier session pass — unrelated to this edition's build.
