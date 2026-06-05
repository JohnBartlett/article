# /check-emails

Check all editorial emails and FormSubmit votes, apply any changes, and commit to dev2.
Run at the start of every session and any time Judy may have sent instructions.
This skill runs independently of the edition cycle — it feeds into whichever phase is active.

## Email Sources

### Tier 1 — Known contributors (checked by address)
- Judy Carmack Bross (`judycbross@aol.com`) — editorial instructions, article text, bio updates, article replacements, holds
- Annie Delfosse (`aedelfosse1@gmail.com`) — DateBook updates, article content (also relays Katherine Harvey's articles)
- Ana Baca (`anabaca8@gmail.com`) — photos and article content for Philip Vidal's About the Town
- Emma Muhleman (`emuhl2@uic.edu`, `muhlemane2@gmail.com`) — article content and photos (intern, coordinator)
- Marcy Carmack (`marcycarmack@icloud.com`) — Fashion Trends articles
- Sig (`sigalina@aol.com`) — article submissions
- Adrian Naves (`niceguyfatz@gmail.com`) — layout and writing
- FormSubmit (`submissions@formsubmit.co`) — reader comments and Quick Votes

### Tier 2 — Unknown writers (keyword search)
- Search recent unread emails mentioning "Classic Chicago" or "article" from senders not in Tier 1
- Catches writers emailing directly: Bob Glaze, Katherine Harvey, Susan Aurinko, David Sweet, Lee Hamilton, Sophie Bross, Sydney Armstrong, Philip Vidal, Elizabeth Dunlop Richter, etc.
- Report any matches with sender + subject; apply changes only if content is unambiguous

## Step 1 — Fetch emails

```python
import sys; sys.path.insert(0, 'tools')
from gmail_api import get_access_token, search_messages, get_metadata, get_body, get_html_body, parse_formsubmit, list_attachments, download_attachment

token = get_access_token()

# Tier 1 — known addresses
tier1_messages = search_messages(token,
    "from:(judycbross@aol.com OR aedelfosse1@gmail.com OR anabaca8@gmail.com OR emuhl2@uic.edu OR muhlemane2@gmail.com OR marcycarmack@icloud.com OR sigalina@aol.com OR niceguyfatz@gmail.com OR submissions@formsubmit.co) newer_than:2d")

# Tier 2 — keyword search for direct writers
tier2_messages = search_messages(token,
    "(\"Classic Chicago\" OR article) is:unread newer_than:2d -from:(judycbross@aol.com OR aedelfosse1@gmail.com OR anabaca8@gmail.com OR emuhl2@uic.edu OR muhlemane2@gmail.com OR marcycarmack@icloud.com OR sigalina@aol.com OR niceguyfatz@gmail.com OR submissions@formsubmit.co)")
```

Fetch metadata first (From, Subject, Date, Snippet), then full body for actionable messages.

## Step 2 — Process each email type

### Judy — new article list for upcoming edition
- This triggers `/prep-edition` — do not build stubs here, just report it
- Note the edition date, article titles, authors, and any holds

### Judy — article text
- If `/prep-edition` has already run: fill in the existing stub at `editions/YYYY-MM-DD/slug/index.html`
- If prep has not run yet: note the content and report — run `/prep-edition` first
- Download attached photos: `download_attachment(token, msg_id, att_id, dest_path)`
- Normalize photos to `photo-01.jpeg`, `photo-02.jpeg`, etc.

### Judy — bio updates
- Locate the author in `about.html` and append the quoted text after the existing bio sentence
- Format: `<p>` italicized or blockquoted, appended — do NOT replace existing bio

### Judy — article holds or replacements
- **Hold:** log in `future-articles.html` as Held; if folder exists, note it for removal in next `/new-edition` pass
- **Replace:** create new article folder if it doesn't exist; mark old article as "Replaced" in `editors/edition.html`; do NOT delete old folder

### Judy — text corrections
- Find the relevant passage in the article HTML and apply the fix exactly as specified

### Annie / Ana / Emma / Marcy / Sig / Adrian — article content or photos
- Apply to the existing stub for the correct article; download all photo attachments
- If photos arrive without article text: update badge in `editors/edition.html` to "Photos Only"

### Tier 2 — Unknown writers
- Report sender + subject for review
- Apply only if content is unambiguous and sender is a known contributor writing from an unexpected address

### FormSubmit — Quick Vote
- Use `get_html_body(token, msg_id)` then `parse_formsubmit(html)` to extract field:value pairs
- Skip if `Environment: dev2` (test vote)
- Tally votes by article; group multiple votes with `(×N)` count
- Update `reader-comments.html`:
  - Find the current-week edition block (red header bar)
  - Update `.tally-card` Yes/No counts and `.bar-chart` percentages (recalculate widths)
  - Update `.tally-total` with new total and date range
  - Append new articles to "Votes by Article" `<ul>`
  - Omit "Not so much" bar row if no-votes = 0

### FormSubmit — Reader Comment (non-empty `comment` field)
- Add to `reader-comments.html` inside current-week `.comments-section`:
  ```html
  <div class="comment-card">
    <p class="comment-text">&ldquo;Comment text here.&rdquo;</p>
    <div class="comment-meta">Date &nbsp;&bull;&nbsp; Article Title &nbsp;&bull;&nbsp; Email (if provided)</div>
  </div>
  ```
- If comment raises an editorial concern, also flag in `comments.html` under "Reader Comments"

### FormSubmit — "Action Required: Activate FormSubmit"
- Ignore entirely

## Step 3 — Update EMAIL_LOG.md

After processing each email, update `EMAIL_LOG.md` at the repo root:

- **New actionable email not yet in the log** → add a row under the correct edition section with status ⏳
- **Action fully applied this session** → update status to ✅ and add a note describing what was done
- **Action started but blocked** (waiting on another email, missing photos, needs Judy input) → status 🔁, note what's missing
- **Irrelevant / spam / activation email** → status ⬛, brief note

Row format:
```
| Jun 5 | Judy | Short subject summary | `msgid` | ✅ | What was done |
```

If no edition section exists yet for the emails being processed, create one (e.g. `## June 14 Edition`).

After updating EMAIL_LOG.md, also update the relevant `editions/YYYY-MM-DD/STATUS.md`:
- Mark article rows as ✅ if now complete
- Check off any action items that were completed this session
- Add new action items if the email revealed something outstanding

## Step 4 — Update editors pages


After applying all changes:

**`editors/edition.html`:**
- Update badge for any newly completed article
- Append new vote tallies to Reader Quick Votes section

**`editors/index.html`:**
- Update progress count and bar if articles moved to Ready
- Update Decisions Needed if Judy flagged holds, replacements, or outstanding items

## Step 5 — Commit and push

```bash
git add <changed files>
git commit -m "Check emails: [summary of what changed — votes logged, bio updated, etc.]"
git push origin dev2
```

## Key conventions
- Always work on dev2 — never commit to dev or master
- GA4 disabled in all new article HTML
- Relative paths from articles: `../../../` root assets, `../<sibling>/` siblings
- Email replies to Judy: `Dear Judy,` / `Cheers, John` / first person (I/me not we/us)
- To send email: `from gmail_api import send_email` then `send_email(token, to, subject, body, cc)`
