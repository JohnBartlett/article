# /send-update

Draft and send a weekly update email to Judy summarizing site activity and reader engagement.
Run after `/publish`, same session or next morning.

## Step 1 — Check if anything has changed

**Gmail access:** requires `~/.gmail-mcp/credentials.json`. If missing, use `mcp__claude_ai_Gmail__search_threads` as a fallback for searching, and `mcp__claude_ai_Gmail__create_draft` for sending (then ask user to send the draft).

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

If no new commits and no new votes since the last update: tell the user "Nothing has changed
since the last update — no email needed." and stop.

## Step 2 — Pull reader stats

Read `reader-comments.html` for current vote tallies (Yes/No counts, per-article breakdown).
Compare against the last update email to identify new votes since last report.

## Step 3 — Pull GA4 stats

```bash
export GA4_PROPERTY_ID="your-numeric-id"
export GOOGLE_APPLICATION_CREDENTIALS="path/to/key.json"
python3 tools/ga4_report.py
```

Identify top articles by page views for the past 7 days and the previous edition overall.

## Step 4 — Update editors pages

**`editors/edition.html`:**
- Update Reader Quick Votes section with final vote tallies per article (Yes/No counts)

**`editors/index.html`:**
- Add GA4 stats summary: top 3 articles by views, total users and sessions for the week

Commit and push to dev2.

## Step 5 — Draft the email

**To:** judycbross@aol.com
**Subject:** Classic Chicago — Site Update

Body structure:
1. New edition is live — link to `https://chicagoclassicmag.com`
2. Work done since last update — articles added, corrections made, bios updated, etc.
3. Reader engagement — total votes, Yes/No breakdown, per-article tally for current edition
4. GA4 highlights — top articles by views, total readers this week
5. Dev2 preview URL — read from `href` of `class="btn-stage"` in `editors/edition.html`
6. Pending items — articles not yet received, photos needed, anything awaiting Judy's input

Style: `Dear Judy,` / `Cheers, John` / first person / warm but concise.
Always include the dev2 preview URL — Judy uses it to review work in progress.

## Step 6 — Confirm before sending

Show the draft to the user. Ask **"Send this?"**

If yes:
```python
from gmail_api import send_email
send_email(token, 'judycbross@aol.com', 'Classic Chicago — Site Update', body_text,
           cc='john.bartlett@gmail.com')
```
