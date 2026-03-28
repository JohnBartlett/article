const { BetaAnalyticsDataClient } = require('@google-analytics/data');

async function getDeepDive(propertyId, credentialsPath) {
  const client = new BetaAnalyticsDataClient({ keyFilename: credentialsPath });
  const articlePath = '/editions/2026-03-15/little-village/';

  // 1. Performance & Engagement
  const [perfResponse] = await client.runReport({
    property: `properties/${propertyId}`,
    dateRanges: [{ startDate: '2026-03-14', endDate: 'today' }],
    dimensions: [{ name: 'pagePath' }],
    metrics: [
      { name: 'screenPageViews' },
      { name: 'activeUsers' },
      { name: 'averageSessionDuration' },
      { name: 'bounceRate' },
      { name: 'engagedSessions' }
    ],
    dimensionFilter: {
      filter: { fieldName: 'pagePath', stringFilter: { matchType: 'EXACT', value: articlePath } },
    },
  });

  // 2. Traffic Sources
  const [sourceResponse] = await client.runReport({
    property: `properties/${propertyId}`,
    dateRanges: [{ startDate: '2026-03-14', endDate: 'today' }],
    dimensions: [{ name: 'sessionSourceMedium' }],
    metrics: [{ name: 'activeUsers' }],
    dimensionFilter: {
      filter: { fieldName: 'pagePath', stringFilter: { matchType: 'EXACT', value: articlePath } },
    },
  });

  // 3. Device breakdown
  const [deviceResponse] = await client.runReport({
    property: `properties/${propertyId}`,
    dateRanges: [{ startDate: '2026-03-14', endDate: 'today' }],
    dimensions: [{ name: 'deviceCategory' }],
    metrics: [{ name: 'activeUsers' }],
    dimensionFilter: {
      filter: { fieldName: 'pagePath', stringFilter: { matchType: 'EXACT', value: articlePath } },
    },
  });

  console.log('\n🏙️  DEEP DIVE: "Visiting Little Village"');
  console.log('--------------------------------------------------');
  
  if (perfResponse.rows.length > 0) {
    const p = perfResponse.rows[0];
    console.log(`Total Views:      ${p.metricValues[0].value}`);
    console.log(`Unique Readers:   ${p.metricValues[1].value}`);
    console.log(`Avg. Read Time:   ${parseFloat(p.metricValues[2].value).toFixed(0)} seconds`);
    console.log(`Bounce Rate:      ${(parseFloat(p.metricValues[3].value) * 100).toFixed(1)}%`);
    console.log(`Engaged Sessions: ${p.metricValues[4].value}`);
  }

  console.log('\n📍 WHERE READERS CAME FROM:');
  sourceResponse.rows.forEach(r => {
    console.log(`- ${r.dimensionValues[0].value.padEnd(30)}: ${r.metricValues[0].value} users`);
  });

  console.log('\n📱 DEVICE BREAKDOWN:');
  deviceResponse.rows.forEach(r => {
    console.log(`- ${r.dimensionValues[0].value.padEnd(30)}: ${r.metricValues[0].value} users`);
  });
  console.log('--------------------------------------------------\n');
}

getDeepDive("523654462", 'tools/credentials.json');
