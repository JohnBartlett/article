# /autopilot-off

Put **Autopilot** to sleep: the three unattended processes that otherwise keep working on the
magazine while nobody is at the keyboard. Use this before a hands-on layout/build session, so an
automated pass can't build the same article you're working on (see memory
`feedback_concurrent_sessions_collision`), or any time John says to leave them dormant.

## What Autopilot is

| # | Process | Where it runs | Schedule (UTC) | Writes to |
|---|---|---|---|---|
| 1 | **Hourly email check + edition build** — cloud routine `trig_01CX83XEEFUbex1Meb2CxgES` | Claude cloud session with the Gmail connector | `39 * * * *` | `dev2` (article builds, `EMAIL_LOG.md`, `STATUS.md`) |
| 2 | **Fetch Email Attachments** — `.github/workflows/fetch-email-attachments.yml` | GitHub Actions | `15 * * * *` | `dev2` (`_attachment-staging/`) |
| 3 | **Refresh Editors Dashboard** — `.github/workflows/refresh-editors-dashboard.yml` | GitHub Actions | `37 * * * *` (GitHub actually runs it every 2–7 h) | `editors` branch only |

Nothing else is part of Autopilot. The FormSubmit Activation Watcher and the Paul Bartlett email
checker were retired on Sept 24, 2026; "Ad-hoc GA4 Query" runs only when triggered by hand.

## Step 1 — Show the current state

```bash
gh workflow list --all | grep -E "Fetch Email Attachments|Refresh Editors Dashboard"
```

Routine state: `RemoteTrigger` `action: "get"`, `trigger_id: "trig_01CX83XEEFUbex1Meb2CxgES"` —
report `enabled`, `last_fired_at`, and `last_run.status`.

## Step 2 — Make sure nothing is mid-run

- Routine: `RemoteTrigger` `action: "list_runs"` for the same trigger. A run started within the last
  ~10 minutes may still be pushing to dev2 — wait for it (runs take ~3–5 min) before turning off.
- Workflows: `gh run list --limit 5` — if one shows `in_progress`, wait for it to finish.

## Step 3 — Turn it off

- Routine: `RemoteTrigger` `action: "update"`, `trigger_id: "trig_01CX83XEEFUbex1Meb2CxgES"`,
  `body: {"enabled": false}`.
- Workflows:
  ```bash
  gh workflow disable "Fetch Email Attachments"
  gh workflow disable "Refresh Editors Dashboard"
  ```

## Step 4 — Verify and report

Repeat Step 1. All three must read disabled (`enabled: false`, `disabled_manually`). Report a short
table of before → after, plus:
- while Autopilot is off, contributor attachments are **not** staged automatically — stage them
  locally with `tools/gmail_api.py` (`list_attachments`/`download_attachment` into
  `_attachment-staging/<msg-id>/`) and append the message ID to `_attachment-staging/.staged_log.json`
  so the fetcher won't re-download them later;
- the editors dashboard stays frozen at its last build.

Update memory `reference_check_emails_automation.md` with the date Autopilot went off.

## Notes

- Never delete the routine or the workflow files to "turn off" Autopilot — disabling is reversible,
  deletion is not (routines can only be deleted at https://claude.ai/code/routines).
- Do not turn Autopilot back on as a side effect of other work. Only `/autopilot-on`, when John asks.
