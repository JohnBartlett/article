#!/usr/bin/env python3
"""
Extract article photos from contributor emails and organize by article folder.

This script extracts attachment photos from Gmail messages sent by contributors
(Ana Baca, Annie Delfosse, Emma Muhleman, etc.) and saves them to the appropriate
article folders in editions/YYYY-MM-DD/.

Can be used as a CLI tool or imported as a module by other scripts.

Usage (CLI):
    python3 tools/extract_article_photos.py 2026-04-26
    python3 tools/extract_article_photos.py 2026-04-26 --contributor ana

Usage (as module):
    from tools.extract_article_photos import extract_photos_from_emails
    files = extract_photos_from_emails(edition="2026-04-26", output_dir="editions/2026-04-26")
"""

import os
import sys
import json
import base64
import email
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
import requests


# Gmail credentials location
GMAIL_MCP_CREDS = os.path.expanduser("~/.gmail-mcp/credentials.json")
GMAIL_MCP_KEYS = os.path.expanduser("~/.gmail-mcp/gcp-oauth.keys.json")

# Email message IDs for article contributions
# Format: {"contributor_name": ("email@example.com", "message_id")}
ARTICLE_EMAIL_MAP = {
    'ana': {
        'email': 'anabaca8@gmail.com',
        'messages': [
            '19dc1876654b519e',  # Doris Kearns Goodwin / Rush Hospital
            '19dc12e149013b93',  # Chicago: An Express Train History
        ],
        'articles': ['rush-hospital', 'trains-chicago'],
    },
    'annie': {
        'email': 'aedelfosse1@gmail.com',
        'messages': [
            '19dc4c8ba211a68d',  # Most recent Annie message
        ],
        'articles': ['second-presbyterian'],
    },
    'emma': {
        'email': 'muhlemane2@gmail.com',
        'messages': [],
        'articles': [],
    },
}


def get_access_token():
    """Get a fresh Gmail API access token."""
    try:
        with open(GMAIL_MCP_CREDS) as f:
            creds = json.load(f)
        with open(GMAIL_MCP_KEYS) as f:
            keys = json.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"Gmail credentials not found. Please authenticate first.\n"
            f"Missing: {e.filename}"
        )

    web = keys.get("web") or keys.get("installed") or {}
    client_id = web.get("client_id")
    client_secret = web.get("client_secret")

    if not client_id or not client_secret:
        raise ValueError("Invalid Gmail credentials file")

    resp = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": creds["refresh_token"],
            "grant_type": "refresh_token",
        },
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def extract_attachments_from_message(message_id: str, token: str) -> List[Tuple[str, bytes]]:
    """
    Extract all attachments from a Gmail message.

    Args:
        message_id: Gmail message ID
        token: Gmail API access token

    Returns:
        List of (filename, content) tuples
    """
    url = f"https://www.googleapis.com/gmail/v1/users/me/messages/{message_id}?format=raw"
    headers = {"Authorization": f"Bearer {token}"}

    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()

    raw = base64.urlsafe_b64decode(resp.json()["raw"])
    msg = email.message_from_bytes(raw)

    attachments = []
    for part in msg.walk():
        filename = part.get_filename()
        if not filename:
            continue

        data = part.get_payload(decode=True)
        if not data:
            continue

        attachments.append((filename, data))

    return attachments


def is_image_file(filename: str) -> bool:
    """Check if file is an image."""
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
    ext = Path(filename).suffix.lower()
    return ext in image_extensions


def extract_photos_from_emails(
    edition: str,
    output_dir: str = None,
    contributors: List[str] = None,
) -> Dict[str, List[str]]:
    """
    Extract photo attachments from contributor emails.

    Args:
        edition: Edition date (e.g., "2026-04-26")
        output_dir: Output directory (default: editions/{edition})
        contributors: List of contributors to extract from (default: all)

    Returns:
        Dict mapping article names to lists of saved files
    """
    if output_dir is None:
        output_dir = f"editions/{edition}"

    output_path = Path(output_dir)
    if not output_path.exists():
        raise FileNotFoundError(f"Edition directory not found: {output_dir}")

    # Get access token
    print("Authenticating with Gmail API...")
    try:
        token = get_access_token()
    except Exception as e:
        print(f"Error: {e}")
        return {}

    results = {}

    # Filter contributors if specified
    contributors_to_process = {
        k: v
        for k, v in ARTICLE_EMAIL_MAP.items()
        if not contributors or k in contributors
    }

    print(f"\nExtracting photos from {len(contributors_to_process)} contributor(s)...\n")

    for contributor, info in contributors_to_process.items():
        print(f"{contributor}:")
        results[contributor] = []

        for msg_id, article in zip(info["messages"], info["articles"]):
            article_path = output_path / article
            article_path.mkdir(exist_ok=True)

            print(f"  {article}:")

            try:
                attachments = extract_attachments_from_message(msg_id, token)

                photo_count = 0
                for filename, content in attachments:
                    if not is_image_file(filename):
                        continue

                    # Save with normalized name
                    ext = Path(filename).suffix.lower()
                    photo_count += 1
                    output_file = article_path / f"photo-{photo_count:02d}{ext}"

                    with open(output_file, "wb") as f:
                        f.write(content)

                    size_mb = len(content) / (1024 * 1024)
                    print(f"    ✓ {output_file.name} ({size_mb:.1f} MB)")
                    results[contributor].append(str(output_file))

                if photo_count == 0:
                    print(f"    ⚠ No image attachments found")

            except requests.exceptions.HTTPError as e:
                print(f"    ✗ HTTP Error: {e}")
            except Exception as e:
                print(f"    ✗ Error: {e}")

        if not results[contributor]:
            del results[contributor]

    # Summary
    total_files = sum(len(v) for v in results.values())
    print(f"\n{'='*60}")
    print(f"Extracted {total_files} photo(s) to {output_dir}")
    print(f"{'='*60}\n")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Extract article photos from contributor emails"
    )
    parser.add_argument(
        "edition",
        help="Edition date (e.g., 2026-04-26)",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output directory (default: editions/{edition})",
    )
    parser.add_argument(
        "--contributor",
        "-c",
        action="append",
        help="Specific contributor(s) to extract from (can be used multiple times)",
    )

    args = parser.parse_args()

    output_dir = args.output or f"editions/{args.edition}"

    try:
        results = extract_photos_from_emails(
            edition=args.edition,
            output_dir=output_dir,
            contributors=args.contributor,
        )
        sys.exit(0 if results else 1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
