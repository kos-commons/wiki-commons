#!/usr/bin/env python3
"""Check relative Markdown links and heading anchors across this repository.

Usage:
    python3 tools/check_links.py [root-dir]

For every *.md file under the root (default: the repository root), every
relative link target must exist, and every `#fragment` must match a heading
anchor in the target file, using GitHub's anchor algorithm (lower-case, strip
punctuation except hyphens and spaces, spaces to hyphens, duplicates suffixed
-1, -2, ...). Links inside code spans and fenced code blocks are ignored, as
are absolute URLs and mailto links. Exit status 1 if any link is broken.
"""
from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote

INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
LINK_RE = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$", re.M)
SKIP_SCHEMES = ("http://", "https://", "mailto:", "urn:")



def strip_fences(text: str) -> str:
    """Remove fenced code blocks, detecting fences line by line (``` or ~~~)."""
    out, fence = [], None
    for line in text.split("\n"):
        stripped = line.lstrip()
        if fence is None and (stripped.startswith("```") or stripped.startswith("~~~")):
            fence = stripped[:3]
            continue
        if fence is not None:
            if stripped.startswith(fence):
                fence = None
            continue
        out.append(line)
    return "\n".join(out)

def github_anchor(text: str) -> str:
    text = re.sub(r"`([^`]*)`", r"\1", text)            # code spans
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)  # links
    text = re.sub(r"[*_~]+", "", text)                    # emphasis
    text = unicodedata.normalize("NFC", text).lower()
    out = []
    for ch in text:
        if ch == " " or ch == "-":
            out.append("-" if ch == "-" else " ")
        elif ch.isalnum() or ch == "_" or unicodedata.category(ch).startswith(("L", "N", "M")):
            out.append(ch)
    return "".join(out).replace(" ", "-")


def anchors_of(path: Path) -> set[str]:
    text = strip_fences(path.read_text(encoding="utf-8"))
    seen: dict[str, int] = {}
    result: set[str] = set()
    for m in HEADING_RE.finditer(text):
        a = github_anchor(m.group(2))
        if a in seen:
            seen[a] += 1
            result.add(f"{a}-{seen[a]}")
        else:
            seen[a] = 0
            result.add(a)
    return result


def main(argv: list[str]) -> int:
    root = Path(argv[1]).resolve() if len(argv) > 1 else Path(__file__).resolve().parent.parent
    anchor_cache: dict[Path, set[str]] = {}
    broken: list[str] = []
    checked = 0
    for md in sorted(root.rglob("*.md")):
        rel_parts = md.relative_to(root).parts
        if ".git" in md.parts or rel_parts[:1] == ("book",):
            continue
        if rel_parts[:1] == ("corpus",) and len(rel_parts) > 2:
            continue  # corpus case files are test data, not documents
        text = strip_fences(md.read_text(encoding="utf-8"))
        text = INLINE_CODE_RE.sub("", text)
        for m in LINK_RE.finditer(text):
            target = m.group(1)
            if target.startswith(SKIP_SCHEMES):
                continue
            checked += 1
            path_part, _, frag = target.partition("#")
            path_part = unquote(path_part)
            dest = md if path_part == "" else (md.parent / path_part).resolve()
            if not dest.exists():
                broken.append(f"{md.relative_to(root)}: missing target {target}")
                continue
            if frag:
                if dest.is_dir():
                    broken.append(f"{md.relative_to(root)}: fragment on a directory {target}")
                    continue
                if dest.suffix.lower() != ".md":
                    continue
                if dest not in anchor_cache:
                    anchor_cache[dest] = anchors_of(dest)
                if unquote(frag).lower() not in anchor_cache[dest]:
                    broken.append(f"{md.relative_to(root)}: no heading for #{frag} in {dest.relative_to(root)}")
    for b in broken:
        print("BROKEN", b)
    print(f"\n{checked} relative links checked, {len(broken)} broken")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
