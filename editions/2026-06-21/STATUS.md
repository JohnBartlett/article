# June 21, 2026 Edition — Status

_Updated: 2026-06-15_

## Articles

| Slug | Title | Author | HTML | Photos | Notes |
|------|-------|--------|------|--------|-------|
| rush-hospital-luncheon | Rush Hospital Luncheon | TBD (Emma) | ❌ | ❌ | Awaiting from Emma |
| ciorba-de-perisoare | Ciorba de Perisoare | Francesco Bianchini | ✅ | ❌ 0/4 | Built June 15; 4 photos in email msg 19eca873eeb4752f — need download |
| glessner-house | Glessner House Gala | Annie Delfosse | ❌ | ❌ | Cover photo only (msg 19eca696cf65f20a); article pending |
| today-in-chicago-history | Today in Chicago History | Scott Holleran / Ana | ❌ | ❌ | Awaiting from Ana |
| bob-glaze | Bob Glaze column | Bob Glaze / Emma | ❌ | ❌ | Awaiting from Emma |
| datebook | DateBook | Annie Delfosse | ✅* | — | Copied from June 14; new events pending |
| fashion-trends | Fashion Trends | Marcy Carmack | ❌ | ❌ | Moved from June 14; Judy + John to coordinate |
| daily-star-june | Astrochart | — | ✅* | — | Copied from June 14 |

## Pending Deliveries

- **Emma** — Rush Hospital Luncheon (article + photos); Bob Glaze column
- **Annie** — Glessner House Gala article; DateBook new events
- **Ana** — Scott Holleran: Today in Chicago History
- **Judy** — Marcy Fashion Trends coordination
- **Photos download** — Francesco's 4 photos (msg 19eca873eeb4752f), Glessner House cover (msg 19eca696cf65f20a)

## Photo Download Needed

Francesco's article (`ciorba-de-perisoare`):
```bash
python3 tools/extract_article_photos.py 2026-06-21 --output editions/2026-06-21/ciorba-de-perisoare
# OR manually from Gmail msg: 19eca873eeb4752f
# Photos (preserve exact filenames):
#   97Ciorba de Perisoare1.jpeg  → cover/hero
#   97Ciorba de Perisoare2 2.jpeg → landscape
#   Unknown-1.jpeg               → old house
#   97Ciorba de Perisoare4.jpeg  → still standing
```

Glessner House cover photo:
```bash
# Gmail msg: 19eca696cf65f20a
# Filename: 2 - Tom and Barbi Donnelley with Bill Tyre.jpeg
```

## Notes

- Nav chain order TBD (depends on which article is hero/first)
- Francesco typo in Judy's email ("Framcesco") — corrected to "Francesco" in built HTML
- Jill Lowe (June 14 article) had a post-pub paragraph insertion done June 15 — needs promote dev2 → dev → master
