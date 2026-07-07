#!/usr/bin/env python3
"""Generate edition landing pages (editions/YYYY-MM-DD/index.html).

The homepage's Past Editions cards link to edition folder roots; without an
index.html there, Cloudflare falls back to serving the homepage (soft 404).
Editions through 2026-05-10 had landing pages; this rebuilds the convention
for later editions using 2026-05-10 as the template.

Usage:
    python3 tools/build_edition_landing.py 2026-06-28 [2026-06-21 ...]
"""

import os, re, sys, html
from datetime import datetime

TEMPLATE = 'editions/2026-05-10/index.html'
SKIP = re.compile(r'^(datebook|daily-star)')


def article_meta(edition, slug):
    path = f'editions/{edition}/{slug}/index.html'
    h = open(path, encoding='utf-8', errors='replace').read()
    def find(pat):
        m = re.search(pat, h, re.S)
        return m.group(1).strip() if m else ''
    title = re.sub(r'<[^>]+>', '', find(r'<h1[^>]*>(.*?)</h1>'))
    author = find(r'By <a[^>]*>([^<]+)</a>')
    label = re.sub(r'<[^>]+>', '', find(r'class="article-category"[^>]*>(.*?)</'))
    img = find(r'<figure[^>]*>\s*(?:<a[^>]*>\s*)?<img[^>]+src="([^"]+)"')
    if not img:
        img = find(r'<img[^>]+class="[^"]*hero[^"]*"[^>]+src="([^"]+)"')
    # first substantial body paragraph as teaser
    teaser = ''
    for m in re.finditer(r'<p[^>]*>(.*?)</p>', h, re.S):
        text = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        if len(text) > 80 and not text.startswith('By '):
            teaser = text
            break
    if len(teaser) > 180:
        teaser = teaser[:180].rsplit(' ', 1)[0] + '&hellip;'
    prev = find(r"var prevUrl\s*=\s*'([^']+)'") or find(r'href="([^"]+)"[^>]*class="back-link"[^>]*>\s*&larr;')
    nxt = find(r"var nextUrl\s*=\s*'([^']+)'")
    if not nxt:
        m = re.search(r'<a href="([^"]+)" class="back-link">Next:', h)
        nxt = m.group(1) if m else ''
    return {'slug': slug, 'title': title, 'author': author, 'label': label,
            'img': f'{slug}/{img}' if img and not img.startswith('..') else img,
            'teaser': teaser, 'prev': prev, 'next': nxt}


def ordered_articles(edition):
    base = f'editions/{edition}'
    slugs = [d for d in sorted(os.listdir(base))
             if os.path.isfile(f'{base}/{d}/index.html') and not SKIP.match(d)]
    metas = {s: article_meta(edition, s) for s in slugs}
    # follow the prev/next chain starting at the article whose prev is the homepage
    start = next((s for s in slugs if 'index.html' in metas[s]['prev']), None)
    order, seen = [], set()
    cur = start
    while cur and cur not in seen:
        order.append(cur); seen.add(cur)
        nxt = metas[cur]['next']
        m = re.match(r'\.\./([^/]+)/', nxt)
        cur = m.group(1) if m and m.group(1) in metas else None
    order += [s for s in slugs if s not in seen]  # any articles outside the chain
    return [metas[s] for s in order]


def build(edition):
    tpl = open(TEMPLATE, encoding='utf-8').read()
    date_h = datetime.strptime(edition, '%Y-%m-%d').strftime('%B %-d, %Y')
    arts = ordered_articles(edition)
    if not arts:
        print(f'{edition}: no articles found, skipped'); return

    hero, cards = arts[0], arts[1:]
    hero_html = f'''      <div class="hero">
        <a href="{hero['slug']}/">
          <img class="hero-image" src="{hero['img']}" alt="{html.escape(hero['title'])}">
        </a>
        <div class="hero-text">
          <div class="hero-label">{hero['label'] or 'This Week'}</div>
          <h2><a href="{hero['slug']}/">{hero['title']}</a></h2>
          <div class="byline">By {hero['author']}</div>
          <p class="teaser">{hero['teaser']}</p>
        </div>
      </div>
'''
    card_html = '      <div class="card-grid">\n'
    for a in cards:
        card_html += f'''
        <div class="card">
          <a href="{a['slug']}/">
            <img class="card-image" src="{a['img']}" alt="{html.escape(a['title'])}">
          </a>
          <h2><a href="{a['slug']}/">{a['title']}</a></h2>
          <div class="meta">By {a['author']}</div>
          <p>{a['teaser']}</p>
        </div>
'''
    card_html += '      </div>\n'

    prefix = tpl[:tpl.index('      <div class="hero">')]
    suffix = tpl[tpl.index('  <footer>'):]
    prefix = prefix.replace('May 10, 2026', date_h)
    out = prefix + hero_html + '\n' + card_html + '\n    </div>\n  </main>\n\n' + suffix
    dest = f'editions/{edition}/index.html'
    open(dest, 'w', encoding='utf-8').write(out)
    print(f'{dest}: hero={hero["slug"]}, {len(cards)} cards, order={[a["slug"] for a in arts]}')


if __name__ == '__main__':
    for ed in sys.argv[1:]:
        build(ed)
