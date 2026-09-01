#!/usr/bin/env python3
"""
tools/content_audit.py — Automated content-fidelity checks not covered by
verify_edition.py or edition_checks.py.

Covers 5 gaps identified in a Sept 2026 audit review against CLAUDE.md's
recorded mistakes list:
  - #20: DateBook page's own internal Astrochart link (distinct from the
    homepage's link, which verify_edition.py / grep already covers)
  - #21: stale past-date <option>/<section> entries left in the Astrochart
    page after copying forward, and missing end-of-month coverage
  - #23: homepage hero-meta must be author-only, no date
  - #30: same photo used as both a hero figure and duplicated inline
  - #34: no emojis anywhere in article content

Usage:
    python3 tools/content_audit.py YYYY-MM-DD
"""

import sys
import re
import glob
import os
from datetime import date, timedelta
import calendar

EMOJI_PATTERN = re.compile(
    "["
    "\U0001F300-\U0001FAFF"
    "\U00002600-\U000027BF"
    "\U0001F1E0-\U0001F1FF"
    "\U00002190-\U000021FF"  # arrows (catches some emoji-adjacent symbols; visually reviewed below)
    "]"
)
# Arrows are used legitimately for nav (&larr; &rarr; etc. are HTML entities, not raw
# unicode, so this range mostly stays quiet — kept narrow deliberately).
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F300-\U0001FAFF"
    "\U00002600-\U000026FF"
    "\U00002700-\U000027BF"
    "\U0001F1E0-\U0001F1FF"
    "]"
)

DATE_WORD_PATTERN = re.compile(
    r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\b"
    r"|\b\d{1,2}/\d{1,2}/\d{2,4}\b"
)


def find_edition_dir(edition_date):
    d = os.path.join("editions", edition_date)
    if not os.path.isdir(d):
        print(f"ERROR: {d} does not exist")
        sys.exit(1)
    return d


def article_dirs(edition_dir):
    dirs = []
    for name in sorted(os.listdir(edition_dir)):
        path = os.path.join(edition_dir, name)
        if not os.path.isdir(path):
            continue
        if name.startswith("datebook") or name.startswith("daily-star"):
            continue
        if os.path.isfile(os.path.join(path, "index.html")):
            dirs.append(path)
    return dirs


def check_emoji(article_dirs):
    print("\n--- Emoji scan (mistake #34) ---")
    found_any = False
    for d in article_dirs:
        content = open(os.path.join(d, "index.html"), encoding="utf-8", errors="ignore").read()
        matches = EMOJI_PATTERN.findall(content)
        if matches:
            found_any = True
            print(f"  ⚠ {d}: found {matches}")
    if not found_any:
        print("  ✓ clean — no emoji found in any article")


def check_duplicate_photos(article_dirs):
    print("\n--- Duplicate photo scan (mistake #30: hero + inline duplicate) ---")
    found_any = False
    for d in article_dirs:
        content = open(os.path.join(d, "index.html"), encoding="utf-8", errors="ignore").read()
        imgs = re.findall(r'<img[^>]*src="([^"]+)"', content)
        imgs = [
            i for i in imgs
            if not i.startswith("http") and "navthumb" not in i and "logo" not in i.lower()
        ]
        seen = {}
        for i in imgs:
            seen[i] = seen.get(i, 0) + 1
        dupes = {k: v for k, v in seen.items() if v > 1}
        if dupes:
            found_any = True
            print(f"  ⚠ {d}: {dupes}")
    if not found_any:
        print("  ✓ clean — no photo used twice in the same article")


def check_hero_meta_date(edition_date):
    print("\n--- Homepage hero-meta date check (mistake #23) ---")
    if not os.path.isfile("index.html"):
        print("  (root index.html not found — skipping)")
        return
    content = open("index.html", encoding="utf-8", errors="ignore").read()
    m = re.search(r'<div class="hero-meta">(.*?)</div>', content)
    if not m:
        print("  (no hero-meta div found — skipping)")
        return
    hero_text = m.group(1)
    if DATE_WORD_PATTERN.search(hero_text):
        print(f"  ⚠ hero-meta contains what looks like a date: \"{hero_text}\"")
    else:
        print(f"  ✓ clean — hero-meta is author-only: \"{hero_text}\"")


def check_datebook_astrochart_link(edition_dir, edition_date):
    print("\n--- DateBook's own internal Astrochart link (mistake #20) ---")
    datebook_index = os.path.join(edition_dir, "datebook", "index.html")
    if not os.path.isfile(datebook_index):
        print("  (no datebook/index.html in this edition — skipping)")
        return

    # Find this edition's actual daily-star-* folder name
    astro_dirs = [
        name for name in os.listdir(edition_dir)
        if name.startswith("daily-star") and os.path.isdir(os.path.join(edition_dir, name))
    ]
    if not astro_dirs:
        print("  ⚠ no daily-star-* folder exists in this edition at all")
        return
    expected_slug = astro_dirs[0]

    content = open(datebook_index, encoding="utf-8", errors="ignore").read()
    links = re.findall(r'href="([^"]*daily-star[^"]*)"', content)
    if not links:
        print("  ⚠ datebook page has no Astrochart link at all")
        return

    stale = [l for l in links if expected_slug not in l]
    if stale:
        print(f"  ⚠ STALE — datebook links to {stale}, but this edition's astrochart is '{expected_slug}/'")
    else:
        print(f"  ✓ clean — datebook's Astrochart link correctly points to '{expected_slug}/'")


def check_astrochart_stale_dates(edition_dir, edition_date):
    print("\n--- Astrochart stale past-date entries (mistake #21) ---")
    astro_dirs = [
        name for name in os.listdir(edition_dir)
        if name.startswith("daily-star") and os.path.isdir(os.path.join(edition_dir, name))
    ]
    if not astro_dirs:
        print("  (no daily-star-* folder in this edition — skipping)")
        return

    astro_path = os.path.join(edition_dir, astro_dirs[0], "index.html")
    if not os.path.isfile(astro_path):
        print(f"  (no index.html in {astro_dirs[0]} — skipping)")
        return

    content = open(astro_path, encoding="utf-8", errors="ignore").read()
    option_dates = re.findall(r'<option value="(\d{4}-\d{2}-\d{2})"', content)
    section_dates = re.findall(r'data-date="(\d{4}-\d{2}-\d{2})"', content)
    all_dates = sorted(set(option_dates) | set(section_dates))

    if not all_dates:
        print("  (no dated <option>/<section> entries found — skipping)")
        return

    parsed = [date.fromisoformat(d) for d in all_dates]
    min_date, max_date = min(parsed), max(parsed)

    # Determine the month this astrochart page is supposed to cover from its
    # most common month among entries (robust to a few cross-month spillover days).
    from collections import Counter
    month_counts = Counter((d.year, d.month) for d in parsed)
    covered_year, covered_month = month_counts.most_common(1)[0][0]
    month_start = date(covered_year, covered_month, 1)
    month_end = date(covered_year, covered_month, calendar.monthrange(covered_year, covered_month)[1])

    stale = [d for d in parsed if d < month_start]
    if stale:
        print(f"  ⚠ STALE — {len(stale)} entries predate {month_start.isoformat()}: {[d.isoformat() for d in stale[:5]]}{' ...' if len(stale) > 5 else ''}")
    else:
        print(f"  ✓ no stale pre-month entries (earliest: {min_date.isoformat()})")

    if max_date < month_end:
        missing_days = (month_end - max_date).days
        print(f"  ⚠ INCOMPLETE — coverage ends {max_date.isoformat()}, missing {missing_days} day(s) through {month_end.isoformat()}")
    else:
        print(f"  ✓ coverage extends through month-end ({max_date.isoformat()})")


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 tools/content_audit.py YYYY-MM-DD")
        sys.exit(1)

    edition_date = sys.argv[1]
    edition_dir = find_edition_dir(edition_date)
    dirs = article_dirs(edition_dir)

    print("=" * 80)
    print(f"CONTENT AUDIT: {edition_date}")
    print("=" * 80)

    check_emoji(dirs)
    check_duplicate_photos(dirs)
    check_hero_meta_date(edition_date)
    check_datebook_astrochart_link(edition_dir, edition_date)
    check_astrochart_stale_dates(edition_dir, edition_date)

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
