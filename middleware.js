// Password gate for the internal editors site (dashboard, comments, future articles, admin).
// The password lives in the DASHBOARD_PASSWORD environment variable on the ccm-editors Vercel project,
// never in this repo. A correct entry sets an HttpOnly cookie holding a hash of the password, valid 30 days;
// changing the password in Vercel logs everyone out. /api/* is excluded: those endpoints have their own auth.
import { next } from '@vercel/functions';

export const config = { matcher: ['/((?!api/|favicon.ico).*)'] };

const COOKIE = 'ccm_editors';
const MAX_AGE = 60 * 60 * 24 * 30;

async function token(password) {
  const data = new TextEncoder().encode('ccm-editors:' + password);
  const digest = await crypto.subtle.digest('SHA-256', data);
  return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

function safeEqual(a, b) {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

function readCookie(request, name) {
  const header = request.headers.get('cookie') || '';
  for (const part of header.split(';')) {
    const [k, ...v] = part.trim().split('=');
    if (k === name) return v.join('=');
  }
  return '';
}

function safeNext(value) {
  return typeof value === 'string' && value.startsWith('/') && !value.startsWith('//') && !value.startsWith('/__')
    ? value : '/dashboard';
}

function escapeHtml(s) {
  return s.replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

function loginPage(nextPath, error, status = 401) {
  const html = `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>Editors Login</title>
<style>
  :root { --bg:#f7f3ee; --card:#fff; --ink:#222; --muted:#777; --red:#b51c20; --line:#e0d8cc; }
  @media (prefers-color-scheme: dark) { :root { --bg:#1b1a19; --card:#262422; --ink:#eee; --muted:#aaa; --line:#3a3633; } }
  body { margin:0; min-height:100vh; display:flex; align-items:center; justify-content:center; background:var(--bg);
         color:var(--ink); font-family: Georgia, 'Times New Roman', serif; padding:16px; box-sizing:border-box; }
  form { background:var(--card); border:1px solid var(--line); padding:32px 28px; width:100%; max-width:340px; }
  h1 { font-size:22px; margin:0 0 4px; }
  p { margin:0 0 20px; color:var(--muted); font-size:14px; }
  input { width:100%; box-sizing:border-box; font-size:16px; padding:10px 12px; border:1px solid var(--line);
          background:var(--bg); color:var(--ink); margin-bottom:12px; }
  button { width:100%; font-size:15px; padding:10px; background:var(--red); color:#fff; border:0; cursor:pointer; }
  .err { color:var(--red); font-size:14px; margin:0 0 12px; }
</style></head><body>
<form method="POST" action="/__login">
  <h1>Classic Chicago Editors</h1>
  <p>Enter the editors' password.</p>
  ${error ? '<div class="err">That password is not right. Please try again.</div>' : ''}
  <input type="password" name="password" autocomplete="current-password" autofocus required aria-label="Password">
  <input type="hidden" name="next" value="${escapeHtml(nextPath)}">
  <button type="submit">Log in</button>
</form></body></html>`;
  return new Response(html, {
    status,
    headers: { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store', 'x-robots-tag': 'noindex' },
  });
}

export default async function middleware(request) {
  const password = process.env.DASHBOARD_PASSWORD;
  if (!password) {
    return new Response('Editors site is locked: DASHBOARD_PASSWORD is not set.', { status: 503 });
  }
  const url = new URL(request.url);
  const expected = await token(password);

  if (url.pathname === '/__logout') {
    return new Response(null, {
      status: 303,
      headers: { location: '/dashboard', 'set-cookie': `${COOKIE}=; Path=/; Max-Age=0; HttpOnly; Secure; SameSite=Lax` },
    });
  }

  if (url.pathname === '/__login') {
    if (request.method !== 'POST') return loginPage('/dashboard', false);
    const form = await request.formData();
    const nextPath = safeNext(form.get('next'));
    const given = String(form.get('password') || '');
    if (!safeEqual(await token(given), expected)) return loginPage(nextPath, true);
    return new Response(null, {
      status: 303,
      headers: {
        location: nextPath,
        'set-cookie': `${COOKIE}=${expected}; Path=/; Max-Age=${MAX_AGE}; HttpOnly; Secure; SameSite=Lax`,
      },
    });
  }

  if (safeEqual(readCookie(request, COOKIE), expected)) {
    return next({ headers: { 'cache-control': 'private, no-store' } });
  }
  return loginPage(safeNext(url.pathname + url.search), false);
}
