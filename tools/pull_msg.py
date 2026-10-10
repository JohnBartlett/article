"""Pull one Gmail message locally: plain body, HTML body, all attachments (original filenames).

Usage: pull_msg.py <message-id> <dest-dir>
Prints attachment list, links, italic/bold runs and image sizes. Does not print the body.
"""
import re
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gmail_api import download_attachment, get_access_token, get_body, get_html_body, list_attachments  # noqa: E402


def main(mid: str, dest: Path) -> None:
    (dest / "atts").mkdir(parents=True, exist_ok=True)
    token = get_access_token()
    plain = get_body(token, mid) or ""
    html = get_html_body(token, mid) or ""
    (dest / "plain.txt").write_text(plain)
    (dest / "body.html").write_text(html)
    print(f"plain {len(plain)} chars, html {len(html)} chars, <p> {html.count('<p')}, <div> {html.count('<div')}, <br> {html.count('<br')}")
    for att in list_attachments(token, mid):
        target = dest / "atts" / att["filename"]
        if not target.exists():
            download_attachment(token, mid, att["attachmentId"], str(target))
        info = ""
        try:
            im = Image.open(target)
            info = f"{im.size} exif={im.getexif().get(274)}"
        except Exception:
            pass
        print(f"  ATT {att['filename']!r} {target.stat().st_size:,} {info}")
    print("LINKS:")
    for m in re.finditer(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', html, re.S):
        print("  ", m.group(1)[:110], "|", re.sub(r"<[^>]+>", "", m.group(2))[:60])
    print("EMPHASIS:")
    for tag in ("i", "em", "b", "strong", "u"):
        for m in re.finditer(rf"<{tag}\b[^>]*>(.*?)</{tag}>", html, re.S):
            t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip()
            if t:
                print(f"   <{tag}> {t[:110]}")
    for m in re.finditer(r'style="[^"]*(font-style:\s*italic|font-weight:\s*(?:bold|[6-9]00))', html):
        print("   inline-style:", m.group(1))


if __name__ == "__main__":
    main(sys.argv[1], Path(sys.argv[2]))
