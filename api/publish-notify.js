import crypto from 'node:crypto';
import { getAccessToken, sendEmail } from './lib/gmail.js';

// Fails closed when required config is missing/empty — mirrors the pattern
// in access-users.js. A misconfigured secret must never fall through to an
// "always allow" state.
export function assertConfig(config) {
  const required = [config.clientId, config.clientSecret, config.refreshToken, config.secret, config.to];
  const missing = required.some((v) => typeof v !== 'string' || v.length === 0);
  if (missing) {
    throw new Error('server misconfigured');
  }
}

export function isValidSecret(provided, expected) {
  if (typeof provided !== 'string' || typeof expected !== 'string' || expected.length === 0) return false;
  const a = Buffer.from(provided);
  const b = Buffer.from(expected);
  if (a.length !== b.length) return false;
  return crypto.timingSafeEqual(a, b);
}

export function buildHandler(deps) {
  const { config } = deps;
  return async function handler(req, res) {
    try {
      assertConfig(config);
    } catch (e) {
      return res.status(500).json({ error: 'server misconfigured' });
    }
    if (req.method !== 'POST') {
      return res.status(405).json({ error: 'method not allowed' });
    }

    const authHeader = req.headers && req.headers.authorization;
    const provided = typeof authHeader === 'string' && authHeader.startsWith('Bearer ')
      ? authHeader.slice('Bearer '.length)
      : null;
    if (!deps.isValidSecret(provided, config.secret)) {
      return res.status(401).json({ error: 'unauthorized' });
    }

    const body = req.body || {};
    const editionDate = typeof body.editionDate === 'string' && body.editionDate.trim()
      ? body.editionDate.trim()
      : null;
    if (!editionDate) {
      return res.status(400).json({ error: 'editionDate is required' });
    }
    const url = typeof body.url === 'string' && body.url.trim() ? body.url.trim() : config.defaultUrl;

    const subject = `Classic Chicago Magazine — ${editionDate} Edition Is Live`;
    const emailBody = `Dear Judy,\n\nThe ${editionDate} edition of Classic Chicago Magazine is now live at:\n\n${url}\n\nCheers, John`;

    try {
      const token = await deps.getAccessToken(config);
      await deps.sendEmail(token, { to: config.to, cc: config.cc, subject, body: emailBody });
      return res.status(200).json({ sent: true });
    } catch (e) {
      return res.status(502).json({ error: e.message });
    }
  };
}

function configFromEnv() {
  const env = process.env;
  return {
    config: {
      clientId: env.GMAIL_CLIENT_ID,
      clientSecret: env.GMAIL_CLIENT_SECRET,
      refreshToken: env.GMAIL_REFRESH_TOKEN,
      secret: env.PUBLISH_NOTIFY_SECRET,
      to: env.PUBLISH_NOTIFY_TO,
      cc: env.PUBLISH_NOTIFY_CC,
      defaultUrl: env.PUBLISH_NOTIFY_DEFAULT_URL || 'https://chicagoclassicmag.com',
    },
    isValidSecret,
    getAccessToken,
    sendEmail,
  };
}

export default function handler(req, res) {
  return buildHandler(configFromEnv())(req, res);
}
