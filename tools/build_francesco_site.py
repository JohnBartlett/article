#!/usr/bin/env python3
"""
Build a standalone Classic Chicago site for Francesco Bianchini's "Continental
Memories" articles. Outputs to /tmp/francesco-site/, same pattern as
build_elizabeth_site.py (see the elizabeth-richter branch / writers/lucia-adams/
for precedent — a per-writer archive site, live but unlinked from the main nav).

Adapted for a Drive-only backup: instead of reading the old WordPress export
from a local filesystem mount, this script expects OLD_BASE to be a local
scratch directory (populated ahead of time by downloading each article's
index.html and one representative image from Google Drive) rather than the
full wp-content/uploads tree. Only one image per old article is available
(the article's hero/first content photo), not every inline image — inline
<img> tags in the body are stripped since we can't resolve most of them.
"""

import os, re, shutil, html as htmllib
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────

OLD_BASE    = Path('/tmp/francesco-old-source')
EDITIONS    = Path('/Users/john/article/editions')
OUT         = Path('/tmp/francesco-site')

CURRENT_SLUGS = [
    ('2026-03-01', 'case-of-the-missing-caramel', 'The Case of the Missing Caramel'),
    ('2026-03-15', 'guardian-san-pietro',         'The Guardian of San Pietro'),
    ('2026-04-12', 'shape-of-bread',               'The Shape of Bread'),
    ('2026-04-26', 'madeira',                      'Madeira'),
    ('2026-05-10', 'guinness-inis-mor',            'The First Guinness on Inis Mor'),
    ('2026-05-31', 'omelette-and-wine',            'An Omelette and a Glass of Wine'),
    ('2026-06-21', 'ciorba-de-perisoare',          'Ciorba de Perisoare'),
    ('2026-07-05', 'tiepolo-sky',                  'Dining Under a Tiepolo Sky'),
    ('2026-07-26', 'on-the-verge-of-a-heatstroke', 'Soup on the Verge of Heatstroke'),
    ('2026-09-06', 'francesco-bianchini',          'Chopsticks'),
]

# ── CSS / Template ────────────────────────────────────────────────────────────

HEADER_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{page_title} | Francesco Bianchini</title>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400;700&display=swap" rel="stylesheet">
  <style>
    *,*::before,*::after{box-sizing:border-box;}
    body{margin:0;font-family:'Lato',sans-serif;background:#f5f3ef;color:#222;-webkit-font-smoothing:antialiased;}
    a{color:#d41f1f;}
    /* Header */
    .site-header{background:#fff;border-bottom:3px solid #d41f1f;padding:14px 24px;display:flex;align-items:center;gap:20px;flex-wrap:wrap;}
    .site-header .site-name{font-family:'Playfair Display',serif;font-size:13px;color:#999;text-transform:uppercase;letter-spacing:0.12em;margin-bottom:2px;}
    .site-header .author-name{font-family:'Playfair Display',serif;font-size:26px;font-weight:700;color:#222;line-height:1.1;}
    .site-header .header-links{margin-left:auto;display:flex;gap:20px;align-items:center;flex-wrap:wrap;}
    .site-header .header-links a{color:#d41f1f;text-decoration:none;font-size:13px;text-transform:uppercase;letter-spacing:0.06em;}
    .site-header .header-links a:hover{text-decoration:underline;}
    /* Layout */
    .wrapper{max-width:780px;margin:40px auto;padding:0 24px;}
    /* Article */
    .article-header{margin-bottom:32px;}
    .article-header .kicker{font-size:12px;text-transform:uppercase;letter-spacing:0.12em;color:#d41f1f;margin-bottom:10px;}
    .article-header h1{font-family:'Playfair Display',serif;font-size:clamp(28px,5vw,44px);font-weight:700;line-height:1.15;margin:0 0 16px;}
    .article-header .byline{font-size:13px;color:#888;border-top:1px solid #e0d8ce;border-bottom:1px solid #e0d8ce;padding:8px 0;margin-bottom:0;}
    .article-header .byline strong{color:#555;}
    .article-body{font-size:17px;line-height:1.75;color:#333;}
    .article-body p{margin:0 0 1.4em;}
    .article-body h2{font-family:'Playfair Display',serif;font-size:24px;margin:1.8em 0 0.6em;}
    .article-body h3{font-family:'Playfair Display',serif;font-size:20px;margin:1.4em 0 0.5em;}
    .article-body img{max-width:100%;height:auto;display:block;margin:2em auto;border-radius:3px;}
    .article-body figure{margin:2em 0;}
    .article-body figure img{margin:0;}
    .article-body figcaption{font-size:13px;color:#888;margin-top:8px;font-style:italic;text-align:center;}
    .article-body blockquote{border-left:4px solid #d41f1f;margin:1.5em 0;padding:0.5em 1.2em;color:#555;font-style:italic;}
    /* Hero */
    .hero-img{width:100%;max-height:480px;object-fit:cover;display:block;border-radius:4px;margin-bottom:28px;}
    /* Index */
    .index-intro{font-family:'Playfair Display',serif;font-size:18px;color:#555;font-style:italic;margin-bottom:36px;padding-bottom:24px;border-bottom:2px solid #e0d8ce;}
    .index-note{font-size:13px;color:#888;background:#fff8f0;border-left:3px solid #e67e22;padding:12px 16px;margin-bottom:28px;}
    .year-group{margin-bottom:40px;}
    .year-label{font-family:'Playfair Display',serif;font-size:22px;font-weight:700;color:#d41f1f;margin:0 0 16px;padding-bottom:8px;border-bottom:1px solid #e0d8ce;}
    .article-card{display:flex;gap:16px;padding:14px 0;border-bottom:1px solid #f0ede8;text-decoration:none;color:inherit;align-items:flex-start;}
    .article-card:last-child{border-bottom:none;}
    .article-card:hover .card-title{color:#d41f1f;}
    .card-thumb{width:90px;height:68px;object-fit:cover;border-radius:3px;flex-shrink:0;background:#e8e3dc;}
    .card-thumb-placeholder{width:90px;height:68px;border-radius:3px;flex-shrink:0;background:#e8e3dc;display:flex;align-items:center;justify-content:center;}
    .card-thumb-placeholder span{font-size:9px;color:#bbb;text-transform:uppercase;letter-spacing:0.05em;}
    .card-info{flex:1;}
    .card-date{font-size:11px;color:#aaa;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:4px;}
    .card-title{font-family:'Playfair Display',serif;font-size:17px;font-weight:700;line-height:1.3;margin-bottom:4px;}
    .card-excerpt{font-size:13px;color:#777;line-height:1.5;}
    /* Footer */
    footer{text-align:center;padding:32px 24px;font-size:12px;color:#aaa;border-top:1px solid #e0d8ce;margin-top:60px;}
    @media(max-width:600px){
      .site-header{padding:12px 16px;}
      .wrapper{padding:0 16px;margin:24px auto;}
      .article-body{font-size:16px;}
    }
  </style>
</head>
<body>
<header class="site-header">
  <div>
    <div class="site-name">Classic Chicago Magazine</div>
    <div class="author-name">Francesco Bianchini</div>
  </div>
  <nav class="header-links">
    <a href="/index.html">All Articles</a>
  </nav>
</header>
'''

FOOTER_HTML = '''<footer>
  Classic Chicago Magazine &mdash; Articles by Francesco Bianchini
</footer>
</body>
</html>
'''

# ── Article parsing ───────────────────────────────────────────────────────────

def parse_old_article(slug):
    path = OLD_BASE / slug / 'index.html'
    with open(path, encoding='utf-8', errors='replace') as f:
        html = f.read()
    # This backup's HTML has literal backslash-escaped angle brackets
    html = html.replace('\\<', '<').replace('\\>', '>').replace('\\&', '&').replace('\\"', '"')

    # Title
    title_m = re.search(r'<h1[^>]*class="[^"]*entry-title[^"]*"[^>]*>(.*?)</h1>', html, re.DOTALL)
    if not title_m:
        title_m = re.search(r'<title>([^|<]+)', html)
    title = re.sub(r'<[^>]+>', '', title_m.group(1)).strip() if title_m else slug.replace('-', ' ').title()
    title = htmllib.unescape(title)

    # Date
    date_m = re.search(r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})', html)
    if not date_m:
        date_m = re.search(r'<time[^>]+datetime="(\d{4}-\d{2}-\d{2})', html)
    date = date_m.group(1) if date_m else '2021-01-01'

    # Body content
    body_m = re.search(r'class="entry-content[^"]*">(.*?)(?:<div class="(?:sharedaddy|post-share|jp-relatedposts|entry-footer)|</article)', html, re.DOTALL)
    body = body_m.group(1).strip() if body_m else ''

    return title, date, body

def clean_body(body, article_dir):
    """Clean WordPress body HTML. Only one hero image is available per old
    article (downloaded ahead of time into article_dir), so all inline <img>
    tags are stripped rather than rewritten -- we don't have most of them."""
    if not body:
        return ''

    body = re.sub(r'<img[^>]+>', '', body)

    # Remove wp-caption wrapper divs entirely (their image is gone anyway)
    body = re.sub(r'<div[^>]+class="wp-caption[^"]*"[^>]*>.*?</div>', '', body, flags=re.DOTALL)
    body = re.sub(r'<div[^>]+id="attachment_\d+"[^>]*>(.*?)</div>', lambda m: m.group(1), body, flags=re.DOTALL)
    body = re.sub(r'<p[^>]*>\s*BY FRANCESCO.*?</p>', '', body, flags=re.I)
    body = re.sub(r'<p[^>]*>\s*&nbsp;\s*</p>', '', body)
    body = re.sub(r'<p[^>]*>\s*</p>', '', body)
    body = re.sub(r'<div[^>]+align="center"[^>]*>', '<div>', body)
    body = re.sub(r'<div>\s*</div>', '', body)
    body = re.sub(r'<div>', '', body)
    body = re.sub(r'</div>', '', body)
    body = re.sub(r'\s*style="[^"]*"', '', body)
    body = re.sub(r'\s*class="[^"]*"', '', body)
    body = re.sub(r'\s*align="[^"]*"', '', body)
    body = re.sub(r'<a\s+href="http[^"]*">(.*?)</a>', r'\1', body)  # remove external links
    body = re.sub(r'\n{3,}', '\n\n', body).strip()

    return body

def find_hero_image(slug, article_dir):
    """Copy the one downloaded image for this old article into imgs/, if any."""
    src_dir = OLD_BASE / slug
    for f in sorted(src_dir.iterdir()):
        if f.suffix.lower() in ('.jpg', '.jpeg', '.png', '.webp') and f.name != 'index.html':
            imgs_out = article_dir / 'imgs'
            imgs_out.mkdir(exist_ok=True)
            dest = imgs_out / f.name
            shutil.copy2(f, dest)
            return f'imgs/{f.name}'
    return None

def format_date(iso):
    from datetime import date as dclass
    try:
        d = dclass.fromisoformat(iso[:10])
        return d.strftime('%B %-d, %Y')
    except Exception:
        return iso

def render_article(title, date, body, hero_img, out_path):
    date_fmt = format_date(date)
    hero_html = f'<img class="hero-img" src="{hero_img}" alt="{htmllib.escape(title)}">\n' if hero_img else ''
    content = HEADER_HTML.replace('{page_title}', htmllib.escape(title))
    content += f'''<main class="wrapper">
  <article>
    <div class="article-header">
      {hero_html}<h1>{htmllib.escape(title)}</h1>
      <div class="byline"><strong>By Francesco Bianchini</strong> &nbsp;&bull;&nbsp; {date_fmt}</div>
    </div>
    <div class="article-body">
{body}
    </div>
  </article>
</main>
'''
    content += FOOTER_HTML
    out_path.write_text(content, encoding='utf-8')

# ── Index page ────────────────────────────────────────────────────────────────

def render_index(articles_meta, missing_note):
    from collections import defaultdict
    by_year = defaultdict(list)
    for slug, title, date, hero in articles_meta:
        yr = date[:4]
        by_year[yr].append((slug, title, date, hero))

    body = HEADER_HTML.replace('{page_title}', 'Articles by Francesco Bianchini')
    body += '<main class="wrapper">\n'
    body += f'<p class="index-intro">A collection of Francesco Bianchini&rsquo;s &ldquo;Continental Memories&rdquo; column for Classic Chicago Magazine, spanning {min(by_year.keys())} to {max(by_year.keys())}.</p>\n'
    body += f'<p class="index-note">{missing_note}</p>\n'

    for yr in sorted(by_year.keys(), reverse=True):
        body += f'<div class="year-group">\n<div class="year-label">{yr}</div>\n'
        for slug, title, date, hero in sorted(by_year[yr], key=lambda x: x[2], reverse=True):
            date_fmt = format_date(date)
            if hero:
                thumb = f'<img class="card-thumb" src="{slug}/{hero}" alt="">'
            else:
                thumb = '<div class="card-thumb-placeholder"><span>Classic Chicago</span></div>'
            body += f'''<a class="article-card" href="{slug}/index.html">
  {thumb}
  <div class="card-info">
    <div class="card-date">{date_fmt}</div>
    <div class="card-title">{htmllib.escape(title)}</div>
  </div>
</a>\n'''
        body += '</div>\n'
    body += '</main>\n' + FOOTER_HTML
    return body

# ── Copy current articles ─────────────────────────────────────────────────────

def copy_current_article(edition_date, slug, out_dir, label):
    src = EDITIONS / edition_date / slug
    if not src.exists():
        print(f'  WARNING: current article not found: {src}')
        return None
    dest = out_dir / slug
    shutil.copytree(src, dest, dirs_exist_ok=True)
    idx = dest / 'index.html'
    with open(idx, encoding='utf-8') as f:
        html = f.read()
    title_m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    title = re.sub(r'<[^>]+>', '', title_m.group(1)).strip() if title_m else label
    title = htmllib.unescape(title)
    date_m = re.search(r'(\w+ \d+, 2026)', html)
    date_str = date_m.group(1) if date_m else edition_date
    body_m = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
    if not body_m:
        body_m = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL)
    body = body_m.group(1).strip() if body_m else ''
    hero_m = re.search(r'<figure[^>]*class="[^"]*hero[^"]*"[^>]*>.*?<img[^>]+src="([^"]+)"', html, re.DOTALL)
    if not hero_m:
        hero_m = re.search(r'<img[^>]+src="([^"]+)"', html)
    hero = hero_m.group(1) if hero_m else None
    hero_html = f'<img class="hero-img" src="{hero}" alt="{htmllib.escape(title)}">\n' if hero else ''
    content = HEADER_HTML.replace('{page_title}', htmllib.escape(title))
    content += f'''<main class="wrapper">
  <article>
    <div class="article-header">
      {hero_html}<h1>{htmllib.escape(title)}</h1>
      <div class="byline"><strong>By Francesco Bianchini</strong> &nbsp;&bull;&nbsp; {date_str}</div>
    </div>
    <div class="article-body">
{body}
    </div>
  </article>
</main>
'''
    content += FOOTER_HTML
    idx.write_text(content, encoding='utf-8')
    return (hero, edition_date, title)

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()

    articles_meta = []
    ok, fail = 0, 0

    old_slugs = sorted(p.name for p in OLD_BASE.iterdir() if p.is_dir())
    print(f'Processing {len(old_slugs)} old articles from Drive backup...')
    for i, slug in enumerate(old_slugs, 1):
        try:
            title, date, body = parse_old_article(slug)
            article_dir = OUT / slug
            article_dir.mkdir()
            hero = find_hero_image(slug, article_dir)
            body_clean = clean_body(body, article_dir)
            render_article(title, date, body_clean, hero, article_dir / 'index.html')
            articles_meta.append((slug, title, date, hero))
            ok += 1
            print(f'  [{i}/{len(old_slugs)}] OK  {title[:55]}  (hero: {"yes" if hero else "no"})')
        except Exception as e:
            fail += 1
            print(f'  [{i}/{len(old_slugs)}] FAIL {slug}: {e}')

    print(f'\nCopying {len(CURRENT_SLUGS)} current articles...')
    for edition_date, slug, label in CURRENT_SLUGS:
        try:
            result = copy_current_article(edition_date, slug, OUT, label)
            if result is None:
                fail += 1
                continue
            hero_src, _, title = result
            articles_meta.append((slug, title, edition_date, hero_src))
            ok += 1
            print(f'  OK  {title[:55]}')
        except Exception as e:
            fail += 1
            print(f'  FAIL {slug}: {e}')

    print('\nBuilding index...')
    missing_note = (
        'This is a partial archive: Francesco has written roughly 100 pieces for Classic Chicago since 2021, '
        'but only those recoverable from the site\'s 2026 backup snapshot (and the ones already rebuilt on the '
        'current site) are shown here. A multi-year gap (2022–2024) was not captured in the available backup.'
    )
    index_html = render_index(articles_meta, missing_note)
    (OUT / 'index.html').write_text(index_html, encoding='utf-8')

    (OUT / 'vercel.json').write_text('{"trailingSlash": false}\n')
    (OUT / '.vercelignore').write_text('node_modules\n')

    print(f'\nDone. Output: {OUT}')
    print(f'Total articles: {len(articles_meta)} (ok={ok}, fail={fail})')

if __name__ == '__main__':
    main()
