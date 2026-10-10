"""Turn a Gmail HTML body into blocks of inline runs, keeping bold, italic and links.

blocks(html) -> list of Block(text, html, all_bold, all_italic, links)
`html` holds only <b>, <i> and <a href> markup, with text HTML-escaped.
"""
import html as htmllib
import re
from dataclasses import dataclass, field

from bs4 import BeautifulSoup, NavigableString, Tag

BLOCK_TAGS = {"p", "div", "li", "h1", "h2", "h3", "h4", "h5", "h6", "blockquote", "tr", "ul", "ol", "table"}


@dataclass
class Block:
    runs: list = field(default_factory=list)  # (text, bold, italic, href)

    @property
    def text(self) -> str:
        return re.sub(r"\s+", " ", "".join(r[0] for r in self.runs)).strip()

    @property
    def all_bold(self) -> bool:
        vis = [r for r in self.runs if r[0].strip()]
        return bool(vis) and all(r[1] for r in vis)

    @property
    def all_italic(self) -> bool:
        vis = [r for r in self.runs if r[0].strip()]
        return bool(vis) and all(r[2] for r in vis)

    @property
    def links(self) -> list:
        out = []
        for r in self.runs:
            if r[3] and r[3] not in out:
                out.append(r[3])
        return out

    def render(self, bold=True, italic=True, links=True, href_map=None) -> str:
        """Inline HTML. Adjacent runs with the same styling are merged; edge spaces sit outside tags."""
        merged = []
        for t, b, i, h in self.runs:
            t = re.sub(r"\s+", " ", t.replace("\xa0", " "))
            if not t:
                continue
            key = (b and bold, i and italic, (href_map or {}).get(h, h) if links else None)
            if not t.strip() and merged:      # whitespace joins whatever is around it
                merged[-1][0] += t
                continue
            if merged and merged[-1][1] == key:
                merged[-1][0] += t
            else:
                merged.append([t, key])
        out = ""
        for t, (b, i, h) in merged:
            lead = t[: len(t) - len(t.lstrip())]
            trail = t[len(t.rstrip()):]
            core = htmllib.escape(t.strip(), quote=False)
            if not core:
                out += t
                continue
            if i:
                core = f"<i>{core}</i>"
            if b:
                core = f"<b>{core}</b>"
            if h:
                core = f'<a href="{htmllib.escape(h, quote=True)}" target="_blank" rel="noopener">{core}</a>'
            out += lead + core + trail
        return re.sub(r"\s+", " ", out).strip()


def _style(tag: Tag) -> str:
    return (tag.get("style") or "").replace(" ", "").lower()


def blocks(html: str) -> list:
    soup = BeautifulSoup(html, "html.parser")
    out = [Block()]

    def walk(node, bold, ital, href):
        for ch in node.children:
            if isinstance(ch, NavigableString):
                if str(ch):
                    out[-1].runs.append((str(ch), bold, ital, href))
                continue
            if not isinstance(ch, Tag):
                continue
            name = ch.name.lower()
            if name in ("style", "script", "head"):
                continue
            if name == "br":
                out.append(Block())
                continue
            st = _style(ch)
            b = bold or name in ("b", "strong") or bool(re.search(r"font-weight:(bold|[6-9]00)", st))
            if re.search(r"font-weight:(normal|[1-4]00)", st):
                b = False
            i = ital or name in ("i", "em") or "font-style:italic" in st
            if "font-style:normal" in st:
                i = False
            h = ch.get("href") if name == "a" and ch.get("href") else href
            if name in BLOCK_TAGS:
                out.append(Block())
                walk(ch, b, i, h)
                out.append(Block())
            else:
                walk(ch, b, i, h)

    walk(soup, False, False, None)
    return [b for b in out if b.text]
