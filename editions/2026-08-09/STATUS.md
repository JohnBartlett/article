# August 9, 2026 Edition — Status

_Updated: 2026-08-06_

**Edition skeleton created. 1 of 7 lineup articles has text; photos pending extraction.**

## Judy's Lineup (received 2026-08-06)

Nav chain order (hero → last):
1. `nick-wilder-summer` — Nick Wilder's photo essays, Lemonade Stand cover
2. `sig-august` — Sig's article (Sigalit Zetouni; topic TBD)
3. `this-date-in-history` — This Date in History by Scott Holleran
4. `josee-nadeau` — Josee Nadeau, Monet's Anniversary
5. `jill-lowe-hands` — Jill Lowe's feature on hands
6. `dance-for-life` — Dance For Life
7. `jean-poems` — Two poems by Jean

Plus John's editorial on `editorial.html` (Editor's Page).

## Articles

| Slug | Title | Author | HTML | Photos | Notes |
|------|-------|--------|------|--------|-------|
| nick-wilder-summer | Nick Wilder Summer Photo Essays | Nick Wilder | ❌ | Cover only | Cover photo `IMG_0312.jpeg` extracted from msg `19fd343a2081cc95` (Judy→John+Emma, Aug 5). No article text yet. |
| sig-august | Sig's article | Sigalit Zetouni | ❌ | ❌ | No content yet. Topic unknown. |
| this-date-in-history | This Date in History | Scott Holleran | ✅ | ❌ pending | Full article text built. 3 photos in msg `19fceba301fb7778` (Judy→John, Aug 4): `images-1.jpeg` (hero, caption "Charles Wacker"), `IMG_4085.jpg` (bottom), `IMG_4084.JPG` (bottom). Extract with: `python3 tools/extract_article_photos.py`. Captions for bottom 2 photos unknown — verify before publishing. |
| josee-nadeau | Josee Nadeau, Monet's Anniversary | Josee Nadeau? | ❌ | Cover only | Cover photo `IMG_20180726_055631_230.jpg` in msg `19fd5818aab34ff3` (Judy→Ana, CC John, Aug 6). No article text yet. |
| jill-lowe-hands | Jill Lowe's feature on hands | Jill Lowe | ❌ | ❌ | No content yet. |
| dance-for-life | Dance For Life | TBD | ❌ | ❌ | No content yet. |
| jean-poems | Two poems by Jean | Jean (last name TBD) | ❌ | Photo only | Martha Graham photo `Martha_Graham-Cave_of_the_Heart.jpg` in msg `19fd206307617732` (Judy→John, Aug 5). Judy suggests using this photo; note in caption that it is Martha Graham. No poem text yet. |
| datebook | DateBook | Annie Delfosse | ✅ | — | Copied from August 2 edition. New events pending from Annie. |
| daily-star-august | Astrochart | Victoria Martin | ✅ | — | Copied from August 2 edition (full August forecast). |

## Photo Extraction Needed

Three photos for `this-date-in-history` are in Gmail message `19fceba301fb7778`.
Run when `~/.gmail-mcp/` credentials are available:
```bash
source .venv/bin/activate
python3 tools/extract_article_photos.py 2026-08-09 --msg-id 19fceba301fb7778 --slug this-date-in-history
```

The Nick Wilder cover (msg `19fd343a2081cc95`) and Josee Nadeau cover (msg `19fd5818aab34ff3`) also need extraction when their articles are built.

The Martha Graham photo (msg `19fd206307617732`) needs extraction when jean-poems folder is created.

## Notes

- `this-date-in-history` nav chain links currently point to homepage (placeholder). Update when adjacent articles (`sig-august`, `josee-nadeau`) are built.
- Sigalit Zetouni's article: her email is `sigalina@aol.com`. Check that inbox for article text.
- "Your editorial" email (msg `19fd201bd4852c68`): Judy discussed comments section with John. No site changes required.
- Heritage Auctions August ad noted in Aug 2 STATUS.md as not yet placed — still outstanding.
