#!/usr/bin/env python3
"""
Rebuild the 5 Elizabeth Dunlop Richter 2026 articles on the elizabeth-richter branch
using the full dev2 HTML as the source, then adapting all paths and nav for this site.
"""

import subprocess, re
from pathlib import Path

REPO = Path('/home/john/article')

# Article chain in date order
CHAIN = [
    {
        'slug': 'downsizing',
        'dev2': 'editions/2026-02-22/downsizing',
        'thumb': 'house-sale.jpg',
        'title': 'The Downsizing Dilemma',
    },
    {
        'slug': 'kanuga',
        'dev2': 'editions/2026-03-22/kanuga',
        'thumb': 'images/image20.jpg',
        'title': 'Kanuga: The Christmas Solution',
    },
    {
        'slug': 'detroit',
        'dev2': 'editions/2026-05-10/detroit',
        'thumb': 'photo-01.jpg',
        'title': 'A Taste of Detroit',
    },
    {
        'slug': 'timeline-theater',
        'dev2': 'editions/2026-05-24/timeline-theater',
        'thumb': 'photo-01.jpeg',
        'title': 'Stage Write: TimeLine Reborn',
    },
    {
        'slug': 'elizabeth-richter-reunion',
        'dev2': 'editions/2026-06-14/elizabeth-richter-reunion',
        'thumb': '1-WelcomeBackSign.png',
        'title': 'The 60th Reunion Is Worth Celebrating!',
    },
]


def get_dev2(path):
    r = subprocess.run(['git', 'show', f'dev2:{path}/index.html'],
                       cwd=REPO, capture_output=True)
    return r.stdout.decode('utf-8', errors='replace')


def build_article_nav(i):
    """Return the article-nav HTML for article at index i in CHAIN."""
    article = CHAIN[i]
    prev_i = i - 1
    next_i = i + 1

    # Previous
    if prev_i < 0:
        prev_html = '''    <a class="prev" href="/">
      <div>
        <span class="nav-label">&larr; Previous</span>
        All Articles
      </div>
    </a>'''
    else:
        prev = CHAIN[prev_i]
        prev_html = f'''    <a class="prev" href="/{prev['slug']}/">
      <img src="/{prev['slug']}/{prev['thumb']}" alt="{prev['title']}">
      <div>
        <span class="nav-label">&larr; Previous</span>
        {prev['title']}
      </div>
    </a>'''

    # Next
    if next_i >= len(CHAIN):
        next_html = '''    <a class="next" href="/">
      <div>
        <span class="nav-label">Next &rarr;</span>
        All Articles
      </div>
    </a>'''
    else:
        nxt = CHAIN[next_i]
        next_html = f'''    <a class="next" href="/{nxt['slug']}/">
      <img src="/{nxt['slug']}/{nxt['thumb']}" alt="{nxt['title']}">
      <div>
        <span class="nav-label">Next &rarr;</span>
        {nxt['title']}
      </div>
    </a>'''

    return f'  <nav class="article-nav">\n{prev_html}\n{next_html}\n  </nav>'


def adapt(html, i):
    """Transform a dev2 article HTML for the elizabeth-richter site."""

    # ── Remove dark-mode.js (not on this branch) ──
    html = re.sub(r'\s*<script src="[^"]*dark-mode\.js[^"]*"></script>', '', html)

    # ── Remove favicon (no favicon on this branch) ──
    html = re.sub(r'\s*<link rel="icon"[^>]*>', '', html)

    # ── Root asset paths ──
    html = html.replace('../../../logo.jpg', '/logo.jpg')
    html = html.replace('../../../index.html', '/')

    # ── Author byline link → just text (no about.html on this site) ──
    html = re.sub(
        r'<a href="[^"]*about\.html#elizabeth-dunlop-richter">Elizabeth Dunlop Richter</a>',
        'Elizabeth Dunlop Richter',
        html
    )

    # ── Nav: remove DateBook, Astrochart, Editors' Page links; keep Home + hamburger ──
    # Replace the nav-inner links with just Home + hamburger
    html = re.sub(
        r'(<div class="nav-inner">)\s*.*?(\s*<button class="hamburger-btn")',
        r'\1\n        <a href="/">Home</a>\n        <a href="https://classicchicagomag.com">Classic Chicago</a>\2',
        html, count=1, flags=re.DOTALL
    )

    # ── Hamburger: point About/Subscribe/Advertise to main site ──
    html = html.replace('../../../about.html', 'https://classicchicagomag.com/about.html')
    html = html.replace('../../../subscribe.html', 'https://classicchicagomag.com/subscribe.html')
    html = html.replace('../../../advertise.html', 'https://classicchicagomag.com/advertise.html')

    # ── Remove editorial banner ──
    html = re.sub(r'\s*<div class="editorial-banner">.*?</div>', '', html, flags=re.DOTALL)

    # ── Remove internal-nav block ──
    html = re.sub(r'<!-- dev2-only -->\s*<div class="internal-nav">.*?</div>', '',
                  html, flags=re.DOTALL)
    html = re.sub(r'<div class="internal-nav">.*?</div>', '', html, flags=re.DOTALL)

    # ── Replace ALL nav patterns with correct chain nav ──
    new_nav = build_article_nav(i)
    # Pattern 1: <nav class="article-nav">...</nav>
    html = re.sub(r'<nav class="article-nav">.*?</nav>', new_nav, html, flags=re.DOTALL)
    # Pattern 2: <div class="edition-nav">...</div>
    html = re.sub(r'<div class="edition-nav">.*?</div>', new_nav, html, flags=re.DOTALL)
    # Pattern 3: bare back-links (no wrapper) — two adjacent <a class="back-link"> tags
    html = re.sub(
        r'<a href="[^"]*" class="back-link[^"]*">.*?</a>\s*\n?\s*<a href="[^"]*" class="back-link[^"]*"[^>]*>.*?</a>',
        new_nav, html, flags=re.DOTALL
    )

    # ── Keyboard shortcut JS: update prevUrl/nextUrl ──
    prev_url = '/' if i == 0 else f'/{CHAIN[i-1]["slug"]}/'
    next_url = '/' if i == len(CHAIN)-1 else f'/{CHAIN[i+1]["slug"]}/'
    html = re.sub(r"var prevUrl\s*=\s*'[^']*'", f"var prevUrl = '{prev_url}'", html)
    html = re.sub(r"var nextUrl\s*=\s*'[^']*'", f"var nextUrl = '{next_url}'", html)

    # ── Fix remaining ../../.. and ../../ relative paths ──
    html = re.sub(r'href="\.\./\.\./\.\./[^"]*"', 'href="https://classicchicagomag.com"', html)
    html = re.sub(r'src="\.\./\.\./\.\./[^"]*"',  'src="/logo.jpg"', html)
    html = re.sub(r'href="\.\./\.\.[^"]*"', 'href="https://classicchicagomag.com"', html)
    html = re.sub(r'src="\.\./\.\.[^"]*"',  'src="/logo.jpg"', html)

    # ── Fix edition-sibling article-nav thumbnails (../OTHER-SLUG/photo.jpg) ──
    html = re.sub(r'src="\.\./[^/]+/[^"]*"', 'src="/no-photo.svg"', html)

    return html


for i, article in enumerate(CHAIN):
    slug = article['slug']
    dev2_html = get_dev2(article['dev2'])
    if not dev2_html.strip():
        print(f'ERROR: could not read dev2:{article["dev2"]}')
        continue

    adapted = adapt(dev2_html, i)

    out = REPO / slug / 'index.html'
    out.write_text(adapted, encoding='utf-8')

    imgs  = len(re.findall(r'<img\b', adapted))
    paras = len(re.findall(r'<p>',    adapted))
    print(f'{slug}: {imgs} imgs, {paras} paras')

print('Done.')
