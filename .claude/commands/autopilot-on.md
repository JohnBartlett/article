# /autopilot-on

Wake **Autopilot** — the three unattended processes described in `/autopilot-off` (hourly email
check + edition build routine, Fetch Email Attachments, Refresh Editors Dashboard). Run only when
John asks.

## Step 1 — Show the current state

```bash
gh workflow list --all | grep -E "Fetch Email Attachments|Refresh Editors Dashboard"
```

Routine: `RemoteTrigger` `action: "get"`, `trigger_id: "trig_01CX83XEEFUbex1Meb2CxgES"` — report
`enabled`, `last_fired_at`, and whether its prompt matches the one in Step 3.

## Step 2 — Make dev2 safe to hand over

- Commit and push any local work on dev2 first (`git status` clean, `git pull --rebase`, push), so
  the routine's first run starts from the same state you finished in.
- If a hands-on build is still in progress (a `STATUS.md` article marked In Progress by this
  session), tell John — the routine may pick it up and build it in parallel.
- Record the last `EMAIL_LOG.md` item number and date; the routine's first run uses that date as its
  search cutoff.

## Step 3 — Refresh the routine's prompt

The routine's prompt is a snapshot; CLAUDE.md keeps moving. Before enabling, `RemoteTrigger`
`action: "update"` with the current prompt below (keep `mcp_connections` as they are — Gmail
connector `b460c5c8-3598-45cb-91ca-b62953936f8b`). Show John any wording change from the stored prompt.

```text
Run the Classic Chicago Magazine /check-emails workflow for the JohnBartlett/article repo. Work on the dev2 branch only.

Steps:
1. cd into the article repo checkout and `git checkout dev2 && git pull --rebase origin dev2`.
2. Read `CLAUDE.md` first (it carries the project rules, including the numbered mistakes list through the latest entry), then `.claude/commands/check-emails.md`, and follow it exactly.
3. Determine the search cutoff from the last entry date in `EMAIL_LOG.md` (never a fixed newer_than window), then check the Tier 1 senders and the Tier 2 keyword search described in the skill. Use the Gmail MCP tools (search_threads, get_thread, get_message with FULL_CONTENT to see attachments and the HTML body) — you only have this connector in this cloud sandbox, not the local gmail_api.py script.
4. For any email with photo/PDF/docx attachments you need to place: check `_attachment-staging/<message-id>/` first (the hourly Fetch Email Attachments workflow stages them there with original filenames). If the folder is there, copy the files into the correct `editions/YYYY-MM-DD/<slug>/` folder (never rename) and delete the consumed `_attachment-staging/<message-id>/` folder in the same commit. If it's not there yet, note the pending extraction in STATUS.md.
5. When building article text, work from the email's HTML body (italics/bold/links), use the contributor's own title, verify photo identity by image comparison when numbering is uncertain, and fix EXIF orientation (CLAUDE.md #61, #62, #67, #68). No template placeholders may remain (#65).
6. Apply only unambiguous changes (article content, photo captions/placement per explicit source instructions, bios, corrections), commit them to dev2 with a descriptive message, `git pull --rebase origin dev2`, then push. Never push to dev or master.
7. Immediately before appending to `EMAIL_LOG.md`, pull again and number from the current last item (parallel sessions append too). Include message IDs. Also update the active edition's `editions/YYYY-MM-DD/STATUS.md` if one exists.

Hard constraints:
- NEVER send an email. Drafts only, and only if the skill calls for one; John approves every send and sends link-bearing mail himself via gmail_api.py (CLAUDE.md #15).
- NEVER rename a contributor's image file or invent a new naming scheme.
- Do not build any article that is blocked on an unanswered editorial or sensitivity question; note it in EMAIL_LOG.md and stop there.
- Do not guess at ambiguous instructions (captions, placement, spelling); log the ambiguity instead of acting on it.
- If nothing new has arrived since the last EMAIL_LOG.md entry, make no commits and end quietly.

Finish with a short summary: what arrived, what you applied, and what needs John's decision.
```

## Step 4 — Turn it on

- Routine: `RemoteTrigger` `action: "update"`, `body: {"enabled": true}`.
- Workflows:
  ```bash
  gh workflow enable "Fetch Email Attachments"
  gh workflow enable "Refresh Editors Dashboard"
  ```

## Step 5 — Prove each one actually runs

Enabling a schedule isn't proof it works; run each once now.

```bash
gh workflow run "Fetch Email Attachments" --ref actions
gh workflow run "Refresh Editors Dashboard" --ref actions
```
Poll `gh run list --limit 4` until both finish; both must conclude `success`. Then:
- fetcher: `git pull` dev2 — either a "Stage new email attachments" commit or a clean
  "No new attachments" log line (`gh run view <id> --log | tail`);
- dashboard: cache-busted `curl` of the editors dashboard shows today's build time.

Routine: `RemoteTrigger` `action: "run"` once, then `list_runs` → `get_run_log` on that run; it must
finish without errors and either make no commit ("nothing new") or a sensible check-emails commit.

## Step 6 — Report

Table of before → after for all three, the result of each test run, and the next scheduled times
(routine `next_run_at`; workflows at :15 and :37 UTC). Update memory
`reference_check_emails_automation.md` with the date Autopilot came back on.
