const { BetaAnalyticsDataClient } = require('@google-analytics/data');

async function getEngagement(propertyId, credentialsPath) {
  const client = new BetaAnalyticsDataClient({ keyFilename: credentialsPath });

  const [response] = await client.runReport({
    property: `properties/${propertyId}`,
    dateRanges: [{ startDate: '30daysAgo', endDate: 'today' }],
    metrics: [
      { name: 'bounceRate' },
      { name: 'engagementRate' },
      { name: 'averageSessionDuration' }
    ],
  });

  const row = response.rows[0];
  console.log('\n📈  ENGAGEMENT STATS (Last 30 Days)');
  console.log('-----------------------------------');
  console.log(`Bounce Rate:      ${(parseFloat(row.metricValues[0].value) * 100).toFixed(2)}%`);
  console.log(`Engagement Rate:  ${(parseFloat(row.metricValues[1].value) * 100).toFixed(2)}%`);
  console.log(`Avg. Session:     ${parseFloat(row.metricValues[2].value).toFixed(0)} seconds`);
  console.log('-----------------------------------\n');
}

getEngagement(process.env.GA4_PROPERTY_ID, 'tools/credentials.json');
