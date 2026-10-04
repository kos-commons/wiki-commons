#!/usr/bin/env python3
"""Check internal links and anchors in a built mdBook site.

Usage:
    python3 tools/check_site.py <site-dir>

Every `href` in every HTML file under the site directory that is relative (not
http(s), mailto, or javascript) must resolve to an existing file, and a
`#fragment` on a link to an HTML file must match an `id` in that file. The
site's own chrome (sidebar, theme) is checked along with the content. Exit
status 1 if anything is broken.
"""
from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

SKIP = ("http://", "https://", "mailto:", "javascript:", "data:")


class Collector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if d.get("id"):
            self.ids.add(d["id"])
        if tag == "a" and d.get("name"):
            self.ids.add(d["name"])
        if tag in ("a", "link") and d.get("href"):
            self.hrefs.append(d["href"])
        if tag in ("img", "script") and d.get("src"):
            self.hrefs.append(d["src"])


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2
    site = Path(argv[1]).resolve()
    pages: dict[Path, Collector] = {}
    for html in site.rglob("*.html"):
        c = Collector()
        c.feed(html.read_text(encoding="utf-8", errors="replace"))
        pages[html] = c
    broken: list[str] = []
    checked = 0
    for html, c in pages.items():
        for href in c.hrefs:
            if href.startswith(SKIP) or href.startswith("#") and not href[1:]:
                continue
            parts = urlsplit(href)
            if parts.scheme or parts.netloc:
                continue
            checked += 1
            path = unquote(parts.path)
            if path == "":
                target = html
            elif path.startswith("/"):
                # site-url prefixed absolute path, e.g. /wiki-commons/...; strip the first segment
                segs = [s for s in path.split("/") if s]
                target = site.joinpath(*segs[1:]) if len(segs) > 1 else site
            else:
                target = (html.parent / path).resolve()
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                broken.append(f"{html.relative_to(site)}: missing {href}")
                continue
            frag = unquote(parts.fragment)
            if frag and target.suffix == ".html":
                ids = pages[target].ids if target in pages else set()
                if frag not in ids:
                    broken.append(f"{html.relative_to(site)}: no id #{frag} in {target.relative_to(site)}")
    for b in sorted(set(broken)):
        print("BROKEN", b)
    print(f"\n{len(pages)} pages, {checked} internal references checked, {len(set(broken))} broken")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
