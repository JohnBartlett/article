const nodemailer = require('nodemailer');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Accept');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

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

  const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
      user: 'john.bartlett@gmail.com',
      pass: process.env.GMAIL_APP_PASSWORD,
    },
  });

  try {
    await transporter.sendMail({
      from: 'Classic Chicago Forms <john.bartlett@gmail.com>',
      to: 'john.bartlett@gmail.com',
      subject,
      text: fields,
    });

    const wantsJson = (req.headers['accept'] || '').includes('application/json');
    if (wantsJson) {
      return res.status(200).json({ success: true });
    }
    if (next) {
      return res.redirect(302, next);
    }
    return res.status(200).send('Message sent.');
  } catch (err) {
    console.error('Mail error:', err);
    const wantsJson = (req.headers['accept'] || '').includes('application/json');
    if (wantsJson) {
      return res.status(500).json({ error: 'Failed to send' });
    }
    return res.status(500).send('Failed to send message.');
  }
};
