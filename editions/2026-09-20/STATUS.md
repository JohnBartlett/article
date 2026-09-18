# September 20, 2026 Edition — Status

_Updated: 2026-09-18 (check-emails pass — Basak Notz article text built, see EMAIL_LOG.md #179-181)_

**⚠️ Pending lineup swap — not yet executed (see Blockers):** Judy (`1a0ab55918f267c8`, 5:48 PM ET)
wants `jean-colonomos-poems` pulled from Sept 20 and held for a future thin week; the Coyote vs
Acme movie review (by Jack LeJeune) takes its slot instead. `jean-colonomos-poems` is still built,
Ready, and sitting in the nav chain as of this pass — the swap needs a `/prep-edition`/`/layout`
pass to actually remove it, create a `coyote-vs-acme` stub, and rewire the nav chain/homepage.
Do not publish this edition with Jean's poems in place without confirming this swap has happened.

Skeleton prepped (nav chain, homepage, DateBook/Astrochart carried forward). `jean-colonomos-poems`
is Ready (both poems built verbatim + Nick Wilder cover photo placed as hero with credit,
per Judy's explicit "at top of page with his credit" instruction) **but per the above is slated
to come back out of this edition.** `baseball-ulysses` is now
**Text Only** — full article text built verbatim (msg `1a0ab428d33b38b8`); no photos placed yet,
see Blockers below. `block-museum` is now **Ready** — article text built verbatim
(msg `1a0ac8315f198ed8`) and its image (`1a0ac872b0343f4e`) is now staged and placed as the
hero figure with the full credit line from Sig's email as the figcaption; also set as the
homepage card image and added to Sigalit Zetouni's article-popup list in about.html. `basak-notz` is now
**Text Only** — full article text built verbatim (msg `1a0b4ea871213509`); 22 photo positions marked
pending in the HTML, only 5 of which are real Gmail attachments (the other 17 are Google Drive links
that cannot be auto-staged — see Blockers). The other 2 articles (`bob-glaze`, `hawthorne-works`)
remain placeholder stubs — no article body text has arrived for either yet (Adrian's Hawthorne Works
cover photo did arrive Sept 18, msg `1a0b4d3abbb9fd88`, but Annie still has his article text).
Dominic Pacyga still needs an about.html bio (Basak Notz's byline is Judy Carmack Bross, who already
has one), and a third new author (Jack/Jackson LeJeune, Coyote vs Acme) will need one too once the
swap above executes.

## Judy's official lineup (`1a0a1ed94574209a`, received 2026-09-14; date corrected to Sept 20 via `1a0a574a949ffeba`, 2026-09-15)

Nav chain order (hero → last):
1. `basak-notz` — Basak Notz, Illustrator and Artist by Judy Carmack Bross
2. `bob-glaze` — Bob Glaze (topic TBD)
3. `baseball-ulysses` — Baseball and Ulysses by David A. F. Sweet
4. `block-museum` — The Block Museum by Sigalit Zetouni
5. `newberry-chicago-machine` — The Newberry Library: A Book on the Chicago Machine, by Dominic Pacyga
6. `hawthorne-works` — The Hawthorne Works Project by Adrian Naves
7. `jean-colonomos-poems` — Two Poems by Jean Colonomos

## Lineup

| Order | Slug | Title | Author | Coordinator |
|---|---|---|---|---|
| 1 | basak-notz | Basak Notz, Illustrator and Artist | Judy Carmack Bross | Ana Baca |
| 2 | bob-glaze | Bob Glaze | Bob Glaze | Emma Muhleman |
| 3 | baseball-ulysses | Baseball and Ulysses | David A. F. Sweet | Judy to John |
| 4 | block-museum | The Block Museum | Sigalit Zetouni | Sig to John |
| 5 | newberry-chicago-machine | The Newberry Library: A Book on the Chicago Machine | Dominic Pacyga | Annie Delfosse |
| 6 | hawthorne-works | The Hawthorne Works Project | Adrian Naves | Emma Muhleman |
| 7 | jean-colonomos-poems | Two Poems | Jean Colonomos | Direct to John |

## Pending Deliveries

- ~~**Basak Notz, Illustrator and Artist** (Judy Carmack Bross)~~ — article text now received from Ana (`1a0b4ea871213509`, Sept 18 2:27 PM UTC) and built verbatim. **Photo situation is unusual and only partly resolved:** the email specifies 22 total images (1 COVER + 21 numbered inline placements, all with explicit inline placement markers from the source — no placement guessing needed) but only 5 came through as real Gmail attachments (`COVER - Basak Colectivo Billboard.jpeg`, `2 - Cartier Drawings.jpg`, `3 - Diamond Bracelet.jpg`, `4 - Basak Desk.jpg`, `16 - Blue Heeler.jpg` — this last one has an explicit caption). The other 17 were sent only as Google Drive `view` links in the email body text, not as MIME attachments — `fetch-email-attachments.yml` only stages real Gmail attachments, so these 17 cannot reach `_attachment-staging/` no matter how long we wait; they need John to either download them manually (Drive access) or ask Ana/Judy to resend as real attachments. Article is now **Text Only** with all 22 photo positions marked as HTML comments (`<!-- PHOTO N pending: ... -->`) in `index.html` so a future pass can drop each one in without re-deriving placement. **Also flagging, not resolved:** the COVER photo appears inline at the very top of the source email (right after the pull-quote, before the first body paragraph) with no explicit "also use in body" instruction and no caption — per CLAUDE.md mistake #27 the default is homepage-card-only, so the hero-figure is left pending rather than assuming it doubles as the in-body opening image. Needs John's confirmation once the image itself is available either way.
- **Bob Glaze** (Bob Glaze) — topic not yet known; owed by Emma.
- **Baseball and Ulysses** (David A. F. Sweet) — not yet received.
- ~~**The Block Museum** (Sigalit Zetouni)~~ — done. Article text built verbatim (`1a0ac8315f198ed8`, "The Blast's text"). Image + credit (`1a0ac872b0343f4e`, "Blast's image and credit": `9-ModernMetropolis-Yuichi Idaka - Untitled El.JPEG`, full credit line given) now staged and placed as the hero figure, and set as the homepage card image. Article is now **Ready**.
- **The Newberry Library: A Book on the Chicago Machine** (Dominic Pacyga) — article text not yet received; cover headshot (`DominicHeadshot.jpeg`) moved from staging into the article folder and set as the homepage card image (subject line only said "Cover Photo," no "also place in body" instruction and no caption — per house rule #27 it stays out of the article body/hero until text arrives). **New author's bio** — needed for about.html; the byline link is dead until it exists.
- **The Hawthorne Works Project** (Adrian Naves) — article text still not received directly by John; Judy's Sept 18 email (`1a0b4d3abbb9fd88`, 2:02 PM UTC) says Annie already has the article from Adrian and only forwards a cover photo (`COVER - Water tower sideview.jpeg`, real Gmail attachment, not yet staged — should appear in `_attachment-staging/` within the hour). Per house rule #27 this is homepage-card material only once staged; the article body still needs Annie to forward Adrian's actual text before this can move off Placeholder.
- ~~**Baseball and Ulysses** (David A. F. Sweet)~~ — article text now received and built verbatim (`1a0ab428d33b38b8`). Three captioned photos (`Baseball 1 2.jpeg`, `Baseball 2.jpeg`, `Baseball 3.jpeg`) attached with captions given in order — now staged in `_attachment-staging/1a0ab428d33b38b8/`, but placement is still blocked: see Blockers below. Article is **Text Only**.
- ~~**Two Poems** (Jean Colonomos)~~ — done. Both poems built verbatim into the stub; Nick Wilder's photo (`IMG_0491.jpeg`) placed as the hero figure with "Photo: Nick Wilder" credit (per Judy's explicit instruction) and set as the homepage card image. Article is now **Ready**.

## Blockers

- **Lineup swap pending: Jean's poems out, Coyote vs Acme in.** Judy confirmed this (`1a0ab55918f267c8`) and forwarded Jack LeJeune's full review text + photos (`1a0ab5430c08b4eb`) the same evening — now staged in `_attachment-staging/1a0ab5430c08b4eb/` (`.pdf` + 4 images) — but the photos aren't placeable yet: no captions given for 3 of the 4 images (`CC CvA Car Image.jpg`, `CC CvA Coyote and Road Runner Image.jpg`, `CC CvA Trial Image.jpg`), and Judy herself is asking John whether to extract photos from the embedded odt/PDF positions or have Jack resend cleaner text+photos separately. Needs John's answer to Judy, then a `/prep-edition` pass to build the `coyote-vs-acme` stub and remove `jean-colonomos-poems` from this edition's nav/homepage (poems stay on disk for a future edition, per Judy's "delay... until then" — don't delete).
- **Baseball and Ulysses photo placement is an open question.** Judy's subject line for `1a0ab428d33b38b8` literally asks "Use book cover for main photo?" — unanswered. Three attachments (`Baseball 1 2.jpeg`, `Baseball 2.jpeg`, `Baseball 3.jpeg`, now staged in `_attachment-staging/1a0ab428d33b38b8/`) came with explicit captions "in the order they should appear," but it's unclear whether any of the three IS the book cover Judy is asking about, or whether a separate cover image is still to come. Needs John's/Judy's decision on (1) which image is the main/hero photo and (2) confirmation the 3 captioned images should run inline in that order.
- **"Movie review" cover photo arrived with no corresponding lineup entry.** Judy sent a cover photo (`CC CvA Poster.jpeg`, msg `1a0a9e2bd9a7c09d`) captioned "Cover photo for new movie review for Sept, 20. Will send shortly" — this is not one of the 7 confirmed lineup articles. Needs Judy/John to clarify: is this a late 8th addition, and who is the reviewer/byline? No article text has arrived for it either way.
- **Basak Notz and Dominic Pacyga have no about.html bios yet** — both are new authors; their byline links (`#basak-notz`, `#dominic-pacyga`) are currently dead. (Note: `basak-notz` article text is now built and byline points to `#judy-carmack-bross` since Judy is the credited author/byline — Judy has an existing bio, so this specific dead-link risk applies to Dominic Pacyga only, not Basak Notz herself, who is the article's subject, not its author.)
- **Basak Notz photos — 17 of 22 are Google Drive links, not Gmail attachments, and cannot be staged automatically.** See Pending Deliveries above. Needs John's decision: download manually, or ask Ana/Judy to resend as real attachments.
- **Basak Notz COVER photo placement is ambiguous** (hero-in-body vs. homepage-card-only) — no explicit instruction either way. See Pending Deliveries above.
- **Annie's DateBook question is still open** — she asked (Sept 13, msg `1a09c1176fa6497d`) whether she can add more events later; needs John's yes/no.

## Articles

| Slug | Title | Author | HTML | Photos | Notes |
|------|-------|--------|------|--------|-------|
| basak-notz | Basak Notz, Illustrator and Artist | Judy Carmack Bross | **Text Only** | 5/22 staged pending (real attachments); 17/22 Drive-link only, unreachable by fetch workflow | Lead/hero; COVER placement ambiguous |
| bob-glaze | Bob Glaze | Bob Glaze | Placeholder | — | Topic TBD |
| baseball-ulysses | Baseball and Ulysses | David A. F. Sweet | **Text Only** | Pending — 3 captioned photos now staged, main-photo/placement question open | Hero photo choice unresolved |
| block-museum | The Block Museum | Sigalit Zetouni | **Ready** | Hero + homepage card (`9-ModernMetropolis-Yuichi Idaka - Untitled El.JPEG`, credited to Yuichi Idaka) | Full credit line placed verbatim |
| newberry-chicago-machine | The Newberry Library: A Book on the Chicago Machine | Dominic Pacyga | Placeholder | In article folder, set as homepage card (`DominicHeadshot.jpeg`) | New author, needs bio |
| hawthorne-works | The Hawthorne Works Project | Adrian Naves | Placeholder | Cover photo staged pending (`COVER - Water tower sideview.jpeg`) | Article text still with Annie |
| jean-colonomos-poems | Two Poems | Jean Colonomos | **Ready** | Hero + homepage card (`IMG_0491.jpeg`, credited to Nick Wilder) | Both poems built verbatim |

## Notes

- Nav chain order (hero → last): basak-notz → bob-glaze → baseball-ulysses → block-museum → newberry-chicago-machine → hawthorne-works → jean-colonomos-poems
- DateBook and Astrochart (daily-star-september) copied forward from Sept 13; stale Sept 13-19 Astrochart entries removed, coverage now runs Sept 20-30.
- FutureSports quote correction (David Sweet's PR-requested fix) was applied to the *previous* edition (Sept 13, already published) during this session's check-emails pass — unrelated to this edition's build, noted here only because it was handled in the same session.
