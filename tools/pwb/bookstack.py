"""BookStack Portable ZIP interchange (optional tooling).

BookStack's Portable ZIP is a ZIP archive holding `data.json` (one `book`, `chapter`, or `page`
tree with tags, images, and attachments) and a `files/` directory; content is Markdown or HTML
and cross-references are written `[[bsexport:<object>:<id>]]`. The format is documented in
BookStack's repository (dev/docs/portable-zip-file-format.md). The mapping used here is
described in guidelines/appendices/H-BookStack_and_MediaWiki_Alignment.md.
"""
from __future__ import annotations

import json
import posixpath
import re
import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import Optional

import yaml  # type: ignore

from . import markup
from .bundle import (as_list, attachment_meta, default_manifest, load_bundle_pages, bundle_index, order_keys,
                     read_manifest, strip_md, write_checksums, write_page)
from .external import html_to_markdown, pandoc_available

BSREF_RE = re.compile(r"\[\[bsexport:(page|chapter|book|image|attachment):(\d+)\]\]")
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp"}


def safe_name(name: str) -> str:
    name = re.sub(r"[\\/:*?\"<>|]", "-", str(name)).strip().strip(".") or "untitled"
    return name


def _tags(tags: Optional[list]) -> tuple[list[str], dict]:
    names, props = [], {}
    for t in tags or []:
        name = str(t.get("name", "")).strip()
        if not name:
            continue
        names.append(name)
        if str(t.get("value", "")).strip():
            props[name] = t["value"]
    return names, props


# --------------------------------------------------------------------------- import
def bookstack_to_bundle(src: Path, out: Path, *, name: Optional[str] = None) -> dict:
    """Import a Portable ZIP (or an extracted directory) into a Portable Wiki Bundle."""
    src, out = src.resolve(), out.resolve()
    if out.exists():
        shutil.rmtree(out)
    (out / "pages").mkdir(parents=True)
    notes = markup.Notes()
    tmp = None
    if src.is_file():
        tmp = tempfile.mkdtemp(prefix="bsexport-")
        with zipfile.ZipFile(src) as zf:
            for member in zf.infolist():
                target = Path(tmp) / member.filename
                if not str(target.resolve()).startswith(str(Path(tmp).resolve())):
                    raise ValueError(f"unsafe path in archive: {member.filename}")
            zf.extractall(tmp)
        root = Path(tmp)
    else:
        root = src
    data = json.loads((root / "data.json").read_text(encoding="utf-8"))
    files_dir = root / "files"

    pages: list[dict] = []          # collected pages: {rel, title, body, fm, images, attachments}
    titles: dict[tuple[str, int], str] = {}   # (object type, id) -> title or path
    file_refs: dict[tuple[str, int], tuple[str, str]] = {}  # (image|attachment, id) -> (file, display name)
    pandoc = pandoc_available()
    html_pages = 0

    def collect_page(page: dict, prefix: str) -> None:
        nonlocal html_pages
        title = str(page.get("name") or f"Page {page.get('id', '')}").strip()
        rel = posixpath.join(prefix, safe_name(title) + ".md") if prefix else safe_name(title) + ".md"
        body, is_html = None, False
        if page.get("markdown"):
            body = page["markdown"]
        elif page.get("html"):
            body, is_html = page["html"], True
            html_pages += 1
        else:
            body = ""
        tags, props = _tags(page.get("tags"))
        fm: dict = {"title": title}
        if page.get("id") is not None:
            fm["id"] = f"bookstack:page:{page['id']}"
            titles[("page", int(page["id"]))] = title
        if tags:
            fm["tags"] = tags
        if props:
            fm["properties"] = props
        ext = {}
        if page.get("priority") is not None:
            ext["priority"] = page["priority"]
        if ext:
            fm["ext"] = {"bookstack": ext}
        for img in page.get("images") or []:
            if img.get("id") is not None and img.get("file"):
                file_refs[("image", int(img["id"]))] = (img["file"], img.get("name") or img["file"])
        for att in page.get("attachments") or []:
            if att.get("id") is not None:
                if att.get("file"):
                    file_refs[("attachment", int(att["id"]))] = (att["file"], att.get("name") or att["file"])
                elif att.get("link"):
                    file_refs[("attachment", int(att["id"]))] = (att["link"], att.get("name") or att["link"])
        pages.append({"rel": rel, "title": title, "body": body or "", "fm": fm, "is_html": is_html})

    def collect_chapter(chapter: dict, prefix: str) -> None:
        title = str(chapter.get("name") or f"Chapter {chapter.get('id', '')}").strip()
        rel_dir = posixpath.join(prefix, safe_name(title)) if prefix else safe_name(title)
        tags, props = _tags(chapter.get("tags"))
        fm = {"title": title, "kind": "category"}
        if chapter.get("id") is not None:
            fm["id"] = f"bookstack:chapter:{chapter['id']}"
            titles[("chapter", int(chapter["id"]))] = rel_dir
        if tags:
            fm["tags"] = tags
        if props:
            fm["properties"] = props
        if chapter.get("description_html"):
            fm["description"] = re.sub(r"<[^>]+>", "", chapter["description_html"]).strip()
        fm["ext"] = {"bookstack": {"type": "chapter", "priority": chapter.get("priority")}}
        pages.append({"rel": rel_dir + ".md", "title": title, "body": "", "fm": fm})
        for p in sorted(chapter.get("pages") or [], key=lambda p: p.get("priority", 0)):
            collect_page(p, rel_dir)

    def collect_book(book: dict) -> None:
        title = str(book.get("name") or "Book").strip()
        rel_dir = safe_name(title)
        tags, props = _tags(book.get("tags"))
        fm = {"title": title, "kind": "category"}
        if book.get("id") is not None:
            fm["id"] = f"bookstack:book:{book['id']}"
            titles[("book", int(book["id"]))] = rel_dir
        if tags:
            fm["tags"] = tags
        if props:
            fm["properties"] = props
        if book.get("description_html"):
            fm["description"] = re.sub(r"<[^>]+>", "", book["description_html"]).strip()
        if book.get("cover"):
            file_refs[("cover", 0)] = (book["cover"], "cover")
            fm["ext"] = {"bookstack": {"type": "book", "cover": book["cover"]}}
        else:
            fm["ext"] = {"bookstack": {"type": "book"}}
        pages.append({"rel": rel_dir + ".md", "title": title, "body": "", "fm": fm})
        items = [("chapter", c) for c in book.get("chapters") or []] + [("page", p) for p in book.get("pages") or []]
        for kind, item in sorted(items, key=lambda kv: kv[1].get("priority", 0)):
            (collect_chapter if kind == "chapter" else collect_page)(item, rel_dir)

    if "book" in data:
        collect_book(data["book"])
    elif "chapter" in data:
        collect_chapter(data["chapter"], "")
    elif "page" in data:
        collect_page(data["page"], "")
    else:
        raise ValueError("data.json has no book, chapter, or page")

    # copy files referenced by images, attachments, and covers
    used_files: dict[str, str] = {}
    for (kind, _id), (fname, display) in file_refs.items():
        if kind == "attachment" and re.match(r"^[a-z]+://", fname):
            continue
        srcf = files_dir / fname
        if srcf.exists():
            used_files[fname] = display
        else:
            notes.add(f"referenced file {fname!r} not found in files/")
    for fname, display in used_files.items():
        dest = out / "attachments" / fname
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(files_dir / fname, dest)
        meta = attachment_meta(files_dir / fname, fname, alt=display if Path(fname).suffix.lower() in IMAGE_EXT else None)
        meta["original_filename"] = display
        (out / "attachments" / (fname + ".meta.yaml")).write_text(yaml.safe_dump(meta, sort_keys=False, allow_unicode=True), encoding="utf-8")

    # rewrite cross-references and write pages
    for p in pages:
        page_dir = posixpath.dirname("pages/" + p["rel"])

        def ref(m: re.Match) -> str:
            kind, oid = m.group(1), int(m.group(2))
            if kind in ("page", "chapter", "book"):
                target = titles.get((kind, oid))
                if target is None:
                    notes.add(f"{p['rel']}: reference to missing {kind} {oid} kept as text")
                    return f"{kind} {oid}"
                return target if kind == "page" else target  # chapter/book paths double as titles
            fname, display = file_refs.get((kind, oid), (None, None))
            if fname is None:
                notes.add(f"{p['rel']}: reference to missing {kind} {oid} kept as text")
                return f"{kind} {oid}"
            if re.match(r"^[a-z]+://", fname):
                return fname
            return posixpath.relpath("attachments/" + fname, page_dir)

        body = p["body"]
        # references inside link/image destinations (Markdown or HTML attributes) become titles or paths
        body = re.sub(r"(\]\(|href=\"|src=\"|href='|src=')\[\[bsexport:(page|chapter|book|image|attachment):(\d+)\]\]",
                      lambda m: m.group(1) + ref(type("M", (), {"group": lambda s, i: (m.group(2), m.group(3))[i - 1]})()), body)
        # bare references become free links (pages, chapters, books) or paths (files)
        body = BSREF_RE.sub(lambda m: ("[[" + ref(m) + "]]") if m.group(1) in ("page", "chapter", "book") else ref(m), body)
        if p.get("is_html"):
            converted = html_to_markdown(body) if pandoc else None
            if converted is not None:
                body = converted
            else:
                p["fm"]["format"] = "text/html; charset=UTF-8"
                notes.add(f"{p['rel']}: HTML page kept as HTML (Pandoc not available to convert it)")
        # [label](Title) links to pages become free links
        page_titles = {v for (k, _), v in titles.items() if k == "page"}
        if page_titles and not p["fm"].get("format"):
            from urllib.parse import unquote
            def wikilinkify(m):
                dest = unquote(m.group(2))
                if dest not in page_titles:
                    return m.group(0)
                return f"[[{dest}|{m.group(1)}]]" if m.group(1) and m.group(1) != dest else f"[[{dest}]]"
            body = re.sub(r"(?<!!)\[([^\]]*)\]\(([^)\s]+)\)", wikilinkify, body)
        write_page(out / "pages" / p["rel"], order_keys(p["fm"]), body)

    inst = data.get("instance") or {}
    manifest = default_manifest(name=name or next((p["title"] for p in pages), src.stem), engine="bookstack",
                                native_format="text/markdown; charset=UTF-8")
    if inst.get("version"):
        manifest["source"]["engine_version"] = str(inst["version"])
    if data.get("exported_at"):
        manifest["source"]["exported_at"] = data["exported_at"]
    manifest["contents"].update({"pages": len(pages), "attachments": len(used_files)})
    manifest["fidelity"]["level"] = 2
    manifest["fidelity"]["degraded"] = [{"construct": "books and chapters", "how": "represented as category pages with their children in subdirectories"}]
    if html_pages and not pandoc:
        manifest["fidelity"]["degraded"].append({"construct": "HTML pages", "count": html_pages, "how": "kept as HTML with format: text/html (Pandoc not available)"})
    elif html_pages:
        manifest["fidelity"]["degraded"].append({"construct": "HTML pages", "count": html_pages, "how": "converted to Markdown with Pandoc"})
    manifest["fidelity"]["dropped"] = [{"construct": "revision history", "how": "the Portable ZIP format carries none"}]
    (out / "wiki-bundle.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True), encoding="utf-8")
    write_checksums(out)
    if tmp:
        shutil.rmtree(tmp, ignore_errors=True)
    return {"pages": len(pages), "attachments": len(used_files), "pandoc": pandoc, "notes": list(notes)}


# --------------------------------------------------------------------------- export
def bundle_to_bookstack(bundle: Path, out_zip: Path, *, name: Optional[str] = None) -> dict:
    """Export a bundle as a BookStack Portable ZIP containing one book.

    Top-level directories become chapters; deeper directories are flattened into the chapter with the
    path kept in the page name; root pages become book pages.
    """
    bundle, out_zip = bundle.resolve(), out_zip.resolve()
    manifest = read_manifest(bundle)
    pages = load_bundle_pages(bundle)
    index = bundle_index(bundle, pages)
    notes = markup.Notes()
    book_name = name or (manifest.get("source") or {}).get("name") or bundle.name
    next_id = {"page": 1, "chapter": 1, "image": 1, "attachment": 1}
    page_ids: dict[str, int] = {}
    for p in pages:
        page_ids[p["path"]] = next_id["page"]; next_id["page"] += 1
    files: dict[str, Path] = {}      # name in files/ -> source path
    images: dict[str, int] = {}      # attachment rel -> image id
    attachments: dict[str, int] = {}

    def resolver(target: str, from_path: Optional[str]):
        r = index.resolve(target, from_path)
        return (r.path, index.title_of(r.path)) if r.path else None

    def register_file(att_rel: str) -> Optional[tuple[str, int]]:
        srcf = bundle / att_rel
        if not srcf.exists():
            return None
        fname = posixpath.basename(att_rel)
        if fname in files and files[fname] != srcf:
            fname = re.sub(r"[^A-Za-z0-9.]", "", att_rel.replace("/", "-"))
        files[fname] = srcf
        is_img = Path(fname).suffix.lower() in IMAGE_EXT
        table = images if is_img else attachments
        if att_rel not in table:
            key = "image" if is_img else "attachment"
            table[att_rel] = next_id[key]; next_id[key] += 1
        return fname, table[att_rel]

    book = {"name": book_name, "tags": [], "chapters": [], "pages": []}
    chapters: dict[str, dict] = {}
    category_pages = {p["path"]: p for p in pages if p["fm"].get("kind") == "category"}
    # a bundle whose root holds exactly one category page and its directory is a single book
    root_entries = {p["path"][len("pages/"):].split("/")[0] for p in pages}
    book_dir = None
    if len(root_entries) == 1:
        only = next(iter(root_entries))
        if only.endswith(".md") is False and ("pages/" + only + ".md") in category_pages:
            book_dir = only
    elif len(root_entries) == 2:
        dirs = [e for e in root_entries if not e.endswith(".md")]
        if len(dirs) == 1 and ("pages/" + dirs[0] + ".md") in category_pages and {e for e in root_entries if e.endswith(".md")} == {dirs[0] + ".md"}:
            book_dir = dirs[0]
    if book_dir:
        bp = category_pages["pages/" + book_dir + ".md"]
        book["name"] = name or bp["title"]
        if bp["fm"].get("description"):
            book["description_html"] = f"<p>{bp['fm']['description']}</p>"
        book["tags"] = [{"name": t} for t in as_list(bp["fm"].get("tags"))]
    elif manifest.get("description"):
        book["description_html"] = f"<p>{manifest['description']}</p>"
    priority = 0
    for p in pages:
        fm = p["fm"]
        if fm.get("kind") == "redirect":
            notes.add(f"{p['path']}: redirect page not exported (BookStack has no redirects)")
            continue
        rel = p["path"][len("pages/"):]
        if book_dir:
            if rel == book_dir + ".md":
                continue
            rel = rel[len(book_dir) + 1:]
        parts = rel.split("/")
        if fm.get("kind") == "category" and (bundle / "pages" / (p["path"][len("pages/"):][:-3])).is_dir():
            # a category page with a directory describes a chapter (first level) and is not a page itself
            if len(parts) == 1:
                ch = chapters.setdefault(parts[0][:-3], {"id": next_id["chapter"], "name": p["title"], "priority": len(chapters) + 1, "pages": [],
                                                          "tags": [{"name": t} for t in as_list(fm.get("tags"))]})
                if ch["id"] == next_id["chapter"]:
                    next_id["chapter"] += 1
                if fm.get("description"):
                    ch["description_html"] = f"<p>{fm['description']}</p>"
            continue
        chapter_name = parts[0] if len(parts) > 1 else None
        page_name = p["title"] if len(parts) <= 2 else "/".join(parts[1:-1]) + "/" + p["title"]
        page_dir = posixpath.dirname(p["path"])

        def rewrite(href: str, is_image: bool, page_dir=page_dir) -> Optional[str]:
            target = posixpath.normpath(posixpath.join(page_dir, href.split("#")[0]))
            if target.startswith("attachments/"):
                reg = register_file(target)
                if reg:
                    return f"[[bsexport:{'image' if target in images else 'attachment'}:{reg[1]}]]"
            return None

        body = markup.convert(p["body"], "portable", "static", resolver=resolver, from_path=p["path"],
                              interwiki=manifest.get("interwiki", {}), link_rewriter=rewrite, notes=notes, absolute_links=True)
        # static links to bundle pages -> bsexport page references
        def page_ref(m: re.Match) -> str:
            from urllib.parse import unquote
            target = unquote(m.group(2)).lstrip("/").split("#")[0]
            pid = page_ids.get(target)
            return f"[{m.group(1)}]([[bsexport:page:{pid}]])" if pid else m.group(0)
        body = re.sub(r"\[([^\]]*)\]\((/[^)\s]+\.md(?:#[^)]*)?)\)", page_ref, body)
        props = {str(k): str(v) for k, v in (fm.get("properties") or {}).items() if isinstance(v, (str, int, float))}
        tags = [{"name": t, "value": props[t]} if t in props else {"name": t} for t in as_list(fm.get("tags"))]
        tags += [{"name": k, "value": v} for k, v in props.items() if k not in as_list(fm.get("tags"))]
        priority += 1
        entry = {"id": page_ids[p["path"]], "name": page_name, "markdown": body.strip("\n") + "\n", "priority": priority, "tags": tags,
                 "images": [], "attachments": []}
        for att_rel, iid in images.items():
            if f"[[bsexport:image:{iid}]]" in body:
                fname = next(k for k, v in files.items() if v == bundle / att_rel)
                entry["images"].append({"id": iid, "name": posixpath.basename(att_rel), "file": fname, "type": "gallery"})
        for att_rel, aid in attachments.items():
            if f"[[bsexport:attachment:{aid}]]" in body:
                fname = next(k for k, v in files.items() if v == bundle / att_rel)
                entry["attachments"].append({"id": aid, "name": posixpath.basename(att_rel), "file": fname})
        if chapter_name:
            ch = chapters.setdefault(chapter_name, {"id": next_id["chapter"], "name": chapter_name, "priority": len(chapters) + 1, "pages": [], "tags": []})
            if ch["id"] == next_id["chapter"]:
                next_id["chapter"] += 1
            ch["pages"].append(entry)
        else:
            book["pages"].append(entry)
    book["chapters"] = list(chapters.values())
    data = {"instance": {"id": "wiki-commons-tools", "version": "portable-wiki-bundle"}, "book": book}
    out_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("data.json", json.dumps(data, ensure_ascii=False, indent=2))
        for fname, srcf in files.items():
            zf.write(srcf, "files/" + fname)
    return {"pages": sum(len(c["pages"]) for c in book["chapters"]) + len(book["pages"]), "chapters": len(book["chapters"]),
            "files": len(files), "notes": list(notes)}
