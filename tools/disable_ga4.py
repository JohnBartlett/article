#!/usr/bin/env python3
"""Wrap GA4 script blocks in <!-- GA4-disabled ... --> comments.

Matches the two-script GA4 block (async loader + config) whether or not
it has a preceding <!-- Google tag --> comment, and wraps it uniformly.
"""

import os, re

# Matches the async gtag loader + inline config script, regardless of indentation
PATTERN = re.compile(
    r'([ \t]*<script async src="https://www\.googletagmanager\.com/gtag/js\?id=[^"]*"[^>]*></script>\s*<script>.*?</script>)',
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
        if 'googletagmanager.com/gtag' not in content:
            continue
        if '<!-- GA4' in content:  # already disabled
            continue
        new_content = PATTERN.sub(lambda m: f'  <!-- GA4-disabled\n{m.group(1)}\n  -->', content)
        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            changed.append(fpath)

print(f"Disabled GA4 in {len(changed)} files")
