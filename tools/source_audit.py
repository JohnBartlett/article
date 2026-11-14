#!/usr/bin/env python3
"""Audit an edition's built articles against their original sources (CLAUDE.md mistake #84).

For each article listed in the edition STATUS.md "## Sources" section:
  - fetches every listed Gmail message fresh (format=full): HTML and plain bodies, attachments
  - downloads Drive-linked photos found in the source HTML (Drive REST API, Gmail token)
  - picks the source text: the HTML body unless the plain text or an attached PDF is much
    longer (forwarded plain-text forms, PDF-only articles)
  - word-level diff of built article text (body + captions) against the source
  - paragraph breaks lost in the build
  - italic/bold phrases (from the HTML body, or from the PDF via pdftohtml -xml)
  - links: count, targets and anchors
  - title and byline as built (compare by eye against the diff's first lines)
  - every figure: caption, and which source image it matches (image fingerprint, #68)

STATUS.md format (first ID = text source; later IDs = extra photo/caption emails):
    ## Sources
    - friends-of-prentice: 1a1b5080fb9057bd, 1a1a335b0abdf363
    - jill-lowe-ice-cream: 1a187835ee3989b1

usage: .venv/bin/python tools/source_audit.py YYYY-MM-DD [--only slug] [--out DIR]
Read-only: it reports; it never edits an article. Expected differences to ignore:
layout markers ([PHOTO 1 - caption: ...], "Photo One: ..., Caption:"), bracketed URLs
turned into links, email headers/signatures, and typo fixes the editor approved.
"""
from __future__ import annotations

import argparse
import base64
import difflib
import glob
import html as H
import os
import re
import subprocess
import sys
import tempfile
import unicodedata
from urllib.parse import unquote, urlsplit

import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
sys.path.insert(0, os.path.expanduser('~/.claude/scripts'))
from mailhtml import blocks  # noqa: E402

GMAIL = 'https://gmail.googleapis.com/gmail/v1/users/me/messages'
IMG_EXT = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.heic')


# ----------------------------------------------------------------- fetching
def token() -> str:
    from gmail_api import get_access_token
    return get_access_token()


def fetch_message(mid: str, d: str, hdr: dict) -> dict:
    os.makedirs(f'{d}/atts', exist_ok=True)
    m = requests.get(f'{GMAIL}/{mid}', headers=hdr, params={'format': 'full'}, timeout=60).json()
    if 'payload' not in m:
        raise SystemExit(f'cannot fetch {mid}: {m}')
    heads = {h['name']: h['value'] for h in m['payload']['headers']}
    info = {'id': mid, 'from': heads.get('From'), 'subject': heads.get('Subject'), 'html': '', 'text': '', 'atts': []}

    def walk(p):
        yield p
        for q in p.get('parts', []) or []:
            yield from walk(q)

    seen = {}
    for p in walk(m['payload']):
        fn, body, mt = p.get('filename'), p.get('body', {}), p.get('mimeType')
        if fn:
            n = seen.get(fn, 0)
            seen[fn] = n + 1
            name = fn if n == 0 else f'{os.path.splitext(fn)[0]} ({n}){os.path.splitext(fn)[1]}'
            data = body.get('data') or requests.get(f"{GMAIL}/{mid}/attachments/{body['attachmentId']}",
                                                    headers=hdr, timeout=120).json()['data']
            raw = base64.urlsafe_b64decode(data)
            open(f'{d}/atts/{name}', 'wb').write(raw)
            info['atts'].append(name)
        elif mt in ('text/html', 'text/plain') and body.get('data'):
            t = base64.urlsafe_b64decode(body['data']).decode('utf-8', 'replace')
            info['html' if mt == 'text/html' else 'text'] += t + '\n'
    return info


def fetch_drive_links(src_html: str, d: str, hdr: dict) -> list[str]:
    got = []
    os.makedirs(f'{d}/drive', exist_ok=True)
    for fid in dict.fromkeys(re.findall(r'drive\.google\.com/file/d/([A-Za-z0-9_-]+)', src_html)):
        meta = requests.get(f'https://www.googleapis.com/drive/v3/files/{fid}', headers=hdr,
                            params={'fields': 'name,mimeType'}, timeout=60)
        if meta.status_code != 200:
            print(f'  ! Drive {fid}: {meta.status_code} (not shared with John?)')
            continue
        name = meta.json()['name']
        if not name.lower().endswith(IMG_EXT):
            continue
        p = f'{d}/drive/{name}'
        if not os.path.exists(p):
            r = requests.get(f'https://www.googleapis.com/drive/v3/files/{fid}', headers=hdr,
                             params={'alt': 'media'}, timeout=300)
            if r.status_code != 200:
                print(f'  ! Drive download {name}: {r.status_code}')
                continue
            open(p, 'wb').write(r.content)
        got.append(p)
    return got


# ----------------------------------------------------------------- text
def norm(t: str) -> str:
    t = unicodedata.normalize('NFC', t.replace('\xa0', ' ').replace('​', '').replace(' ', ' ').replace('￼', ''))
    return re.sub(r'\s+', ' ', t).strip()


def text_to_html(t: str) -> str:
    t = re.sub(r'^\s*>+ ?', '', t, flags=re.M)  # forwarded-quote markers
    return ''.join(f'<p>{H.escape(p)}</p>' for p in re.split(r'\n\s*\n', t))


def pdf_source(pdf: str) -> str:
    """PDF -> HTML paragraphs with <b>/<i>/<a> kept, from pdftohtml's positioned XML.

    Style comes from each run's font name (Bold, Italic, BoldItalic, Oblique), because
    pdftohtml tags bold-italic runs as <b> only. A new paragraph starts at a vertical gap
    larger than 1.6 line heights or at a page break.
    """
    xml = subprocess.run(['pdftohtml', '-xml', '-i', '-q', '-stdout', pdf], capture_output=True, text=True).stdout
    full = re.findall(r'^(\S+)', subprocess.run(['pdffonts', pdf], capture_output=True, text=True).stdout, flags=re.M)[2:]
    fonts = {}
    for fid, fam in re.findall(r'<fontspec id="(\d+)"[^>]*family="([^"]*)"', xml):
        fonts[fid] = next((n for n in full if n.startswith(fam)), fam)  # pdftohtml drops "-BoldItalicMT"
    paras, cur, prev = [], [], None
    for pg, body in re.findall(r'<page number="(\d+)"[^>]*>(.*?)</page>', xml, flags=re.S):
        items = []
        for top, left, width, height, font, inner in re.findall(
                r'<text top="(-?\d+)" left="(-?\d+)" width="(\d+)" height="(\d+)" font="(\d+)">(.*?)</text>', body, flags=re.S):
            items.append((int(top), int(left), int(width), int(height), font, inner))
        items.sort(key=lambda x: (x[0], x[1]))
        right = None
        for top, left, width, height, font, inner in items:
            fam = fonts.get(font, '')
            inner = re.sub(r'</?[bi]>', '', inner)
            if re.search(r'italic|oblique', fam, re.I):
                inner = f'<i>{inner}</i>'
            if re.search(r'bold|black|heavy', fam, re.I):
                inner = f'<b>{inner}</b>'
            glue = True
            if prev is not None:
                ptop, pheight, ppg = prev
                if ppg != pg or top - ptop > 1.6 * max(pheight, height):
                    paras.append(cur); cur = []
                elif abs(top - ptop) > 3:
                    cur.append('\n')
                elif right is not None and left - right < 0.2 * height and cur:
                    cur[-1] = cur[-1] + inner  # same line, touching: no space between pieces
                    glue = False
            if glue:
                cur.append(inner)
            prev = (top, height, pg)
            right = left + width
    if cur:
        paras.append(cur)
    out = []
    for p in paras:
        t = ' '.join(x for x in p if x != '\n')
        t = re.sub(r'(\w)- +(\w)', r'\1-\2', t)  # line-end hyphen splits ("ice- cream")
        out.append(f'<p>{t}</p>')
    return ''.join(out)


def links_of(bl):
    out = []
    for b in bl:
        cur, h = '', None
        for r in b.runs + [('', False, False, None)]:
            if r[3] != h:
                if h:
                    out.append((norm(cur), h))
                cur, h = '', r[3]
            cur += r[0]
    return out


def lkey(h):
    u = urlsplit(H.unescape(h))
    return (u.netloc.lower().removeprefix('www.') + unquote(u.path).rstrip('/')).lower()


ZAP = dict.fromkeys(map(ord, '\u200b\ufffc\u00ad'), None)


def tokens(bl):
    """[(word, block_index, bold, italic, href)] from mailhtml blocks; a word takes the style of its first letter."""
    out = []
    for bi, b in enumerate(bl):
        chars = []
        for t, bo, it, h in b.runs:
            t = unicodedata.normalize('NFC', t).translate(ZAP).replace('\xa0', ' ').replace('\u202f', ' ')
            chars += [(c, bo, it, h) for c in t]
        word, flags = '', None
        for c, bo, it, h in chars + [(' ', False, False, None)]:
            if c.isspace():
                if word:
                    out.append((word, bi, flags[0], flags[1], flags[2]))
                word, flags = '', None
            else:
                if flags is None or (not word.strip('“”"‘’\'([') and c.isalnum()):
                    flags = (bo, it, h)
                word += c
    return out


def styled_built(html_: str) -> str:
    """Built body with caption italics (CSS) and heading bold made explicit for comparison."""
    soup = BeautifulSoup(html_, 'html.parser')
    for c in soup.find_all(class_='feedback-widget'):
        c.decompose()
    for cap in soup.find_all('figcaption'):
        a = soup.new_tag('a', href='#caption')
        for ch in list(cap.children):
            a.append(ch.extract())
        cap.append(a)
    for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        inner = soup.new_tag('b')
        for ch in list(h.children):
            inner.append(ch.extract())
        h.append(inner)
    return str(soup)


# ----------------------------------------------------------------- images
def fp(path):
    im = ImageOps.exif_transpose(Image.open(path)).convert('L').resize((20, 20))
    return list(im.getdata())


def dist(a, b):
    return sum(abs(x - y) for x, y in zip(a, b)) / len(a)


# ----------------------------------------------------------------- audit
def audit(slug: str, ids: list[str], ed: str, out: str, hdr: dict) -> None:
    d = f'{out}/{slug}'
    os.makedirs(d, exist_ok=True)
    msgs = [fetch_message(mid, f'{d}/{mid}', hdr) for mid in ids]
    main = msgs[0]
    page = open(f'{ROOT}/editions/{ed}/{slug}/index.html', encoding='utf-8').read()
    soup = BeautifulSoup(page, 'html.parser')
    body_el = soup.find(class_='article-body')
    print(f'\n{"=" * 78}\n{slug}')
    for m in msgs:
        print(f'  source {m["id"]}: {m["from"]} | {m["subject"]} | attachments: {", ".join(m["atts"]) or "none"}')
    t = soup.find('h1', class_='article-title')
    sub = soup.find(class_='article-subtitle')
    print(f'  BUILT TITLE: {t.get_text(" ", strip=True) if t else "?"}' + (f'  | SUBTITLE: {sub.get_text(" ", strip=True)}' if sub else ''))
    meta = soup.find(class_='article-meta')
    print(f'  BUILT BYLINE: {meta.get_text(" ", strip=True) if meta else "?"}')

    # choose source text
    pdfs = [f'{d}/{main["id"]}/atts/{a}' for a in main['atts'] if a.lower().endswith('.pdf')]
    cands = []
    if main['html'].strip():
        cands.append(('HTML body', main['html']))
    if main['text'].strip():
        cands.append(('plain-text body', text_to_html(main['text'])))
    pdf_html = pdf_source(pdfs[0]) if pdfs else None
    if pdf_html:
        cands.append((f'PDF {os.path.basename(pdfs[0])}', pdf_html))
    words = {lab: len(norm(' '.join(b.text for b in blocks(h))).split()) for lab, h in cands}
    best = max(words.values()) if words else 0
    lab, src_html = next(((l, h) for l, h in cands if l == 'HTML body' and words[l] >= 0.8 * best),
                         max(cands, key=lambda c: words[c[0]]))
    print(f'  TEXT SOURCE: {lab} ({words[lab]} words; candidates {words})')

    SB, BB = blocks(src_html), blocks(styled_built(str(body_el)))
    st, bt = tokens(SB), tokens(BB)
    sw, bw = [x[0] for x in st], [x[0] for x in bt]
    sm = difflib.SequenceMatcher(None, sw, bw, autojunk=False)
    ops = sm.get_opcodes()
    print(f'\n  --- TEXT DIFFS, source -> built ({len(sw)} vs {len(bw)} words) ---')
    nd = 0
    for op, i1, i2, j1, j2 in ops:
        if op == 'equal':
            continue
        nd += 1
        s_, b_ = ' '.join(sw[i1:i2]), ' '.join(bw[j1:j2])
        s_ = s_ if len(s_) < 300 else s_[:150] + ' … ' + s_[-120:]
        b_ = b_ if len(b_) < 300 else b_[:150] + ' … ' + b_[-120:]
        print(f'  [{op}] after «…{" ".join(sw[max(0, i1 - 6):i1])[-60:]}»\n      SRC «{s_}»\n      OUT «{b_}»')
    if not nd:
        print('  ✓ identical')

    a2b = {}
    for op, i1, i2, j1, j2 in ops:
        if op == 'equal':
            a2b.update({i1 + k: j1 + k for k in range(i2 - i1)})
    print('\n  --- PARAGRAPH BREAKS LOST IN BUILD ---')
    sstarts = [k for k in range(1, len(st)) if st[k][1] != st[k - 1][1]]
    bstarts = {k for k in range(1, len(bt)) if bt[k][1] != bt[k - 1][1]}
    lost = [k for k in sstarts if k in a2b and (k - 1) in a2b and a2b[k] not in bstarts]
    for k in lost:
        print('  before «' + ' '.join(sw[k:k + 10]) + '»')
    if not lost:
        print('  ✓ none')

    # formatting, word by word on aligned text (labels, headers, edits and captions are not compared)
    sflags = [[x[2], x[3]] for x in st]
    fmt_from = 'source text'
    if pdf_html and not lab.startswith('PDF') and not any(b or i for b, i in sflags):
        pt = tokens(blocks(pdf_html))  # take styles from the PDF, aligned word by word
        pm = difflib.SequenceMatcher(None, sw, [x[0] for x in pt], autojunk=False)
        sflags = [[False, False] for _ in st]
        for op, i1, i2, j1, j2 in pm.get_opcodes():
            if op == 'equal':
                for k in range(i2 - i1):
                    sflags[i1 + k] = [pt[j1 + k][2], pt[j1 + k][3]]
        fmt_from = 'PDF'
    cap_blocks = {x[1] for x in bt if x[4] == '#caption'}
    for name, idx in (('BOLD', 0), ('ITALIC', 1)):
        diffs, cur = [], None
        for k in sorted(a2b):
            j = a2b[k]
            if not re.search(r'\w', sw[k]) or bt[j][1] in cap_blocks:
                continue
            sv, bv = sflags[k][idx], bt[j][2 + idx]
            kind = None if sv == bv else ('in source, not in build' if sv else 'in build, not in source')
            if kind and cur and cur[0] == kind and cur[2] == k - 1:
                cur[1].append(sw[k]); cur[2] = k
            elif kind:
                cur = [kind, [sw[k]], k]; diffs.append(cur)
            else:
                cur = None
        print(f'\n  --- {name} (from {fmt_from}), compared word by word ---')
        for kind, ws, _ in diffs:
            print(f'  {kind}: «{" ".join(ws)[:110]}»')
        if not diffs:
            print('  ✓ match')
    print('  (captions skipped: the site sets them in italic by CSS)')

    src_links = links_of(SB)
    brk = r'\[\s*((?:https?://)?[a-z0-9.-]+\.[a-z]{2,}/[^\]\s]*)\s*\]'
    for b in SB:
        for u in re.findall(brk, b.text):
            src_links.append(('(bracketed URL in text)', u if u.startswith('http') else 'https://' + u))
    src_links = [l for l in src_links if not l[1].startswith('mailto:') and 'mail.google' not in l[1]
                 and 'drive.google.com' not in l[1]]
    bl = [l for l in links_of(BB) if not l[1].startswith(('mailto:', '../', '#'))]
    print(f'\n  --- LINKS: source {len(src_links)}, built {len(bl)} (Drive photo links excluded) ---')
    bkeys = [(t_, lkey(h)) for t_, h in bl]
    for t_, h in src_links:
        hit = [x for x in bkeys if x[1] == lkey(h)]
        note = '' if not hit or hit[0][0] == t_ else f'  (built anchor «{hit[0][0][:50]}»)'
        print(('  ✓ ' if hit else '  ✗ MISSING ') + f'«{t_[:50]}» {h[:100]}{note}')
    sk = {lkey(h) for _, h in src_links}
    for t_, h in bl:
        if lkey(h) not in sk:
            print(f'  + only in build «{t_[:50]}» {h[:100]}')

    # photos
    srcimgs = []
    for m in msgs:
        md = f'{d}/{m["id"]}'
        for a in m['atts']:
            if a.lower().endswith(IMG_EXT):
                srcimgs.append(f'{md}/atts/{a}')
        srcimgs += fetch_drive_links(m['html'], md, hdr)
        for a in m['atts']:
            if a.lower().endswith('.pdf'):
                pd = f'{md}/pdfimg'
                os.makedirs(pd, exist_ok=True)
                subprocess.run(['pdfimages', '-png', f'{md}/atts/{a}', f'{pd}/img'], check=False)
                srcimgs += sorted(glob.glob(f'{pd}/*.png'))
    cands_fp = []
    for p in srcimgs:
        try:
            im = Image.open(p)
            if min(im.size) >= 60:
                cands_fp.append((p, fp(p)))
        except Exception:
            pass
    print(f'\n  --- FIGURES ({len(cands_fp)} source images to match against) ---')
    for f in body_el.find_all('figure'):
        img = f.find('img')
        cap = f.find('figcaption')
        if img is None:
            src = f.find('source')
            print(f'  (non-image figure: {src["src"] if src else f.find(True).name}) — not compared')
            continue
        name = unquote(img['src'])
        line = f'  {name[:44]:44} | {norm(cap.get_text()) if cap else "(no caption)"}'
        print(line[:230])
        path = f'{ROOT}/editions/{ed}/{slug}/{name}'
        if not os.path.exists(path) or not cands_fp:
            print('      ! image file missing' if not os.path.exists(path) else '      (no source images)')
            continue
        g = fp(path)
        r = sorted((dist(g, c), os.path.basename(p)) for p, c in cands_fp)
        tag = 'same name' if r[0][1] == os.path.basename(name) else f'matches «{r[0][1]}»'
        warn = '' if r[0][0] < 6 else '   <-- NO CLEAR MATCH: check by eye'
        print(f'      image: {tag} (score {r[0][0]:.1f}, next {r[1][0] if len(r) > 1 else 0:.1f}){warn}')


def read_sources(ed: str) -> dict[str, list[str]]:
    p = f'{ROOT}/editions/{ed}/STATUS.md'
    s = open(p, encoding='utf-8').read()
    m = re.search(r'^## Sources\s*\n(.*?)(?=^## |\Z)', s, flags=re.M | re.S)
    if not m:
        raise SystemExit(f'{p} has no "## Sources" section (see this script\'s docstring).')
    out = {}
    for slug, ids in re.findall(r'^\s*-\s*([a-z0-9-]+)\s*:\s*(.+)$', m.group(1), flags=re.M):
        out[slug] = re.findall(r'\b[0-9a-f]{16}\b', ids)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('date')
    ap.add_argument('--only')
    ap.add_argument('--out', default=os.path.join(tempfile.gettempdir(), 'source_audit'))
    a = ap.parse_args()
    out = os.path.join(a.out, a.date)
    src = read_sources(a.date)
    if a.only:
        src = {a.only: src[a.only]}
    hdr = {'Authorization': f'Bearer {token()}'}
    for slug, ids in src.items():
        if not ids:
            print(f'\n{slug}: no message IDs listed — skipped')
            continue
        audit(slug, ids, a.date, out, hdr)
    print(f'\nSource copies saved under {out}. Review every difference; report before fixing.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
