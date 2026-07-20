import { getAuthorizedEmail, verifyAccessJwt } from './lib/auth.js';
import { getPolicyEmails, setPolicyEmails } from './lib/cloudflare.js';
import { addEmail, removeEmail } from './lib/access-list.js';

export function buildHandler(deps) {
  const { config, authConfig } = deps;
  return async function handler(req, res) {
    // 1) authorize
    let adminEmail;
    try {
      adminEmail = await deps.getAuthorizedEmail(req.headers, authConfig, verifyAccessJwt);
    } catch (e) {
      return res.status(e.status || 401).json({ error: e.message });
    }
    try {
      if (req.method === 'GET') {
        const emails = await deps.getPolicyEmails(config);
        return res.status(200).json({ emails });
      }
      if (req.method === 'POST' || req.method === 'DELETE') {
        const email = req.body && req.body.email;
        const current = await deps.getPolicyEmails(config);
        const next = req.method === 'POST'
          ? addEmail(current, email)
          : removeEmail(current, email, authConfig.adminEmail);
        await deps.setPolicyEmails(config, next);
        return res.status(200).json({ emails: next });
      }
      return res.status(405).json({ error: 'method not allowed' });
    } catch (e) {
      return res.status(400).json({ error: e.message });
    }
  };
}

function configFromEnv() {
  const env = process.env;
  return {
    config: {
      accountId: env.CF_ACCOUNT_ID,
      appId: env.CF_ACCESS_APP_ID,
      policyId: env.CF_ACCESS_POLICY_ID,
      token: env.CF_API_TOKEN,
    },
    authConfig: {
      teamDomain: env.CF_ACCESS_TEAM_DOMAIN,
      aud: env.CF_ADMIN_AUD,
      adminEmail: env.ADMIN_EMAIL,
    },
    getAuthorizedEmail,
    getPolicyEmails,
    setPolicyEmails,
  };
}

export default function handler(req, res) {
  return buildHandler(configFromEnv())(req, res);
}
