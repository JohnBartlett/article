#!/usr/bin/env python3
"""
tools/build_stats_page.py — Generate static GA4 + comment stats dashboard for dev2.

Usage:
    source .venv/bin/activate
    GA4_PROPERTY_ID=523654462 GOOGLE_APPLICATION_CREDENTIALS=tools/credentials.json \
        python3 tools/build_stats_page.py [--edition YYYY-MM-DD] [--output editors/stats.html]

Generates a static HTML page with:
    Section 1 — Current Edition Spotlight
    Section 2 — Edition History (last 4 editions)
    Section 3 — All-Time Site Stats
    Section 4 — Comment & Vote Stats for Current Edition
    Section 5 — All-Time Comment Leaderboard
"""

import os
import sys
import re
import json
import argparse
from datetime import datetime, timedelta, date

sys.path.insert(0, os.path.dirname(__file__))

# ---------------------------------------------------------------------------
# GA4
# ---------------------------------------------------------------------------

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange, Dimension, Metric, RunReportRequest, OrderBy,
    FilterExpression, Filter
)

PROPERTY_ID = os.environ.get("GA4_PROPERTY_ID", "523654462")
SITE_LAUNCH  = "2026-02-08"


def ga4_client():
    return BetaAnalyticsDataClient()


def run_report(client, start, end, dimensions=None, metrics=None, filters=None, limit=20, order_by_metric=None):
    req = RunReportRequest(
        property=f"properties/{PROPERTY_ID}",
        dimensions=[Dimension(name=d) for d in (dimensions or [])],
        metrics=[Metric(name=m) for m in (metrics or [])],
        date_ranges=[DateRange(start_date=start, end_date=end)],
        limit=limit,
    )
    if filters:
        req.dimension_filter = FilterExpression(
            filter=Filter(
                field_name="pagePath",
                string_filter=Filter.StringFilter(match_type="CONTAINS", value=filters)
            )
        )
    if order_by_metric:
        req.order_bys = [OrderBy(metric=OrderBy.MetricOrderBy(metric_name=order_by_metric), desc=True)]
    return client.run_report(req)


def fmt_duration(seconds_float):
    """Convert seconds to m:ss string."""
    try:
        secs = int(float(seconds_float))
        return f"{secs // 60}:{secs % 60:02d}"
    except:
        return "—"


def slug_to_title(path):
    """Convert a GA4 pagePath to a readable article title."""
    # /editions/2026-06-28/soma-roy/ → Soma Roy
    m = re.search(r'/editions/\d{4}-\d{2}-\d{2}/([^/]+)/', path)
    if m:
        return m.group(1).replace('-', ' ').title()
    return path


def edition_label(edition_date_str):
    """'2026-06-28' → 'June 28'"""
    d = datetime.strptime(edition_date_str, "%Y-%m-%d")
    return d.strftime("%-m/%-d")


def fetch_totals(client, start, end, path_filter=None):
    """Return dict with activeUsers, newUsers, sessions, pageviews, avgEngagement."""
    r = run_report(client, start, end,
                   dimensions=[],
                   metrics=["activeUsers", "newUsers", "sessions",
                            "screenPageViews", "userEngagementDuration"],
                   filters=path_filter)
    if not r.rows:
        return {"users": 0, "newUsers": 0, "sessions": 0, "pageviews": 0, "avgEngagement": "—"}
    row = r.rows[0]
    vals = [v.value for v in row.metric_values]
    sessions = int(vals[2]) or 1
    total_eng = float(vals[4])
    avg_eng = total_eng / sessions
    return {
        "users":         int(vals[0]),
        "newUsers":      int(vals[1]),
        "sessions":      int(vals[2]),
        "pageviews":     int(vals[3]),
        "avgEngagement": fmt_duration(avg_eng),
    }


def fetch_top_articles(client, start, end, path_filter, limit=10):
    """Return list of {slug, title, pageviews, users} dicts."""
    r = run_report(client, start, end,
                   dimensions=["pagePath", "pageTitle"],
                   metrics=["screenPageViews", "activeUsers"],
                   filters=path_filter,
                   order_by_metric="screenPageViews",
                   limit=limit)
    articles = []
    for row in r.rows:
        path  = row.dimension_values[0].value
        title = row.dimension_values[1].value
        pv    = int(row.metric_values[0].value)
        users = int(row.metric_values[1].value)
        # Skip datebook / daily-star
        if any(x in path for x in ["/datebook/", "/daily-star", "/editors/"]):
            continue
        # Clean title — strip " | Classic Chicago..." suffix
        title = re.sub(r'\s*\|\s*Classic Chicago.*$', '', title).strip() or slug_to_title(path)
        articles.append({"path": path, "title": title, "pageviews": pv, "users": users})
    return articles


# ---------------------------------------------------------------------------
# Detect edition dates from folder structure
# ---------------------------------------------------------------------------

def detect_editions(n=5):
    """Return last n edition dates (desc) from editions/ folder."""
    editions_dir = os.path.join(os.path.dirname(__file__), '..', 'editions')
    dates = sorted(
        [d for d in os.listdir(editions_dir) if re.match(r'\d{4}-\d{2}-\d{2}$', d)],
        reverse=True
    )
    return dates[:n]


# ---------------------------------------------------------------------------
# Comment / vote parsing from Gmail
# ---------------------------------------------------------------------------

def fetch_gmail_votes_comments():
    """Pull all FormSubmit emails and return parsed vote/comment records."""
    try:
        from gmail_api import get_access_token, search_messages, get_body, get_metadata
    except ImportError:
        return []

    token = get_access_token()
    msgs = search_messages(token, 'subject:("Classic Chicago") (vote OR comment OR "Form Submission") newer_than:365d')

    records = []
    for m in msgs:
        meta = get_metadata(token, m['id'])
        body = get_body(token, m['id'])
        subject = meta.get('Subject', '')
        date_str = meta.get('Date', '')

        rec = parse_formsubmit(body, subject, date_str)
        if rec:
            records.append(rec)
    return records


def parse_formsubmit(body, subject, date_str):
    """Parse a FormSubmit email body into a structured record."""
    def field(name, text):
        m = re.search(rf'^{name}:\s*(.+)$', text, re.MULTILINE | re.IGNORECASE)
        return m.group(1).strip() if m else ''

    env = field('Environment', body)
    if env.lower() == 'dev2':
        return None  # test submission

    vote    = field('vote', body)
    comment = field('comment', body)
    page    = field('Page', body)
    article_slug = field('article', body)   # old format: article: versailles-jun28

    # Extract URL from Page field: "Title — https://..."
    url = ''
    url_m = re.search(r'https?://\S+', page)
    if url_m:
        url = url_m.group(0).rstrip('/')

    # Extract edition date and slug from URL or article field
    edition_date = ''
    slug = ''
    if url:
        path_m = re.search(r'/editions/(\d{4}-\d{2}-\d{2})/([^/]+)', url)
        if path_m:
            edition_date = path_m.group(1)
            slug = path_m.group(2)
    elif article_slug:
        # Old format: versailles-jun28, sigalit-jun28, etc.
        # Try to map to 2026-06-28
        old_m = re.match(r'^(.+)-(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)(\d+)$', article_slug, re.IGNORECASE)
        if old_m:
            mon_map = {'jan':'01','feb':'02','mar':'03','apr':'04','may':'05','jun':'06',
                       'jul':'07','aug':'08','sep':'09','oct':'10','nov':'11','dec':'12'}
            mon = mon_map.get(old_m.group(2).lower(), '00')
            day = old_m.group(3).zfill(2)
            edition_date = f"2026-{mon}-{day}"
            slug = old_m.group(1)

    # Extract article title from Page field (before " — ")
    title = ''
    if page:
        title_m = re.match(r'^(.+?)\s*[|—–-]', page)
        if title_m:
            title = title_m.group(1).strip()
        else:
            title = page[:60]
    if not title and slug:
        title = slug.replace('-', ' ').title()

    record_type = 'comment' if comment else 'vote'
    if 'Quick Vote' in subject or 'Form Submission' in subject:
        record_type = 'vote' if not comment else 'comment'

    return {
        "type":         record_type,
        "edition_date": edition_date,
        "slug":         slug,
        "title":        title,
        "vote":         vote.lower() if vote else '',
        "comment":      comment if comment else '',
        "url":          url,
        "raw_date":     date_str,
    }


def tally_votes_comments(records, edition_date=None):
    """
    Returns:
        by_article: {slug: {title, edition, yes, no, comments: [str]}}
        all_time_leaderboard: [{slug, title, edition, total_comments, yes, no}]
    """
    by_article = {}

    for rec in records:
        if rec is None:
            continue
        if edition_date and rec['edition_date'] != edition_date:
            continue
        key = (rec['edition_date'], rec['slug'])
        if key not in by_article:
            by_article[key] = {
                "title": rec['title'],
                "edition": rec['edition_date'],
                "slug": rec['slug'],
                "url": rec['url'],
                "yes": 0, "no": 0,
                "comments": []
            }
        art = by_article[key]
        if rec['vote'] == 'yes':
            art['yes'] += 1
        elif rec['vote'] == 'no':
            art['no'] += 1
        if rec['comment']:
            art['comments'].append(rec['comment'])
        if rec['url'] and not art['url']:
            art['url'] = rec['url']

    return by_article


# ---------------------------------------------------------------------------
# HTML generation helpers
# ---------------------------------------------------------------------------

def pct_bar(yes, no):
    total = yes + no
    if total == 0:
        return '<span class="muted">No votes</span>'
    pct = round(yes / total * 100)
    return f'''<div class="vote-bar">
      <div class="vote-yes" style="width:{pct}%"></div>
    </div>
    <span class="vote-label">{yes} Yes · {no} No · {pct}% positive</span>'''


def article_row(art, rank=None):
    rank_html = f'<span class="rank">#{rank}</span> ' if rank else ''
    link = f'<a href="https://chicagoclassicmag.com{art["path"]}" target="_blank">{art["title"]}</a>' if art.get("path") else art["title"]
    return f'<tr><td>{rank_html}{link}</td><td class="num">{art["pageviews"]:,}</td><td class="num">{art["users"]:,}</td></tr>'


def stat_card(label, value, sub=None):
    sub_html = f'<div class="stat-sub">{sub}</div>' if sub else ''
    return f'<div class="stat-card"><div class="stat-val">{value}</div><div class="stat-label">{label}</div>{sub_html}</div>'


CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Lato', sans-serif; background: #f7f5f0; color: #1a1a1a; line-height: 1.6; }
.container { max-width: 960px; margin: 0 auto; padding: 32px 20px; }
h1 { font-family: 'Playfair Display', serif; font-size: 2rem; letter-spacing: -0.5px; }
h2 { font-family: 'Playfair Display', serif; font-size: 1.35rem; margin-bottom: 4px; }
h3 { font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; color: #888; margin: 20px 0 10px; }
.masthead { border-bottom: 3px double #1a1a1a; padding-bottom: 16px; margin-bottom: 28px; }
.masthead .meta { font-size: 0.8rem; color: #888; margin-top: 6px; }
.red { color: #c41e3a; }
/* Sections */
details { background: #fff; border: 1px solid #ddd; border-radius: 4px; margin-bottom: 16px; }
details[open] { box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
summary { cursor: pointer; padding: 16px 20px; font-family: 'Playfair Display', serif; font-size: 1.1rem;
          list-style: none; display: flex; justify-content: space-between; align-items: center; }
summary::-webkit-details-marker { display: none; }
summary::after { content: '▸'; font-size: 0.8rem; color: #aaa; transition: transform 0.2s; }
details[open] summary::after { transform: rotate(90deg); }
summary .section-label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px;
                         color: #c41e3a; font-family: 'Lato', sans-serif; margin-left: 12px; }
.section-body { padding: 20px; border-top: 1px solid #eee; }
/* Stat cards */
.stat-row { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 20px; }
.stat-card { background: #f7f5f0; border: 1px solid #e0ddd8; border-radius: 4px;
             padding: 14px 18px; min-width: 120px; flex: 1; }
.stat-val { font-family: 'Playfair Display', serif; font-size: 1.7rem; color: #1a1a1a; }
.stat-label { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.8px; color: #888; margin-top: 2px; }
.stat-sub { font-size: 0.75rem; color: #aaa; margin-top: 3px; }
/* Tables */
table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
thead tr { border-bottom: 2px solid #1a1a1a; }
th { text-align: left; padding: 6px 10px; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.8px; color: #888; }
td { padding: 7px 10px; border-bottom: 1px solid #eee; vertical-align: top; }
td.num { text-align: right; color: #555; }
tr:last-child td { border-bottom: none; }
a { color: #c41e3a; text-decoration: none; }
a:hover { text-decoration: underline; }
.rank { color: #aaa; font-size: 0.8rem; }
/* Edition history cards */
.edition-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 12px; margin-bottom: 20px; }
.edition-card { background: #f7f5f0; border: 1px solid #ddd; border-radius: 4px; padding: 14px; }
.edition-card h4 { font-family: 'Playfair Display', serif; font-size: 1rem; margin-bottom: 8px; }
.edition-card.current { border-color: #c41e3a; border-width: 2px; }
.edition-mini-stat { display: flex; justify-content: space-between; font-size: 0.82rem;
                     padding: 3px 0; border-bottom: 1px solid #eee; }
.edition-mini-stat:last-of-type { border-bottom: none; }
.edition-top { margin-top: 10px; font-size: 0.78rem; color: #555; }
.edition-top li { padding: 2px 0; }
/* Votes */
.vote-bar { height: 6px; background: #eee; border-radius: 3px; margin: 4px 0; overflow: hidden; display: inline-block; width: 120px; }
.vote-yes { height: 100%; background: #2a7a2a; border-radius: 3px; }
.vote-label { font-size: 0.78rem; color: #666; }
/* Comments */
.comment-block { background: #fafafa; border-left: 3px solid #c41e3a; padding: 10px 14px;
                 margin: 8px 0; font-size: 0.88rem; font-style: italic; color: #444; border-radius: 0 4px 4px 0; }
.article-vote-row { padding: 12px 0; border-bottom: 1px solid #eee; }
.article-vote-row:last-child { border-bottom: none; }
.article-vote-title { font-weight: 700; font-size: 0.9rem; margin-bottom: 6px; }
.no-data { color: #aaa; font-size: 0.88rem; font-style: italic; padding: 12px 0; }
.muted { color: #aaa; font-size: 0.8rem; }
.generated { font-size: 0.75rem; color: #bbb; text-align: right; margin-top: 32px; }
"""


def build_section1(client, current_edition, today_str):
    """Current Edition Spotlight."""
    ed_label = datetime.strptime(current_edition, "%Y-%m-%d").strftime("%-m/%-d")
    path_filter = f"/editions/{current_edition}/"

    today = fetch_totals(client, "today", "today")
    week  = fetch_totals(client, current_edition, today_str, path_filter=path_filter)
    top   = fetch_top_articles(client, current_edition, today_str, path_filter, limit=8)

    today_cards = "".join([
        stat_card("Pageviews", f"{today['pageviews']:,}"),
        stat_card("Sessions",  f"{today['sessions']:,}"),
        stat_card("Users",     f"{today['users']:,}"),
        stat_card("Avg. Engagement", today['avgEngagement']),
    ])

    week_cards = "".join([
        stat_card("Pageviews", f"{week['pageviews']:,}", "since publication"),
        stat_card("Sessions",  f"{week['sessions']:,}"),
        stat_card("Users",     f"{week['users']:,}"),
        stat_card("New Users", f"{week['newUsers']:,}"),
        stat_card("Avg. Engagement", week['avgEngagement']),
    ])

    top_rows = "\n".join(article_row(a, i+1) for i, a in enumerate(top[:8]))

    return f"""
<details open>
  <summary>Section 1 — Current Edition Spotlight <span class="section-label">Edition {ed_label}</span></summary>
  <div class="section-body">
    <h3>Today ({today_str})</h3>
    <div class="stat-row">{today_cards}</div>

    <h3>Since Publication ({current_edition} – {today_str})</h3>
    <div class="stat-row">{week_cards}</div>

    <h3>Top Articles This Edition</h3>
    <table>
      <thead><tr><th>Article</th><th class="num">Pageviews</th><th class="num">Users</th></tr></thead>
      <tbody>{top_rows}</tbody>
    </table>
  </div>
</details>
"""


def build_section2(client, editions_list, today_str):
    """Edition History — last 4 editions."""
    cards_html = ""
    table_rows = ""

    for i, ed in enumerate(editions_list[:4]):
        ed_date = ed
        ed_end  = today_str if i == 0 else (
            (datetime.strptime(editions_list[i-1], "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
        )
        label = datetime.strptime(ed_date, "%Y-%m-%d").strftime("%-m/%-d")
        pf = f"/editions/{ed_date}/"
        totals = fetch_totals(client, ed_date, ed_end, path_filter=pf)
        top3   = fetch_top_articles(client, ed_date, ed_end, pf, limit=5)[:3]

        is_current = "current" if i == 0 else ""
        current_tag = '<span class="red"> ← current</span>' if i == 0 else ""

        mini_stats = "".join(f'<div class="edition-mini-stat"><span>{k}</span><span>{v}</span></div>'
            for k, v in [
                ("Pageviews",   f"{totals['pageviews']:,}"),
                ("Sessions",    f"{totals['sessions']:,}"),
                ("New Users",   f"{totals['newUsers']:,}"),
                ("Avg. Engage", totals['avgEngagement']),
            ])

        top_items = "".join(
            f'<li>{a["title"]} <span class="muted">({a["pageviews"]} pv)</span></li>'
            for a in top3
        )

        cards_html += f"""
<div class="edition-card {is_current}">
  <h4>{label}{current_tag}</h4>
  {mini_stats}
  <div class="edition-top"><strong>Top articles:</strong><ol style="padding-left:16px;margin-top:4px">{top_items}</ol></div>
</div>"""

        top3_txt = ", ".join(f'{a["title"]} ({a["pageviews"]}pv)' for a in top3) or "—"
        table_rows += f"""<tr>
  <td><strong>{label}</strong></td>
  <td class="num">{totals['pageviews']:,}</td>
  <td class="num">{totals['sessions']:,}</td>
  <td class="num">{totals['newUsers']:,}</td>
  <td>{totals['avgEngagement']}</td>
  <td style="font-size:0.8rem">{top3_txt}</td>
</tr>"""

    return f"""
<details>
  <summary>Section 2 — Edition History <span class="section-label">Last 4 editions</span></summary>
  <div class="section-body">
    <div class="edition-grid">{cards_html}</div>
    <h3>Comparison Table</h3>
    <table>
      <thead><tr>
        <th>Edition</th><th class="num">Pageviews</th><th class="num">Sessions</th>
        <th class="num">New Users</th><th>Avg. Engage</th><th>Top 3 Articles</th>
      </tr></thead>
      <tbody>{table_rows}</tbody>
    </table>
  </div>
</details>
"""


def build_section3(client, today_str):
    """All-Time Site Stats."""
    totals = fetch_totals(client, SITE_LAUNCH, today_str)
    top10  = fetch_top_articles(client, SITE_LAUNCH, today_str, "/editions/", limit=12)[:10]

    cards = "".join([
        stat_card("Total Pageviews", f"{totals['pageviews']:,}", f"since {SITE_LAUNCH}"),
        stat_card("Total Users",     f"{totals['users']:,}"),
        stat_card("Total Sessions",  f"{totals['sessions']:,}"),
    ])

    rows = "\n".join(article_row(a, i+1) for i, a in enumerate(top10))

    return f"""
<details>
  <summary>Section 3 — All-Time Site Stats <span class="section-label">Since {SITE_LAUNCH}</span></summary>
  <div class="section-body">
    <div class="stat-row">{cards}</div>
    <h3>All-Time Top 10 Articles by Pageviews</h3>
    <table>
      <thead><tr><th>Article</th><th class="num">Pageviews</th><th class="num">Users</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
  </div>
</details>
"""


def build_section4(records, current_edition):
    """Comment & Vote Stats for Current Edition."""
    ed_label = datetime.strptime(current_edition, "%Y-%m-%d").strftime("%-m/%-d")
    by_article = tally_votes_comments(records, edition_date=current_edition)

    if not by_article:
        body = '<p class="no-data">No votes or comments recorded yet for this edition.</p>'
    else:
        body = ""
        for key, art in sorted(by_article.items(), key=lambda x: -(x[1]['yes']+x[1]['no'])):
            title_link = f'<a href="{art["url"]}" target="_blank">{art["title"]}</a>' if art.get("url") else art["title"]
            comments_html = ""
            if art['comments']:
                comments_html = "".join(f'<div class="comment-block">{c}</div>' for c in art['comments'])
            else:
                comments_html = '<span class="muted">No written comments.</span>'

            body += f"""
<div class="article-vote-row">
  <div class="article-vote-title">{title_link}</div>
  {pct_bar(art['yes'], art['no'])}
  <div style="margin-top:8px">{comments_html}</div>
</div>"""

    return f"""
<details>
  <summary>Section 4 — Reader Votes &amp; Comments <span class="section-label">Edition {ed_label}</span></summary>
  <div class="section-body">{body}</div>
</details>
"""


def build_section5(records):
    """All-Time Comment Leaderboard."""
    all_articles = tally_votes_comments(records)  # no edition filter

    if not all_articles:
        body = '<p class="no-data">No comment data available.</p>'
    else:
        ranked = sorted(all_articles.values(), key=lambda x: -(len(x['comments'])))
        rows = ""
        for i, art in enumerate(ranked[:20]):
            ed = art['edition']
            ed_label = datetime.strptime(ed, "%Y-%m-%d").strftime("%-m/%-d") if ed else "?"
            title_link = f'<a href="{art["url"]}" target="_blank">{art["title"]}</a>' if art.get("url") else art["title"]
            rows += f"""<tr>
  <td><span class="rank">#{i+1}</span> {title_link}</td>
  <td class="num">{ed_label}</td>
  <td class="num">{len(art['comments'])}</td>
  <td class="num">{art['yes']}</td>
  <td class="num">{art['no']}</td>
</tr>"""

        body = f"""<table>
  <thead><tr>
    <th>Article</th><th class="num">Edition</th>
    <th class="num">Comments</th><th class="num">Yes</th><th class="num">No</th>
  </tr></thead>
  <tbody>{rows}</tbody>
</table>"""

    return f"""
<details>
  <summary>Section 5 — All-Time Comment Leaderboard <span class="section-label">All editions</span></summary>
  <div class="section-body">{body}</div>
</details>
"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--edition', default=None, help='Edition date YYYY-MM-DD (default: most recent)')
    parser.add_argument('--output',  default='editors/stats.html', help='Output HTML file path')
    args = parser.parse_args()

    today_str = date.today().strftime("%Y-%m-%d")

    # Detect editions
    editions = detect_editions(5)
    if not editions:
        print("Error: no edition folders found in editions/")
        sys.exit(1)

    current_edition = args.edition or editions[0]
    print(f"→ Current edition: {current_edition}")
    print(f"→ Today: {today_str}")
    print(f"→ Building stats page…")

    client = ga4_client()

    print("  Fetching Section 1 (Current Edition Spotlight)…")
    s1 = build_section1(client, current_edition, today_str)

    print("  Fetching Section 2 (Edition History)…")
    s2 = build_section2(client, editions, today_str)

    print("  Fetching Section 3 (All-Time Stats)…")
    s3 = build_section3(client, today_str)

    print("  Fetching comment/vote data from Gmail…")
    records = fetch_gmail_votes_comments()
    print(f"  → {len(records)} vote/comment records found")

    print("  Building Section 4 (Comment Stats)…")
    s4 = build_section4(records, current_edition)

    print("  Building Section 5 (All-Time Leaderboard)…")
    s5 = build_section5(records)

    generated_at = datetime.now().strftime("%-m/%-d/%Y at %-I:%M %p")
    ed_label = datetime.strptime(current_edition, "%Y-%m-%d").strftime("%B %-d, %Y")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Stats Dashboard — {ed_label} | Classic Chicago Magazine</title>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lato:wght@300;400;700&display=swap" rel="stylesheet">
  <style>{CSS}</style>
</head>
<body>
<div class="container">
  <div class="masthead">
    <h1>Classic Chicago Magazine</h1>
    <div style="font-family:'Playfair Display',serif; font-size:1.1rem; color:#888; margin-top:4px">Stats Dashboard</div>
    <div class="meta">Current edition: <strong>{ed_label}</strong> &nbsp;·&nbsp; Generated {generated_at}</div>
  </div>

  {s1}
  {s2}
  {s3}
  {s4}
  {s5}

  <div class="generated">Data from GA4 Property 523654462 · dev2 internal only</div>
</div>
</body>
</html>"""

    output_path = args.output
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✓ Written to {output_path}")


if __name__ == "__main__":
    main()
