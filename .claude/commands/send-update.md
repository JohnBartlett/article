# /send-update

Draft and send a weekly update email to Judy summarizing recent site activity and reader engagement stats. If nothing has changed since the last update, say so and skip the email.

## Step 1 — Check if anything has changed

Find the last update email sent to Judy:
- Search Gmail: `from:me to:judycbross@aol.com subject:"Site Update"` (max 1) to get the date of the last update

Then check git for commits since that date:
```
git log --oneline --after="YYYY-MM-DD"
```

Also run `/check-emails` logic to see if there are any unprocessed emails from Judy or new FormSubmit votes since the last update.

**If there are no new commits and no new votes or emails since the last update:** tell the user "Nothing has changed since the last update — no email needed." and stop.

## Step 2 — Gather activity

Summarize commits since the last update email — bios added, articles published, corrections made, photos added, etc.

## Step 3 — Pull reader stats

Read `reader-comments.html` to get the current vote tallies for the most recent edition (Yes/No counts, per-article breakdown).

Compare against what was reported in the last update email (if readable) to identify any new votes since then.

## Step 4 — Draft the email

Write the email in this format:

**To:** judycbross@aol.com
**Subject:** Classic Chicago — Site Update

**Body structure:**
1. Brief summary of what was worked on since the last update (bios added, articles published, corrections made, etc.)
2. Reader engagement stats — total votes, Yes/No breakdown, per-article tally
3. Dev2 preview URL: `https://article-git-dev2-johns-projects-e5fce345.vercel.app`
4. Any items still pending (articles not yet received, photos needed, etc.)

**Email style:**
- Salutation: `Dear Judy,`
- Sign-off: `Cheers, John`
- First person — use "I/me", not "we/us"
- Keep it warm but concise

## Step 5 — Confirm before sending

Show the draft to the user and ask: **"Send this?"**

If yes, use the Gmail tool to send to `judycbross@aol.com` from the current account.

## Notes

- Dev2 URL: `https://article-git-dev2-johns-projects-e5fce345.vercel.app`
- Judy's email: `judycbross@aol.com`
- Only send after user confirms
