# /check-emails

Check all editorial emails and FormSubmit votes, apply any changes, and commit to dev2.

## Sources to check
- Judy Carmack Bross (judycbross@aol.com) — editorial instructions, article text, bio updates, photo requests, corrections
- Annie Delfosse (aedelfosse1@gmail.com) — DateBook updates, article content (e.g. Cheryl Anderson articles)
- Ana Baca (anabaca8@gmail.com) — photos and article content for BandWith / Philip Vidal's About the Town
- Emma Muhleman (emuhl2@uic.edu) — article content and photos (intern)
- FormSubmit (submissions@formsubmit.co) — reader comments and Quick Votes

## Step 1 — Fetch emails

Use `tools/gmail_api.py` for all Gmail access:

```python
import sys; sys.path.insert(0, 'tools')
from gmail_api import get_access_token, search_messages, get_metadata, get_body, list_attachments, download_attachment

token = get_access_token()
messages = search_messages(token,
    "from:(judycbross@aol.com OR aedelfosse1@gmail.com OR anabaca8@gmail.com OR emuhl2@uic.edu OR submissions@formsubmit.co) newer_than:2d")
```

Fetch metadata first (From, Subject, Date, Snippet), then fetch full body for messages that look actionable.

## Step 2 — Process each email type

### Judy — article text
- Build article HTML in the correct edition folder using the standard template (GA4-disabled, keyboard nav, feedback widget)
- Download attached photos to the article folder: `download_attachment(token, msg_id, att_id, dest_path)`
- Name photos `<slug>-cover.jpg`, `<slug>-1.jpg`, etc.

### Judy — writer bios
- "at the end of their piece" → add bio block just above the feedback widget in the article HTML
- "for Writers This Week" → also add to `about.html` Our Writers This Week section
- Bio block format: `<div style="margin-top:32px; padding-top:20px; border-top:1px solid #eee; font-family:'Lato',sans-serif; font-size:14px; color:#555; line-height:1.6;"><strong>Name</strong> — bio text</div>`

### Judy — text corrections
- Find the relevant passage in the article HTML and apply the fix exactly as Judy specifies

### Annie / Ana / Emma — article content
- Build article HTML with photos interleaved as indicated in the email body
- Download all photo attachments to the article folder

### FormSubmit — Quick Vote
- Skip if `Environment: dev2` (test)
- Note votes in the editors/edition.html reader engagement section

### FormSubmit — Reader Comment (non-empty `comment` field)
- Add to `reader-comments.html`
- If editorial concern, also add to `comments.html`

### FormSubmit — "Action Required: Activate FormSubmit"
- Ignore entirely

## Step 3 — Update editors pages

After applying content changes:
- `editors/edition.html` — mark newly completed articles Ready, update pending notes
- `editors/index.html` — update progress count and waiting-on list

## Step 4 — Commit and push

```bash
git add <changed files>
git commit -m "descriptive message"
git push origin dev2
```

## Key conventions
- Always work on dev2 — never commit to dev or master
- GA4 disabled in all new article HTML
- Relative paths from articles: `../../../` root assets, `../<sibling>/` siblings
- BandWith: capital W
- Email replies: `Dear Judy,` / `Cheers, John` / first person (I/me not we/us)
- To send email: `from gmail_api import send_email` then `send_email(token, to, subject, body, cc)`
