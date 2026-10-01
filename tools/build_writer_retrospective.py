#!/usr/bin/env python3
"""
tools/build_writer_retrospective.py — build a standalone writer retrospective under
writers/<slug>/ from the old-site archive in Google Drive plus articles on the current site.

Run by /writer-retrospective (.claude/commands/writer-retrospective.md). Dev2-only tooling.

What a retrospective is (John, Oct 1, 2026):
  - the magazine's own look and feel (logo header, Playfair/Lato, article-category /
    article-title / article-meta, magazine figure and nav styling, dark footer)
  - NO links to the magazine: nothing in the header, footer or body points at the main site,
    and nothing on the main site links to the retrospective
  - pagination between the article pages: Previous / Next with thumbnails and "n of N"
  - article text verbatim; photos under their original filenames

Usage:
    source .venv/bin/activate
    python3 tools/build_writer_retrospective.py tools/retrospectives/<slug>.json --find
    python3 tools/build_writer_retrospective.py tools/retrospectives/<slug>.json

  --find   search the Drive archive for the writer's byline and list candidate articles
           (nothing is built); use it to fill "archive_articles" in the config
  (none)   download what is missing into .retrospective-cache/, build writers/<slug>/,
           and verify text, local references and outbound links

The old site lives in Drive at
  !    CCM ARCHIVE/ccm-restore/restore/20260208/classicchicagomagazine.com/<old-slug>/index.html
with photos under wp-content/uploads/YYYY/MM/. It is read with the local OAuth token
(~/.gmail-mcp), which carries the drive.readonly scope. Queries are always scoped to the
archive folders; never search the whole Drive by filename.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote

import requests
from bs4 import BeautifulSoup, Tag
from PIL import Image, ImageOps

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
from gmail_api import get_access_token  # noqa: E402

CACHE_ROOT = REPO / ".retrospective-cache"
API = "https://www.googleapis.com/drive/v3/files"
FOLDER = "application/vnd.google-apps.folder"
# classicchicagomagazine.com (recovered copy) and classicchicagomagazine.com-original
ARCHIVE_SITES = ["1kRqG96H9OGMDbaE06Fo7Ay-snBjFtjLp", "1iLLX51qWu_zyOqVAOldF9-WGVbgsbT1f"]
MISSING_NOTE = "Photo not recovered from the archive"
KEEP_TAGS = {"p", "em", "i", "b", "strong", "sup", "sub", "a", "ul", "ol", "li", "h2", "h3", "h4", "blockquote",
             "br", "table", "tbody", "tr", "td", "th", "span", "img", "figure", "figcaption", "u"}

# ── Google Drive (read-only) ──────────────────────────────────────────────────

_token: dict = {}
_folder_cache: dict[tuple[str, str], str | None] = {}
_listing_cache: dict[str, dict[str, str]] = {}


def _headers() -> dict:
    if not _token or time.time() - _token["t"] > 1800:
        _token.update(v=get_access_token(), t=time.time())
    return {"Authorization": f"Bearer {_token['v']}"}


def drive_query(q: str) -> list[dict]:
    out, page = [], None
    while True:
        params = {"q": q, "fields": "files(id,name,mimeType,parents),nextPageToken", "pageSize": 1000}
        if page:
            params["pageToken"] = page
        r = requests.get(API, headers=_headers(), params=params, timeout=60)
        r.raise_for_status()
        d = r.json()
        out += d.get("files", [])
        page = d.get("nextPageToken")
        if not page:
            return out


def drive_download(file_id: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    r = requests.get(f"{API}/{file_id}", headers=_headers(), params={"alt": "media"}, timeout=180)
    r.raise_for_status()
    dest.write_bytes(r.content)


def child_folder(parent: str, name: str) -> str | None:
    key = (parent, name)
    if key not in _folder_cache:
        safe = name.replace("'", "\\'")
        r = drive_query(f"'{parent}' in parents and name = '{safe}' and mimeType = '{FOLDER}' and trashed = false")
        _folder_cache[key] = r[0]["id"] if r else None
    return _folder_cache[key]


def folder_listing(folder_id: str) -> dict[str, str]:
    if folder_id not in _listing_cache:
        _listing_cache[folder_id] = {f["name"]: f["id"]
                                     for f in drive_query(f"'{folder_id}' in parents and trashed = false")}
    return _listing_cache[folder_id]


def fetch_page(old_slug: str, dest: Path) -> None:
    for site in ARCHIVE_SITES:
        fid = child_folder(site, old_slug)
        index = folder_listing(fid).get("index.html") if fid else None
        if index:
            drive_download(index, dest)
            return
    raise SystemExit(f"'{old_slug}' has no index.html in the Drive archive")


def image_candidates(img: Tag) -> list[str]:
    """Upload paths for one <img>: full-size original first, then the sizes the page referenced."""
    srcs = [img.get("src") or ""] + [p.strip().split(" ")[0] for p in (img.get("srcset") or "").split(",") if p.strip()]
    paths: list[str] = []
    for s in srcs:
        s = unquote(s.split("?")[0])
        if "/wp-content/uploads/" not in s:
            continue
        s = s[s.index("/wp-content/uploads/"):]
        for c in (re.sub(r"-\d+x\d+(\.\w+)$", r"\1", s), s):
            if c not in paths:
                paths.append(c)
    return sorted(paths, key=lambda p: bool(re.search(r"-\d+x\d+\.\w+$", p)))


def fetch_image(img: Tag, dest_dir: Path) -> str | None:
    for path in image_candidates(img):
        m = re.match(r"/wp-content/uploads/(\d{4})/(\d{2})/(.+)$", path)
        if not m:
            continue
        year, month, name = m.groups()
        if (dest_dir / name).exists():
            return name
        for site in ARCHIVE_SITES:
            fid: str | None = site
            for part in ("wp-content", "uploads", year, month):
                fid = child_folder(fid, part) if fid else None
            file_id = folder_listing(fid).get(name) if fid else None
            if file_id:
                drive_download(file_id, dest_dir / name)
                return name
    return None

# ── Finding a writer's articles ───────────────────────────────────────────────


def entry_content(page_html: str) -> tuple[BeautifulSoup, Tag]:
    soup = BeautifulSoup(page_html, "html.parser")
    ec = soup.find(class_="entry-content")
    if ec is None:
        raise SystemExit("page has no .entry-content block")
    for junk in ec.find_all(class_=re.compile(r"sharedaddy|sd-|jp-relatedposts")):
        junk.decompose()
    for junk in ec.find_all(["script", "style", "noscript", "iframe"]):
        junk.decompose()
    return soup, ec


def has_byline(ec: Tag, byline_re: re.Pattern) -> bool:
    for p in ec.find_all(["p", "h2", "h3", "h4"]):
        text = re.sub(r"\s+", " ", p.get_text(" ").replace(" ", " ")).strip()
        if byline_re.match(text):
            return True
    return False


def find_articles(cfg: dict, cache: Path) -> None:
    """Full-text search limited to pages inside the archive's slug folders, then confirm the byline
    in the article body (the old site's sidebars mention many writers, so the search alone over-matches)."""
    byline_re = re.compile(cfg["byline_pattern"], re.I)
    slug_of = {}
    for site in ARCHIVE_SITES:
        for k in drive_query(f"'{site}' in parents and mimeType = '{FOLDER}' and trashed = false"):
            slug_of.setdefault(k["id"], k["name"])
    hits: dict[str, str] = {}
    for phrase in cfg["search_phrases"]:
        safe = phrase.replace("'", "\\'")
        for f in drive_query(f"mimeType = 'text/html' and fullText contains '\"{safe}\"' and trashed = false"):
            parent = (f.get("parents") or [""])[0]
            if parent in slug_of:
                hits.setdefault(slug_of[parent], f["id"])
    print(f"{len(hits)} archive pages mention {cfg['search_phrases']}; checking bylines…")

    def get(item: tuple[str, str]) -> str:
        dest = cache / "candidates" / f"{item[0]}.html"
        if not dest.exists():
            drive_download(item[1], dest)
        return item[0]

    with ThreadPoolExecutor(8) as ex:
        list(ex.map(get, sorted(hits.items())))
    found = []
    for slug in sorted(hits):
        soup, ec = entry_content((cache / "candidates" / f"{slug}.html").read_text(encoding="utf-8", errors="replace"))
        if has_byline(ec, byline_re):
            t = soup.find("time")
            found.append((t["datetime"][:10] if t else "", slug, soup.find("h1").get_text(" ", strip=True)))
    known = {a["old_slug"] for a in cfg.get("archive_articles", [])}
    print(f"\n{len(found)} articles carry the byline in the article body:")
    for date, slug, title in sorted(found):
        print(f"  {date}  {'(in config)' if slug in known else '(NEW)     '}  {slug}\n              {title}")

# ── Cleaning articles ─────────────────────────────────────────────────────────


def clean_style(tag: Tag) -> None:
    style = tag.get("style", "")
    keep = []
    for decl in style.split(";"):
        if ":" in decl:
            k, v = (x.strip().lower() for x in decl.split(":", 1))
            if k in ("font-weight", "font-style", "text-decoration"):
                keep.append(f"{k}:{v}")
    centered = "text-align" in style.lower() and "center" in style.lower()
    attrs = {"href": tag["href"]} if tag.name == "a" and tag.get("href") else {}
    tag.attrs = attrs
    if keep:
        tag["style"] = ";".join(keep)
    if centered and tag.name in ("p", "h2", "h3", "h4"):
        tag["class"] = ["center"]


def place_photo(src: Path, dest: Path) -> str:
    """Copy a photo under its original filename; shrink only if very large or stored sideways.
    Returns 'wide' or 'tall' for layout."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    im = Image.open(src)
    upright = ImageOps.exif_transpose(im)
    if max(im.size) > 2000 or src.stat().st_size > 1_500_000 or upright.size != im.size:
        upright.thumbnail((2000, 2000), Image.LANCZOS)
        if src.suffix.lower() in (".jpg", ".jpeg"):
            upright.convert("RGB").save(dest, "JPEG", quality=82, optimize=True)
        else:
            upright.save(dest, optimize=True)
    else:
        shutil.copy2(src, dest)
    return "wide" if upright.width >= upright.height * 1.15 else "tall"


def archive_article(entry: dict, cfg: dict, cache: Path, out: Path) -> dict:
    old_slug, slug = entry["old_slug"], entry["slug"]
    page = cache / "pages" / f"{old_slug}.html"
    if not page.exists():
        fetch_page(old_slug, page)
    soup, ec = entry_content(page.read_text(encoding="utf-8", errors="replace"))
    title = re.sub(r"\s+", " ", soup.find("h1").get_text(" ", strip=True).replace(" ", " "))
    date = datetime.fromisoformat(soup.find("time")["datetime"]).replace(tzinfo=None)
    byline_re = re.compile(cfg["byline_pattern"], re.I)
    kicker_re = re.compile(cfg["kicker_pattern"], re.I) if cfg.get("kicker_pattern") else None
    source_text = ec.get_text(" ")
    stats = {"photos": 0, "missing": 0}
    removed: list[str] = []
    byline = None

    for img in ec.find_all("img"):
        width = int(re.sub(r"\D", "", img.get("width") or "0") or 0)
        if 0 < width < 200 and "alignleft" in (img.get("class") or []):
            img.decompose()        # the author headshot that opened each old-site column
            continue
        name = fetch_image(img, cache / "imgs" / old_slug)
        if name:
            shape = place_photo(cache / "imgs" / old_slug / name, out / slug / name)
            fig = soup.new_tag("figure")
            fig["class"] = [shape]
            fig.append(soup.new_tag("img", src=name, alt=""))
            img.replace_with(fig)
            stats["photos"] += 1
        else:
            note = soup.new_tag("p")
            note["class"] = ["missing"]
            note.string = f"[{MISSING_NOTE}]"
            img.replace_with(note)
            stats["missing"] += 1

    for t in list(ec.find_all(True)):
        if t.name not in KEEP_TAGS:
            t.unwrap()
    for t in ec.find_all(True):
        if t.name == "img" or (t.name in ("p", "figure") and t.get("class") and t["class"][0] in ("missing", "wide", "tall")):
            continue
        clean_style(t)
    for t in list(ec.find_all("span")):
        if not t.get("style"):
            t.unwrap()
    for a in list(ec.find_all("a")):
        href = a.get("href") or ""
        if not href or href.startswith("/") or re.search(r"classicchicagomagazine\.com|chicagoclassicmag\.com", href):
            a.unwrap()             # photo links and links into the magazine are dropped; the text stays
        else:
            a["target"] = "_blank"
            a["rel"] = "noopener"

    for p in list(ec.find_all(["p", "h2", "h3", "h4"])):
        text = re.sub(r"\s+", " ", p.get_text(" ").replace(" ", " ")).strip()
        fig = p.find("figure")
        if fig:
            if not text:
                p.replace_with(fig.extract())
            continue
        if not text:
            p.decompose()
        elif kicker_re and kicker_re.match(text):
            removed.append(text)
            p.decompose()
        elif byline is None and byline_re.match(text):
            byline = text
            removed.append(text)
            p.decompose()

    for fig in ec.find_all("figure"):      # a centered paragraph straight after a photo is its caption
        nxt = fig.find_next_sibling()
        if isinstance(nxt, Tag) and nxt.name == "p" and "center" in (nxt.get("class") or []):
            cap = soup.new_tag("figcaption")
            for child in list(nxt.contents):
                cap.append(child.extract())
            nxt.decompose()
            fig.append(cap)
            fig.img["alt"] = re.sub(r"\s+", " ", cap.get_text(" ")).strip()

    return {"slug": slug, "title": title, "date": date, "byline": byline or f"By {cfg['author']}",
            "body": "".join(str(c) for c in ec.contents), "stats": stats,
            "source_text": source_text, "removed": removed}


def current_article(entry: dict, cfg: dict, out: Path) -> dict:
    slug = entry["slug"]
    src_dir = REPO / "editions" / entry["edition"] / entry.get("edition_slug", slug)
    soup = BeautifulSoup((src_dir / "index.html").read_text(encoding="utf-8"), "html.parser")
    body = soup.find(class_="article-body")
    source_text = body.get_text(" ")
    stats = {"photos": 0, "missing": 0}
    for img in body.find_all("img"):
        name = unquote(img["src"])
        shape = place_photo(src_dir / name, out / slug / name)
        img.attrs = {"src": name, "alt": img.get("alt", "")}
        if img.parent.name == "figure":
            img.parent["class"] = [shape]
        stats["photos"] += 1
    for t in body.find_all(True):
        if t.name in ("img", "figure"):
            continue
        cls = [c for c in (t.get("class") or []) if c in ("question", "qa-question", "pullquote")]
        href = t.get("href")
        t.attrs = {}
        if cls:
            t["class"] = cls
        if href and not re.match(r"(\.\./|/|https?://(www\.)?(chicagoclassicmag|classicchicagomagazine)\.com)", href):
            t["href"], t["target"], t["rel"] = href, "_blank", "noopener"
    for a in list(body.find_all("a")):
        if not a.get("href"):
            a.unwrap()
    meta = soup.find(class_="article-meta")
    byline = entry.get("byline") or re.split(r"\s*[••]\s*", meta.get_text(" ", strip=True))[0]
    return {"slug": slug, "title": soup.find("h1").get_text(" ", strip=True),
            "date": datetime.strptime(entry["edition"], "%Y-%m-%d"), "byline": byline,
            "body": "".join(str(c) for c in body.contents), "stats": stats,
            "source_text": source_text, "removed": []}

# ── Magazine-look page shell ──────────────────────────────────────────────────

CSS = """
    *, *::before, *::after { box-sizing: border-box; }
    body { margin: 0; font-family: Georgia, "Times New Roman", serif; background: #fff; color: #222; line-height: 1.7; -webkit-font-smoothing: antialiased; }
    header { padding: 20px 0; border-bottom: 1px solid #eee; }
    .logo-container { text-align: center; margin-bottom: 20px; }
    .logo-container img { width: 390px; max-width: 80%; height: auto; }
    nav { border-top: 1px solid #eee; border-bottom: 1px solid #eee; padding: 10px 0; }
    .nav-inner { max-width: 1200px; margin: 0 auto; padding: 0 16px; display: flex; justify-content: center; flex-wrap: wrap; }
    .nav-inner a, .nav-inner span { font-family: 'Lato', sans-serif; font-size: 16px; font-weight: 400; color: #d41f1f; text-decoration: none; text-transform: uppercase; margin: 0 15px; padding: 5px 0; letter-spacing: 0.05em; }
    .nav-inner span { color: #888; }
    .nav-inner a:hover { color: #b51c20; text-decoration: underline; }
    .article-wrapper { max-width: 780px; margin: 0 auto 60px; padding: 0 20px; }
    .article-category { font-family: 'Lato', sans-serif; font-size: 11px; font-weight: 700; color: #b51c20; text-transform: uppercase; letter-spacing: 0.2em; text-align: center; margin: 40px 0 12px; }
    h1.article-title { font-family: 'Playfair Display', Georgia, serif; font-size: 42px; font-weight: 700; line-height: 1.2; text-align: center; margin: 0 0 14px; color: #111; }
    .article-meta { font-family: 'Lato', sans-serif; font-size: 13px; color: #888; text-align: center; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 32px; border-bottom: 1px solid #eee; padding-bottom: 24px; }
    .article-body p { font-size: 17px; color: #333; margin: 0 0 20px; }
    .article-body p.center { text-align: center; }
    .article-body p.question, .article-body p.qa-question { font-weight: 700; }
    .article-body p.missing { font-family: 'Lato', sans-serif; font-size: 12px; color: #aaa; text-align: center; text-transform: uppercase; letter-spacing: 0.08em; border: 1px dashed #ddd; padding: 26px 12px; margin: 36px 10% 8px; }
    .article-body p.missing + p.center { font-family: 'Lato', sans-serif; font-size: 12px; color: #888; font-style: italic; margin-bottom: 36px; }
    .article-body h2, .article-body h3, .article-body h4 { font-family: 'Playfair Display', Georgia, serif; font-weight: 700; color: #111; margin: 36px 0 14px; }
    .article-body h2 { font-size: 24px; } .article-body h3 { font-size: 21px; } .article-body h4 { font-size: 18px; }
    .article-body a { color: #b51c20; }
    .article-body blockquote, .article-body .pullquote { font-size: 20px; font-style: italic; color: #555; border-left: 4px solid #b51c20; padding: 10px 20px; margin: 30px 0; }
    .article-body table { border-collapse: collapse; margin: 24px 0; }
    .article-body td, .article-body th { border: 1px solid #eee; padding: 6px 10px; vertical-align: top; font-size: 16px; }
    figure { margin: 36px 0; }
    figure img { width: 100%; height: auto; display: block; }
    figure.tall img { width: auto; max-width: 100%; max-height: 680px; margin: 0 auto; }
    figure figcaption { font-family: 'Lato', sans-serif; font-size: 12px; color: #888; text-align: center; margin-top: 8px; font-style: italic; }
    .retro-nav { display: flex; justify-content: space-between; align-items: center; gap: 16px; margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; }
    .back-link { display: inline-flex; align-items: center; gap: 10px; max-width: 42%; font-family: 'Lato', sans-serif; font-size: 14px; line-height: 1.4; text-transform: uppercase; color: #b51c20; text-decoration: none; }
    .back-link span { border-bottom: 1px dashed #b51c20; }
    .back-link:hover span { color: #d41f1f; border-bottom: 1px solid #d41f1f; }
    .back-link.next { text-align: right; margin-left: auto; }
    .nav-thumb { width: 70px; height: 70px; object-fit: cover; object-position: center 25%; display: block; flex-shrink: 0; }
    .retro-nav-count { font-family: 'Lato', sans-serif; font-size: 12px; color: #999; text-transform: uppercase; letter-spacing: 0.08em; white-space: nowrap; }
    .page-head { text-align: center; padding: 24px 16px 10px; }
    .page-head h1 { font-family: 'Playfair Display', Georgia, serif; font-size: 36px; font-weight: 700; margin: 0 0 6px; color: #222; }
    .page-head .sub { font-family: 'Lato', sans-serif; font-size: 14px; letter-spacing: 0.12em; text-transform: uppercase; color: #999; margin-bottom: 12px; }
    .wrapper { max-width: 1200px; margin: 0 auto; padding: 0 16px 60px; }
    .index-intro { max-width: 780px; margin: 8px auto 10px; text-align: center; font-size: 18px; color: #555; font-style: italic; }
    .index-note { max-width: 780px; margin: 0 auto 26px; text-align: center; font-family: 'Lato', sans-serif; font-size: 13px; color: #999; }
    .card-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-top: 30px; padding-top: 30px; border-top: 1px solid #eee; }
    .article-card { display: block; text-decoration: none; color: inherit; border-bottom: 1px solid #eee; padding-bottom: 24px; }
    .card-thumb, .card-thumb-placeholder { width: 100%; height: 300px; object-fit: cover; object-position: center 25%; display: block; border-radius: 3px; margin-bottom: 14px; background: #f0ebe3; }
    .card-thumb-placeholder { display: flex; align-items: center; justify-content: center; }
    .card-thumb-placeholder span { font-family: 'Lato', sans-serif; font-size: 11px; color: #b9b0a3; text-transform: uppercase; letter-spacing: 0.12em; }
    .card-title { font-family: 'Playfair Display', Georgia, serif; font-size: 22px; font-weight: 700; line-height: 1.3; color: #222; margin: 0 0 6px; }
    .article-card:hover .card-title { color: #b51c20; }
    .card-date { font-family: 'Lato', sans-serif; font-size: 12px; color: #999; text-transform: uppercase; letter-spacing: 0.03em; }
    footer { background: #333; color: #fff; padding: 40px 20px; text-align: center; margin-top: 60px; }
    .copyright { font-family: 'Lato', sans-serif; font-size: 14px; color: #aaa; }
    @media (max-width: 700px) { .card-grid { grid-template-columns: 1fr; } }
    @media (max-width: 600px) {
      h1.article-title { font-size: 32px; }
      .article-body p { font-size: 16px; }
      .retro-nav-count { display: none; }
      .back-link { max-width: 48%; font-size: 12px; }
    }
"""
FONTS = ("https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,800;1,400"
         "&family=Lato:ital,wght@0,300;0,400;0,700;1,300;1,400&display=swap")
FOOTER = """  <footer>
    <div class="copyright">
      COPYRIGHT &copy; Classic Chicago Magazine.<br>
      All rights reserved.
    </div>
  </footer>
</body>
</html>
"""


def head(title: str, author: str, up: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{html.escape(title)} | {html.escape(author)} | Classic Chicago Magazine</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex">
  <link href="{FONTS}" rel="stylesheet">
  <style>{CSS}  </style>
</head>

<body>
  <header>
    <div class="logo-container">
      <a href="{up}index.html"><img src="{up}logo.jpg" alt="Classic Chicago Magazine"></a>
    </div>
"""


def first_photo(body: str) -> str | None:
    m = re.search(r'<img[^>]+src="([^"]+)"', body)
    return html.unescape(m.group(1)) if m else None


def write_site(cfg: dict, arts: list[dict], out: Path) -> None:
    author, column, total = cfg["author"], cfg["column"], len(arts)
    shutil.copy2(REPO / "logo.jpg", out / "logo.jpg")
    for i, a in enumerate(arts):
        def link(j: int, kind: str) -> str:
            if j < 0 or j >= total:
                text = "&larr; All Articles" if kind == "prev" else "All Articles &rarr;"
                return f'<a href="../index.html" class="back-link {kind}"><span>{text}</span></a>'
            n = arts[j]
            thumb = (f'<img src="../{n["slug"]}/{html.escape(n["thumb"], quote=True)}" class="nav-thumb retro-nav-thumb" alt="">'
                     if n["thumb"] else "")
            title = html.escape(n["title"])
            if kind == "prev":
                return f'<a href="../{n["slug"]}/" class="back-link prev">{thumb}<span>&larr; Previous: {title}</span></a>'
            return f'<a href="../{n["slug"]}/" class="back-link next"><span>Next: {title} &rarr;</span>{thumb}</a>'

        page = head(a["title"], author, "../") + f"""    <nav>
      <div class="nav-inner">
        <a href="../index.html">All Articles</a>
      </div>
    </nav>
  </header>

  <main>
    <div class="article-wrapper">

      <div class="article-category">{html.escape(column)}</div>

      <h1 class="article-title">{html.escape(a["title"])}</h1>

      <div class="article-meta">{html.escape(a["byline"])} &nbsp;&bull;&nbsp; {a["date"].strftime("%B %-d, %Y")}</div>

      <div class="article-body">
{a["body"]}
      </div><!-- end article-body -->

      <!-- Pagination: order matches the index page (newest first) -->
      <div class="retro-nav">
        {link(i - 1, "prev")}
        <span class="retro-nav-count">{i + 1} of {total}</span>
        {link(i + 1, "next")}
      </div>

    </div><!-- end article-wrapper -->
  </main>

""" + FOOTER
        (out / a["slug"]).mkdir(exist_ok=True)
        (out / a["slug"] / "index.html").write_text(page, encoding="utf-8")

    blocks = ['    <div class="card-grid">\n']
    for a in arts:
        thumb = (f'<img class="card-thumb" src="{a["slug"]}/{html.escape(a["thumb"], quote=True)}" alt="">'
                 if a["thumb"] else '<div class="card-thumb-placeholder"><span>Photographs not recovered</span></div>')
        blocks.append(f'<a class="article-card" href="{a["slug"]}/index.html">\n  {thumb}\n'
                      f'  <div class="card-title">{html.escape(a["title"])}</div>\n'
                      f'  <div class="card-date">{a["date"].strftime("%B %-d, %Y")}</div>\n</a>\n')
    blocks.append("    </div>\n")
    years = f'{arts[-1]["date"].year}&ndash;{arts[0]["date"].year}'
    missing = sum(a["stats"]["missing"] for a in arts)
    note = cfg.get("note", "")
    if missing and "{missing}" in note:
        note = note.replace("{missing}", str(missing))
    index = head(column, author, "") + f"""    <nav>
      <div class="nav-inner">
        <span>{total} Articles</span>
      </div>
    </nav>
  </header>

  <div class="page-head">
    <h1>{html.escape(column)}</h1>
    <div class="sub">{html.escape(author)} &nbsp;&bull;&nbsp; {years}</div>
  </div>

  <main class="wrapper">
    <p class="index-intro">{cfg.get("intro", "")}</p>
    {f'<p class="index-note">{note}</p>' if note else ''}
{"".join(blocks)}  </main>

""" + FOOTER
    (out / "index.html").write_text(index, encoding="utf-8")

# ── Verification ──────────────────────────────────────────────────────────────


def norm(s: str) -> str:
    return re.sub(r"\s+", "", html.unescape(s).replace(" ", ""))


def verify(cfg: dict, arts: list[dict], out: Path) -> bool:
    ok = True
    print("\nVerification")
    for a in arts:
        page = BeautifulSoup((out / a["slug"] / "index.html").read_text(encoding="utf-8"), "html.parser")
        built = norm(page.find(class_="article-body").get_text(" ")).replace(norm(f"[{MISSING_NOTE}]"), "")
        source = norm(a["source_text"])
        for r in a["removed"]:
            source = source.replace(norm(r), "", 1)
        same = built == source
        ok &= same
        print(f"  {'✓' if same else '✗'} {a['date']:%Y-%m-%d}  {a['slug']:36} photos {a['stats']['photos']:2}"
              f"  missing {a['stats']['missing']}  text {'identical' if same else 'DIFFERS'} ({len(built)} chars)")
    broken, to_magazine = [], []
    for page in out.rglob("index.html"):
        raw = re.sub(r"<!--.*?-->", "", page.read_text(encoding="utf-8"), flags=re.S)
        for ref in re.findall(r'\b(?:href|src)="([^"]+)"', raw):
            ref = html.unescape(ref)
            if re.match(r"https?://", ref):
                if re.search(r"chicagoclassicmag\.com|classicchicagomagazine\.com|2ccmag\.com|article-dev", ref):
                    to_magazine.append((page.parent.name, ref))
                continue
            if ref.startswith(("#", "mailto:")):
                continue
            target = (page.parent / unquote(ref)).resolve()
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                broken.append((page.parent.name, ref))
            elif out.resolve() not in target.parents:
                to_magazine.append((page.parent.name, ref))
    slug = out.name
    inbound = [str(p.relative_to(REPO)) for p in list(REPO.glob("*.html")) + list((REPO / "editions").rglob("index.html"))
               if f"writers/{slug}" in p.read_text(encoding="utf-8", errors="replace")]
    for label, items in (("broken local references", broken), ("links into the magazine", to_magazine),
                         ("magazine pages linking to this retrospective", inbound)):
        print(f"  {'✓' if not items else '✗'} {label}: {items[:6] or 'none'}")
        ok &= not items
    return ok

# ── Main ──────────────────────────────────────────────────────────────────────


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("config", type=Path, help="tools/retrospectives/<slug>.json")
    ap.add_argument("--find", action="store_true", help="list candidate articles in the Drive archive; build nothing")
    args = ap.parse_args()
    cfg = json.loads(args.config.read_text(encoding="utf-8"))
    for key in ("slug", "author", "column", "byline_pattern", "search_phrases"):
        if not cfg.get(key):
            raise SystemExit(f"config is missing '{key}'")
    if not re.fullmatch(r"[a-z0-9-]+", cfg["slug"]):
        raise SystemExit("slug must be lowercase letters, digits and hyphens")
    cache = CACHE_ROOT / cfg["slug"]
    if args.find:
        find_articles(cfg, cache)
        return 0

    out = REPO / "writers" / cfg["slug"]
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    arts = [archive_article(e, cfg, cache, out) for e in cfg.get("archive_articles", [])]
    arts += [current_article(e, cfg, out) for e in cfg.get("current_articles", [])]
    if not arts:
        raise SystemExit("config lists no articles; run with --find first")
    slugs = [a["slug"] for a in arts]
    if len(set(slugs)) != len(slugs):
        raise SystemExit("duplicate article slugs in config")
    for a in arts:
        a["thumb"] = first_photo(a["body"])
    arts.sort(key=lambda a: a["date"], reverse=True)
    write_site(cfg, arts, out)
    size = sum(f.stat().st_size for f in out.rglob("*") if f.is_file()) / 1e6
    print(f"built writers/{cfg['slug']}/: {len(arts)} articles, {size:.1f} MB")
    return 0 if verify(cfg, arts, out) else 1


if __name__ == "__main__":
    sys.exit(main())
