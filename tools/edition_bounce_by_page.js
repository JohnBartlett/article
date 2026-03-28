const { BetaAnalyticsDataClient } = require('@google-analytics/data');

async function getBounceByPage(propertyId, credentialsPath) {
  const client = new BetaAnalyticsDataClient({ keyFilename: credentialsPath });
  const editionPath = '/editions/2026-03-15/';

  const [response] = await client.runReport({
    property: `properties/${propertyId}`,
    dateRanges: [{ startDate: 'yesterday', endDate: 'today' }],
    dimensions: [{ name: 'pagePath' }],
    metrics: [
      { name: 'bounceRate' },
      { name: 'screenPageViews' },
      { name: 'averageSessionDuration' }
    ],
    dimensionFilter: {
      filter: {
        fieldName: 'pagePath',
        stringFilter: {
          matchType: 'BEGINS_WITH',
          value: editionPath,
        },
      },
    },
  });

  console.log('\n📄  BOUNCE RATE BY ARTICLE (Today\'s Edition)');
  console.log('---------------------------------------------');
  console.log(`${'Article'.padEnd(25)} | Views | Bounce | Avg. Session`);
  console.log('---------------------------------------------');

  const rows = response.rows.map(row => ({
    path: row.dimensionValues[0].value,
    bounce: (parseFloat(row.metricValues[0].value) * 100).toFixed(1),
    views: parseInt(row.metricValues[1].value),
    duration: parseFloat(row.metricValues[2].value).toFixed(0)
  })).sort((a, b) => b.views - a.views);

  rows.forEach(r => {
    const cleanName = r.path.replace(editionPath, '').replace(/\/$/, '') || 'Landing Page';
    console.log(`${cleanName.padEnd(25)} | ${r.views.toString().padStart(5)} | ${r.bounce.padStart(5)}% | ${r.duration.padStart(5)}s`);
  });
  console.log('---------------------------------------------\n');
}

getBounceByPage(process.env.GA4_PROPERTY_ID, 'tools/credentials.json');
