const { BetaAnalyticsDataClient } = require('@google-analytics/data');

module.exports = async (req, res) => {
  // 1. Setup credentials
  // Vercel Environment variables are preferred
  const propertyId = process.env.GA4_PROPERTY_ID;
  const keyContent = process.env.GA4_SERVICE_ACCOUNT_KEY;

  if (!propertyId || !keyContent) {
    return res.status(500).json({ 
      error: 'Environment variables GA4_PROPERTY_ID or GA4_SERVICE_ACCOUNT_KEY are missing.' 
    });
  }

  try {
    const credentials = JSON.parse(keyContent);
    const client = new BetaAnalyticsDataClient({
      credentials,
    });

    // 2. Fetch Totals (Last 30 days)
    const [totalsResponse] = await client.runReport({
      property: `properties/${propertyId}`,
      dateRanges: [{ startDate: '30daysAgo', endDate: 'today' }],
      metrics: [
        { name: 'activeUsers' },
        { name: 'sessions' },
        { name: 'screenPageViews' }
      ],
    });

    // 3. Fetch Edition Stats (Current Sunday Edition)
    // Find the most recent Sunday (publish date)
    const today = new Date();
    const dayOfWeek = today.getDay(); // 0 (Sun) to 6 (Sat)
    const diffToSunday = dayOfWeek === 0 ? 0 : dayOfWeek;
    const lastSunday = new Date(today);
    lastSunday.setDate(today.getDate() - diffToSunday);
    
    const editionDate = lastSunday.toISOString().split('T')[0];
    const editionPath = `/editions/${editionDate}/`;

    const [editionResponse] = await client.runReport({
      property: `properties/${propertyId}`,
      dateRanges: [{ startDate: 'yesterday', endDate: 'today' }], // Captures Sat 6pm to now roughly
      dimensions: [{ name: 'pagePath' }],
      metrics: [
        { name: 'activeUsers' },
        { name: 'screenPageViews' }
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

    // 4. Format Data
    const overall = {
      users: totalsResponse.rows[0]?.metricValues[0]?.value || 0,
      sessions: totalsResponse.rows[0]?.metricValues[1]?.value || 0,
      views: totalsResponse.rows[0]?.metricValues[2]?.value || 0,
    };

    let editionTotalViews = 0;
    let editionTotalUsers = 0;
    const topArticles = editionResponse.rows.map(row => {
      const views = parseInt(row.metricValues[1].value);
      const users = parseInt(row.metricValues[0].value);
      editionTotalViews += views;
      editionTotalUsers += users;

      return {
        path: row.dimensionValues[0].value,
        views,
        users
      };
    }).sort((a, b) => b.views - a.views).slice(0, 10);

    // 5. Return Response
    res.status(200).json({
      fetched_at: new Date().toISOString(),
      edition: editionDate,
      overall,
      editionStats: {
        totalViews: editionTotalViews,
        totalUsers: editionTotalUsers,
        topArticles
      }
    });

  } catch (error) {
    console.error('GA4 API Error:', error);
    res.status(500).json({ error: error.message });
  }
};
