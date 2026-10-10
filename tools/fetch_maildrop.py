"""Download the PDF Mail Drop attachments linked in Jill's emails.

Usage: fetch_maildrop.py <dest-dir> <message-id> [<message-id> ...]
"""
import re
import sys
from pathlib import Path
from urllib.parse import parse_qs, quote, urlparse

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gmail_api import get_access_token, get_body, get_html_body  # noqa: E402


def direct_url(link: str) -> tuple[str, str]:
    q = parse_qs(urlparse(link).query)
    name = q["f"][0]
    url = q["u"][0].replace("${f}", quote(name)).replace("${uk}", q["uk"][0])
    return name, url


def main(dest: Path, msg_ids: list[str]) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    token = get_access_token()
    seen = set()
    for mid in msg_ids:
        text = (get_html_body(token, mid) or "") + "\n" + (get_body(token, mid) or "")
        links = re.findall(r'https://www\.icloud\.com/attachment/\?[^\s"<>]+', text.replace("&amp;", "&"))
        for link in links:
            name, url = direct_url(link)
            if not name.lower().endswith(".pdf") or url in seen:
                continue
            seen.add(url)
            r = requests.get(url, timeout=300)
            target = dest / f"{mid}__{name}"
            if r.ok and r.content[:4] == b"%PDF":
                target.write_bytes(r.content)
                print(f"saved {target.name}  {len(r.content):,} bytes")
            else:
                print(f"FAILED {name}: HTTP {r.status_code}, {len(r.content)} bytes")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    main(Path(sys.argv[1]), sys.argv[2:])
