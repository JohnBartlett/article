#!/usr/bin/env python3
"""
tools/ga4_edition_stats.py — Per-edition page view breakdown with article titles

Usage:
    export GOOGLE_APPLICATION_CREDENTIALS="tools/credentials.json"
    python3 tools/ga4_edition_stats.py

Writes tools/editions_stats.json (read by editors/stats.html).
"""

import os, re, json
from datetime import datetime
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest, OrderBy

PROPERTY_ID = '523654462'
EDITIONS_ROOT = os.path.join(os.path.dirname(__file__), '..', 'editions')

EDITIONS = [
    ('2026-02-08', 'February 8, 2026'),
    ('2026-02-15', 'February 15, 2026'),
    ('2026-02-22', 'February 22, 2026'),
    ('2026-03-01', 'March 1, 2026'),
    ('2026-03-08', 'March 8, 2026'),
    ('2026-03-15', 'March 15, 2026'),
    ('2026-03-22', 'March 22, 2026'),
    ('2026-03-29', 'March 29, 2026'),
    ('2026-04-05', 'April 5, 2026'),
]

def get_title(date, slug):
    path = os.path.join(EDITIONS_ROOT, date, slug, 'index.html')
    if not os.path.exists(path):
        return slug
    content = open(path).read()
    m = re.search(r'<h1[^>]*class="article-title"[^>]*>(.*?)</h1>', content, re.DOTALL)
    if m:
        return re.sub(r'<[^>]+>', '', m.group(1)).strip()
    return slug

def main():
    client = BetaAnalyticsDataClient()
    today = datetime.now().strftime('%Y-%m-%d')

    resp = client.run_report(RunReportRequest(
        property=f'properties/{PROPERTY_ID}',
        dimensions=[Dimension(name='pagePath')],
        metrics=[Metric(name='screenPageViews')],
        date_ranges=[DateRange(start_date='2026-01-01', end_date=today)],
        limit=500,
        order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name='screenPageViews'), desc=True)]
    ))
    pages = {r.dimension_values[0].value: int(r.metric_values[0].value) for r in resp.rows}

    result = []
    for date, label in EDITIONS:
        prefix = f'/editions/{date}/'
        # Collect and normalize slugs (merge trailing-slash variants, skip .html files and root)
        slug_views = {}
        for path, views in pages.items():
            if not path.startswith(prefix):
                continue
            remainder = path[len(prefix):].strip('/')
            if not remainder or '.' in remainder or remainder == 'index.html':
                continue
            # Take only the first path segment (the article slug)
            slug = remainder.split('/')[0]
            slug_views[slug] = slug_views.get(slug, 0) + views

        articles = []
        for slug, views in sorted(slug_views.items(), key=lambda x: -x[1]):
            articles.append({
                'slug': slug,
                'title': get_title(date, slug),
                'views': views
            })

        total = sum(a['views'] for a in articles)
        result.append({'date': date, 'label': label, 'total': total, 'articles': articles})
        print(f"{label}: {total:,} views ({len(articles)} articles)")

    data = {'updated': datetime.now().strftime('%Y-%m-%d %H:%M'), 'editions': result}
    out = os.path.join(os.path.dirname(__file__), 'editions_stats.json')
    with open(out, 'w') as f:
        json.dump(data, f, indent=2)
    print(f'\n✓ Saved {out}')

if __name__ == '__main__':
    main()
