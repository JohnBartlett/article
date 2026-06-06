#!/usr/bin/env python3
"""
Verify actual article status for an edition.
Reports content, photos, nav chain, broken images, datebook link,
internal-nav state, byline anchor, feedback widget, and footer.

Usage: python3 tools/verify_edition.py 2026-04-26
"""

import sys
import os
import re
from pathlib import Path
from urllib.parse import unquote

IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.JPG', '.JPEG', '.PNG'}

# ── HTML parsing helpers ──────────────────────────────────────────────────────

def parse_html(content):
    """Return a simple dict of facts extracted from an article's HTML."""
    facts = {
        'prev_href': None,
        'next_href': None,
        'img_srcs': [],          # all img src values
        'datebook_href': None,
        'internal_nav_active': False,   # <!-- dev2-only --> style (uncommented)
        'internal_nav_commented': False, # <!-- dev2-only ... --> style
        'byline_anchor': None,   # the #fragment in the byline author link
        'has_feedback': False,
        'has_footer': False,
        'has_social_icons': False,
        'has_h1': False,
        'has_byline': False,
    }

    # Internal-nav state
    if '<!-- dev2-only -->' in content:
        facts['internal_nav_active'] = True
    if re.search(r'<!-- dev2-only\s*\n', content):
        facts['internal_nav_commented'] = True

    # h1
    facts['has_h1'] = bool(re.search(r'<h1[ >]', content))

    # byline: look for class="byline"
    byline_m = re.search(r'class="byline"[^>]*>.*?<a href="[^"]*about\.html(#[^"]+)"', content, re.DOTALL)
    if byline_m:
        facts['has_byline'] = True
        facts['byline_anchor'] = byline_m.group(1)

    # feedback widget
    facts['has_feedback'] = 'feedback-widget' in content

    # footer
    facts['has_footer'] = '<footer' in content
    # social icons: footer should have SVG icons, not plain text links
    footer_m = re.search(r'<footer>(.*?)</footer>', content, re.DOTALL)
    facts['has_social_icons'] = bool(footer_m and '<svg' in footer_m.group(1))

    # datebook link in nav
    db_m = re.search(r'<a href="([^"]*datebook[^"]*)"[^>]*>DateBook</a>', content)
    if db_m:
        facts['datebook_href'] = db_m.group(1)

    # article-nav prev/next
    nav_m = re.search(r'<nav class="article-nav">(.*?)</nav>', content, re.DOTALL)
    if nav_m:
        nav_html = nav_m.group(1)
        prev_m = re.search(r'class="prev"[^>]*href="([^"]+)"', nav_html)
        next_m = re.search(r'class="next"[^>]*href="([^"]+)"', nav_html)
        if prev_m:
            facts['prev_href'] = prev_m.group(1)
        if next_m:
            facts['next_href'] = next_m.group(1)

    # all img srcs
    facts['img_srcs'] = re.findall(r'<img[^>]+src="([^"]+)"', content)

    return facts


# ── Per-article checks ────────────────────────────────────────────────────────

def check_article_status(edition_path, article_slug):
    """Check content + photo count (existing behaviour)."""
    article_dir = edition_path / article_slug
    if not article_dir.exists():
        return {"status": "MISSING", "reason": "folder does not exist"}
    index_file = article_dir / "index.html"
    if not index_file.exists():
        return {"status": "MISSING", "reason": "index.html does not exist"}

    with open(index_file, encoding='utf-8') as f:
        content = f.read()

    has_placeholder = "placeholder-notice" in content or "[Article text coming soon]" in content
    images = [p for p in article_dir.iterdir() if p.suffix in IMAGE_EXTS]
    image_count = len(images)

    if has_placeholder:
        if image_count > 0:
            return {"status": "IN PROGRESS", "reason": "placeholder text, photos ready"}
        return {"status": "PLACEHOLDER", "reason": "no content, no photos"}
    if image_count > 0:
        return {"status": "READY", "reason": f"content + {image_count} photos", "photos": image_count}
    return {"status": "TEXT ONLY", "reason": "content but no photos"}


def check_article_structure(edition_path, article_slug, about_anchors):
    """Run structural checks on a ready article. Returns list of issue strings."""
    article_dir = edition_path / article_slug
    index_file = article_dir / "index.html"
    if not index_file.exists():
        return []

    with open(index_file, encoding='utf-8') as f:
        content = f.read()

    facts = parse_html(content)
    issues = []
    repo_root = edition_path.parent.parent  # editions/../ = repo root

    # ── Structure ──
    if not facts['has_h1']:
        issues.append("missing <h1>")
    if not facts['has_byline']:
        issues.append("missing byline / author link to about.html")
    if not facts['has_feedback']:
        issues.append("missing feedback widget")
    if not facts['has_footer']:
        issues.append("missing footer")
    if not facts['has_social_icons']:
        issues.append("footer has text social links instead of SVG icons")

    # ── Internal-nav state ──
    if facts['internal_nav_active'] and facts['internal_nav_commented']:
        issues.append("internal-nav: both active and commented markers found (confused state)")
    # (active on dev2 is correct; we don't know which branch we're on here, so just report)

    # ── DateBook link ──
    if facts['datebook_href'] is None:
        issues.append("no DateBook link in nav")
    else:
        # Resolve relative to article dir
        db_path = (article_dir / facts['datebook_href']).resolve()
        db_index = db_path / "index.html"
        if not db_index.exists():
            issues.append(f"DateBook link broken: {facts['datebook_href']}")

    # ── Byline anchor ──
    if facts['byline_anchor'] and about_anchors is not None:
        anchor = facts['byline_anchor'].lstrip('#')
        if anchor not in about_anchors:
            issues.append(f"byline anchor #{anchor} not found in about.html")

    # ── Nav links ──
    for direction, href in [("prev", facts['prev_href']), ("next", facts['next_href'])]:
        if href is None:
            issues.append(f"missing {direction} nav link")
            continue
        # home link is fine
        if href.endswith('index.html') and '../../..' in href:
            continue
        target = (article_dir / href).resolve()
        # nav links point to sibling dirs; target should contain index.html
        target_index = target / "index.html" if target.is_dir() else target
        if not target_index.exists():
            issues.append(f"{direction} nav target missing: {href}")

    # ── Broken images ──
    broken = []
    for src in facts['img_srcs']:
        if src.startswith('http') or src.startswith('//'):
            continue
        img_path = (article_dir / unquote(src)).resolve()
        if not img_path.exists():
            broken.append(src)
    if broken:
        for b in broken:
            issues.append(f"broken image: {b}")

    return issues


# ── about.html anchor extraction ─────────────────────────────────────────────

def get_about_anchors(repo_root):
    """Return set of id= values in about.html."""
    about = repo_root / "about.html"
    if not about.exists():
        return None
    with open(about, encoding='utf-8') as f:
        content = f.read()
    return set(re.findall(r'\bid=["\']([^"\']+)["\']', content))


# ── Main ──────────────────────────────────────────────────────────────────────

def verify_edition(edition_date):
    edition_path = Path(f"editions/{edition_date}")
    if not edition_path.exists():
        print(f"❌ Edition {edition_date} not found")
        return False

    articles = sorted([d.name for d in edition_path.iterdir() if d.is_dir()])
    if not articles:
        print(f"❌ No articles found in {edition_path}")
        return False

    repo_root = Path(".")
    about_anchors = get_about_anchors(repo_root)

    status_counts = {"READY": 0, "TEXT ONLY": 0, "IN PROGRESS": 0, "PLACEHOLDER": 0, "MISSING": 0}

    print(f"\n{'='*80}")
    print(f"EDITION STATUS VERIFICATION: {edition_date}")
    print(f"{'='*80}\n")

    all_issues = {}

    for article in articles:
        status_info = check_article_status(edition_path, article)
        status = status_info["status"]
        status_counts[status] += 1

        symbol = "✓" if status == "READY" else "⚠" if status in ["TEXT ONLY", "IN PROGRESS"] else "✗"
        photos = f" [{status_info.get('photos', 0)} photos]" if "photos" in status_info else ""
        print(f"{symbol} {article:30} | {status:15} | {status_info['reason']}{photos}")

        if status not in ("MISSING", "PLACEHOLDER"):
            issues = check_article_structure(edition_path, article, about_anchors)
            if issues:
                all_issues[article] = issues

    # Summary
    print(f"\n{'-'*80}")
    print(f"SUMMARY:")
    print(f"  ✓ Ready (content + photos):        {status_counts['READY']}")
    print(f"  ⚠ Text only (no photos):          {status_counts['TEXT ONLY']}")
    print(f"  ⚠ In Progress (partial):          {status_counts['IN PROGRESS']}")
    print(f"  ✗ Placeholders (no content):      {status_counts['PLACEHOLDER']}")
    print(f"  ✗ Missing:                        {status_counts['MISSING']}")
    print(f"  {'─'*40}")
    print(f"  Total articles: {len(articles)}")
    print(f"{'-'*80}\n")

    # Structural issues
    if all_issues:
        print(f"STRUCTURAL ISSUES:")
        for article, issues in all_issues.items():
            print(f"\n  {article}:")
            for issue in issues:
                print(f"    ✗ {issue}")
        print()
    else:
        print("STRUCTURAL ISSUES: none\n")

    return {"status_counts": status_counts, "issues": all_issues}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 tools/verify_edition.py YYYY-MM-DD")
        sys.exit(1)
    verify_edition(sys.argv[1])
