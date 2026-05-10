#!/usr/bin/env python3
"""Add hamburger menu to May 3 articles that don't have it yet."""
import re, os

CSS_INSERT = """
    .hamburger-btn {
      background: none;
      border: none;
      cursor: pointer;
      font-size: 22px;
      color: #d41f1f;
      padding: 2px 8px;
      margin-left: 10px;
      line-height: 1;
      font-family: 'Lato', sans-serif;
    }

    .hamburger-btn:hover {
      color: #b51c20;
    }

    .hamburger-menu {
      display: none;
      background: #fff;
      border-bottom: 1px solid #eee;
      text-align: center;
      padding: 10px 0;
    }

    .hamburger-menu.open {
      display: block;
    }

    .hamburger-menu a {
      font-family: 'Lato', sans-serif;
      font-size: 15px;
      font-weight: 400;
      color: #d41f1f;
      text-decoration: none;
      text-transform: uppercase;
      display: inline-block;
      margin: 0 15px;
      padding: 5px 0;
      letter-spacing: 0.05em;
    }

    .hamburger-menu a:hover {
      color: #b51c20;
      text-decoration: underline;
    }
"""

JS_INSERT = """  <script>
    (function() {
      var btn = document.getElementById('hamburger-btn');
      var menu = document.getElementById('hamburger-menu');
      if (btn && menu) {
        btn.addEventListener('click', function() {
          menu.classList.toggle('open');
        });
        document.addEventListener('click', function(e) {
          if (!btn.contains(e.target) && !menu.contains(e.target)) {
            menu.classList.remove('open');
          }
        });
      }
    })();
  </script>
"""

# Per-article nav replacements: (old_nav_inner_content, new_nav_inner_content, astrochart_href)
# Each tuple: slug -> (home_href, datebook_href, astrochart_href or None)
ARTICLES = {
    'unsung-gems-lfpf':     ('../../../index.html', '../datebook/', '../daily-star-may/'),
    'bill-kurtis':          ('../../../index.html', '../datebook/', '../daily-star-may/'),
    'about-the-town-may':   ('../../../index.html', '../datebook/', '../daily-star-may/'),
    'facets':               ('../../../index.html', '../datebook/', '../daily-star-may/'),
    'st-james':             ('../../../index.html', '../datebook/', '../daily-star-may/'),
    'origami':              ('../../../index.html', '../datebook/', '../daily-star-may/'),
    'marcy-carmack':        ('../../../index.html', '../datebook/', '../daily-star-may/'),
    'train-history-part-two': ('../index.html',     '../datebook/', '../daily-star-may/'),
    'datebook':             ('../../../index.html', './',           '../daily-star-may/'),
}

BASE = '/home/john/article/editions/2026-05-03'

def make_new_nav(home, datebook, astrochart, label_datebook='DateBook', label_astrochart='Astrochart'):
    lines = [
        '      <div class="nav-inner">',
        f'        <a href="{home}">Home</a>',
        f'        <a href="{datebook}">{label_datebook}</a>',
    ]
    if astrochart:
        lines.append(f'        <a href="{astrochart}">{label_astrochart}</a>')
    lines += [
        '        <button class="hamburger-btn" id="hamburger-btn" aria-label="More">&#9776;</button>',
        '      </div>',
        '      <div class="hamburger-menu" id="hamburger-menu">',
        '        <a href="../../../about.html">About</a>',
        '        <a href="../../../subscribe.html">Subscribe</a>',
        '        <a href="../../../advertise.html">Advertise</a>',
        '      </div>',
    ]
    return '\n'.join(lines)

for slug, (home, datebook, astrochart) in ARTICLES.items():
    path = os.path.join(BASE, slug, 'index.html')
    with open(path) as f:
        html = f.read()

    if 'hamburger-btn' in html:
        print(f'SKIP (already has hamburger): {slug}')
        continue

    # 1. Add CSS after .nav-inner a:hover block
    # Find the closing brace after .nav-inner a:hover {
    css_marker = '.nav-inner a:hover {'
    idx = html.find(css_marker)
    if idx == -1:
        print(f'ERROR: nav-inner a:hover not found in {slug}')
        continue
    # Find the closing } after this
    close = html.find('}', idx)
    # Insert CSS after that }
    html = html[:close+1] + '\n' + CSS_INSERT + html[close+1:]

    # 2. Replace nav-inner div block (old style: 4-6 links, no hamburger)
    new_nav = make_new_nav(home, datebook, astrochart if slug != 'datebook' else None)
    # For datebook, no astrochart (it IS the datebook page)
    if slug == 'datebook':
        new_nav = make_new_nav(home, './', None, label_datebook='DateBook')
        # Also add astrochart separately
        new_nav = new_nav.replace(
            '        <button class="hamburger-btn"',
            '        <a href="../daily-star-may/">Astrochart</a>\n        <button class="hamburger-btn"'
        )

    # Replace the entire nav-inner div including all its links
    nav_pattern = re.compile(
        r'      <div class="nav-inner">.*?</div>\s*\n    </nav>',
        re.DOTALL
    )
    new_nav_block = new_nav + '\n    </nav>'
    html, n = nav_pattern.subn(new_nav_block, html, count=1)
    if n == 0:
        print(f'ERROR: nav-inner pattern not matched in {slug}')
        continue

    # Fix about.html path for train-history (Home uses ../index.html so depth is different)
    if slug == 'train-history-part-two':
        html = html.replace(
            '        <a href="../../../about.html">About</a>\n        <a href="../../../subscribe.html">Subscribe</a>\n        <a href="../../../advertise.html">Advertise</a>',
            '        <a href="../../about.html">About</a>\n        <a href="../../subscribe.html">Subscribe</a>\n        <a href="../../advertise.html">Advertise</a>'
        )

    # 3. Add JS before </body>
    html = html.replace('</body>', JS_INSERT + '</body>')

    with open(path, 'w') as f:
        f.write(html)
    print(f'OK: {slug}')

print('Done.')
