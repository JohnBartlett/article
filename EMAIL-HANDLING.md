# Email Content Extraction & Handling

**Never claim "content received" unless you have actually extracted and verified it.**

## Article Content Sources

Judy sends article content via:
1. **Docx attachments** (most common) - requires extraction
2. **Email body text** - can be directly used
3. **Forwarded content** - may be wrapped in other messages

## Extraction Workflow

### When Article Comes as .docx Attachment

```python
# Use: tools/email_attachments.py
python3 tools/email_attachments.py --msg-id <ID> --output /tmp/article.txt
```

What this does:
- Downloads docx from Gmail
- Extracts text from document.xml
- Cleans up formatting
- Saves plain text output
- Reports success/failure

**CRITICAL:** If extraction fails, mark article as "Content received but extraction pending" (not "Ready").

### When Article Comes in Email Body

1. Find the email in Gmail by subject/date
2. Manually copy the text (gmail_api.py won't be needed)
3. Create the HTML article from copied text
4. Mark status as "Text received, converting to HTML"

### When Content is Forwarded/Quoted

- Extract only the ACTUAL article text, not quotes
- Remove email headers ("On [date] so-and-so wrote:")
- Look for boundaries: "---", "Begin forwarded message", etc.

## Process for Each Article Type

### Document with Photos

```markdown
1. Search Gmail: from:contributor "article name" has:attachment
2. Download docx via tools/email_attachments.py
3. Extract text
4. Search same sender for photo emails
5. Download photos to article folder
6. Build HTML article
7. Mark status as "Ready" (when both text AND photos exist)
```

### Story Only (No Photos Yet)

```markdown
1. Extract story text from email/docx
2. Build HTML article with placeholder photo divs
3. Mark status as "Text Only - Photos Pending"
4. When photos arrive:
   - Download to article folder
   - Update article HTML to reference real photos
   - Mark status as "Ready"
```

### Photos Only (Text Coming Later)

```markdown
1. Download photos to article folder
2. Create placeholder article with photo divs
3. Mark status as "Photos Ready - Text Pending"
4. When text arrives:
   - Extract and build article
   - Reference existing photos
   - Mark status as "Ready"
```

## Logging Rules

**Always log what actually happened:**

✓ GOOD: "Brit Marling article text extracted from Judy's April 21 email; photos not found"
✗ BAD: "Brit Marling ready" (hides what's missing)

✓ GOOD: "Biba's Favorites docx downloaded but Python extraction failed; manual extraction needed"
✗ BAD: "Biba content received" (hides extraction failure)

## Editors Page Status

Use these exact status indicators in `editors/edition.html`:

```html
<!-- Story received (docx) April 24, photos from Emma pending -->
<!-- Story + cover photo received April 22, pending full story extraction -->
<!-- Photos received (Tree.jpeg), story text pending -->
```

## Integration with /check-emails Skill

When `/check-emails` processes contributor emails:

1. Note what was received (docx? email body? photos?)
2. Run extraction tools
3. Log SUCCESS or FAILURE with reason
4. Update article status based on ACTUAL extraction
5. Do NOT assume success without verification

## Common Issues & Workarounds

### Docx Extraction Fails
- Reason: Old Word format, corrupted file, or zipfile issue
- Workaround: Manually copy text from email or ask writer to resend as text

### Photo Files Named Unclearly
- Log the actual filename received
- In article HTML, use the actual filename (don't rename)
- Note in editors page: "Photos: IMG_12345.jpeg, IMG_12346.jpeg"

### Email Content Is Partial
- Mark as "Text partial - writer cut off mid-sentence"
- Follow up with contributor
- Don't claim "ready" when text is obviously incomplete

### No Communication From Writer
- Check for emails using different addresses or subject variations
- After 3 days: escalate to Judy
- Mark as "Awaiting from [name] - no communication since [date]"
