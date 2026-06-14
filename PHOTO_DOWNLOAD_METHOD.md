# Photo Download Methods

## Primary Method: Gmail API (always use this first)

```bash
source .venv/bin/activate
python3 tools/extract_article_photos.py YYYY-MM-DD --contributor ana
```

Downloads all photo attachments from the contributor's most recent email for that edition date. Preserves original filenames exactly as sent.

For manual extraction of a specific message:

```python
import sys; sys.path.insert(0, 'tools')
from gmail_api import get_access_token, list_attachments, download_attachment

token = get_access_token()
attachments = list_attachments(token, 'MESSAGE_ID_HERE')
for att in attachments:
    download_attachment(token, 'MESSAGE_ID_HERE', att['id'],
        f'editions/YYYY-MM-DD/slug/{att["filename"]}')
```

**Never rename the downloaded files.** `att["filename"]` is the original filename — use it as-is.

## Secondary Method: Windows Downloads Folder

If photos were forwarded to john.bartlett@gmail.com and saved locally:

```bash
cp "/mnt/c/Users/johnb/Downloads/photo-folder/"*.jpeg editions/YYYY-MM-DD/slug/
```

Keep original filenames. Do not rename.

## Google Drive (use with caution)

Only works for publicly shared files (not shortcuts):

```bash
FILE_ID="1KpKKswF39lgyEIPjGYajcWTya7PtKib4"
curl -s -L "https://drive.google.com/uc?export=download&id=$FILE_ID" -o original-filename.jpg
```

**Important:** Drive shortcuts download as HTML, not images. If a file downloads as HTML, ask the contributor to send via email attachment instead. If Drive has renamed files generically (e.g. `image1.jpg`), ask contributor for originals with proper names.

## Rules That Apply Regardless of Source

1. **Never rename files** — original filename is the permanent link between photo and caption
2. **Build a photo map first** — `filename → caption → placement` before writing any `<figure>` HTML
3. **COVER files stay off the article body** — files with "COVER" in the name are homepage card images only
4. **Verify after downloading** — run `python3 tools/verify_edition.py YYYY-MM-DD` to confirm photo counts
