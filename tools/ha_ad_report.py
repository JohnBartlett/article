#!/usr/bin/env python3
"""
tools/ha_ad_report.py — Heritage Auctions ad impression report

Queries GA4 for ha_ad_impression events, broken down by article page.
Impressions fire on production (master) each time a reader loads an article
containing the HA ad.

Usage:
    export GA4_PROPERTY_ID="123456789"
    export GOOGLE_APPLICATION_CREDENTIALS="tools/credentials.json"
    python3 tools/ha_ad_report.py [--days 30]

Requirements:
    pip install google-analytics-data
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
    OrderBy,
    FilterExpression,
    Filter,
)


def get_ad_impressions(property_id, days_ago=30):
    client = BetaAnalyticsDataClient()

    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="pagePath")],
        metrics=[Metric(name="eventCount")],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        dimension_filter=FilterExpression(
            filter=Filter(
                field_name="eventName",
                string_filter=Filter.StringFilter(value="ha_ad_impression"),
            )
        ),
        order_bys=[OrderBy(
            metric=OrderBy.MetricOrderBy(metric_name="eventCount"),
            desc=True
        )],
    )

    response = client.run_report(request)

    rows = []
    total = 0
    for row in response.rows:
        count = int(row.metric_values[0].value)
        rows.append({
            "pagePath": row.dimension_values[0].value,
            "impressions": count,
        })
        total += count

    return {
        "date_range": f"{start_date} to {end_date}",
        "fetched_at": datetime.now().isoformat(),
        "total_impressions": total,
        "by_article": rows,
    }


def main():
    parser = argparse.ArgumentParser(description="Heritage Auctions ad impression report")
    parser.add_argument("--days", type=int, default=30,
                        help="Number of days to look back (default: 30)")
    args = parser.parse_args()

    property_id = os.environ.get("GA4_PROPERTY_ID")
    if not property_id:
        print("Error: GA4_PROPERTY_ID environment variable not set.")
        print("Note: Use the numeric Property ID from GA4 Admin, not the G-XXXX Measurement ID.")
        sys.exit(1)

    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        print("Error: GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
        print("Provide the path to your Service Account JSON key (e.g. tools/credentials.json).")
        sys.exit(1)

    try:
        print(f"→ Fetching HA ad impressions for last {args.days} days...")
        report = get_ad_impressions(property_id, args.days)

        print(f"\n  Heritage Auctions Ad Impressions")
        print(f"  Period : {report['date_range']}")
        print(f"  Total  : {report['total_impressions']:,}")
        if report["by_article"]:
            print()
            for row in report["by_article"]:
                print(f"  {row['impressions']:>5}  {row['pagePath']}")
        else:
            print("\n  No impressions recorded yet (only fires on production).")

        filename = f"ha_ad_report_{datetime.now().strftime('%Y-%m-%d')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        print(f"\n✓ Saved to {filename}")

    except Exception as e:
        print(f"Error fetching report: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
