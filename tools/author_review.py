#!/usr/bin/env python3
"""Build an "author's review" page: an unlinked copy of a laid-out dev2 article for its writer to check.

    python3 tools/author_review.py 2026-11-15 francesco-iguazu
    -> review/2026-11-15/francesco-iguazu/index.html
       https://article-dev2.vercel.app/review/2026-11-15/francesco-iguazu/

The copy keeps the article exactly as laid out (text, photos, captions, video) but links nowhere else on
dev2 (CLAUDE.md #33): no site menu, no internal nav, no logo or byline links, no About the Author link,
no feedback widget, no prev/next links, no N/P keyboard shortcuts. Photos and video load from the article's
own folder, so nothing is duplicated. It carries a noindex tag and a banner saying it is unpublished.
review/ is dev2-only: tools/strip_internal_files.sh removes it from dev and master.
Re-run after any change to the article so the review stays current.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def build(date: str, slug: str) -> Path:
    src = ROOT / 'editions' / date / slug / 'index.html'
    if not src.exists():
        sys.exit(f'no article at {src}')
    s = src.read_text()
    edition_label = re.search(r'&bull;&nbsp;\s*([A-Z][a-z]+ \d{1,2}, \d{4})', s)
    edition_label = edition_label.group(1) if edition_label else date

    def sub1(pattern: str, repl: str, text: str, what: str) -> str:
        out, n = re.subn(pattern, repl, text, count=1, flags=re.S)
        if n != 1:
            sys.exit(f'could not find {what} in {src}')
        return out

    s = sub1(r'(<meta name="viewport"[^>]*>)', r'\1\n  <meta name="robots" content="noindex, nofollow">', s, 'viewport meta')
    s = sub1(r'<a href="\.\./\.\./\.\./index\.html">\s*(<img src="\.\./\.\./\.\./logo\.jpg"[^>]*>)\s*</a>', r'\1', s, 'logo link')
    s = sub1(r'\n    <nav>.*?</nav>', '', s, 'site menu')
    s = re.sub(r'\n  <!-- dev2-only -->\n  <div class="internal-nav">.*?</div>\n', '\n', s, count=1, flags=re.S)
    banner = ('\n  <div style="background:#fdf3e7; border-bottom:1px solid #e8d5bd; padding:12px 16px; text-align:center; '
              "font-family:'Lato',sans-serif; font-size:14px; color:#6b4e2e;\">"
              f"<strong>Author&rsquo;s review.</strong> This is your article as it will appear in the {edition_label} edition "
              'of Classic Chicago Magazine. It is not yet published; please do not share this link.</div>\n')
    s = sub1(r'(</header>\n)', r'\1' + banner.replace('\\', r'\\'), s, 'end of header')
    s = sub1(r'(<div class="article-meta">By )<a href="[^"]*">([^<]+)</a>', r'\1\2', s, 'byline link')
    s = sub1(r'\n      <!-- About the Author -->.*?<!-- end feedback widget -->\n', '\n', s, 'About the Author + feedback widget')
    s = sub1(r'\n      <!-- Article Navigation.*?<!-- Last article:[^\n]*-->\n', '\n', s, 'article navigation')
    s = sub1(r'\n  <!-- Keyboard nav.*?</script>\n', '\n', s, 'keyboard nav script')
    s = re.sub(r"\n  <script>\(function\(\)\{var btn=document\.getElementById\('hamburger-btn'\).*?</script>\n", '\n', s, count=1, flags=re.S)

    prefix = f'../../../editions/{date}/{slug}/'
    s = re.sub(r'\b(src|poster)="(?![a-z]+:|/|\.\./|#)([^"]+)"', lambda m: f'{m.group(1)}="{prefix}{m.group(2)}"', s)

    body = s[s.find('<body'):]
    leftover = [h for h in re.findall(r'href="([^"]+)"', body) if not h.startswith(('http://', 'https://', 'mailto:'))]
    if leftover:
        sys.exit(f'internal links remain: {leftover}')
    out = ROOT / 'review' / date / slug / 'index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(s)
    for m in re.findall(r'(?:src|poster)="(\.\./\.\./\.\./[^"#]+)', s):
        if not (out.parent / m).resolve().exists():
            sys.exit(f'missing file: {m}')
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('date')
    ap.add_argument('slug')
    a = ap.parse_args()
    out = build(a.date, a.slug)
    print(out.relative_to(ROOT))
    print(f'https://article-dev2.vercel.app/review/{a.date}/{a.slug}/')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
