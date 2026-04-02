#!/usr/bin/env python3
"""
tools/ga4_edition_stats.py — Per-edition page view breakdown

Usage:
    export GOOGLE_APPLICATION_CREDENTIALS="tools/credentials.json"
    python3 tools/ga4_edition_stats.py

Writes tools/editions_stats.json (read by editors/stats.html).
"""

import os, json
from datetime import datetime
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest, OrderBy

PROPERTY_ID = '523654462'

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
        articles = [(k, v) for k, v in pages.items() if k.startswith(prefix) and k.count('/') >= 3]
        articles.sort(key=lambda x: -x[1])
        total = sum(v for _, v in articles)
        result.append({
            'date': date,
            'label': label,
            'total': total,
            'articles': [{'slug': k.replace(prefix, '').strip('/'), 'views': v} for k, v in articles]
        })
        print(f"{label}: {total:,} views ({len(articles)} articles)")

    data = {'updated': datetime.now().strftime('%Y-%m-%d %H:%M'), 'editions': result}
    out = os.path.join(os.path.dirname(__file__), 'editions_stats.json')
    with open(out, 'w') as f:
        json.dump(data, f, indent=2)
    print(f'\n✓ Saved {out}')

if __name__ == '__main__':
    main()
