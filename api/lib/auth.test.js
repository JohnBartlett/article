import { test } from 'node:test';
import assert from 'node:assert/strict';
import { generateKeyPair, exportJWK, SignJWT, createLocalJWKSet } from 'jose';
import { getAuthorizedEmail, verifyAccessJwt } from './auth.js';

const authConfig = { teamDomain: 'team.cloudflareaccess.com', aud: 'AUD', adminEmail: 'john@x.com' };
const headers = { 'cf-access-jwt-assertion': 'token123' };

test('returns email when token verifies and matches admin', async () => {
  const verify = async () => ({ email: 'John@x.com' });
  assert.equal(await getAuthorizedEmail(headers, authConfig, verify), 'john@x.com');
});

test('throws 401 when the token header is missing', async () => {
  const verify = async () => ({ email: 'john@x.com' });
  await assert.rejects(
    () => getAuthorizedEmail({}, authConfig, verify),
    (e) => e.status === 401);
});

test('throws 401 when verification fails', async () => {
  const verify = async () => { throw new Error('bad sig'); };
  await assert.rejects(
    () => getAuthorizedEmail(headers, authConfig, verify),
    (e) => e.status === 401);
});

test('throws 403 when a valid token is not the admin', async () => {
  const verify = async () => ({ email: 'someoneelse@x.com' });
  await assert.rejects(
    () => getAuthorizedEmail(headers, authConfig, verify),
    (e) => e.status === 403);
});

test('real verifyAccessJwt enforces iss/aud against a local JWKS', async () => {
  const { publicKey, privateKey } = await generateKeyPair('RS256');
  const jwk = await exportJWK(publicKey);
  jwk.kid = 'test-key-1';
  jwk.alg = 'RS256';
  const localJwks = createLocalJWKSet({ keys: [jwk] });

  const teamDomain = authConfig.teamDomain;
  const aud = authConfig.aud;

  const sign = (claims, iss = `https://${teamDomain}`, audience = aud) =>
    new SignJWT({ email: 'john@x.com', ...claims })
      .setProtectedHeader({ alg: 'RS256', kid: 'test-key-1' })
      .setIssuedAt()
      .setIssuer(iss)
      .setAudience(audience)
      .setExpirationTime('5m')
      .sign(privateKey);

  const goodToken = await sign({});
  const result = await verifyAccessJwt(goodToken, { teamDomain, aud }, localJwks);
  assert.equal(result.email, 'john@x.com');

  const wrongAudToken = await sign({}, `https://${teamDomain}`, 'WRONG_AUD');
  await assert.rejects(() => verifyAccessJwt(wrongAudToken, { teamDomain, aud }, localJwks));

  const wrongIssToken = await sign({}, 'https://evil.example.com', aud);
  await assert.rejects(() => verifyAccessJwt(wrongIssToken, { teamDomain, aud }, localJwks));
});
