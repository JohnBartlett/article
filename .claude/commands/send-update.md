# /send-update

Draft and send a weekly update email to Judy summarizing recent site activity and reader engagement stats. If nothing has changed since the last update, say so and skip the email.

## Step 1 — Check if anything has changed

```python
import sys; sys.path.insert(0, 'tools')
from gmail_api import get_access_token, search_messages

token = get_access_token()
messages = search_messages(token,
    'from:john.bartlett@gmail.com to:judycbross@aol.com subject:"Site Update"',
    max_results=1)
```

Get the date of the last update, then check git:
```bash
git log --oneline --after="YYYY-MM-DD"
```

**If no new commits and no new votes or emails since the last update:** tell the user "Nothing has changed since the last update — no email needed." and stop.

## Step 2 — Gather activity

Summarize commits since the last update — bios added, articles published, corrections made, photos added, etc.

## Step 3 — Pull reader stats

Read `reader-comments.html` for current vote tallies (Yes/No counts, per-article breakdown). Compare against the last update email to identify new votes.

## Step 4 — Draft the email

**To:** judycbross@aol.com  
**Subject:** Classic Chicago — Site Update

Body:
1. Brief summary of work done since last update
2. Reader engagement stats — total votes, Yes/No breakdown, per-article tally
3. Dev2 preview URL — read from the `href` of `class="btn-stage"` in `editors/edition.html`
4. Pending items (articles not yet received, photos needed, etc.)

Style: `Dear Judy,` / `Cheers, John` / first person / warm but concise

## Step 5 — Confirm before sending

Show the draft. Ask **"Send this?"**

If yes:
```python
from gmail_api import send_email
send_email(token, 'judycbross@aol.com', 'Classic Chicago — Site Update', body_text)
```
