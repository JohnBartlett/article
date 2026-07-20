import { createRemoteJWKSet, jwtVerify } from 'jose';

function httpError(status, message) {
  const e = new Error(message);
  e.status = status;
  return e;
}

const jwksCache = new Map();
function jwksFor(teamDomain) {
  if (!jwksCache.has(teamDomain)) {
    jwksCache.set(teamDomain, createRemoteJWKSet(
      new URL(`https://${teamDomain}/cdn-cgi/access/certs`)));
  }
  return jwksCache.get(teamDomain);
}

// Real verifier used in production wiring.
export async function verifyAccessJwt(token, { teamDomain, aud }) {
  const { payload } = await jwtVerify(token, jwksFor(teamDomain), {
    issuer: `https://${teamDomain}`,
    audience: aud,
  });
  return { email: payload.email };
}

export async function getAuthorizedEmail(headers, authConfig, verifyFn) {
  const token = headers['cf-access-jwt-assertion'];
  if (!token) throw httpError(401, 'missing Cloudflare Access token');
  let claims;
  try {
    claims = await verifyFn(token, { teamDomain: authConfig.teamDomain, aud: authConfig.aud });
  } catch {
    throw httpError(401, 'invalid Cloudflare Access token');
  }
  const email = String(claims.email || '').trim().toLowerCase();
  if (email !== authConfig.adminEmail.toLowerCase()) {
    throw httpError(403, 'not authorized');
  }
  return email;
}
