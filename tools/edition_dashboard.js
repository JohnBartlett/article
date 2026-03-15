const { BetaAnalyticsDataClient } = require('@google-analytics/data');
const path = require('path');

async function getEditionDashboard(propertyId, credentialsPath) {
  const analyticsDataClient = new BetaAnalyticsDataClient({
    keyFilename: credentialsPath,
  });

  const currentEdition = '2026-03-15';
  const editionPath = `/editions/${currentEdition}/`;

  console.log(`\n📊  DASHBOARD: Edition ${currentEdition}`);
  console.log(`📅  Reporting since Saturday 6pm (est. March 14) until now\n`);

  const [response] = await analyticsDataClient.runReport({
    property: `properties/${propertyId}`,
    dateRanges: [
      {
        startDate: 'yesterday',
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
        name: 'screenPageViews',
      },
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

  let totalViews = 0;
  let totalUsers = 0;
  const articles = [];

  response.rows.forEach(row => {
    const views = parseInt(row.metricValues[1].value);
    const users = parseInt(row.metricValues[0].value);
    totalViews += views;
    totalUsers += users;

    // Clean up the article name from the path
    const articleName = row.dimensionValues[0].value
      .replace(editionPath, '')
      .replace('/', '') || 'Landing Page';

    articles.push({
      name: articleName,
      views,
      users
    });
  });

  // Sort by views
  articles.sort((a, b) => b.views - a.views);

  // Print Summary Table
  console.log('--- EDITION SUMMARY ---');
  console.log(`Total Edition Views: ${totalViews}`);
  console.log(`Total Edition Users: ${totalUsers}`);
  console.log('------------------------\n');

  console.log('--- BY ARTICLE ---');
  if (articles.length === 0) {
    console.log('No data yet for this edition (or check tracking setup).');
  } else {
    articles.forEach(a => {
      const bar = '█'.repeat(Math.ceil((a.views / (totalViews || 1)) * 20));
      console.log(`${a.name.padEnd(25)} | ${a.views.toString().padStart(5)} views | ${bar}`);
    });
  }
  console.log('\n');
}

const propertyId = process.env.GA4_PROPERTY_ID;
const credentialsPath = path.join(__dirname, 'credentials.json');

getEditionDashboard(propertyId, credentialsPath).catch(err => {
  console.error('Error fetching dashboard:', err);
  process.exit(1);
});
