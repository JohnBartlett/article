import { test } from 'node:test';
import assert from 'node:assert/strict';
import { buildHandler, assertConfig, isValidSecret } from './publish-notify.js';

function mockRes() {
  return {
    _status: 200, _json: null,
    status(c) { this._status = c; return this; },
    json(o) { this._json = o; return this; },
  };
}

const baseConfig = {
  clientId: 'id', clientSecret: 'secret', refreshToken: 'refresh',
  secret: 'the-shared-secret', to: 'judycbross@aol.com', cc: 'john.bartlett@gmail.com',
  defaultUrl: 'https://chicagoclassicmag.com',
};

function makeDeps(overrides = {}) {
  return {
    config: baseConfig,
    isValidSecret,
    getAccessToken: async () => 'fake-access-token',
    sendEmail: async () => ({ id: 'fake-message-id' }),
    ...overrides,
  };
}

test('rejects non-POST methods', async () => {
  const handler = buildHandler(makeDeps());
  const res = mockRes();
  await handler({ method: 'GET', headers: {}, body: {} }, res);
  assert.equal(res._status, 405);
});

test('rejects missing/invalid bearer secret', async () => {
  const handler = buildHandler(makeDeps());
  const res = mockRes();
  await handler({ method: 'POST', headers: {}, body: { editionDate: 'August 2, 2026' } }, res);
  assert.equal(res._status, 401);
});

test('rejects wrong bearer secret', async () => {
  const handler = buildHandler(makeDeps());
  const res = mockRes();
  await handler({
    method: 'POST',
    headers: { authorization: 'Bearer wrong-secret' },
    body: { editionDate: 'August 2, 2026' },
  }, res);
  assert.equal(res._status, 401);
});

test('rejects missing editionDate', async () => {
  const handler = buildHandler(makeDeps());
  const res = mockRes();
  await handler({
    method: 'POST',
    headers: { authorization: 'Bearer the-shared-secret' },
    body: {},
  }, res);
  assert.equal(res._status, 400);
});

test('sends email and returns 200 on valid request', async () => {
  let sentWith = null;
  const handler = buildHandler(makeDeps({
    sendEmail: async (token, message) => { sentWith = { token, message }; return { id: 'x' }; },
  }));
  const res = mockRes();
  await handler({
    method: 'POST',
    headers: { authorization: 'Bearer the-shared-secret' },
    body: { editionDate: 'August 2, 2026' },
  }, res);
  assert.equal(res._status, 200);
  assert.deepEqual(res._json, { sent: true });
  assert.equal(sentWith.token, 'fake-access-token');
  assert.equal(sentWith.message.to, 'judycbross@aol.com');
  assert.equal(sentWith.message.cc, 'john.bartlett@gmail.com');
  assert.match(sentWith.message.subject, /August 2, 2026/);
  assert.match(sentWith.message.body, /chicagoclassicmag\.com/);
});

test('uses caller-supplied url when provided', async () => {
  let sentWith = null;
  const handler = buildHandler(makeDeps({
    sendEmail: async (token, message) => { sentWith = message; return { id: 'x' }; },
  }));
  const res = mockRes();
  await handler({
    method: 'POST',
    headers: { authorization: 'Bearer the-shared-secret' },
    body: { editionDate: 'August 2, 2026', url: 'https://article-dev2.vercel.app' },
  }, res);
  assert.equal(res._status, 200);
  assert.match(sentWith.body, /article-dev2\.vercel\.app/);
});

test('returns 502 when the Gmail send fails', async () => {
  const handler = buildHandler(makeDeps({
    sendEmail: async () => { throw new Error('gmail send failed: 500 boom'); },
  }));
  const res = mockRes();
  await handler({
    method: 'POST',
    headers: { authorization: 'Bearer the-shared-secret' },
    body: { editionDate: 'August 2, 2026' },
  }, res);
  assert.equal(res._status, 502);
});

test('assertConfig throws when any required field is missing', () => {
  assert.throws(() => assertConfig({ ...baseConfig, secret: '' }));
  assert.throws(() => assertConfig({ ...baseConfig, to: undefined }));
  assert.doesNotThrow(() => assertConfig(baseConfig));
});
