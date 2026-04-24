#!/usr/bin/env python3
"""
Verify actual article status for an edition.
Reports what's ACTUALLY in the filesystem, not what we assume.

Usage: python3 tools/verify_edition.py 2026-04-26
"""

import sys
import os
import re
from pathlib import Path

def check_article_status(edition_path, article_slug):
    """Check actual status of an article."""
    article_dir = edition_path / article_slug

    if not article_dir.exists():
        return {"status": "MISSING", "reason": "folder does not exist"}

    index_file = article_dir / "index.html"
    if not index_file.exists():
        return {"status": "MISSING", "reason": "index.html does not exist"}

    # Read index.html to check for placeholder
    with open(index_file) as f:
        content = f.read()

    has_placeholder = "placeholder-notice" in content or "[Article text coming soon]" in content

    # Count image files
    images = list(article_dir.glob("*.jpg")) + list(article_dir.glob("*.jpeg")) + \
             list(article_dir.glob("*.png")) + list(article_dir.glob("*.gif"))
    image_count = len(images)

    # Determine status
    if has_placeholder:
        if image_count > 0:
            return {"status": "IN PROGRESS", "reason": "placeholder text, photos ready"}
        else:
            return {"status": "PLACEHOLDER", "reason": "no content, no photos"}
    else:
        # Has real content
        if image_count > 0:
            return {"status": "READY", "reason": f"content + {image_count} photos", "photos": image_count}
        else:
            return {"status": "TEXT ONLY", "reason": "content but no photos"}

def verify_edition(edition_date):
    """Verify all articles in an edition."""
    edition_path = Path(f"editions/{edition_date}")

    if not edition_path.exists():
        print(f"❌ Edition {edition_date} not found")
        return False

    # Get all article folders
    articles = sorted([d.name for d in edition_path.iterdir() if d.is_dir()])

    if not articles:
        print(f"❌ No articles found in {edition_path}")
        return False

    # Check status of each
    results = {}
    status_counts = {
        "READY": 0,
        "TEXT ONLY": 0,
        "IN PROGRESS": 0,
        "PLACEHOLDER": 0,
        "MISSING": 0
    }

    print(f"\n{'='*80}")
    print(f"EDITION STATUS VERIFICATION: {edition_date}")
    print(f"{'='*80}\n")

    for article in articles:
        status_info = check_article_status(edition_path, article)
        status = status_info["status"]
        results[article] = status_info
        status_counts[status] += 1

        symbol = "✓" if status == "READY" else "⚠" if status in ["TEXT ONLY", "IN PROGRESS"] else "✗"

        photos = f" [{status_info.get('photos', 0)} photos]" if "photos" in status_info else ""
        print(f"{symbol} {article:30} | {status:15} | {status_info['reason']}{photos}")

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

    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 tools/verify_edition.py YYYY-MM-DD")
        sys.exit(1)

    edition_date = sys.argv[1]
    verify_edition(edition_date)
