# /send-update

Draft and send a weekly update email to Judy summarizing recent site activity and reader engagement stats.

## Step 1 — Gather activity

Review the current session's work and recent git log for changes made since the last update:
```
git log --oneline -10
```

## Step 2 — Pull reader stats

Read `reader-comments.html` to get the current vote tallies for the most recent edition (Yes/No counts, per-article breakdown).

## Step 3 — Draft the email

Write the email in this format:

**To:** judycbross@aol.com
**Subject:** Classic Chicago — Site Update

**Body structure:**
1. Brief summary of what was worked on (bios added, articles published, corrections made, etc.)
2. Reader engagement stats — total votes, Yes/No breakdown, per-article tally
3. Dev2 preview URL: `https://article-git-dev2-johns-projects-e5fce345.vercel.app`
4. Any items still pending (articles not yet received, photos needed, etc.)

**Email style:**
- Salutation: `Dear Judy,`
- Sign-off: `Cheers, John`
- First person — use "I/me", not "we/us"
- Keep it warm but concise

## Step 4 — Confirm before sending

Show the draft to the user and ask: **"Send this?"**

If yes, use the Gmail tool to send to `judycbross@aol.com` from the current account.

## Notes

- Dev2 URL: `https://article-git-dev2-johns-projects-e5fce345.vercel.app`
- Judy's email: `judycbross@aol.com`
- Only send after user confirms
