#!/usr/bin/env python3
"""
tools/ga4_report.py — Collect stats from Google Analytics 4 (GA4)

Usage:
    export GA4_PROPERTY_ID="123456789"
    export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"
    python3 tools/ga4_report.py

Requirements:
    pip install google-analytics-data
"""

import os
import sys
import json
from datetime import datetime, timedelta
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
    OrderBy
)

def get_report(property_id, days_ago=30):
    """Fetches GA4 report for the last X days."""
    client = BetaAnalyticsDataClient()

    # Define date range
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")

    # 1. Fetch Totals (Users, Sessions, Page Views)
    totals_request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[],
        metrics=[
            Metric(name="activeUsers"),
            Metric(name="sessions"),
            Metric(name="screenPageViews"),
        ],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
    )

    totals_response = client.run_report(totals_request)
    
    totals = {}
    if totals_response.rows:
        row = totals_response.rows[0]
        totals = {
            "activeUsers": int(row.metric_values[0].value),
            "sessions": int(row.metric_values[1].value),
            "screenPageViews": int(row.metric_values[2].value),
        }

    # 2. Fetch Top 10 Pages by Views
    pages_request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="pagePath")],
        metrics=[Metric(name="screenPageViews")],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        limit=10,
        order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="screenPageViews"), desc=True)]
    )

    pages_response = client.run_report(pages_request)
    
    top_pages = []
    for row in pages_response.rows:
        top_pages.append({
            "pagePath": row.dimension_values[0].value,
            "screenPageViews": int(row.metric_values[0].value)
        })

    return {
        "property_id": property_id,
        "date_range": f"{start_date} to {end_date}",
        "fetched_at": datetime.now().isoformat(),
        "totals": totals,
        "top_pages": top_pages
    }

def main():
    property_id = os.environ.get("GA4_PROPERTY_ID")
    if not property_id:
        print("Error: GA4_PROPERTY_ID environment variable not set.")
        print("Note: This must be the NUMERIC Property ID, not the G-XXXX Measurement ID.")
        sys.exit(1)

    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        print("Error: GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
        print("Provide the path to your Service Account JSON key.")
        sys.exit(1)

    try:
        print(f"→ Fetching stats for Property {property_id}...")
        report = get_report(property_id)
        
        filename = f"ga4_report_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
            
        print(f"✓ Success! Report saved to {filename}")
        
    except Exception as e:
        print(f"Error fetching GA4 report: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
