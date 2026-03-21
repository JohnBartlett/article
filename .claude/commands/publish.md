# /publish

Push the staged dev edition to production (master → Cloudflare). Run this after Judy has approved the Vercel preview, either manually or on a scheduled basis.

## Step 1 — Switch to master and merge dev

```
git checkout master
git merge -X theirs dev
```

The GA4 state always differs between dev (disabled) and master (enabled), so use `-X theirs` to take dev's content for all conflicts — GA4 will be re-enabled in the next step.

## Step 2 — Re-enable GA4 on master

GA4 was disabled on dev to prevent skewing stats. It must be re-enabled on master before pushing to production. Run this Python script:

```python
import os, re

GA4_DISABLED_PATTERN = re.compile(
    r'\n?\s*<!-- GA4-disabled(\s*<!-- Google tag \(gtag\.js\) -->.*?</script>)\n?\s*-->',
    re.DOTALL
)
RESTORE = lambda m: m.group(1)

root = '/home/john/article'
changed = []
for dirpath, _, files in os.walk(root):
    for fname in files:
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(dirpath, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        if '<!-- GA4-disabled' not in content:
            continue
        new_content = GA4_DISABLED_PATTERN.sub(RESTORE, content)
        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            changed.append(fpath)

print(f"Re-enabled GA4 in {len(changed)} files")
```

Verify the count matches the number of HTML files in the repo.

## Step 3 — Commit and push to master

```
git add -u
git commit -m "Publish <edition date> edition to production

Re-enables GA4 for production deployment.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"

git push origin master
```

Cloudflare will detect the push and deploy automatically to `chicagoclassicmag.com`.

## Step 4 — Send publication notification emails

Send an email to both Judy and John confirming the edition is live. Use the Gmail MCP tool (`mcp__gmail__send_email`) to send to each recipient.

**To:** `judycbross@aol.com` and `john.bartlett@gmail.com`
**From:** `editor@classicchicagomagazine.com`
**Subject:** `Classic Chicago Magazine — <Edition Date> Edition Is Live`

**Body:**
```
Dear Judy,

The March 22 edition of Classic Chicago Magazine is now live at:

https://chicagoclassicmag.com

Cheers, John
```

Adjust the edition date and greeting appropriately. John's email uses the same body but opens with "Hi John," instead of "Dear Judy,".

## Step 5 — Switch back to dev2

```
git checkout dev2
```

## Step 6 — Confirm deployment

Return the production URL to the user:

**https://chicagoclassicmag.com**

Note that Cloudflare may take 1–2 minutes to propagate after the push.

## Notes

- Never push to master without GA4 re-enabled — production must always have analytics active
- Never push to master without Judy having reviewed and approved the Vercel preview first
- If the merge is not a fast-forward (unexpected), investigate before proceeding — do not force-merge
- After publishing, dev and master will have diverged slightly (GA4 state). This is expected and handled automatically on the next `/stage` run
