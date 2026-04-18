#!/usr/bin/env python3
"""Remove <!-- GA4-disabled ... --> wrappers to re-enable GA4 for production."""

import os, re

GA4_DISABLED_PATTERN = re.compile(
    r'[ \t]*<!-- GA4-disabled\s*(.*?)\s*-->',
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
        if '<!-- GA4-disabled' not in content:
            continue
        new_content = GA4_DISABLED_PATTERN.sub(lambda m: m.group(1), content)
        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            changed.append(fpath)

print(f"Re-enabled GA4 in {len(changed)} files")
