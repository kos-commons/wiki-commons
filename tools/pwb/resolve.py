"""Title normalization and free-link resolution (guidelines MKUP-5, NAV-6).

Resolution order, as recommended by MKUP-5: interwiki prefix; exact title or
path; alias; case-insensitive; normalized (Unicode NFC, runs of spaces,
underscores and hyphens collapsed, case folded); hierarchy fallback for bare
titles (same directory first, then a unique match anywhere, else ambiguous);
relative paths; otherwise dangling.
"""
from __future__ import annotations

import posixpath
import re
import unicodedata
from dataclasses import dataclass, field
from typing import Iterable, Optional
from urllib.parse import quote

SEP_RE = re.compile(r"[\s_\-]+")


def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s).strip()


def normalize(s: str) -> str:
    """Comparison key: NFC, trimmed, separator runs collapsed to one space, case folded."""
    return SEP_RE.sub(" ", nfc(s)).casefold()


def strip_md(path: str) -> str:
    return path[:-3] if path.lower().endswith(".md") else path


@dataclass
class Page:
    path: str                      # content-root-relative, "/" separated, with .md
    title: str
    aliases: list[str] = field(default_factory=list)
    kind: str = "page"

    @property
    def path_title(self) -> str:
        return strip_md(self.path)

    @property
    def directory(self) -> str:
        return posixpath.dirname(self.path)

    @property
    def basename(self) -> str:
        return strip_md(posixpath.basename(self.path))


@dataclass
class Resolution:
    path: Optional[str]
    via: str                       # interwiki | exact | alias | case | normalized | hierarchy | relative | self | ambiguous | dangling
    url: Optional[str] = None
    candidates: list[str] = field(default_factory=list)

    @property
    def resolved(self) -> bool:
        return self.path is not None or self.url is not None

    def to_dict(self) -> dict:
        d = {"path": self.path, "via": self.via}
        if self.url:
            d["url"] = self.url
        if self.candidates:
            d["candidates"] = self.candidates
        return d


class PageIndex:
    """Index of pages for free-link resolution.

    `pages_prefix` names a directory (such as "pages") that is stripped when a page's path is
    used as a title, so that [[Guides/Getting Started]] matches pages/Guides/Getting Started.md.
    """

    def __init__(self, pages: Iterable[Page] = (), *, namespaces: Iterable[str] = (), interwiki: Optional[dict] = None,
                 pages_prefix: str = ""):
        self.pages: list[Page] = []
        self.namespaces = set(namespaces)
        self.interwiki = dict(interwiki or {})
        self.pages_prefix = pages_prefix.rstrip("/") + "/" if pages_prefix else ""
        self._exact: dict[str, list[Page]] = {}
        self._alias: dict[str, list[Page]] = {}
        self._case: dict[str, list[Page]] = {}
        self._norm: dict[str, list[Page]] = {}
        self._base: dict[str, list[Page]] = {}
        for p in pages:
            self.add(p)

    def logical_path(self, path: str) -> str:
        p = strip_md(path)
        if self.pages_prefix and p.startswith(self.pages_prefix):
            return p[len(self.pages_prefix):]
        return p

    def add(self, page: Page) -> None:
        self.pages.append(page)
        for key in {nfc(page.title), nfc(self.logical_path(page.path)), nfc(page.path_title)}:
            self._exact.setdefault(key, []).append(page)
            self._case.setdefault(key.casefold(), []).append(page)
            self._norm.setdefault(normalize(key), []).append(page)
        for a in page.aliases:
            self._alias.setdefault(nfc(str(a)), []).append(page)
            self._norm.setdefault(normalize(str(a)), []).append(page)
        self._base.setdefault(normalize(page.basename), []).append(page)

    def resolve(self, target: str, from_path: Optional[str] = None) -> Resolution:
        target = nfc(target)
        if not target:
            return Resolution(from_path, "self")
        if ":" in target and not target.startswith(("/", ".")):
            prefix, rest = target.split(":", 1)
            if prefix in self.interwiki:
                return Resolution(None, "interwiki", url=self.interwiki[prefix].replace("{title}", quote(rest.strip())))
        if target.startswith(("./", "../")) and from_path is not None:
            cand = strip_md(posixpath.normpath(posixpath.join(posixpath.dirname(from_path), target)))
            for p in self.pages:
                if p.path_title == cand or self.logical_path(p.path) == cand:
                    return Resolution(p.path, "relative")
            return Resolution(None, "dangling")
        if target.startswith("/"):
            target = target[1:]
        for table, via in ((self._exact, "exact"), (self._alias, "alias")):
            hits = table.get(target)
            if hits:
                return self._pick(hits, via, from_path)
        hits = self._case.get(target.casefold())
        if hits:
            return self._pick(hits, "case", from_path)
        hits = self._norm.get(normalize(target))
        if hits:
            return self._pick(hits, "normalized", from_path)
        if "/" not in target:
            hits = self._base.get(normalize(target))
            if hits:
                return self._pick(hits, "hierarchy", from_path)
        return Resolution(None, "dangling")

    def _pick(self, hits: list[Page], via: str, from_path: Optional[str]) -> Resolution:
        uniq: list[Page] = []
        for h in hits:
            if h not in uniq:
                uniq.append(h)
        if len(uniq) == 1:
            return Resolution(uniq[0].path, via)
        if from_path is not None:
            here = posixpath.dirname(from_path)
            same = [p for p in uniq if p.directory == here]
            if len(same) == 1:
                return Resolution(same[0].path, via)
        return Resolution(uniq[0].path, "ambiguous", candidates=[p.path for p in uniq])

    def by_path(self, path: str) -> Optional[Page]:
        for p in self.pages:
            if p.path == path:
                return p
        return None

    def title_of(self, path: str) -> Optional[str]:
        p = self.by_path(path)
        return p.title if p else None
