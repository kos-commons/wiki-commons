#!/usr/bin/env python3
"""Assemble the mdBook source tree for the Wiki Commons site.

The repository keeps its chapters under guidelines/ with README.md,
CONTRIBUTING.md, CHANGELOG.md, schemas/, examples/, and tools/ beside them, and
every link between those files is relative. mdBook needs one source directory,
so this script mirrors the repository layout into book/src/ (ignored by git),
adapts the few files that need it, copies book/SUMMARY.md in, and checks that
every entry in the summary points at a file that exists.

Adaptations made while copying:
  * Example bundle pages (examples/**/pages/**/*.md) get a title heading, a
    note about their origin, and their YAML frontmatter shown as a fenced
    ``yaml`` block, because mdBook has no frontmatter support. Spaces in their
    file names become hyphens so that SUMMARY.md links stay plain.
  * An index page is generated for the example bundle directory so that links
    to the directory resolve to a page listing its files.
  * Every README.md becomes index.md and links to README.md files are rewritten
    accordingly, because mdBook renders README.md as index.html but rewrites
    links to it as README.html.

Usage:
    python3 tools/build_book.py [--out book/src]
    mdbook build book          # or: mdbook serve book --open

Exit status 1 if a summary entry points nowhere or a chapter file is missing.
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "book"
ROOT_FILES = ["README.md", "CONTRIBUTING.md", "CHANGELOG.md", "LICENSE"]
TREES = ["guidelines", "schemas", "examples"]
TOOL_FILES = ["tools/README.md", "tools/build_book.py", "tools/check_links.py", "tools/check_site.py", "tools/validate_bundle.py", "tools/wikicommons.py", "tools/wiki-commons.yaml"]
BUNDLE_REL = Path("examples/portable-wiki-bundle")
SUMMARY_LINK_RE = re.compile(r"\]\(([^)]+)\)")
REPO_URL = "https://github.com/kos-commons/wiki-commons"


def split_frontmatter(text: str) -> tuple[str | None, str]:
    if text.startswith("---\n"):
        end = re.search(r"\n---[ \t]*(\n|$)", text[3:])
        if end:
            return text[4 : 3 + end.start() + 1], text[3 + end.end() :]
    return None, text


def title_from_frontmatter(fm: str | None, fallback: str) -> str:
    if fm:
        m = re.search(r"^title:\s*(.+?)\s*$", fm, re.M)
        if m:
            return m.group(1).strip().strip('"').strip("'")
    return fallback


def book_name(path: Path) -> Path:
    """File name used inside the book: spaces become hyphens."""
    return path.with_name(path.name.replace(" ", "-"))


def adapt_example_page(src: Path, rel: Path) -> str:
    text = src.read_text(encoding="utf-8")
    fm, body = split_frontmatter(text)
    title = title_from_frontmatter(fm, src.stem)
    depth = len(rel.parent.parts)  # e.g. examples/portable-wiki-bundle/pages -> 3
    to_root = "../" * depth
    out = [f"# {title}", ""]
    out.append(
        f"> Rendered from [`{rel.as_posix()}`]({REPO_URL}/blob/main/{rel.as_posix().replace(' ', '%20')}) "
        f"in the example bundle. Wiki-specific constructs such as `[[free links]]`, `^block-ids`, and "
        f"snapshot envelopes are shown as a plain Markdown renderer shows them; see "
        f"[Appendix D]({to_root}guidelines/appendices/D-Portable_Wiki_Bundle_Example.md)."
    )
    out.append("")
    if fm is not None:
        out += ["**Frontmatter**", "", "```yaml", fm.rstrip("\n"), "```", ""]
    out.append(body.lstrip("\n"))
    return "\n".join(out)


def generate_bundle_index(out_bundle: Path, page_links: list[tuple[str, str]]) -> None:
    files = sorted(p for p in out_bundle.rglob("*") if p.is_file() and p.name != "index.md")
    lines = [
        "# Example Portable Wiki Bundle",
        "",
        f"This is the example bundle from [`{BUNDLE_REL.as_posix()}/`]({REPO_URL}/tree/main/{BUNDLE_REL.as_posix()}) "
        "in the repository, included here so that links from the guidelines resolve and so that the pages "
        "can be read as a plain Markdown renderer shows them. "
        "[Appendix D](../../guidelines/appendices/D-Portable_Wiki_Bundle_Example.md) walks through every file; "
        "[Chapter 10](../../guidelines/10-Interchange_and_Portability.md) defines the layout.",
        "",
        "On this site the page files are renamed with hyphens instead of spaces and their frontmatter is shown "
        "as a code block; the files in the repository are the authoritative form.",
        "",
        "## Pages (rendered)",
        "",
    ]
    lines += [f"- [{title}]({href})" for title, href in page_links]
    lines += ["", "## Files", ""]
    for f in files:
        rel = f.relative_to(out_bundle).as_posix()
        if rel.startswith("pages/") and f.suffix == ".md":
            continue
        lines.append(f"- [`{rel}`]({rel})")
    lines.append("")
    (out_bundle / "index.md").write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str]) -> int:
    out = BOOK / "src"
    if "--out" in argv:
        out = Path(argv[argv.index("--out") + 1]).resolve()
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    for name in ROOT_FILES:
        shutil.copy2(ROOT / name, out / name)
    for tree in TREES:
        if tree == "examples":
            continue
        shutil.copytree(ROOT / tree, out / tree)
    (out / "tools").mkdir()
    for name in TOOL_FILES:
        shutil.copy2(ROOT / name, out / name)
    (out / "book").mkdir()
    shutil.copy2(BOOK / "README.md", out / "book" / "README.md")  # the "Building the site" page
    (out / "corpus").mkdir()
    shutil.copy2(ROOT / "corpus" / "README.md", out / "corpus" / "README.md")
    for sub in ("", "remark", "pandoc", "markdown-it"):
        (out / "converters" / sub).mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / "converters" / sub / "README.md", out / "converters" / sub / "README.md")

    # examples: copy everything, adapting Markdown pages
    page_links: list[tuple[str, str]] = []
    for src in sorted((ROOT / "examples").rglob("*")):
        if not src.is_file():
            continue
        rel = src.relative_to(ROOT)
        if src.suffix == ".md" and "pages" in rel.parts:
            dest = out / book_name(rel)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(adapt_example_page(src, rel), encoding="utf-8")
            fm, _ = split_frontmatter(src.read_text(encoding="utf-8"))
            title = title_from_frontmatter(fm, src.stem)
            page_links.append((title, dest.relative_to(out / BUNDLE_REL).as_posix()))
        else:
            dest = out / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
    generate_bundle_index(out / BUNDLE_REL, page_links)

    # README.md -> index.md, and rewrite links that point at README.md files
    for readme in list(out.rglob("README.md")):
        readme.rename(readme.with_name("index.md"))
    readme_link = re.compile(r"\]\(((?:[^)\s]*/)?)README\.md(#[^)]*)?\)")
    for md in out.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        new = readme_link.sub(lambda m: f"]({m.group(1)}index.md{m.group(2) or ''})", text)
        if new != text:
            md.write_text(new, encoding="utf-8")

    shutil.copy2(BOOK / "SUMMARY.md", out / "SUMMARY.md")

    # verify the summary
    missing = []
    summary_targets = set()
    for m in SUMMARY_LINK_RE.finditer((out / "SUMMARY.md").read_text(encoding="utf-8")):
        target = m.group(1).strip()
        if not target:
            continue
        summary_targets.add(target)
        if not (out / target).exists():
            missing.append(target)
    for t in missing:
        print(f"ERROR SUMMARY.md points at a missing file: {t}")
    unlisted = [
        p.relative_to(out).as_posix()
        for p in (out / "guidelines").rglob("*.md")
        if p.relative_to(out).as_posix() not in summary_targets
    ]
    for u in unlisted:
        print(f"WARNING guideline file not listed in SUMMARY.md: {u}")
    print(f"assembled {sum(1 for p in out.rglob('*') if p.is_file())} files into {out.relative_to(ROOT)}")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
