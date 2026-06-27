#!/usr/bin/env python3
"""
Redesign the elizabeth-richter Vercel site:
  1. Copy logo.jpg from dev2 git history
  2. Fix all broken image refs (../../../logo.jpg → real first photo or placeholder)
  3. Fix timeline-theater nav thumbs
  4. Fix index.html card thumb srcs
  5. Write shared ccm.css
  6. Rebuild index.html with 2-col card grid
  7. Apply new header/CSS link to all article pages
"""

import subprocess, re, shutil
from pathlib import Path

REPO = Path('/home/john/article')
PLACEHOLDER = '/no-photo.svg'

# ── 1. Get logo.jpg from dev2 ─────────────────────────────────────────────────
logo_dest = REPO / 'logo.jpg'
if not logo_dest.exists():
    result = subprocess.run(['git', 'show', 'dev2:logo.jpg'], cwd=REPO,
                            capture_output=True)
    if result.returncode == 0:
        logo_dest.write_bytes(result.stdout)
        print('Copied logo.jpg from dev2')
    else:
        print('WARNING: could not get logo.jpg from dev2')
else:
    print('logo.jpg already present')

# ── 2. Fix ../../../logo.jpg hero in the 5 current CCM articles ───────────────
# Use first real photo found in that folder as hero, or placeholder
def first_photo(folder):
    for ext in ('*.jpg','*.jpeg','*.png','*.JPG','*.PNG','*.JPEG'):
        imgs = [p for p in folder.glob(ext)
                if p.name.lower() not in ('logo.jpg', 'no-photo.svg')]
        if imgs:
            return imgs[0].name
    return None

broken_hero = ['detroit','downsizing','elizabeth-richter-reunion','kanuga','timeline-theater']
for slug in broken_hero:
    html = REPO / slug / 'index.html'
    if not html.exists():
        continue
    content = html.read_text(encoding='utf-8')
    if '../../../logo.jpg' not in content:
        continue
    photo = first_photo(REPO / slug)
    new_src = photo if photo else PLACEHOLDER
    content = content.replace('../../../logo.jpg', new_src, 1)
    html.write_text(content, encoding='utf-8')
    print(f'Fixed hero in {slug} → {new_src}')

# ── 3. Fix timeline-theater nav thumbs ───────────────────────────────────────
tt = REPO / 'timeline-theater' / 'index.html'
if tt.exists():
    content = tt.read_text(encoding='utf-8')
    content = content.replace('../merit-school-of-music/photo-01.jpeg', PLACEHOLDER)
    content = content.replace('../kenilworth-centennial-quilt/photo-01.jpeg', PLACEHOLDER)
    tt.write_text(content, encoding='utf-8')
    print('Fixed timeline-theater nav thumbs')

# ── 4. Build article metadata (for index rebuild) ────────────────────────────
import re as _re

MONTH_ORDER = {'january':1,'february':2,'march':3,'april':4,'may':5,'june':6,
               'july':7,'august':8,'september':9,'october':10,'november':11,'december':12}

def parse_article(slug):
    html = REPO / slug / 'index.html'
    if not html.exists():
        return None
    content = html.read_text(encoding='utf-8', errors='replace')
    title_m = _re.search(r'<h1[^>]*>(.*?)</h1>', content, _re.DOTALL)
    title = _re.sub(r'<[^>]+>', '', title_m.group(1)).strip() if title_m else slug
    date_m = _re.search(r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d+,\s+\d{4}', content)
    date_str = date_m.group(0) if date_m else ''
    # Sort key
    year = int(_re.search(r'\d{4}', date_str).group()) if date_str and _re.search(r'\d{4}', date_str) else 0
    mo_m = _re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)', date_str)
    mo = MONTH_ORDER.get(mo_m.group(1).lower(), 0) if mo_m else 0
    day_m = _re.search(r'(?:January|February|...)\s+(\d+),', date_str)
    day = int(_re.search(r',\s*\d{4}', date_str).group(0).replace(',','').strip()) if date_str else 0
    # Thumbnail: first local img
    thumb_m = _re.search(r'<img\b[^>]+src=["\'](?!/no-photo)(?!http)([^"\']+)["\']', content)
    thumb = thumb_m.group(1) if thumb_m else None
    # Verify thumb exists
    if thumb and not (REPO / slug / thumb).exists() and not thumb.startswith('/'):
        thumb = None
    # Excerpt: first real paragraph text
    paras = _re.findall(r'<p>(.*?)</p>', content, _re.DOTALL)
    excerpt = ''
    for p in paras:
        t = _re.sub(r'<[^>]+>', '', p).strip()
        if len(t) > 40:
            excerpt = t[:160] + ('…' if len(t) > 160 else '')
            break
    return {'slug': slug, 'title': title, 'date': date_str,
            'year': year, 'month': mo, 'day': day,
            'thumb': thumb, 'excerpt': excerpt}

articles = []
for d in REPO.iterdir():
    if d.is_dir() and (d / 'index.html').exists() and d.name not in (
            'OTHER','editions','.git','.vercel','.claude','.venv','node_modules',
            'resendingdatebook','future-articles','pastel-photos','tools','ads',
            '_template','editors','_bios'):
        meta = parse_article(d.name)
        if meta:
            articles.append(meta)

articles.sort(key=lambda a: (-a['year'], -a['month'], -a['day']))
print(f'Found {len(articles)} articles')

# ── 5. Shared CSS ─────────────────────────────────────────────────────────────
CSS = r"""
/* Classic Chicago Magazine — Elizabeth Dunlop Richter Archive */
*,*::before,*::after{box-sizing:border-box;}
html{font-size:16px;}
body{margin:0;font-family:'Lato',sans-serif;background:#faf8f4;color:#1c1c1c;-webkit-font-smoothing:antialiased;}
a{color:#b52b2b;text-decoration:none;}
a:hover{text-decoration:underline;}
img{max-width:100%;height:auto;}

/* ── Site Header ── */
.site-header{background:#fff;border-bottom:1px solid #e8e0d5;box-shadow:0 1px 6px rgba(0,0,0,.06);}
.site-header-inner{max-width:960px;margin:0 auto;padding:18px 24px;display:flex;flex-direction:column;align-items:center;gap:6px;}
.site-header .logo-img{height:52px;width:auto;display:block;}
.site-header .author-byline{font-family:'Playfair Display',serif;font-size:14px;font-style:italic;color:#888;letter-spacing:0.04em;}
.site-header nav{display:flex;gap:24px;margin-top:6px;}
.site-header nav a{font-size:12px;text-transform:uppercase;letter-spacing:0.1em;color:#666;font-family:'Lato',sans-serif;}
.site-header nav a:hover{color:#b52b2b;text-decoration:none;}

/* ── Index Page ── */
.index-wrapper{max-width:960px;margin:0 auto;padding:0 24px 80px;}
.index-hero{text-align:center;padding:56px 0 40px;border-bottom:1px solid #e8e0d5;margin-bottom:48px;}
.index-hero h1{font-family:'Playfair Display',serif;font-size:clamp(28px,5vw,42px);font-weight:700;color:#1c1c1c;margin:0 0 12px;line-height:1.15;}
.index-hero .tagline{font-family:'Playfair Display',serif;font-size:17px;font-style:italic;color:#888;max-width:560px;margin:0 auto;}

.year-section{margin-bottom:56px;}
.year-label{font-family:'Playfair Display',serif;font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:0.18em;color:#b52b2b;margin:0 0 20px;padding-bottom:10px;border-bottom:2px solid #e8e0d5;}
.card-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:28px;}

.article-card{display:flex;flex-direction:column;text-decoration:none;color:inherit;background:#fff;border-radius:6px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,.07);transition:box-shadow .2s,transform .2s;}
.article-card:hover{box-shadow:0 4px 18px rgba(0,0,0,.12);transform:translateY(-2px);text-decoration:none;}
.card-img-wrap{width:100%;aspect-ratio:16/9;overflow:hidden;background:#f0ebe3;flex-shrink:0;}
.card-img-wrap img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .3s;}
.article-card:hover .card-img-wrap img{transform:scale(1.03);}
.card-body{padding:16px 18px 20px;flex:1;display:flex;flex-direction:column;}
.card-date{font-size:11px;color:#aaa;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:7px;}
.card-title{font-family:'Playfair Display',serif;font-size:17px;font-weight:700;line-height:1.35;color:#1c1c1c;margin-bottom:8px;flex:1;}
.article-card:hover .card-title{color:#b52b2b;}
.card-excerpt{font-size:13px;color:#888;line-height:1.55;}

/* ── Article Page ── */
.article-wrapper{max-width:760px;margin:48px auto 80px;padding:0 24px;}
.article-label{font-size:11px;text-transform:uppercase;letter-spacing:0.15em;color:#b52b2b;font-weight:700;margin-bottom:14px;}
.article-wrapper h1{font-family:'Playfair Display',serif;font-size:clamp(26px,5vw,42px);font-weight:700;line-height:1.15;margin:0 0 20px;color:#1c1c1c;}
.article-byline{font-size:13px;color:#999;border-top:1px solid #e8e0d5;border-bottom:1px solid #e8e0d5;padding:10px 0;margin-bottom:32px;display:flex;gap:12px;flex-wrap:wrap;align-items:center;}
.article-byline strong{color:#555;}

.hero-figure{margin:0 0 36px;}
.hero-figure img{width:100%;max-height:520px;object-fit:cover;display:block;border-radius:5px;}
.hero-figure figcaption{font-size:12px;color:#aaa;margin-top:8px;font-style:italic;text-align:center;}

.article-body{font-size:18px;line-height:1.8;color:#2c2c2c;}
.article-body p{margin:0 0 1.5em;}
.article-body h2{font-family:'Playfair Display',serif;font-size:26px;margin:2em 0 0.7em;color:#1c1c1c;}
.article-body h3{font-family:'Playfair Display',serif;font-size:21px;margin:1.7em 0 0.6em;color:#1c1c1c;}
.article-body figure{margin:2.2em 0;}
.article-body figure img{width:100%;height:auto;display:block;border-radius:4px;}
.article-body figcaption{font-size:13px;color:#999;margin-top:9px;font-style:italic;text-align:center;line-height:1.5;}
.article-body blockquote{border-left:3px solid #b52b2b;margin:1.8em 0;padding:0.5em 1.4em;color:#666;font-style:italic;font-size:19px;}
.article-body img{border-radius:4px;}

/* Article nav (prev/next) */
.article-nav{display:flex;justify-content:space-between;gap:16px;margin-top:56px;padding-top:24px;border-top:1px solid #e8e0d5;}
.article-nav a{display:flex;align-items:center;gap:12px;text-decoration:none;color:#555;font-size:13px;max-width:48%;transition:color .15s;}
.article-nav a:hover{color:#b52b2b;}
.article-nav .nav-thumb{width:64px;height:64px;object-fit:cover;border-radius:4px;flex-shrink:0;background:#f0ebe3;}
.article-nav .nav-label{font-size:10px;text-transform:uppercase;letter-spacing:0.1em;color:#bbb;margin-bottom:4px;}
.article-nav .nav-title{font-family:'Playfair Display',serif;font-size:14px;line-height:1.4;}
.article-nav .nav-next{margin-left:auto;text-align:right;flex-direction:row-reverse;}

/* Footer */
footer{text-align:center;padding:32px 24px;font-size:12px;color:#bbb;border-top:1px solid #e8e0d5;margin-top:40px;}
footer a{color:#bbb;}

/* No-photo placeholder */
img[src="/no-photo.svg"]{border-radius:4px;opacity:.75;}

@media(max-width:640px){
  .card-grid{grid-template-columns:1fr 1fr;gap:16px;}
  .article-wrapper{margin-top:28px;}
  .article-body{font-size:16px;}
  .article-nav{flex-direction:column;}
  .article-nav .nav-next{flex-direction:row;text-align:left;margin-left:0;}
}
@media(max-width:400px){
  .card-grid{grid-template-columns:1fr;}
}
"""

css_path = REPO / 'ccm.css'
css_path.write_text(CSS.strip(), encoding='utf-8')
print('Wrote ccm.css')

# ── 6. Rebuild index.html ─────────────────────────────────────────────────────
from itertools import groupby

def card_html(a):
    slug = a['slug']
    thumb = a['thumb']
    if thumb:
        img_src = f"{slug}/{thumb}"
    else:
        img_src = PLACEHOLDER
    # Check if index-level thumb exists
    img_tag = f'<img src="{img_src}" alt="{a["title"]}" loading="lazy">'
    return f'''    <a class="article-card" href="/{slug}/">
      <div class="card-img-wrap">{img_tag}</div>
      <div class="card-body">
        <div class="card-date">{a["date"]}</div>
        <div class="card-title">{a["title"]}</div>
        <div class="card-excerpt">{a["excerpt"]}</div>
      </div>
    </a>'''

year_sections = []
for year, group in groupby(articles, key=lambda a: a['year']):
    cards = '\n'.join(card_html(a) for a in group)
    year_label = str(year) if year else 'Undated'
    year_sections.append(f'''  <section class="year-section">
    <h2 class="year-label">{year_label}</h2>
    <div class="card-grid">
{cards}
    </div>
  </section>''')

INDEX_HTML = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Elizabeth Dunlop Richter | Classic Chicago Magazine</title>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/ccm.css">
</head>
<body>
<header class="site-header">
  <div class="site-header-inner">
    <a href="/"><img class="logo-img" src="/logo.jpg" alt="Classic Chicago Magazine"></a>
    <div class="author-byline">A writing archive</div>
    <nav>
      <a href="/">All Articles</a>
      <a href="https://classicchicagomagazine.com" target="_blank">Classic Chicago Magazine</a>
    </nav>
  </div>
</header>
<main>
  <div class="index-wrapper">
    <div class="index-hero">
      <h1>Elizabeth Dunlop Richter</h1>
      <p class="tagline">Travel, culture, and the art of the well-lived life — {len(articles)} articles from Classic Chicago Magazine.</p>
    </div>
{chr(10).join(year_sections)}
  </div>
</main>
<footer>
  <p>© Classic Chicago Magazine &nbsp;·&nbsp; <a href="https://classicchicagomagazine.com">classicchicagomagazine.com</a></p>
</footer>
</body>
</html>'''

(REPO / 'index.html').write_text(INDEX_HTML, encoding='utf-8')
print('Rebuilt index.html')

# ── 7. Update all article pages: new header, link to ccm.css ─────────────────
ARTICLE_HEADER = '''<header class="site-header">
  <div class="site-header-inner">
    <a href="/"><img class="logo-img" src="/logo.jpg" alt="Classic Chicago Magazine"></a>
    <div class="author-byline">Elizabeth Dunlop Richter</div>
    <nav>
      <a href="/">&#8592; All Articles</a>
    </nav>
  </div>
</header>'''

FONT_LINK = '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400;700&display=swap" rel="stylesheet">'
CSS_LINK  = '<link rel="stylesheet" href="/ccm.css">'

patched = 0
for a in articles:
    html_path = REPO / a['slug'] / 'index.html'
    content = html_path.read_text(encoding='utf-8', errors='replace')

    # Replace <style>...</style> block with CSS link (keep font link)
    content = _re.sub(r'<style>.*?</style>', '', content, flags=_re.DOTALL)
    content = content.replace(FONT_LINK, FONT_LINK + '\n  ' + CSS_LINK)
    # If font link not there, add CSS link before </head>
    if CSS_LINK not in content:
        content = content.replace('</head>', f'  {CSS_LINK}\n</head>')

    # Replace <header ...>...</header> with new header
    content = _re.sub(r'<header\b[^>]*>.*?</header>', ARTICLE_HEADER, content,
                      count=1, flags=_re.DOTALL)

    # Update wrapper classes: old .wrapper → .article-wrapper
    content = content.replace(' class="wrapper"', ' class="article-wrapper"')

    # Update nav thumb class
    content = content.replace('class="nav-thumb"', 'class="nav-thumb"')  # already correct

    # Update article-body nav sections: .article-nav may already exist
    html_path.write_text(content, encoding='utf-8')
    patched += 1

print(f'Updated {patched} article pages')
print('Done.')
