(function () {
  // ── 1. Apply theme immediately — no flash ────────────────────────────────
  var isDark = localStorage.getItem('cc-theme') === 'dark';
  if (isDark) document.documentElement.classList.add('dark');

  // ── 2. Inject CSS ─────────────────────────────────────────────────────────
  var style = document.createElement('style');
  style.textContent = [
    /* Base */
    'html.dark body { background: #111 !important; color: #ddd !important; }',

    /* Header / Nav */
    'html.dark header { background: #1a1a1a !important; border-color: #2a2a2a !important; }',
    'html.dark nav { border-color: #2a2a2a !important; }',
    'html.dark .hamburger-menu { background: #1a1a1a !important; border-color: #2a2a2a !important; }',
    'html.dark .internal-nav { background: #161616 !important; border-color: #2a2a2a !important; }',
    'html.dark .internal-nav-inner a { color: #888 !important; }',
    'html.dark .internal-nav-inner a:hover { color: #bbb !important; }',

    /* Homepage titles with inline styles */
    'html.dark h1[style] { color: #eee !important; }',
    'html.dark div[style*="color: #222"] { color: #ddd !important; }',
    'html.dark div[style*="color: #111"] { color: #ddd !important; }',

    /* Card grid */
    'html.dark .card { border-color: #2a2a2a !important; }',
    'html.dark .card h2 a { color: #e0e0e0 !important; }',
    'html.dark .card h2 a:hover { color: #e05555 !important; }',
    'html.dark .card .meta { color: #777 !important; }',
    'html.dark .card p { color: #aaa !important; }',
    'html.dark .card-image { opacity: 0.88; }',

    /* Hero text (below image) */
    'html.dark .hero h2 a { color: #e0e0e0 !important; }',
    'html.dark .hero h2 a:hover { color: #e05555 !important; }',
    'html.dark .hero .hero-label { color: #e05555 !important; }',
    'html.dark .hero .hero-meta { color: #777 !important; }',
    'html.dark .hero .hero-teaser { color: #aaa !important; }',

    /* Past editions band */
    'html.dark .past-editions { background: #161616 !important; border-color: #b51c20 !important; }',
    'html.dark .past-editions h2 { color: #777 !important; }',

    /* Article page */
    'html.dark h1.article-title { color: #eee !important; }',
    'html.dark .article-subtitle { color: #999 !important; }',
    'html.dark .article-meta { color: #777 !important; border-color: #2a2a2a !important; }',
    'html.dark .article-intro { color: #ccc !important; border-color: #2a2a2a !important; }',
    'html.dark .article-body p { color: #ccc !important; }',
    'html.dark .article-body h2 { color: #eee !important; border-color: #2a2a2a !important; }',
    'html.dark .article-body .pullquote { color: #bbb !important; }',
    'html.dark .article-body .question { border-color: #e05555 !important; }',
    'html.dark .article-category { color: #e05555 !important; }',
    'html.dark figure figcaption, html.dark .hero-figure figcaption { color: #777 !important; }',
    'html.dark .edition-nav { border-color: #2a2a2a !important; }',
    'html.dark .back-link { color: #e05555 !important; border-color: #e05555 !important; }',
    'html.dark .back-link:hover { color: #ff7070 !important; border-color: #ff7070 !important; }',

    /* Feedback widget (inline-styled) */
    'html.dark [style*="background: #fdfaf7"] { background: #1e1e1e !important; border-color: #333 !important; }',
    'html.dark [style*="border: 1px solid #e8e0d5"] { border-color: #333 !important; }',
    'html.dark [style*="border-top: 1px solid #ece5dd"] { border-color: #2a2a2a !important; }',
    'html.dark [style*="color: #888"] { color: #777 !important; }',
    'html.dark [style*="color: #555"] { color: #bbb !important; }',
    'html.dark [style*="color: #999; text-transform: uppercase; letter-spacing: 0.08em"] { color: #777 !important; }',
    'html.dark textarea[name="comment"] { background: #252525 !important; border-color: #3a3a3a !important; color: #ddd !important; }',
    'html.dark input[type="email"][name="email"] { background: #252525 !important; border-color: #3a3a3a !important; color: #ddd !important; }',
    'html.dark #thumbUp { background: #1a2b1a !important; border-color: #2e5430 !important; }',
    'html.dark #thumbDown { background: #2b1a1a !important; border-color: #542e2e !important; }',

    /* Article wrapper card (reader-comments style wrapper) */
    'html.dark .article-wrapper { background: #1e1e1e !important; box-shadow: 0 2px 20px rgba(0,0,0,0.5) !important; }',

    /* About page bios */
    'html.dark .bio-card, html.dark [class*="bio"] { background: #1e1e1e !important; border-color: #2a2a2a !important; }',
    'html.dark h2[style*="color: #111"], html.dark h3[style*="color: #111"] { color: #eee !important; }',
    'html.dark p[style*="color: #333"], html.dark p[style*="color: #444"], html.dark p[style*="color: #555"] { color: #bbb !important; }',

    /* Footer stays dark — already dark, just slightly deeper */
    'html.dark footer { background: #0d0d0d !important; }',

    /* Theme toggle button */
    '#cc-theme-toggle {',
    '  position: absolute; top: 14px; right: 20px;',
    '  background: none; border-radius: 20px; padding: 4px 12px;',
    '  cursor: pointer; font-family: Lato, sans-serif; font-size: 12px;',
    '  display: flex; align-items: center; gap: 5px;',
    '  transition: border-color 0.2s, color 0.2s;',
    '  z-index: 100;',
    '}',
    '@media (max-width: 600px) {',
    '  #cc-theme-toggle {',
    '    position: static;',
    '    margin: 8px auto 4px;',
    '    justify-content: center;',
    '  }',
    '}',
    'html.dark #cc-theme-toggle { border: 1px solid #3a3a3a; color: #aaa; }',
    'html:not(.dark) #cc-theme-toggle { border: 1px solid #ddd; color: #666; }',
    'html.dark #cc-theme-toggle:hover { border-color: #e05555; color: #e05555; }',
    'html:not(.dark) #cc-theme-toggle:hover { border-color: #b51c20; color: #b51c20; }',

    /* ── Editors' Pages ──────────────────────────────────────────────────── */
    /* Page chrome */
    'html.dark .page-header { border-color: #b51c20 !important; }',
    'html.dark .section-head { border-color: #2a2a2a !important; }',
    'html.dark .dash-section .section-title { color: #e05555 !important; }',
    'html.dark .breadcrumb { color: #555 !important; }',
    'html.dark .stage-note { color: #555 !important; }',
    'html.dark .edition-tag { color: #666 !important; }',

    /* Section cards (hub) */
    'html.dark .section-card { background: #1a1a1a !important; border-color: #2a2a2a !important; border-top-color: #b51c20 !important; }',
    'html.dark .section-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.4) !important; }',
    'html.dark .card-label { color: #e05555 !important; }',
    'html.dark .card-title { color: #ddd !important; }',
    'html.dark .card-desc { color: #666 !important; }',

    /* Edition / status tables */
    'html.dark .edition-table th, html.dark .status-mini th { background: #1e1e1e !important; color: #555 !important; }',
    'html.dark .edition-table td, html.dark .status-mini td { border-color: #222 !important; }',
    'html.dark .article-name { color: #ddd !important; }',
    'html.dark .article-sub { color: #555 !important; }',
    'html.dark .writer-cell { color: #777 !important; }',
    'html.dark .stage-dash { color: #444 !important; }',

    /* Badges */
    'html.dark .badge-published { background: #0d1f0e !important; color: #4caf50 !important; }',
    'html.dark .badge-pending   { background: #1f1800 !important; color: #f9a825 !important; }',
    'html.dark .badge-missing   { background: #1a1a1a !important; color: #555 !important; }',

    /* Homepage order list */
    'html.dark .order-list li { border-color: #222 !important; }',
    'html.dark .order-title { color: #ddd !important; }',
    'html.dark .order-by { color: #555 !important; }',
    'html.dark .order-tag { color: #e05555 !important; border-color: #3a1e1e !important; }',
    'html.dark .order-num { color: #333 !important; }',

    /* Pipeline */
    'html.dark .pipeline-list li { border-color: #222 !important; color: #777 !important; }',
    'html.dark .pipeline-list strong { color: #bbb !important; }',

    /* Stats cards */
    'html.dark .stat-card { background: #1a1a1a !important; border-color: #2a2a2a !important; }',
    'html.dark .stat-big { color: #e05555 !important; }',
    'html.dark .stat-label { color: #555 !important; }',
    'html.dark .stat-note { color: #444 !important; }',
    'html.dark .refresh-note { color: #444 !important; }',
    'html.dark .refresh-note code { background: #222 !important; color: #aaa !important; }',

    /* Breakdown tables */
    'html.dark .breakdown-table th { background: #1e1e1e !important; color: #555 !important; }',
    'html.dark .breakdown-table td { border-color: #222 !important; color: #888 !important; }',
    'html.dark .breakdown-table td.num { color: #e05555 !important; }',

    /* Reader pulse */
    'html.dark .pulse-stat.yes { background: #0d1f0e !important; border-color: #1a3d1c !important; }',
    'html.dark .pulse-stat.no  { background: #1f0d0d !important; border-color: #3d1a1a !important; }',
    'html.dark .pulse-stat.neutral { background: #1a1a1a !important; border-color: #2a2a2a !important; }',
    'html.dark .pulse-lbl { color: #555 !important; }',

    /* Comment cards */
    'html.dark .comment-card { background: #1a1a1a !important; border-color: #2a2a2a !important; border-left-color: #b51c20 !important; }',
    'html.dark .comment-card p { color: #bbb !important; }',
    'html.dark .comment-card .meta { color: #555 !important; }',
    'html.dark .comment-section-label { color: #e05555 !important; }',
    'html.dark .empty-note { color: #444 !important; }',

    /* Quick links */
    'html.dark .quick-link { background: #1a1a1a !important; border-color: #2a2a2a !important; }',
    'html.dark .quick-link:hover { border-color: #b51c20 !important; }',
    'html.dark .ql-label { color: #444 !important; }',
    'html.dark .ql-title { color: #e05555 !important; }',
  ].join('\n');
  document.head.appendChild(style);

  // ── 3. Inject toggle button ───────────────────────────────────────────────
  document.addEventListener('DOMContentLoaded', function () {
    var header = document.querySelector('header');
    if (!header) return;
    if (header.style.position !== 'relative' && getComputedStyle(header).position === 'static') {
      header.style.position = 'relative';
    }
    var btn = document.createElement('button');
    btn.id = 'cc-theme-toggle';
    btn.title = 'Toggle dark / light mode';
    btn.innerHTML = isDark
      ? '<span style="font-size:13px">☀️</span> Light'
      : '<span style="font-size:13px">🌙</span> Dark';
    btn.addEventListener('click', function () {
      isDark = !isDark;
      document.documentElement.classList.toggle('dark', isDark);
      btn.innerHTML = isDark
        ? '<span style="font-size:13px">☀️</span> Light'
        : '<span style="font-size:13px">🌙</span> Dark';
      localStorage.setItem('cc-theme', isDark ? 'dark' : 'light');
    });
    header.appendChild(btn);
  });
})();
