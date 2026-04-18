#!/usr/bin/env python3
"""Wrap all GA4 script blocks in <!-- GA4-disabled ... --> comments."""

import os, re

GA4_PATTERN = re.compile(
    r'(\s*<!-- Google tag \(gtag\.js\) -->.*?</script>)',
    re.DOTALL
)
DISABLED_WRAP = lambda m: f'\n  <!-- GA4-disabled{m.group(1)}\n  -->'

changed = []
for dirpath, _, files in os.walk('.'):
    for fname in files:
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(dirpath, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        if '<!-- Google tag (gtag.js) -->' not in content or '<!-- GA4-disabled' in content:
            continue
        new_content = GA4_PATTERN.sub(DISABLED_WRAP, content)
        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            changed.append(fpath)

print(f"Disabled GA4 in {len(changed)} files")
