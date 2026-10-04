"""Optional external converters: Pandoc, when installed, for formats the built-in code does not cover."""
from __future__ import annotations

import os
import shutil
import subprocess
from functools import lru_cache
from typing import Optional


@lru_cache(maxsize=1)
def pandoc_path() -> Optional[str]:
    env = os.environ.get("WIKI_COMMONS_PANDOC")
    if env == "off":
        return None  # force the built-in converters even when pandoc is installed
    if env and os.path.exists(env):
        return env
    return shutil.which("pandoc")


def pandoc_available() -> bool:
    return pandoc_path() is not None


def pandoc(text: str, src: str, dst: str, *extra: str) -> Optional[str]:
    path = pandoc_path()
    if not path:
        return None
    proc = subprocess.run([path, "-f", src, "-t", dst, "--wrap=none", *extra], input=text.encode("utf-8"),
                          capture_output=True, check=False)
    if proc.returncode != 0:
        return None
    return proc.stdout.decode("utf-8")


def html_to_markdown(html: str) -> Optional[str]:
    return pandoc(html, "html", "gfm")


def wikitext_to_markdown(wikitext: str) -> Optional[str]:
    """Wikitext -> Portable Wiki Markdown through Pandoc's mediawiki reader, restoring free links."""
    out = pandoc(wikitext, "mediawiki", "gfm")
    if out is None:
        return None
    import re
    from urllib.parse import unquote

    def wl(target: str, label: str) -> str:
        target = unquote(target).replace("_", " ").strip()
        label = label.strip()
        return f"[[{target}]]" if label == target or not label else f"[[{target}|{label}]]"

    # pandoc's gfm writer renders wiki links as <a href="Target" class="wikilink" title="...">label</a>
    out = re.sub(r'<a href="([^"]+)" class="wikilink"(?: title="[^"]*")?>(.*?)</a>', lambda m: wl(m.group(1), m.group(2)), out, flags=re.S)
    out = re.sub(r'\[([^\]]*)\]\(([^)\s]+) "wikilink"\)', lambda m: wl(m.group(2), m.group(1)), out)
    out = re.sub(r'<span id="[^"]*"></span>\n*', "", out)          # heading anchor spans from the reader
    out = re.sub(r"\n?<references\s*/>\n?", "\n", out)             # reference list placeholder
    return out


def markdown_to_wikitext(markdown: str) -> Optional[str]:
    return pandoc(markdown, "commonmark_x+wikilinks_title_after_pipe-gfm_auto_identifiers", "mediawiki")
