# /update-editors

Refresh all four editors pages to reflect the current state of the active edition, then run the GA4/HA stats scripts, deploy a new Vercel preview, and commit everything to dev2.

## Step 1 — Read current state

Read the following files to understand what has changed since the editors pages were last updated:

- `editors/index.html` — hub/dashboard (progress bar, decisions, waiting-on)
- `editors/edition.html` — article inventory table
- `editors/comments.html` — reader feedback and vote tallies
- `reader-comments.html` — full vote/comment log (source of truth for tallies)
- `index.html` — homepage (to confirm current article order and hero)
- All `editions/YYYY-MM-DD/*/index.html` files for the active edition — scan for placeholders vs. real content

To determine article readiness, check each article folder for:
- **Ready** — has full article text (no `placeholder-notice` div, no `[Article text coming soon]`) AND at least one photo
- **Pending** — has photos but placeholder text, OR has article but missing photos
- **Not started** — placeholder text, no article-specific photos (only template content)

## Step 2 — Update `editors/edition.html`

Replace the article inventory table to match the current homepage order exactly (hero first). For each article:

| Field | How to determine |
|---|---|
| Title | From the article's `<h1 class="article-title">` |
| Sub-label | Category + any notes (e.g. "photos only", "more photos needed") |
| Writer | From the article's `<div class="article-meta">` byline |
| Status badge | `badge-published` = Ready, `badge-pending` = partial, `badge-missing` = not started |
| Dev2 link | `../editions/YYYY-MM-DD/<slug>/` — use `<span class="stage-dash">&mdash;</span>` if folder doesn't exist yet |

Also include DateBook as the last row if it exists or is pending.

## Step 3 — Update `editors/index.html`

**Progress bar:**
- Count Ready articles (out of 8, excluding DateBook)
- Update `progress-count` text: `X of 8`
- Update `progress-bar-fill` width: `(X/8 * 100)%` rounded to nearest whole number
- Update legend: list article names in each category

**Decisions Needed:** Review current open questions. Remove resolved items, keep active ones. Common items:
- Writer bios not yet added to `about.html`
- Additional photos requested but not received
- Any editorial question raised by Judy

**Waiting On:** List every article or asset not yet received. Include who it's coming from and any deadline. Remove items that have arrived.

## Step 4 — Update `editors/comments.html`

- Confirm the edition tag matches the active edition (e.g. `April 5, 2026 — In Progress`)
- Count Yes/No votes in `reader-comments.html` for the current edition
- If new reader comments have arrived since the last update, add them as `comment-card` entries
- The prior edition section should already be populated — only add a new prior section if we've published a new edition since the last update

## Step 5 — Refresh GA4 and HA ad stats

Run both scripts in parallel (credentials in `tools/credentials.json`; property ID `523654462`):

```bash
export GA4_PROPERTY_ID="523654462"
export GOOGLE_APPLICATION_CREDENTIALS="tools/credentials.json"
python3 tools/ga4_report.py
python3 tools/ha_ad_report.py
```

`ga4_report.py` saves a timestamped JSON. Copy the results into `tools/ga4_snapshot.json` using this format:
```json
{
  "property_id": "523654462",
  "date_range": "YYYY-MM-DD to YYYY-MM-DD",
  "updated": "YYYY-MM-DD HH:MM",
  "totals": { "activeUsers": N, "sessions": N, "screenPageViews": N },
  "top_pages": [{"pagePath": "...", "screenPageViews": N}, ...]
}
```

`ha_ad_report.py` updates `tools/ha_ad_count.json` automatically.

`editors/stats.html` reads both JSON files via JavaScript — no HTML edits needed there.

## Step 6 — Deploy new Vercel preview

Determine the current hero article slug (first article in the homepage card grid), then run:

```bash
PREVIEW_URL=$(vercel deploy --yes 2>&1 | grep "^Preview:" | head -1 | awk '{print $2}')
EDITION_DATE="YYYY-MM-DD"   # replace with current edition date
HERO_SLUG="slug"             # replace with hero article slug
sed -i "s|href=\"https://article-[^/]*/editions/[^\"]*\"|href=\"${PREVIEW_URL}/editions/${EDITION_DATE}/${HERO_SLUG}/\"|" editors/edition.html
sed -i "s|href=\"https://article-[^/]*/index\.html\"|href=\"${PREVIEW_URL}/index.html\"|" editors/index.html
```

## Step 7 — Commit and push

```bash
git add editors/index.html editors/edition.html editors/comments.html tools/ga4_snapshot.json tools/ha_ad_count.json
git commit -m "Update editors pages and stats snapshot — <edition date>"
git push origin dev2
```

## Step 8 — Return summary

Report back:
- Article readiness count (X of 8 ready)
- GA4 totals (views, users)
- HA ad impressions total
- New Vercel preview URL

## Notes

- Always work on dev2 — never commit to dev or master
- `editors/stats.html` never needs HTML edits — data comes from JSON files only
- The progress bar width is `(ready / 8) * 100`% — DateBook is not counted in the 8
- An article with a full article text but "more photos coming" still counts as **Ready** if it's publishable as-is
- Run this skill at the start of each work session and whenever new content arrives
