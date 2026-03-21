const { BetaAnalyticsDataClient } = require('@google-analytics/data');
const fs = require('fs');
const path = require('path');

async function runReport(propertyId, credentialsPath) {
  const analyticsDataClient = new BetaAnalyticsDataClient({
    keyFilename: credentialsPath,
  });

  const [response] = await analyticsDataClient.runReport({
    property: `properties/${propertyId}`,
    dateRanges: [
      {
        startDate: '30daysAgo',
        endDate: 'today',
      },
    ],
    dimensions: [
      {
        name: 'pagePath',
      },
    ],
    metrics: [
      {
        name: 'activeUsers',
      },
      {
        name: 'sessions',
      },
      {
        name: 'screenPageViews',
      },
    ],
  });

  const totals = {
    activeUsers: 0,
    sessions: 0,
    screenPageViews: 0,
  };

  const topPages = response.rows.map(row => {
    const views = parseInt(row.metricValues[2].value);
    totals.activeUsers += parseInt(row.metricValues[0].value);
    totals.sessions += parseInt(row.metricValues[1].value);
    totals.screenPageViews += views;

    return {
      pagePath: row.dimensionValues[0].value,
      screenPageViews: views,
    };
  });

  // Sort by views and take top 10
  const sortedTopPages = topPages
    .sort((a, b) => b.screenPageViews - a.screenPageViews)
    .slice(0, 10);

  const report = {
    property_id: propertyId,
    date_range: 'Last 30 days',
    fetched_at: new Date().toISOString(),
    totals: {
        activeUsers: totals.activeUsers, // Note: This is a sum of daily unique users, not true unique users for the period.
        sessions: totals.sessions,
        screenPageViews: totals.screenPageViews
    },
    top_pages: sortedTopPages,
  };

  const filename = `ga4_report_${new Date().toISOString().split('T')[0]}.json`;
  fs.writeFileSync(filename, JSON.stringify(report, null, 2));
  console.log(`✓ Success! Report saved to ${filename}`);
  console.log(JSON.stringify(report, null, 2));
}

const propertyId = process.env.GA4_PROPERTY_ID;
const credentialsPath = path.join(__dirname, 'credentials.json');

runReport(propertyId, credentialsPath).catch(err => {
  console.error('Error fetching GA4 report:', err);
  process.exit(1);
});
