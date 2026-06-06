#!/usr/bin/env python3
"""Comment out <!-- dev2-only --> internal-nav blocks in all HTML files for dev/master."""

import os, re

# Matches: <!-- dev2-only -->\n<div class="internal-nav">...</div>\n
# and wraps it in <!-- dev2-only ... -->
PATTERN = re.compile(
    r'(  <!-- dev2-only -->)\s*\n(\s*<div class="internal-nav">.*?</div>)\s*\n',
    re.DOTALL
)

def replace(m):
    return f'  <!-- dev2-only\n{m.group(2)}\n  -->\n'

changed = []
for dirpath, _, files in os.walk('.'):
    for fname in files:
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(dirpath, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        if '<!-- dev2-only -->' not in content:
            continue
        new_content = PATTERN.sub(replace, content)
        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            changed.append(fpath)

print(f"Commented out internal-nav in {len(changed)} files")
