# Editors Login Admin — Design

**Date:** 2026-07-19
**Status:** Approved (design), pending implementation plan
**Author:** John Bartlett (with Claude)

## Summary

A John-only `/admin` page on `editors.2ccmag.com` for viewing and managing who
can log in to the internal editors dashboard. It adds/removes emails on the
**Cloudflare Access "Editors" policy** (the allowlist that already gates the
dashboard) via the Cloudflare API. The existing email + one-time-code login
(Cloudflare Access) is unchanged; this feature only manages *who is on the
allowlist*.

## Context

- The editors dashboard is served by the Vercel project **`ccm-editors`**
  (production branch = `editors`) at `https://editors.2ccmag.com`, with routes
  `/dashboard`, `/comments`, `/future` defined in the editors branch
  `vercel.json`.
- The `editors` branch is static HTML, regenerated every 6 hours by
  `.github/workflows/refresh-editors-dashboard.yml` (which runs
  `tools/build_editors_dashboard.py` and commits **`editors/dashboard.html`**
  only).
- Access is gated by **Cloudflare Access** (Zero Trust) on the `2ccmag.com`
  zone: a self-hosted application on `editors.2ccmag.com` with policy
  **"Editors"** whose Include rule is an **Emails** list. Login is one-time PIN
  (enter allowed email → emailed code → 24h session).
- Current allowlist (4): `john.bartlett@gmail.com`, `judycbross@aol.com`,
  `emuhl2@uic.edu`, `muhlemane2@gmail.com`.

## Goals

- John (only) can view the current login allowlist and add/remove emails from a
  web page, without opening the Cloudflare dashboard.
- Changes take effect immediately for the existing email+code login.
- No change to the login experience for editors.

## Non-goals (YAGNI)

- No homegrown authentication (Cloudflare Access keeps handling codes, sessions,
  security).
- No per-user metadata beyond the email (no names, roles, notes). Email is all
  Cloudflare Access needs. Can be added later if wanted.
- No audit log / history UI (Cloudflare's own audit log already records policy
  edits).
- No management of the admin allowlist itself from the page (only John; changing
  who is "John" is a rare manual Cloudflare edit).

## Architecture

Four components:

1. **`admin.html`** — static page on the `editors` branch. Lists current allowed
   emails, an "Add email" form (single email input + submit), and a "Remove"
   button per row. Talks only to the API function below (same origin). No
   secrets in the browser.

2. **`api/access-users.js`** — Vercel serverless function on `ccm-editors`
   (Vercel serves `api/*` as functions regardless of the "Other" framework
   preset). Endpoints:
   - `GET /api/access-users` → `{ emails: [...] }` (current allowlist)
   - `POST /api/access-users` `{ email }` → adds (dedupe, basic email validation)
   - `DELETE /api/access-users` `{ email }` → removes (refuses to remove John)
   It reads/writes the Cloudflare "Editors" policy via the Cloudflare API.

3. **Second Cloudflare Access application** scoped to the `/admin` page **and**
   the `/api/access-users` path on `editors.2ccmag.com`, with a **John-only**
   policy (Include → Emails → `john.bartlett@gmail.com`). Access evaluates the
   most specific path match, so `/admin` + `/api/access-users` require John while
   the rest of the site stays on the "Editors" policy.

4. **Cloudflare API token** — scoped to *Account → Access: Apps and Policies →
   Edit* for the account. Created by John, stored as Vercel env vars on
   `ccm-editors`: `CF_API_TOKEN`, `CF_ACCOUNT_ID`, `CF_ACCESS_APP_ID`,
   `CF_ACCESS_POLICY_ID` (IDs discoverable via the API/dashboard during setup).

## Data flow — add a user

1. John opens `https://editors.2ccmag.com/admin`.
2. Cloudflare Access (John-only policy on `/admin`) authenticates him.
3. Page `GET`s `/api/access-users`; function returns the current emails; page
   renders them.
4. John enters an email, clicks Add → `POST /api/access-users`.
5. Function verifies the request passed Cloudflare Access **as John**
   (validates the `Cf-Access-Jwt-Assertion` / `Cf-Access-Authenticated-User-Email`
   and checks it equals `john.bartlett@gmail.com`).
6. Function `GET`s the "Editors" policy, appends the email to the Include→Emails
   list (dedupe), `PUT`s it back.
7. Returns the updated list; page refreshes. The new person can immediately log
   in with the email+code flow.

Remove is the same with the email filtered out; John's own email cannot be
removed.

## Security

- **Edge:** `/admin` and `/api/access-users` are behind the John-only Cloudflare
  Access policy — non-John identities are blocked before reaching Vercel.
- **Defense in depth:** the function independently verifies the Cloudflare Access
  identity (JWT/header) is `john.bartlett@gmail.com`, so the endpoint cannot be
  driven without passing Access as John (protects against any misconfiguration
  or direct-origin hit).
- **Secret handling:** the CF API token lives only in Vercel server-side env
  vars, never sent to the browser; scoped to Access policy edits only.
- **Lockout guard:** the function refuses to remove `john.bartlett@gmail.com`.
- **Input:** basic email-format validation; dedupe; no-ops are safe.

## Operations / deployment

- New files (`admin.html`, `api/access-users.js`, updated `vercel.json`) are
  committed to the **`editors`** branch. The 6-hour refresh workflow only
  rewrites `dashboard.html`, so these persist untouched. (If desired later, the
  workflow can be updated to leave them alone explicitly, but no change is
  required.)
- `vercel.json` gains a rewrite: `/admin` → `/admin.html`.
- Env vars added to the `ccm-editors` Vercel project (Production).
- Manual one-time setup by John: create the CF API token; create the second
  Cloudflare Access app (John-only) on `/admin` + `/api/access-users`. (Claude
  can drive the Cloudflare/Vercel UI in Chrome for the app + env-var steps; John
  supplies the token value himself.)

## Testing

- **Unit (function, mock CF API):** GET returns emails; POST adds and dedupes and
  validates format; DELETE removes; DELETE refuses to remove John; requests
  without a valid John Access identity are rejected (401/403).
- **Manual:** open `/admin` as John → works; as another editor → denied; add a
  throwaway email → confirm it can complete the email+code login; remove it →
  confirm it can no longer log in.

## Open items / dependencies

- **John must create the Cloudflare API token** (Access: Apps and Policies →
  Edit) and add it to Vercel env vars. Claude will not create or handle the raw
  token value.
- Confirm the account-level CF API supports editing the specific policy's Include
  list via `PUT` of the policy (expected; verify during implementation).
