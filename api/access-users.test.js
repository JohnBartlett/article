import { test } from 'node:test';
import assert from 'node:assert/strict';
import { buildHandler } from './access-users.js';

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
