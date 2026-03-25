const { BetaAnalyticsDataClient } = require('@google-analytics/data');

async function getEditionEngagement(propertyId, credentialsPath) {
  const client = new BetaAnalyticsDataClient({ keyFilename: credentialsPath });
  const editionPath = '/editions/2026-03-15/';

  const [response] = await client.runReport({
    property: `properties/${propertyId}`,
    dateRanges: [{ startDate: 'yesterday', endDate: 'today' }],
    dimensions: [{ name: 'pagePath' }],
    metrics: [
      { name: 'bounceRate' },
      { name: 'engagementRate' },
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

  // Calculate weighted averages across all edition pages
  let totalViews = 0;
  let weightedBounce = 0;
  let weightedEngagement = 0;
  let weightedDuration = 0;

  // We need page views to weight the averages correctly
  const [viewsResponse] = await client.runReport({
    property: `properties/${propertyId}`,
    dateRanges: [{ startDate: 'yesterday', endDate: 'today' }],
    dimensions: [{ name: 'pagePath' }],
    metrics: [{ name: 'screenPageViews' }],
    dimensionFilter: {
      filter: { fieldName: 'pagePath', stringFilter: { matchType: 'BEGINS_WITH', value: editionPath } },
    },
  });

  const viewMap = {};
  viewsResponse.rows.forEach(r => viewMap[r.dimensionValues[0].value] = parseInt(r.metricValues[0].value));

  response.rows.forEach(row => {
    const path = row.dimensionValues[0].value;
    const views = viewMap[path] || 0;
    totalViews += views;
    weightedBounce += parseFloat(row.metricValues[0].value) * views;
    weightedEngagement += parseFloat(row.metricValues[1].value) * views;
    weightedDuration += parseFloat(row.metricValues[2].value) * views;
  });

  console.log('\n📈  TODAY\'S EDITION ENGAGEMENT (2026-03-15)');
  console.log('-------------------------------------------');
  console.log(`Bounce Rate:      ${((weightedBounce / totalViews) * 100).toFixed(2)}%`);
  console.log(`Engagement Rate:  ${((weightedEngagement / totalViews) * 100).toFixed(2)}%`);
  console.log(`Avg. Session:     ${(weightedDuration / totalViews).toFixed(0)} seconds`);
  console.log('-------------------------------------------\n');
}

getEditionEngagement(process.env.GA4_PROPERTY_ID, 'tools/credentials.json');
