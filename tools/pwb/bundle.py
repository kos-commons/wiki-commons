"""Assemble a Portable Wiki Bundle from a folder of Markdown pages, and back (guidelines chapter 10).

`build_bundle` reads a vault or wiki folder written in a known dialect (Obsidian, Foam, Dendron,
Logseq, Gollum, plain Markdown with Hugo/Jekyll-style frontmatter), converts pages to the portable
profile, relocates attachments under attachments/ with sidecar metadata, maps frontmatter to
Portable Page Metadata, optionally replays git history into history/*.jsonl, and writes the
manifest and checksums. `unbundle` writes a bundle back out as a folder in a chosen dialect.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import mimetypes
import posixpath
import re
import shutil
import uuid
from pathlib import Path
from typing import Optional

import yaml  # type: ignore

from . import __version__, history as githistory, markup
from .resolve import Page, PageIndex, strip_md

EXCLUDE_DIRS = {".git", ".obsidian", ".trash", ".logseq", "logseq", ".foam", ".dendron.cache", ".vscode",
                "node_modules", "__pycache__", ".github", "book", "_site", "public", "bak", "version-files"}
LOGSEQ_PROP_RE = re.compile(r"^([A-Za-z][\w-]*)::[ \t]*(.*)$")
H1_RE = re.compile(r"^#[ \t]+(.+?)[ \t]*#*[ \t]*$", re.M)
STATUS_FROM_OKF = {"draft": "draft", "stable": "stable", "deprecated": "deprecated"}
NAMESPACE = uuid.UUID("6b1a0d0e-9c3f-4d2a-8f6e-5a7b9c1d2e3f")


# --------------------------------------------------------------------------- small helpers
def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def iso_from_epoch_ms(value) -> Optional[str]:
    try:
        v = float(value)
    except (TypeError, ValueError):
        return None
    if v > 1e11:  # milliseconds
        v /= 1000.0
    return dt.datetime.fromtimestamp(v, dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def to_iso(value) -> Optional[str]:
    """Coerce YAML dates/datetimes/numbers/strings to an RFC 3339 string."""
    if value is None:
        return None
    if isinstance(value, dt.datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=dt.timezone.utc)
        return value.isoformat().replace("+00:00", "Z")
    if isinstance(value, dt.date):
        return value.isoformat()
    if isinstance(value, (int, float)):
        return iso_from_epoch_ms(value)
    s = str(value).strip()
    if s.isdigit():
        return iso_from_epoch_ms(s)
    return s


def as_list(value, split_spaces: bool = False) -> list:
    """Coerce a scalar or list to a list of strings; strings split on commas (and on spaces when asked and no comma is present)."""
    if value is None:
        return []
    if isinstance(value, str):
        if "," in value or not split_spaces:
            parts = value.split(",")
        else:
            parts = re.split(r"\s+", value)
        return [v.strip() for v in parts if v.strip()]
    if isinstance(value, (list, tuple)):
        return [str(v) for v in value if v is not None]
    return [str(value)]


def dump_frontmatter(fm: dict) -> str:
    text = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, width=1000, default_flow_style=False)
    return "---\n" + text + "---\n"


def write_page(path: Path, fm: dict, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    body = body.lstrip("\n")
    if body and not body.endswith("\n"):
        body += "\n"
    path.write_text(dump_frontmatter(fm) + ("\n" + body if body else ""), encoding="utf-8")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def attachment_meta(src_file: Path, filename: str, *, alt: Optional[str] = None, license: Optional[str] = None) -> dict:
    media, _ = mimetypes.guess_type(filename)
    meta = {"filename": posixpath.basename(filename), "media_type": media or "application/octet-stream",
            "sha256": sha256_file(src_file), "size": src_file.stat().st_size}
    if alt:
        meta["alt"] = alt
    if license:
        meta["license"] = license
    return meta


def write_checksums(out: Path) -> None:
    lines = []
    for f in sorted(out.rglob("*")):
        if f.is_file() and f.name not in ("sha256sums.txt", "wiki-bundle.yaml"):
            lines.append(f"{sha256_file(f)}  {f.relative_to(out).as_posix()}")
    (out / "sha256sums.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def default_manifest(*, name: str, engine: str, lang: str = "en", license: Optional[str] = None,
                     url: Optional[str] = None, native_format: Optional[str] = None,
                     native_separator: str = "/", label_order: str = "target-first") -> dict:
    m = {
        "format": "portable-wiki-bundle", "version": "0.1",
        "generator": {"name": "wiki-commons-tools", "version": __version__,
                      "url": "https://github.com/kos-commons/wiki-commons"},
        "exported_at": now_iso(),
        "source": {"name": name, "engine": engine},
        "lang": lang,
        "visibility_default": "public",
        "markup": {"profile": "portable-wiki-markdown/2", "link_label_order": "target-first",
                   "hierarchy_separator": "/", "native_hierarchy_separator": native_separator,
                   "heading_anchor_algorithm": "github", "directives": [], "html_subset": []},
        "contents": {"pages": 0, "attachments": 0, "history": False, "discussions": False, "users": False, "structured": False},
        "fidelity": {"level": 2, "degraded": [], "dropped": []},
        "checksums": "sha256sums.txt",
    }
    if url:
        m["source"]["url"] = url
    if license:
        m["license"] = license
    if native_format:
        m["markup"]["native_format"] = native_format
    if label_order != "target-first":
        m["markup"]["native_link_label_order"] = label_order
    return m


def read_manifest(bundle: Path) -> dict:
    p = bundle / "wiki-bundle.yaml"
    return yaml.safe_load(p.read_text(encoding="utf-8")) if p.exists() else {}


# --------------------------------------------------------------------------- frontmatter mapping
def logseq_properties(body: str) -> tuple[dict, str]:
    """Split leading `key:: value` lines (Logseq page properties) from the body."""
    props: dict = {}
    lines = body.split("\n")
    i = 0
    while i < len(lines):
        m = LOGSEQ_PROP_RE.match(lines[i])
        if not m:
            break
        props[m.group(1).lower()] = m.group(2).strip()
        i += 1
    return props, "\n".join(lines[i:])


def map_frontmatter_in(fm: Optional[dict], *, dialect: str, rel: str, body: str) -> tuple[dict, str]:
    """Map a source dialect's frontmatter (and Logseq page properties) to Portable Page Metadata.

    Returns (portable frontmatter, body) because Logseq properties are removed from the body.
    """
    fm = dict(fm or {})
    if dialect == "logseq":
        props, body = logseq_properties(body)
        fm.update(props)
    out: dict = {}
    ext: dict = {}
    stem = strip_md(posixpath.basename(rel))
    title = fm.pop("title", None)
    if not title:
        m = H1_RE.search(markup.mask_code(body))
        if m and dialect != "logseq":
            title = markup.HEADING_RE.match(m.group(0)).group(2) if markup.HEADING_RE.match(m.group(0)) else m.group(1)
            title = re.sub(r"[*_`]", "", title).strip()
    if not title:
        title = stem.replace("_", " ") if dialect in ("logseq", "gollum") else stem
        if dialect == "dendron":
            title = stem.rsplit(".", 1)[-1].replace("-", " ").title()
    out["title"] = str(title)
    if "id" in fm:
        out["id"] = str(fm.pop("id"))
    aliases = as_list(fm.pop("aliases", None)) + as_list(fm.pop("alias", None))
    if aliases:
        out["aliases"] = aliases
    tags = (as_list(fm.pop("tags", None), True) + as_list(fm.pop("tag", None), True)
            + as_list(fm.pop("categories", None), True) + as_list(fm.pop("category", None), True))
    if tags:
        out["tags"] = list(dict.fromkeys(tags))
    for key in ("description", "desc", "summary"):
        if key in fm and "description" not in out:
            out["description"] = str(fm.pop(key))
        else:
            fm.pop(key, None)
    created = fm.pop("created", None)
    if created is None:
        created = fm.pop("date", None)
    updated = fm.pop("updated", None)
    if updated is None:
        updated = fm.pop("lastmod", None)
    if updated is None:
        updated = fm.pop("modified", None)
    if created is not None:
        out["created"] = to_iso(created)
    if updated is not None:
        out["updated"] = to_iso(updated)
    if "lang" in fm:
        out["lang"] = str(fm.pop("lang"))
    elif "language" in fm:
        out["lang"] = str(fm.pop("language"))
    if fm.pop("draft", False) is True or fm.pop("stub", False) is True:
        out["status"] = "draft"
    if "status" in fm:
        out["status"] = str(fm.pop("status"))
    if "public" in fm:
        val = fm.pop("public")
        out["visibility"] = "public" if str(val).lower() in ("true", "yes", "1") else "internal"
    if "license" in fm:
        out["license"] = str(fm.pop("license"))
    for key in ("cssclasses", "cssclass", "publish", "cover", "image"):
        if key in fm:
            ext.setdefault("obsidian", {})[key] = fm.pop(key)
    for key in ("permalink", "slug", "layout", "weight", "nav_order", "parent", "children", "uri", "data", "custom"):
        if key in fm:
            ext.setdefault("site" if key in ("permalink", "slug", "layout", "weight") else "dendron", {})[key] = fm.pop(key)
    if "filters" in fm or "icon" in fm or "template" in fm:
        for key in ("filters", "icon", "template", "template-including-parent", "exclude-from-graph-view"):
            if key in fm:
                ext.setdefault("logseq", {})[key] = fm.pop(key)
    # everything else: known portable keys pass through, unknown keys are preserved
    for key, value in list(fm.items()):
        out[key] = value
    if ext:
        out.setdefault("ext", {}).update(ext)
    return order_keys(out), body


def order_keys(fm: dict) -> dict:
    """Stable, readable key order: identity first, engine-specific data last."""
    first = [k for k in ("id", "title", "aliases", "tags", "kind", "lang") if k in fm]
    last = [k for k in ("properties", "ext") if k in fm]
    middle = [k for k in fm if k not in first and k not in last]
    return {k: fm[k] for k in first + middle + last}


def map_frontmatter_out(fm: dict, dialect: str) -> dict:
    """Map Portable Page Metadata to a destination dialect's frontmatter."""
    fm = dict(fm)
    if dialect in ("obsidian", "foam", "portable", "gollum"):
        return fm
    if dialect == "dendron":
        out = {"id": fm.pop("id", None) or uuid.uuid4().hex[:23], "title": fm.pop("title", "")}
        if "description" in fm:
            out["desc"] = fm.pop("description")
        for key in ("created", "updated"):
            if key in fm:
                try:
                    d = dt.datetime.fromisoformat(str(fm[key]).replace("Z", "+00:00"))
                    out[key] = int(d.timestamp() * 1000)
                except ValueError:
                    out[key] = fm[key]
                fm.pop(key)
        out.update(fm)
        return out
    if dialect == "static":
        out = {"title": fm.pop("title", "")}
        if "created" in fm:
            out["date"] = fm.pop("created")
        if "updated" in fm:
            out["lastmod"] = fm.pop("updated")
        if "description" in fm:
            out["description"] = fm.pop("description")
        if "tags" in fm:
            out["tags"] = fm.pop("tags")
        if "aliases" in fm:
            out["aliases"] = fm.pop("aliases")
        if fm.get("status") in ("draft", "wip"):
            out["draft"] = True
        for key in ("id", "lang", "license"):
            if key in fm:
                out[key] = fm.pop(key)
        return out
    return fm


def logseq_property_block(fm: dict) -> str:
    """Logseq page properties: title, alias, tags, public, and free-form `properties` entries."""
    lines = []
    if fm.get("title"):
        lines.append(f"title:: {fm['title']}")
    if fm.get("aliases"):
        lines.append("alias:: " + ", ".join(str(v) for v in as_list(fm["aliases"])))
    if fm.get("tags"):
        lines.append("tags:: " + ", ".join(str(v) for v in as_list(fm["tags"])))
    if fm.get("visibility") == "public":
        lines.append("public:: true")
    if fm.get("description"):
        lines.append(f"description:: {fm['description']}")
    for key, value in (fm.get("properties") or {}).items():
        if isinstance(value, (list, tuple)):
            value = ", ".join(str(v) for v in value)
        if not isinstance(value, dict):
            lines.append(f"{key}:: {value}")
    return "\n".join(lines) + ("\n\n" if lines else "")


# --------------------------------------------------------------------------- reading a folder
def iter_files(src: Path):
    for p in sorted(src.rglob("*")):
        if not p.is_file():
            continue
        parts = p.relative_to(src).parts
        if any(part in EXCLUDE_DIRS or (part.startswith(".") and part not in (".", "..")) for part in parts[:-1]):
            continue
        if parts[-1].startswith(".") or parts[-1] in ("wiki-bundle.yaml", "sha256sums.txt"):
            continue
        if len(parts) == 1 and parts[-1] in ("import-report.md", "export-report.md"):
            continue  # conversion reports written by the tooling are not content
        yield p


def logseq_block_index(pages: list[tuple[str, str, str]]) -> dict:
    """Map Logseq block UUIDs to page titles from `id::` lines."""
    index: dict = {}
    for rel, title, body in pages:
        for m in markup.LOGSEQ_ID_LINE_RE.finditer(body):
            index[m.group(1)] = title
    return index


def stable_id(name: str, rel: str) -> str:
    return str(uuid.uuid5(NAMESPACE, f"{name}:{rel}"))


# --------------------------------------------------------------------------- build
def build_bundle(src: Path, out: Path, *, dialect: str = "obsidian", name: Optional[str] = None,
                 license: Optional[str] = None, lang: str = "en", history: bool = False,
                 id_mode: str = "uuid4", source_url: Optional[str] = None) -> dict:
    src = src.resolve()
    out = out.resolve()
    name = name or src.name
    if out.exists():
        shutil.rmtree(out)
    (out / "pages").mkdir(parents=True)
    notes = markup.Notes()
    files = list(iter_files(src))
    md_files = [f for f in files if f.suffix.lower() == ".md"]
    other_files = [f for f in files if f.suffix.lower() != ".md"]
    repo = githistory.git_root(src) if (history and githistory.is_git_repo(src)) else None
    if history and repo is None:
        notes.add("history requested but the source is not a git repository; no history exported")

    # first pass: frontmatter, titles, bodies
    pages = []
    for f in md_files:
        rel = f.relative_to(src).as_posix()
        text = f.read_text(encoding="utf-8")
        fm_text, body, _ = markup.split_frontmatter(text)
        fm = markup.parse_frontmatter(fm_text) if fm_text is not None else {}
        if fm and ("_error" in fm or "_raw" in fm):
            notes.add(f"{rel}: frontmatter could not be parsed and was kept as text")
            body = text
            fm = {}
        fm, body = map_frontmatter_in(fm, dialect=dialect, rel=rel, body=body)
        pages.append({"rel": rel, "fm": fm, "body": body, "new_path": "pages/" + rel})
    index = PageIndex([Page(p["new_path"], p["fm"]["title"], as_list(p["fm"].get("aliases"))) for p in pages], pages_prefix="pages")
    # attachments: map original relative path -> new path under attachments/
    attachments: dict[str, Path] = {f.relative_to(src).as_posix(): f for f in other_files}
    by_basename: dict[str, list[str]] = {}
    for rel in attachments:
        by_basename.setdefault(posixpath.basename(rel), []).append(rel)
    block_index = logseq_block_index([(p["rel"], p["fm"]["title"], p["body"]) for p in pages]) if dialect == "logseq" else None
    alt_texts: dict[str, str] = {}

    def make_rewriter(page_rel: str):
        page_dir = posixpath.dirname(page_rel)

        def rewrite(href: str, is_image: bool) -> Optional[str]:
            clean = href.split("#", 1)[0].split("?", 1)[0]
            from urllib.parse import unquote
            clean = unquote(clean)
            cand = posixpath.normpath(posixpath.join(page_dir, clean)) if not clean.startswith("/") else clean.lstrip("/")
            target = None
            if cand in attachments:
                target = cand
            elif clean in attachments:
                target = clean
            else:
                hits = by_basename.get(posixpath.basename(clean), [])
                if len(hits) == 1:
                    target = hits[0]
            if target is None:
                if is_image or not clean.lower().endswith(".md"):
                    notes.add(f"{page_rel}: reference to {href!r} not found among the folder's files")
                return None
            new_target = "attachments/" + target
            new_page_dir = posixpath.dirname("pages/" + page_rel)
            return posixpath.relpath(new_target, new_page_dir)
        return rewrite

    for p in pages:
        rewriter = make_rewriter(p["rel"])
        p["body"] = markup.convert(p["body"], dialect, "portable", link_rewriter=rewriter, block_index=block_index, notes=notes)
        for m in markup.MD_LINK_RE.finditer(markup.mask_code(p["body"])):
            if m.group(1) == "!" and m.group(2):
                alt_texts.setdefault(posixpath.basename(m.group(3)), m.group(2))
        fm = p["fm"]
        if "id" not in fm and id_mode != "none":
            fm["id"] = stable_id(name, p["rel"]) if id_mode == "stable" else str(uuid.uuid4())
        if repo is not None:
            created, updated = githistory.file_dates(repo, str(Path(src, p["rel"]).relative_to(repo)))
            fm.setdefault("created", created) if created else None
            fm.setdefault("updated", updated) if updated else None
        if "updated" not in fm:
            fm["updated"] = dt.datetime.fromtimestamp((src / p["rel"]).stat().st_mtime, dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        if source_url:
            from urllib.parse import quote
            fm.setdefault("source", source_url.replace("{path}", quote(strip_md(p["rel"]))).replace("{title}", quote(fm["title"])))
        p["fm"] = order_keys({k: v for k, v in fm.items() if v is not None})

    # history
    users: dict = {}
    if repo is not None:
        (out / "history").mkdir()
        for p in pages:
            rel_in_repo = str(Path(src, p["rel"]).relative_to(repo))
            rewriter = make_rewriter(p["rel"])
            records, page_users = githistory.file_history(
                repo, rel_in_repo,
                convert=lambda t, rw=rewriter: _convert_revision(t, dialect, rw, block_index),
            )
            if records:
                users.update(page_users)
                hist_name = p["fm"].get("id") or strip_md(p["rel"]).replace("/", "__")
                (out / "history" / f"{hist_name}.jsonl").write_text(
                    "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records), encoding="utf-8")
                contributors = []
                for r in records:
                    a = r.get("author", {})
                    if a and a not in contributors:
                        contributors.append(a)
                p["fm"]["contributors"] = [{"name": a["name"], "id": a["id"]} for a in contributors]
                old_names = [strip_md(posixpath.basename(r["from"])) for r in records if r.get("type") == "rename" and r.get("from")]
                extra = [n for n in old_names if n and n != p["fm"]["title"] and n not in as_list(p["fm"].get("aliases"))]
                if extra:
                    p["fm"]["aliases"] = as_list(p["fm"].get("aliases")) + extra
                    index.add(Page(p["new_path"], p["fm"]["title"], extra))
                p["fm"] = order_keys(p["fm"])
        if users:
            (out / "users.yaml").write_text(yaml.safe_dump(list(users.values()), sort_keys=False, allow_unicode=True), encoding="utf-8")

    # write pages, attachments, indexes
    blocks: dict = {}
    for p in pages:
        write_page(out / p["new_path"], p["fm"], p["body"])
        for b in markup.scan(p["body"])["block_ids"]:
            blocks[b["id"]] = p["new_path"]
    for rel, f in attachments.items():
        dest = out / "attachments" / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, dest)
        meta = attachment_meta(f, rel, alt=alt_texts.get(posixpath.basename(rel)), license=license)
        (out / "attachments" / (rel + ".meta.yaml")).write_text(yaml.safe_dump(meta, sort_keys=False, allow_unicode=True), encoding="utf-8")
    if blocks:
        (out / "blocks.json").write_text(json.dumps(blocks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    d = markup.DIALECTS.get(dialect, markup.DIALECTS["portable"])
    manifest = default_manifest(name=name, engine=dialect, lang=lang, license=license,
                                native_format="text/markdown; charset=UTF-8", native_separator=d.separator,
                                label_order=d.label_order)
    manifest["contents"].update({"pages": len(pages), "attachments": len(attachments),
                                 "history": repo is not None, "users": bool(users)})
    manifest["fidelity"]["level"] = 3 if repo is not None else 2
    summary: dict[str, int] = {}
    for n in notes:
        key = re.sub(r"'[^']*'|\(\([^)]*\)\)|\^\S+|\S+:(?= )", "…", n)
        summary[key] = summary.get(key, 0) + 1
    manifest["fidelity"]["degraded"] = [{"construct": k, "count": v, "how": "see tool notes"} for k, v in sorted(summary.items())]
    if dialect == "obsidian":
        manifest["fidelity"]["dropped"].append({"construct": "==highlight== and Obsidian-only syntax", "how": "kept as written; no portable equivalent"})
    (out / "wiki-bundle.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True), encoding="utf-8")
    write_checksums(out)
    return {"pages": len(pages), "attachments": len(attachments), "history": repo is not None, "notes": list(notes)}


def _convert_revision(text: str, dialect: str, rewriter, block_index) -> str:
    fm_text, body, _ = markup.split_frontmatter(text)
    fm = markup.parse_frontmatter(fm_text) if fm_text is not None else {}
    if fm and ("_error" in fm or "_raw" in fm):
        fm, body = {}, text
    fm, body = map_frontmatter_in(fm, dialect=dialect, rel="revision.md", body=body)
    body = markup.convert(body, dialect, "portable", link_rewriter=rewriter, block_index=block_index)
    return dump_frontmatter(fm) + "\n" + body.lstrip("\n")


# --------------------------------------------------------------------------- unbundle
def load_bundle_pages(bundle: Path) -> list[dict]:
    pages = []
    for f in sorted((bundle / "pages").rglob("*.md")):
        rel = f.relative_to(bundle).as_posix()
        text = f.read_text(encoding="utf-8")
        fm_text, body, _ = markup.split_frontmatter(text)
        fm = markup.parse_frontmatter(fm_text) or {}
        pages.append({"path": rel, "fm": fm, "body": body, "title": str(fm.get("title") or strip_md(posixpath.basename(rel)))})
    return pages


def bundle_index(bundle: Path, pages: Optional[list[dict]] = None) -> PageIndex:
    manifest = read_manifest(bundle)
    pages = pages if pages is not None else load_bundle_pages(bundle)
    return PageIndex([Page(p["path"], p["title"], as_list(p["fm"].get("aliases")), str(p["fm"].get("kind", "page"))) for p in pages],
                     namespaces=manifest.get("namespaces", []), interwiki=manifest.get("interwiki", {}), pages_prefix="pages")


def unbundle(bundle: Path, out: Path, *, dialect: str = "obsidian") -> dict:
    bundle = bundle.resolve()
    out = out.resolve()
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    manifest = read_manifest(bundle)
    pages = load_bundle_pages(bundle)
    index = bundle_index(bundle, pages)
    notes = markup.Notes()
    interwiki = manifest.get("interwiki", {})

    def resolver(target: str, from_path: Optional[str]):
        r = index.resolve(target, "pages/" + from_path if from_path else None)
        return (index.logical_path(r.path) + ".md", index.title_of(r.path)) if r.path else None

    for p in pages:
        new_rel = p["path"][len("pages/"):]
        page_dir = posixpath.dirname(p["path"])
        new_dir = posixpath.dirname(new_rel)

        def rewrite(href: str, is_image: bool, page_dir=page_dir, new_dir=new_dir) -> Optional[str]:
            target = posixpath.normpath(posixpath.join(page_dir, href))
            if target.startswith("attachments/"):
                return posixpath.relpath(target, new_dir) if new_dir else target
            return None

        body = markup.convert(p["body"], "portable", dialect, resolver=resolver if dialect == "static" else None,
                              from_path=new_rel, interwiki=interwiki, link_rewriter=rewrite, notes=notes)
        fm = map_frontmatter_out(p["fm"], dialect)
        dest = out / new_rel
        if dialect == "logseq":
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(logseq_property_block(fm) + body.lstrip("\n"), encoding="utf-8")
        else:
            write_page(dest, fm, body)
    att = bundle / "attachments"
    if att.exists():
        for f in att.rglob("*"):
            if f.is_file() and not f.name.endswith(".meta.yaml") and f.name != "attachments.yaml":
                dest = out / "attachments" / f.relative_to(att)
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dest)
    return {"pages": len(pages), "notes": list(notes)}
