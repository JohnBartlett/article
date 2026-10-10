"""Download one Google Drive file by id, keeping its Drive filename.

Usage: fetch_drive.py <file-id> <dest-dir>
"""
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gmail_api import get_access_token  # noqa: E402


def main(file_id: str, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    headers = {"Authorization": f"Bearer {get_access_token()}"}
    base = f"https://www.googleapis.com/drive/v3/files/{file_id}"
    meta = requests.get(base, headers=headers, params={"fields": "name,size,mimeType", "supportsAllDrives": "true"}, timeout=60)
    print("meta:", meta.status_code, meta.text[:300])
    meta.raise_for_status()
    name = meta.json()["name"]
    data = requests.get(base, headers=headers, params={"alt": "media", "supportsAllDrives": "true"}, timeout=300)
    data.raise_for_status()
    target = dest / name
    target.write_bytes(data.content)
    print(f"saved {name}  {target.stat().st_size:,} bytes")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], Path(sys.argv[2]))
