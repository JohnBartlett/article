# /check-emails

Check all editorial emails and FormSubmit votes, apply any changes, and commit to dev2.

## Email Sources

### Tier 1 — Known contributors (checked by address)
- Judy Carmack Bross (judycbross@aol.com) — editorial instructions, article text, bio updates, article replacements
- Annie Delfosse (aedelfosse1@gmail.com) — DateBook updates, article content
- Ana Baca (anabaca8@gmail.com) — photos and article content for Philip Vidal's About the Town
- Emma Muhleman (emuhl2@uic.edu, muhlemane2@gmail.com) — article content and photos (intern)
- Marcy Carmack (marcycarmack@icloud.com) — Fashion Trends articles
- Sig (sigalina@aol.com) — article submissions
- Adrian Naves (niceguyfatz@gmail.com) — layout and writing
- FormSubmit (submissions@formsubmit.co) — reader comments and Quick Votes

### Tier 2 — Unknown writers (keyword search)
- Search recent unread emails mentioning "Classic Chicago" or "article" from senders not in Tier 1
- Catches writers emailing directly: Bob Glaze, Katherine Harvey, Susan Aurinko, David Sweet, Lee Hamilton, Sophie Bross, Sydney Armstrong, Philip Vidal, Elizabeth Dunlop Richter, etc.
- Report any matches with sender + subject; apply changes only if content is unambiguous

## Step 1 — Fetch emails

**Gmail access — two options:**
- **Python script** (requires `~/.gmail-mcp/credentials.json`): use `tools/gmail_api.py` as below
- **MCP fallback** (if credentials.json missing): use `mcp__claude_ai_Gmail__search_threads` and `mcp__claude_ai_Gmail__get_thread` directly — they work without credentials

Use `tools/gmail_api.py` for all Gmail access when credentials are present:

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

Fetch metadata first (From, Subject, Date, Snippet), then fetch full body for messages that look actionable.

## Step 2 — Process each email type

### Judy — article text
- Build article HTML in the correct edition folder using the standard template (GA4-disabled, keyboard nav, feedback widget)
- Download attached photos to the article folder: `download_attachment(token, msg_id, att_id, dest_path)`
- Name photos `<slug>-cover.jpg`, `<slug>-1.jpg`, etc.

### Judy — bio updates
- When Judy's email says "add this to [Author]'s About the Author", locate the author in `about.html` and append the quoted text
- Format: quoted block (using `<blockquote>` or italicized `<p>`) added after existing bio sentence
- Do NOT replace existing bio, only append

### Judy — article replacements
- When Judy's email says "replacing [old article] with [new article]":
  - Create the new article folder if it doesn't exist: `editions/YYYY-MM-DD/<new-slug>/`
  - Mark in `editors/edition.html`: old article as "Replaced", new article as "Pending"
  - Do NOT delete the old folder

### Judy — text corrections
- Find the relevant passage in the article HTML and apply the fix exactly as Judy specifies

### Annie / Ana / Emma / Marcy / Sig / Adrian — article content
- Build article HTML with photos interleaved as indicated in the email body
- Download all photo attachments to the article folder

### Tier 2 — Unknown writers (direct emails)
- Report sender + subject for review
- If sender claims to be a known contributor (e.g., "Hi, I'm David Sweet, here's my article"), apply cautiously
- If docx/PDF attachment with clear article content, build the HTML

### FormSubmit — Quick Vote
- Use `get_html_body(token, msg_id)` to fetch HTML form data (FormSubmit only sends HTML, not plain text)
- Use `parse_formsubmit(html)` to extract field: value pairs
- Skip if `Environment: dev2` (test vote)
- Tally votes by article: group multiple votes for same article with `(&times;N)` count
- Update `reader-comments.html`:
  - Find current-week edition block (header bar with red background `#b51c20`)
  - Update `.tally-card` counts: `.count` divs for Yes and No
  - Update `.bar-chart` percentages: recalculate widths as `round(yes/total*100)` and `round(no/total*100)`
  - Update `.bar-pct` text with percentages
  - Update `.tally-total` with new total count and date range
  - Append new articles to the "Votes by Article" `<ul>`: `<li><span class="vote-badge yes">Yes</span> Article Title (&times;N)</li>`
  - Omit "Not so much" bar row if no-votes = 0 (conditional rendering)

### FormSubmit — Reader Comment (non-empty `comment` field)
- Extract comment text from parsed form data
- Add to `reader-comments.html` inside current-week `.comments-section`:
  ```html
  <div class="comment-card">
    <p class="comment-text">&ldquo;Comment text here.&rdquo;</p>
    <div class="comment-meta">Date &nbsp;&bull;&nbsp; Article Title &nbsp;&bull;&nbsp; Commenter email (if provided)</div>
  </div>
  ```
- If comment raises an editorial concern (criticism, content question, feature request), also flag it in `comments.html` under "Reader Comments" section

### FormSubmit — "Action Required: Activate FormSubmit"
- Ignore entirely

## Step 3 — Update editors pages

After applying content changes:
- `editors/edition.html` — mark newly completed articles Ready, update pending notes
- `editors/index.html` — update progress count and waiting-on list based on Judy's latest article list email

## Step 4 — Commit and push

```bash
git add <changed files>
git commit -m "Log FormSubmit votes and reader comments; apply bio updates"
git push origin dev2
```

## Key conventions
- Always work on dev2 — never commit to dev or master
- GA4 disabled in all new article HTML
- Relative paths from articles: `../../../` root assets, `../<sibling>/` siblings
- BandWith: capital W
- Email replies: `Dear Judy,` / `Cheers, John` / first person (I/me not we/us)
- To send email: `from gmail_api import send_email` then `send_email(token, to, subject, body, cc)`
