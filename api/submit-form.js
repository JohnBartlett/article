module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const body = req.body || {};
  const subject = body._subject || 'Classic Chicago Form Submission';
  const next = body._next || null;

  const fields = Object.entries(body)
    .filter(([k]) => !k.startsWith('_'))
    .map(([k, v]) => `${k}: ${v}`)
    .join('\n');

  try {
    const response = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${process.env.RESEND_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: 'Classic Chicago <forms@2ccmag.com>',
        to: ['john.bartlett@gmail.com'],
        subject,
        text: fields,
      }),
    });

    if (!response.ok) {
      const err = await response.text();
      console.error('Resend error:', err);
      throw new Error(err);
    }

    const wantsJson = (req.headers['accept'] || '').includes('application/json');
    if (wantsJson) {
      return res.status(200).json({ success: true });
    }
    if (next) {
      return res.redirect(302, next);
    }
    return res.status(200).send('Message sent.');
  } catch (err) {
    console.error('Submit form error:', err);
    const wantsJson = (req.headers['accept'] || '').includes('application/json');
    if (wantsJson) {
      return res.status(500).json({ error: 'Failed to send' });
    }
    return res.status(500).send('Failed to send message.');
  }
};
