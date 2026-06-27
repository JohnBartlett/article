#!/usr/bin/env python3
"""
Build a standalone Classic Chicago site for Elizabeth Dunlop Richter's articles.
Outputs to /tmp/elizabeth-site/ ready for git commit to the elizabeth-richter branch.
"""

import os, re, shutil, html as htmllib
from pathlib import Path
from urllib.parse import urlparse

# ── Config ────────────────────────────────────────────────────────────────────

OLD_BASE    = Path('/home/john/OldCCM/ccm-restore/restore/20260208/classicchicagomagazine.com-original')
IMG_BASE    = Path('/home/john/OldCCM/ccm-restore/restore/20260208/classicchicagomagazine.com-original/wp-content/uploads')
IMG_BASE2   = Path('/home/john/OldCCM/ccm-restore/restore/classicchicagomagazine.com/wp-content/uploads')
EDITIONS    = Path('/home/john/article/editions')
OUT         = Path('/tmp/elizabeth-site')
REPO        = Path('/home/john/article')

CURRENT_SLUGS = [
    ('2026-02-22', 'downsizing',       'Downsizing'),
    ('2026-03-22', 'kanuga',           'Kanuga'),
    ('2026-05-10', 'detroit',          'Detroit'),
    ('2026-05-24', 'timeline-theater', 'TimeLine Theater'),
    ('2026-06-14', 'elizabeth-richter-reunion', '60th Reunion'),
]

# ── CSS / Template ────────────────────────────────────────────────────────────

HEADER_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{page_title} | Elizabeth Dunlop Richter</title>
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
    <div class="author-name">Elizabeth Dunlop Richter</div>
  </div>
  <nav class="header-links">
    <a href="/index.html">All Articles</a>
  </nav>
</header>
'''

FOOTER_HTML = '''<footer>
  Classic Chicago Magazine &mdash; Articles by Elizabeth Dunlop Richter
</footer>
</body>
</html>
'''

# ── Image resolution ──────────────────────────────────────────────────────────

def resolve_image(url):
    """Return local Path if image exists in backup, else None."""
    if not url or 'wp-content/uploads' not in url:
        return None
    # Extract path after wp-content/uploads
    m = re.search(r'wp-content/uploads/(.+)', url)
    if not m:
        return None
    rel = m.group(1).split('?')[0]
    for base in [IMG_BASE, IMG_BASE2]:
        p = base / rel
        if p.exists():
            return p
    # Try without size suffix (e.g. image-300x200.jpg -> image.jpg)
    rel_nosuffix = re.sub(r'-\d+x\d+(\.\w+)$', r'\1', rel)
    for base in [IMG_BASE, IMG_BASE2]:
        p = base / rel_nosuffix
        if p.exists():
            return p
    return None

# ── Article parsing ───────────────────────────────────────────────────────────

def parse_old_article(slug):
    path = OLD_BASE / slug / 'index.html'
    with open(path, encoding='utf-8', errors='replace') as f:
        html = f.read()

    # Title
    title_m = re.search(r'<h1[^>]*class="[^"]*entry-title[^"]*"[^>]*>(.*?)</h1>', html, re.DOTALL)
    if not title_m:
        title_m = re.search(r'<title>([^|<]+)', html)
    title = re.sub(r'<[^>]+>', '', title_m.group(1)).strip() if title_m else slug.replace('-', ' ').title()

    # Date
    date_m = re.search(r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})', html)
    if not date_m:
        date_m = re.search(r'<time[^>]+datetime="(\d{4}-\d{2}-\d{2})', html)
    date = date_m.group(1) if date_m else '2016-01-01'

    # Body content
    body_m = re.search(r'class="entry-content[^"]*">(.*?)(?:<div class="(?:sharedaddy|post-share|jp-relatedposts|entry-footer)|</article)', html, re.DOTALL)
    body = body_m.group(1).strip() if body_m else ''

    return title, date, body

def clean_body(body, article_dir, img_dir_name):
    """Clean WordPress body HTML, copy images to article_dir/imgs/, rewrite src."""
    if not body:
        return '', None

    imgs_out = article_dir / 'imgs'
    first_img_dest = None

    def rewrite_img(m):
        nonlocal first_img_dest
        tag = m.group(0)
        # Get src
        src_m = re.search(r'src="([^"]+)"', tag)
        if not src_m:
            return tag
        src = src_m.group(1)
        local = resolve_image(src)
        if local:
            imgs_out.mkdir(exist_ok=True)
            dest_name = local.name
            dest = imgs_out / dest_name
            if not dest.exists():
                shutil.copy2(local, dest)
            if first_img_dest is None:
                first_img_dest = f'imgs/{dest_name}'
            # Strip WordPress classes/sizes, rewrite src
            new_tag = re.sub(r'src="[^"]+"', f'src="imgs/{dest_name}"', tag)
            new_tag = re.sub(r'srcset="[^"]+"', '', new_tag)
            new_tag = re.sub(r'sizes="[^"]+"', '', new_tag)
            new_tag = re.sub(r'class="[^"]+"', '', new_tag)
            new_tag = re.sub(r'width="\d+"', '', new_tag)
            new_tag = re.sub(r'height="\d+"', '', new_tag)
            new_tag = re.sub(r'loading="[^"]+"', '', new_tag)
            new_tag = re.sub(r'decoding="[^"]+"', '', new_tag)
            return new_tag
        else:
            # Image not available — remove tag entirely
            return ''

    body = re.sub(r'<img[^>]+>', rewrite_img, body)

    # Remove wp-caption wrapper divs, keep caption text as figcaption
    def wp_caption(m):
        inner = m.group(1)
        img_m = re.search(r'<img[^>]+>', inner)
        cap_m = re.search(r'class="wp-caption-text"[^>]*>(.*?)</p>', inner, re.DOTALL)
        img_part = img_m.group(0) if img_m else ''
        cap_part = f'<figcaption>{cap_m.group(1).strip()}</figcaption>' if cap_m else ''
        if img_part:
            return f'<figure>{img_part}{cap_part}</figure>'
        return ''
    body = re.sub(r'<div[^>]+class="wp-caption[^"]*"[^>]*>(.*?)</div>', wp_caption, body, flags=re.DOTALL)

    # Remove WordPress-specific elements
    body = re.sub(r'<div[^>]+id="attachment_\d+"[^>]*>(.*?)</div>', lambda m: m.group(1), body, flags=re.DOTALL)
    body = re.sub(r'<p[^>]*>\s*BY ELIZABETH.*?</p>', '', body, flags=re.I)
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

    return body, first_img_dest

def format_date(iso):
    from datetime import date as dclass
    try:
        d = dclass.fromisoformat(iso[:10])
        return d.strftime('%B %-d, %Y')
    except:
        return iso

def render_article(title, date, body, hero_img, out_path):
    date_fmt = format_date(date)
    hero_html = f'<img class="hero-img" src="{hero_img}" alt="{htmllib.escape(title)}">\n' if hero_img else ''
    content = HEADER_HTML.replace('{page_title}', htmllib.escape(title))
    content += f'''<main class="wrapper">
  <article>
    <div class="article-header">
      {hero_html}<h1>{htmllib.escape(title)}</h1>
      <div class="byline"><strong>By Elizabeth Dunlop Richter</strong> &nbsp;&bull;&nbsp; {date_fmt}</div>
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

def render_index(articles_meta):
    from collections import defaultdict
    by_year = defaultdict(list)
    for slug, title, date, hero in articles_meta:
        yr = date[:4]
        by_year[yr].append((slug, title, date, hero))

    body = HEADER_HTML.replace('{page_title}', 'Articles by Elizabeth Dunlop Richter')
    body += '<main class="wrapper">\n'
    body += f'<p class="index-intro">A complete collection of Elizabeth Dunlop Richter&rsquo;s writing for Classic Chicago Magazine, spanning {min(by_year.keys())} to {max(by_year.keys())}.</p>\n'

    for yr in sorted(by_year.keys(), reverse=True):
        body += f'<div class="year-group">\n<div class="year-label">{yr}</div>\n'
        for slug, title, date, hero in sorted(by_year[yr], key=lambda x: x[2], reverse=True):
            date_fmt = format_date(date)
            if hero:
                thumb = f'<img class="card-thumb" src="{slug}/imgs/{Path(hero).name}" alt="">'
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

def copy_current_article(edition_date, slug, out_dir):
    src = EDITIONS / edition_date / slug
    if not src.exists():
        print(f'  WARNING: current article not found: {src}')
        return None
    dest = out_dir / slug
    shutil.copytree(src, dest, dirs_exist_ok=True)
    # Read index.html, strip nav/header/footer, wrap in our template
    idx = dest / 'index.html'
    with open(idx, encoding='utf-8') as f:
        html = f.read()
    # Extract h1 title
    title_m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    title = re.sub(r'<[^>]+>', '', title_m.group(1)).strip() if title_m else slug
    # Extract date from byline or meta
    date_m = re.search(r'(\w+ \d+, 2026)', html)
    date_str = date_m.group(1) if date_m else edition_date
    # Extract article body between <article> tags or main content div
    body_m = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
    if not body_m:
        body_m = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL)
    body = body_m.group(1).strip() if body_m else ''
    # Find hero image
    hero_m = re.search(r'<figure[^>]*class="[^"]*hero[^"]*"[^>]*>.*?<img[^>]+src="([^"]+)"', html, re.DOTALL)
    if not hero_m:
        hero_m = re.search(r'<img[^>]+src="([^"]+)"', html)
    hero = hero_m.group(1) if hero_m else None
    # Write cleaned version
    hero_html = f'<img class="hero-img" src="{hero}" alt="{htmllib.escape(title)}">\n' if hero else ''
    content = HEADER_HTML.replace('{page_title}', htmllib.escape(title))
    content += f'''<main class="wrapper">
  <article>
    <div class="article-header">
      {hero_html}<h1>{htmllib.escape(title)}</h1>
      <div class="byline"><strong>By Elizabeth Dunlop Richter</strong> &nbsp;&bull;&nbsp; {date_str}</div>
    </div>
    <div class="article-body">
{body}
    </div>
  </article>
</main>
'''
    content += FOOTER_HTML
    idx.write_text(content, encoding='utf-8')
    return (hero, edition_date)

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    # Reset output
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()

    articles_meta = []  # (slug, title, date, hero_local_path)

    # ── Old articles ──
    old_slugs = []
    for slug in os.listdir(OLD_BASE):
        path = OLD_BASE / slug / 'index.html'
        if not path.exists():
            continue
        with open(path, encoding='utf-8', errors='replace') as f:
            html = f.read()
        if re.search(r'by elizabeth.*?richter|elizabeth.*?richter.*?author', html, re.I):
            old_slugs.append(slug)

    print(f'Processing {len(old_slugs)} old articles...')
    for i, slug in enumerate(old_slugs, 1):
        try:
            title, date, body = parse_old_article(slug)
            article_dir = OUT / slug
            article_dir.mkdir()
            body_clean, hero = clean_body(body, article_dir, slug)
            render_article(title, date, body_clean, hero, article_dir / 'index.html')
            articles_meta.append((slug, title, date, hero))
            print(f'  [{i}/{len(old_slugs)}] {title[:55]}')
        except Exception as e:
            print(f'  ERROR {slug}: {e}')

    # ── Current articles ──
    print(f'\nCopying {len(CURRENT_SLUGS)} current articles...')
    for edition_date, slug, label in CURRENT_SLUGS:
        try:
            result = copy_current_article(edition_date, slug, OUT)
            # Get title from actual file
            idx = OUT / slug / 'index.html'
            with open(idx, encoding='utf-8') as f:
                h = f.read()
            title_m = re.search(r'<h1[^>]*>(.*?)</h1>', h, re.DOTALL)
            title = re.sub(r'<[^>]+>', '', title_m.group(1)).strip() if title_m else label
            hero_m = re.search(r'<img class="hero-img" src="([^"]+)"', h)
            hero_src = hero_m.group(1) if hero_m else None
            articles_meta.append((slug, title, edition_date, hero_src))
            print(f'  ✓ {title[:55]}')
        except Exception as e:
            print(f'  ERROR {slug}: {e}')

    # ── Index ──
    print('\nBuilding index...')
    index_html = render_index(articles_meta)
    (OUT / 'index.html').write_text(index_html, encoding='utf-8')

    # ── vercel.json ──
    (OUT / 'vercel.json').write_text('{"trailingSlash": false}\n')

    # ── .vercelignore ──
    (OUT / '.vercelignore').write_text('node_modules\n')

    print(f'\nDone. Output: {OUT}')
    print(f'Total articles: {len(articles_meta)}')

if __name__ == '__main__':
    main()
