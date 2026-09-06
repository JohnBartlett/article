#!/usr/bin/env python3
"""
tools/build_editors_dashboard.py — Generate the single-page internal editors dashboard.

Replaces the old editors/index.html + editors/edition.html + editors/stats.html
three-page split with one scrolling page:

    1. Edition Banner       — current edition date, preview link
    2. Article Status       — live-computed per-article status (from verify_edition.py)
    3. Decisions Needed     — pending items / blockers, parsed from STATUS.md
    4. Current Edition Spotlight, Votes & Comments, Edition History,
       All-Time Stats, Heritage Auctions Ad, Comment Leaderboard — reused
       from build_stats_page.py

Output is meant to live on the `editors` branch only (editors/dashboard.html),
published by .github/workflows/refresh-stats.yml. Never commit the output to
dev2/dev/master.

Usage:
    source .venv/bin/activate
    GA4_PROPERTY_ID=523654462 GOOGLE_APPLICATION_CREDENTIALS=tools/credentials.json \
        python3 tools/build_editors_dashboard.py [--edition YYYY-MM-DD] [--output editors/dashboard.html]
"""

import os
import sys
import re
import argparse
from pathlib import Path
from datetime import datetime, date

sys.path.insert(0, os.path.dirname(__file__))

import build_stats_page as bsp
import verify_edition as ve

# ---------------------------------------------------------------------------
# Edition / STATUS.md discovery
# ---------------------------------------------------------------------------

NON_ARTICLE_SLUGS_PREFIXES = ("daily-star",)
NON_ARTICLE_SLUGS = {"datebook", "astrochart"}


def find_current_edition():
    """Most recent edition folder that has a STATUS.md (the active/upcoming one).
    Falls back to the most recent edition folder overall if none has one."""
    editions_dir = Path(__file__).parent.parent / "editions"
    dates = sorted(
        [d.name for d in editions_dir.iterdir() if d.is_dir() and re.match(r'\d{4}-\d{2}-\d{2}$', d.name)],
        reverse=True
    )
    for d in dates:
        if (editions_dir / d / "STATUS.md").exists():
            return d
    return dates[0] if dates else None


def parse_status_md(edition_date):
    """Extract Lineup table + Pending Deliveries + Blockers from STATUS.md, if present."""
    path = Path(__file__).parent.parent / "editions" / edition_date / "STATUS.md"
    if not path.exists():
        return None

    content = path.read_text(encoding="utf-8")

    lineup = []
    lineup_m = re.search(r'## Lineup.*?\n(?:(?!\|).*\n)*((?:\|.*\n?)+)', content)
    if lineup_m:
        rows = [l for l in lineup_m.group(1).split('\n') if l.strip().startswith('|')]
        for row in rows[2:]:  # skip header + separator
            cols = [c.strip() for c in row.strip().strip('|').split('|')]
            if len(cols) >= 5:
                slug = cols[1]
                if slug and slug not in ('—', '-') and slug not in NON_ARTICLE_SLUGS \
                        and not slug.startswith(NON_ARTICLE_SLUGS_PREFIXES):
                    lineup.append({
                        "order": cols[0], "slug": slug, "title": cols[2],
                        "author": cols[3], "coordinator": cols[4],
                    })

    def md_bold_to_html(text):
        return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)

    def extract_bullets(section_name):
        m = re.search(rf'## {re.escape(section_name)}\n\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
        if not m:
            return []
        return [md_bold_to_html(l.lstrip('-').strip()) for l in m.group(1).split('\n') if l.strip().startswith('-')]

    return {
        "lineup": lineup,
        "pending": extract_bullets("Pending Deliveries"),
        "blockers": extract_bullets("Blockers"),
    }


# ---------------------------------------------------------------------------
# Article Status section
# ---------------------------------------------------------------------------

STATUS_BADGE = {
    "READY":       ("#2a7a2a", "Ready"),
    "TEXT ONLY":   ("#b5860b", "Text Only"),
    "IN PROGRESS": ("#b5860b", "In Progress"),
    "PLACEHOLDER": ("#c41e3a", "Placeholder"),
    "MISSING":     ("#c41e3a", "Missing"),
}


def badge_html(status):
    color, label = STATUS_BADGE.get(status, ("#888", status))
    return f'<span style="color:{color}; font-weight:700;">{label}</span>'


def build_article_status_section(edition_date, status_data):
    edition_path = Path("editions") / edition_date

    if status_data and status_data["lineup"]:
        entries = status_data["lineup"]
    else:
        # Fall back to scanning the folder directly — no author/coordinator info available
        entries = []
        if edition_path.exists():
            for d in sorted(edition_path.iterdir()):
                if d.is_dir() and d.name not in NON_ARTICLE_SLUGS and not d.name.startswith(NON_ARTICLE_SLUGS_PREFIXES):
                    entries.append({"order": "", "slug": d.name, "title": d.name.replace('-', ' ').title(),
                                     "author": "—", "coordinator": "—"})

    if not entries:
        return '<p class="no-data">No articles found for this edition.</p>'

    rows = ""
    counts = {"READY": 0, "TEXT ONLY": 0, "IN PROGRESS": 0, "PLACEHOLDER": 0, "MISSING": 0}
    for e in entries:
        info = ve.check_article_status(edition_path, e["slug"])
        counts[info["status"]] = counts.get(info["status"], 0) + 1
        rows += f'''<tr>
  <td>{e["title"]}<div class="muted" style="font-size:0.75rem">{e["slug"]}</div></td>
  <td>{e["author"]}</td>
  <td>{e["coordinator"]}</td>
  <td>{badge_html(info["status"])}<div class="muted" style="font-size:0.75rem">{info["reason"]}</div></td>
</tr>'''

    summary = " &nbsp;·&nbsp; ".join(
        f'{badge_html(k)} {v}' for k, v in counts.items() if v
    )

    return f'''
    <div class="stat-sub" style="margin-bottom:14px">{summary}</div>
    <table>
      <thead><tr><th>Article</th><th>Author</th><th>Coordinator</th><th>Status</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
'''


def build_decisions_section(status_data):
    if not status_data or not (status_data["pending"] or status_data["blockers"]):
        return '<p class="no-data">Nothing tracked — no STATUS.md pending items for this edition.</p>'

    html = ""
    if status_data["pending"]:
        items = "".join(f'<li>{p}</li>' for p in status_data["pending"])
        html += f'<div style="margin-bottom:16px"><strong>Pending Deliveries</strong><ul style="padding-left:18px; margin-top:6px">{items}</ul></div>'
    if status_data["blockers"]:
        items = "".join(f'<li>{b}</li>' for b in status_data["blockers"])
        html += f'<div><strong class="red">Blockers</strong><ul style="padding-left:18px; margin-top:6px">{items}</ul></div>'
    return html


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--edition', default=None, help='Edition date YYYY-MM-DD (default: latest with a STATUS.md)')
    parser.add_argument('--output',  default='editors/dashboard.html', help='Output HTML file path')
    args = parser.parse_args()

    today_str = date.today().strftime("%Y-%m-%d")

    # The "prep" edition is whatever has an active STATUS.md — may be a future,
    # not-yet-published date (e.g. mid-week prep for next Sunday). Article Status
    # and Decisions Needed track that one.
    prep_edition = args.edition or find_current_edition()
    if not prep_edition:
        print("Error: no edition folders found")
        sys.exit(1)

    # GA4 can only report on published editions — never query a future date.
    editions = bsp.detect_editions(5)
    ga4_edition = editions[0] if editions else None

    print(f"→ Prep edition (Article Status / Decisions): {prep_edition}")
    print(f"→ GA4 edition (Reader Stats): {ga4_edition}")

    status_data = parse_status_md(prep_edition)

    print("  Building Article Status…")
    article_status_html = build_article_status_section(prep_edition, status_data)

    print("  Building Decisions Needed…")
    decisions_html = build_decisions_section(status_data)

    client = bsp.ga4_client()

    if ga4_edition:
        print("  Fetching Current Edition Spotlight…")
        s1 = bsp.build_section1(client, ga4_edition, today_str)
    else:
        s1 = '<p class="no-data">No published editions yet.</p>'

    print("  Fetching comment/vote data from Gmail…")
    records = bsp.fetch_gmail_votes_comments()
    print(f"  → {len(records)} vote/comment records found")

    print("  Building Votes & Comments…")
    s4 = bsp.build_section4(records, ga4_edition) if ga4_edition else '<p class="no-data">No published editions yet.</p>'

    print("  Fetching Edition History…")
    s2 = bsp.build_section2(client, editions, today_str) if editions else '<p class="no-data">No published editions yet.</p>'

    print("  Fetching All-Time Stats…")
    s3 = bsp.build_section3(client, today_str)

    print("  Fetching Heritage Auctions ad impressions…")
    s6 = bsp.build_section6(client, ga4_edition, today_str)

    print("  Building Comment Leaderboard…")
    s5 = bsp.build_section5(records)

    generated_at = datetime.now().strftime("%-m/%-d/%Y at %-I:%M %p")
    ed_label = datetime.strptime(prep_edition, "%Y-%m-%d").strftime("%B %-d, %Y")
    ga4_ed_label = datetime.strptime(ga4_edition, "%Y-%m-%d").strftime("%B %-d, %Y") if ga4_edition else "—"
    preview_url = f"https://article-dev2.vercel.app/editions/{prep_edition}/"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Editors Dashboard — {ed_label} | Classic Chicago Magazine</title>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lato:wght@300;400;700&display=swap" rel="stylesheet">
  <style>
{bsp.CSS}
    .jump-links {{ display:flex; gap:16px; flex-wrap:wrap; margin: 16px 0 28px; font-size:0.8rem; }}
    .jump-links a {{ color:#888; text-transform:uppercase; letter-spacing:0.5px; }}
    section {{ margin-bottom: 40px; }}
    section h2 {{ font-family:'Playfair Display',serif; font-size:1.3rem; border-bottom:2px solid #1a1a1a; padding-bottom:8px; margin-bottom:14px; }}
  </style>
</head>
<body>
<div class="container">
  <div class="masthead">
    <h1>Classic Chicago Magazine</h1>
    <div style="font-family:'Playfair Display',serif; font-size:1.1rem; color:#888; margin-top:4px">Editors Dashboard</div>
    <div class="meta">Current edition: <strong>{ed_label}</strong>
      &nbsp;·&nbsp; <a href="{preview_url}" target="_blank">Preview →</a>
      &nbsp;·&nbsp; Generated {generated_at}</div>
  </div>

  <nav class="jump-links">
    <a href="#status">Article Status</a>
    <a href="#decisions">Decisions Needed</a>
    <a href="#spotlight">Current Edition</a>
    <a href="#votes">Votes &amp; Comments</a>
    <a href="#history">Edition History</a>
    <a href="#alltime">All-Time Stats</a>
    <a href="#ha-ad">Heritage Auctions Ad</a>
    <a href="#leaderboard">Comment Leaderboard</a>
  </nav>

  <section id="status">
    <h2>Article Status</h2>
    {article_status_html}
  </section>

  <section id="decisions">
    <h2>Decisions Needed</h2>
    {decisions_html}
  </section>

  <section id="spotlight">
    <h2>Latest Published Edition Spotlight — {ga4_ed_label}</h2>
    {s1}
  </section>

  <section id="votes">
    <h2>Votes &amp; Comments — {ga4_ed_label}</h2>
    {s4}
  </section>

  <section id="history">
    <h2>Edition History</h2>
    {s2}
  </section>

  <section id="alltime">
    <h2>All-Time Site Stats</h2>
    {s3}
  </section>

  <section id="ha-ad">
    <h2>Heritage Auctions Ad — Impressions</h2>
    {s6}
  </section>

  <section id="leaderboard">
    <h2>All-Time Comment Leaderboard</h2>
    {s5}
  </section>

  <div class="generated">Data from GA4 Property {bsp.PROPERTY_ID} · editors branch only, never merged into dev2/dev/master</div>
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
