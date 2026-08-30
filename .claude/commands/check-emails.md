# /check-emails

Check all editorial emails and FormSubmit votes, apply any changes, and commit to dev2.
Run at the start of every session and any time Judy may have sent instructions.
This skill runs independently of the edition cycle — it feeds into whichever phase is active.

## Email Sources

### Tier 1 — CCM staff and coordinators (checked by address)
- Judy Carmack Bross (`judycbross@aol.com`, also occasionally `judycbross@icloud.com`) — editorial instructions, article text, bio updates, article replacements, holds
- Annie Delfosse (`aedelfosse1@gmail.com`) — DateBook updates, article content (also relays Katherine Harvey's articles)
- Ana Baca (`anabaca8@gmail.com`) — photos and article content for Philip Vidal's About the Town
- Emma Muhleman (`emuhl2@uic.edu`, `muhlemane2@gmail.com`) — article content and photos (intern, coordinator)
- Sig (`sigalina@aol.com`) — article submissions
- Victoria Martin (`viccimartin@gmail.com`) — monthly Astro Chart / Daily Star content (Word doc attachment). **Added 2026-08-29** after her Sept chart (sent Aug 26) was missed by a full check-emails pass and only surfaced when John asked directly — she wasn't in this list before.
- Adrian Naves (`niceguyfatz@gmail.com`) — layout and writing (not currently in tier1 search)

**Not in tier1 search:**
- Marcy Carmack (`marcycarmack@icloud.com`) — writer/contributor; caught by tier2 keyword search
- FormSubmit (`submissions@formsubmit.co`) — reader votes/comments; checked only during `/send-update` stats run, not here

### Tier 2 — Unknown writers (keyword search)
- Search recent emails mentioning "Classic Chicago" or "article" from senders not in Tier 1
- **Never filter by `is:unread`** — John often opens emails in Gmail before the session, so read state means nothing. Filter by date (`after:` the last EMAIL_LOG.md entry) and dedupe against message IDs already in the log instead.
- Catches writers emailing directly: Bob Glaze, Katherine Harvey, Susan Aurinko, David Sweet, Lee Hamilton, Sophie Bross, Sydney Armstrong, Philip Vidal, Elizabeth Dunlop Richter, etc.
- Report any matches with sender + subject; apply changes only if content is unambiguous

## Step 1 — Determine the search cutoff date

**Before fetching any emails**, read `EMAIL_LOG.md` and find the date of the most recent entry. Use that date as the `after:` cutoff — do NOT use a fixed `newer_than:Nd` window, which re-fetches already-logged emails.

```python
# Read EMAIL_LOG.md, find last entry date, format as YYYY/MM/DD for Gmail
# Example: if last log entry is "Jun 28", cutoff = "2026/06/28"
after_date = "YYYY/MM/DD"  # replace with actual last-log date
```

Then fetch:

```python
import sys; sys.path.insert(0, 'tools')
from gmail_api import get_access_token, search_messages, get_metadata, get_body, get_html_body, parse_formsubmit, list_attachments, download_attachment

token = get_access_token()

# Tier 1 — known addresses, only after last processed date
tier1_messages = search_messages(token,
    f"from:(judycbross@aol.com OR judycbross@icloud.com OR aedelfosse1@gmail.com OR anabaca8@gmail.com OR emuhl2@uic.edu OR muhlemane2@gmail.com OR sigalina@aol.com OR viccimartin@gmail.com) after:{after_date}")

# Tier 2 — keyword search for writers (no is:unread — read state is meaningless,
# John may have opened emails in Gmail already; dedupe against EMAIL_LOG.md msg IDs)
tier2_messages = search_messages(token,
    f"(\"Classic Chicago\" OR article) after:{after_date} -from:(judycbross@aol.com OR judycbross@icloud.com OR aedelfosse1@gmail.com OR anabaca8@gmail.com OR emuhl2@uic.edu OR muhlemane2@gmail.com OR sigalina@aol.com OR viccimartin@gmail.com)")
```

Fetch metadata first (From, Subject, Date, Snippet), then full body for actionable messages.

## Step 2 — Process each email type

### Judy — new article list for upcoming edition
- This triggers `/prep-edition` — do not build stubs here, just report it
- Note the edition date, article titles, authors, and any holds

### Judy — article text
- If `/prep-edition` has already run: fill in the existing stub at `editions/YYYY-MM-DD/slug/index.html`
- If prep has not run yet: note the content and report — run `/prep-edition` first
- Download attached photos using the original filename — never rename:
  ```python
  for att in list_attachments(token, msg_id):
      download_attachment(token, msg_id, att['id'],
          f'editions/YYYY-MM-DD/slug/{att["filename"]}')
  ```
- **Never rename contributor image files.** The original filename is the permanent link between a photo and its caption/position. Renaming to `photo-01.jpeg` etc. severs that link.
- **Before placing any `<figure>` HTML**, build an explicit photo map: `filename → caption (verbatim from email) → placement (after which sentence/paragraph)`. If any field is unknown, stop and find it — never infer captions or placement.
- **COVER photos** (filename contains "COVER"): use as the homepage card image only. Do not place in the article body unless the contributor explicitly says to AND it has a caption.
- **Caption vs. placement label**: a label appearing before a photo in an email may be a caption or a placement instruction (e.g. "Photo 1", "Cover"). Verify from context before using as `<figcaption>`. When uncertain, ask.
- After placing all photos: count `<figure>` elements vs. photos on disk (excluding COVER-only files); for 6+ photo articles, read through the HTML sequentially and confirm each figure is at its specified anchor.

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

### FormSubmit — votes and comments
Search for votes since the last update date noted in `editors/stats.html` (check the data-note line):

```
subject:"Classic Chicago" newer_than:7d
```

Tally Yes/No counts by article. Fetch body of "Classic Chicago Reader Comment" threads to check for non-empty `comment:` fields.

**Update `reader-comments.html`** (always):
- If the current edition section exists: add vote tally cards, bar chart, and Votes by Article list. Add comment cards for any non-empty comments.
- If the section doesn't exist yet: create it with the current edition header, tally, and vote log. Use the same edition-block pattern as the existing June 7 section.
- Add "Late Votes — Other Editions" sub-section for any votes that arrived for older articles.

**Update `editors/stats.html`** (always):
- Update the Reader Approval KPI (Yes count, No count, total, approval %). **Do this in the same edit as any row update — never update a row without also updating the KPI.**
- Update the data-note "Reader votes updated" date to today.
- Prepend new edition rows to the Reader Votes table (use the section-header row pattern from the June 7 block).
- Add any late-vote rows near the bottom of their original edition's entries.

After updating both files, commit and push to dev2.

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

After updating EMAIL_LOG.md, also update the relevant `editions/YYYY-MM-DD/STATUS.md` if it exists (only active/upcoming editions have one — do not create it for past editions):
- Mark article rows as ✅ if now complete
- Check off any action items that were completed this session
- Add new action items if the email revealed something outstanding

## Step 4 — Update the edition's STATUS.md

`editors/edition.html` and `editors/index.html` no longer exist (removed Jun 22, 2026) — do
not recreate them on dev2. Progress now lives in `editions/YYYY-MM-DD/STATUS.md` (only
active/upcoming editions have one) and is read live by `editors/dashboard.html` on the
`editors` branch — nothing else needs updating to keep that dashboard current.

After applying all changes:
- Update article rows to reflect newly completed content (text/photos)
- Note any holds, replacements, or outstanding decisions in STATUS.md's Notes section

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
