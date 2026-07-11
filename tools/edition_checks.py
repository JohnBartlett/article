#!/usr/bin/env python3
"""
edition_checks.py — Weekly automated checks and fixes for Classic Chicago Magazine.

Run after adding a new edition to:
  1. Add dark-mode.js to any pages missing it
  2. Add nav-thumb CSS to any articles missing it
  3. Update about.html author popups with new articles
  4. Report any new authors who need manual bio entries

Usage:
    python3 tools/edition_checks.py [--dry-run]
"""

import os
import re
import sys
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
EDITIONS = ROOT / 'editions'
ABOUT = ROOT / 'about.html'
DRY_RUN = '--dry-run' in sys.argv

EDITION_DATES = {
    '2026-02-08': 'February 8, 2026',
    '2026-02-15': 'February 15, 2026',
    '2026-02-22': 'February 22, 2026',
    '2026-03-01': 'March 1, 2026',
    '2026-03-08': 'March 8, 2026',
    '2026-03-15': 'March 15, 2026',
    '2026-03-22': 'March 22, 2026',
    '2026-03-29': 'March 29, 2026',
    '2026-04-05': 'April 5, 2026',
    '2026-04-12': 'April 12, 2026',
    '2026-04-19': 'April 19, 2026',
    '2026-04-26': 'April 26, 2026',
    '2026-05-03': 'May 3, 2026',
    '2026-05-10': 'May 10, 2026',
    '2026-05-17': 'May 17, 2026',
    '2026-05-24': 'May 24, 2026',
    '2026-05-31': 'May 31, 2026',
}

NAV_CSS = (
    "\n    .edition-nav .back-link { display: flex; align-items: center; gap: 12px; border-bottom: none; }"
    "\n    .nav-thumb { width: 64px; height: 48px; object-fit: cover; border-radius: 2px; flex-shrink: 0; }"
    "\n    .nav-text { display: flex; flex-direction: column; gap: 4px; }"
    "\n    .nav-dir { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: #b51c20; }"
    "\n    .nav-title { font-size: 13px; line-height: 1.3; color: #333; }"
)

results = {
    'dark_mode_added': [],
    'nav_css_added': [],
    'popup_articles_added': [],
    'new_authors_needing_bios': [],
    'stale_datebook_months': [],
}

MONTH_NAMES = ['', 'January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']


# ── helpers ──────────────────────────────────────────────────────────────────

def write_file(path, content):
    if DRY_RUN:
        print(f'  [dry-run] would write {path}')
        return
    path.write_text(content)


def edition_date_str(edition):
    """Return human-readable date string for an edition folder name."""
    if edition in EDITION_DATES:
        return EDITION_DATES[edition]
    # Parse YYYY-MM-DD generically
    parts = edition.split('-')
    if len(parts) == 3:
        months = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
        try:
            m, d, y = int(parts[1]), int(parts[2]), parts[0]
            return f'{months[m]} {d}, {y}'
        except Exception:
            pass
    return edition


def extract_article_meta(html_path):
    """Return (author_id, title, cover_image) from an article index.html."""
    text = html_path.read_text(errors='replace')

    # Author ID from about.html# anchor
    m = re.search(r'about\.html#([\w-]+)', text)
    author_id = m.group(1) if m else None

    # Title from h1.article-title or first <h1>
    m = re.search(r'<h1[^>]*class="[^"]*article-title[^"]*"[^>]*>(.*?)</h1>', text, re.S)
    if not m:
        m = re.search(r'<h1[^>]*>(.*?)</h1>', text, re.S)
    title = re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else ''

    # Cover image: first <img> after <main> or after byline, skipping logo
    # Look for hero-figure img or first figure img
    m = re.search(r'<(?:figure|div)[^>]*class="[^"]*hero[^"]*"[^>]*>.*?<img[^>]+src="([^"]+)"', text, re.S)
    if not m:
        # First img that isn't logo.jpg or favicon
        imgs = re.findall(r'<img[^>]+src="([^"]+)"', text)
        cover = next((i for i in imgs if 'logo' not in i and 'favicon' not in i
                      and not i.startswith('http') and not i.startswith('../../../')), None)
        m = None
        cover_img = cover
    else:
        cover_img = m.group(1)

    # Get just the filename
    if cover_img:
        cover_img = cover_img.split('/')[-1]

    return author_id, title, cover_img


def article_mini_html(edition, slug, title, date_str, img):
    img_tag = f'\n          <img src="editions/{edition}/{slug}/{img}" alt="{title}">' if img else ''
    return (
        f'        <a href="editions/{edition}/{slug}/" class="article-mini">{img_tag}\n'
        f'          <span class="article-mini-info">\n'
        f'            <span class="article-mini-title">{title}</span>\n'
        f'            <span class="article-mini-date">{date_str}</span>\n'
        f'          </span>\n'
        f'        </a>'
    )


# ── 1 & 2. Per-page fixes: dark-mode.js and nav-thumb CSS ───────────────────

def fix_page(html_path, depth):
    """Add dark-mode.js and nav-thumb CSS to a page if missing. Returns True if changed."""
    text = html_path.read_text(errors='replace')
    changed = False

    # dark-mode.js
    if 'dark-mode.js' not in text and '</head>' in text:
        rel = '../../' if depth == 2 else '../../../'
        text = text.replace('</head>', f'  <script src="{rel}dark-mode.js"></script>\n</head>', 1)
        changed = True
        results['dark_mode_added'].append(str(html_path.relative_to(ROOT)))

    # nav-thumb CSS: only needed in articles (depth 3) that have nav-thumb img elements
    if depth == 3 and 'class="nav-thumb"' in text and '.nav-thumb' not in text:
        # Insert after .back-link:hover block (handles both inline and multiline forms)
        inline_pat = r'(    \.back-link:hover \{ color: #d41f1f; border-bottom: 1px solid #d41f1f; \})'
        multi_pat  = r'(    \.back-link:hover \{[^}]+\})'
        if re.search(inline_pat, text):
            text = re.sub(inline_pat, r'\1' + NAV_CSS, text, count=1)
            changed = True
        elif re.search(multi_pat, text):
            text = re.sub(multi_pat, r'\1' + NAV_CSS, text, count=1)
            changed = True
        if changed:
            results['nav_css_added'].append(str(html_path.relative_to(ROOT)))

    if changed:
        write_file(html_path, text)
    return changed


def scan_pages():
    """Fix dark-mode and nav-thumb across all edition pages."""
    for edition_dir in sorted(EDITIONS.iterdir()):
        if not edition_dir.is_dir():
            continue
        # Edition homepage (depth 2)
        homepage = edition_dir / 'index.html'
        if homepage.exists():
            fix_page(homepage, depth=2)
        # Article pages (depth 3)
        for article_dir in sorted(edition_dir.iterdir()):
            if not article_dir.is_dir():
                continue
            article = article_dir / 'index.html'
            if article.exists():
                fix_page(article, depth=3)


# ── 3. Update about.html author popups ──────────────────────────────────────

def get_popup_existing_hrefs(about_html, author_id):
    """Return set of href values already in the author's articles popup."""
    popup_pat = re.compile(
        rf'<div id="articles-{re.escape(author_id)}"[^>]*>(.*?)</div>\s*</div>',
        re.S
    )
    m = popup_pat.search(about_html)
    if not m:
        return set()
    return set(re.findall(r'href="([^"]+)"', m.group(1)))


def insert_mini_into_popup(about_html, author_id, mini_html):
    """Append a new article-mini entry to an existing author popup."""
    # Find the articles-grid closing tag inside this author's popup
    popup_pat = re.compile(
        rf'(<div id="articles-{re.escape(author_id)}"[^>]*>.*?<div class="articles-grid">)(.*?)(        </div>\s*</div>\s*</div>)',
        re.S
    )
    m = popup_pat.search(about_html)
    if not m:
        return about_html, False
    new_grid = m.group(2) + mini_html + '\n'
    return about_html[:m.start()] + m.group(1) + new_grid + m.group(3) + about_html[m.end():], True


def update_about_popups(articles_by_author):
    """Add missing articles to existing author popups in about.html."""
    about_html = ABOUT.read_text()
    changed = False

    for author_id, articles in sorted(articles_by_author.items()):
        existing = get_popup_existing_hrefs(about_html, author_id)
        if not existing:
            # Author has no popup at all — flag for manual attention
            continue
        for (edition, slug, title, cover_img) in articles:
            href = f'editions/{edition}/{slug}/'
            if href in existing:
                continue
            date_str = edition_date_str(edition)
            mini = article_mini_html(edition, slug, title, date_str, cover_img)
            about_html, ok = insert_mini_into_popup(about_html, author_id, mini)
            if ok:
                results['popup_articles_added'].append(f'{author_id}: {title} ({date_str})')
                changed = True

    if changed:
        write_file(ABOUT, about_html)


def check_datebook_stale_months():
    """Flag month-header sections in the current (STATUS.md-active) edition's
    DateBook that are chronologically before that edition's own month — these
    are past events left over from copying the previous week's DateBook and
    should be edited out before staging."""
    current_edition_dir = None
    current_edition_date = None
    for edition_dir in sorted(EDITIONS.iterdir()):
        if edition_dir.is_dir() and (edition_dir / 'STATUS.md').exists():
            current_edition_dir = edition_dir
    if current_edition_dir is None:
        return
    parts = current_edition_dir.name.split('-')
    if len(parts) != 3:
        return
    try:
        edition_month = int(parts[1])
    except ValueError:
        return
    datebook_path = current_edition_dir / 'datebook' / 'index.html'
    if not datebook_path.exists():
        return
    text = datebook_path.read_text(errors='replace')
    for m in re.finditer(r'<div class="month-header">(\w+)</div>', text):
        month_name = m.group(1)
        if month_name in MONTH_NAMES:
            month_num = MONTH_NAMES.index(month_name)
            if month_num < edition_month:
                results['stale_datebook_months'].append({
                    'edition': current_edition_dir.name,
                    'month': month_name,
                })


def check_new_authors(articles_by_author):
    """Flag authors who have articles but no bio in about.html."""
    about_html = ABOUT.read_text()
    for author_id in sorted(articles_by_author):
        if f'id="{author_id}"' not in about_html:
            articles = articles_by_author[author_id]
            results['new_authors_needing_bios'].append({
                'id': author_id,
                'articles': [f"{edition_date_str(e)}: {t}" for e, s, t, _ in articles]
            })


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    print('Classic Chicago Magazine — Weekly Edition Checks')
    print('=' * 52)
    if DRY_RUN:
        print('DRY RUN — no files will be written\n')

    # Collect all article metadata
    articles_by_author = {}  # author_id → [(edition, slug, title, cover_img)]
    skip_slugs = {'datebook', 'daily-star-april', 'daily-star-march'}

    for edition_dir in sorted(EDITIONS.iterdir()):
        if not edition_dir.is_dir():
            continue
        edition = edition_dir.name
        for article_dir in sorted(edition_dir.iterdir()):
            if not article_dir.is_dir() or article_dir.name in skip_slugs:
                continue
            article = article_dir / 'index.html'
            if not article.exists():
                continue
            author_id, title, cover_img = extract_article_meta(article)
            if not author_id or not title:
                continue
            articles_by_author.setdefault(author_id, []).append(
                (edition, article_dir.name, title, cover_img)
            )

    # Run fixes
    print('\n[1/4] Checking dark-mode.js and nav-thumb CSS…')
    scan_pages()

    print('[2/4] Updating about.html author popups…')
    update_about_popups(articles_by_author)

    print('[3/4] Checking for new authors needing bios…')
    check_new_authors(articles_by_author)

    print('[4/4] Checking DateBook for stale past-month sections…')
    check_datebook_stale_months()

    # Report
    print('\n── Results ──────────────────────────────────────')
    if results['dark_mode_added']:
        print(f'\n✓ dark-mode.js added to {len(results["dark_mode_added"])} pages:')
        for p in results['dark_mode_added']:
            print(f'    {p}')
    else:
        print('\n✓ dark-mode.js: all pages OK')

    if results['nav_css_added']:
        print(f'\n✓ nav-thumb CSS added to {len(results["nav_css_added"])} articles:')
        for p in results['nav_css_added']:
            print(f'    {p}')
    else:
        print('✓ nav-thumb CSS: all articles OK')

    if results['popup_articles_added']:
        print(f'\n✓ about.html popups updated — {len(results["popup_articles_added"])} articles added:')
        for entry in results['popup_articles_added']:
            print(f'    {entry}')
    else:
        print('✓ about.html popups: all up to date')

    if results['new_authors_needing_bios']:
        print(f'\n⚠  {len(results["new_authors_needing_bios"])} new author(s) need manual bios in about.html:')
        for a in results['new_authors_needing_bios']:
            print(f'\n    id="{a["id"]}"')
            for art in a['articles']:
                print(f'      • {art}')
        print('\n  → Run /edition-checks for guided bio writing')
    else:
        print('✓ about.html bios: all authors covered')

    if results['stale_datebook_months']:
        print(f'\n⚠  DateBook has {len(results["stale_datebook_months"])} stale past-month section(s):')
        for s in results['stale_datebook_months']:
            print(f'    {s["edition"]}/datebook — {s["month"]} (before this edition\'s month, should be removed)')
    else:
        print('✓ DateBook: no stale past-month sections')

    print('\n── Done ─────────────────────────────────────────')

    # Machine-readable output for the skill
    report_path = ROOT / 'tools' / 'edition_checks_report.json'
    if not DRY_RUN:
        report_path.write_text(json.dumps(results, indent=2))

    return 0 if not results['new_authors_needing_bios'] else 1


if __name__ == '__main__':
    sys.exit(main())
