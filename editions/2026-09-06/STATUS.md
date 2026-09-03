# September 6, 2026 Edition — Status

_Updated: 2026-09-03_

**Skeleton, nav chain, homepage, DateBook, and Astrochart are wired.** 1 of 8 articles (Fill The Stands) is Ready; the other 7 are placeholder stubs awaiting content that has been announced but not yet fully delivered. Content-fetching work continues in `/new-edition` passes.

## Judy's official lineup (`1a05977b5615c844`, received 2026-08-31, refined through Sept 3 emails)

Nav chain order (hero → last):
1. `francesco-bianchini` — Francesco Bianchini's 100th Story (his 100th published piece — lead article)
2. `silvia-beltrametti-satire` — Silvia Beltrametti and Satire, by Judy (Annie building)
3. `jafra-canaan-wellspring` — Young Dancer's Perspective, by Judy (Jafra / Canaan Wellspring Q&A)
4. `rush-benefit` — Rush Woman's Board Benefit, by Emma
5. `sounds-good-choir-river` — Sounds Good Choir on the River, by Emma
6. `dr-ruth-gannon-cook` — Dr. Ruth Gannon-Cook profile, by Marcie Harrison
7. `tadoussac` — A Photo Trip to Tadoussac, by Marjorie Schwebel
8. `fill-the-stands` — How Sweet It Is: Fill The Stands Gives Boost to Girls' Sports, by David A. F. Sweet

Sig's piece (originally floated for this edition) is confirmed **delayed to Sept 13** — see her Sept 2 emails (`1a0637a582460b96` thread). Not part of this lineup.

Judy is also writing a separate Editor's Page piece about Francesco's 100th-article milestone — that's `editorial.html` content, not part of this edition's nav chain.

## Articles

| Slug | Title | Author | HTML | Photos | Notes |
|------|-------|--------|------|--------|-------|
| francesco-bianchini | Francesco Bianchini's 100th Story | Francesco Bianchini | Placeholder | — | Judy says content is going directly to Ana, not John — check with Ana before assuming it hasn't arrived. |
| silvia-beltrametti-satire | Silvia Beltrametti and Satire | Judy Carmack Bross | Placeholder | Cover photo in hand (`IMG_4010.jpeg`, msg `1a05f306943b5e4d`), not yet placed | Confirmed by John (Sept 3) to be the same article the Aug 31 lineup called "Silvia Krehbiel Driehaus curator" — name corrected to Beltrametti. Article text not yet received. |
| jafra-canaan-wellspring | Young Dancer's Perspective | Judy Carmack Bross | Placeholder | Photos in hand (Google Drive folder + `hananpicture.JPG`/`sarahpicture.jpeg`, msg `1a0536f036aaa3e6`; cover-photo options sent Sept 2, msg `1a06174ba14099e2`), not yet placed | Q&A with dancer Sarah Zakarneh and choreographer Hanan (Canaan Wellspring / Jafra event at the Athenaeum Center). Judy's draft docx in hand (`Canaan Wellspring.docx`, msg `1a0526f7b944412d`). **John still owes Judy a reply** on whether interview form is the right approach and whether it's OK the piece leans on the cause more than dancing (asked Aug 30 and again Sept 1, msg `1a05d1d5f6f9cc6f`) — resolve before finalizing text. |
| rush-benefit | Rush Woman's Board Benefit | Judy Carmack Bross (byline TBD — likely Emma) | Placeholder | Cover photo in hand (msg `1a0575715a1e8423`), not yet placed | By Emma per lineup. Article text not yet received. |
| sounds-good-choir-river | Sounds Good Choir on the River | Judy Carmack Bross (byline TBD — likely Emma) | Placeholder | Two candidate cover photos sent Sept 1 (msg `1a05d171149a00d8` "river music" and msg `1a05c81fbf12bf31` "Hallelujah Chorus sing-a-long") — same event; need to confirm which Judy prefers before placing | By Emma per lineup. Article text not yet received. |
| dr-ruth-gannon-cook | Dr. Ruth Gannon-Cook: The Female Robert Langdon | Marcie Harrison | Placeholder | Full article + 5 photos (headshot, bumblebee, Penelope the Pig, book cover, ring x2) sent as attachments in the original Aug 22 email in this thread — not yet fetched/extracted | **New author** — bio added to about.html (Sept 3) from Marcie's own text (msg `1a066d81336c9639`). Byline spelling confirmed "Harrison," not the earlier "Harrington." Full content is ready to build — highest-priority next pass. |
| tadoussac | A Photo Trip to Tadoussac | Marjorie Schwebel | Placeholder | Cover photo in hand (msg `1a05e0f62a76d0bd`), not yet placed | **New author** — about.html entry added Sept 3 with bio marked pending (no bio text received yet). Article text not yet received; original lineup flagged this may be delayed. |
| fill-the-stands | How Sweet It Is: Fill The Stands Gives Boost to Girls' Sports | David A. F. Sweet | ✅ Full text built (parallel session, Sept 2; nav fixed Sept 3) | ✅ 2/3 placed (`FTS 1.jpeg` hero, `FTS 3.jpeg` body) — `FTS 2.JPEG` pending, Google Drive permissions block automated download (msg `1a05d0c35428c573`) | About nonprofit Fill The Stands and founder Elizabeth Sweet. Verifies READY per `verify_edition.py` (2/3 photos is enough for Ready since at least one photo exists per convention — confirm with Judy whether Photo 2 is essential before publish). |
| datebook | DateBook | Annie Delfosse | Copied forward from Aug 30 (stale Aug 23 copy found and corrected Sept 3 — title/kicker updated to Sept 6, stale internal Astrochart link fixed from `daily-star-august` to `daily-star-september`) | — | `edition_checks.py` confirms no stale past-month sections as of Sept 3. |
| daily-star-september | Astrochart | Victoria Martin | Built ahead of prep (Aug 27); `astro_day_change` GA4 tracking added Sept 1; pushed to production Sept 3 ahead of Victoria's reply | — | Sent to Victoria for review Aug 31/Sept 1 (preview + "goes live the moment you approve"); no reply as of Sept 3. Pushed to production anyway per John's direct instruction — follow up with her to confirm content is correct. |

## Notes

- Nav chain order (hero → last): francesco-bianchini → silvia-beltrametti-satire → jafra-canaan-wellspring → rush-benefit → sounds-good-choir-river → dr-ruth-gannon-cook → tadoussac → fill-the-stands
- Homepage hero and all 7 non-Fill-The-Stands cards use `card-placeholder.jpg` — replace with real cover images as they're extracted/received.
- Nav thumbnails across the edition use a shared `thumb-placeholder.jpg` at the edition root — replace with real navthumbs as content/covers arrive. Same harmless "duplicate image used 2×" pattern as prior editions (`content_audit.py` now excludes this from its duplicate-photo check).
- **Open decisions needed from Judy/contributors:**
  - Confirm Silvia Beltrametti naming with Judy directly (John inferred same-article-name-correction per his own judgment call; not yet confirmed with Judy).
  - Which "Sounds Good Choir" cover photo to use (river music vs. Hallelujah Chorus sing-a-long).
  - Dr. Ruth Cook byline: confirmed "Marcie Harrison" (resolves the earlier Harrison/Harrington ambiguity).
  - Marjorie Schwebel's bio is still needed for about.html.
  - John owes Judy a reply on the Jafra/Canaan Wellspring interview-form approach.
- Two new authors this edition: Marcie Harrison, Marjorie Schwebel — both added to about.html "More Contributors."
