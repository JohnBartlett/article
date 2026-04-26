#!/usr/bin/env python3
"""
Download photos from Google Drive for article folders.

This script downloads photos from Google Drive file IDs and organizes them
into the appropriate article folders.

Usage:
    python3 tools/download_drive_photos.py [--edition YYYY-MM-DD]

Example:
    python3 tools/download_drive_photos.py --edition 2026-04-26
"""

import sys
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

# Google Drive file mappings
DRIVE_FILES = {
    'second-presbyterian': {
        'photo-01': '1uqvh2-hSX8KUxK4fyFoX3gfA3Yuowti1',
        'photo-02': '1HuvJ0eCPlt6BQTcNXh7BAAqMRPN1CaPA',
        'photo-03': '1_y9HQmSqBm8v9p3Xq67YFo-NINksfR1i',
        'photo-04': '1NnpZ-0VnXbB3epAB-6m9UlQtMsxTDjW0',
        'photo-05': '1PWICyTPS6wa26pTHX5Ik8yhSy_Xpxh7L',
        'photo-06': '1-MyKF6g8VaFF871Uwkx4tEpSoPOGLnba',
        'photo-07': '1cHMCutMbT-Aqf7-CddEYZa2VWXHp1ADi',
        'photo-08': '15bq3-nPv2MpKUTFiwVqkVKxdvVX4Wr3e',
    },
    'rush-hospital': {
        'photo-09': '1e0a60gRp-X80ZGmY_ZgM2wEl9XQOfpdM',
        'photo-10': '13nMJ88lM7IDogXxdk8ZBC9ogL6Eb7Afj',
        'photo-11': '1KpKKswF39lgyEIPjGYajcWTya7PtKib4',
        'photo-12': '1HjWPFHG20B_mao33ppMHLyR6e1rwY6n9',
    }
}


def is_valid_jpeg(filepath):
    """Check if file is a valid JPEG."""
    try:
        with open(filepath, 'rb') as f:
            # Check JPEG magic bytes
            return f.read(2) == b'\xff\xd8'
    except (IOError, OSError):
        return False


def download_photo(file_id, output_path, max_retries=3):
    """
    Download a photo from Google Drive.

    Args:
        file_id: Google Drive file ID
        output_path: Path to save the file
        max_retries: Number of download attempts

    Returns:
        bool: True if successful, False otherwise
    """
    url = f"https://drive.google.com/uc?export=download&id={file_id}"

    for attempt in range(max_retries):
        try:
            # Use curl to download
            result = subprocess.run(
                ['curl', '-s', '-L', url, '-o', str(output_path)],
                capture_output=True,
                timeout=30,
                check=False
            )

            # Verify the file is a valid JPEG
            if output_path.exists():
                if is_valid_jpeg(output_path):
                    return True
                else:
                    # File exists but isn't a JPEG (probably HTML redirect)
                    output_path.unlink()
                    if attempt < max_retries - 1:
                        print(f"  ⚠ Attempt {attempt + 1}: Downloaded file was not a JPEG, retrying...")
                    continue
            else:
                if attempt < max_retries - 1:
                    print(f"  ⚠ Attempt {attempt + 1}: Download failed, retrying...")
                continue

        except subprocess.TimeoutExpired:
            print(f"  ⚠ Attempt {attempt + 1}: Download timeout, retrying...")
            continue
        except Exception as e:
            print(f"  ⚠ Attempt {attempt + 1}: Error - {e}")
            continue

    return False


def main():
    parser = argparse.ArgumentParser(
        description='Download photos from Google Drive for article folders'
    )
    parser.add_argument(
        '--edition',
        default='2026-04-26',
        help='Edition date in YYYY-MM-DD format (default: 2026-04-26)'
    )
    args = parser.parse_args()

    # Validate edition date format
    try:
        datetime.strptime(args.edition, '%Y-%m-%d')
    except ValueError:
        print(f"Error: Invalid date format '{args.edition}'. Use YYYY-MM-DD")
        sys.exit(1)

    edition_path = Path('editions') / args.edition

    if not edition_path.exists():
        print(f"Error: Edition directory not found: {edition_path}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"Downloading Google Drive Photos for {args.edition}")
    print(f"{'='*60}\n")

    total_attempted = 0
    total_success = 0
    total_failed = 0

    # Download photos for each article
    for article_name, photos in DRIVE_FILES.items():
        article_path = edition_path / article_name

        if not article_path.exists():
            print(f"⚠ Skipping {article_name}: folder not found")
            continue

        print(f"\n{article_name}:")
        article_success = 0

        for photo_name, file_id in photos.items():
            total_attempted += 1
            output_file = article_path / f"{photo_name}.jpg"

            print(f"  Downloading {photo_name}...", end=" ", flush=True)

            if download_photo(file_id, output_file):
                file_size = output_file.stat().st_size / (1024 * 1024)  # Size in MB
                print(f"✓ ({file_size:.1f} MB)")
                article_success += 1
                total_success += 1
            else:
                print(f"✗ Failed")
                total_failed += 1
                if output_file.exists():
                    output_file.unlink()

        print(f"  {article_name}: {article_success}/{len(photos)} photos")

    # Summary
    print(f"\n{'='*60}")
    print(f"Download Summary")
    print(f"{'='*60}")
    print(f"Total attempted: {total_attempted}")
    print(f"Successful: {total_success}")
    print(f"Failed: {total_failed}")
    print(f"Success rate: {(total_success/total_attempted*100):.0f}%\n")

    if total_failed > 0:
        print("\n⚠ DOWNLOAD ISSUE DETECTED")
        print("="*60)
        print("\nThe Google Drive file IDs are SHORTCUTS, not actual image files.")
        print("Shortcuts download as HTML redirects, not JPEGs.\n")
        print("SOLUTION: Manually download photos from Google Drive folders:\n")
        print("Option 1 - Direct Drive Access (Fastest):")
        print("  1. Visit Google Drive")
        print("  2. Find the PHOTO folders/files")
        print("  3. Right-click → Download → Save to:")
        print(f"     editions/{args.edition}/second-presbyterian/")
        print(f"     editions/{args.edition}/rush-hospital/\n")
        print("Option 2 - Use Drive Links:")
        print("  See: tools/DRIVE_PHOTOS.md for all file IDs\n")
        print("Option 3 - Ask for actual image files:")
        print("  The file IDs we have point to shortcuts.")
        print("  Request the actual image file IDs from contributors.\n")

    return 0 if total_failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
