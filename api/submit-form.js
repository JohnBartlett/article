const { Resend } = require('resend');

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const resend = new Resend(process.env.RESEND_API_KEY);

  const body = req.body || {};
  const subject = body._subject || 'Classic Chicago Form Submission';
  const next = body._next || null;

  // Build email body from all non-underscore fields
  const fields = Object.entries(body)
    .filter(([k]) => !k.startsWith('_'))
    .map(([k, v]) => `${k}: ${v}`)
    .join('\n');

  try {
    await resend.emails.send({
      from: 'Classic Chicago <forms@classicchicagomagazine.com>',
      to: 'editor@2ccmag.com',
      subject,
      text: fields,
    });

    // AJAX requests (Accept: application/json) get JSON back
    const wantsJson = (req.headers['accept'] || '').includes('application/json');
    if (wantsJson) {
      return res.status(200).json({ success: true });
    }

    // Regular form POST — redirect back
    if (next) {
      return res.redirect(302, next);
    }
    return res.status(200).send('Message sent.');
  } catch (err) {
    console.error('Resend error:', err);
    const wantsJson = (req.headers['accept'] || '').includes('application/json');
    if (wantsJson) {
      return res.status(500).json({ error: 'Failed to send' });
    }
    return res.status(500).send('Failed to send message.');
  }
};
