#!/bin/bash
# Remove internal-only files from a deploy branch (dev or master) so Cloudflare/Vercel never serve them.
# Run from the repo root on `dev` during /stage, AFTER the tools/ scripts have run and BEFORE committing.
# Background: until 2026-09-26, /stage merged all of dev2 into dev and /publish merged dev into master,
# so EMAIL_LOG.md, CLAUDE.md, tools/, .claude/, _attachment-staging/ and STATUS.md files were publicly
# served at chicagoclassicmag.com (fixed in master a5242f40 / dev aa52fe84).
set -euo pipefail
paths=(
  .claude ".claude.backup.20260411_074723" .claude_last_session_id .DS_Store
  tools _template _attachment-staging _bios docs dashboard editors john-article-ideas
  deploy.log install-google-gcloud-mcp.sh install-google-workspace-mcp.sh
)
for p in "${paths[@]}"; do
  if git ls-files --error-unmatch "$p" >/dev/null 2>&1; then git rm -r -q -f "$p"; echo "removed $p"; fi
done
# writer retrospectives built by /writer-retrospective are dev2-only (John, Oct 1, 2026): their pages carry a
# ccm-retrospective marker. Older retrospectives (lucia-adams, francesco-bianchini) have no marker and stay.
while IFS= read -r d; do git rm -r -q -f "$d"; echo "removed $d"; done < <(
  { git grep -l 'name="ccm-retrospective" content="dev2-only"' -- 'writers/*/index.html' || true; } | cut -d/ -f1-2 | sort -u)
# root-level markdown docs and report dumps
while IFS= read -r f; do git rm -q -f "$f"; echo "removed $f"; done < <(git ls-files | grep -E '^[^/]+\.md$|^(ga4_report|ha_ad_report)_[^/]*\.json$')
# per-edition STATUS.md
while IFS= read -r f; do git rm -q -f "$f"; echo "removed $f"; done < <(git ls-files 'editions/*/STATUS.md')
