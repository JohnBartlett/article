# Email Content Extraction & Handling

**Never claim "content received" unless you have actually extracted and verified it.**

## Article Content Sources

Contributors send article content via:
1. **Docx attachments** — extract text via `zipfile` + `word/document.xml` parsing (see `/new-edition`)
2. **PDF attachments** — extract via PyPDF2 (activate `.venv` first)
3. **Email body text** — use directly
4. **Forwarded/quoted content** — strip headers, extract only the actual article text

## Extraction Tools

```python
# Gmail API — primary tool for all email access
import sys; sys.path.insert(0, 'tools')
from gmail_api import get_access_token, search_messages, get_body, list_attachments, download_attachment

# Download photo attachments (preserves original filenames)
python3 tools/extract_article_photos.py YYYY-MM-DD --contributor ana
```

**Never use `munpack`, `uudeview`, or manual `.eml` extraction** — the Gmail API handles all attachment extraction directly with original filenames preserved.

## Word Doc Extraction

```python
import zipfile, re
with zipfile.ZipFile('/tmp/article.docx') as z:
    xml = z.read('word/document.xml').decode('utf-8')
text = re.sub(r'<[^>]+>', ' ', xml)
text = re.sub(r'\s+', ' ', text).strip()
```

**⚠ Word doc extraction is silently lossy.** After building the HTML, do a paragraph-by-paragraph diff against the original `.docx`. Entire paragraphs can disappear with no visible gap.

## PDF Extraction

```bash
source .venv/bin/activate
```
```python
import PyPDF2
reader = PyPDF2.PdfReader('/tmp/article.pdf')
text = '\n'.join(page.extract_text() for page in reader.pages)
```

## Photo Handling

**Never rename contributor image files.** Save with the original filename exactly as sent. See CLAUDE.md mistake #1.

Before placing any `<figure>` HTML, build an explicit photo map:
`filename → caption (verbatim from email) → placement (after which sentence/paragraph)`

## Article Status Definitions

- **Ready** = content + photos both exist
- **Text Only** = content exists, no photos
- **In Progress** = has one but not both
- **Placeholder** = no real content

Run `python3 tools/verify_edition.py YYYY-MM-DD` to confirm actual state before claiming any status.

## Logging Rules

**Always log what actually happened:**

✓ GOOD: "Brit Marling article text extracted from Judy's April 21 email; photos not found"  
✗ BAD: "Brit Marling ready" (hides what's missing)

## Common Issues

### Docx Extraction Fails
Reason: Old Word format, corrupted file, or zipfile issue.  
Workaround: Ask writer to resend as plain text or copy-paste from email.

### Google Drive Shortcuts
Drive shortcuts download as HTML, not the actual file. Ask contributor for the real file or email attachment instead.

### Email Content Is Partial
Mark as "Text partial — writer cut off mid-sentence." Follow up with contributor. Don't claim Ready when text is obviously incomplete.

### No Communication From Writer
Check for emails using different addresses or subject variations. After 3 days: escalate to Judy.
