import test from 'node:test';
import assert from 'node:assert/strict';
import middleware from './middleware.js';

process.env.DASHBOARD_PASSWORD = 'test-word';
const base = 'https://2ccmag.com';

function post(body) {
  return new Request(base + '/__login', {
    method: 'POST',
    headers: { 'content-type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams(body).toString(),
  });
}

test('no cookie shows the login page', async () => {
  const r = await middleware(new Request(base + '/dashboard'));
  assert.equal(r.status, 401);
  assert.match(await r.text(), /name="next" value="\/dashboard"/);
});

test('wrong password is refused without a cookie', async () => {
  const r = await middleware(post({ password: 'nope', next: '/comments' }));
  assert.equal(r.status, 401);
  assert.equal(r.headers.get('set-cookie'), null);
});

test('right password sets the cookie and redirects, and the cookie lets requests through', async () => {
  const r = await middleware(post({ password: 'test-word', next: '/comments' }));
  assert.equal(r.status, 303);
  assert.equal(r.headers.get('location'), '/comments');
  const cookie = r.headers.get('set-cookie').split(';')[0];
  const ok = await middleware(new Request(base + '/dashboard', { headers: { cookie } }));
  assert.equal(ok.headers.get('x-middleware-next'), '1');
});

test('open redirects are blocked', async () => {
  const r = await middleware(post({ password: 'test-word', next: '//evil.example' }));
  assert.equal(r.headers.get('location'), '/dashboard');
});

test('a forged cookie is refused', async () => {
  const r = await middleware(new Request(base + '/dashboard', { headers: { cookie: 'ccm_editors=abc' } }));
  assert.equal(r.status, 401);
});

test('missing password env locks the site', async () => {
  const saved = process.env.DASHBOARD_PASSWORD;
  delete process.env.DASHBOARD_PASSWORD;
  const r = await middleware(new Request(base + '/dashboard'));
  assert.equal(r.status, 503);
  process.env.DASHBOARD_PASSWORD = saved;
});
