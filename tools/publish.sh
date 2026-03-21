#!/usr/bin/env bash
# tools/publish.sh — Cherry-pick commits from dev2 to master, enabling GA4
#
# Usage:
#   tools/publish.sh <commit> [commit ...]
#
# Example:
#   tools/publish.sh abc1234 def5678
#
# What it does:
#   1. Cherry-picks the given commit(s) onto master
#   2. Strips the "<!-- GA4 disabled on dev2 ... -->" wrapper from all HTML files
#      (the comment is the signal — it tells us the file came from dev2)
#   3. Strips any "<!-- dev2-only ... -->" blocks from all HTML files
#   4. Commits the GA4/cleanup changes and pushes to master
#   5. Returns you to your original branch
#
# To mark dev2-only content in any HTML file, wrap it like this:
#   <!-- dev2-only
#   <div>...staging-only content...</div>
#   -->

set -e

REPO_ROOT="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
ORIGINAL_BRANCH="$(git -C "$REPO_ROOT" branch --show-current)"

if [ "$#" -eq 0 ]; then
  echo "Usage: tools/publish.sh <commit> [commit ...]"
  echo "Example: tools/publish.sh abc1234 def5678"
  exit 1
fi

echo "→ Switching to master..."
git -C "$REPO_ROOT" checkout master

echo "→ Cherry-picking $# commit(s)..."
git -C "$REPO_ROOT" cherry-pick "$@"

echo "→ Applying production transforms (GA4, dev2-only blocks)..."
python3 - "$REPO_ROOT" <<'PYEOF'
import re, glob, sys, os

repo = sys.argv[1]
files = glob.glob(os.path.join(repo, '**/*.html'), recursive=True)

# Pattern 1: <!-- GA4 disabled on dev2\n  <script...>\n  </script>\n  -->
# Strips the comment wrapper, leaving the GA4 scripts enabled.
ga4_pattern = re.compile(
    r'  <!-- GA4 disabled on dev2\n'
    r'  (<script async src="https://www\.googletagmanager\.com/gtag/js\?id=G-5J2HWKC0B1"></script>\n'
    r'  <script>\n'
    r'    window\.dataLayer = window\.dataLayer \|\| \[\];\n'
    r'    function gtag\(\)\{dataLayer\.push\(arguments\);\}\n'
    r'    gtag\(\'js\', new Date\(\)\);\n'
    r'    gtag\(\'config\', \'G-5J2HWKC0B1\'\);\n'
    r'  </script>)\n'
    r'  -->'
)

# Pattern 2: <!-- dev2-only\n...\n-->
# Strips entire block (including the comment markers and content).
dev2_only_pattern = re.compile(
    r'\n?[ \t]*<!-- dev2-only\n.*?-->[ \t]*\n?',
    re.DOTALL
)

changed = []
for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()

    original = content

    if '<!-- GA4 disabled on dev2' in content:
        content = ga4_pattern.sub(r'  \1', content)

    if '<!-- dev2-only' in content:
        content = dev2_only_pattern.sub('\n', content)

    if content != original:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(content)
        rel = f.replace(repo + '/', '')
        changed.append(rel)
        print(f'  transformed: {rel}')

print(f'  {len(changed)} file(s) updated')
PYEOF

echo "→ Committing production transforms..."
git -C "$REPO_ROOT" add -A
if git -C "$REPO_ROOT" diff --cached --quiet; then
  echo "  (no transform changes to commit)"
else
  git -C "$REPO_ROOT" commit -m "Enable GA4 and strip dev2-only blocks for production"
fi

echo "→ Pushing to master..."
git -C "$REPO_ROOT" push origin master

echo "→ Returning to $ORIGINAL_BRANCH..."
git -C "$REPO_ROOT" checkout "$ORIGINAL_BRANCH"

echo "Done. Production updated."
