// Minimal Gmail-send helper for the publish-notify endpoint. Pure functions,
// no top-level env reads, so this stays unit-testable with a fake fetch.

export async function getAccessToken(config, fetchImpl = fetch) {
  const res = await fetchImpl('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      client_id: config.clientId,
      client_secret: config.clientSecret,
      refresh_token: config.refreshToken,
      grant_type: 'refresh_token',
    }),
  });
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`token refresh failed: ${res.status} ${text}`);
  }
  const data = await res.json();
  return data.access_token;
}

// Strip CR/LF so header values can't be used to inject extra headers
// (e.g. a caller-supplied editionDate containing "\r\nBcc: ...").
function sanitizeHeaderValue(value) {
  return String(value).replace(/[\r\n]+/g, ' ').trim();
}

// RFC 2047 encoded-word: a header FIELD VALUE (unlike the body) can't just
// contain raw UTF-8 bytes even though Content-Type declares UTF-8 for the
// body — that charset doesn't cover header fields. Without this, non-ASCII
// characters (e.g. the em dash in "Magazine — <date>") arrive mojibake'd.
function encodeHeaderValue(value) {
  const sanitized = sanitizeHeaderValue(value);
  if (/^[\x00-\x7F]*$/.test(sanitized)) return sanitized;
  return `=?UTF-8?B?${Buffer.from(sanitized, 'utf-8').toString('base64')}?=`;
}

function buildRawMessage({ to, cc, subject, body }) {
  const headers = [
    `To: ${sanitizeHeaderValue(to)}`,
    cc ? `Cc: ${sanitizeHeaderValue(cc)}` : null,
    `Subject: ${encodeHeaderValue(subject)}`,
    'Content-Type: text/plain; charset="UTF-8"',
  ].filter(Boolean).join('\r\n');
  const raw = `${headers}\r\n\r\n${body}`;
  return Buffer.from(raw, 'utf-8').toString('base64url');
}

export async function sendEmail(accessToken, message, fetchImpl = fetch) {
  const raw = buildRawMessage(message);
  const res = await fetchImpl('https://gmail.googleapis.com/gmail/v1/users/me/messages/send', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ raw }),
  });
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`gmail send failed: ${res.status} ${text}`);
  }
  return res.json();
}
