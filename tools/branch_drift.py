#!/usr/bin/env python3
"""Report reader-facing differences between dev2 and dev (CLAUDE.md mistake #85).

Ignores what is supposed to differ: internal files (never promoted), the GA4 block
(disabled/enabled wrappers) and the internal-nav comment wrapper. Anything left is a
fix that exists on one branch only: a hotfix made on dev that dev2 lacks, or a dev2
fix that git will not carry to dev because it considers the file merged.

usage: python3 tools/branch_drift.py [--a origin/dev2] [--b origin/dev] [--no-fetch]
Exit status 1 when drift is found.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys

INTERNAL = re.compile(
    r'^(CLAUDE\.md|tools/|\.claude/|EMAIL_LOG\.md|.*STATUS\.md|_template/|demos/|editors/|'
    r'_attachment-staging/|john-article-ideas/|.*\.DS_Store$|requirements\.txt$|\.vercelignore$|\.github/)')
# lines allowed to differ: GA4 wrappers/body and internal-nav comment markers
EXPECTED = re.compile(
    r'^\s*(<!--\s*dev2-only.*|-->|<!--\s*GA4[- ]disabled.*|</script>\s*-->|'
    r'<!-- Google tag \(gtag\.js\) -->|<script async src="https://www\.googletagmanager\.com/gtag/js\?id=G-5J2HWKC0B1"></script>|'
    r'<script>|</script>|window\.dataLayer = window\.dataLayer \|\| \[\];|function gtag\(\)\{dataLayer\.push\(arguments\);\}|'
    r"gtag\('js', new Date\(\)\);|gtag\('config', 'G-5J2HWKC0B1'\);|)\s*$")


def git(*args: str) -> str:
    return subprocess.run(['git', *args], capture_output=True, text=True, errors='replace', check=True).stdout


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--a', default='origin/dev2')
    ap.add_argument('--b', default='origin/dev')
    ap.add_argument('--no-fetch', action='store_true')
    o = ap.parse_args()
    if not o.no_fetch:
        git('fetch', '-q', 'origin')
    only_b, only_a, real = [], [], []
    for line in git('diff', '--name-status', o.a, o.b).splitlines():
        st, *paths = line.split('\t')
        p = paths[-1]
        if INTERNAL.match(p):
            continue
        if st.startswith('A'):
            only_b.append(p)
            continue
        if st.startswith('D'):
            only_a.append(p)
            continue
        d = git('diff', '-U0', o.a, o.b, '--', p)
        bad = [l for l in d.splitlines()
               if l[:1] in '+-' and not l.startswith(('+++', '---')) and not EXPECTED.match(l[1:])]
        # internal-nav blocks whose indentation differs between branches are expected too
        bad = [l for l in bad if 'class="internal-nav"' not in l and 'reader-comments.html' not in l
               and 'future-articles.html' not in l and 'editors/index.html' not in l and '>Edition Index<' not in l]
        if bad:
            real.append((p, bad))
    print(f'Comparing {o.a} (A) with {o.b} (B), reader-facing files only\n')
    print(f'Files only on {o.b}: {len(only_b)}')
    for p in only_b:
        print('   ', p)
    print(f'\nFiles with real content differences: {len(real)}')
    for p, bad in real:
        print(f'  {p}')
        for l in bad[:6]:
            print('     ' + l[:170])
        if len(bad) > 6:
            print(f'     … {len(bad) - 6} more lines')
    print(f'\n(Files only on {o.a}: {len(only_a)} — usually new dev2 work not yet staged; not listed.)')
    print('\nFor each real difference decide which branch is right, then put the fix on dev2 '
          '(and patch dev/master directly if git will not carry it).')
    return 1 if (real or only_b) else 0


if __name__ == '__main__':
    sys.exit(main())
