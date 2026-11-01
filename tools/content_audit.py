#!/usr/bin/env python3
"""
tools/content_audit.py — Automated content-fidelity checks not covered by
verify_edition.py or edition_checks.py.

Covers 6 gaps identified in a Sept 2026 audit review against CLAUDE.md's
recorded mistakes list:
  - #20: DateBook page's own internal Astrochart link (distinct from the
    homepage's link, which verify_edition.py / grep already covers)
  - #21: stale past-date <option>/<section> entries left in the Astrochart
    page after copying forward, and missing end-of-month coverage
  - #23: homepage hero-meta must be author-only, no date
  - #30: same photo used as both a hero figure and duplicated inline
  - #34: no emojis anywhere in article content
  - byline links to about.html cards (added Oct 31, 2026)
  - root pages' DateBook/Astrochart nav links (added Oct 31, 2026)
  - spacing: punctuation spacing and run-together words (added Oct 31, 2026)
  - #60: stale "Coming in the [date] edition" placeholder teaser left on a
    homepage card/hero after the linked article was actually built and made
    Ready

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
            and "thumb-placeholder" not in i and "card-placeholder" not in i
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


def check_homepage_stale_teasers(edition_date):
    print("\n--- Homepage stale placeholder teasers (mistake #60) ---")
    if not os.path.isfile("index.html"):
        print("  (root index.html not found — skipping)")
        return
    content = open("index.html", encoding="utf-8", errors="ignore").read()
    stale_patterns = [
        r"Coming in the [^<]*edition\.?",
        r"\[Article text coming soon\]",
        r"[Cc]oming soon\b",
    ]
    hits = []
    for pat in stale_patterns:
        hits.extend(re.findall(pat, content))
    if hits:
        print(f"  ⚠ STALE placeholder teaser(s) still on homepage: {hits}")
        print(f"    (a card/hero linking to a Ready article must have a real teaser, not prep-edition boilerplate)")
    else:
        print("  ✓ clean — no stale placeholder teaser text found on homepage")


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


def check_writer_retrospective_nav():
    """Mistake #35: standalone writers/<author>/ archive pages must have
    working Previous/Next navigation (with thumbnails) on every article page,
    matching the order shown on the archive's own index.html. Bookend
    articles (first/last) link to ../index.html instead of a sibling."""
    print("\n--- Writer retrospective nav check (mistake #35) ---")

    archive_indexes = sorted(glob.glob("writers/*/index.html"))
    if not archive_indexes:
        print("  (no writers/*/ archive pages found — nothing to check)")
        return

    card_pattern = re.compile(
        r'<a class="article-card" href="([^"/]+)/[^"]*">\s*'
        r'(<img class="card-thumb"|<div class="card-thumb-placeholder")'
    )

    any_problems = False
    for index_path in archive_indexes:
        author_dir = os.path.dirname(index_path)
        with open(index_path, encoding="utf-8", errors="replace") as f:
            index_html = f.read()

        cards = card_pattern.findall(index_html)
        if not cards:
            print(f"  ⚠ {index_path}: no article-card entries found — skipping")
            continue

        slugs = [slug for slug, _ in cards]
        has_thumb = {slug: (marker.startswith("<img")) for slug, marker in cards}

        for i, slug in enumerate(slugs):
            article_path = os.path.join(author_dir, slug, "index.html")
            if not os.path.isfile(article_path):
                print(f"  ✗ {article_path}: missing (linked from {index_path})")
                any_problems = True
                continue

            with open(article_path, encoding="utf-8", errors="replace") as f:
                article_html = f.read()

            if 'class="retro-nav"' not in article_html:
                print(f"  ✗ {article_path}: no retro-nav block found")
                any_problems = True
                continue

            expected_prev = f"../{slugs[i-1]}/" if i > 0 else "../index.html"
            expected_next = f"../{slugs[i+1]}/" if i < len(slugs) - 1 else "../index.html"

            nav_block_match = re.search(
                r'<div class="retro-nav">(.*?)</div>', article_html, re.S
            )
            nav_block = nav_block_match.group(1) if nav_block_match else ""

            if f'href="{expected_prev}"' not in nav_block:
                print(f"  ✗ {article_path}: expected prev link to {expected_prev!r} not found")
                any_problems = True
            if f'href="{expected_next}"' not in nav_block:
                print(f"  ✗ {article_path}: expected next link to {expected_next!r} not found")
                any_problems = True

            # Non-bookend neighbors should carry a thumbnail image alongside the
            # link, unless that neighbor genuinely has no photo of its own
            # (has_thumb[slug] is False, e.g. a text-only recovered article).
            if i > 0 and has_thumb.get(slugs[i - 1], True):
                if "retro-nav-thumb" not in nav_block.split(f'href="{expected_prev}"')[-1].split("</a>")[0]:
                    print(f"  ✗ {article_path}: prev link to {expected_prev!r} is missing its thumbnail image")
                    any_problems = True
            if i < len(slugs) - 1 and has_thumb.get(slugs[i + 1], True):
                if "retro-nav-thumb" not in nav_block.split(f'href="{expected_next}"')[-1].split("</a>")[0]:
                    print(f"  ✗ {article_path}: next link to {expected_next!r} is missing its thumbnail image")
                    any_problems = True

        print(f"  checked {len(slugs)} articles under {author_dir}/")

    if not any_problems:
        print("  ✓ clean — every retrospective article has correct prev/next nav")


# ---------------------------------------------------------------------------
# Punctuation / spacing scan (added Oct 31, 2026)
# ---------------------------------------------------------------------------
# Flags visible spacing slips left by copying contributor text: a space before
# punctuation, a missing space after it, spaces inside brackets or quotes, and
# words run together ("asmayor", "Federation'sdissolution"). It only reports;
# contributor text is verbatim, so fix with the editor's OK (mistake #3, #18).
# Double spaces are counted but not listed: browsers collapse them, so readers
# never see them.
SPACING_PATTERNS = [
    ("space before , . ; : ! ?", r"(?<=\S) +[,.;:!?](?=\s|$|[\u201d\"\u2019)])"),
    ("no space after , ; :", r"[,;:](?=[A-Za-z\u201c\u2018(])"),
    ("no space after sentence period",
     r"(?<![A-Z.\d])(?<!\bSt)(?<!\bDr)(?<!\bMr)(?<!\bMrs)(?<!\bMs)(?<!\bNo)(?<!\bvs)(?<!\bJr)(?<!\bSr)"
     r"(?<!\bInc)(?<!\bCo)\.(?=[A-Z\u201c\"\u2018][a-z])"),
    ("no space after ? or !", r"[?!](?=[A-Za-z])"),
    ("closing quote then letter", r"\u201d(?=[A-Za-z])"),
    ("letter then opening quote or bracket", r"[a-z](?=[\u201c(])"),
    ("space after ( or before )", r"\( | \)"),
    ("space inside curly quotes", r"\u201c +| +\u201d"),
    ("word run together after 's", r"[a-z][\u2019']s[a-z]{5,}"),
]
_DICT = None


def _dictionary():
    global _DICT
    if _DICT is None:
        try:
            _DICT = {w.strip().lower() for w in open("/usr/share/dict/words", encoding="utf-8", errors="ignore")}
        except OSError:
            _DICT = set()
    return _DICT


_RUN_ON_ALLOW = {"troubleshooting", "spokesperson", "onsite", "withdrew"}
_GLUED = re.compile(r"\b(isa|ofa|ofthe|inthe|tothe|onthe|atthe|andthe|forthe|asthe|bythe)\b")
_FUNCTION_WORDS = ("as", "is", "of", "to", "in", "on", "at", "by", "or", "an", "so", "it", "he", "we", "if",
                   "the", "and", "but", "for", "with", "from", "was", "are", "has", "had", "his", "her")


def _word_ok(w, words):
    """True if w, or w without a common inflection, is a dictionary word."""
    if w in words:
        return True
    for suf, add in (("ing", ""), ("ing", "e"), ("ed", ""), ("ed", "e"), ("es", ""), ("s", ""), ("ies", "y"), ("ly", ""), ("er", ""), ("ers", "")):
        if w.endswith(suf) and len(w) > len(suf) + 2 and (w[:-len(suf)] + add) in words:
            return True
    return False


def _possible_run_ons(text):
    """Lowercase words 6+ letters that are not words but split into (function word or inflected word) + word."""
    words = _dictionary()
    if not words:
        return []
    out = []
    for w in set(re.findall(r"\b[a-z]{6,}\b", text)):
        if w in _RUN_ON_ALLOW or _word_ok(w, words):
            continue
        for i in range(2, len(w) - 3):
            a, b = w[:i], w[i:]
            if len(b) < 4 or not _word_ok(b, words):
                continue
            if a in _FUNCTION_WORDS or (len(a) >= 4 and (a.endswith("ed") or a.endswith("s")) and _word_ok(a, words)):
                out.append((w, a, b))
                break
    for mm in _GLUED.finditer(text):
        out.append((mm.group(0), mm.group(0), "(two short words run together)"))
    return out


def check_punctuation_spacing(edition_dir):
    print("\n--- Punctuation and spacing scan ---")
    import html as _html
    problems = False
    double = 0
    for name in sorted(os.listdir(edition_dir)):
        path = os.path.join(edition_dir, name, "index.html")
        if not os.path.isfile(path):
            continue
        h = open(path, encoding="utf-8", errors="ignore").read()
        if name.startswith("datebook"):
            m = re.search(r'<div class="datebook-body">(.*?)<!-- /datebook-body', h, re.S)
        elif name.startswith("daily-star"):
            m = re.search(r'(<section class="astro-day".*</section>)', h, re.S)
        else:
            m = re.search(r'<div class="article-body">(.*?)<!-- end article-body', h, re.S)
        if not m:
            continue
        body = re.sub(r"</(p|h2|figcaption|li|div)>|<br\s*/?>", "\n", m.group(1))
        text = _html.unescape(re.sub(r"<[^>]+>", "", body))
        text = re.sub(r"https?://\S+", "URL", text)
        double += len(re.findall(r"(?<=\S)  +(?=\S)", text))
        hits = []
        for label, pat in SPACING_PATTERNS:
            for mm in re.finditer(pat, text):
                ctx = text[max(0, mm.start() - 30):mm.end() + 30].replace("\n", " / ")
                hits.append((label, ctx))
        for w, a, b in _possible_run_ons(text):
            hits.append(("possible run-on", f"{w} ({a} + {b})"))
        if hits:
            problems = True
            print(f"  ⚠ {name}: {len(hits)} to look at")
            for label, ctx in hits[:12]:
                print(f"      {label}: ...{ctx}...")
    if not problems:
        print("  ✓ clean — no spacing or run-together problems found")
    if double:
        print(f"  (note: {double} double spaces in the source text; invisible in browsers, not listed)")


def check_root_page_nav_links(edition_date):
    """Every root page with a DateBook or Astrochart nav link must point at the current edition (added Oct 31, 2026).

    edition_checks.py and the homepage grep only looked at index.html, so about, advertise, subscribe, write-for-us and
    editorial kept linking to August and October DateBooks (October events dimmed as past) for weeks.
    """
    print("\n--- Root pages: DateBook and Astrochart nav links ---")
    problems = False
    for path in sorted(glob.glob("*.html")):
        h = open(path, encoding="utf-8", errors="ignore").read()
        h = re.sub(r"<!--.*?-->", "", h, flags=re.S)
        for kind, pat in (("DateBook", r'href="[^"]*editions/(\d{4}-\d{2}-\d{2})/datebook/"'),
                          ("Astrochart", r'href="[^"]*editions/(\d{4}-\d{2}-\d{2})/daily-star[^"]*"')):
            for found in sorted(set(re.findall(pat, h))):
                if found != edition_date:
                    print(f"  \u2717 {path}: {kind} link points to the {found} edition, not {edition_date}")
                    problems = True
    if not problems:
        print(f"  \u2713 clean \u2014 every root page's DateBook and Astrochart links point to {edition_date}")


def check_bylines(article_dirs):
    """Every byline must link to an existing about.html card, matching the About the Author link (added Oct 31, 2026).

    The article template once shipped a plain-text byline and all seven Nov 1 articles went live unlinked.
    """
    print("\n--- Byline links (article structure #4 and #7) ---")
    about = open("about.html", encoding="utf-8", errors="ignore").read()
    cards = dict(re.findall(r'<div class="team-member" id="([a-z0-9-]+)".*?<h3>(.*?)</h3>', about, re.S))
    problems = False
    for d in article_dirs:
        h = open(os.path.join(d, "index.html"), encoding="utf-8", errors="ignore").read()
        h = re.sub(r"<!--.*?-->", "", h, flags=re.S)
        by = re.search(r'class="article-meta">By <a href="[^"]*about\.html#([a-z0-9-]+)">([^<]+)</a>', h)
        if not by:
            print(f"  \u2717 {d}: byline is not a link to about.html")
            problems = True
            continue
        aid, name = by.group(1), by.group(2).strip()
        about_link = re.search(r'about\.html#([a-z0-9-]+)"[^>]*>About the Author', h)
        if aid not in cards:
            print(f"  \u2717 {d}: about.html has no card with id {aid!r}")
            problems = True
        elif re.sub(r"<[^>]+>", "", cards[aid]).strip() != name:
            print(f"  \u2717 {d}: byline {name!r} does not match about.html card {cards[aid]!r}")
            problems = True
        if not about_link or about_link.group(1) != aid:
            print(f"  \u2717 {d}: 'About the Author' link is missing or uses a different anchor than the byline")
            problems = True
    if not problems:
        print(f"  \u2713 clean \u2014 all {len(article_dirs)} bylines link to a matching about.html card")


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
    check_homepage_stale_teasers(edition_date)
    check_datebook_astrochart_link(edition_dir, edition_date)
    check_astrochart_stale_dates(edition_dir, edition_date)
    check_bylines(dirs)
    check_punctuation_spacing(edition_dir)
    check_root_page_nav_links(edition_date)
    check_writer_retrospective_nav()

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
