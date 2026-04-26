# Deployment Verification Checklist

**Never claim deployment is complete without this checklist.**

## After `vercel deploy --yes`

### Step 1: Capture Preview URL
```bash
PREVIEW_URL=$(vercel deploy --yes 2>&1 | grep "^Preview:" | head -1 | awk '{print $2}')
echo "Preview URL: $PREVIEW_URL"
```

### Step 2: Verify Actual State Locally First
```bash
python3 tools/verify_edition.py <edition-date>
```

Document what the script says before comparing to deployed version.

### Step 3: Verify Each Article on Live Preview

For each article marked as "Ready" or "Text Only" in verification:

**Homepage:**
- [ ] Article card appears in the grid
- [ ] Article title and byline are correct
- [ ] Teaser text displays

**Article Page:**
- [ ] Page loads (no 404 errors)
- [ ] Article title displays correctly
- [ ] Article content is visible (not placeholder text)
- [ ] Photos load (if they should exist)
- [ ] Navigation links work (Previous/Next buttons)

**Keyboard Navigation:**
- [ ] Press 'N' to go to next article
- [ ] Press 'P' to go to previous article
- [ ] Full nav chain works (can cycle through articles)

### Step 4: Update Editors Pages
```bash
sed -i "s|href=\"https://article-[^/]*/editions/[^\"]*\"|href=\"${PREVIEW_URL}/editions/2026-XX-XX/article-slug/\"|" editors/edition.html
sed -i "s|href=\"https://article-[^/]*/index\.html\"|href=\"${PREVIEW_URL}/index.html\"|" editors/index.html
```

### Step 5: Commit Changes
```bash
git add editors/index.html editors/edition.html
git commit -m "Update Vercel preview URL to latest deployment"
git push origin dev2
```

### Step 6: Record Deployment

Update editors/edition.html with deployment timestamp and verification result:
```html
<!-- Deployed 2026-04-24 14:23 -->
<!-- Verified: 2 ready, 1 text-only, 6 placeholders -->
```

## What NOT to Do

✗ Don't claim "articles deployed" without checking Vercel actually shows them  
✗ Don't update editors pages without verifying the URL works  
✗ Don't trust local file state; verify remote matches  
✗ Don't skip the "every article" checks - spot check is insufficient  

## Template for Deployment Summary

After completing this checklist:

```markdown
✓ Deployment verified: https://article-XXXX.vercel.app
  - Homepage loads
  - 2 ready articles (Madeira, Unsung Gems) visible with photos
  - 1 text-only article (Brit Marling) visible
  - 6 placeholders visible
  - Navigation working (N/P keys functional)
  - Editors pages updated with new URL
```
