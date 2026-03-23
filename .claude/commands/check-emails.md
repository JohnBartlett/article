# /check-emails

Check recent emails from Judy and FormSubmit for actionable site updates, apply any changes, then commit and push to dev2.

## Step 1 — Search for emails (run in parallel)

Use `mcp__google-workspace__search_gmail_messages` with these two queries simultaneously:

- `from:judycbross@aol.com newer_than:7d` (max 10)
- `from:submissions@formsubmit.co newer_than:14d` (max 20)

## Step 2 — Read Judy's emails

Use `mcp__google-workspace__get_gmail_messages_content_batch` to read all messages returned from the Judy search. Look for:
- Bio updates or corrections (bios live in `about.html`)
- Photo requests (cover photo, hero image, carousel additions)
- Text corrections to any article
- New article content or attachments
- Questions to answer or decisions pending
- Any other editorial instructions

If a message has attachments or is part of a thread with more context, use `mcp__google-workspace__get_gmail_thread_content` to read the full thread.

## Step 3 — Read FormSubmit emails

Use `mcp__google-workspace__get_gmail_messages_content_batch` to read all messages returned from the FormSubmit search.

Two types arrive at `editor@2ccmag.com`:

**"Classic Chicago Reader Comment"** — check the `comment` field:
- If empty: no action needed (reader opened the form but didn't submit)
- If has text: add the comment to `reader-comments.html`

**"Classic Chicago Quick Vote"** — check the `vote` field and `Page`:
- Votes are "Yes" confirmations that readers liked the article
- Log them to `reader-comments.html` if keeping a tally, otherwise just note them
- `Environment: dev2` submissions are test submissions — ignore

## Step 4 — Apply changes

Common updates and where they live:

| What | File |
|---|---|
| Judy or Megan bio update | `about.html` — Our Team section |
| Writer bio update | `about.html` — Our Writers This Week section |
| Annie Delfosse bio | `about.html` — id="annie-delfosse" |
| Reader comments | `reader-comments.html` |
| Article text correction | `editions/YYYY-MM-DD/<slug>/index.html` |
| Hero/cover photo swap | article `index.html` + homepage card |

## Step 5 — Commit and push

After all changes are applied:
```
git add <files>
git commit -m "descriptive message"
git push origin dev2
```

If there are no actionable changes, report a summary of what was found (votes, empty submissions, etc.) and skip the commit.

## Notes

- Always work on `dev2` — never commit directly to `dev` or `master`
- Judy's email address: `judycbross@aol.com`
- FormSubmit sends to: `editor@2ccmag.com`
- Empty FormSubmit comments are common — readers click the form open then close it
- Judy often sends photo emails with short subject lines — read them even if vague

## Email style (when drafting emails to Judy)

- Salutation: `Dear Judy,`
- Sign-off: `Cheers, John`
- Write in first person — use "I/me", not "we/us"
