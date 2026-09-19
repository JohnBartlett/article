# September 20, 2026 Edition — Status

_Updated: 2026-09-19 (newberry-chicago-machine now Ready — the edition's last open article; all 7 nav-linked articles are Ready, edition is stage-ready)_

**✅ Bob Glaze — Ready, all 25 photos placed.** Judy's forward (`1a0b96e5ce14e81c`) confirmed "My Favorite Fall Destinations in Chicago" fills the Bob Glaze slot. Emma initially sent an unedited draft with no photo markers, then followed up (`1a0bafa1de77c944`, Sept 19 6:42 PM UTC): "I apologize, I accidentally sent the unedited version. This one has the pictures listed." — the corrected version has inline "Photo N" markers throughout (matching the `photo N.jpg` attachment filenames 1:1, confirmed by opening and visually checking photo 1/photo 3/photo 18 against their described locations/captions before trusting the correspondence for all 25) and an explicit "By Bob Glaze" byline line, resolving the earlier authorship ambiguity directly from the source rather than inference. Photo 3 is marked "cover photo" and used as both the homepage card and its own inline position (explicit dual-use instruction, not a violation of house rule #27). All 25 photos placed at their marked anchors, compressed per house rule #26. Category "Weekend Road Trips" (matches prior columns). One verbatim-but-flagged source issue per house rule #18: the Garfield Park Conservatory paragraph has an unbalanced quotation mark in the source itself — left as written. One flagged assumption: the source lists "Photo 24" twice in a row (an apparent typo) immediately before the closing paragraph — treated as Photo 24 then Photo 25 sequentially, since that's the only placement that accounts for all 25 numbered attachments; not confirmed with Emma/Bob directly. `bob-glaze` is now **Ready** — verify_edition.py confirms 25/25 photos, no oversized images.

**✅ Hawthorne Works — text and all 4 photos now in, article Ready.** Judy's "My article" forward (`1a0b97097e6da9d9`) looked photos-only at first glance (the email body just says "Here's my article and photos" plus 4 Drive links) — but it actually carries a real attachment, `History of The Hawthorne Works Complex.docx`, missed on the first body-only read and found by checking the message's MIME parts directly. Extracted via `python-docx`, placed verbatim in `hawthorne-works/index.html` (title "History of The Hawthorne Works Complex"), with the docx's own inline `PHOTO #1/#2/#3` placement labels followed exactly: `IMG_1554.png` → "PHOTO #2 - BLACK & WHITE HAWTHORNE WORKS COMPLEX" anchor; `IMG_1555.png` → "PHOTO #3 - BLACK & WHITE INSIDE THE COMPLEX" anchor; `Old fireproof water tower.jpeg` → "PHOTO #1 - OLD FIREPROOF WATER TOWER" anchor — the first two downloaded via the Drive connector, the third downloaded manually through Chrome (the connector's 10MB cap had blocked it), then compressed 8064×6048 → within 3000px/quality 85 per house rule #26. All 3 matches confirmed by opening the actual images, not guessed. The COVER photo (`COVER - Water tower sideview.jpeg`) stays homepage-card-only per house rule #27 (no caption given) — its existing 1280×960 downsized version was left in place; a full-res 8064×6048 copy was also pulled via Chrome for reference but not swapped in, since the existing one already displays correctly at homepage-card size. Two verbatim-but-flagged typos per house rule #18, not corrected: "Cermack Rd." (should be Cermak) and a dropped word — "was later i Cicero" (should likely read "later annexed into Cicero" or similar). `hawthorne-works` is now **Ready**.

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
`basak-notz` is **Ready** with all 22/22 photos placed — the remaining 17 Drive-link-only photos
were downloaded manually via Chrome (the Drive connector's 10MB cap blocked all of them; navigating
directly to `drive.google.com/uc?export=download&id=<id>` bypassed the flaky download-button UI and
worked reliably for the last several). All 17 compressed per house rule #26 (max 3000px, quality
85). COVER stays homepage/hero card only per house rule #27 (no explicit "also use in body"
instruction, still unconfirmed if it should double as the in-body opener). `hawthorne-works` is now **Ready** — see above; text extracted and placed, all 4 photos
in, its COVER photo remains the homepage card only. `bob-glaze` is now **Ready** — see
above; all 25 photos placed. `newberry-chicago-machine` is now **Ready** — see below; byline is Judy Carmack Bross (already has a bio), not Dominic Pacyga, so the bio blocker is resolved as moot — **all 7 nav-linked articles are now Ready.**

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
  intro paragraph about the exhibition, or omitted as redundant with each other). Both files are
  now downloaded and sitting in `editions/2026-09-20/block-museum/` (copied from
  `_attachment-staging/` once the hourly fetch caught up), but neither is wired into the HTML —
  no `<figure>` built for either pending that call.

`block-museum` is now **Ready** with 7/9 of Sig's promised photos placed (was 2/9); #8/#9 are on
disk but unplaced. Only #8/#9's placement remains an open question.

## Judy's official lineup (`1a0a1ed94574209a`, received 2026-09-14; date corrected to Sept 20 via `1a0a574a949ffeba`, 2026-09-15; swapped per `1a0ab55918f267c8`, 2026-09-16)

Nav chain order (hero → last):
1. `basak-notz` — Basak Notz, Illustrator and Artist by Judy Carmack Bross
2. `bob-glaze` — Bob Glaze (topic TBD)
3. `baseball-ulysses` — Baseball and Ulysses by David A. F. Sweet
4. `block-museum` — The Block Museum by Sigalit Zetouni
5. `newberry-chicago-machine` — The Newberry Library: A Book on the Chicago Machine, by Dominic Pacyga *(Judy's original lineup listed Pacyga as author; the article text itself, received `1a0bb9b780c3dc19`, states "Author: Judy Carmack Bross" — Judy profiling Pacyga, same pattern as basak-notz. Byline corrected accordingly.)*
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
| 5 | newberry-chicago-machine | The Newberry Library: A Book on the Chicago Machine | Judy Carmack Bross | Annie Delfosse |
| 6 | hawthorne-works | The Hawthorne Works Project | Adrian Naves | Emma Muhleman |
| 7 | coyote-vs-acme | Coyote vs. Acme Review: A Well-Done Romp in Spite of All Odds | Jackson LeJeune | Judy to John |

## Pending Deliveries

- ~~**Basak Notz, Illustrator and Artist** (Judy Carmack Bross)~~ — done, article **Ready**, all 22/22 photos placed. `2 - Cartier Drawings.jpg`, `3 - Diamond Bracelet.jpg`, `4 - Basak Desk.jpg` inline with no caption (none given in source); `16 - Blue Heeler.jpg` inline with its verbatim caption; the other 17 (all Drive-link-only in the source) downloaded manually via Chrome and placed inline at their marked PHOTO N anchors, no captions given for any of them; `COVER - Basak Colectivo Billboard.jpeg` set as the homepage/hero card image only.
- ~~**Bob Glaze** (Bob Glaze)~~ — done, article **Ready**. Emma's corrected email had explicit "Photo N" inline markers and a "By Bob Glaze" byline; all 25 photos placed at their marked anchors, photo 3 doubling as cover + inline per explicit instruction.
- ~~**The Block Museum** (Sigalit Zetouni)~~ — done, article **Ready**.
- ~~**The Newberry Library: A Book on the Chicago Machine**~~ — done, article **Ready**. Annie sent the full article Sept 19 9:38 PM UTC (`1a0bb9b780c3dc19`) after Judy escalated with her directly. Byline is **Judy Carmack Bross** (the source's own "Author:" line), not Dominic Pacyga — he's the subject/interviewee, quoted throughout, not the writer. This resolves the bio blocker as moot (Judy already has an about.html bio). All 7 numbered photos placed at their explicit anchors (source gave "Photo N, Caption: ..." markers for each) — photos 4/5 (Frank Corr and Richard J. Daley) placed side-by-side per the source's explicit "(side by side with photo five/four)" instruction. Several verbatim-but-flagged typos per house rule #18, not corrected: "Couglin" (should be Coughlin), "Richand M. Daley" (should be Richard), "Chicago soon because the second largest" (should be "became"), a missing space in "1871changed." Title kept as "The Newberry Library: A Book on the Chicago Machine" (Judy's official lineup name, already used on homepage/nav) rather than the source email's own subject line "Dominic Pacyga on Chicago's Political Machines" — same open-title-question pattern as block-museum, not resolved either way, just left as originally published.
- ~~**The Hawthorne Works Project** (Adrian Naves)~~ — done, article **Ready**. Text found (docx attachment on Judy's forward, missed on first pass) and all 4 photos placed (last one pulled manually via Chrome after the Drive connector's 10MB cap blocked it).
- ~~**Baseball and Ulysses** (David A. F. Sweet)~~ — done, article **Ready**. All 3 photos placed; book cover resolved as hero from the source captions themselves.
- ~~**Coyote vs. Acme Review** (Jackson LeJeune)~~ — done, article **Ready**. Full text + all 4 photos placed at their exact PDF-source positions.

## Blockers

- **Basak Notz COVER photo placement is ambiguous** (hero-in-body vs. homepage-card-only) — file is in hand and set as homepage card image; whether it should *also* run inline as the hero/opening image is still unconfirmed (no caption, no explicit instruction).
- ~~**Annie's DateBook question**~~ — resolved. John's answer: yes, she can send additions anytime, ideally before publication, but a post-publish hotfix is fine too.
- **`block-museum`'s title is ambiguous.** The published H1/title is "The Block Museum" (Judy's official lineup name); Sig's own Sept 19 email headed the full article text "Megalopolis." Left unchanged pending John's/Judy's call on which title to publish under.
- **`block-museum` — 2 of Sig's 9 promised photos (#8/#9) have no textual anchor at all** (both generic, identically-captioned installation views) — both are now downloaded into the article folder, but placement is still John's/Judy's call, not guessable from the source. 7 of 9 are now placed.

## Articles

| Slug | Title | Author | HTML | Photos | Notes |
|------|-------|--------|------|--------|-------|
| basak-notz | Basak Notz, Illustrator and Artist | Judy Carmack Bross | **Ready** | 22/22 placed (COVER as homepage card only; 21 inline, 1 captioned) | COVER in-body placement still unconfirmed |
| bob-glaze | My Favorite Fall Destinations in Chicago | Bob Glaze | **Ready** | 25/25 placed (photo 3 = cover + inline, explicit dual-use instruction) | Byline confirmed both by Judy's forward and Emma's explicit "By Bob Glaze" line |
| baseball-ulysses | Baseball and Ulysses | David A. F. Sweet | **Ready** | Hero (book cover) + 2 inline, resolved from source captions | Judy's "use book cover?" question answered by caption 1 itself |
| block-museum | The Block Museum | Sigalit Zetouni | **Ready** | Hero + 6 inline (7/9 of Sig's promised photos placed); 2 of 9 (#8/#9) downloaded into folder but unplaced (open question) | Full ~10-paragraph text placed verbatim (msg `1a0b82e61d6002fa`) |
| newberry-chicago-machine | The Newberry Library: A Book on the Chicago Machine | Judy Carmack Bross (Dominic Pacyga is the subject, not the writer) | **Ready** | 7/7 placed, all at explicit numbered anchors from the source | Bio blocker resolved — Judy already has a bio |
| hawthorne-works | History of The Hawthorne Works Complex | Adrian Naves | **Ready** | COVER as homepage card; 3 inline (`Old fireproof water tower.jpeg`, `IMG_1554.png`, `IMG_1555.png`) at docx-specified anchors | Full text placed verbatim from docx attachment |
| coyote-vs-acme | Coyote vs. Acme Review: A Well-Done Romp in Spite of All Odds | Jackson LeJeune | **Ready** | Hero (poster) + 3 inline, all at exact PDF-source positions | No captions given in source; none invented |

**Held, not in nav/homepage:** `jean-colonomos-poems` (Jean Colonomos) — **Ready**, fully built, kept on disk for a future thin week.

## Notes

- Nav chain order (hero → last): basak-notz → bob-glaze → baseball-ulysses → block-museum → newberry-chicago-machine → hawthorne-works → coyote-vs-acme
- DateBook and Astrochart (daily-star-september) copied forward from Sept 13; stale Sept 13-19 Astrochart entries removed, coverage now runs Sept 20-30.
- FutureSports quote correction (David Sweet's PR-requested fix) was applied to the *previous* edition (Sept 13, already published) in an earlier session pass — unrelated to this edition's build.
