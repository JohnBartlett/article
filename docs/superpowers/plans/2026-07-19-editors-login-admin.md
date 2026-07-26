# Editors Login Admin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a John-only `/admin` page on `editors.2ccmag.com` that adds/removes login emails on the Cloudflare Access "Editors" policy via a Vercel serverless function.

**Architecture:** All code lives on the **`editors`** git branch (deployed by the `ccm-editors` Vercel project). A static `admin.html` calls a Node ESM serverless function `api/access-users.js`, which verifies the caller is John (Cloudflare Access JWT) and edits the Cloudflare Access policy through the Cloudflare API. Pure logic is split into small, injectable modules so it is unit-testable with Node's built-in test runner.

**Tech Stack:** Node.js (Vercel serverless, ESM), `jose` (Access JWT verification), Cloudflare API v4, `node:test` for tests. No frontend framework — `admin.html` is vanilla HTML + fetch.

## Global Constraints

- All work happens on the **`editors`** branch, in a dedicated git worktree (the `editors` branch is orphan/disconnected from `dev2`/`dev`/`master` — never merge across).
- Node runtime: Vercel default (Node 24). Use ESM (`"type": "module"` in `package.json`).
- The protected/admin email is `john.bartlett@gmail.com` (env `ADMIN_EMAIL`). It can never be removed from the allowlist.
- Cloudflare account id: `865fb6f8947e64cf5971cc3095f8eaf8`. Access team domain: `john-bartlett.cloudflareaccess.com`.
- Secrets (`CF_API_TOKEN`) live only in Vercel env vars, never in the browser or git.
- The 6-hour refresh workflow only rewrites `editors/dashboard.html`; do not touch that file. New files (`admin.html`, `api/**`, `package.json`, `vercel.json`) are independent and persist.
- Frequent commits, TDD, DRY, YAGNI.

---

## Task 1: Scaffold branch worktree, package.json, vercel.json rewrite

**Files:**
- Create: `package.json`
- Modify: `vercel.json` (add `/admin` rewrite)
- Create: `api/lib/` (directory, via first file in Task 2)

**Interfaces:**
- Produces: an installable Node project on the `editors` branch with `jose` available to functions, and a `/admin` → `/admin.html` rewrite.

- [ ] **Step 1: Create an editors worktree**

```bash
cd /Users/john/article
git worktree add /tmp/editors-admin editors
cd /tmp/editors-admin
```

- [ ] **Step 2: Create `package.json`**

```json
{
  "name": "ccm-editors",
  "private": true,
  "type": "module",
  "dependencies": {
    "jose": "^5.9.6"
  },
  "scripts": {
    "test": "node --test"
  }
}
```

- [ ] **Step 3: Install deps and confirm the test runner works**

Run: `cd /tmp/editors-admin && npm install`
Expected: `jose` installed, `node_modules/` created, no errors.

- [ ] **Step 4: Add `.gitignore` entry for node_modules**

Append to `.gitignore` (create if absent):

```
node_modules/
```

- [ ] **Step 5: Add the `/admin` rewrite to `vercel.json`**

Current `vercel.json` has `redirects` (`/`→`/dashboard`, `/stats`→`/dashboard`) and `rewrites` for `/comments`, `/future`, `/dashboard`. Add one rewrite so `/admin` serves `admin.html`. The full `rewrites` array becomes:

```json
"rewrites": [
  { "source": "/comments", "destination": "/reader-comments.html" },
  { "source": "/future",   "destination": "/future-articles.html" },
  { "source": "/dashboard", "destination": "/editors/dashboard.html" },
  { "source": "/admin",     "destination": "/admin.html" }
]
```

- [ ] **Step 6: Commit**

```bash
git add package.json vercel.json .gitignore
git commit -m "chore: scaffold node project + /admin rewrite for editors login admin"
```

---

## Task 2: Email allowlist logic (`api/lib/access-list.js`)

Pure functions for validating and mutating the email list. No network, no env — trivially testable.

**Files:**
- Create: `api/lib/access-list.js`
- Test: `api/lib/access-list.test.js`

**Interfaces:**
- Produces:
  - `validateEmail(email: string): boolean`
  - `normalizeEmail(email: string): string` — trimmed, lowercased
  - `addEmail(emails: string[], email: string): string[]` — returns new array, deduped (case-insensitive), throws `Error` on invalid email
  - `removeEmail(emails: string[], email: string, protectedEmail: string): string[]` — returns new array without `email`; throws `Error` if `email` equals `protectedEmail` (case-insensitive)

- [ ] **Step 1: Write the failing test**

`api/lib/access-list.test.js`:

```js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { validateEmail, normalizeEmail, addEmail, removeEmail } from './access-list.js';

test('validateEmail accepts a normal address and rejects junk', () => {
  assert.equal(validateEmail('a@b.com'), true);
  assert.equal(validateEmail('nope'), false);
  assert.equal(validateEmail(''), false);
  assert.equal(validateEmail('a@b'), false);
});

test('normalizeEmail trims and lowercases', () => {
  assert.equal(normalizeEmail('  John@Example.COM '), 'john@example.com');
});

test('addEmail adds and dedupes case-insensitively', () => {
  assert.deepEqual(addEmail(['a@b.com'], 'c@d.com'), ['a@b.com', 'c@d.com']);
  assert.deepEqual(addEmail(['a@b.com'], 'A@B.com'), ['a@b.com']);
});

test('addEmail throws on invalid email', () => {
  assert.throws(() => addEmail([], 'nope'), /invalid email/i);
});

test('removeEmail removes case-insensitively and is a no-op if absent', () => {
  assert.deepEqual(removeEmail(['a@b.com', 'c@d.com'], 'C@D.com', 'x@y.com'), ['a@b.com']);
  assert.deepEqual(removeEmail(['a@b.com'], 'z@z.com', 'x@y.com'), ['a@b.com']);
});

test('removeEmail refuses to remove the protected email', () => {
  assert.throws(() => removeEmail(['john@x.com'], 'JOHN@x.com', 'john@x.com'), /cannot remove/i);
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node --test api/lib/access-list.test.js`
Expected: FAIL — cannot find module `./access-list.js`.

- [ ] **Step 3: Write minimal implementation**

`api/lib/access-list.js`:

```js
export function validateEmail(email) {
  if (typeof email !== 'string') return false;
  // simple, deliberately conservative address check
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim());
}

export function normalizeEmail(email) {
  return String(email).trim().toLowerCase();
}

export function addEmail(emails, email) {
  if (!validateEmail(email)) throw new Error('invalid email');
  const norm = normalizeEmail(email);
  if (emails.some((e) => normalizeEmail(e) === norm)) return emails.slice();
  return [...emails, norm];
}

export function removeEmail(emails, email, protectedEmail) {
  const norm = normalizeEmail(email);
  if (norm === normalizeEmail(protectedEmail)) {
    throw new Error('cannot remove the protected admin email');
  }
  return emails.filter((e) => normalizeEmail(e) !== norm);
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `node --test api/lib/access-list.test.js`
Expected: PASS (all tests).

- [ ] **Step 5: Commit**

```bash
git add api/lib/access-list.js api/lib/access-list.test.js
git commit -m "feat: email allowlist logic (validate/add/remove) for login admin"
```

---

## Task 3: Cloudflare policy read/write (`api/lib/cloudflare.js`)

Reads and writes the "Editors" Access policy's email allowlist through the Cloudflare API. `fetch` is injected so tests use a fake.

**Files:**
- Create: `api/lib/cloudflare.js`
- Test: `api/lib/cloudflare.test.js`

**Interfaces:**
- Consumes: none.
- Produces:
  - `getPolicyEmails(config, fetchFn): Promise<string[]>`
  - `setPolicyEmails(config, emails: string[], fetchFn): Promise<void>`
  - where `config = { accountId, appId, policyId, token }`.
- Cloudflare policy shape: emails live in `result.include` as `{ email: { email: "x@y.com" } }` entries. Non-email include rules (if any) are preserved on write.

- [ ] **Step 1: Write the failing test**

`api/lib/cloudflare.test.js`:

```js
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

test('getPolicyEmails throws on API error', async () => {
  const fetchFn = async () => ({ ok: false, status: 403, json: async () => ({ success: false, errors: [{ message: 'nope' }] }) });
  await assert.rejects(() => getPolicyEmails(config, fetchFn), /cloudflare api/i);
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node --test api/lib/cloudflare.test.js`
Expected: FAIL — cannot find module `./cloudflare.js`.

- [ ] **Step 3: Write minimal implementation**

`api/lib/cloudflare.js`:

```js
const BASE = 'https://api.cloudflare.com/client/v4';

function policyUrl({ accountId, appId, policyId }) {
  return `${BASE}/accounts/${accountId}/access/apps/${appId}/policies/${policyId}`;
}

async function callCf(url, opts, token, fetchFn) {
  const res = await fetchFn(url, {
    ...opts,
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
      ...(opts.headers || {}),
    },
  });
  const data = await res.json();
  if (!res.ok || data.success === false) {
    const msg = data?.errors?.[0]?.message || `status ${res.status}`;
    throw new Error(`Cloudflare API error: ${msg}`);
  }
  return data.result;
}

async function getPolicy(config, fetchFn) {
  return callCf(policyUrl(config), { method: 'GET' }, config.token, fetchFn);
}

export async function getPolicyEmails(config, fetchFn = fetch) {
  const policy = await getPolicy(config, fetchFn);
  return (policy.include || [])
    .filter((r) => r.email && typeof r.email.email === 'string')
    .map((r) => r.email.email);
}

export async function setPolicyEmails(config, emails, fetchFn = fetch) {
  const policy = await getPolicy(config, fetchFn);
  const nonEmail = (policy.include || []).filter((r) => !r.email);
  const emailRules = emails.map((email) => ({ email: { email } }));
  const body = {
    name: policy.name,
    decision: policy.decision,
    include: [...nonEmail, ...emailRules],
  };
  await callCf(policyUrl(config), { method: 'PUT', body: JSON.stringify(body) }, config.token, fetchFn);
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `node --test api/lib/cloudflare.test.js`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add api/lib/cloudflare.js api/lib/cloudflare.test.js
git commit -m "feat: read/write Cloudflare Access policy email allowlist"
```

---

## Task 4: Access JWT verification (`api/lib/auth.js`)

Confirms the request carries a valid Cloudflare Access JWT for the admin app and that the identity is the admin email. The JWT verifier is injected so tests avoid real network/JWKS.

**Files:**
- Create: `api/lib/auth.js`
- Test: `api/lib/auth.test.js`

**Interfaces:**
- Consumes: none.
- Produces:
  - `getAuthorizedEmail(headers, authConfig, verifyFn): Promise<string>` — returns the email if the `cf-access-jwt-assertion` header verifies AND its `email` equals `authConfig.adminEmail`; otherwise throws `Error` with `.status` 401 (missing/invalid token) or 403 (valid token, wrong identity).
  - `authConfig = { teamDomain, aud, adminEmail }`.
  - `verifyFn(token, { teamDomain, aud }): Promise<{ email }>` — real impl uses `jose`; tests inject a fake.
  - `verifyAccessJwt(token, { teamDomain, aud }): Promise<{ email }>` — the real `jose`-based verifier exported for wiring.

- [ ] **Step 1: Write the failing test**

`api/lib/auth.test.js`:

```js
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node --test api/lib/auth.test.js`
Expected: FAIL — cannot find module `./auth.js`.

- [ ] **Step 3: Write minimal implementation**

`api/lib/auth.js`:

```js
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `node --test api/lib/auth.test.js`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add api/lib/auth.js api/lib/auth.test.js
git commit -m "feat: verify Cloudflare Access JWT and enforce admin identity"
```

---

## Task 5: Serverless handler (`api/access-users.js`)

Wires auth + Cloudflare + list logic into a Vercel HTTP function. Reads env config. Thin — the tested logic lives in the libs.

**Files:**
- Create: `api/access-users.js`
- Test: `api/access-users.test.js`

**Interfaces:**
- Consumes: `getAuthorizedEmail`, `verifyAccessJwt` (auth.js); `getPolicyEmails`, `setPolicyEmails` (cloudflare.js); `addEmail`, `removeEmail`, `validateEmail` (access-list.js).
- Produces: default export `handler(req, res)` (Vercel Node function). Also exports `buildHandler(deps)` so tests inject fakes.
- Env: `CF_API_TOKEN`, `CF_ACCOUNT_ID`, `CF_ACCESS_APP_ID`, `CF_ACCESS_POLICY_ID`, `CF_ACCESS_TEAM_DOMAIN`, `CF_ADMIN_AUD`, `ADMIN_EMAIL`.

- [ ] **Step 1: Write the failing test**

`api/access-users.test.js`:

```js
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node --test api/access-users.test.js`
Expected: FAIL — `buildHandler` not exported.

- [ ] **Step 3: Write minimal implementation**

`api/access-users.js`:

```js
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
```

Note: `buildHandler` receives the real `getAuthorizedEmail`/`getPolicyEmails`/`setPolicyEmails` in production (via `configFromEnv`); those call `verifyAccessJwt` and the global `fetch` respectively.

- [ ] **Step 4: Run test to verify it passes**

Run: `node --test api/access-users.test.js`
Expected: PASS.

- [ ] **Step 5: Run the whole suite**

Run: `node --test`
Expected: PASS (all four test files).

- [ ] **Step 6: Commit**

```bash
git add api/access-users.js api/access-users.test.js
git commit -m "feat: /api/access-users handler wiring auth + Cloudflare + list logic"
```

---

## Task 6: Admin page (`admin.html`)

Static page: lists emails, add form, remove buttons. Calls the API on the same origin. Matches the existing editors visual style (simple, `Lato`/system fonts, red `#b51c20` accents like the dashboard).

**Files:**
- Create: `admin.html`

**Interfaces:**
- Consumes: `GET/POST/DELETE /api/access-users` returning `{ emails }` or `{ error }`.

- [ ] **Step 1: Write `admin.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Editor Logins — Admin</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body { font-family: 'Lato', system-ui, sans-serif; max-width: 640px; margin: 40px auto; padding: 0 20px; color: #222; }
    h1 { font-size: 22px; border-bottom: 3px solid #b51c20; padding-bottom: 10px; }
    .row { display: flex; align-items: center; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #eee; }
    .email { font-family: monospace; font-size: 15px; }
    button { font-family: inherit; cursor: pointer; }
    .remove { background: none; border: 1px solid #b51c20; color: #b51c20; border-radius: 3px; padding: 3px 10px; }
    form { display: flex; gap: 8px; margin-top: 20px; }
    input[type=email] { flex: 1; padding: 8px; border: 1px solid #ccc; border-radius: 3px; font-size: 15px; }
    .add { background: #b51c20; color: #fff; border: none; border-radius: 3px; padding: 8px 16px; }
    .msg { margin-top: 14px; font-size: 14px; min-height: 18px; }
    .msg.err { color: #b51c20; }
    .muted { color: #888; font-size: 13px; }
  </style>
</head>
<body>
  <h1>Editor Logins</h1>
  <p class="muted">People who can log in to the editors site. Changes take effect immediately.</p>
  <div id="list">Loading…</div>
  <form id="addForm">
    <input type="email" id="email" placeholder="name@example.com" required>
    <button class="add" type="submit">Add</button>
  </form>
  <div id="msg" class="msg"></div>

  <script>
    const listEl = document.getElementById('list');
    const msgEl = document.getElementById('msg');
    const form = document.getElementById('addForm');
    const input = document.getElementById('email');

    function setMsg(text, isErr) { msgEl.textContent = text || ''; msgEl.className = 'msg' + (isErr ? ' err' : ''); }

    async function api(method, email) {
      const opts = { method, headers: { 'Content-Type': 'application/json' } };
      if (email) opts.body = JSON.stringify({ email });
      const res = await fetch('/api/access-users', opts);
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || ('HTTP ' + res.status));
      return data.emails;
    }

    function render(emails) {
      if (!emails.length) { listEl.innerHTML = '<p class="muted">No one yet.</p>'; return; }
      listEl.innerHTML = '';
      emails.forEach((e) => {
        const row = document.createElement('div');
        row.className = 'row';
        const span = document.createElement('span');
        span.className = 'email'; span.textContent = e;
        const btn = document.createElement('button');
        btn.className = 'remove'; btn.textContent = 'Remove';
        btn.onclick = () => remove(e);
        row.append(span, btn);
        listEl.append(row);
      });
    }

    async function load() {
      try { render(await api('GET')); setMsg(''); }
      catch (err) { listEl.innerHTML = ''; setMsg('Could not load: ' + err.message, true); }
    }

    async function remove(email) {
      if (!confirm('Remove ' + email + '?')) return;
      try { render(await api('DELETE', email)); setMsg('Removed ' + email); }
      catch (err) { setMsg(err.message, true); }
    }

    form.onsubmit = async (ev) => {
      ev.preventDefault();
      try { render(await api('POST', input.value)); setMsg('Added ' + input.value.trim().toLowerCase()); input.value = ''; }
      catch (err) { setMsg(err.message, true); }
    };

    load();
  </script>
</body>
</html>
```

- [ ] **Step 2: Commit**

```bash
git add admin.html
git commit -m "feat: admin.html page to view/add/remove editor logins"
```

---

## Task 7: Provision Cloudflare + Vercel (manual / Chrome-driven)

This task creates the real infrastructure the code depends on. It is interactive: John creates the API token; Claude can drive the Cloudflare/Vercel UIs in Chrome for everything else. No automated test — verification is the deploy in Task 8.

**Files:** none (dashboard configuration + Vercel env vars).

- [ ] **Step 1: John creates a Cloudflare API token**

In Cloudflare dashboard → My Profile → API Tokens → Create Token → Custom token:
- Permissions: **Account → Access: Apps and Policies → Edit**
- Account resources: **Include → John Bartlett's account** (`865fb6f8947e64cf5971cc3095f8eaf8`)
- Create, copy the token value. **John keeps the value; Claude does not handle it.**

- [ ] **Step 2: Discover the dashboard app id + Editors policy id**

Using the token, from a shell John runs (or Claude via the API with values John pastes into env, not the plan):

```bash
curl -s -H "Authorization: Bearer $CF_API_TOKEN" \
  "https://api.cloudflare.com/client/v4/accounts/865fb6f8947e64cf5971cc3095f8eaf8/access/apps" \
  | python3 -c "import sys,json; [print(a['id'], a.get('name'), a.get('domain')) for a in json.load(sys.stdin)['result']]"
```
Find the app whose domain is `editors.2ccmag.com` (the dashboard app) → that is `CF_ACCESS_APP_ID`. Then list its policies:

```bash
curl -s -H "Authorization: Bearer $CF_API_TOKEN" \
  "https://api.cloudflare.com/client/v4/accounts/865fb6f8947e64cf5971cc3095f8eaf8/access/apps/<APP_ID>/policies" \
  | python3 -c "import sys,json; [print(p['id'], p.get('name')) for p in json.load(sys.stdin)['result']]"
```
The policy named **Editors** → `CF_ACCESS_POLICY_ID`.

- [ ] **Step 3: Create the John-only admin Access application (Chrome)**

Cloudflare Zero Trust → Access → Applications → Add → Self-hosted:
- Destinations (public hostnames), two entries on the same app:
  - `editors.2ccmag.com` path `/admin`
  - `editors.2ccmag.com` path `/api/access-users`
- Policy: Allow, Include → Emails → `john.bartlett@gmail.com`.
- Create. Open the app → copy its **Application Audience (AUD) tag** → that is `CF_ADMIN_AUD`.

Because Access matches the most specific path, `/admin` and `/api/access-users` now require John while the rest of the site stays on the "Editors" policy.

- [ ] **Step 4: Add Vercel env vars (Chrome or CLI) to `ccm-editors` (Production)**

- `CF_API_TOKEN` = (John's token)
- `CF_ACCOUNT_ID` = `865fb6f8947e64cf5971cc3095f8eaf8`
- `CF_ACCESS_APP_ID` = (dashboard app id from Step 2)
- `CF_ACCESS_POLICY_ID` = (Editors policy id from Step 2)
- `CF_ACCESS_TEAM_DOMAIN` = `john-bartlett.cloudflareaccess.com`
- `CF_ADMIN_AUD` = (admin app AUD from Step 3)
- `ADMIN_EMAIL` = `john.bartlett@gmail.com`

- [ ] **Step 5: Record the non-secret values** (not the token) in a scratch note for Task 8 verification.

---

## Task 8: Deploy to `editors` and verify end-to-end

**Files:** none new — pushes Tasks 1–6 to the `editors` branch and confirms behavior on production.

- [ ] **Step 1: Push the branch**

```bash
cd /tmp/editors-admin
git status   # confirm only intended files staged/committed
git pull --rebase origin editors
git push origin editors
```
This triggers a `ccm-editors` production deploy (editors branch).

- [ ] **Step 2: Confirm the static dashboard still serves** (regression: package.json added)

Run: `curl -s -o /dev/null -w "%{http_code}\n" https://editors.2ccmag.com/dashboard`
Expected: `302` (redirect to Cloudflare Access login) — i.e., still gated and serving.

- [ ] **Step 3: Confirm `/admin` requires John**

Run: `curl -sI https://editors.2ccmag.com/admin | grep -i location`
Expected: a `302` to `https://john-bartlett.cloudflareaccess.com/cdn-cgi/access/login/...` (the admin Access app).

- [ ] **Step 4: Confirm the API rejects unauthenticated direct calls**

Run: `curl -s -o /dev/null -w "%{http_code}\n" https://editors.2ccmag.com/api/access-users`
Expected: `302` (Access login) — the API path is gated at the edge.

- [ ] **Step 5: Manual browser check as John**

In Chrome (logged in as John via Access): open `https://editors.2ccmag.com/admin`.
Expected: the page loads and lists the current 4 emails.

- [ ] **Step 6: Add + verify a throwaway login**

On `/admin`, add a test address you control (e.g. a `+test` Gmail alias). Expected: it appears in the list. Open an incognito window → `editors.2ccmag.com` → enter the test address → confirm the emailed code arrives and logs in. Then remove it from `/admin` and confirm it can no longer log in.

- [ ] **Step 7: Confirm the "cannot remove John" guard**

On `/admin`, attempt to remove `john.bartlett@gmail.com`. Expected: an error message, John stays in the list.

- [ ] **Step 8: Clean up the worktree**

```bash
cd /Users/john/article
git worktree remove /tmp/editors-admin
```

- [ ] **Step 9: Final commit / note** — record completion in `EMAIL_LOG.md`/session notes as appropriate (dev2), and update the design spec status to "Implemented".

---

## Self-Review Notes

- **Spec coverage:** admin page (Task 6), serverless function editing CF policy (Tasks 3+5), second John-only Access app on `/admin`+`/api` (Task 7 Step 3), CF API token as env var / John-created (Task 7 Steps 1,4), function verifies Access identity is John (Task 4), lockout guard (Tasks 2+5), survives 6h refresh (independent files, Task 1/8 Step 2), `/admin` rewrite (Task 1), email-only (Task 2), testing unit+manual (Tasks 2–5 unit, Task 8 manual). All covered.
- **Placeholders:** none — all code shown. `<APP_ID>`/token values in Task 7 are genuinely runtime-discovered/secret, not plan gaps.
- **Type consistency:** `getPolicyEmails(config, fetchFn)`, `setPolicyEmails(config, emails, fetchFn)`, `getAuthorizedEmail(headers, authConfig, verifyFn)`, `verifyAccessJwt(token, {teamDomain, aud})`, `addEmail/removeEmail` signatures match across Tasks 2–5 and the handler.
