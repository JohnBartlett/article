import { test } from 'node:test';
import assert from 'node:assert/strict';
import { getPolicyEmails, setPolicyEmails } from './cloudflare.js';

const config = { accountId: 'acct', appId: 'app', policyId: 'pol', token: 'tok' };

function fakeFetch(responseBody, capture) {
  return async (url, opts) => {
    if (capture) { capture.url = url; capture.opts = opts; }
    return { ok: true, status: 200, json: async () => responseBody };
  };
}

test('getPolicyEmails extracts email include rules', async () => {
  const body = { success: true, result: { name: 'Editors', decision: 'allow',
    include: [ { email: { email: 'a@b.com' } }, { email: { email: 'c@d.com' } } ] } };
  const emails = await getPolicyEmails(config, fakeFetch(body));
  assert.deepEqual(emails, ['a@b.com', 'c@d.com']);
});

test('getPolicyEmails sends the auth header and hits the policy URL', async () => {
  const cap = {};
  const body = { success: true, result: { name: 'Editors', decision: 'allow', include: [] } };
  await getPolicyEmails(config, fakeFetch(body, cap));
  assert.match(cap.url, /accounts\/acct\/access\/apps\/app\/policies\/pol$/);
  assert.equal(cap.opts.headers.Authorization, 'Bearer tok');
});

test('setPolicyEmails PUTs name+decision+rebuilt include, preserving non-email rules', async () => {
  const cap = {};
  // GET first (current policy has one non-email rule to preserve), then PUT.
  let call = 0;
  const fetchFn = async (url, opts) => {
    call++;
    if (call === 1) {
      return { ok: true, status: 200, json: async () => ({ success: true, result: {
        name: 'Editors', decision: 'allow',
        include: [ { everyone: {} }, { email: { email: 'old@x.com' } } ] } }) };
    }
    cap.url = url; cap.opts = opts;
    return { ok: true, status: 200, json: async () => ({ success: true, result: {} }) };
  };
  await setPolicyEmails(config, ['new@x.com'], fetchFn);
  assert.equal(cap.opts.method, 'PUT');
  const sent = JSON.parse(cap.opts.body);
  assert.equal(sent.name, 'Editors');
  assert.equal(sent.decision, 'allow');
  assert.deepEqual(sent.include, [ { everyone: {} }, { email: { email: 'new@x.com' } } ]);
});

test('setPolicyEmails preserves other policy fields (e.g. session_duration) on write', async () => {
  const cap = {};
  let call = 0;
  const fetchFn = async (url, opts) => {
    call++;
    if (call === 1) {
      return { ok: true, status: 200, json: async () => ({ success: true, result: {
        name: 'Editors', decision: 'allow', session_duration: '24h',
        include: [ { email: { email: 'old@x.com' } } ] } }) };
    }
    cap.url = url; cap.opts = opts;
    return { ok: true, status: 200, json: async () => ({ success: true, result: {} }) };
  };
  await setPolicyEmails(config, ['new@x.com'], fetchFn);
  const sent = JSON.parse(cap.opts.body);
  assert.equal(sent.session_duration, '24h');
});

test('getPolicyEmails throws on API error', async () => {
  const fetchFn = async () => ({ ok: false, status: 403, json: async () => ({ success: false, errors: [{ message: 'nope' }] }) });
  await assert.rejects(() => getPolicyEmails(config, fetchFn), /cloudflare api/i);
});
