#!/usr/bin/env python3
"""Keep phrases that must not be split across lines together in article pages (John, Nov 14, 2026).

    python3 tools/keep_together.py 2026-11-15            # every article in the edition
    python3 tools/keep_together.py 2026-11-15 --dry-run  # report only

Only spacing changes (non-breaking spaces and white-space:nowrap spans); the words stay exactly as sent.
- Photo credits ("Photo credit: Angela Garbot.", "Photo: S. Zetouni", "Video: …", "Photos and video by …") are
  kept on one line, moving to the next line as a unit. A credit too long for a phone line (over 34 characters)
  keeps its label together and its name together, so it can only break between the two.
- Titles and initials stay with the name: "Dr. Tessa", "Mrs. J. Young", "Alan M. Bell".
- Month and day ("April 6", "Nov. 15") and number + unit ("50 cents", "7 p.m.") stay together.
Applies to the article region only (headline to end of article-body), text between tags only (never inside
tags or attributes), and is safe to re-run.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NB = '&nbsp;'
NOWRAP = '<span style="white-space:nowrap">'
MAX_NOWRAP = 34  # characters that fit on one caption line at phone width

HONORIFIC = re.compile(r'\b(Mr|Mrs|Ms|Dr|St|Capt|Gen|Rev|Prof|Sr|Jr|Lt|Col|Sgt|Gov|Sen|Rep)\. +(?=\S)')
INITIAL = re.compile(r'\b([A-Z]\.) +(?=[A-Z])')
MONTH_DAY = re.compile(r'\b(January|February|March|April|May|June|July|August|September|October|November|December|'
                       r'Jan\.|Feb\.|Mar\.|Apr\.|Aug\.|Sept\.|Sep\.|Oct\.|Nov\.|Dec\.) +(\d{1,2})\b')
NUM_UNIT = re.compile(r'(\d) +(cents|percent|a\.m\.|p\.m\.|am|pm|AM|PM)\b')
CREDIT_KEY = re.compile(r'(Photo credits?:|Photos? courtesy of|Image courtesy of|Images courtesy of|Courtesy of|'
                        r'Photos and video by|Photos by|Photo by|Video by|Photos?:|Video:|Courtesy)(?= )')


def space_rules(text: str) -> str:
    text = HONORIFIC.sub(lambda m: m.group(1) + '.' + NB, text)
    text = INITIAL.sub(lambda m: m.group(1) + NB, text)
    text = MONTH_DAY.sub(lambda m: m.group(1) + NB + m.group(2), text)
    return NUM_UNIT.sub(lambda m: m.group(1) + NB + m.group(2), text)


def credit_rules(text: str) -> str:
    """Wrap each credit (keyword to the next credit keyword or the end of the text) so it stays together."""
    starts = [m.start() for m in CREDIT_KEY.finditer(text)]
    if not starts:
        return text
    out, pos = [], 0
    for i, st in enumerate(starts):
        end = starts[i + 1] if i + 1 < len(starts) else len(text)
        out.append(text[pos:st])
        seg = text[st:end]
        trail = seg[len(seg.rstrip()):]
        seg = seg.rstrip()
        plain = re.sub(r'&nbsp;', ' ', seg)
        if len(plain) <= MAX_NOWRAP:
            out.append(NOWRAP + seg + '</span>' + trail)
        else:
            m = CREDIT_KEY.match(seg)
            label, name = seg[:m.end()], seg[m.end():].strip()
            # "Image courtesy of" + "Kunstmuseum Liechtenstein.": label together, name together where it fits
            name_html = NOWRAP + name + '</span>' if len(re.sub(r'&nbsp;', ' ', name)) <= MAX_NOWRAP else name
            out.append(label.replace(' ', NB) + ' ' + name_html + trail)
        pos = end
    out.append(text[pos:])
    return ''.join(out)


def process(html: str) -> tuple[str, int]:
    a = html.find('<h1')
    b = html.find('<!-- end article-body')
    if a < 0 or b < 0:
        return html, 0
    region = html[a:b]
    parts = re.split(r'(<[^>]+>)', region)
    changes = 0
    in_caption = in_credit_p = False
    for i, p in enumerate(parts):
        if p.startswith('<'):
            low = p.lower()
            if low.startswith('<figcaption'):
                in_caption = True
            elif low.startswith('</figcaption'):
                in_caption = False
            elif low.startswith('<p'):
                nxt = parts[i + 1] if i + 1 < len(parts) else ''
                in_credit_p = bool(CREDIT_KEY.match(nxt.strip()))
            elif low.startswith('</p'):
                in_credit_p = False
            continue
        if not p.strip() or 'white-space:nowrap' in (parts[i - 1] if i else ''):
            continue
        new = space_rules(p)
        if in_caption or in_credit_p:
            new = credit_rules(new)
        if new != p:
            parts[i] = new
            changes += 1
    return html[:a] + ''.join(parts) + html[b:], changes


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('date')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    files = sorted((ROOT / 'editions' / a.date).glob('*/index.html'))
    if not files:
        sys.exit(f'no articles under editions/{a.date}')
    total = 0
    for f in files:
        s = f.read_text()
        new, n = process(s)
        if n:
            total += n
            print(f'{f.parent.name}: {n} text runs adjusted')
            if not a.dry_run:
                f.write_text(new)
    print(f'{total} text runs adjusted' + (' (dry run)' if a.dry_run else ''))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
