const { BetaAnalyticsDataClient } = require('@google-analytics/data');

async function getAllArticlesEngagement(propertyId, credentialsPath) {
  const client = new BetaAnalyticsDataClient({ keyFilename: credentialsPath });

  const [response] = await client.runReport({
    property: `properties/${propertyId}`,
    dateRanges: [{ startDate: '30daysAgo', endDate: 'today' }],
    dimensions: [{ name: 'pagePath' }],
    metrics: [
      { name: 'screenPageViews' },
      { name: 'activeUsers' },
      { name: 'averageSessionDuration' },
      { name: 'bounceRate' }
    ],
    dimensionFilter: {
      filter: {
        fieldName: 'pagePath',
        stringFilter: {
          matchType: 'BEGINS_WITH',
          value: '/editions/',
        },
      },
    },
  });

  console.log('\n📚  ALL ARTICLES ENGAGEMENT (Last 30 Days)');
  console.log('---------------------------------------------------------------------------');
  console.log(`${'Article Path'.padEnd(45)} | Views | Users | Avg. Time | Bounce`);
  console.log('---------------------------------------------------------------------------');

  const rows = response.rows.map(row => ({
    path: row.dimensionValues[0].value,
    views: parseInt(row.metricValues[0].value),
    users: parseInt(row.metricValues[1].value),
    duration: parseFloat(row.metricValues[2].value).toFixed(0),
    bounce: (parseFloat(row.metricValues[3].value) * 100).toFixed(1)
  })).sort((a, b) => b.views - a.views);

  rows.forEach(r => {
    // Shorten path for display
    let displayPath = r.path.replace('/editions/', '');
    if (displayPath.length > 45) displayPath = '...' + displayPath.slice(-42);
    
    console.log(`${displayPath.padEnd(45)} | ${r.views.toString().padStart(5)} | ${r.users.toString().padStart(5)} | ${r.duration.padStart(8)}s | ${r.bounce.padStart(5)}%`);
  });
  console.log('---------------------------------------------------------------------------\n');
}

getAllArticlesEngagement(process.env.GA4_PROPERTY_ID, 'tools/credentials.json');
