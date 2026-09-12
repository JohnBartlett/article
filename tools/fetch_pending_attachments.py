#!/usr/bin/env python3
"""
tools/fetch_pending_attachments.py — Download contributor email attachments
into a staging area so the hourly Claude cloud routine (which builds article
text via the Gmail MCP connector but cannot download attachments in its
sandbox) can pick them up and place them into the correct article folder.

Runs on a schedule via .github/workflows/fetch-email-attachments.yml, using
the same GMAIL_OAUTH_KEYS/GMAIL_CREDENTIALS secrets already provisioned for
the editors-dashboard refresh workflow.

Idempotent: a message already staged (its _attachment-staging/<msg_id>/
folder exists and is non-empty) is skipped on subsequent runs, so this is
safe to run hourly with an overlapping lookback window.

Usage:
    python3 tools/fetch_pending_attachments.py [--days 14] [--staging-dir _attachment-staging]
"""

import os
import sys
import json
import argparse
import re
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from gmail_api import get_access_token, search_messages, get_metadata, list_attachments, download_attachment

TIER1_SENDERS = [
    "judycbross@aol.com",
    "judycbross@icloud.com",
    "aedelfosse1@gmail.com",
    "anabaca8@gmail.com",
    "emuhl2@uic.edu",
    "muhlemane2@gmail.com",
    "sigalina@aol.com",
    "viccimartin@gmail.com",
]

ATTACHMENT_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff", ".tif", ".pdf", ".docx"}


def is_wanted_attachment(filename):
    return Path(filename).suffix.lower() in ATTACHMENT_EXTENSIONS


def find_current_edition():
    """Most recent edition folder that has a STATUS.md (the active/upcoming one)."""
    editions_dir = Path(__file__).parent.parent / "editions"
    dates = sorted(
        [d.name for d in editions_dir.iterdir() if d.is_dir() and re.match(r"\d{4}-\d{2}-\d{2}$", d.name)],
        reverse=True,
    )
    for d in dates:
        if (editions_dir / d / "STATUS.md").exists():
            return d
    return dates[0] if dates else None


def main():
    parser = argparse.ArgumentParser(description="Stage contributor email attachments for pickup")
    parser.add_argument("--days", type=int, default=14, help="Lookback window in days (default: 14)")
    parser.add_argument("--staging-dir", default="_attachment-staging", help="Staging directory (default: _attachment-staging)")
    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent
    staging_root = repo_root / args.staging_dir
    staging_root.mkdir(exist_ok=True)

    edition = find_current_edition()
    print(f"Active edition (for context only): {edition}")

    token = get_access_token()

    query = f"from:({' OR '.join(TIER1_SENDERS)}) has:attachment newer_than:{args.days}d"
    messages = search_messages(token, query)
    print(f"Found {len(messages)} tier-1 message(s) with attachments in the last {args.days} day(s)")

    staged_count = 0
    skipped_count = 0

    for m in messages:
        msg_id = m["id"]
        msg_dir = staging_root / msg_id

        if msg_dir.exists() and any(msg_dir.iterdir()):
            skipped_count += 1
            continue

        attachments = list_attachments(token, msg_id)
        wanted = [a for a in attachments if is_wanted_attachment(a["filename"])]
        if not wanted:
            continue

        meta = get_metadata(token, msg_id)
        msg_dir.mkdir(exist_ok=True)

        saved = []
        for a in wanted:
            dest = msg_dir / a["filename"]
            if dest.exists():
                continue
            download_attachment(token, msg_id, a["attachmentId"], str(dest))
            saved.append(a["filename"])
            print(f"  staged: {msg_id}/{a['filename']}")

        (msg_dir / "meta.json").write_text(json.dumps({
            "message_id": msg_id,
            "from": meta.get("From"),
            "subject": meta.get("Subject"),
            "date": meta.get("Date"),
            "files": saved,
        }, indent=2))

        staged_count += 1

    print(f"\nStaged {staged_count} new message(s); skipped {skipped_count} already-staged message(s).")


if __name__ == "__main__":
    main()
