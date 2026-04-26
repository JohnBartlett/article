# Article Photo Download Methods

## Status: April 26, 2026 Edition

### What Works

#### 1. **Google Drive Downloads** ✓
Direct curl download from shared Google Drive links (no authentication needed):

```bash
FILE_ID="1KpKKswF39lgyEIPjGYajcWTya7PtKib4"
curl -s -L "https://drive.google.com/uc?export=download&id=$FILE_ID" -o photo.jpg
```

**Source**: Photo credit URLs from email content
**Status**: Successfully tested - 878KB file downloaded

#### 2. **Public Website Images** ~ (Partial)
Some websites allow direct image downloads:

```bash
curl -L "https://chicagology.com/wp-content/themes/revolution-20/PreFire3/..." -o photo.jpg
```

**Status**: Some URLs available, others blocked by Cloudflare/robots.txt

#### 3. **Email Attachments** ✗
Gmail API attachment extraction requires valid authentication:
- Token-based approach: Requires non-expired OAuth token
- Raw message format: Requires authorization scope `https://www.googleapis.com/auth/gmail.readonly`

**Status**: Blocked due to expired token

### Article Photos Status

#### Rush Hospital (15 photos total)
- **Downloaded**: 2 photos from Google Drive links
- **Pending**: 13 photos (likely in email attachments or external sources)
- **Action needed**: Manual download from email or provide Drive link list

#### Second Presbyterian (8 photos total)
- **Downloaded**: 0 photos
- **Pending**: 8 photos (in email attachments only)
- **Action needed**: Manual download from email attachments

#### Trains Chicago (6 photos total)
- **Downloaded**: 1 photo from chicagology.com
- **Pending**: 5 photos (external sources: WBEZ, trains.com, Chicago History Museum, etc.)
- **Action needed**: Source public URLs or provide local files

### Recommended Process for Future Editions

1. **When editor sends articles via email:**
   - Extract any Google Drive file IDs from email body: `drive.google.com/file/d/[ID]/`
   - Use curl download method above for each ID
   - Save to `editions/YYYY-MM-DD/[article-slug]/`

2. **For email attachments:**
   - Export Gmail conversation to .eml format
   - Use `munpack` or `uudeview` to extract attachments:
     ```bash
     munpack -C download-folder message.eml
     ```
   - Or manually download via Gmail web interface

3. **For external sources:**
   - Try downloading with curl/wget
   - If blocked, manually download and upload
   - Document source URL for attribution

### Tools and Commands

```bash
# Check if file downloaded successfully
file photo.jpg

# Batch download multiple Drive files
while IFS= read -r id; do
  curl -s -L "https://drive.google.com/uc?export=download&id=$id" -o "photo-${COUNTER}.jpg"
  ((COUNTER++))
done < file-ids.txt
```

### Future Improvements

1. Set up Google Drive API credentials for authenticated downloads
2. Configure Gmail API with proper scopes for attachment extraction
3. Create Python script to automate email parsing and attachment extraction
4. Build Perplexity/web search integration for missing external images

---
*Last updated: April 24, 2026*
