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
