# Classic Chicago Magazine — TODO

## TODO — SEPTEMBER 6 EDITION (prepped, mostly awaiting content)

Skeleton, nav chain, homepage, DateBook, and Astrochart all wired Sept 3. Full detail in
`editions/2026-09-06/STATUS.md`. 1 of 8 articles (Fill The Stands) Ready.

- [ ] **September Astrochart went live on production (chicagoclassicmag.com) ahead of Victoria's approval.** We told her explicitly on Aug 31 ("the moment you give me the okay, I'll push it live") — she had not replied as of this push (Sept 3, per John's direct instruction). Follow up with her to confirm the published version is acceptable.
- [ ] **Reply still owed to Judy re: the Jafra/Canaan Wellspring draft** (`1a0526f7b944412d`, Aug 30) — she asked whether interview form is the right call and whether it's OK the piece leans on the cause more than dancing. Needs John's actual answer before that article's text is finalized.
- [x] ~~Dr. Ruth Cook byline spelling~~ — **RESOLVED Sept 3.** Confirmed "Marcie Harrison" via her own bio email (`1a066d81336c9639`); about.html entry added.
- [x] ~~Dr. Ruth Gannon-Cook article: extract full text + 5 photos~~ — **TEXT BUILT Sept 3** from Ana Baca's laid-out version (`1a06898d75d7c71f`), which supersedes the Aug 22 attachments: full text + explicit photo placement, cover, and captions. Title corrected to the contributor's own, "Meet Dr. Ruth Gannon Cook—the Female Robert Langdon" (no hyphen in the name). **Photos still need downloading** — see below.
- [ ] **Jafra/Canaan Wellspring: build full article** once John's reply to Judy (above) resolves the approach — text and most photos already in hand.
- [ ] **Confirm "Silvia Beltrametti and Satire" naming with Judy directly** — John treated it as the same article as the original lineup's "Silvia Krehbiel Driehaus curator" (name corrected) per his own judgment call; not yet confirmed with Judy herself.
- [ ] **Confirm which "Sounds Good Choir" cover photo Judy wants** — river-music photo (msg `1a05d171149a00d8`) vs. Hallelujah Chorus sing-a-long photo (msg `1a05c81fbf12bf31`), same event.
- [ ] **Marjorie Schwebel's bio** still needed for about.html (currently marked "[Bio pending]").
- [x] ~~Francesco Bianchini's 100th-story content~~ — **ARRIVED and TEXT BUILT Sept 3.** Ana sent it (`1a068a69a0218757`); the article's real title is **"Chopsticks"** (Cuandixia, China), not "Francesco Bianchini's 100th Story" — homepage hero, about.html mini-card and the article itself all renamed. Category changed Milestone → Travel to match the content. **Photos still need downloading** — see below.
- [ ] **Judy still owes the milestone line** to run below Chopsticks' cover photo marking it as Francesco's 100th story (promised in the Aug 31 lineup email `1a05977b5615c844`). A `PREP NOTE` comment marks the spot in the article HTML.
- [ ] **Rush Benefit and Sounds Good Choir article text** not yet received from Emma.
- [ ] **Tadoussac article text** not yet received from Marjorie/Annie; may be delayed further per original lineup note.
- [ ] **Download the 12 Gmail photo attachments for Chopsticks and Dr. Ruth** — both articles' text and `<figure>` markup are built and reference the exact original filenames, but the image files themselves are not on disk (this session had no Gmail OAuth credentials; `~/.gmail-mcp/` was absent). `verify_edition.py` currently reports both as TEXT ONLY with broken images. Run locally:
  ```bash
  source .venv/bin/activate
  python3 - <<'EOF'
  import sys; sys.path.insert(0, 'tools')
  from gmail_api import get_access_token, list_attachments, download_attachment
  t = get_access_token()
  for msg, dest in [('1a068a69a0218757', 'editions/2026-09-06/francesco-bianchini'),
                    ('1a06898d75d7c71f', 'editions/2026-09-06/dr-ruth-gannon-cook')]:
      for a in list_attachments(t, msg):
          download_attachment(t, msg, a['attachmentId'], f"{dest}/{a['filename']}")
          print(dest, a['filename'])
  EOF
  ```
  Then set the two homepage cards to `COVER - Chopsticks.jpeg` and `COVER - Ruth Gannon Cook.png` (currently `card-placeholder.jpg`) and build real nav thumbnails.
- [ ] **Fill The Stands photo #2** blocked by Google Drive permissions (msg `1a05d0c35428c573`) — ask David Sweet to re-share or email the file directly.
- [ ] **Flag two verbatim-text quirks to Judy/Marcie** in the Dr. Ruth piece, left unchanged per the never-edit-contributor-text rule: (1) the paragraph beginning "She points out that signs are all around us" opens with a quotation mark and closes with one, but is written in the third person — it reads like a quote wrapper applied to narration; (2) the article spells the subject's surname "Gannon Cook" throughout while earlier lineup emails and the stub used "Gannon-Cook." Used the contributor's spelling.
- [ ] **Confirm with Judy whether Griffin Museum (Sydney Armstrong)** is still planned for a future edition — flagged delayed-to-Sept-6 on Aug 25 but absent from the final Sept 6 lineup emails.

## DONE — Sept 1-3 session (audit + fixes)

- [x] **Restored Philip Vidal's 39 dropped links** in "About the Town in September" — silently missing from the built HTML vs. the source email; added CLAUDE.md mistake #42 (link-count check) to prevent recurrence.
- [x] **Fixed missing past-edition landing pages** for Aug 16 and Aug 23 — neither `editions/2026-08-16/index.html` nor `editions/2026-08-23/index.html` had ever been built, so Cloudflare's fallback silently served the current homepage instead of a 404. This was the root cause of a reader (Shelley, via Judy) being unable to find last week's Bonnie McDonald article. Rebuilt both from git history; confirmed live; replied to Judy.
- [x] **Fixed stray internal-nav bar exposed on production** in Murray Bay Part 2 — leftover from the Aug 30 post-publish photo hotfix, which rewrote the file without re-commenting the dev2-only block.
- [x] **Fixed a real GA4 leak on dev2**: 6 articles in the March 22 edition (`pokemon-fossil-museum`, `unsung-gems-lfhs`, `two-sisters-and-a-piano`, `kanuga`, `chicago-chamber-music-society`, `building-blocks`) had fully live, uncommented GA4 tracking on dev2 — meaning every `vercel deploy` from dev2 was sending real traffic into production analytics. Normalized to the standard `<!-- GA4-disabled -->` convention, plus 2 sibling files with non-standard-but-working comment variants.
- [x] **Fixed a ~6-month-old GA4 gap on production**: `moneyball` and `wells-street-kitchen-juice` (March 1 edition) had their gtag.js loader commented out while the config call stayed live — meaning zero analytics data was ever actually sent for these two pages since publish. Fixed directly on master.
- [x] **Added `astro_day_change` GA4 event tracking** to the Astrochart's Prev/Next/dropdown navigation (previously untracked — GA4 couldn't distinguish a visitor who browsed all 30 days from one who loaded the page and left). Added to the live Aug 30 page, the Sept 6 page, and pushed to production for both.
- [x] Built `tools/content_audit.py` — automates 5 content-fidelity checks that were previously gaps in every audit pass: DateBook's own internal Astrochart link (mistake #20), stale past-date Astrochart entries (mistake #21), dated homepage hero-meta (mistake #23), duplicate hero+inline photos (mistake #30), emoji in article content (mistake #34).
- [x] Built `tools/ga4_astrochart_query.py` + `.github/workflows/adhoc-ga4-query.yml` for one-off GA4 queries beyond the standard dashboard report (used for Astrochart page-view and session-engagement stats).
- [x] Sent Victoria the September Astrochart preview (dev2), then pushed it to production per John's direct instruction — see the pending-reply item above.
- [x] **Set up the September 6 edition**: built on top of a parallel session's Fill The Stands article (fixed its broken nav-thumb path, extracted its 2 remaining photos). Built 7 remaining article stubs with correct nav chain, wired homepage hero+cards, moved Aug 30 into Past Editions, and built the missing `editions/2026-08-30/index.html` (would have hit the same Cloudflare-fallback 404 bug fixed earlier for Aug 16/23). Found and fixed two more real bugs in the copied-forward DateBook: a stale internal Astrochart link and a full stale August month section. Added Marcie Harrison and Marjorie Schwebel to about.html as new authors. Full status in `editions/2026-09-06/STATUS.md`.

## TODO — AUGUST 30 EDITION (next)

Nav order (final, per Judy's Aug 29 request — Murray Bay Part 2 last): chicago-innovation (hero) → about-the-town → sporting-life → silk-roads-health-retreat → soma-roy → garfield-park-pigments → murray-bay-part-2

### Article status (7 of 7 Ready — full edition built)
- [x] **Chicago Innovation** — "Rallying Chicago's Next Innovators" by Judy Carmack Bross. Built: `editions/2026-08-30/chicago-innovation/` (11 photos placed, READY)
- [x] **About the Town in September** — Philip Vidal. Built: `editions/2026-08-30/about-the-town/` (10 photos placed, READY)
- [x] **The Sporting Life** (David Sweet, Olympia column) — Built: `editions/2026-08-30/sporting-life/` (4 photos placed, READY)
- [x] **My Silk Roads: Dispatch from MAYRLIFE** — Susan Aurinko. Built: `editions/2026-08-30/silk-roads-health-retreat/` (11 photos placed, READY)
- [x] **"Hyperlink, a Connection"** — Soma Roy (real byline, not Annie). Built: `editions/2026-08-30/soma-roy/` (15 photos placed, READY). Text verified word-for-word against the contributor's Word doc.
- [x] **"Colors of Nature"** — Sigalit Zetouni. Built: `editions/2026-08-30/garfield-park-pigments/` (6 photos placed, READY). Renoir's "Two Sisters" at the Art Institute + Garfield Park Conservatory's Pigments! garden show. Applied Sig's own requested "1974"→"1874" correction.
- [x] **Only in Murray Bay: Part II** — Judy Carmack Bross. Built: `editions/2026-08-30/murray-bay-part-2/` (29 photos placed, READY). Moved to last position per Judy's request.

### Held for Sept 6
- [ ] **Young Dancer's Perspective** — Judy Carmack Bross, Q&A format with the young dancer + her company's director. Delayed a week (Judy, Aug 29) — sensitive subject, wants to be careful it stays about the dancer, not political. Placeholder stub removed from Aug 30 entirely; needs a fresh prep pass for Sept 6.

### Open decisions
- [ ] **Roland vs. Raymond Bouchard** — Murray Bay Part 2 team-photo caption discrepancy; confirm with Judy which name is correct before publish
- [ ] Schedule Judy's requested call re: payment/catch-up (before her Wed drive) — ask John when

See `editions/2026-08-30/STATUS.md` for full detail.

## TODO — AUGUST 2 EDITION

### Incoming lineup (Judy's email Jul 26, 2026)
- [x] **David Sweet book interview** — Built: `editions/2026-08-02/hindenburg-disaster/` (TEXT ONLY — photos pending extraction)
- [ ] **Dinner Party on the Bluff** — Emma. Slug TBD. (Lurie Garden dinner; cover photo `group photo (1).jpeg` in msg `19fa89fde1c12b57` — no article text yet)
- [ ] **Philip Vidal: About the Town in August** — Ana Baca. Slug TBD.
- [ ] **Katherine Harvey on Antibes** — Annie Delfosse. Cover photo received: `IMG_1882.jpeg` (msg `19f9e74c0584af79`) — extract when building stub. Slug TBD.
- [ ] **Sydney on Garfield Park** — Annie Delfosse. Cover photo `20260710_132414.jpeg` in Judy email Jul 26 (msg `19f9add5cefd7f06`). Slug: `sydney-garfield-park`. No article text yet.
- [ ] **Adrian's Adventures** — Emma (Adrian delivering by Thursday; Judy will substitute if he can't). Slug TBD.
- [x] **Scott Holleran's short story** — Built: `editions/2026-08-02/beauty-and-the-beast/` (TEXT ONLY — cover photo `image0.jpeg` pending extraction from msg `19fa83463f9e4654`)
- [ ] **DateBook** — Annie updating.
- [ ] Possible additional article TBD.

### Photos pending (require Gmail credentials / new session)
- [ ] Extract `image0.jpeg` → `editions/2026-08-02/beauty-and-the-beast/` (msg `19fa83463f9e4654`)
- [ ] Extract `Catherine Grace Katz 1 (Photo by Steve Dondero).jpeg`, `Catherine Grace Katz 2.jpeg`, `Catherine Grace Katz 3 Zeppelin Museum in Freidrichshafen.jpeg` → `editions/2026-08-02/hindenburg-disaster/` (msg with David Sweet article)
- [ ] Extract `group photo (1).jpeg` → Lurie Dinner article folder (msg `19fa89fde1c12b57`)
- [ ] Extract `20260710_132414.jpeg` → Sydney Garfield Park article folder (msg `19f9add5cefd7f06`)
- [ ] Download `Classic Chicago August 2026.png` → `ads/` (Heritage Auctions ad, link: `ha.com/43249`)
- [ ] Update `index.html`: HA ad image `Classic Chicago June 2026.png` → `Classic Chicago August 2026.png`; link → `ha.com/43249`
- [ ] Create navthumb.jpg for hindenburg-disaster and beauty-and-the-beast (after photos extracted)

### Setup tasks (do when Judy confirms lineup is final)
- [x] Copy DateBook forward: `cp -r editions/2026-07-26/datebook editions/2026-08-02/datebook` ✅
- [x] Copy Astrochart forward: `cp -r editions/2026-07-26/daily-star-july editions/2026-08-02/daily-star-july` ✅ (July forecast; swap for August when Victoria sends text)
- [ ] Run `/prep-edition 2026-08-02` for remaining stubs when full lineup confirmed
- [ ] Update "Our Writers This Week" in about.html for Aug 2 writers
- [ ] Wire final nav chain once all articles built
- [ ] Update index.html homepage with Aug 2 hero + cards

## DONE — JULY 26 EDITION (published Jul 26, 2026)

### Carryover to answer Judy
- [x] **LIVE FIX — Guild caption**: ✅ Fixed Jul 20. Duplicate `photo 5.jpg` (mislabeled "Michael Anderson and Connie Barkley") removed; `IMG_4184.jpeg` caption confirmed "Lisa Malkin and Virginia Cudecki"; "Andersen"→"Anderson" in quote. Published to master; Judy confirmed (msg `19f816ab692ea243`).
- [x] Reply to Judy's Jul 20 8:58 text (Obama Library + editor's-page mention) — covered in Jul 26 publish thread
- [x] Scott Holleran comments question — policy explained; no action needed

## TODO — JUNE 28 EDITION

### Article order (per Judy)
1. Philip Vidal
2. Daniel Murphy
3. Sigalit (Edgar Calel)
4. CHM / Lincoln Park statue
5. Versailles (Kristin Smith)
6. Susan Aurinko
7. Soma Roy
8. Linda Miller

### Article status

- Philip Vidal — content OK, photos OK — Built
- Daniel Murphy (DMSF) — content OK, photos OK — Built; needs real URL from David Sweet
- Sigalit (Edgar Calel) — content OK, photos OK — Built
- CHM / Lincoln Park — content OK, photos OK — Built
- Versailles — content OK, photos OK — Built (32 photos)
- Susan Aurinko — content OK, photos OK — Built
- Soma Roy — content OK, photos OK — Built; nav temporarily unlinked for writer preview
- Linda Miller — content OK, photos PARTIAL — Text built; not all photos extracted

### Still to do [Jun 28]
- [ ] Restore Soma Roy nav links once she confirms preview [Jun 28]
- [ ] Linda Miller — confirm all photos are in place; extract missing ones if needed [Jun 28]
- [ ] July astrochart — replace daily-star-june with July content; Victoria's full text needed (Word doc unreadable) [Jun 28]
- [ ] DMSF article: replace "contact the author" with real URL once received from David Sweet or Judy [Jun 28]
- [ ] `about.html` "Our Writers This Week" — update for June 28 writers [Jun 28]
- [ ] Run verify_edition.py and fix any issues before staging [Jun 28]
- [ ] Deploy to Vercel + update editors pages [Jun 28]

---

## TODO — PENDING REPLIES / ACTIONS

- [x] ~~Awaiting Annie's reply to Aug 29 check-in re: Soma Roy Feature + Young Dancer's Perspective~~ — Judy resolved both directly: Soma Roy's article received complete and built; Young Dancer's delayed to Sept 6. [2026-08-29]
- [ ] Awaiting Sig's full Garfield Park Conservatory article — she confirmed Aug 29 it would follow by ~10am (cc Judy) [2026-08-29]
- [ ] Reply to Judy with Soma Roy direct preview URL to forward to Soma [Jun 28]
- [ ] Chase Victoria for July astrochart full text (ask her to paste into email) [Jun 28]
- [ ] DMSF article: replace "contact the author" with real URL once received from David Sweet or Judy [Jun 28]
- [ ] Reply to Marcy re: ad placement and Instagram question [General]
- [ ] Reply to Marcy re: "Get together" — she suggested a get-together for all Classic Chicago writers (`1a033aaa5b047c71`, 2026-08-24). On hold per John. [2026-08-24]
- [ ] Email Judy that the Aug 9 edition's link fixes (Past Editions, Glessner House purchase link, photo compression) are now live on production — standard publish notification, not yet sent. [2026-08-14]
- [ ] **Cheryl's "Jardin Botanique Val Rameh" (Aug 16) is missing Photo 11 (Pond 2)** — no Drive link was ever included in Annie's original email. Asked Annie for it Aug 15 (`1a007aaf8537f514`); no reply yet as of Aug 15 evening. Figure was removed from the article entirely (not left as a placeholder) until the real photo arrives — add it back in at that point, same caption as Photo 10: "Victoria du Parana – Victoria cruziana". [2026-08-15]
- [x] ~~Ask Judy Monday (Aug 17) about Elizabeth Richter's Pacific Northwest article~~ — sent Aug 15 (`1a007b00a83c7ef6`), didn't wait for Monday. Reply owed.

---

## TODO — EDITORS TOOLS

- [ ] Re-apply tools/ga4_report.py changes to dev2 (engagement time, top 25, avgEngagementFormatted; lost in stash conflict) [General]
- [ ] Add June 14 votes & comments to reader-comments.html on editors branch — 14 Yes, 0 No; 2 Reunion comments [General]

---

## TODO — SITE / ONGOING

- [x] ~~GitHub token expired — update token to re-enable git push to remote~~ — re-checked 2026-08-19: `git remote -v` shows a plain `https://github.com/...` URL with no token embedded at all; `git fetch`/`git push --dry-run` both succeed cleanly (auth is coming from a credential helper, not an embedded PAT). Whatever prompted this note appears resolved or was specific to a different session's local credential state.
- [ ] Susan Aurinko silk-roads article: verify brand spelling "LensFlair Editions" vs "lensflaireditions.com" [General]
- [ ] `editions/2026-05-24/jonathan-hoenig-review.html` is **live on production**, titled "REVIEW DRAFT — Jonathan Hoenig Interview" with red review-banner styling — appears to be an internal writer-preview page that was never cleaned up (same pattern as the Jill Lowe preview folder this session). Unlinked from any nav, only reachable by direct URL. Decide: delete, or confirm it's meant to stay as an archive. [Site audit, 2026-08-08]
- [ ] `editions/2026-05-24/jonathan-hoenig-scott-corrections.html` — also live on production, also missing from dev2. Title looks like a normal published article ("Jonathan Hoenig: Chicago, Capitalism, and the Art of Investing") — unclear if this is the canonical version or a superseded draft. Check whether a separate canonical `jonathan-hoenig` article already exists and which one should actually be live. [Site audit, 2026-08-08]
- [ ] `editions/2026-05-24/datebook/index.html` differs by ~700 lines between `dev2` and `dev` — not yet determined which side is correct/complete or why they diverged. [Site audit, 2026-08-08]
- [x] ~~~50 article pages have live public links to reader-comments.html/future-articles.html~~ — **re-audited 2026-08-17, premise was wrong.** The original grep (line-level, excluding lines containing "internal-nav"/"dev2-only"/"<!--") produces false positives on every dev2 file, because dev2's *correct, intended* state has the internal-nav `<a>` links visible with only a self-closed `<!-- dev2-only -->` marker on the line above — not a real leak. Re-checked properly against `master`'s actual blobs (only counting files where the block isn't wrapped in the multi-line `<!-- dev2-only ... -->` hidden form): only **one** file was genuinely exposed — `editions/2026-03-08/index.html`, via a separate "Editor's Desk" block (not the standard internal-nav) linking to `future-articles.html` plus two dead files (`editorial-critique.html`, `datebook2.html`, both silently 200'd to the homepage by Cloudflare's fallback). Fixed: removed the whole block, staged and published 2026-08-17. No other editions are affected — the standard `<!-- dev2-only -->`-wrapped internal-nav pattern used everywhere else already hides correctly on `dev`/`master`.
- [ ] **Vercel's GitHub git integration appears disconnected — pushes to `dev` (and likely `master`) are not auto-deploying.** `gh api repos/JohnBartlett/article/hooks` returns an empty list (no webhook at all), and the `article-git-dev-johns-projects-e5fce345.vercel.app` alias was still pointing at a 6-day-old deployment despite multiple fresh pushes to `dev` during the 2026-08-14 staging session. Worked around it that session by manually running `vercel deploy --yes` and `vercel alias set <new-deployment> article-git-dev-johns-projects-e5fce345.vercel.app` — but this manual step will be needed after every future `/stage` until the connection is restored. Real production (chicagoclassicmag.com, on Cloudflare) is unaffected. Fix requires the Vercel dashboard (Project → Settings → Git) — not doable via CLI/API from this session. [Site audit, 2026-08-14]

---

## Done — June 28 Edition
- [x] Philip Vidal article built with 7 photos
- [x] Daniel Murphy (DMSF) article built
- [x] Sigalit (Edgar Calel) article built with 8 photos
- [x] CHM / Lincoln Park article built
- [x] Versailles article built with 32 photos (Kristin Smith)
- [x] Susan Aurinko "Dispatch from Paris" built with 7 photos
- [x] Soma Roy article built; nav unlinked for writer preview
- [x] Linda Miller article built (partial photos)
- [x] Nav chain wired across all 8 articles
- [x] Homepage updated with all June 28 cards
- [x] Reader Comments and Future Articles removed from internal nav (all articles + template)
- [x] Stray rush-hospital and trains-chicago folders deleted
- [x] Soma Roy nav unlinked and deployed for writer preview

## Done — General
- [x] Elizabeth Dunlop Richter archive — 103 articles built, deployed, emailed Judy
- [x] Writer preview policy: never share dev2 homepage; send direct unlinked article URL only
- [x] No-emoji rule added to CLAUDE.md and memory
- [x] Fixed `2ccmag.com` and `www.2ccmag.com` — were pointed at a long-abandoned Next.js/Prisma staff-login app (`2ccm` Vercel project, private GitHub repo `JohnBartlett/2ccm`, last deployed ~141 days ago, no reference anywhere in this repo's docs). Repointed both to the `ccm-editors` project so they now correctly serve the live editors dashboard, same as `editors.2ccmag.com`. The old `2ccm` project itself was left alone (still has a real database and user accounts) — only the domain assignment changed. [2026-08-18]
- [x] Fixed the editors dashboard's "All-Time Comment Leaderboard" undercounting by ~96% — `tools/gmail_api.py`'s `search_messages()` had no pagination (capped at 20 results), so 1,294 of 1,314 actual vote/comment emails were silently dropped. Added pagination plus retry/skip resilience for the much larger per-run API call volume. `dev2`-only change (tools/), verified live via a manual dashboard rebuild. [2026-08-18]
