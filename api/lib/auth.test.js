import { test } from 'node:test';
import assert from 'node:assert/strict';
import { getAuthorizedEmail } from './auth.js';

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
