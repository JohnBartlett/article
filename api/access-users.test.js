import { test } from 'node:test';
import assert from 'node:assert/strict';
import { buildHandler, assertConfig } from './access-users.js';

function mockRes() {
  return { _status: 200, _json: null,
    status(c) { this._status = c; return this; },
    json(o) { this._json = o; return this; } };
}

const deps = {
  config: { accountId: 'a', appId: 'app', policyId: 'p', token: 't' },
  authConfig: { teamDomain: 'team', aud: 'AUD', adminEmail: 'john@x.com' },
  getAuthorizedEmail: async () => 'john@x.com',
  getPolicyEmails: async () => ['john@x.com', 'a@b.com'],
  setPolicyEmails: async () => {},
};

test('GET returns the current emails', async () => {
  const handler = buildHandler(deps);
  const res = mockRes();
  await handler({ method: 'GET', headers: {}, body: {} }, res);
  assert.equal(res._status, 200);
  assert.deepEqual(res._json, { emails: ['john@x.com', 'a@b.com'] });
});

test('POST adds an email and returns the new list', async () => {
  let saved = null;
  const handler = buildHandler({ ...deps, setPolicyEmails: async (_c, emails) => { saved = emails; } });
  const res = mockRes();
  await handler({ method: 'POST', headers: {}, body: { email: 'New@x.com' } }, res);
  assert.equal(res._status, 200);
  assert.deepEqual(saved, ['john@x.com', 'a@b.com', 'new@x.com']);
});

test('DELETE removes an email', async () => {
  let saved = null;
  const handler = buildHandler({ ...deps, setPolicyEmails: async (_c, emails) => { saved = emails; } });
  const res = mockRes();
  await handler({ method: 'DELETE', headers: {}, body: { email: 'a@b.com' } }, res);
  assert.deepEqual(saved, ['john@x.com']);
});

test('DELETE of the admin email is rejected 400', async () => {
  const handler = buildHandler(deps);
  const res = mockRes();
  await handler({ method: 'DELETE', headers: {}, body: { email: 'john@x.com' } }, res);
  assert.equal(res._status, 400);
});

test('unauthorized caller gets the auth error status', async () => {
  const handler = buildHandler({ ...deps, getAuthorizedEmail: async () => { const e = new Error('no'); e.status = 403; throw e; } });
  const res = mockRes();
  await handler({ method: 'GET', headers: {}, body: {} }, res);
  assert.equal(res._status, 403);
});

test('unknown method gets 405', async () => {
  const handler = buildHandler(deps);
  const res = mockRes();
  await handler({ method: 'PUT', headers: {}, body: {} }, res);
  assert.equal(res._status, 405);
});

test('assertConfig throws when aud is missing', () => {
  assert.throws(() => assertConfig(deps.config, { ...deps.authConfig, aud: '' }));
  assert.throws(() => assertConfig(deps.config, { ...deps.authConfig, aud: undefined }));
});

test('assertConfig throws when adminEmail is missing or invalid', () => {
  assert.throws(() => assertConfig(deps.config, { ...deps.authConfig, adminEmail: '' }));
  assert.throws(() => assertConfig(deps.config, { ...deps.authConfig, adminEmail: 'not-an-email' }));
});

test('assertConfig passes with a fully populated config', () => {
  assert.doesNotThrow(() => assertConfig(deps.config, deps.authConfig));
});

test('missing aud in config: request returns 500 and never calls getPolicyEmails/setPolicyEmails', async () => {
  let getCalled = false;
  let setCalled = false;
  const handler = buildHandler({
    ...deps,
    authConfig: { ...deps.authConfig, aud: '' },
    getPolicyEmails: async () => { getCalled = true; return []; },
    setPolicyEmails: async () => { setCalled = true; },
  });
  const res = mockRes();
  await handler({ method: 'GET', headers: {}, body: {} }, res);
  assert.equal(res._status, 500);
  assert.deepEqual(res._json, { error: 'server misconfigured' });
  assert.equal(getCalled, false);
  assert.equal(setCalled, false);
});

test('missing adminEmail in config: request returns 500 and never calls getPolicyEmails/setPolicyEmails', async () => {
  let getCalled = false;
  let setCalled = false;
  const handler = buildHandler({
    ...deps,
    authConfig: { ...deps.authConfig, adminEmail: '' },
    getPolicyEmails: async () => { getCalled = true; return []; },
    setPolicyEmails: async () => { setCalled = true; },
  });
  const res = mockRes();
  await handler({ method: 'GET', headers: {}, body: {} }, res);
  assert.equal(res._status, 500);
  assert.deepEqual(res._json, { error: 'server misconfigured' });
  assert.equal(getCalled, false);
  assert.equal(setCalled, false);
});

test('DELETE that would empty the allowlist is refused with 400 and setPolicyEmails is not called', async () => {
  let setCalled = false;
  const handler = buildHandler({
    ...deps,
    getPolicyEmails: async () => ['a@b.com'],
    // adminEmail differs from the sole remaining entry so removeEmail succeeds,
    // leaving an empty list for the guard to catch.
    authConfig: { ...deps.authConfig, adminEmail: 'someone-else@x.com' },
    setPolicyEmails: async () => { setCalled = true; },
  });
  const res = mockRes();
  await handler({ method: 'DELETE', headers: {}, body: { email: 'a@b.com' } }, res);
  assert.equal(res._status, 400);
  assert.deepEqual(res._json, { error: 'refusing to empty the allowlist' });
  assert.equal(setCalled, false);
});

test('DELETE of the admin email is still rejected 400 after error-status changes', async () => {
  const handler = buildHandler(deps);
  const res = mockRes();
  await handler({ method: 'DELETE', headers: {}, body: { email: 'john@x.com' } }, res);
  assert.equal(res._status, 400);
});

test('invalid email on POST is still rejected 400', async () => {
  const handler = buildHandler(deps);
  const res = mockRes();
  await handler({ method: 'POST', headers: {}, body: { email: 'not-an-email' } }, res);
  assert.equal(res._status, 400);
});

test('a plain Error thrown by getPolicyEmails (upstream failure) surfaces as 502', async () => {
  const handler = buildHandler({
    ...deps,
    getPolicyEmails: async () => { throw new Error('Cloudflare API error: boom'); },
  });
  const res = mockRes();
  await handler({ method: 'GET', headers: {}, body: {} }, res);
  assert.equal(res._status, 502);
});
