#!/usr/bin/env python3
"""Remove GA4-disabled comment wrappers to re-enable GA4 for production.

Handles both comment forms used in the repo:
  <!-- GA4-disabled ... -->
  <!-- GA4 disabled on dev2 ... -->
"""

import os, re

# Matches either form: "GA4-disabled" or "GA4 disabled on dev2" (or any text after "disabled")
PATTERN = re.compile(
    r'[ \t]*<!-- GA4[ -]disabled[^\n]*\n(.*?)[ \t]*-->',
    re.DOTALL
)

changed = []
for dirpath, _, files in os.walk('.'):
    for fname in files:
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(dirpath, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        if '<!-- GA4' not in content:
            continue
        new_content = PATTERN.sub(lambda m: m.group(1), content)
        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            changed.append(fpath)

print(f"Re-enabled GA4 in {len(changed)} files")
