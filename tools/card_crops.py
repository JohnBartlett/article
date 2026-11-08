#!/usr/bin/env python3
"""Simulate how the homepage crops each card and hero photo (CLAUDE.md mistake #86).

Cards are 300 px tall with object-fit: cover, so landscape group photos lose heads as
well as portraits. This renders every card/hero of an edition at the widths readers
see and writes one contact sheet per image, so faces can be checked by eye before
staging.

usage: python3 tools/card_crops.py YYYY-MM-DD [--out DIR]
Prints each image with its object-position and the contact-sheet path.
"""
from __future__ import annotations

import argparse
import html
import os
import re
import sys
import tempfile
from urllib.parse import unquote

from PIL import Image, ImageDraw, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# (label, box width, box height) as rendered by index.html's CSS
CARD_BOXES = [('phone 330', 330, 300), ('phone 480', 480, 300), ('desktop 2-col 545', 545, 300), ('tablet 660', 660, 300)]
HERO_BOXES = [('phone 360', 360, 320), ('tablet 800', 800, 440), ('desktop 1140', 1140, 560)]


def parse_position(style: str) -> tuple[float, float]:
    """object-position -> (x, y) fractions. Supports keywords and percentages."""
    m = re.search(r'object-position:\s*([^;"]+)', style or '')
    if not m:
        return 0.5, 0.5
    words = m.group(1).split()
    kw = {'left': 0.0, 'top': 0.0, 'center': 0.5, 'right': 1.0, 'bottom': 1.0}
    vals = []
    for w in words[:2]:
        if w.endswith('%'):
            vals.append(float(w[:-1]) / 100)
        elif w in kw:
            vals.append(kw[w])
    if len(words) == 1:  # a single keyword like "top" sets y only when it is top/bottom
        if words[0] in ('top', 'bottom'):
            return 0.5, kw[words[0]]
        return (vals[0] if vals else 0.5), 0.5
    if words and words[0] in ('top', 'bottom'):  # "top center" form
        vals = vals[::-1]
    return (vals + [0.5, 0.5])[0], (vals + [0.5, 0.5])[1]


def cover_crop(im: Image.Image, bw: int, bh: int, px: float, py: float) -> Image.Image:
    scale = max(bw / im.width, bh / im.height)
    w, h = round(im.width * scale), round(im.height * scale)
    r = im.resize((w, h))
    x, y = round((w - bw) * px), round((h - bh) * py)
    return r.crop((x, y, x + bw, y + bh))


def sheet(im: Image.Image, boxes, px: float, py: float, title: str) -> Image.Image:
    tiles = []
    for label, bw, bh in boxes:
        c = cover_crop(im, bw, bh, px, py)
        f = 330 / max(bw, 330) if bw > 660 else 1  # keep the sheet a readable size
        c = c.resize((round(bw * f), round(bh * f)))
        t = Image.new('RGB', (c.width, c.height + 18), 'white')
        t.paste(c, (0, 18))
        ImageDraw.Draw(t).text((2, 3), label, fill='black')
        tiles.append(t)
    W = sum(t.width for t in tiles) + 10 * (len(tiles) - 1)
    H = max(t.height for t in tiles) + 20
    s = Image.new('RGB', (W, H), 'white')
    ImageDraw.Draw(s).text((2, 3), title[:120], fill='black')
    x = 0
    for t in tiles:
        s.paste(t, (x, 20))
        x += t.width + 10
    return s


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('date')
    ap.add_argument('--out', default=os.path.join(tempfile.gettempdir(), 'card_crops'))
    a = ap.parse_args()
    out = os.path.join(a.out, a.date)
    os.makedirs(out, exist_ok=True)
    page = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
    imgs = re.findall(r'<img\s+class="(hero|card)-image"([^>]*)>', page)
    n = 0
    for kind, attrs in imgs:
        src = re.search(r'src="([^"]+)"', attrs)
        if not src or f'editions/{a.date}/' not in src.group(1):
            continue
        rel = unquote(html.unescape(src.group(1)))
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            print(f'MISSING {rel}')
            continue
        style = (re.search(r'style="([^"]*)"', attrs) or [None, ''])[1]
        px, py = parse_position(style)
        im = ImageOps.exif_transpose(Image.open(path)).convert('RGB')
        boxes = HERO_BOXES if kind == 'hero' else CARD_BOXES
        name = re.sub(r'[^A-Za-z0-9]+', '_', rel.split(f'{a.date}/')[1])[:80] + '.png'
        sheet(im, boxes, px, py, f'{kind}: {rel}  object-position {px:.0%} {py:.0%}').save(os.path.join(out, name))
        orient = 'portrait' if im.height > im.width else 'landscape'
        print(f'{kind:5} {orient:9} pos {px:.0%} {py:.0%}  {rel}\n      -> {os.path.join(out, name)}')
        n += 1
    print(f'{n} images. Open each sheet and confirm no heads are cut; if they are, add '
          f'style="object-position: center NN%;" to that <img> in index.html and re-run.')
    return 0 if n else 1


if __name__ == '__main__':
    sys.exit(main())
