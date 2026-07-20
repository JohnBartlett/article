export function validateEmail(email) {
  if (typeof email !== 'string') return false;
  // simple, deliberately conservative address check
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim());
}

export function normalizeEmail(email) {
  return String(email).trim().toLowerCase();
}

function validationError(message) {
  const e = new Error(message);
  e.status = 400;
  return e;
}

export function addEmail(emails, email) {
  if (!validateEmail(email)) throw validationError('invalid email');
  const norm = normalizeEmail(email);
  if (emails.some((e) => normalizeEmail(e) === norm)) return emails.slice();
  return [...emails, norm];
}

export function removeEmail(emails, email, protectedEmail) {
  const norm = normalizeEmail(email);
  if (norm === normalizeEmail(protectedEmail)) {
    throw validationError('cannot remove the protected admin email');
  }
  return emails.filter((e) => normalizeEmail(e) !== norm);
}
