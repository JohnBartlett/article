const nodemailer = require('nodemailer');
const dns = require('dns').promises;

const MIN_COMMENT_LENGTH = 4;

function fakeSuccess(req, res, next) {
  // Always look like a normal success to a bot — no signal that it was rejected.
  const wantsJson = (req.headers['accept'] || '').includes('application/json');
  if (wantsJson) return res.status(200).json({ success: true });
  if (next) return res.redirect(302, next);
  return res.status(200).send('OK');
}

async function isDeliverableDomain(email) {
  const at = email.lastIndexOf('@');
  if (at === -1) return false;
  const domain = email.slice(at + 1).trim();
  if (!domain) return false;
  try {
    const mx = await dns.resolveMx(domain);
    return Array.isArray(mx) && mx.length > 0;
  } catch (err) {
    return false;
  }
}

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

  // Honeypot: real visitors never see or fill this field. Anything in it means a bot.
  if (body._gotcha) {
    return fakeSuccess(req, res, next);
  }

  const fields = Object.entries(body)
    .filter(([k]) => !k.startsWith('_'))
    .map(([k, v]) => `${k}: ${v}`)
    .join('\n');

  // Reject empty submissions (bots, crawlers, health checks)
  if (!fields.trim()) {
    return fakeSuccess(req, res, next);
  }

  // Reject junk/too-short comments (defense in depth — the form's own
  // minlength already blocks this client-side, but bots can post to this
  // endpoint directly, bypassing the HTML entirely). `comment` is the
  // current field name; `message` is used by older article pages.
  for (const field of ['comment', 'message']) {
    const val = body[field];
    if (typeof val === 'string' && val.trim() && val.trim().length < MIN_COMMENT_LENGTH) {
      return fakeSuccess(req, res, next);
    }
  }

  // If an email address was given, flag (don't reject) ones that are
  // malformed or whose domain has no mail servers — catches typos and
  // obviously fake addresses without blocking a genuine reader over a
  // DNS hiccup.
  const EMAIL_FORMAT = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  let emailNote = '';
  if (typeof body.email === 'string' && body.email.trim()) {
    const emailValue = body.email.trim();
    if (!EMAIL_FORMAT.test(emailValue)) {
      emailNote = '\n\n[Note: the email address above is not shaped like a valid email address.]';
    } else {
      const deliverable = await isDeliverableDomain(emailValue);
      if (!deliverable) {
        emailNote = '\n\n[Note: the email address above has no valid mail server on its domain — may be a typo or fake address.]';
      }
    }
  }

  const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
      user: 'john.bartlett@gmail.com',
      pass: process.env.GMAIL_APP_PASSWORD,
    },
  });

  const isWriterApplication = subject === 'Classic Chicago Writer Application';

  try {
    await transporter.sendMail({
      from: 'Classic Chicago Forms <john.bartlett@gmail.com>',
      to: 'john.bartlett@gmail.com',
      cc: isWriterApplication ? 'judycbross@aol.com' : undefined,
      subject,
      text: fields + emailNote,
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
