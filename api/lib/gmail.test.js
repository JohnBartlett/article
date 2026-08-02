import { test } from 'node:test';
import assert from 'node:assert/strict';
import { sendEmail } from './gmail.js';

function fakeFetchCapturing(capture) {
  return async (url, opts) => {
    capture.url = url;
    capture.opts = opts;
    return { ok: true, json: async () => ({ id: 'fake-id' }) };
  };
}

function decodeRawMessage(body) {
  const { raw } = JSON.parse(body);
  return Buffer.from(raw, 'base64url').toString('utf-8');
}

test('sendEmail base64url-encodes the raw MIME message', async () => {
  const capture = {};
  await sendEmail('token', {
    to: 'judycbross@aol.com', cc: 'john.bartlett@gmail.com',
    subject: 'Plain ASCII subject', body: 'hello',
  }, fakeFetchCapturing(capture));
  const raw = decodeRawMessage(capture.opts.body);
  assert.match(raw, /^To: judycbross@aol\.com\r\n/);
  assert.match(raw, /Subject: Plain ASCII subject\r\n/);
});

test('non-ASCII subject (e.g. an em dash) round-trips correctly via RFC 2047 encoded-word', async () => {
  const capture = {};
  const subject = 'Classic Chicago Magazine — August 2, 2026 Edition Is Live';
  await sendEmail('token', {
    to: 'judycbross@aol.com', subject, body: 'body text',
  }, fakeFetchCapturing(capture));
  const raw = decodeRawMessage(capture.opts.body);
  const subjectLine = raw.split('\r\n').find((l) => l.startsWith('Subject: '));
  const match = subjectLine.match(/^Subject: =\?UTF-8\?B\?(.+)\?=$/);
  assert.ok(match, `expected an RFC 2047 encoded-word subject line, got: ${subjectLine}`);
  const decoded = Buffer.from(match[1], 'base64').toString('utf-8');
  assert.equal(decoded, subject);
});

test('CRLF in subject cannot inject extra headers', async () => {
  const capture = {};
  await sendEmail('token', {
    to: 'judycbross@aol.com',
    subject: 'Innocuous\r\nBcc: attacker@example.com',
    body: 'hello',
  }, fakeFetchCapturing(capture));
  const raw = decodeRawMessage(capture.opts.body);
  // The CRLF must be collapsed into the Subject text (safe), not survive as
  // an actual separate header line — check no line literally starts with "Bcc:".
  const headerLines = raw.split('\r\n\r\n')[0].split('\r\n');
  assert.ok(!headerLines.some((l) => l.startsWith('Bcc:')));
});

test('throws with response body text when Gmail API returns an error', async () => {
  await assert.rejects(
    () => sendEmail('token', { to: 'a@b.com', subject: 's', body: 'b' },
      async () => ({ ok: false, status: 500, text: async () => 'boom' })),
    /gmail send failed: 500 boom/,
  );
});
