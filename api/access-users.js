import { getAuthorizedEmail, verifyAccessJwt } from './lib/auth.js';
import { getPolicyEmails, setPolicyEmails } from './lib/cloudflare.js';
import { addEmail, removeEmail, validateEmail } from './lib/access-list.js';

// Fails closed when required config is missing/empty. Rationale: jose skips
// audience validation when `aud` is undefined, and the lockout guard in
// access-list.js degrades silently if adminEmail is unset/invalid — both
// must be caught here before any request is processed.
export function assertConfig(config, authConfig) {
  const required = [
    authConfig && authConfig.teamDomain,
    authConfig && authConfig.aud,
    authConfig && authConfig.adminEmail,
    config && config.accountId,
    config && config.appId,
    config && config.policyId,
    config && config.token,
  ];
  const missing = required.some((v) => typeof v !== 'string' || v.length === 0);
  if (missing || !validateEmail(authConfig.adminEmail)) {
    throw new Error('server misconfigured');
  }
}

// CSRF note: this endpoint relies on Cloudflare Access's session model plus
// requiring `application/json` bodies for state-changing requests (POST/DELETE).
// Simple HTML forms cannot set a JSON content-type, so a cross-site form post
// cannot trigger a mutation here — no separate CSRF token is needed.
export function buildHandler(deps) {
  const { config, authConfig } = deps;
  return async function handler(req, res) {
    try {
      assertConfig(config, authConfig);
    } catch (e) {
      return res.status(500).json({ error: 'server misconfigured' });
    }
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
        if (next.length === 0) {
          const e = new Error('refusing to empty the allowlist');
          e.status = 400;
          throw e;
        }
        await deps.setPolicyEmails(config, next);
        return res.status(200).json({ emails: next });
      }
      return res.status(405).json({ error: 'method not allowed' });
    } catch (e) {
      return res.status(e.status || 502).json({ error: e.message });
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
