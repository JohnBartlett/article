# Article Status Verification

**Golden Rule:** Never claim article status without running the verification script.

## Quick Check

```bash
python3 tools/verify_edition.py 2026-04-26
```

This shows the ACTUAL state of every article:
- ✓ **Ready** = HTML file with article content + photos in folder
- ⚠ **Text Only** = HTML file with article content, but no photos
- ⚠ **In Progress** = Has some deliverables (photos or story, not both)
- ✗ **Placeholder** = HTML structure only, no real content
- ✗ **Missing** = Folder exists but no index.html

## Article Status Definitions (STRICT)

### READY
- Article folder exists
- `index.html` contains actual article text (no `[Article text coming soon]`)
- At least one photo file exists in the folder (`.jpg`, `.jpeg`, `.png`, `.gif`)
- Navigation links are correct

### TEXT ONLY
- Article folder exists
- `index.html` contains actual article text
- **NO photo files in the folder**
- Ready to be published but needs photos added

### IN PROGRESS
- Article folder exists
- Has SOME deliverables (either text OR photos, but not both)
- Waiting on the missing part

### PLACEHOLDER
- Article folder exists
- `index.html` contains `placeholder-notice` div
- Contains `[Article text coming soon]` or similar placeholder text
- No photos

### MISSING
- Article folder doesn't exist, OR
- Folder exists but no `index.html`

## Before Claiming Status

**Always do this:**
1. Run verification script
2. Check the output matches your claims
3. If discrepancies, investigate before updating docs
4. Use verification output in status summaries

## Commit Message Requirements

Include actual counts verified by the script:

✓ GOOD: `"Build articles: 2 ready, 1 text-only, 6 placeholders, 2 missing"`
✗ BAD: `"Build article placeholders"` (hides what's actually there)

## Integration Points

- `/update-editors` skill: Run before updating pages
- `/new-edition` skill: Run after building articles
- Git commits: Include verification output
- Editor pages: Report VERIFIED counts only
