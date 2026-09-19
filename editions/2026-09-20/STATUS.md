# September 20, 2026 Edition — Status

_Updated: 2026-09-19 (cloud pass — Moholy-Nagy portrait placed in block-museum; 5 more of Sig's 9 promised photos mapped but not yet staged)_

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
open. `hawthorne-works` remains a placeholder stub (Annie still has Adrian's article text) but its
cover photo is placed as the homepage card. `bob-glaze` remains a placeholder stub — topic not
yet known (see new open question below re: Emma's Sept 19 "Fall Destinations" email — possibly
this, possibly not; not assumed either way). Dominic Pacyga still needs an about.html bio.

**Sig's 9 promised block-museum photos (msg `1a0b82e61d6002fa`'s follow-up) have started arriving,
sent Sept 19 as 9 separate emails ("1 of 9" through "9 of 9"), each with one attachment and a full
credit line.** Photo map built from the credits against the article text (all unambiguous matches —
each credit quotes the same work title/description the article text already names):
- **1 of 9** (`IMG_8343.JPG`, Moholy-Nagy portrait by Hugo Erfurth, ca. 1930) — **placed** this pass,
  after paragraph 1 (the Moholy-Nagy biography paragraph).
- **2 of 9** (`9-ModernMetropolis-Yuichi Idaka - Untitled El.JPEG`) — confirmed via MD5 to be a
  byte-identical resend of the photo already placed as the hero (msg `1a0ac872b0343f4e`, item #155).
  Not re-placed; staging folder deleted as a duplicate, not consumed as new content.
- **3 of 9** (`2-ModernMetropolis-Yuichi Idaka-Untitled Skyline.PNG`, Idaka "Untitled" 1940s,
  5 3/4 × 9 11/16in) → anchor: end of paragraph 4 ("Another one of Idaka's photographs is
  rectangular and more abstract...raindrops on a glass window...urban skyline"). **Not staged yet.**
- **4 of 9** (`5-ModernMetroplis-Henry Simon - State and Monroe Streets.PNG`, Simon "Untitled"
  State and Monroe Streets, ca. 1965) → anchor: paragraph 6, first Simon photo ("captivating play
  of shadows in 'Untitled (State and Monroe Streets,)'"). **Not staged yet.**
- **5 of 9** (`6-ModernMetropolis-Henry Simon - Wacker Drive.PNG`, Simon "Untitled" Wacker Drive/
  West Madison, old Chicago Daily News Building, ca. 1960) → anchor: paragraph 6, second Simon
  photo ("In a different photograph...Simon focuses on architecture"). **Not staged yet.**
- **6 of 9** (`IMG_8275.jpeg`, view of Maier's "At the Balaban and Katz United Artist Theater, 1961")
  → anchor: paragraph 7, first Maier photo. **Not staged yet.**
- **7 of 9** (`IMG_8341.jpg`, view of Maier's "Chicago, IL, 1962" / Snack Shop & Diner) → anchor:
  paragraph 7, second Maier photo ("To the left of the photo, we see another one by Maier..."). **Not
  staged yet.**
- **8 of 9** (`IMG_8273.jpeg`) and **9 of 9** (`IMG_8289.jpeg`) — both captioned identically as
  generic installation views of the exhibition, with no distinguishing detail and no sentence in
  the article text naming a specific installation shot. **Placement genuinely ambiguous — not
  guessed at.** Needs John's/Judy's call on whether/where these two run (e.g. near the intro
  paragraph about the exhibition, or omitted as redundant with each other). **Not staged yet either.**

Photos 3–9 were not yet in `_attachment-staging/` as of this pass (Sig sent them 5:46–6:19 AM UTC
Sept 19; the hourly fetch workflow should catch up within the hour of whenever it next runs) — this
map is recorded here so a future pass can drop them in directly at their anchors without
re-deriving order, per house rule #28. Only #8/#9's placement remains an open question once staged.

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
- ~~**Baseball and Ulysses** (David A. F. Sweet)~~ — done, article **Ready**. All 3 photos placed; book cover resolved as hero from the source captions themselves.
- ~~**Coyote vs. Acme Review** (Jackson LeJeune)~~ — done, article **Ready**. Full text + all 4 photos placed at their exact PDF-source positions.

## Blockers

- **Basak Notz and Dominic Pacyga have no about.html bios yet.** Basak Notz's byline points to `#judy-carmack-bross` (she's the credited author, already has a bio) so this risk applies to Dominic Pacyga only.
- **Basak Notz photos — 17 of 22 are Google Drive links, not Gmail attachments, and cannot be staged automatically.** Needs John's decision: download manually, or ask Ana/Judy to resend as real attachments.
- **Basak Notz COVER photo placement is ambiguous** (hero-in-body vs. homepage-card-only) — file is in hand and set as homepage card image; whether it should *also* run inline as the hero/opening image is still unconfirmed (no caption, no explicit instruction).
- **Annie's DateBook question is still open** — she asked (Sept 13, msg `1a09c1176fa6497d`) whether she can add more events later; needs John's yes/no.
- **`block-museum`'s title is ambiguous.** The published H1/title is "The Block Museum" (Judy's official lineup name); Sig's own Sept 19 email headed the full article text "Megalopolis." Left unchanged pending John's/Judy's call on which title to publish under.
- **`block-museum` — 5 of Sig's 9 promised photos (3–9 minus the already-placed duplicate #2) are mapped to exact anchors but not yet staged** — see the photo map above. **2 of the 9 (#8/#9) have no textual anchor at all (both generic, identically-captioned installation views)** — needs John's/Judy's decision on placement once staged, not guessable from the source.
- **NEW — authorship of Emma Muhleman's Sept 19 "My Favorite Fall Destinations in Chicago- 9/20" email is unconfirmed.** 25 photo attachments, full first-person travel-guide text, subject dated for this edition, but no byline stated anywhere in the email and no explicit statement that it's Bob Glaze's piece (despite Emma being Bob Glaze's coordinator per the lineup table). Not built, not staged, not assumed to fill the `bob-glaze` slot — needs John's/Judy's confirmation of whose byline this runs under before anything is done with it. See EMAIL_LOG.md item for full detail.

## Articles

| Slug | Title | Author | HTML | Photos | Notes |
|------|-------|--------|------|--------|-------|
| basak-notz | Basak Notz, Illustrator and Artist | Judy Carmack Bross | **Ready** | 5/22 placed (COVER as homepage card only; 2/3/4/16 inline, 16 captioned); 17/22 Drive-link only, unreachable by fetch workflow | COVER in-body placement still unconfirmed |
| bob-glaze | Bob Glaze | Bob Glaze | Placeholder | — | Topic TBD |
| baseball-ulysses | Baseball and Ulysses | David A. F. Sweet | **Ready** | Hero (book cover) + 2 inline, resolved from source captions | Judy's "use book cover?" question answered by caption 1 itself |
| block-museum | The Block Museum | Sigalit Zetouni | **Ready** | Hero/homepage card + 1 inline (Moholy-Nagy portrait, `IMG_8343.JPG`); 5 more of Sig's 9 promised photos mapped to exact anchors, not yet staged; 2 of the 9 have no anchor (open question) | Full ~10-paragraph text placed verbatim (msg `1a0b82e61d6002fa`) |
| newberry-chicago-machine | The Newberry Library: A Book on the Chicago Machine | Dominic Pacyga | Placeholder | In article folder, set as homepage card (`DominicHeadshot.jpeg`) | New author, needs bio |
| hawthorne-works | The Hawthorne Works Project | Adrian Naves | Placeholder | Cover photo placed as homepage card (`COVER - Water tower sideview.jpeg`) | Article text still with Annie |
| coyote-vs-acme | Coyote vs. Acme Review: A Well-Done Romp in Spite of All Odds | Jackson LeJeune | **Ready** | Hero (poster) + 3 inline, all at exact PDF-source positions | No captions given in source; none invented |

**Held, not in nav/homepage:** `jean-colonomos-poems` (Jean Colonomos) — **Ready**, fully built, kept on disk for a future thin week.

## Notes

- Nav chain order (hero → last): basak-notz → bob-glaze → baseball-ulysses → block-museum → newberry-chicago-machine → hawthorne-works → coyote-vs-acme
- DateBook and Astrochart (daily-star-september) copied forward from Sept 13; stale Sept 13-19 Astrochart entries removed, coverage now runs Sept 20-30.
- FutureSports quote correction (David Sweet's PR-requested fix) was applied to the *previous* edition (Sept 13, already published) in an earlier session pass — unrelated to this edition's build.
