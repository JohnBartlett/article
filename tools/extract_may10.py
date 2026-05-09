#!/usr/bin/env python3
"""Extract photos for May 10 edition from specific Gmail message IDs."""
import sys
sys.path.insert(0, '.')
from tools.extract_article_photos import get_access_token, extract_attachments_from_message, is_image_file
from pathlib import Path

EXTRACTIONS = [
    # (message_id, dest_folder, start_num)
    ("19dfef4437244ade", "editions/2026-05-10/kentucky-derby", 1),
    ("19e030334c08b963", "editions/2026-05-10/train-history-part-three", 1),
    ("19e076e123bb8489", "editions/2026-05-10/anti-cruelty-bonded-pair", 1),
    ("19df8accaf8e9cac", "editions/2026-05-10/guinness-inis-mor", 1),
    ("19dfa2e70402239d", "editions/2026-05-10/ordinary-people", 1),
    ("19dfefe2018f4145", "editions/2026-05-10/newberry-awards", 1),
    ("19ded9bc580a8029", "editions/2026-05-10/intuit-art-party", 1),
    ("19dfcabd66c77031", "editions/2026-05-10/anti-cruelty-bonded-pair", 10),  # extra bonded pair photos from earlier email
    ("19dfa4f275aef132", "editions/2026-05-10/anti-cruelty-bonded-pair", 20),  # another cover photo attempt
]

token = get_access_token()
print("Authenticated.\n")

for msg_id, dest, start_num in EXTRACTIONS:
    folder = Path(dest)
    folder.mkdir(parents=True, exist_ok=True)
    attachments = extract_attachments_from_message(msg_id, token)
    images = [(fn, data) for fn, data in attachments if is_image_file(fn)]
    print(f"{msg_id} → {dest}: {len(images)} images found (of {len(attachments)} attachments)")
    for i, (fn, data) in enumerate(images):
        ext = Path(fn).suffix.lower()
        if ext == '.jpeg':
            ext = '.jpg'
        num = start_num + i
        out = folder / f"photo-{num:02d}{ext}"
        out.write_bytes(data)
        print(f"  Saved {fn} → {out.name}")
    print()
