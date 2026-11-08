#!/usr/bin/env python3
"""Comment out <!-- dev2-only --> internal-nav blocks in all HTML files for dev/master."""

import os, re

# Matches: <!-- dev2-only -->\n<div class="internal-nav">...</div>\n
# and wraps it in <!-- dev2-only ... -->
# The div may carry inline attributes (style=...) and any indentation (Nov 7, 2026: the
# May 24 DateBook's styled nav was missed and reached dev).
PATTERN = re.compile(
    r'([ \t]*)<!-- dev2-only -->\s*\n(\s*<div class="internal-nav"[^>]*>.*?</div>)[ \t]*\n',
    re.DOTALL
)

def replace(m):
    return f'{m.group(1)}<!-- dev2-only\n{m.group(2)}\n{m.group(1)}-->\n'

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
