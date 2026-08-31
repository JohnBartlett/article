#!/usr/bin/env python3
"""
tools/ga4_astrochart_query.py — One-off GA4 query for Astrochart (daily-star) page views.

Usage:
    export GA4_PROPERTY_ID="123456789"
    export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"
    python3 tools/ga4_astrochart_query.py [days_ago]
"""

import os
import sys
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

def main():
    days_ago = int(sys.argv[1]) if len(sys.argv) > 1 else 90
    property_id = os.environ["GA4_PROPERTY_ID"]
    client = BetaAnalyticsDataClient()

    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")

    # Per-page breakdown
    page_request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="pagePath")],
        metrics=[Metric(name="screenPageViews"), Metric(name="activeUsers")],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        dimension_filter=FilterExpression(
            filter=Filter(
                field_name="pagePath",
                string_filter=Filter.StringFilter(value="daily-star", match_type=Filter.StringFilter.MatchType.CONTAINS),
            )
        ),
        order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="screenPageViews"), desc=True)],
    )
    page_response = client.run_report(page_request)

    # Per-month breakdown
    month_request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="yearMonth")],
        metrics=[Metric(name="screenPageViews"), Metric(name="activeUsers")],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        dimension_filter=FilterExpression(
            filter=Filter(
                field_name="pagePath",
                string_filter=Filter.StringFilter(value="daily-star", match_type=Filter.StringFilter.MatchType.CONTAINS),
            )
        ),
        order_bys=[OrderBy(dimension=OrderBy.DimensionOrderBy(dimension_name="yearMonth"))],
    )
    month_response = client.run_report(month_request)

    print(f"=== Astrochart (daily-star) page views, last {days_ago} days ({start_date} to {end_date}) ===\n")

    print("--- By page ---")
    if not page_response.rows:
        print("(no data)")
    for row in page_response.rows:
        path = row.dimension_values[0].value
        views = row.metric_values[0].value
        users = row.metric_values[1].value
        print(f"{views:>6} views | {users:>6} users | {path}")

    print("\n--- By month ---")
    if not month_response.rows:
        print("(no data)")
    for row in month_response.rows:
        ym = row.dimension_values[0].value
        views = row.metric_values[0].value
        users = row.metric_values[1].value
        print(f"{ym}: {views:>6} views | {users:>6} users")

    total_views = sum(int(r.metric_values[0].value) for r in page_response.rows)
    total_users = sum(int(r.metric_values[1].value) for r in page_response.rows)
    print(f"\n--- Total ---\n{total_views} views, {total_users} users across all daily-star pages")

    # Session-level engagement for sessions that included an astrochart page
    engagement_request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[],
        metrics=[
            Metric(name="sessions"),
            Metric(name="engagedSessions"),
            Metric(name="engagementRate"),
            Metric(name="averageSessionDuration"),
            Metric(name="screenPageViewsPerSession"),
            Metric(name="userEngagementDuration"),
        ],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        dimension_filter=FilterExpression(
            filter=Filter(
                field_name="pagePath",
                string_filter=Filter.StringFilter(value="daily-star", match_type=Filter.StringFilter.MatchType.CONTAINS),
            )
        ),
    )
    engagement_response = client.run_report(engagement_request)

    print("\n--- Session engagement (sessions that included an astrochart page) ---")
    if not engagement_response.rows:
        print("(no data)")
    else:
        row = engagement_response.rows[0]
        sessions = int(row.metric_values[0].value)
        engaged = int(row.metric_values[1].value)
        rate = float(row.metric_values[2].value)
        avg_duration = float(row.metric_values[3].value)
        views_per_session = float(row.metric_values[4].value)
        total_engagement_secs = float(row.metric_values[5].value)
        print(f"Sessions: {sessions}")
        print(f"Engaged sessions: {engaged} ({rate*100:.1f}% engagement rate)")
        print(f"Average session duration: {avg_duration:.1f}s")
        print(f"Screen page views per session: {views_per_session:.2f}")
        print(f"Total user engagement time: {total_engagement_secs:.0f}s ({total_engagement_secs/60:.1f} min)")

if __name__ == "__main__":
    main()
